from sqlalchemy.orm import Session
from typing import List, Optional, Dict, Any
from sqlalchemy.exc import IntegrityError
from datetime import datetime

from app.models.coding import CodingSheet, CodingData
from app.models.paper import Paper, PaperStatus
from app.models.project import Project
from app.schemas.coding import CodingSheetCreate, CodingDataCreate
import logging

logger = logging.getLogger(__name__)

def create_coding_sheet_service(db: Session, coding_sheet: CodingSheetCreate, owner_id: int) -> CodingSheet:
    """
    Create a new coding sheet.
    
    Args:
        db: Database session
        coding_sheet: CodingSheet data
        
    Returns:
        The created CodingSheet object
    """
    try:
        db_sheet = CodingSheet(**coding_sheet.dict())
        db.add(db_sheet)
        db.commit()
        db.refresh(db_sheet)
        return db_sheet
    except IntegrityError as e:
        db.rollback()
        raise ValueError(f"Error creating coding sheet: {str(e)}")
    except Exception as e:
        db.rollback()
        raise Exception(f"Error creating coding sheet: {str(e)}")

def list_coding_sheets_service(db: Session, owner_id: int = None, project_id: int = None, skip: int = 0, limit: int = 100) -> List[CodingSheet]:
    """
    Get a list of all coding sheets.
    
    Args:
        db: Database session
        owner_id: Optional ID of the user to filter by
        project_id: Optional ID of the project to filter by
        skip: Number of records to skip
        limit: Maximum number of records to return
        
    Returns:
        List of CodingSheet objects
    """
    query = db.query(CodingSheet)
    
    if project_id:
        query = query.filter(CodingSheet.project_id == project_id)
        
    if owner_id:
        # Join with Project to filter by the project owner
        query = query.join(Project).filter(Project.owner_id == owner_id)
        
    return query.offset(skip).limit(limit).all()

def get_coding_sheet_service(db: Session, sheet_id: int) -> Optional[CodingSheet]:
    """
    Get a specific coding sheet by ID.
    
    Args:
        db: Database session
        sheet_id: ID of the coding sheet to retrieve
        
    Returns:
        CodingSheet object if found, None otherwise
    """
    return db.query(CodingSheet).filter(CodingSheet.id == sheet_id).first()

def update_coding_sheet_service(db: Session, sheet_id: int, coding_sheet_data: Dict[str, Any]) -> Optional[CodingSheet]:
    """
    Update a coding sheet.
    
    Args:
        db: Database session
        sheet_id: ID of the coding sheet to update
        coding_sheet_data: Data to update the coding sheet with
        
    Returns:
        Updated CodingSheet object if found, None otherwise
    """
    try:
        db_sheet = db.query(CodingSheet).filter(CodingSheet.id == sheet_id).first()
        if not db_sheet:
            return None
            
        # Update fields
        for key, value in coding_sheet_data.items():
            setattr(db_sheet, key, value)
            
        db.commit()
        db.refresh(db_sheet)
        return db_sheet
    except Exception as e:
        db.rollback()
        raise Exception(f"Error updating coding sheet: {str(e)}")

def delete_coding_sheet_service(db: Session, sheet_id: int) -> bool:
    """
    Delete a coding sheet.
    
    Args:
        db: Database session
        sheet_id: ID of the coding sheet to delete
        
    Returns:
        True if the coding sheet was deleted, False otherwise
    """
    try:
        db_sheet = db.query(CodingSheet).filter(CodingSheet.id == sheet_id).first()
        if not db_sheet:
            return False
            
        db.delete(db_sheet)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise Exception(f"Error deleting coding sheet: {str(e)}")

