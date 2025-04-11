from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, Any
from sqlalchemy.orm import Session
from sqlalchemy import func, and_, or_
import logging

from app.db.session import get_db
from app.models.paper import Paper as PaperModel

router = APIRouter()

@router.get("/papers/counts", response_model=Dict[str, Any])
async def get_paper_counts(db: Session = Depends(get_db)):
    """
    Get counts of papers by category for dashboard metrics.
    """
    try:
        # Get total papers count
        total_count = db.query(func.count(PaperModel.id)).scalar()
        
        # Count papers with potential duplicates
        # Subquery to find papers with similar titles
        duplicate_titles = db.query(
            PaperModel.title,
            func.count(PaperModel.id).label('count')
        ).group_by(
            PaperModel.title
        ).having(
            func.count(PaperModel.id) > 1
        ).subquery()
        
        duplicate_count = db.query(
            func.count(PaperModel.id)
        ).join(
            duplicate_titles,
            PaperModel.title == duplicate_titles.c.title
        ).scalar()
        
        # Count papers with incomplete metadata
        incomplete_count = db.query(
            func.count(PaperModel.id)
        ).filter(
            or_(
                PaperModel.journal == None,
                PaperModel.journal == "",
                PaperModel.publication_date == None,
                PaperModel.abstract == None,
                PaperModel.abstract == "",
                PaperModel.authors == "[]"
            )
        ).scalar()
        
        # Count papers with missing PDFs
        missing_pdf_count = db.query(
            func.count(PaperModel.id)
        ).filter(
            or_(
                PaperModel.open_access_url == None,
                PaperModel.open_access_url == ""
            )
        ).scalar()
        
        # Count papers with available PDFs
        available_pdf_count = db.query(
            func.count(PaperModel.id)
        ).filter(
            PaperModel.open_access_url != None,
            PaperModel.open_access_url != ""
        ).scalar()
        
        return {
            "total": total_count,
            "duplicates": duplicate_count,
            "incomplete": incomplete_count,
            "missing_pdf": missing_pdf_count,
            "available_pdf": available_pdf_count
        }
        
    except Exception as e:
        logging.error(f"Error getting paper counts: {str(e)}")
        raise HTTPException(status_code=500, detail=f"Error getting paper counts: {str(e)}")
