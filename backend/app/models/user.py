from sqlalchemy import Column, Integer, String, Boolean, DateTime, ForeignKey
from sqlalchemy.orm import relationship
from datetime import datetime
from app.db.base_class import Base

class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True, index=True)
    email = Column(String, unique=True, index=True, nullable=False)
    hashed_password = Column(String, nullable=False)
    is_active = Column(Boolean(), default=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    # Relationships (add backrefs later if needed in other models)
    projects = relationship("Project", back_populates="owner", cascade="all, delete-orphan")
    # Add relationships for other user-owned data if necessary (e.g., directly owned papers if not via project)
    # coding_sheets = relationship("CodingSheet", back_populates="owner", cascade="all, delete-orphan")
