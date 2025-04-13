from fastapi import APIRouter, Depends, HTTPException, Path, Query, status, UploadFile, File, Form
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, and_
import httpx
import logging
import json
from datetime import datetime

from app.db.session import get_db
from app.models.paper import Paper as PaperModel, PaperStatus
from app.models.project import paper_project
from app.schemas.paper import Paper as PaperSchema
from app.services.paper import get_paper_by_id, update_paper, list_papers
from app.services.pdf_service import get_paper_pdf_url

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/projects/{project_id}/processing", response_model=List[Dict[str, Any]])
async def get_papers_for_processing(
    project_id: int = Path(..., description="Filter by project ID"),
    db: Session = Depends(get_db),
    skip: int = Query(0, description="Number of papers to skip"),
    limit: int = Query(100, description="Maximum number of papers to return"),
    search: Optional[str] = Query(None, description="Search term"),
    sort_by: Optional[str] = Query("title", description="Sort field (title, date_added, journal)"),
    sort_desc: bool = Query(False, description="Sort in descending order")
):
    """
    Get papers within a specific project that need processing (status='processing').
    """
    query = db.query(PaperModel)\
              .join(paper_project)\
              .filter(paper_project.c.project_id == project_id)\
              .filter(PaperModel.status == PaperStatus.PROCESSING) # Filter by status

    # Apply search filter if specified
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                PaperModel.title.ilike(search_term),
                PaperModel.journal.ilike(search_term),
                # Add author search if needed
            )
        )

    # Apply sorting (adjust fields as needed)
    sort_column = PaperModel.title
    if sort_by == "date_added":
         # Assuming 'created_at' reflects when it was added/imported
         sort_column = PaperModel.created_at
    elif sort_by == "journal":
         sort_column = PaperModel.journal

    if sort_desc:
        query = query.order_by(sort_column.desc())
    else:
        query = query.order_by(sort_column)

    # Apply pagination
    papers = query.offset(skip).limit(limit).all()

    # Process results (similar to existing code, but simplify status logic)
    processed_papers = []
    for paper in papers:
         # Format authors
         author_list = paper.authors if isinstance(paper.authors, list) else json.loads(paper.authors or '[]')
         formatted_authors = [a.get("name", "Unknown") for a in author_list] if author_list else []

         # Check PDF status (based on open_access_url OR file_path)
         pdf_status = "available" if (paper.open_access_url or paper.file_path) else "missing"

         processed_paper = {
             "id": paper.id,
             "title": paper.title,
             "authors": formatted_authors,
             "journal": paper.journal or "",
             "year": paper.publication_date.year if paper.publication_date else None,
             "doi": paper.doi,
             "pdfStatus": pdf_status,
             "status": paper.status.value, # Return current status
             # Add other relevant fields like abstract snippet?
         }
         processed_papers.append(processed_paper)

    return processed_papers


