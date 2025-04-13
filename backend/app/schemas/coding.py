from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from enum import Enum


class FieldType(str, Enum):
    TEXT = "text"
    NUMBER = "number"
    SELECT = "select"
    BOOLEAN = "boolean"
    DATE = "date"
    TEXTAREA = "textarea"


class CodingField(BaseModel):
    name: str
    label: str
    type: FieldType
    required: bool = False
    description: Optional[str] = None
    options: Optional[List[str]] = None  # For SELECT type
    default_value: Optional[Any] = None


class CodingSection(BaseModel):
    name: str
    title: str
    description: Optional[str] = None
    fields: List[CodingField]


class CodingSheetBase(BaseModel):
    name: str
    description: Optional[str] = None
    sections: List[CodingSection]
    project_id: int


class CodingSheetCreate(CodingSheetBase):
    pass


class CodingSheet(CodingSheetBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Updated from orm_mode


class CodingDataBase(BaseModel):
    paper_id: int
    sheet_id: int
    coder_id: Optional[int] = None
    data: Dict[str, Any]  # Stores the actual coding data


class CodingDataCreate(CodingDataBase):
    pass


class CodingData(CodingDataBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Updated from orm_mode
