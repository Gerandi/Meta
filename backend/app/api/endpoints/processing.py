from fastapi import APIRouter, Depends, HTTPException, Path, Query, status, UploadFile, File, Form
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, or_, and_
import httpx
import logging
import json
from datetime import datetime

from app.db.session import get_db
from app.models.paper import Paper as PaperModel
from app.schemas.paper import Paper as PaperSchema
from app.services.paper import get_paper_by_id, update_paper, list_papers
from app.services.pdf_service import get_paper_pdf_url

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/papers/cleanup", response_model=List[Dict[str, Any]])
async def get_papers_for_processing(
    db: Session = Depends(get_db),
    skip: int = Query(0, description="Number of papers to skip"),
    limit: int = Query(100, description="Maximum number of papers to return"),
    collection_id: Optional[int] = Query(None, description="Filter by collection ID"),
    filter_type: Optional[str] = Query(None, description="Filter by type (all, duplicates, incomplete, flagged)"),
    search: Optional[str] = Query(None, description="Search term"),
    sort_by: Optional[str] = Query("title", description="Sort field (title, author, year, journal)"),
    sort_desc: bool = Query(False, description="Sort in descending order")
):
    """
    Get papers for processing with various filtering options.
    """
    # Start with a base query
    query = db.query(PaperModel)
    
    # Apply collection filter if specified
    if collection_id:
        query = query.filter(PaperModel.collections.any(id=collection_id))
    
    # Apply search filter if specified
    if search:
        search_term = f"%{search}%"
        query = query.filter(
            or_(
                PaperModel.title.ilike(search_term),
                PaperModel.journal.ilike(search_term),
                PaperModel.abstract.ilike(search_term)
            )
        )
    
    # Apply type-based filters
    if filter_type:
        if filter_type == "duplicates":
            # Subquery to find papers with similar titles
            subquery = db.query(
                PaperModel.title, 
                func.count(PaperModel.id).label('count')
            ).group_by(
                PaperModel.title
            ).having(
                func.count(PaperModel.id) > 1
            ).subquery()
            
            query = query.join(
                subquery, 
                PaperModel.title == subquery.c.title
            )
        elif filter_type == "incomplete":
            # Papers with missing metadata
            query = query.filter(
                or_(
                    PaperModel.journal == None,
                    PaperModel.journal == "",
                    PaperModel.publication_date == None,
                    PaperModel.abstract == None,
                    PaperModel.abstract == "",
                    PaperModel.authors == "{}"
                )
            )
    
    # Apply sorting
    if sort_by == "title":
        if sort_desc:
            query = query.order_by(PaperModel.title.desc())
        else:
            query = query.order_by(PaperModel.title)
    elif sort_by == "year":
        if sort_desc:
            query = query.order_by(PaperModel.publication_date.desc())
        else:
            query = query.order_by(PaperModel.publication_date)
    elif sort_by == "journal":
        if sort_desc:
            query = query.order_by(PaperModel.journal.desc())
        else:
            query = query.order_by(PaperModel.journal)
    
    # Apply pagination
    papers = query.offset(skip).limit(limit).all()
    
    # Process the results to include status information
    processed_papers = []
    for paper in papers:
        # Check paper status
        status = "clean"
        flagged_reason = None
        
        # Check for duplicate
        duplicate_check = db.query(PaperModel).filter(
            and_(
                PaperModel.title == paper.title,
                PaperModel.id != paper.id
            )
        ).first()
        
        if duplicate_check:
            status = "duplicate"
            flagged_reason = f"Potential duplicate of paper ID {duplicate_check.id}"
        
        # Check for incomplete metadata
        elif (not paper.journal or not paper.publication_date or not paper.abstract 
              or not paper.authors or paper.authors == "[]"):
            status = "incomplete"
            missing = []
            if not paper.journal or paper.journal == "":
                missing.append("journal")
            if not paper.publication_date:
                missing.append("publication date")
            if not paper.abstract or paper.abstract == "":
                missing.append("abstract")
            if not paper.authors or paper.authors == "[]":
                missing.append("authors")
            
            flagged_reason = f"Missing metadata: {', '.join(missing)}"
        
        # Format authors
        author_list = paper.authors if isinstance(paper.authors, list) else json.loads(paper.authors)
        formatted_authors = [a["name"] for a in author_list] if author_list else []
        
        # Check PDF status
        pdf_status = "available" if paper.open_access_url else "missing"
        
        processed_paper = {
            "id": paper.id,
            "title": paper.title,
            "authors": formatted_authors,
            "journal": paper.journal or "",
            "year": paper.publication_date.year if paper.publication_date else None,
            "doi": paper.doi,
            "pdfStatus": pdf_status,
            "status": status,
            "flagged": flagged_reason
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
    collection_id: Optional[int] = Query(None, description="Filter by collection ID")
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
    
    # Apply collection filter if specified
    if collection_id:
        subquery = subquery.filter(PaperModel.collections.any(id=collection_id))
    
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
    
    # Apply collection filter again to the main query
    if collection_id:
        query = query.filter(PaperModel.collections.any(id=collection_id))
    
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


@router.post("/papers/{paper_id}/retrieve-pdf")
async def retrieve_pdf_for_paper(
    paper_id: int = Path(..., description="The ID of the paper to retrieve PDF for"),
    db: Session = Depends(get_db)
):
    """
    Attempt to retrieve a PDF for a paper using its DOI.
    """
    paper = get_paper_by_id(db, paper_id)
    if not paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    if not paper.doi:
        raise HTTPException(status_code=400, detail="Paper does not have a DOI")
    
    try:
        pdf_url = await get_paper_pdf_url(paper.doi)
        
        if pdf_url:
            # Update the paper with the PDF URL
            update_paper(db, paper_id, {"open_access_url": pdf_url})
            
            return {
                "success": True,
                "pdf_url": pdf_url,
                "message": "PDF URL retrieved successfully"
            }
        else:
            return {
                "success": False,
                "message": "No open access PDF found for this paper"
            }
    except Exception as e:
        logger.error(f"Error retrieving PDF for paper {paper_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error retrieving PDF: {str(e)}")
