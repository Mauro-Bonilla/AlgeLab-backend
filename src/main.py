"""
Main application entry point for AlgeLab API.

This module initializes the FastAPI application, configures middleware,
sets up routes, and handles startup/shutdown events.
"""

import logging
from fastapi import FastAPI, Depends
from contextlib import asynccontextmanager

from src.config import get_settings
from src.config.middleware import setup_middleware
from src.config.logging import configure_logging
from src.config.constants import API_V1_STR
from src.api.routes import api_router
from src.exceptions import add_exception_handlers
from src.db.client import get_db_client

# Load settings based on environment
settings = get_settings()

# Configure logging
loggers = configure_logging()
logger = logging.getLogger("algelab.main")


@asynccontextmanager
async def lifespan(app: FastAPI):
    # Startup logic
    env_type = settings.model_config["env_file"].split(".")[-1]
    logger.info(f"Starting AlgeLab API in {env_type} mode")
    db_client = get_db_client()
    logger.info(f"{settings.PROJECT_NAME} API started successfully")
    
    yield
    
    # Shutdown logic
    logger.info(f"{settings.PROJECT_NAME} API shutting down")


# Create FastAPI app
app = FastAPI(
    title=settings.PROJECT_NAME,
    description=settings.PROJECT_DESCRIPTION,
    version=settings.VERSION,
    docs_url="/swagger" if settings.SHOW_SWAGGER else None,
    redoc_url="/redoc" if settings.SHOW_SWAGGER else None,
    lifespan=lifespan,
)

# Set up middleware
setup_middleware(app)

# Register exception handlers
add_exception_handlers(app)

# Include API router
app.include_router(api_router, prefix=API_V1_STR)


# Health check endpoint
@app.get("/health", tags=["health"])
async def health_check():
    """Health check endpoint to verify API is running."""
    return {
        "status": "healthy",
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "environment": settings.model_config["env_file"].split(".")[-1]
    }


# Root endpoint
@app.get("/", tags=["root"])
async def root():
    """Root endpoint returning basic API information."""
    return {
        "name": settings.PROJECT_NAME,
        "version": settings.VERSION,
        "description": settings.PROJECT_DESCRIPTION,
        "environment": settings.model_config["env_file"].split(".")[-1],
        "docs": "/swagger" if settings.SHOW_SWAGGER else None,
    }


if __name__ == "__main__":
    import uvicorn
    
    logger.info(f"Starting AlgeLab API in {settings.model_config['env_file'].split('.')[-1]} mode")
    
    uvicorn.run(
        "src.main:app",
        host="0.0.0.0",
        port=8000,
        reload=settings.DEBUG
    )