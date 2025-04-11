from fastapi import APIRouter, Depends, HTTPException, Query, Path, status, UploadFile, File, Form, BackgroundTasks
from typing import List, Optional, Dict, Any
from sqlalchemy.orm import Session
import httpx
import json
import csv
import logging
from io import StringIO

logger = logging.getLogger(__name__)

from app.schemas.paper import Paper, PaperCreate, PaperSearch
from app.services.paper_provider import get_paper_access, get_doi_for_paper, get_dois_for_papers, get_paper_pdf_url, process_csv_for_dois, process_csv_for_pdfs
from app.services.paper import create_paper, get_paper_by_id, update_paper, delete_paper, list_papers
from app.services.pdf_service import get_paper_pdf_url, get_paper_details
from app.services.doi_service import get_doi_for_paper, get_dois_for_papers
from app.services.openalex_search import search_papers_openalex
from app.db.session import get_db

router = APIRouter()


@router.get("/test-search")
async def test_search(query: str = Query(..., description="Search query")):
    """
    Simple test search endpoint.
    """
    try:
        # Use OpenAlex search with minimal parameters
        results, total_count = await search_papers_openalex(query=query, limit=5)
        
        return {
            "results": results,
            "totalResults": total_count,
            "metadata": {
                "query": query
            }
        }
    except Exception as e:
        logger.error(f"Error in test search: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/search")
async def search_papers(
    query: str = Query(..., description="Search query"),
    limit: int = Query(100, description="Number of results to return"),
    offset: int = Query(0, description="Number of results to skip"),
    year_from: Optional[int] = Query(None, description="Filter from year"),
    year_to: Optional[int] = Query(None, description="Filter to year"),
    journal: Optional[str] = Query(None, description="Filter by journal"),
    author: Optional[str] = Query(None, description="Filter by author"),
    open_access_only: bool = Query(False, description="Filter to open access only"),
    sort_by: str = Query("relevance", description="Sort results by"),
    providers: Optional[str] = Query(None, description="Parameter kept for backwards compatibility"),
    client_pagination: Optional[bool] = Query(None, description="Whether to use client-side pagination"),
    db: Session = Depends(get_db),
):
    """
    Search for papers using OpenAlex via PyAlex.
    """
    try:
        # Use OpenAlex search
        results, total_count = await search_papers_openalex(
            query=query, 
            limit=limit,
            offset=offset,
            year_from=year_from,
            year_to=year_to,
            journal=journal,
            author=author,
            open_access_only=open_access_only,
            sort=sort_by,
            fetch_all=client_pagination
        )
        
        return {
            "results": results,
            "totalResults": total_count,
            "metadata": {
                "query": query,
                "filters": {
                    "yearFrom": year_from,
                    "yearTo": year_to,
                    "journal": journal,
                    "author": author,
                    "openAccessOnly": open_access_only,
                    "providers": ["openalex"]
                },
                "sortBy": sort_by
            }
        }
    except httpx.HTTPError as e:
        logger.error(f"HTTP error during paper search: {e}")
        raise HTTPException(status_code=502, detail=f"Error connecting to external API: {str(e)}")
    except httpx.TimeoutException as e:
        logger.error(f"Timeout during paper search: {e}")
        raise HTTPException(status_code=504, detail="External API request timed out")
    except ValueError as e:
        logger.error(f"Value error during paper search: {e}")
        raise HTTPException(status_code=400, detail=f"Invalid request parameters: {str(e)}")
    except Exception as e:
        logger.error(f"Unexpected error during paper search: {e}")
        # More descriptive error when using object notation
        error_msg = str(e)
        if isinstance(e, object) and not error_msg:
            error_msg = f"Error of type {type(e).__name__}"
        raise HTTPException(status_code=500, detail=error_msg)


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
    """
    try:
        details = await get_paper_details(doi)
        return details
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving paper details: {str(e)}")


@router.post("/find-doi", response_model=Dict[str, Any])
async def find_paper_doi(
    title: str = Form(...),
    author: str = Form(...),
    year: str = Form(...),
):
    """
    Find DOI for a paper based on title, author and year.
    """
    try:
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
        raise HTTPException(status_code=500, detail=f"Error finding DOI: {str(e)}")


@router.post("/batch-find-doi", response_model=List[Dict[str, Any]])
async def batch_find_dois(
    file: UploadFile = File(...),
    background_tasks: BackgroundTasks = None,
):
    """
    Find DOIs for multiple papers from a CSV file.
    The CSV should have columns: title, authors, year
    """
    try:
        # Read the CSV file
        content = await file.read()
        text_content = content.decode("utf-8-sig")
        
        # Process the CSV for DOIs
        results = await process_csv_for_dois(text_content)
        
        # Add PDF URLs to papers with DOIs
        results_with_pdf = await process_csv_for_pdfs(results)
        
        return results_with_pdf
    
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error processing CSV file: {str(e)}")


@router.get("/advanced-search", response_model=Dict[str, Any])
async def advanced_search_papers(
    query: str = Query(..., description="Search query"),
    limit: int = Query(100, description="Number of results to return"),
    offset: int = Query(0, description="Number of results to skip"),
    open_access_only: bool = Query(False, description="Filter to open access only"),
    year_from: Optional[int] = Query(None, description="Filter from year"),
    year_to: Optional[int] = Query(None, description="Filter to year"),
    journal: Optional[str] = Query(None, description="Filter by journal"),
    author: Optional[str] = Query(None, description="Filter by author"),
    providers: Optional[str] = Query(None, description="Parameter kept for backwards compatibility"),
    sort_by: str = Query("relevance", description="Sort results by"),
    client_pagination: Optional[bool] = Query(None, description="Whether to use client-side pagination"),
):
    """
    Advanced search for papers using OpenAlex via direct API calls.
    """
    try:
        # Log the received parameters for debugging
        logger.info(f"Advanced search parameters: query={query}, limit={limit}, offset={offset}, year_from={year_from}, "
                  f"year_to={year_to}, journal={journal}, author={author}, open_access_only={open_access_only}, "
                  f"sort_by={sort_by}, providers={providers}")

        # Use OpenAlex search
        results, total_count = await search_papers_openalex(
            query=query, 
            limit=limit,
            offset=offset,
            year_from=year_from,
            year_to=year_to,
            journal=journal,
            author=author,
            open_access_only=open_access_only,
            sort=sort_by,
            fetch_all=client_pagination
        )
        
        return {
            "results": results,
            "totalResults": total_count,
            "metadata": {
                "query": query,
                "filters": {
                    "yearFrom": year_from,
                    "yearTo": year_to,
                    "journal": journal,
                    "author": author,
                    "openAccessOnly": open_access_only,
                    "providers": ["openalex"]
                },
                "sortBy": sort_by,
                "offset": offset,
                "limit": limit
            }
        }
    
    except httpx.HTTPError as e:
        logger.error(f"HTTP error during advanced paper search: {e}")
        raise HTTPException(status_code=502, detail=f"Error connecting to external API: {str(e)}")
    except httpx.TimeoutException as e:
        logger.error(f"Timeout during advanced paper search: {e}")
        raise HTTPException(status_code=504, detail="External API request timed out")
    except Exception as e:
        logger.error(f"Error in advanced search: {str(e)}")
        error_msg = str(e)
        if isinstance(e, object) and not error_msg:
            error_msg = f"Error of type {type(e).__name__}"
        raise HTTPException(status_code=500, detail=error_msg)
