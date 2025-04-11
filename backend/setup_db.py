import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Import models
from app.models.paper import Paper
from app.models.coding import CodingSheet, CodingData
from app.models.collection import Collection, paper_collection
from app.db.base_class import Base

# Create database engine
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./metareview.db")
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False})

# Create all tables
Base.metadata.create_all(bind=engine)

print("Database tables created successfully!")
