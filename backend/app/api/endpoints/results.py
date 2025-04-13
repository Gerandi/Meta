from fastapi import APIRouter, Depends, HTTPException, Query
from fastapi.responses import JSONResponse
from typing import List, Optional
from sqlalchemy.orm import Session
import logging

from app.schemas.results import ResultsTable, ResultsExport
from app.services.results_service import get_results_table_service
from app.db.session import get_db

logger = logging.getLogger(__name__)

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
        # The service already handles the 'no coding sheet' case gracefully
        results = get_results_table_service(db, project_id)
        return results
    except HTTPException as http_exc:
        # Re-raise HTTPExceptions directly
        raise http_exc
    except Exception as e:
        logger.exception(f"Error generating results table for project {project_id}: {str(e)}") # Log full traceback
        # Return a JSON response for internal server errors
        return JSONResponse(
            status_code=500,
            content={"detail": f"Internal server error generating results table: {str(e)}"}
        )


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
