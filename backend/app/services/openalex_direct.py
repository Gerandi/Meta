"""
OpenAlex direct API client for academic search.
"""
import logging
import httpx
import asyncio # Added for potential retries/sleep
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime
from app.core.config import settings

logger = logging.getLogger(__name__)

# Helper function to reconstruct abstract from inverted index
def reconstruct_abstract(inverted_index: Optional[Dict[str, List[int]]]) -> Optional[str]:
    """Reconstructs the abstract string from OpenAlex's inverted index format."""
    if not inverted_index:
        return None
    
    try:
        # Create a list of (word, position) tuples
        word_positions = []
        for word, positions in inverted_index.items():
            for pos in positions:
                word_positions.append((word, pos))
        
        # Sort by position
        word_positions.sort(key=lambda x: x[1])
        
        # Join words
        abstract = ' '.join([word for word, pos in word_positions])
        return abstract
    except Exception as e:
        logger.error(f"Error reconstructing abstract: {e}")
        return None

# Email for the polite pool - get from settings
EMAIL = settings.OPENALEX_EMAIL

# --- Consolidated Search Function ---
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
            
            # Make the request with retry logic for rate limits
            max_retries = 3
            retry_delay = 2  # seconds
            
            for attempt in range(max_retries):
                try:
                    response = await client.get(base_url, params=params)
                    
                    # Log the response status
                    logger.info(f"OpenAlex API response status: {response.status_code}")
                    
                    if response.status_code == 200:
                        # Successful response
                        try:
                            data = response.json()
                            
                            if not data or not isinstance(data, dict):
                                logger.error(f"Invalid response format from OpenAlex: {type(data)}")
                                return [], 0
                            
                            results = data.get('results', [])
                            if results is None: results = []
                                
                            meta = data.get('meta', {})
                            if meta is None: meta = {}
                                
                            total_count = meta.get('count', 0)
                            if total_count is None: total_count = 0
                            
                            # Format the results (using detailed formatting from openalex_search.py)
                            formatted_results = []
                            if not isinstance(results, list):
                                logger.error(f"Results is not a list: {type(results)}")
                                return [], 0
                                
                            for paper in results:
                                # Extract authors with affiliations
                                try:
                                    authors = []
                                    for authorship in paper.get("authorships", []):
                                        author_info = authorship.get("author", {})
                                        name = author_info.get("display_name", "")
                                        affiliation = None
                                        if authorship.get("institutions"):
                                            institution = authorship.get("institutions", [])[0] if authorship.get("institutions") else None
                                            if institution:
                                                affiliation = institution.get("display_name")
                                        authors.append({"name": name, "affiliation": affiliation})
                                except Exception as e:
                                    logger.error(f"Error processing authors: {e}")
                                    authors = []
                                
                                # Reconstruct abstract
                                abstract = reconstruct_abstract(paper.get("abstract_inverted_index"))
                                
                                # Extract journal
                                journal_name = None
                                publisher = None
                                host_venue = paper.get("host_venue") # Use host_venue instead of primary_location for journal
                                if host_venue:
                                    journal_name = host_venue.get("display_name")
                                    publisher = host_venue.get("publisher")

                                # Extract open access info
                                is_oa = False
                                oa_url = None
                                best_oa_location = paper.get("best_oa_location")
                                if best_oa_location and best_oa_location.get("is_oa"):
                                    is_oa = True
                                    oa_url = best_oa_location.get("landing_page_url") or best_oa_location.get("pdf_url")
                                
                                # Extract concepts as keywords
                                keywords = []
                                if paper.get("concepts"):
                                    for concept in paper.get("concepts", [])[:5]: # Limit to top 5
                                        if isinstance(concept, dict) and concept.get("display_name"):
                                            keywords.append(concept.get("display_name"))
                                
                                # Parse publication date
                                pub_date_str = paper.get("publication_date")
                                
                                # Format the paper
                                formatted_paper = {
                                    "title": paper.get("title", ""),
                                    "doi": paper.get("doi", None),
                                    "authors": authors,
                                    "publication_date": pub_date_str, # Keep as string for frontend
                                    "abstract": abstract,
                                    "journal": journal_name,
                                    "volume": paper.get("biblio", {}).get("volume", None),
                                    "issue": paper.get("biblio", {}).get("issue", None),
                                    "pages": f"{paper.get('biblio', {}).get('first_page', '')}-{paper.get('biblio', {}).get('last_page', '')}" if paper.get('biblio', {}).get('first_page') else None,
                                    "publisher": publisher,
                                    "url": paper.get("doi") or (best_oa_location.get("landing_page_url") if best_oa_location else None), # Prefer DOI, fallback to OA landing page
                                    "is_open_access": is_oa,
                                    "open_access_url": oa_url,
                                    "citation_count": paper.get("cited_by_count", 0),
                                    "references_count": len(paper.get("referenced_works", [])) if paper.get("referenced_works") else 0,
                                    "keywords": keywords,
                                    "source": "OpenAlex"
                                }
                                formatted_results.append(formatted_paper)
                            
                            return formatted_results, total_count
                        except Exception as e:
                            logger.error(f"Error processing OpenAlex response: {str(e)}")
                            return [], 0
                    
                    elif response.status_code == 429:
                        logger.warning(f"OpenAlex API rate limit hit (attempt {attempt+1}/{max_retries}). Waiting {retry_delay}s.")
                        await asyncio.sleep(retry_delay)
                        retry_delay *= 2
                    elif response.status_code == 400:
                        logger.error(f"OpenAlex API bad request: {response.text}")
                        return [], 0 # Don't retry on bad request
                    elif response.status_code >= 500:
                        logger.warning(f"OpenAlex API server error {response.status_code} (attempt {attempt+1}/{max_retries}). Retrying.")
                        await asyncio.sleep(retry_delay)
                    else:
                        logger.error(f"OpenAlex API unexpected error: {response.status_code} - {response.text}")
                        return [], 0 # Don't retry unknown errors
                
                except httpx.ReadTimeout:
                    logger.warning(f"OpenAlex API timeout (attempt {attempt+1}/{max_retries}). Retrying.")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(retry_delay)
                        retry_delay *= 2
                    else:
                        logger.error("OpenAlex API timeout - max retries reached")
                        raise # Re-raise after max retries
            
            # If loop finishes without returning, all retries failed
            logger.error("OpenAlex API request failed after all retries")
            return [], 0

    except Exception as e:
        logger.exception(f"Unexpected error in search_papers_direct: {str(e)}") # Use logger.exception for stack trace
        return [], 0

