from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional, Dict, Any
from fastapi import HTTPException
from datetime import datetime

from app.models.project import Project as ProjectModel
from app.models.paper import Paper as PaperModel
from app.schemas.project import ProjectCreate, ProjectUpdate


def get_project_by_id(db: Session, project_id: int) -> Optional[ProjectModel]:
    """
    Get a project by ID.
    """
    return db.query(ProjectModel).filter(ProjectModel.id == project_id).first()


def create_project(db: Session, project: ProjectCreate) -> ProjectModel:
    """
    Create a new project.
    """
    db_project = ProjectModel(
        name=project.name,
        description=project.description
    )
    
    db.add(db_project)
    db.commit()
    db.refresh(db_project)
    
    return db_project


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
    query = db.query(
        ProjectModel, 
        func.count(ProjectModel.papers).label('paper_count')
    ).outerjoin(
        ProjectModel.papers
    ).group_by(
        ProjectModel.id
    ).offset(skip).limit(limit)
    
    projects = []
    for project, paper_count in query:
        project_data = {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "created_at": project.created_at,
            "updated_at": project.updated_at,
            "paper_count": paper_count
        }
        projects.append(project_data)
    
    return projects


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
