from fastapi import APIRouter, Query, HTTPException
from typing import Optional, Dict, Any, List

import logging
import httpx

from app.services.openalex_search import search_papers_openalex

logger = logging.getLogger(__name__)

router = APIRouter()

@router.get("/papers/simple-search")
async def simple_search(
    query: str = Query(..., description="Search query"),
    limit: int = Query(100, description="Number of results to return"),
):
    """
    Simplified search endpoint that only requires a query.
    """
    try:
        results, total_count = await search_papers_openalex(
            query=query, 
            limit=limit,
            fetch_all=True
        )
        
        return {
            "results": results,
            "totalResults": total_count,
            "metadata": {
                "query": query
            }
        }
    except Exception as e:
        logger.error(f"Error in simple search: {str(e)}")
        raise HTTPException(status_code=500, detail=str(e))