# --- Consolidated DOI Lookup Function ---
async def get_paper_by_doi_direct(doi: str) -> Optional[Dict[str, Any]]:
    """
    Get paper details from OpenAlex using DOI using the direct client logic.
    
    Args:
        doi: The DOI of the paper
        
    Returns:
        Formatted paper details if available, None otherwise
    """
    try:
        # OpenAlex uses DOIs with "https://doi.org/" prefix or just the DOI suffix
        # Let's try the suffix first as it seems more reliable based on API docs examples
        doi_suffix = doi.replace("https://doi.org/", "")
        
        url = f"https://api.openalex.org/works/{doi_suffix}"
        params = {"mailto": EMAIL}
        
        # Make the request with retry logic
        max_retries = 3
        retry_delay = 1 # Shorter delay for single lookup

        async with httpx.AsyncClient(timeout=15.0) as client: # Slightly longer timeout for single lookup
            for attempt in range(max_retries):
                try:
                    logger.info(f"Attempting OpenAlex DOI lookup: {url}")
                    response = await client.get(url, params=params)
                    
                    if response.status_code == 200:
                        paper = response.json()
                        # Format the single result using the same logic as search
                        # (Could be refactored into a shared formatting function later)
                        try:
                            authors = []
                            for authorship in paper.get("authorships", []):
                                author_info = authorship.get("author", {})
                                name = author_info.get("display_name", "")
                                affiliation = None
                                if authorship.get("institutions"):
                                    institution = authorship.get("institutions", [])[0] if authorship.get("institutions") else None
                                    if institution: affiliation = institution.get("display_name")
                                authors.append({"name": name, "affiliation": affiliation})
                        except Exception as e: authors = []

                        abstract = reconstruct_abstract(paper.get("abstract_inverted_index"))
                        
                        journal_name = None
                        publisher = None
                        host_venue = paper.get("host_venue")
                        if host_venue:
                            journal_name = host_venue.get("display_name")
                            publisher = host_venue.get("publisher")

                        is_oa = False
                        oa_url = None
                        best_oa_location = paper.get("best_oa_location")
                        if best_oa_location and best_oa_location.get("is_oa"):
                            is_oa = True
                            oa_url = best_oa_location.get("landing_page_url") or best_oa_location.get("pdf_url")
                        
                        keywords = []
                        if paper.get("concepts"):
                            for concept in paper.get("concepts", [])[:5]:
                                if isinstance(concept, dict) and concept.get("display_name"):
                                    keywords.append(concept.get("display_name"))
                        
                        pub_date_str = paper.get("publication_date")

                        formatted_paper = {
                            "title": paper.get("title", ""), "doi": paper.get("doi", None),
                            "authors": authors, "publication_date": pub_date_str,
                            "abstract": abstract, "journal": journal_name,
                            "volume": paper.get("biblio", {}).get("volume", None),
                            "issue": paper.get("biblio", {}).get("issue", None),
                            "pages": f"{paper.get('biblio', {}).get('first_page', '')}-{paper.get('biblio', {}).get('last_page', '')}" if paper.get('biblio', {}).get('first_page') else None,
                            "publisher": publisher,
                            "url": paper.get("doi") or (best_oa_location.get("landing_page_url") if best_oa_location else None),
                            "is_open_access": is_oa, "open_access_url": oa_url,
                            "citation_count": paper.get("cited_by_count", 0),
                            "references_count": len(paper.get("referenced_works", [])) if paper.get("referenced_works") else 0,
                            "keywords": keywords, "source": "OpenAlex"
                        }
                        return formatted_paper
                        
                    elif response.status_code == 429:
                        logger.warning(f"OpenAlex DOI lookup rate limit (attempt {attempt+1}/{max_retries}). Waiting {retry_delay}s.")
                        await asyncio.sleep(retry_delay)
                        retry_delay *= 2
                    elif response.status_code == 404:
                        logger.warning(f"Paper with DOI {doi} (suffix: {doi_suffix}) not found in OpenAlex.")
                        return None # Not found, don't retry
                    else:
                        logger.warning(f"OpenAlex DOI lookup error {response.status_code} (attempt {attempt+1}/{max_retries}). Retrying.")
                        await asyncio.sleep(retry_delay)
            
                except httpx.ReadTimeout:
                    logger.warning(f"OpenAlex DOI lookup timeout (attempt {attempt+1}/{max_retries}). Retrying.")
                    if attempt < max_retries - 1:
                        await asyncio.sleep(retry_delay)
                        retry_delay *= 2
                    else:
                        logger.error("OpenAlex DOI lookup timeout - max retries reached")
                        return None # Timeout after retries
        
        # If loop finishes, all retries failed
        logger.error(f"OpenAlex DOI lookup failed after all retries for DOI {doi}")
        return None
    
    except Exception as e:
        logger.exception(f"Unexpected error retrieving paper details from OpenAlex for DOI {doi}: {str(e)}")
        return None
