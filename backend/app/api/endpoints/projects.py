from fastapi import APIRouter, Depends, HTTPException, Path, Query, status, Body
from typing import List, Dict, Any
from sqlalchemy.orm import Session
from pydantic import BaseModel

from app.schemas.project import Project, ProjectCreate, ProjectUpdate, ProjectWithPaperCount
from app.schemas.paper import Paper as PaperSchema, PaperCreate
from app.services.project import (
    create_project, get_project_by_id, update_project, 
    delete_project, list_projects, add_paper_to_project,
    remove_paper_from_project, add_papers_to_project_batch
)
from app.db.session import get_db
from app.services.paper import create_paper
from app.models.paper import PaperStatus
from app.api import deps
from app.models.user import User as UserModel
import logging

logger = logging.getLogger(__name__)

router = APIRouter()


# Define a payload model for batch paper IDs
class PaperIdsPayload(BaseModel):
    paper_ids: List[int]


@router.post("/", response_model=Project, status_code=status.HTTP_201_CREATED)
async def create_new_project(
    project: ProjectCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
):
    """
    Create a new project owned by the current user.
    """
    return create_project(db, project, owner_id=current_user.id)


@router.get("/", response_model=List[ProjectWithPaperCount])
async def get_projects(
    skip: int = Query(0, description="Number of projects to skip"),
    limit: int = Query(100, description="Maximum number of projects to return"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
):
    """
    List all projects with paper count for the current user.
    """
    return list_projects(db, owner_id=current_user.id, skip=skip, limit=limit)


@router.get("/{project_id}", response_model=Project)
async def get_project(
    project_id: int = Path(..., description="The ID of the project to retrieve"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
):
    """
    Get a specific project owned by the current user.
    """
    db_project = get_project_by_id(db, project_id=project_id, owner_id=current_user.id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found or not owned by user")
    return db_project


@router.put("/{project_id}", response_model=Project)
async def update_project_details(
    project_id: int = Path(..., description="The ID of the project to update"),
    project: ProjectUpdate = None,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
):
    """
    Update a project owned by the current user.
    """
    return update_project(db, project_id, project, owner_id=current_user.id)


@router.delete("/{project_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_project_by_id(
    project_id: int = Path(..., description="The ID of the project to delete"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
):
    """
    Delete a project owned by the current user.
    """
    delete_project(db, project_id, owner_id=current_user.id)
    return None


@router.post("/{project_id}/papers/{paper_id}", response_model=Project)
async def add_paper_to_project_by_id(
    project_id: int = Path(..., description="The ID of the project"),
    paper_id: int = Path(..., description="The ID of the paper to add"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
):
    """
    Add a paper to a project owned by the current user.
    """
    return add_paper_to_project(db, project_id, paper_id, owner_id=current_user.id)


@router.post("/{project_id}/papers/batch", response_model=Dict[str, Any])
async def add_papers_to_project_batch_endpoint(
    project_id: int = Path(..., description="The ID of the project"),
    payload: PaperIdsPayload = Body(..., description="List of paper IDs to add to the project"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
):
    """
    Add multiple papers to a project owned by the current user in a single batch operation.
    
    This is more efficient than adding papers one by one when adding multiple papers.
    """
    return add_papers_to_project_batch(db, project_id, payload.paper_ids, owner_id=current_user.id)


@router.delete("/{project_id}/papers/{paper_id}", response_model=Project)
async def remove_paper_from_project_by_id(
    project_id: int = Path(..., description="The ID of the project"),
    paper_id: int = Path(..., description="The ID of the paper to remove"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
):
    """
    Remove a paper from a project owned by the current user.
    """
    return remove_paper_from_project(db, project_id, paper_id, owner_id=current_user.id)


@router.post("/{project_id}/import-paper", response_model=PaperSchema, status_code=status.HTTP_201_CREATED)
async def import_and_add_paper_to_project(
    project_id: int = Path(..., description="The ID of the project to add the paper to"),
    paper_data: PaperCreate = Body(..., description="Data for the paper to import"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
):
    """
    Imports a single paper directly into a project with 'processing' status.
    Checks for duplicates based on DOI before creating.
    """
    db_project = get_project_by_id(db, project_id, owner_id=current_user.id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found or not owned by user")

    # Set status to PROCESSING directly
    paper_data.status = PaperStatus.PROCESSING

    try:
        # create_paper handles DOI duplication check - pass owner_id
        db_paper = create_paper(db, paper_data, owner_id=current_user.id)

        # Add paper to project if not already associated
        # (create_paper might return an existing paper)
        if db_paper not in db_project.papers:
            db_project.papers.append(db_paper)
            db.commit()
            db.refresh(db_paper) # Refresh to get updated relationships if needed
        
        # Ensure the status is PROCESSING even if paper existed
        if db_paper.status != PaperStatus.PROCESSING:
             db_paper.status = PaperStatus.PROCESSING
             db.commit()
             db.refresh(db_paper)

        return db_paper
    except Exception as e:
        db.rollback()
        logger.error(f"Error importing paper directly to project {project_id}: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Could not import paper: {str(e)}")


@router.get("/{project_id}/papers", response_model=List[PaperSchema])
async def get_papers_in_project(
    project_id: int = Path(..., description="The ID of the project"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(deps.get_current_active_user)
):
    """
    Get all papers in a project owned by the current user.
    """
    db_project = get_project_by_id(db, project_id, owner_id=current_user.id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found or not owned by user")
    return db_project.papers
