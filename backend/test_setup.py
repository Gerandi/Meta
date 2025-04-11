"""
Simple script to test the database setup.
"""

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

# Create a connection to the database
engine = create_engine("sqlite:///./metareview.db", connect_args={"check_same_thread": False})
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# Create a session
session = SessionLocal()

# Try to perform a basic query 
try:
    # Try to get the first collection
    result = session.execute("SELECT 1").fetchone()
    print("✅ Database connection successful!")
    
    # Check if tables exist
    result = session.execute("SELECT name FROM sqlite_master WHERE type='table'").fetchall()
    print(f"Tables in database: {[row[0] for row in result]}")
    
except Exception as e:
    print(f"❌ Error connecting to database: {e}")
finally:
    session.close()
