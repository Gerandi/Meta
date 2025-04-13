from fastapi import APIRouter

from app.api.endpoints import papers, coding, results, search, processing, counts, projects

api_router = APIRouter()

api_router.include_router(papers.router, prefix="/papers", tags=["papers"])
api_router.include_router(coding.router, prefix="/coding", tags=["coding"])
api_router.include_router(results.router, prefix="/results", tags=["results"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
api_router.include_router(search.router, prefix="", tags=["search"]) # Using renamed search implementation
api_router.include_router(processing.router, prefix="", tags=["processing"]) # Add processing endpoints
api_router.include_router(counts.router, prefix="", tags=["counts"]) # Add counting endpoints
