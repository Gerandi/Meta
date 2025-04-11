import os
from typing import List
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    API_V1_STR: str = "/api"
    
    # CORS
    BACKEND_CORS_ORIGINS: List[str] = ["http://localhost:5173"]  # Vue dev server
    
    # Database
    DATABASE_URL: str = "sqlite:///./metareview.db"
    
    # Set default keys - only use these if environment variables are not set
    OPENALEX_EMAIL: str = os.getenv("OPENALEX_EMAIL", "user@example.com")
    UNPAYWALL_EMAIL: str = os.getenv("UNPAYWALL_EMAIL", "user@example.com")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "development_secret_key")
    
    class Config:
        env_file = ".env"


settings = Settings()
