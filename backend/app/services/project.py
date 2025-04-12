from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional, Dict, Any
from fastapi import HTTPException
from datetime import datetime
import logging

from app.models.project import Project as ProjectModel, paper_project
from app.models.paper import Paper as PaperModel
from app.schemas.project import ProjectCreate, ProjectUpdate

logger = logging.getLogger(__name__)

def get_project_by_id(db: Session, project_id: int) -> Optional[ProjectModel]:
    """
    Get a project by ID.
    """
    return db.query(ProjectModel).filter(ProjectModel.id == project_id).first()


def create_project(db: Session, project: ProjectCreate) -> ProjectModel:
    """
    Create a new project.
    """
    logger.info(f"Attempting to create project with name: {project.name}")
    try:
        db_project = ProjectModel(
            name=project.name,
            description=project.description
        )
        
        db.add(db_project)
        db.commit()
        db.refresh(db_project)
        logger.info(f"Project '{project.name}' created successfully with ID: {db_project.id}")
        
        return db_project
    except Exception as e:
        logger.exception(f"Database error creating project '{project.name}': {str(e)}") # Log exception with stack trace
        db.rollback() # Rollback on error
        raise HTTPException(status_code=500, detail=f"Database error: Could not create project. {str(e)}")


def update_project(db: Session, project_id: int, project: ProjectUpdate) -> ProjectModel:
    """
    Update an existing project.
    """
    db_project = get_project_by_id(db, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    # Update fields if provided
    if project.name is not None:
        db_project.name = project.name
    if project.description is not None:
        db_project.description = project.description
    
    db_project.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_project)
    
    return db_project


def delete_project(db: Session, project_id: int) -> bool:
    """
    Delete a project.
    """
    db_project = get_project_by_id(db, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db.delete(db_project)
    db.commit()
    
    return True


def list_projects(db: Session, skip: int = 0, limit: int = 100) -> List[Dict]:
    """
    List all projects with paper counts.
    """
    import logging
    logger = logging.getLogger(__name__)
    
    try:
        # Get all projects with pagination
        projects_query = db.query(ProjectModel).offset(skip).limit(limit).all()
        logger.info(f"Found {len(projects_query)} projects in database")
        
        # Format the results with paper counts
        projects = []
        for project in projects_query:
            # Simply count the number of papers directly using len()
            paper_count = len(project.papers) if project.papers else 0
            
            logger.info(f"Project: id={project.id}, name={project.name}, paper_count={paper_count}")
            
            project_data = {
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "created_at": project.created_at,
                "updated_at": project.updated_at,
                "paper_count": paper_count
            }
            projects.append(project_data)
        
        logger.info(f"Returning {len(projects)} projects")
        return projects
    except Exception as e:
        logger.exception(f"Error in list_projects: {str(e)}")
        return []  # Return empty list instead of letting the exception propagate


def add_paper_to_project(db: Session, project_id: int, paper_id: int) -> ProjectModel:
    """
    Add a paper to a project.
    """
    db_project = get_project_by_id(db, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db_paper = db.query(PaperModel).filter(PaperModel.id == paper_id).first()
    if not db_paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    # Check if paper is already in project
    if db_paper in db_project.papers:
        return db_project
    
    db_project.papers.append(db_paper)
    db.commit()
    db.refresh(db_project)
    
    return db_project


def remove_paper_from_project(db: Session, project_id: int, paper_id: int) -> ProjectModel:
    """
    Remove a paper from a project.
    """
    db_project = get_project_by_id(db, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    db_paper = db.query(PaperModel).filter(PaperModel.id == paper_id).first()
    if not db_paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    # Check if paper is in project
    if db_paper not in db_project.papers:
        raise HTTPException(status_code=404, detail="Paper not in this project")
    
    db_project.papers.remove(db_paper)
    db.commit()
    db.refresh(db_project)
    
    return db_project


def add_papers_to_project_batch(db: Session, project_id: int, paper_ids: List[int]) -> Dict[str, Any]:
    """
    Add multiple papers to a project in a single batch operation.
    
    Args:
        db: Database session
        project_id: ID of the project to add papers to
        paper_ids: List of paper IDs to add to the project
        
    Returns:
        Dictionary with summary of the operation (added_count, skipped_count)
    """
    db_project = get_project_by_id(db, project_id)
    if not db_project:
        raise HTTPException(status_code=404, detail="Project not found")
    
    added_count = 0
    skipped_count = 0
    
    # Get all papers in a single query for efficiency
    papers = db.query(PaperModel).filter(PaperModel.id.in_(paper_ids)).all()
    
    # Create a set of IDs of papers already in the project for fast lookup
    existing_paper_ids = {paper.id for paper in db_project.papers}
    
    # Add papers that are not already in the project
    for paper in papers:
        if paper.id not in existing_paper_ids:
            db_project.papers.append(paper)
            added_count += 1
        else:
            skipped_count += 1
    
    db.commit()
    db.refresh(db_project)
    
    return {
        "added_count": added_count,
        "skipped_count": skipped_count,
        "total_papers": len(db_project.papers)
    }
