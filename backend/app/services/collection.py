from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional, Dict, Any
from fastapi import HTTPException
from datetime import datetime

from app.models.collection import Collection as CollectionModel
from app.models.paper import Paper as PaperModel
from app.schemas.collection import CollectionCreate, CollectionUpdate


def get_collection_by_id(db: Session, collection_id: int) -> Optional[CollectionModel]:
    """
    Get a collection by ID.
    """
    return db.query(CollectionModel).filter(CollectionModel.id == collection_id).first()


def create_collection(db: Session, collection: CollectionCreate) -> CollectionModel:
    """
    Create a new collection.
    """
    db_collection = CollectionModel(
        name=collection.name,
        description=collection.description
    )
    
    db.add(db_collection)
    db.commit()
    db.refresh(db_collection)
    
    return db_collection


def update_collection(db: Session, collection_id: int, collection: CollectionUpdate) -> CollectionModel:
    """
    Update an existing collection.
    """
    db_collection = get_collection_by_id(db, collection_id)
    if not db_collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    # Update fields if provided
    if collection.name is not None:
        db_collection.name = collection.name
    if collection.description is not None:
        db_collection.description = collection.description
    
    db_collection.updated_at = datetime.utcnow()
    db.commit()
    db.refresh(db_collection)
    
    return db_collection


def delete_collection(db: Session, collection_id: int) -> bool:
    """
    Delete a collection.
    """
    db_collection = get_collection_by_id(db, collection_id)
    if not db_collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    db.delete(db_collection)
    db.commit()
    
    return True


def list_collections(db: Session, skip: int = 0, limit: int = 100) -> List[Dict]:
    """
    List all collections with paper counts.
    """
    query = db.query(
        CollectionModel, 
        func.count(CollectionModel.papers).label('paper_count')
    ).outerjoin(
        CollectionModel.papers
    ).group_by(
        CollectionModel.id
    ).offset(skip).limit(limit)
    
    collections = []
    for collection, paper_count in query:
        collection_data = {
            "id": collection.id,
            "name": collection.name,
            "description": collection.description,
            "created_at": collection.created_at,
            "updated_at": collection.updated_at,
            "paper_count": paper_count
        }
        collections.append(collection_data)
    
    return collections


def add_paper_to_collection(db: Session, collection_id: int, paper_id: int) -> CollectionModel:
    """
    Add a paper to a collection.
    """
    db_collection = get_collection_by_id(db, collection_id)
    if not db_collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    db_paper = db.query(PaperModel).filter(PaperModel.id == paper_id).first()
    if not db_paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    # Check if paper is already in collection
    if db_paper in db_collection.papers:
        return db_collection
    
    db_collection.papers.append(db_paper)
    db.commit()
    db.refresh(db_collection)
    
    return db_collection


def remove_paper_from_collection(db: Session, collection_id: int, paper_id: int) -> CollectionModel:
    """
    Remove a paper from a collection.
    """
    db_collection = get_collection_by_id(db, collection_id)
    if not db_collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    
    db_paper = db.query(PaperModel).filter(PaperModel.id == paper_id).first()
    if not db_paper:
        raise HTTPException(status_code=404, detail="Paper not found")
    
    # Check if paper is in collection
    if db_paper not in db_collection.papers:
        raise HTTPException(status_code=404, detail="Paper not in this collection")
    
    db_collection.papers.remove(db_paper)
    db.commit()
    db.refresh(db_collection)
    
    return db_collection
