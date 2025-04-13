from datetime import datetime
from sqlalchemy import Column, String, Text, Table, ForeignKey, DateTime, Integer, func
from sqlalchemy.orm import relationship

from app.db.base_class import Base


# Association table for many-to-many relationship between papers and projects
paper_project = Table(
    "paper_project",
    Base.metadata,
    Column("paper_id", ForeignKey("paper.id"), primary_key=True),
    Column("project_id", ForeignKey("project.id"), primary_key=True),
)


class Project(Base):
    """Project model for grouping papers together."""
    __tablename__ = 'project'
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    # Owner relationship
    owner_id = Column(Integer, ForeignKey("user.id"), nullable=False)
    owner = relationship("User", back_populates="projects")
    
    # Relationships
    papers = relationship("Paper", secondary=paper_project, backref="projects")
