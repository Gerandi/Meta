from fastapi import APIRouter, Depends, HTTPException, Query, Path, status, UploadFile, File, Form, BackgroundTasks
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
import httpx
import json
import csv
import logging
import asyncio
from io import StringIO

logger = logging.getLogger(__name__)

from app.schemas.paper import Paper, PaperCreate # Removed PaperSearch as the endpoint is removed
# Remove paper_provider import and directly import from service modules
from app.services.paper import create_paper, get_paper_by_id, update_paper, delete_paper, list_papers
from app.services.pdf_service import get_paper_pdf_url, get_paper_details
from app.services.doi_service import get_doi_for_paper, get_dois_for_papers
# Removed import for openalex_search as it's being deprecated
from app.services.openalex_direct import search_papers_direct # Import the consolidated function
from app.db.session import get_db

router = APIRouter()

# Removed the redundant /search endpoint previously defined here
# The main search endpoint is now in app/api/endpoints/search.py



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


@router.get("/", response_model=List[Paper])
async def get_papers(
    skip: int = Query(0, description="Number of papers to skip"),
    limit: int = Query(100, description="Maximum number of papers to return"),
    db: Session = Depends(get_db),
):
    """
    Get a list of papers with pagination.
    """
    return list_papers(db, skip, limit)


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
            # Removed duplicate year_to=year,
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

# Advanced search endpoint removed - consolidated into main search endpoint
