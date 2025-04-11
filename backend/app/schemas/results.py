from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any
from datetime import datetime


class ResultColumn(BaseModel):
    name: str
    label: str
    data_type: str  # text, number, date, etc.
    description: Optional[str] = None


class ResultRow(BaseModel):
    paper_id: int
    values: Dict[str, Any]  # Column name to value mapping


class ResultsTable(BaseModel):
    columns: List[ResultColumn]
    rows: List[ResultRow]
    total_rows: int
    page: int = 1
    page_size: int = 50


class ResultsExport(BaseModel):
    data: str  # Base64 encoded file content
    filename: str
    mime_type: str  # application/csv, application/vnd.openxmlformats-officedocument.spreadsheetml.sheet, etc.
