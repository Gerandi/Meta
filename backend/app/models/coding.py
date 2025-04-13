from datetime import datetime
from sqlalchemy import Column, String, Text, Boolean, Integer, JSON, ForeignKey, DateTime
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class CodingSheet(Base):
    __tablename__ = 'codingsheet'
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    name = Column(String, index=True, nullable=False)
    description = Column(Text, nullable=True)
    sections = Column(JSON, nullable=False)  # List of CodingSection objects
    project_id = Column(Integer, ForeignKey("project.id"), nullable=False, index=True)
    
    # Relationships
    coding_data = relationship("CodingData", back_populates="sheet", cascade="all, delete-orphan")
    project = relationship("Project")


class CodingData(Base):
    __tablename__ = 'codingdata'
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    paper_id = Column(Integer, ForeignKey("paper.id"), nullable=False)
    sheet_id = Column(Integer, ForeignKey("codingsheet.id"), nullable=False)
    coder_id = Column(Integer, nullable=True)  # Will be foreign key in the future
    data = Column(JSON, nullable=False)  # Dictionary of field values
    
    # Relationships
    paper = relationship("Paper", back_populates="coding_data")
    sheet = relationship("CodingSheet", back_populates="coding_data")
