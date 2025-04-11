"""
OpenAlex API client for academic search using direct API calls.
"""
import logging
import httpx
from typing import Dict, Any, List, Optional, Tuple
from datetime import datetime

logger = logging.getLogger(__name__)

# Email for the polite pool
EMAIL = "meta@example.com"  # Replace with your actual email

# Maximum results to fetch per page from OpenAlex
MAX_RESULTS_PER_PAGE = 100
# Maximum total results to fetch for client-side pagination
MAX_TOTAL_RESULTS = 200

async def search_papers_openalex(
    query: str,
    limit: int = 20,
    offset: int = 0,
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    journal: Optional[str] = None,
    author: Optional[str] = None,
    open_access_only: bool = False,
    sort: Optional[str] = None,
    fetch_all: bool = False  # Whether to fetch all available results for client-side pagination
) -> Tuple[List[Dict[str, Any]], int]:
    """
    Search for papers using OpenAlex API directly
    
    Args:
        query: Search query
        limit: Maximum number of results to return
        offset: Number of results to skip
        year_from: Earliest publication year
        year_to: Latest publication year
        journal: Filter by journal
        author: Filter by author
        open_access_only: Whether to return only open access papers
        sort: Sort order for results
        
    Returns:
        Tuple of (list of papers, total results count)
    """
    try:
        # Base URL for OpenAlex API
        base_url = "https://api.openalex.org/works"
        
        # Build filter string for OpenAlex
        filters = []
        
        # Add year filters
        if year_from:
            filters.append(f"publication_year:>={year_from}")
        if year_to:
            filters.append(f"publication_year:<={year_to}")
            
        # Add journal filter
        if journal:
            filters.append(f"primary_location.source.display_name.search:{journal}")
            
        # Add author filter
        if author:
            filters.append(f"author.display_name.search:{author}")
            
        # Add open access filter
        if open_access_only:
            filters.append("is_oa:true")
        
        # Build parameters
        params = {
            "search": query,
            "per_page": min(MAX_RESULTS_PER_PAGE, limit if not fetch_all else MAX_RESULTS_PER_PAGE),
            "page": 1 if fetch_all else ((offset // limit) + 1 if limit else 1),
            "mailto": EMAIL
        }
        
        # Add filters if any
        if filters:
            params["filter"] = ",".join(filters)
            
        # Add sorting
        if sort:
            if sort == "date":
                params["sort"] = "publication_date:desc"
            elif sort == "cited":
                params["sort"] = "cited_by_count:desc"
            elif sort == "title":
                params["sort"] = "title:asc"
            # Default is relevance, no need to specify
        
        # Make the request
        async with httpx.AsyncClient(timeout=30.0) as client:
            response = await client.get(base_url, params=params)
            
            if response.status_code == 200:
                data = response.json()
                results = data.get('results', [])
                total_count = data.get('meta', {}).get('count', 0)
                
                # If fetching all results for client-side pagination, fetch additional pages
                if fetch_all and total_count > 0:
                    # Calculate how many pages to fetch (up to the max results limit)
                    pages_to_fetch = min(MAX_TOTAL_RESULTS // MAX_RESULTS_PER_PAGE,
                                        (total_count + MAX_RESULTS_PER_PAGE - 1) // MAX_RESULTS_PER_PAGE)
                    
                    for page in range(2, pages_to_fetch + 1):
                        # Update page parameter
                        params["page"] = page
                        
                        # Make additional request
                        try:
                            page_response = await client.get(base_url, params=params)
                            if page_response.status_code == 200:
                                page_data = page_response.json()
                                results.extend(page_data.get('results', []))
                            else:
                                logger.warning(f"Failed to fetch page {page}: {page_response.status_code}")
                                break
                        except Exception as e:
                            logger.error(f"Error fetching additional page: {e}")
                            break
                
                # Format the results to match the expected structure
                formatted_results = []
                for paper in results:
                    # Extract authors
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
                    
                    # Extract abstract
                    abstract = None
                    if paper.get("abstract_inverted_index"):
                        # Convert inverted index to text
                        try:
                            words = []
                            for word, positions in paper["abstract_inverted_index"].items():
                                for pos in positions:
                                    while len(words) <= pos:
                                        words.append("")
                                    words[pos] = word
                            abstract = " ".join(words)
                        except Exception as e:
                            logger.error(f"Error processing abstract: {e}")
                            abstract = "Abstract available but could not be processed"
                    
                    # Extract journal
                    journal_name = None
                    if paper.get("primary_location") and paper["primary_location"].get("source"):
                        journal_name = paper["primary_location"]["source"].get("display_name")
                    
                    # Extract open access info
                    is_oa = False
                    oa_url = None
                    if paper.get("open_access"):
                        is_oa = paper["open_access"].get("is_oa", False)
                        oa_url = paper["open_access"].get("oa_url")
                    
                    # Extract concepts as keywords
                    keywords = []
                    if paper.get("concepts"):
                        for concept in paper.get("concepts", [])[:5]:
                            if isinstance(concept, dict) and concept.get("display_name"):
                                keywords.append(concept.get("display_name"))
                    
                    # Format the paper
                    formatted_paper = {
                        "title": paper.get("title", ""),
                        "doi": paper.get("doi", None),
                        "authors": authors,
                        "publication_date": paper.get("publication_date", None),
                        "abstract": abstract,
                        "journal": journal_name,
                        "volume": paper.get("biblio", {}).get("volume", None),
                        "issue": paper.get("biblio", {}).get("issue", None),
                        "pages": f"{paper.get('biblio', {}).get('first_page', '')}-{paper.get('biblio', {}).get('last_page', '')}" if paper.get('biblio', {}).get('first_page') else None,
                        "publisher": paper.get("primary_location", {}).get("source", {}).get("publisher", None),
                        "url": paper.get("doi") or paper.get("primary_location", {}).get("landing_page_url"),
                        "is_open_access": is_oa,
                        "open_access_url": oa_url,
                        "citation_count": paper.get("cited_by_count", 0),
                        "references_count": len(paper.get("referenced_works", [])) if paper.get("referenced_works") else 0,
                        "keywords": keywords,
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
