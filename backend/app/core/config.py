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
    CROSSREF_EMAIL: str = os.getenv("CROSSREF_EMAIL", "metareview@example.com")
    SCOPUS_API_KEY: str = os.getenv("SCOPUS_API_KEY", "fba37f1f78cf589c198c81c8bdf035f3")
    EXA_API_KEY: str = os.getenv("EXA_API_KEY", "80297ab6-7f57-4bf7-88f9-d9369d23404c")
    
    # Security
    SECRET_KEY: str = os.getenv("SECRET_KEY", "development_secret_key")
    
    class Config:
        env_file = ".env"


settings = Settings()
