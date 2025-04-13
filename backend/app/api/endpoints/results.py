from fastapi import APIRouter, Depends, HTTPException, Query
from typing import List, Optional
from sqlalchemy.orm import Session

from app.schemas.results import ResultsTable, ResultsExport
from app.services.results_service import get_results_table_service
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
    try:
        return get_results_table_service(db, project_id)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error generating results table: {str(e)}")


@router.get("/export", response_model=ResultsExport)
async def export_results(
    project_id: int = Query(..., description="Project ID"),
    format: str = Query("csv", description="Export format (csv, xlsx)"),
    db: Session = Depends(get_db),
):
    """
    Export results in various formats.
    """
    # Implementation will be added later - beyond current scope
    raise HTTPException(status_code=501, detail="Export functionality not implemented yet")
