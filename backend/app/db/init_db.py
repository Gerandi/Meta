import logging
from sqlalchemy.orm import Session

from app.db.base_class import Base
from app.db.session import engine
from app.models import paper, coding
from app.models.collection import Collection, paper_collection

# Make sure all models are imported
logger = logging.getLogger(__name__)


def init_db() -> None:
    """
    Initialize database tables.
    """
    # Create tables if they don't exist
    Base.metadata.create_all(bind=engine)
    logger.info("Database initialized")


if __name__ == "__main__":
    init_db()
