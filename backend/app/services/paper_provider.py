import requests
import time
import json
import re
import logging
import asyncio
from typing import List, Dict, Optional, Any, Union, Tuple
import unicodedata
from datetime import datetime

from app.core.config import settings
from app.services.openalex_search import search_papers_openalex

logger = logging.getLogger(__name__)

async def search_papers(query: str, limit: int = 20, offset: int = 0, 
                       year_from: Optional[int] = None, year_to: Optional[int] = None,
                       journal: Optional[str] = None, author: Optional[str] = None,
                       open_access_only: bool = False,
                       sort: Optional[str] = None) -> Tuple[List[Dict[str, Any]], int]:
    """
    Search for papers using OpenAlex API
    """
    return await search_papers_openalex(
        query=query,
        limit=limit,
        offset=offset,
        year_from=year_from,
        year_to=year_to,
        journal=journal,
        author=author,
        open_access_only=open_access_only,
        sort=sort
    )

async def get_paper_access(doi: str) -> Dict[str, Any]:
    """
    Get open access information for a paper using OpenAlex with fallback to Unpaywall.
    """
    # Import here to avoid circular imports
    from app.services.pdf_service import get_paper_details
    
    details = await get_paper_details(doi)
    
    return {
        "is_oa": details.get("is_oa", False),
        "open_access_url": details.get("pdf_url"),
        "url": details.get("url"),
        "oa_status": details.get("oa_status")
    }

def clean_author(author_string: str) -> str:
    """Clean up an author string to extract the last name of the first author"""
    # Import here to avoid circular imports
    from app.services.doi_service import clean_author as doi_clean_author
    return doi_clean_author(author_string)

async def get_doi_for_paper(title: str, author: str, year: str) -> Optional[str]:
    """
    Find DOI for a paper based on title, author, and year using OpenAlex
    """
    # Import here to avoid circular imports
    from app.services.doi_service import get_doi_for_paper as doi_get_doi
    return await doi_get_doi(title, author, year)

async def get_dois_for_papers(papers: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Find DOIs for multiple papers using OpenAlex
    
    Args:
        papers: List of dictionaries containing paper information
               Each dict should have 'title', 'authors', and 'year' keys
    
    Returns:
        The same list with DOIs added where found
    """
    # Import here to avoid circular imports
    from app.services.doi_service import get_dois_for_papers as doi_get_dois
    return await doi_get_dois(papers)

async def get_paper_pdf_url(doi: str) -> Optional[str]:
    """
    Get PDF URL for a paper if available as open access using OpenAlex with fallback to Unpaywall
    """
    # Import here to avoid circular imports
    from app.services.pdf_service import get_paper_pdf_url as pdf_get_url
    return await pdf_get_url(doi)

async def process_csv_for_dois(csv_content: str) -> List[Dict[str, Any]]:
    """
    Process a CSV file to find DOIs for papers using OpenAlex
    
    Args:
        csv_content: Content of CSV file as string
        
    Returns:
        List of paper dictionaries with DOIs
    """
    import csv
    from io import StringIO
    
    reader = csv.DictReader(StringIO(csv_content))
    papers = list(reader)
    
    # Check if required fields exist
    required_columns = ['title', 'authors', 'year']
    for paper in papers:
        if not all(key in paper for key in required_columns):
            logger.error(f"CSV must contain 'title', 'authors', and 'year' columns")
            raise ValueError("CSV must contain 'title', 'authors', and 'year' columns")
    
    # Find DOIs for the papers
    # Import here to avoid circular imports
    from app.services.doi_service import get_dois_for_papers as doi_get_dois
    results = await doi_get_dois(papers)
    return results

async def process_csv_for_pdfs(papers_with_doi: List[Dict[str, Any]]) -> List[Dict[str, Any]]:
    """
    Process papers with DOIs to find PDF URLs using OpenAlex with fallback to Unpaywall
    
    Args:
        papers_with_doi: List of paper dictionaries with DOIs
        
    Returns:
        List of paper dictionaries with PDF URLs
    """
    results = []
    
    for paper in papers_with_doi:
        doi = paper.get('doi')
        if doi and doi != "Not found":
            # Import here to avoid circular imports
            from app.services.pdf_service import get_paper_pdf_url as pdf_get_url
            pdf_url = await pdf_get_url(doi)
            paper['pdf_url'] = pdf_url if pdf_url else "Not found"
        else:
            paper['pdf_url'] = "No DOI"
        
        results.append(paper)
        
        # Add a small delay to avoid rate limiting
        await asyncio.sleep(0.5)
    
    return results
