from fastapi import APIRouter

from app.api.endpoints import papers, coding, results, collections, simple_search

api_router = APIRouter()

api_router.include_router(papers.router, prefix="/papers", tags=["papers"])
api_router.include_router(coding.router, prefix="/coding", tags=["coding"])
api_router.include_router(results.router, prefix="/results", tags=["results"])
api_router.include_router(collections.router, prefix="/collections", tags=["collections"])
api_router.include_router(simple_search.router, prefix="", tags=["search"]) # Added simple search router
