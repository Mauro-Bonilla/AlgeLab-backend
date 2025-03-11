"""
API routes configuration for the application.

This module aggregates all API routes from different modules
and provides a centralized router for the FastAPI application.
"""

from fastapi import APIRouter

from src.api.auth import router as auth_router
from src.api.users import router as users_router

# Create main API router
api_router = APIRouter()

# Include all routers
api_router.include_router(auth_router, prefix="/auth")
api_router.include_router(users_router, prefix="/user")