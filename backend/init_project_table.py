"""
Script to initialize just the Project table
"""
import logging
from sqlalchemy import inspect

from app.db.base_class import Base
from app.db.session import engine
# Explicitly import only the Project model
from app.models.project import Project, paper_project

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

def init_project_table():
    """Initialize just the Project table"""
    try:
        # Log tables before creation
        inspector = inspect(engine)
        tables_before = set(inspector.get_table_names())
        logger.info(f"Tables before creation: {tables_before}")
        
        # Create only the Project-related tables
        Project.__table__.create(bind=engine, checkfirst=True)
        paper_project.create(bind=engine, checkfirst=True)
        
        # Log tables after creation
        tables_after = set(inspector.get_table_names())
        logger.info(f"Tables after creation: {tables_after}")
        
        # Log newly created tables
        new_tables = tables_after - tables_before
        if new_tables:
            logger.info(f"Newly created tables: {new_tables}")
        else:
            logger.info("No new tables were created")
            
        logger.info("Project table initialization complete")
        
    except Exception as e:
        logger.error(f"Error initializing Project table: {str(e)}")

if __name__ == "__main__":
    init_project_table()
