from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from app.schemas.paper import Paper


class ProjectBase(BaseModel):
    name: str
    description: Optional[str] = None


class ProjectCreate(ProjectBase):
    pass


class ProjectUpdate(ProjectBase):
    name: Optional[str] = None


class Project(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime
    papers: List[Paper] = []

    class Config:
        from_attributes = True


class ProjectWithPaperCount(ProjectBase):
    id: int
    created_at: datetime
    updated_at: datetime
    paper_count: int

    class Config:
        from_attributes = True
