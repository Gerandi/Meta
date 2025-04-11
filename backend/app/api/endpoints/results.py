from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from app.schemas.results import ResultsTable, ResultsExport
from app.db.session import get_db

router = APIRouter()


@router.get("/table", response_model=ResultsTable)
async def get_results_table(
    project_id: int = Query(..., description="Project ID"),
    db: Session = Depends(get_db),
):
    """
    Get a formatted results table for a project.
    """
    # Implementation will be added later
    pass


@router.get("/export", response_model=ResultsExport)
async def export_results(
    project_id: int = Query(..., description="Project ID"),
    format: str = Query("csv", description="Export format (csv, xlsx)"),
    db: Session = Depends(get_db),
):
    """
    Export results in various formats.
    """
    # Implementation will be added later
    pass
