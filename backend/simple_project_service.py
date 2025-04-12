"""
Simplified project service to avoid dependencies
"""
import logging
from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey, Table
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import relationship, sessionmaker
from sqlalchemy import create_engine
from datetime import datetime
import json

# Set up logging
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Create a database engine
engine = create_engine('sqlite:///./simple_metareview.db')
Base = declarative_base()
Session = sessionmaker(bind=engine)

# Define the models directly here
paper_project = Table(
    "paper_project",
    Base.metadata,
    Column("paper_id", Integer, ForeignKey("paper.id"), primary_key=True),
    Column("project_id", Integer, ForeignKey("project.id"), primary_key=True),
)

class Paper(Base):
    __tablename__ = 'paper'
    
    id = Column(Integer, primary_key=True, index=True)
    title = Column(String, nullable=False)
    
class Project(Base):
    __tablename__ = 'project'
    
    id = Column(Integer, primary_key=True, index=True)
    created_at = Column(DateTime, default=datetime.utcnow)
    updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow)
    name = Column(String, nullable=False, index=True)
    description = Column(Text, nullable=True)
    
    papers = relationship("Paper", secondary=paper_project, backref="projects")

def setup_database():
    """Create the tables"""
    try:
        Base.metadata.create_all(bind=engine)
        logger.info("Database tables created successfully")
    except Exception as e:
        logger.error(f"Error creating tables: {str(e)}")

def create_project(name, description=""):
    """Create a new project"""
    session = Session()
    try:
        project = Project(name=name, description=description)
        session.add(project)
        session.commit()
        
        # Return a dict that can be converted to JSON
        result = {
            "id": project.id,
            "name": project.name,
            "description": project.description,
            "created_at": project.created_at.isoformat(),
            "updated_at": project.updated_at.isoformat()
        }
        
        logger.info(f"Created project: {result}")
        return result
    except Exception as e:
        session.rollback()
        logger.error(f"Error creating project: {str(e)}")
        raise
    finally:
        session.close()

def list_projects():
    """List all projects"""
    session = Session()
    try:
        projects = session.query(Project).all()
        
        # Convert to JSON-compatible format
        result = []
        for project in projects:
            result.append({
                "id": project.id,
                "name": project.name,
                "description": project.description,
                "created_at": project.created_at.isoformat(),
                "updated_at": project.updated_at.isoformat(),
                "paper_count": len(project.papers)
            })
        
        logger.info(f"Listed {len(result)} projects")
        return result
    except Exception as e:
        logger.error(f"Error listing projects: {str(e)}")
        return []
    finally:
        session.close()

if __name__ == "__main__":
    # Setup the database
    setup_database()
    
    # Create a test project
    project = create_project("Simple Test Project", "This is a test project")
    print(json.dumps(project, indent=2))
    
    # List all projects
    projects = list_projects()
    print(json.dumps(projects, indent=2))
