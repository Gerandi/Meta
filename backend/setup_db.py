import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy import inspect # Import inspect

# Import models needed
from app.models.paper import Paper
from app.models.project import Project, paper_project # Ensure association table is imported
from app.models.coding import CodingSheet, CodingData # Keep coding models
from app.db.base_class import Base

# Create database engine
DATABASE_URL = os.getenv("DATABASE_URL", "sqlite:///./metareview.db")
# Add echo=True for debugging SQL
engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False}, echo=True)

# Log tables before creation
inspector = inspect(engine)
print(f"Tables before creation: {inspector.get_table_names()}")

# Create all tables for imported models inheriting from Base
Base.metadata.create_all(bind=engine)

# Log tables after creation
print(f"Tables after creation: {inspector.get_table_names()}")
print("Database tables created/verified successfully!")
