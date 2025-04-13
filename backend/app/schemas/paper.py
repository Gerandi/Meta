from pydantic import BaseModel, Field
from typing import List, Optional, Dict, Any, Union
from datetime import datetime
from app.models.paper import PaperStatus  # Import the enum


class Author(BaseModel):
    name: str = Field(..., description="Author's full name")
    affiliation: Optional[str] = Field(None, description="Author's institutional affiliation")
    
    class Config:
        schema_extra = {
            "example": {
                "name": "Jane Smith",
                "affiliation": "University of Science"
            }
        }


class PaperBase(BaseModel):
    title: str = Field(..., description="Title of the paper")
    abstract: Optional[str] = Field(None, description="Abstract or summary of the paper")
    doi: Optional[str] = Field(None, description="DOI in https://doi.org/format as provided by OpenAlex")
    authors: List[Author] = Field(default=[], description="List of authors with their affiliations")
    publication_date: Optional[datetime] = Field(None, description="Publication date (YYYY-MM-DD)")
    journal: Optional[str] = Field(None, description="Journal or publication venue name")
    volume: Optional[str] = Field(None, description="Volume number")
    issue: Optional[str] = Field(None, description="Issue number")
    pages: Optional[str] = Field(None, description="Page range (e.g., '123-145')")
    publisher: Optional[str] = Field(None, description="Publisher name")
    url: Optional[str] = Field(None, description="URL to the publication")
    keywords: List[str] = Field(default=[], description="Subject keywords or concepts from OpenAlex")
    is_open_access: bool = Field(False, description="Whether this paper is available via open access")
    open_access_url: Optional[str] = Field(None, description="URL to open access version if available")
    citation_count: Optional[int] = Field(None, description="Number of citations according to OpenAlex")
    references_count: Optional[int] = Field(None, description="Number of references in the paper")
    source: Optional[str] = Field("OpenAlex", description="Data source for this paper record")
    file_path: Optional[str] = Field(None, description="Path to the locally stored PDF file, if any")
    status: PaperStatus = Field(PaperStatus.IMPORTED, description="Current status of the paper in the workflow")


class PaperCreate(PaperBase):
    status: Optional[PaperStatus] = Field(PaperStatus.IMPORTED, description="Current status of the paper in the workflow")
    class Config:
        schema_extra = {
            "example": {
                "title": "The impact of climate change on biodiversity",
                "abstract": "This paper examines the effects of climate change on global biodiversity...",
                "doi": "https://doi.org/10.1234/example.5678",
                "authors": [
                    {"name": "Jane Smith", "affiliation": "University of Science"},
                    {"name": "John Doe", "affiliation": "Research Institute"}
                ],
                "publication_date": "2023-01-15T00:00:00",
                "journal": "Journal of Environmental Research",
                "volume": "45",
                "issue": "2",
                "pages": "123-145",
                "publisher": "Academic Press",
                "keywords": ["climate change", "biodiversity", "ecology"],
                "is_open_access": True,
                "open_access_url": "https://repository.example.org/paper.pdf"
            }
        }


class PaperUpdate(BaseModel):
    title: Optional[str] = Field(None, description="Title of the paper")
    abstract: Optional[str] = Field(None, description="Abstract or summary of the paper")
    doi: Optional[str] = Field(None, description="DOI in https://doi.org/format as provided by OpenAlex")
    authors: Optional[List[Author]] = Field(None, description="List of authors with their affiliations")
    publication_date: Optional[datetime] = Field(None, description="Publication date (YYYY-MM-DD)")
    journal: Optional[str] = Field(None, description="Journal or publication venue name")
    volume: Optional[str] = Field(None, description="Volume number")
    issue: Optional[str] = Field(None, description="Issue number")
    pages: Optional[str] = Field(None, description="Page range (e.g., '123-145')")
    publisher: Optional[str] = Field(None, description="Publisher name")
    url: Optional[str] = Field(None, description="URL to the publication")
    keywords: Optional[List[str]] = Field(None, description="Subject keywords or concepts from OpenAlex")
    is_open_access: Optional[bool] = Field(None, description="Whether this paper is available via open access")
    open_access_url: Optional[str] = Field(None, description="URL to open access version if available")
    citation_count: Optional[int] = Field(None, description="Number of citations according to OpenAlex")
    references_count: Optional[int] = Field(None, description="Number of references in the paper")
    status: Optional[PaperStatus] = Field(None, description="Current status of the paper in the workflow")


class PaperSearch(BaseModel):
    query: str = Field(..., description="Search query text")
    fields: List[str] = Field(["title", "abstract", "authors", "keywords"], description="Fields to search in")
    year_from: Optional[int] = Field(None, description="Start year for filtering")
    year_to: Optional[int] = Field(None, description="End year for filtering")
    journal: Optional[str] = Field(None, description="Filter by journal name")
    author: Optional[str] = Field(None, description="Filter by author name")
    open_access_only: bool = Field(False, description="Filter to only open access papers")
    sort_by: str = Field("relevance", description="Sort order (relevance, date, cited, title)")


class Paper(PaperBase):
    id: int = Field(..., description="Database ID for this paper")
    created_at: datetime = Field(..., description="Timestamp when this record was created")
    updated_at: datetime = Field(..., description="Timestamp when this record was last updated")
    status: PaperStatus = Field(..., description="Current status of the paper in the workflow")

    class Config:
        from_attributes = True  # Updated from orm_mode
        schema_extra = {
            "example": {
                "id": 1,
                "title": "The impact of climate change on biodiversity",
                "abstract": "This paper examines the effects of climate change on global biodiversity...",
                "doi": "https://doi.org/10.1234/example.5678",
                "authors": [
                    {"name": "Jane Smith", "affiliation": "University of Science"},
                    {"name": "John Doe", "affiliation": "Research Institute"}
                ],
                "publication_date": "2023-01-15T00:00:00",
                "journal": "Journal of Environmental Research",
                "volume": "45",
                "issue": "2",
                "pages": "123-145", 
                "publisher": "Academic Press",
                "url": "https://doi.org/10.1234/example.5678",
                "keywords": ["climate change", "biodiversity", "ecology"],
                "is_open_access": True,
                "open_access_url": "https://repository.example.org/paper.pdf",
                "citation_count": 42,
                "references_count": 56,
                "source": "OpenAlex",
                "created_at": "2023-04-10T14:32:10.123456",
                "updated_at": "2023-04-10T14:32:10.123456"
            }
        }


class PaperSearchResponse(BaseModel):
    results: List[Paper] = Field(..., description="List of papers matching the search criteria")
    totalResults: int = Field(..., description="Total number of results available in OpenAlex")
    
    class Config:
        schema_extra = {
            "example": {
                "results": [
                    {
                        "id": 1,
                        "title": "The impact of climate change on biodiversity",
                        "doi": "https://doi.org/10.1234/example.5678",
                        "authors": [
                            {"name": "Jane Smith", "affiliation": "University of Science"}
                        ],
                        "publication_date": "2023-01-15T00:00:00",
                        "journal": "Journal of Environmental Research",
                        "is_open_access": True,
                        "citation_count": 42,
                        "source": "OpenAlex"
                    }
                ],
                "totalResults": 1542
            }
        }
