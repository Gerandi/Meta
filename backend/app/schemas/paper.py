from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime


class Author(BaseModel):
    name: str
    affiliation: Optional[str] = None


class PaperBase(BaseModel):
    title: str
    abstract: Optional[str] = None
    doi: Optional[str] = None
    authors: List[Author] = []
    publication_date: Optional[datetime] = None
    journal: Optional[str] = None
    volume: Optional[str] = None
    issue: Optional[str] = None
    pages: Optional[str] = None
    publisher: Optional[str] = None
    url: Optional[str] = None
    keywords: List[str] = []
    is_open_access: bool = False
    open_access_url: Optional[str] = None


class PaperCreate(PaperBase):
    pass


class PaperSearch(BaseModel):
    query: str
    fields: List[str] = ["title", "abstract", "authors", "keywords"]
    year_from: Optional[int] = None
    year_to: Optional[int] = None
    journal: Optional[str] = None
    open_access_only: bool = False


class Paper(PaperBase):
    id: int
    created_at: datetime
    updated_at: datetime

    class Config:
        from_attributes = True  # Updated from orm_mode


class PaperSearchResponse(BaseModel):
    results: List[Paper]
    totalResults: int