@router.put("/papers/{paper_id}/update-metadata", response_model=PaperSchema)
async def update_paper_metadata(
    paper_id: int = Path(..., description="The ID of the paper to update"),
    title: Optional[str] = Form(None, description="Paper title"),
    journal: Optional[str] = Form(None, description="Journal name"),
    year: Optional[int] = Form(None, description="Publication year"),
    authors: Optional[str] = Form(None, description="Author names (JSON format)"),
    db: Session = Depends(get_db)
):
    """
    Update basic metadata for a paper.
    """
    paper = get_paper_by_id(db, paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    update_data = {}
    
    if title:
        update_data["title"] = title
    
    if journal:
        update_data["journal"] = journal
    
    if year:
        # Convert year to datetime
        if paper.publication_date:
            # Keep the month and day, update the year
            new_date = paper.publication_date.replace(year=year)
        else:
            # Create a new date with January 1st of the specified year
            new_date = datetime(year=year, month=1, day=1)
        
        update_data["publication_date"] = new_date
    
    if authors:
        try:
            # Parse authors from JSON
            authors_list = json.loads(authors)
            update_data["authors"] = authors_list
        except json.JSONDecodeError:
            raise HTTPException(status_code=400, detail="Invalid authors JSON format")
    
    # Update the paper
    updated_paper = update_paper(db, paper_id, update_data)
    
    return updated_paper


@router.get("/papers/find-duplicates", response_model=List[Dict[str, Any]])
async def find_duplicate_papers(
    db: Session = Depends(get_db),
    project_id: Optional[int] = Query(None, description="Filter by project ID")
):
    """
    Find potential duplicate papers using title similarity.
    Returns groups of papers that might be duplicates.
    """
    # Query to find papers with identical titles
    subquery = db.query(
        PaperModel.title, 
        func.count(PaperModel.id).label('count')
    )
    
    # Apply project filter if specified
    if project_id:
        subquery = subquery.filter(PaperModel.projects.any(id=project_id))
    
    subquery = subquery.group_by(
        PaperModel.title
    ).having(
        func.count(PaperModel.id) > 1
    ).subquery()
    
    # Get all papers with duplicate titles
    query = db.query(PaperModel).join(
        subquery, 
        PaperModel.title == subquery.c.title
    )
    
    # Apply project filter again to the main query
    if project_id:
        query = query.filter(PaperModel.projects.any(id=project_id))
    
    duplicate_papers = query.all()
    
    # Group by title
    duplicate_groups = {}
    for paper in duplicate_papers:
        if paper.title not in duplicate_groups:
            duplicate_groups[paper.title] = []
        
        # Format authors
        author_list = paper.authors if isinstance(paper.authors, list) else json.loads(paper.authors)
        formatted_authors = [a["name"] for a in author_list] if author_list else []
        
        duplicate_groups[paper.title].append({
            "id": paper.id,
            "title": paper.title,
            "authors": formatted_authors,
            "journal": paper.journal or "",
            "year": paper.publication_date.year if paper.publication_date else None,
            "doi": paper.doi
        })
    
    # Convert to list of duplicate groups
    result = []
    for title, papers in duplicate_groups.items():
        result.append({
            "title": title,
            "papers": papers
        })
    
    return result


@router.post("/papers/{paper_id}/retrieve-pdf", response_model=Dict[str, Any])
async def retrieve_pdf_for_paper(
    paper_id: int = Path(..., description="The ID of the paper to retrieve PDF for"),
    db: Session = Depends(get_db)
):
    """
    Attempt to retrieve a PDF for a paper using its DOI.
    Also updates paper status to READY_TO_CODE if successful.
    """
    paper = get_paper_by_id(db, paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    if not paper.doi:
        raise HTTPException(status_code=400, detail="Paper does not have a DOI")
    
    try:
        pdf_url = await get_paper_pdf_url(paper.doi)
        
        if pdf_url:
            # Update the paper with the PDF URL AND status to ready_to_code
            update_data = {
                "open_access_url": pdf_url,
                "status": PaperStatus.READY_TO_CODE
            }
            update_paper(db, paper_id, update_data)
            
            return {
                "success": True,
                "pdf_url": pdf_url,
                "message": "PDF URL retrieved and paper ready for coding"
            }
        else:
            return {
                "success": False,
                "message": "No open access PDF found for this paper"
            }
    except Exception as e:
        logger.error(f"Error retrieving PDF for paper {paper_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving PDF: {str(e)}")


# Add a new endpoint to manually mark a paper as ready for coding
@router.put("/papers/{paper_id}/mark-ready", response_model=PaperSchema)
async def mark_paper_ready_for_coding(
    paper_id: int = Path(..., description="The ID of the paper to mark as ready"),
    db: Session = Depends(get_db)
):
    """
    Manually mark a paper as ready for coding.
    Use this when PDF is manually confirmed or not relevant for coding.
    """
    paper = get_paper_by_id(db, paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")

    if paper.status == PaperStatus.PROCESSING:
        updated_paper = update_paper(db, paper_id, {"status": PaperStatus.READY_TO_CODE})
        return updated_paper
    else:
        # Return current paper if status is not PROCESSING
        return paper
