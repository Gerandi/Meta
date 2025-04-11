from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from app.schemas.coding import CodingSheet, CodingSheetCreate, CodingData, CodingDataCreate
from app.db.session import get_db

router = APIRouter()


@router.post("/sheets", response_model=CodingSheet)
async def create_coding_sheet(
    coding_sheet: CodingSheetCreate,
    db: Session = Depends(get_db),
):
    """
    Create a new coding sheet template.
    """
    # Implementation will be added later
    pass


@router.get("/sheets", response_model=List[CodingSheet])
async def list_coding_sheets(
    db: Session = Depends(get_db),
):
    """
    List all coding sheet templates.
    """
    # Implementation will be added later
    pass


@router.get("/sheets/{sheet_id}", response_model=CodingSheet)
async def get_coding_sheet(
    sheet_id: int,
    db: Session = Depends(get_db),
):
    """
    Get a specific coding sheet by ID.
    """
    # Implementation will be added later
    pass


@router.post("/data", response_model=CodingData)
async def create_coding_data(
    coding_data: CodingDataCreate,
    db: Session = Depends(get_db),
):
    """
    Save coding data for a paper.
    """
    # Implementation will be added later
    pass


@router.get("/data/{paper_id}", response_model=CodingData)
async def get_coding_data(
    paper_id: int,
    db: Session = Depends(get_db),
):
    """
    Get coding data for a specific paper.
    """
    # Implementation will be added later
    pass
