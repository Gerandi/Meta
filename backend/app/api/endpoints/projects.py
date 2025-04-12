from fastapi import APIRouter, Depends, HTTPException, Path, Query, status, Body
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.schemas.project import Project, ProjectCreate, ProjectUpdate, ProjectWithPaperCount
from app.schemas.paper import Paper
from app.services.project import (
    create_project, get_project_by_id, update_project, 
    delete_project, list_projects, add_paper_to_project,
    remove_paper_from_project, add_papers_to_project_batch
)
from app.db.session import get_db

router = APIRouter()


# Define a payload model for batch paper IDs
class PaperIdsPayload(BaseModel):
    paper_ids: List[int]


@router.post("/", response_model=Project, status_code=status.HTTP_201_CREATED)
async def create_new_project(
    project: ProjectCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new project.
    """
    return create_project(db, project)


@router.get("/", response_model=List[ProjectWithPaperCount])
async def get_projects(
    skip: int = Query(0, description="Number of projects to skip"),
    limit: int = Query(100, description="Maximum number of projects to return"),
    db: Session = Depends(get_db)
):
    """
    List all projects with paper count.
    """
    return list_projects(db, skip, limit)


@router.get("/{project_id}", response_model=Project)
async def get_project(
    project_id: int = Path(..., description="The ID of the project to retrieve"),
    db: Session = Depends(get_db)
):
    """
    Get a specific project by ID.
    """
    db_project = get_project_by_id(db, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project


@router.put("/{project_id}", response_model=Project)
async def update_project_details(
    project_id: int = Path(..., description="The ID of the project to update"),
    project: ProjectUpdate = None,
    db: Session = Depends(get_db)
):
    """
    Update a project.
    """
    return update_project(db, project_id, project)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project_by_id(
    project_id: int = Path(..., description="The ID of the project to delete"),
    db: Session = Depends(get_db)
):
    """
    Delete a project.
    """
    delete_project(db, project_id)
    return None


@router.post("/{project_id}/papers/{paper_id}", response_model=Project)
async def add_paper_to_project_by_id(
    project_id: int = Path(..., description="The ID of the project"),
    paper_id: int = Path(..., description="The ID of the paper to add"),
    db: Session = Depends(get_db)
):
    """
    Add a paper to a project.
    """
    return add_paper_to_project(db, project_id, paper_id)


@router.post("/{project_id}/papers/batch", response_model=Dict[str, Any])
async def add_papers_to_project_batch_endpoint(
    project_id: int = Path(..., description="The ID of the project"),
    payload: PaperIdsPayload = Body(..., description="List of paper IDs to add to the project"),
    db: Session = Depends(get_db)
):
    """
    Add multiple papers to a project in a single batch operation.
    
    This is more efficient than adding papers one by one when adding multiple papers.
    """
    return add_papers_to_project_batch(db, project_id, payload.paper_ids)


@router.delete("/{project_id}/papers/{paper_id}", response_model=Project)
async def remove_paper_from_project_by_id(
    project_id: int = Path(..., description="The ID of the project"),
    paper_id: int = Path(..., description="The ID of the paper to remove"),
    db: Session = Depends(get_db)
):
    """
    Remove a paper from a project.
    """
    return remove_paper_from_project(db, project_id, paper_id)


@router.get("/{project_id}/papers", response_model=List[Paper])
async def get_papers_in_project(
    project_id: int = Path(..., description="The ID of the project"),
    db: Session = Depends(get_db)
):
    """
    Get all papers in a project.
    """
    db_project = get_project_by_id(db, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    return db_project.papers
