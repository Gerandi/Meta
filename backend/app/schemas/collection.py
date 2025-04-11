from pydantic import BaseModel
from typing import List, Optional
from datetime import datetime

from app.schemas.paper import Paper


class CollectionBase(BaseModel):
    name: str
    description: Optional[str] = None


class CollectionCreate(CollectionBase):
    pass


class CollectionUpdate(CollectionBase):
    name: Optional[str] = None


class Collection(CollectionBase):
    id: int
    created_at: datetime
    updated_at: datetime
    papers: List[Paper] = []

    class Config:
        from_attributes = True


class CollectionWithPaperCount(CollectionBase):
    id: int
    created_at: datetime
    updated_at: datetime
    paper_count: int

    class Config:
        from_attributes = True
