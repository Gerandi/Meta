from fastapi import APIRouter, Depends, HTTPException, Query, Path
from typing import List, Optional
from sqlalchemy.orm import Session

from app.schemas.coding import CodingSheet, CodingSheetCreate, CodingData, CodingDataCreate
from app.services.coding_service import (
    create_coding_sheet_service, 
    list_coding_sheets_service, 
    get_coding_sheet_service,
    update_coding_sheet_service,
    delete_coding_sheet_service,
    create_coding_data_service,
    get_coding_data_service,
    update_coding_data_service,
    delete_coding_data_service,
    get_coding_sheet_by_project_service
)
from app.db.session import get_db
from app.api import deps
from app.models.user import User as UserModel

router = APIRouter()


@router.post("/sheets", response_model=CodingSheet)
async def create_coding_sheet(
    coding_sheet: CodingSheetCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(deps.get_current_active_user),
):
    """
    Create a new coding sheet template.
    """
    try:
        return create_coding_sheet_service(db, coding_sheet, owner_id=current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sheets", response_model=List[CodingSheet])
async def list_coding_sheets(
    skip: int = Query(0, description="Number of sheets to skip"),
    limit: int = Query(100, description="Maximum number of sheets to return"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(deps.get_current_active_user),
):
    """
    List all coding sheet templates for projects owned by the current user.
    """
    return list_coding_sheets_service(db, owner_id=current_user.id, skip=skip, limit=limit)


@router.get("/sheets/{sheet_id}", response_model=CodingSheet)
async def get_coding_sheet(
    sheet_id: int = Path(..., description="The ID of the sheet to retrieve"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(deps.get_current_active_user),
):
    """
    Get a specific coding sheet by ID that belongs to a project owned by the current user.
    """
    sheet = get_coding_sheet_service(db, sheet_id)
    if not sheet:
        raise HTTPException(status_code=404, detail="Coding sheet not found")
        
    # Additional check to make sure sheet belongs to the user's project
    project_sheets = list_coding_sheets_service(db, owner_id=current_user.id)
    if sheet.id not in [s.id for s in project_sheets]:
        raise HTTPException(status_code=403, detail="Not authorized to access this coding sheet")
        
    return sheet


@router.put("/sheets/{sheet_id}", response_model=CodingSheet)
async def update_coding_sheet(
    sheet_id: int = Path(..., description="The ID of the sheet to update"),
    coding_sheet: CodingSheetCreate = None,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(deps.get_current_active_user),
):
    """
    Update a specific coding sheet that belongs to a project owned by the current user.
    """
    try:
        # Verify the sheet belongs to the user's project
        project_sheets = list_coding_sheets_service(db, owner_id=current_user.id)
        if sheet_id not in [s.id for s in project_sheets]:
            raise HTTPException(status_code=403, detail="Not authorized to update this coding sheet")
            
        updated_sheet = update_coding_sheet_service(db, sheet_id, coding_sheet.dict())
        if not updated_sheet:
            raise HTTPException(status_code=404, detail="Coding sheet not found")
        return updated_sheet
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/sheets/{sheet_id}", status_code=204)
async def delete_coding_sheet(
    sheet_id: int = Path(..., description="The ID of the sheet to delete"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(deps.get_current_active_user),
):
    """
    Delete a specific coding sheet that belongs to a project owned by the current user.
    """
    try:
        # Verify the sheet belongs to the user's project
        project_sheets = list_coding_sheets_service(db, owner_id=current_user.id)
        if sheet_id not in [s.id for s in project_sheets]:
            raise HTTPException(status_code=403, detail="Not authorized to delete this coding sheet")
            
        success = delete_coding_sheet_service(db, sheet_id)
        if not success:
            raise HTTPException(status_code=404, detail="Coding sheet not found")
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.post("/data", response_model=CodingData)
async def create_coding_data(
    coding_data: CodingDataCreate,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(deps.get_current_active_user),
):
    """
    Save coding data for a paper.
    """
    try:
        # Verify the sheet belongs to the user's project
        project_sheets = list_coding_sheets_service(db, owner_id=current_user.id)
        if coding_data.sheet_id not in [s.id for s in project_sheets]:
            raise HTTPException(status_code=403, detail="Not authorized to use this coding sheet")
            
        return create_coding_data_service(db, coding_data, coder_id=current_user.id)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/data/{paper_id}", response_model=CodingData)
async def get_coding_data(
    paper_id: int = Path(..., description="The ID of the paper"),
    sheet_id: Optional[int] = Query(None, description="Optional coding sheet ID"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(deps.get_current_active_user),
):
    """
    Get coding data for a specific paper that belongs to the current user.
    """
    data = get_coding_data_service(db, paper_id, sheet_id, owner_id=current_user.id)
    if not data:
        raise HTTPException(status_code=404, detail="Coding data not found")
    return data


@router.put("/data/{coding_data_id}", response_model=CodingData)
async def update_coding_data(
    coding_data_id: int = Path(..., description="The ID of the coding data to update"),
    coding_data: CodingDataCreate = None,
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(deps.get_current_active_user),
):
    """
    Update coding data created by the current user.
    """
    try:
        updated_data = update_coding_data_service(db, coding_data_id, coding_data.dict(), coder_id=current_user.id)
        if not updated_data:
            raise HTTPException(status_code=404, detail="Coding data not found or not created by you")
        return updated_data
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.delete("/data/{coding_data_id}", status_code=204)
async def delete_coding_data(
    coding_data_id: int = Path(..., description="The ID of the coding data to delete"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(deps.get_current_active_user),
):
    """
    Delete coding data created by the current user.
    """
    try:
        success = delete_coding_data_service(db, coding_data_id, coder_id=current_user.id)
        if not success:
            raise HTTPException(status_code=404, detail="Coding data not found or not created by you")
        return None
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@router.get("/sheets/project/{project_id}", response_model=CodingSheet)
async def get_coding_sheet_by_project(
    project_id: int = Path(..., description="The ID of the project"),
    db: Session = Depends(get_db),
    current_user: UserModel = Depends(deps.get_current_active_user),
):
    """
    Get the coding sheet associated with a project owned by the current user.
    """
    sheet = get_coding_sheet_by_project_service(db, project_id, owner_id=current_user.id)
    if not sheet:
        raise HTTPException(status_code=404, detail="No coding sheet found for this project or not authorized to access it")
    return sheet
