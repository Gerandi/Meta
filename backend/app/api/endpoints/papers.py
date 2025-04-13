from fastapi import APIRouter, Depends, HTTPException, Query, Path, status, UploadFile, File, Form, BackgroundTasks
from fastapi.responses import FileResponse
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
import httpx
import json
import csv
import logging
import asyncio
import os
import uuid
from io import StringIO

logger = logging.getLogger(__name__)

from app.schemas.paper import Paper, PaperCreate
from app.services.paper import create_paper, get_paper_by_id, update_paper, delete_paper, list_papers, list_imported_papers
from app.models.paper import PaperStatus
from app.services.pdf_service import get_paper_pdf_url, get_paper_details
from app.services.doi_service import get_doi_for_paper, get_dois_for_papers
from app.services.openalex_direct import search_papers_direct
from app.services.pdf_extraction import process_pdf_file, extract_metadata_from_pdf, enhance_metadata_with_api
from app.services.project import add_paper_to_project
from app.db.session import get_db

router = APIRouter()


@router.get("/counts", response_model=Dict[str, int])
async def get_paper_counts(
    db: Session = Depends(get_db),
):
    """
    Get counts of papers by various criteria.
    """
    # Count total papers
    total_count = db.query(Paper).count()
    
    # Count papers with PDFs
    with_pdf_count = db.query(Paper).filter(Paper.file_path.isnot(None)).count()
    
    # Count papers with DOIs
    with_doi_count = db.query(Paper).filter(Paper.doi.isnot(None)).count()
    
    # Count open access papers
    open_access_count = db.query(Paper).filter(Paper.is_open_access == True).count()
    
    return {
        "total": total_count,
        "with_pdf": with_pdf_count,
        "with_doi": with_doi_count,
        "open_access": open_access_count
    }


@router.get("/cleanup", response_model=List[Paper])
async def list_papers_for_cleanup(
    skip: int = Query(0, description="Number of papers to skip"),
    limit: int = Query(100, description="Maximum number of papers to return"),
    sort_by: str = Query("title", description="Field to sort by"),
    db: Session = Depends(get_db),
):
    """
    Get a list of papers with pagination and sorting for cleanup purposes.
    """
    query = db.query(Paper)
    
    # Add sorting
    if sort_by == "title":
        query = query.order_by(Paper.title)
    elif sort_by == "date":
        query = query.order_by(Paper.publication_date.desc())
    elif sort_by == "journal":
        query = query.order_by(Paper.journal)
    
    papers = query.offset(skip).limit(limit).all()
    return papers


@router.post("/", response_model=Paper, status_code=status.HTTP_201_CREATED)
async def save_paper(
    paper: PaperCreate,
    db: Session = Depends(get_db),
):
    """
    Save a paper to the database. If a paper with the same DOI already exists,
    the existing paper will be returned.
    """
    return create_paper(db, paper)


@router.get("/{paper_id}", response_model=Paper)
async def get_paper(
    paper_id: int = Path(..., description="The ID of the paper to retrieve"),
    db: Session = Depends(get_db),
):
    """
    Get a specific paper by ID.
    """
    db_paper = get_paper_by_id(db, paper_id)
    if not db_paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    return db_paper


@router.patch("/{paper_id}", response_model=Paper)
async def update_paper_details(
    paper_id: int = Path(..., description="The ID of the paper to update"),
    paper_data: Dict[str, Any] = None,
    db: Session = Depends(get_db),
):
    """
    Update specific fields of a paper.
    """
    return update_paper(db, paper_id, paper_data)


@router.delete("/{paper_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_paper_by_id(
    paper_id: int = Path(..., description="The ID of the paper to delete"),
    db: Session = Depends(get_db),
):
    """
    Delete a paper by ID.
    """
    delete_paper(db, paper_id)
    return None


@router.get("/{paper_id}/content", response_class=FileResponse)
@router.head("/{paper_id}/content")
async def get_paper_content(
    paper_id: int = Path(..., description="The ID of the paper"),
    db: Session = Depends(get_db)
):
    """
    Get the content (PDF) of a paper stored locally.
    """
    db_paper = get_paper_by_id(db, paper_id)
    if not db_paper:
        raise HTTPException(status_code=404, detail="Paper not found")

    if not db_paper.file_path:
        raise HTTPException(status_code=404, detail="No local file associated with this paper")

    file_path = db_paper.file_path
    if not os.path.exists(file_path):
        logger.error(f"File not found at path: {file_path} for paper ID {paper_id}")
        raise HTTPException(status_code=404, detail="File not found on server")

    # Return the file
    # Extract filename for download suggestion
    filename = os.path.basename(file_path)
    # Remove potential UUID prefix for cleaner download name
    if "_" in filename and len(filename.split("_")[0]) == 36:  # Basic check for UUID prefix
        filename = "_".join(filename.split("_")[1:])

    return FileResponse(path=file_path, filename=filename, media_type='application/pdf')


