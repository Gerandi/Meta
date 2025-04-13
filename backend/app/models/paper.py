from datetime import datetime
from sqlalchemy import Column, String, Text, Boolean, DateTime, JSON, ForeignKey, Integer, Enum as SQLAlchemyEnum
import enum
from sqlalchemy.orm import relationship

from app.db.base_class import Base


class PaperStatus(str, enum.Enum):
    IMPORTED = "imported"      # Newly imported, not yet added to a project
    PROCESSING = "processing"  # Added to project, undergoing cleanup/PDF retrieval
    READY_TO_CODE = "ready_to_code" # Processed, has PDF, ready for coding
    CODING_IN_PROGRESS = "coding_in_progress" # Being actively coded
    CODED = "coded"            # Coding complete


class Paper(Base):
    __tablename__ = 'paper'
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    title = Column(String, index=True, nullable=False)
    abstract = Column(Text, nullable=True)
    doi = Column(String, unique=True, index=True, nullable=True)
    authors = Column(JSON, nullable=False, default=list)  # List of Author objects
    publication_date = Column(DateTime, nullable=True)
    journal = Column(String, nullable=True)
    volume = Column(String, nullable=True)
    issue = Column(String, nullable=True)
    pages = Column(String, nullable=True)
    publisher = Column(String, nullable=True)
    url = Column(String, nullable=True)
    keywords = Column(JSON, nullable=False, default=list)  # List of strings
    is_open_access = Column(Boolean, default=False)
    open_access_url = Column(String, nullable=True)
    file_path = Column(String, nullable=True)  # Store path to locally saved PDF
    status = Column(SQLAlchemyEnum(PaperStatus), default=PaperStatus.IMPORTED, nullable=False, index=True)
    
    # Relationships
    coding_data = relationship("CodingData", back_populates="paper", cascade="all, delete-orphan")
