from datetime import datetime
from sqlalchemy import Column, String, Text, Table, ForeignKey, DateTime, Integer, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base


# Association table for many-to-many relationship between papers and collections
paper_collection = Table(
    "paper_collection",
    Base.metadata,
    Column("paper_id", ForeignKey("paper.id"), primary_key=True),
    Column("collection_id", ForeignKey("collection.id"), primary_key=True),
)


class Collection(Base):
    """Collection model for grouping papers together."""
    __tablename__ = 'collection'
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Relationships
    papers = relationship("Paper", secondary=paper_collection, backref="collections")
