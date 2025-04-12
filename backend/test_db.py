"""
Test script to directly create a project in the database
"""
import logging
from sqlalchemy.orm import Session
from sqlalchemy import inspect
from datetime import datetime

from app.db.session import SessionLocal, engine
from app.models.project import Project

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def create_test_project():
    """Create a test project directly in the database"""
    db = SessionLocal()
    try:
        # Check if the project table exists using inspector
        inspector = inspect(engine)
        if "project" not in inspector.get_table_names():
            logger.error("Project table does not exist in the database!")
            return
            
        logger.info("Creating test project directly in database")
        
        # Create a new project
        test_project = Project(
            name="Test Project - Direct DB Insert",
            description="This project was created directly via a test script",
            created_at=datetime.utcnow(),
            updated_at=datetime.utcnow()
        )
        
        # Add and commit
        db.add(test_project)
        db.commit()
        db.refresh(test_project)
        
        logger.info(f"Test project created successfully with ID: {test_project.id}")
        
        # Verify we can retrieve it
        projects = db.query(Project).all()
        logger.info(f"Total projects in database: {len(projects)}")
        for p in projects:
            logger.info(f"Project: id={p.id}, name={p.name}")
            
    except Exception as e:
        logger.exception(f"Error creating test project: {str(e)}")
    finally:
        db.close()

if __name__ == "__main__":
    create_test_project()
