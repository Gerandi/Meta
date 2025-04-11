"""
OpenAlex direct API client for academic search.
"""
import logging
import httpx
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from app.core.config import settings

logger = logging.getLogger(__name__)

# Email for the polite pool - get from settings
EMAIL = settings.OPENALEX_EMAIL

async def search_papers_direct(
    query: str,
    page: int = 1,
    per_page: int = 10,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    journal: Optional[str] = None,
    author: Optional[str] = None,
    open_access_only: bool = False,
    sort: Optional[str] = None
) -> Tuple[List[Dict[str, Any]], int]:
    """
    Search for papers using OpenAlex API directly
    
    Args:
        query: Search query
        page: Page number
        per_page: Results per page
        year_from: Earliest publication year
        year_to: Latest publication year
        journal: Filter by journal
        author: Filter by author name
        open_access_only: Whether to return only open access papers
        sort: Sort order for results
        
    Returns:
        Tuple of (list of papers, total results count)
    """
    try:
        # Build the API URL
        base_url = "https://api.openalex.org/works"
        
        # Build parameters
        params = {
            "per-page": per_page,
            "page": page,
            "mailto": EMAIL
        }
        
        # Add search term
        if query:
            params["search"] = query
            
        # Add sort
        if sort:
            if sort == "date":
                params["sort"] = "publication_date:desc"
            elif sort == "cited":
                params["sort"] = "cited_by_count:desc"
            elif sort == "title":
                params["sort"] = "title:asc"
                
        # Build filters
        filters = []
        
        # Year filters
        if year_from:
            filters.append(f"publication_year:>{year_from-1}")
        if year_to:
            filters.append(f"publication_year:<{year_to+1}")
            
        # Journal filter
        if journal:
            filters.append(f"host_venue.display_name.search:{journal}")
            
        # Author filter
        if author:
            filters.append(f"author.display_name.search:{author}")
            
        # Open access filter
        if open_access_only:
            filters.append("is_oa:true")
            
        # Add filters to params
        if filters:
            params["filter"] = ",".join(filters)
        
        # Log the request
        logger.info(f"OpenAlex request: {base_url} with params: {params}")
        
        # Make the request
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(base_url, params=params)
            
            # Check if request was successful
            if response.status_code == 200:
                data = response.json()
                
                # Get results and count
                results = data.get("results", [])
                total_count = data.get("meta", {}).get("count", 0)
                
                # Format results
                formatted_results = []
                for paper in results:
                    # Extract basic info
                    title = paper.get("title", "")
                    doi = paper.get("doi")
                    
                    # Extract authors
                    authors = []
                    for authorship in paper.get("authorships", []):
                        author_info = authorship.get("author", {})
                        name = author_info.get("display_name", "")
                        authors.append({"name": name, "affiliation": None})
                    
                    # Extract journal info from host_venue
                    journal_name = None
                    if paper.get("host_venue"):
                        journal_name = paper["host_venue"].get("display_name")
                    
                    # Extract publication date
                    pub_date = paper.get("publication_date")
                    
                    # Extract citation count
                    citation_count = paper.get("cited_by_count", 0)
                    
                    # Format the paper
                    formatted_paper = {
                        "title": title,
                        "doi": doi,
                        "authors": authors,
                        "publication_date": pub_date,
                        "journal": journal_name,
                        "citation_count": citation_count,
                        "source": "OpenAlex"
                    }
                    
                    formatted_results.append(formatted_paper)
                
                return formatted_results, total_count
            else:
                logger.error(f"OpenAlex API error: {response.status_code} - {response.text}")
                return [], 0
    
    except Exception as e:
        logger.error(f"Error searching OpenAlex: {str(e)}")
        return [], 0