@router.get("/imported", response_model=List[Paper])
async def get_imported_papers(
    skip: int = Query(0, description="Number of papers to skip"),
    limit: int = Query(100, description="Maximum number of papers to return"),
    db: Session = Depends(get_db),
):
    """
    Get papers that have been imported but not yet added to a project.
    """
    return list_imported_papers(db, skip, limit)


@router.get("/", response_model=List[Paper])
async def get_papers(
    skip: int = Query(0, description="Number of papers to skip"),
    limit: int = Query(100, description="Maximum number of papers to return"),
    status: Optional[PaperStatus] = Query(None, description="Filter by paper status"),
    project_id: Optional[int] = Query(None, description="Filter by project ID"),
    db: Session = Depends(get_db),
):
    """
    Get a list of papers with pagination and optional filters.
    """
    return list_papers(db, skip, limit, status, project_id)


@router.get("/pdf/{doi}", response_model=Dict[str, Any])
async def get_paper_pdf(
    doi: str = Path(..., description="The DOI of the paper"),
):
    """
    Get PDF URL for a paper if available as open access.
    
    Uses OpenAlex as the primary source with fallback to Unpaywall if needed.
    Returns the direct URL to the PDF when available from either source.
    """
    try:
        pdf_url = await get_paper_pdf_url(doi)
        
        if pdf_url:
            return {"pdf_url": pdf_url, "status": "success"}
        else:
            return {"pdf_url": None, "status": "not_found", "message": "No open access PDF found for this DOI"}
    
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving PDF URL: {str(e)}")


@router.get("/details/{doi}", response_model=Dict[str, Any])
async def get_detailed_paper_info(
    doi: str = Path(..., description="The DOI of the paper"),
):
    """
    Get detailed information about a paper including open access status.
    
    Retrieves comprehensive paper metadata from OpenAlex, including:
    - Publication details (journal, volume, issue)
    - Open access status and availability
    - URLs to full text when available
    - Journal open access status
    
    Falls back to Unpaywall if OpenAlex doesn't have details for the requested DOI.
    """
    try:
        details = await get_paper_details(doi)
        return details
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving paper details: {str(e)}")


@router.post("/find-doi", response_model=Dict[str, Any])
async def find_paper_doi(
    title: str = Form(..., description="Paper title"),
    author: str = Form(..., description="Author name"),
    year: str = Form(..., description="Publication year"),
):
    """
    Find DOI for a paper based on title, author and year using OpenAlex.
    
    Uses a two-step process:
    1. Search OpenAlex directly with the provided metadata
    2. Apply matching algorithms to find the most relevant paper
    
    Returns a DOI if found, along with open access URL if available.
    """
    try:
        # Use OpenAlex search directly for more control
        logger.info(f"Finding DOI for: '{title}' by {author} ({year})")
        
        # Use the consolidated direct search function
        results, count = await search_papers_direct(
            query=title,
            per_page=3,  # Get top 3 results to improve matching chances
            page=1,
            year_from=int(year) if year else None, # Ensure year is int
            year_to=int(year) if year else None,   # Ensure year is int
            author=author,
            sort="relevance"
        )
        
        if results and count > 0:
            # Get the DOI from the first result
            doi = results[0].get("doi")
            pdf_url = results[0].get("open_access_url")
            
            if doi:
                logger.info(f"Found DOI: {doi}")
                return {
                    "doi": doi, 
                    "status": "success",
                    "pdf_url": pdf_url
                }
        
        # If the direct search didn't work, try the backup method
        logger.info("Direct search failed, trying backup DOI lookup method")
        doi = await get_doi_for_paper(title, author, year)
        
        if doi:
            # Also get PDF URL if available
            pdf_url = await get_paper_pdf_url(doi)
            
            return {
                "doi": doi, 
                "status": "success",
                "pdf_url": pdf_url
            }
        else:
            return {"doi": None, "status": "not_found", "message": "DOI not found for the given paper details"}
    
    except Exception as e:
        logger.error(f"Error finding DOI: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error finding DOI: {str(e)}")


@router.post("/batch-find-doi", response_model=List[Dict[str, Any]])
async def batch_find_dois(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
):
    """
    Find DOIs for multiple papers from a CSV file using OpenAlex.
    
    The CSV file should have columns:
    - title: Paper title
    - authors: Author names (comma or 'and' separated)
    - year: Publication year
    
    The system processes each entry through OpenAlex to find matching DOIs
    and open access PDF links where available. Results maintain the original
    input data plus any found DOIs and PDF URLs.
    """
    try:
        # Read the CSV file
        content = await file.read()
        text_content = content.decode("utf-8-sig")
        
        # Process CSV content into paper dictionaries
        import csv
        from io import StringIO
        
        reader = csv.DictReader(StringIO(text_content))
        papers = list(reader)
        
        # Check if required fields exist
        required_columns = ['title', 'authors', 'year']
        for paper in papers:
            if not all(key in paper for key in required_columns):
                logger.error(f"CSV must contain 'title', 'authors', and 'year' columns")
                raise ValueError("CSV must contain 'title', 'authors', and 'year' columns")
        
        # Find DOIs for the papers
        results = await get_dois_for_papers(papers)
        
        # Add PDF URLs to papers with DOIs
        results_with_pdf = []
        
        for paper in results:
            doi = paper.get('doi')
            if doi and doi != "Not found":
                pdf_url = await get_paper_pdf_url(doi)
                paper['pdf_url'] = pdf_url if pdf_url else "Not found"
            else:
                paper['pdf_url'] = "No DOI"
            
            results_with_pdf.append(paper)
            
            # Add a small delay to avoid rate limiting
            await asyncio.sleep(0.5)
        
        return results_with_pdf
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV file: {str(e)}")


