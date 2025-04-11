from typing import Any
from datetime import datetime

from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, DateTime

# Create a simple declarative base without annotation issues
Base = declarative_base()

# Add common columns directly through __table_args__ in models
# This avoids the type annotation errors with newer SQLAlchemy
