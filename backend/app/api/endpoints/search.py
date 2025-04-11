from fastapi import APIRouter, Query, HTTPException
from typing import Optional, Dict, Any, List

import logging
import httpx

from app.services.openalex_direct import search_papers_direct

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/papers/search")
async def search_papers(
    query: str = Query(..., description="Search query"),
    page: int = Query(1, description="Page number"),
    per_page: int = Query(10, description="Results per page"),
    year_from: Optional[int] = Query(None, description="Filter from year"),
    year_to: Optional[int] = Query(None, description="Filter to year"),
    journal: Optional[str] = Query(None, description="Filter by journal name"),
    author: Optional[str] = Query(None, description="Filter by author name"),
    open_access_only: bool = Query(False, description="Filter to open access only"),
    sort: str = Query("relevance", description="Sort results by (relevance, date, cited, title)"),
):
    """
    Search for papers using OpenAlex API.
    
    This endpoint maps directly to OpenAlex's works endpoint with appropriate parameters.
    """
    try:
        # Validate query parameter
        if not query or query.strip() == "":
            return {
                "results": [],
                "totalResults": 0,
                "metadata": {
                    "message": "Please provide a search term"
                }
            }
            
        logger.info(f"Search params: query={query}, page={page}, per_page={per_page}")
        
        # Call the simplified direct search function
        results, total_count = await search_papers_direct(
            query=query,
            page=page,
            per_page=per_page,
            year_from=year_from,
            year_to=year_to,
            journal=journal,
            author=author,
            open_access_only=open_access_only,
            sort=sort
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
                    "openAccessOnly": open_access_only
                },
                "sortBy": sort,
                "page": page,
                "perPage": per_page
            }
        }
        
    except Exception as e:
        logger.error(f"Error in search: {str(e)}")
        error_msg = str(e)
        if not error_msg or error_msg == '{}':
            error_msg = f"Error processing search request: {type(e).__name__}"
        raise HTTPException(status_code=500, detail=error_msg)