@router.post("/upload", response_model=Paper)
async def upload_pdf(
    file: UploadFile = File(...),
    project_id: Optional[int] = Query(None, description="Optional project ID to associate the file with"),
    db: Session = Depends(get_db),
):
    """
    Upload a PDF file, extract metadata, and save to database.
    
    This endpoint handles the full process of:
    1. Receiving the PDF upload
    2. Extracting metadata from the PDF
    3. Enhancing metadata with OpenAlex API
    4. Creating a Paper record in the database
    5. Associating with a project if project_id is provided
    
    Returns the created Paper object.
    """
    try:
        # Check if the file is a PDF
        if not file.filename.lower().endswith('.pdf'):
            raise HTTPException(status_code=400, detail="Uploaded file must be a PDF")
        
        # Read the file contents
        file_content = await file.read()
        
        # Process the PDF file - extract metadata and store file
        metadata = await process_pdf_file(file_content, file.filename, project_id)
        
        # Create PaperCreate object from metadata
        paper_data = {
            "title": metadata.get("title") or "Unknown Title",
            "authors": metadata.get("authors") or [],
            "doi": metadata.get("doi"),
            "abstract": metadata.get("abstract"),
            "publication_date": None,  # Will be set based on year below
            "journal": metadata.get("journal"),
            "volume": metadata.get("volume"),
            "issue": metadata.get("issue"),
            "pages": metadata.get("pages"),
            "publisher": metadata.get("publisher"),
            "url": metadata.get("url") or metadata.get("doi"),
            "keywords": metadata.get("keywords", []),
            "is_open_access": metadata.get("is_open_access", False),
            "open_access_url": metadata.get("open_access_url"),
            "source": "PDF Upload",
            "file_path": metadata.get("file_path")
        }
        
        # Set publication date based on year if available
        if metadata.get("year"):
            from datetime import datetime
            paper_data["publication_date"] = datetime(metadata["year"], 1, 1).isoformat()
        elif metadata.get("publication_date"):
            paper_data["publication_date"] = metadata["publication_date"]
            
        # Set the status from metadata or default to IMPORTED
        paper_data["status"] = metadata.get("status", PaperStatus.IMPORTED)
            
        # Create paper in database
        paper_create = PaperCreate(**paper_data)
        paper = create_paper(db, paper_create)
        
        # If project_id is provided, add paper to project
        if project_id and paper:
            add_paper_to_project(db, paper.id, project_id)
        
        return paper
    
    except HTTPException as e:
        # Re-raise HTTP exceptions
        raise
    except Exception as e:
        logger.error(f"Error processing PDF upload: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error processing PDF: {str(e)}")


@router.post("/import-batch", response_model=Dict[str, Any])
async def import_papers_batch(
    papers: List[Dict[str, Any]],
    db: Session = Depends(get_db),
):
    """
    Import multiple papers from search results.
    
    This endpoint accepts a list of paper objects and stores them in the database,
    consolidating duplicates based on DOI or title similarity.
    
    Returns:
        A dictionary containing import status, counts, and the list of successfully imported papers
        with their database IDs.
    """
    try:
        imported_count = 0
        skipped_count = 0
        errors = []
        imported_papers = []
        
        for paper_data in papers:
            try:
                # Convert the paper data to PaperCreate schema
                paper_create = PaperCreate(**paper_data)
                
                # Create or update the paper in the database
                created_paper = create_paper(db, paper_create)
                
                if created_paper:
                    # Add the successfully created/found paper to our result list
                    imported_papers.append({
                        "id": created_paper.id,
                        "title": created_paper.title,
                        "doi": created_paper.doi,
                        "authors": created_paper.authors,
                        "journal": created_paper.journal,
                        "publication_date": created_paper.publication_date
                    })
                    imported_count += 1
                else:
                    skipped_count += 1
                    
            except Exception as e:
                logger.error(f"Error importing paper: {str(e)}")
                errors.append({
                    "paper": paper_data.get("title", "Unknown title"),
                    "error": str(e)
                })
                skipped_count += 1
        
        return {
            "status": "success",
            "imported_count": imported_count,
            "skipped_count": skipped_count,
            "errors": errors,
            "imported_papers": imported_papers
        }
    
    except Exception as e:
        logger.error(f"Error in batch import: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error importing papers: {str(e)}")
