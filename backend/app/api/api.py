from fastapi import APIRouter

from app.api.endpoints import papers, coding, results, search, processing, counts, projects

api_router = APIRouter()

# Add specific prefix routers first to avoid conflicts with dynamic routes
api_router.include_router(counts.router, prefix="/counts", tags=["counts"])
api_router.include_router(processing.router, prefix="/processing", tags=["processing"])
api_router.include_router(search.router, prefix="/search", tags=["search"])

# Then add the routers with dynamic routes
api_router.include_router(papers.router, prefix="/papers", tags=["papers"])
api_router.include_router(coding.router, prefix="/coding", tags=["coding"])
api_router.include_router(results.router, prefix="/results", tags=["results"])
api_router.include_router(projects.router, prefix="/projects", tags=["projects"])
