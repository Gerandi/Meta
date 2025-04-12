import logging
from sqlalchemy.orm import Session

from app.db.base_class import Base
from app.db.session import engine

# Make sure all models are imported
logger = logging.getLogger(__name__)


def init_db() -> None:
    """
    Initialize database tables.
    """
    # Import all models here to ensure they are registered with SQLAlchemy
    from app.models.paper import Paper
    from app.models.project import Project, paper_project
    from app.models.collection import Collection, paper_collection
    # Removed problematic import: from app.models.coding import Coding
    
    # Log all models being initialized
    logger.info("Initializing database with models: Paper, Project, Collection")
    
    # Log tables before creation using inspector
    from sqlalchemy import inspect
    inspector = inspect(engine)
    tables_before = set(inspector.get_table_names())
    logger.info(f"Tables before creation: {tables_before}")
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    
    # Log tables after creation
    tables_after = set(inspector.get_table_names())
    logger.info(f"Tables after creation: {tables_after}")
    
    # Log newly created tables
    new_tables = tables_after - tables_before
    if new_tables:
        logger.info(f"Newly created tables: {new_tables}")
    else:
        logger.info("No new tables were created")
        
    logger.info("Database initialization complete")


if __name__ == "__main__":
    init_db()
