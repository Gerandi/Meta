"""
Standalone API for project management
"""
import uvicorn
from fastapi import FastAPI, HTTPException, Depends
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
from typing import List, Optional
import logging

# Import our simple service
from simple_project_service import create_project as create_project_service
from simple_project_service import list_projects as list_projects_service
from simple_project_service import setup_database

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create the FastAPI app
app = FastAPI(title="Project API")

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Define request and response models
class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None

class ProjectCreate(ProjectBase):
    pass

class ProjectResponse(ProjectBase):
    id: int
    created_at: str
    updated_at: str
    paper_count: Optional[int] = 0

# Initialize database
@app.on_event("startup")
def on_startup():
    setup_database()
    logger.info("Database initialized on startup")

# API endpoints
@app.post("/projects/", response_model=ProjectResponse)
async def create_project(project: ProjectCreate):
    """Create a new project"""
    try:
        result = create_project_service(project.name, project.description)
        return result
    except Exception as e:
        logger.exception(f"Error creating project: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Could not create project: {str(e)}")

@app.get("/projects/", response_model=List[ProjectResponse])
async def list_projects():
    """List all projects"""
    try:
        return list_projects_service()
    except Exception as e:
        logger.exception(f"Error listing projects: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Could not list projects: {str(e)}")

# Run the app
if __name__ == "__main__":
    uvicorn.run("project_api:app", host="127.0.0.1", port=8001, reload=True)
