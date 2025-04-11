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
from app.services.api_client import get_crossref_data, get_unpaywall_data

logger = logging.getLogger(__name__)

async def search_papers_crossref(query: str, limit: int = 20, offset: int = 0, 
                                year_from: Optional[int] = None, year_to: Optional[int] = None,
                                journal: Optional[str] = None, author: Optional[str] = None,
                                open_access_only: bool = False,
                                sort: Optional[str] = None) -> Tuple[List[Dict[str, Any]], int]:
    """
    Search for papers using the Crossref API
    """
    # Use our standardized API client
    papers, total_results = await get_crossref_data(
        query=query,
        limit=limit,
        offset=offset,
        year_from=year_from,
        year_to=year_to,
        journal=journal,
        author=author,
        sort=sort
    )
    
    return papers, total_results


async def get_paper_access(doi: str) -> Dict[str, Any]:
    """
    Get open access information for a paper using the Unpaywall API.
    """
    # Use our standardized API client
    return await get_unpaywall_data(doi)


def clean_author(author_string: str) -> str:
    """Clean up an author string to extract the last name of the first author"""
    # Import here to avoid circular imports
    from app.services.doi_service import clean_author as doi_clean_author
    return doi_clean_author(author_string)


async def get_doi_for_paper(title: str, author: str, year: str) -> Optional[str]:
    """
    Find DOI for a paper based on title, author, and year
    """
    # Import here to avoid circular imports
    from app.services.doi_service import get_doi_for_paper as doi_get_doi
    return await doi_get_doi(title, author, year)


async def get_dois_for_papers(papers: List[Dict[str, str]]) -> List[Dict[str, str]]:
    """
    Find DOIs for multiple papers
    
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
    Get PDF URL for a paper if available as open access
    """
    # Import here to avoid circular imports
    from app.services.pdf_service import get_paper_pdf_url as pdf_get_url
    return await pdf_get_url(doi)


async def process_csv_for_dois(csv_content: str) -> List[Dict[str, Any]]:
    """
    Process a CSV file to find DOIs for papers
    
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
    Process papers with DOIs to find PDF URLs
    
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


# Import modules
import httpx

# Import the additional providers
from app.services.additional_providers import (
    search_papers_semantic_scholar,
    search_papers_scopus,
    search_papers_exa,
    search_papers_combined
)
