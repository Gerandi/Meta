from fastapi import APIRouter, Depends, HTTPException, Path, Query, status
from typing import List, Dict
from sqlalchemy.orm import Session

from app.schemas.collection import Collection, CollectionCreate, CollectionUpdate, CollectionWithPaperCount
from app.schemas.paper import Paper
from app.services.collection import (
    create_collection, get_collection_by_id, update_collection, 
    delete_collection, list_collections, add_paper_to_collection,
    remove_paper_from_collection
)
from app.db.session import get_db

router = APIRouter()


@router.post("/", response_model=Collection, status_code=status.HTTP_201_CREATED)
async def create_new_collection(
    collection: CollectionCreate,
    db: Session = Depends(get_db)
):
    """
    Create a new collection.
    """
    return create_collection(db, collection)


@router.get("/", response_model=List[CollectionWithPaperCount])
async def get_collections(
    skip: int = Query(0, description="Number of collections to skip"),
    limit: int = Query(100, description="Maximum number of collections to return"),
    db: Session = Depends(get_db)
):
    """
    List all collections with paper count.
    """
    return list_collections(db, skip, limit)


@router.get("/{collection_id}", response_model=Collection)
async def get_collection(
    collection_id: int = Path(..., description="The ID of the collection to retrieve"),
    db: Session = Depends(get_db)
):
    """
    Get a specific collection by ID.
    """
    db_collection = get_collection_by_id(db, collection_id)
    if not db_collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return db_collection


@router.put("/{collection_id}", response_model=Collection)
async def update_collection_details(
    collection_id: int = Path(..., description="The ID of the collection to update"),
    collection: CollectionUpdate = None,
    db: Session = Depends(get_db)
):
    """
    Update a collection.
    """
    return update_collection(db, collection_id, collection)


@router.delete("/{collection_id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_collection_by_id(
    collection_id: int = Path(..., description="The ID of the collection to delete"),
    db: Session = Depends(get_db)
):
    """
    Delete a collection.
    """
    delete_collection(db, collection_id)
    return None


@router.post("/{collection_id}/papers/{paper_id}", response_model=Collection)
async def add_paper_to_collection_by_id(
    collection_id: int = Path(..., description="The ID of the collection"),
    paper_id: int = Path(..., description="The ID of the paper to add"),
    db: Session = Depends(get_db)
):
    """
    Add a paper to a collection.
    """
    return add_paper_to_collection(db, collection_id, paper_id)


@router.delete("/{collection_id}/papers/{paper_id}", response_model=Collection)
async def remove_paper_from_collection_by_id(
    collection_id: int = Path(..., description="The ID of the collection"),
    paper_id: int = Path(..., description="The ID of the paper to remove"),
    db: Session = Depends(get_db)
):
    """
    Remove a paper from a collection.
    """
    return remove_paper_from_collection(db, collection_id, paper_id)


@router.get("/{collection_id}/papers", response_model=List[Paper])
async def get_papers_in_collection(
    collection_id: int = Path(..., description="The ID of the collection"),
    db: Session = Depends(get_db)
):
    """
    Get all papers in a collection.
    """
    db_collection = get_collection_by_id(db, collection_id)
    if not db_collection:
        raise HTTPException(status_code=404, detail="Collection not found")
    return db_collection.papers