def create_coding_data_service(db: Session, coding_data: CodingDataCreate, coder_id: Optional[int] = None) -> CodingData:
    """
    Create a new coding data entry or update if it already exists.
    Also updates the paper status to 'coded' when coding data is saved.
    
    Args:
        db: Database session
        coding_data: CodingData to create
        
    Returns:
        The created/updated CodingData object
    """
    try:
        # Check if coding data already exists for this paper and sheet
        existing_data = db.query(CodingData).filter(
            CodingData.paper_id == coding_data.paper_id,
            CodingData.sheet_id == coding_data.sheet_id
        ).first()
        
        if existing_data:
            # Update existing data
            for key, value in coding_data.dict().items():
                setattr(existing_data, key, value)
            db.commit()
            db.refresh(existing_data)
            db_coding_data = existing_data
        else:
            # Create new data
            db_coding_data = CodingData(**coding_data.dict())
            db.add(db_coding_data)
            db.commit()
            db.refresh(db_coding_data)
        
        # Update the paper status to CODED
        paper = db.query(Paper).filter(Paper.id == coding_data.paper_id).first()
        if paper and paper.status != PaperStatus.CODED:
            paper.status = PaperStatus.CODED
            paper.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(paper)
            logger.info(f"Updated paper {paper.id} status to CODED")
        
        return db_coding_data
    except IntegrityError as e:
        db.rollback()
        logger.error(f"Integrity error saving coding data for paper {coding_data.paper_id}: {e}")
        raise ValueError(f"Error creating coding data: {str(e)}")
    except Exception as e:
        db.rollback()
        logger.error(f"Error saving coding data for paper {coding_data.paper_id}: {e}")
        raise Exception(f"Error creating coding data: {str(e)}")

def get_coding_data_service(db: Session, paper_id: int, sheet_id: Optional[int] = None, owner_id: Optional[int] = None) -> Optional[CodingData]:
    """
    Get coding data for a paper.
    
    Args:
        db: Database session
        paper_id: ID of the paper
        sheet_id: Optional ID of the coding sheet
        
    Returns:
        CodingData object if found, None otherwise
    """
    query = db.query(CodingData).filter(CodingData.paper_id == paper_id)
    
    if sheet_id:
        query = query.filter(CodingData.sheet_id == sheet_id)
        
    if owner_id:
        # Join with Paper to filter by owner
        query = query.join(Paper).filter(Paper.owner_id == owner_id)
        
    return query.first()

def update_coding_data_service(db: Session, coding_data_id: int, coding_data: Dict[str, Any], coder_id: Optional[int] = None) -> Optional[CodingData]:
    """
    Update coding data and set paper status to CODED.
    
    Args:
        db: Database session
        coding_data_id: ID of the coding data to update
        coding_data: Data to update
        
    Returns:
        Updated CodingData object if found, None otherwise
    """
    try:
        query = db.query(CodingData).filter(CodingData.id == coding_data_id)
        
        if coder_id is not None:
            # Only allow the coder to update their own coding data
            query = query.filter(CodingData.coder_id == coder_id)
        
        db_coding_data = query.first()
        if not db_coding_data:
            return None
            
        # Update fields
        for key, value in coding_data.items():
            setattr(db_coding_data, key, value)
            
        db.commit()
        db.refresh(db_coding_data)
        
        # Update the paper status to CODED
        paper = db.query(Paper).filter(Paper.id == db_coding_data.paper_id).first()
        if paper and paper.status != PaperStatus.CODED:
            paper.status = PaperStatus.CODED
            paper.updated_at = datetime.utcnow()
            db.commit()
            db.refresh(paper)
            logger.info(f"Updated paper {paper.id} status to CODED")
        
        return db_coding_data
    except Exception as e:
        db.rollback()
        logger.error(f"Error updating coding data: {e}")
        raise Exception(f"Error updating coding data: {str(e)}")

def delete_coding_data_service(db: Session, coding_data_id: int, coder_id: Optional[int] = None) -> bool:
    """
    Delete coding data.
    
    Args:
        db: Database session
        coding_data_id: ID of the coding data to delete
        
    Returns:
        True if the coding data was deleted, False otherwise
    """
    try:
        query = db.query(CodingData).filter(CodingData.id == coding_data_id)
        
        if coder_id is not None:
            # Only allow the coder to delete their own coding data
            query = query.filter(CodingData.coder_id == coder_id)
            
        db_coding_data = query.first()
        if not db_coding_data:
            return False
            
        db.delete(db_coding_data)
        db.commit()
        return True
    except Exception as e:
        db.rollback()
        raise Exception(f"Error deleting coding data: {str(e)}")

def get_coding_sheet_by_project_service(db: Session, project_id: int, owner_id: Optional[int] = None) -> Optional[CodingSheet]:
    """
    Get the coding sheet associated with a project.
    
    Args:
        db: Database session
        project_id: ID of the project
        
    Returns:
        CodingSheet object if found, None otherwise
    """
    query = db.query(CodingSheet).filter(CodingSheet.project_id == project_id)
    
    if owner_id:
        # Join with Project to filter by the project owner
        query = query.join(Project).filter(Project.owner_id == owner_id)
        
    return query.first()
