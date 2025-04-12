import logging
from sqlalchemy.orm import Session
from sqlalchemy import inspect

from app.db.base_class import Base
from app.db.session import engine

logger = logging.getLogger(__name__)


def init_db() -> None:
    """
    Initialize database tables.
    """
    # Import necessary models ONLY
    from app.models.paper import Paper
    from app.models.project import Project, paper_project
    from app.models.coding import CodingSheet, CodingData # Keep coding models


    
    logger.info("Initializing database with models: Paper, Project, CodingSheet, CodingData")
    
    inspector = inspect(engine)
    tables_before = set(inspector.get_table_names())
    logger.info(f"Tables before creation: {tables_before}")
    
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine, checkfirst=True) # Use checkfirst=True
    
    tables_after = set(inspector.get_table_names())
    logger.info(f"Tables after creation: {tables_after}")
    
    new_tables = tables_after - tables_before
    if new_tables:
        logger.info(f"Newly created tables: {new_tables}")
    else:
        logger.info("No new tables were created (or they already existed)")
        
    logger.info("Database initialization complete")


if __name__ == "__main__":
    init_db()
