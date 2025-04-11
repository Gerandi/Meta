import logging
from typing import Dict, List, Any, Optional, Tuple
from app.services.openalex_search import search_papers_openalex

logger = logging.getLogger(__name__)

async def search_papers(
    query: str, 
    limit: int = 20, 
    offset: int = 0,
    providers: Optional[List[str]] = None,  # Kept for backward compatibility
    year_from: Optional[int] = None,
    year_to: Optional[int] = None,
    journal: Optional[str] = None,
    author: Optional[str] = None,
    open_access_only: bool = False,
    sort: Optional[str] = None,
    fetch_all: bool = False
) -> Dict[str, Any]:
    """
    Search for papers using only the OpenAlex provider.
    
    Args:
        query: Search query
        limit: Maximum number of results to return
        offset: Number of results to skip
        providers: Ignored - kept for backward compatibility
        year_from: Earliest publication year
        year_to: Latest publication year
        journal: Filter by journal
        author: Filter by author
        open_access_only: Whether to return only open access papers
        sort: Sort order for results
        fetch_all: Whether to fetch all available results for client-side pagination
        
    Returns:
        Dictionary containing results and total count
    """
    logger.info(f"Searching papers with query: '{query}' (using OpenAlex only)")
    
    try:
        # Call the OpenAlex search function
        results, total_count = await search_papers_openalex(
            query=query,
            limit=limit,
            offset=offset,
            year_from=year_from,
            year_to=year_to,
            journal=journal,
            author=author,
            open_access_only=open_access_only,
            sort=sort,
            fetch_all=fetch_all
        )
        
        return {
            "results": results,
            "total": total_count
        }
        
    except Exception as e:
        logger.error(f"Error in paper search: {str(e)}")
        return {
            "results": [],
            "total": 0
        }
