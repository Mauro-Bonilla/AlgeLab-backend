"""
Main application entry point for AlgeLab API.

This module initializes the FastAPI application, configures middleware,
sets up routes, and includes a Supabase connection test.
"""

import logging
from fastapi import FastAPI, Depends, HTTPException, status
from fastapi.responses import JSONResponse

from src.config import get_settings
from src.config.middleware import setup_middleware
from src.config.logging import configure_logging

# Load settings based on environment
settings = get_settings()

# Configure logging
loggers = configure_logging()
logger = logging.getLogger("algelab.main")

# Create FastAPI app
app = FastAPI(
    title="AlgeLab API",
    description="API for AlgeLab - Linear Algebra Learning Platform",
    version="1.0.0",
    docs_url="/swagger" if getattr(settings, "SHOW_SWAGGER", False) else None,
    redoc_url="/redoc" if getattr(settings, "SHOW_SWAGGER", False) else None,
)

setup_middleware(app)

# Root endpoint
@app.get("/")
async def root():
    """Root endpoint returning basic API information."""
    return {
        "name": settings.PROJECT_NAME,
        "version": getattr(settings, "VERSION", "1.0.0"),
        "description": getattr(settings, "PROJECT_DESCRIPTION", "AlgeLab API"),
        "environment": settings.Config.env_file.split(".")[-1],
    }

if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting AlgeLab API in {settings.Config.env_file.split('.')[-1]} mode")
    
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )
