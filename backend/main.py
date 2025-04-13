import uvicorn
from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.exceptions import RequestValidationError
from fastapi.responses import JSONResponse
import logging

from app.api.api import api_router
from app.core.config import settings
from app.db.init_db import init_db

logger = logging.getLogger(__name__)

app = FastAPI(
    title="MetaReview API",
    description="API for MetaReview - A meta-analysis tool for researchers",
    version="0.1.0",
)

# CORS middleware - Updated allow_origins
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins in development
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Initialize database on startup
@app.on_event("startup")
def on_startup():
    logger.info("Running database initialization on startup...")
    init_db()
    logger.info("Database initialization complete.")

# Add validation error handler
@app.exception_handler(RequestValidationError)
async def validation_exception_handler(request: Request, exc: RequestValidationError):
    error_details = str(exc)
    logger.error(f"Validation error: {error_details}")
    # Log the request body if possible/safe
    try:
        body = await request.json()
        logger.error(f"Request body: {body}")
    except Exception:
        logger.error("Could not parse request body.")
    logger.error(f"Full exception details: {exc.errors()}")
    return JSONResponse(
        status_code=422,
        content={
            "detail": "Request validation error",
            "errors": exc.errors(),
            "message": "Check the server logs for details"
        }
    )

# General exception handler
@app.exception_handler(Exception)
async def general_exception_handler(request: Request, exc: Exception):
    logger.exception(f"Unhandled exception during request to {request.url.path}: {str(exc)}")
    return JSONResponse(
        status_code=500,
        content={
            "detail": "Internal server error",
            "message": str(exc) # Provide exception message in response for debugging
        }
    )

# Include all API routes
app.include_router(api_router, prefix="")

if __name__ == "__main__":
    # Ensure the host is correct for accessibility if running in Docker later
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
