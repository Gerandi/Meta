from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from fastapi import HTTPException
from datetime import datetime

from app.models.paper import Paper as PaperModel
from app.schemas.paper import PaperCreate, Paper as PaperSchema
from app.schemas.paper import Author as AuthorSchema


def get_paper_by_id(db: Session, paper_id: int) -> Optional[PaperModel]:
    """
    Get a paper by ID.
    """
    return db.query(PaperModel).filter(PaperModel.id == paper_id).first()


def get_paper_by_doi(db: Session, doi: str) -> Optional[PaperModel]:
    """
    Get a paper by DOI.
    """
    return db.query(PaperModel).filter(PaperModel.doi == doi).first()


def create_paper(db: Session, paper: PaperCreate) -> PaperModel:
    """
    Create a new paper record.
    """
    # Check if paper with this DOI already exists
    if paper.doi:
        existing_paper = get_paper_by_doi(db, paper.doi)
        if existing_paper:
            return existing_paper
    
    # Process authors correctly - handle both AuthorSchema objects and dicts
    formatted_authors = []
    for author in paper.authors:
        if isinstance(author, AuthorSchema):
            formatted_authors.append(author.dict())
        elif isinstance(author, dict):
            # Validate dict has at least a name
            if 'name' in author:
                formatted_authors.append(author)
            else:
                # Use a default name if missing
                author_copy = author.copy()
                author_copy['name'] = 'Unknown Author'
                formatted_authors.append(author_copy)
    
    # Convert Pydantic model to SQLAlchemy model
    db_paper = PaperModel(
        title=paper.title,
        abstract=paper.abstract or "",
        doi=paper.doi,
        authors=formatted_authors,
        publication_date=paper.publication_date,
        journal=paper.journal,
        volume=paper.volume,
        issue=paper.issue,
        pages=paper.pages,
        publisher=paper.publisher,
        url=paper.url or (paper.doi if paper.doi else ""),
        keywords=paper.keywords,
        is_open_access=paper.is_open_access,
        open_access_url=paper.open_access_url
    )
    
    # Add to database
    db.add(db_paper)
    db.commit()
    db.refresh(db_paper)
    
    return db_paper


def update_paper(db: Session, paper_id: int, paper_data: Dict[str, Any]) -> PaperModel:
    """
    Update an existing paper.
    """
    db_paper = get_paper_by_id(db, paper_id)
    if not db_paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    # Update fields
    for field, value in paper_data.items():
        if hasattr(db_paper, field):
            setattr(db_paper, field, value)
    
    db_paper.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_paper)
    
    return db_paper


def delete_paper(db: Session, paper_id: int) -> bool:
    """
    Delete a paper.
    """
    db_paper = get_paper_by_id(db, paper_id)
    if not db_paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    db.delete(db_paper)
    db.commit()
    
    return True


def list_papers(db: Session, skip: int = 0, limit: int = 100) -> List[PaperModel]:
    """
    List all papers with pagination.
    """
    return db.query(PaperModel).offset(skip).limit(limit).all()
