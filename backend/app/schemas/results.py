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


class PaperSearchResult(BaseModel):
    id: Optional[int] = None
    title: str
    doi: Optional[str] = None
    url: Optional[str] = None
    journal: Optional[str] = None
    publication_date: Optional[datetime] = None
    authors: List[Dict[str, str]] = []
    is_open_access: bool = False
    abstract: Optional[str] = None
    open_access_url: Optional[str] = None
    source: str = "OpenAlex"
    
    class Config:
        from_attributes = True


class SearchResults(BaseModel):
    results: List[PaperSearchResult]
    total_results: int
    page: int = 1
    page_size: int = 10
    query: str = ""
