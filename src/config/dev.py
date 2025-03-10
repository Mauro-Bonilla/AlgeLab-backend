"""
Development settings for the AlgeLab application.

This module defines settings that are specific to the development environment.
These settings override the base settings when running in development mode.
"""

import os
from typing import List, Dict, Any

from src.config.base import Settings
from src.config import BASE_DIR


class DevSettings(Settings):
    """
    Development-specific settings.
    
    Inherits from base Settings and overrides values
    suitable for local development.
    """
    # Enable debug mode
    DEBUG: bool = True
    
    # Development URL settings
    FRONTEND_URL: str = "http://localhost:5173"
    GITHUB_REDIRECT_URI: str = "http://localhost:8000/api/auth/github/callback"
    
    # CORS settings for local development
    CORS_ALLOWED_ORIGINS: List[str] = [
        "http://localhost:5173",  # Frontend
        "http://localhost:3000",  # Alternative React port
        "http://127.0.0.1:5173",
        "http://127.0.0.1:3000",
    ]
    
    # Cookie settings for local development
    COOKIE_SECURE: bool = False  # Allow HTTP (not HTTPS) in development
    
    # Development log settings
    LOG_LEVEL: str = "DEBUG"
    
    # Documentation settings
    SHOW_SWAGGER: bool = True
    SWAGGER_UI_OAUTH2_REDIRECT_URL: str = "/api/docs/oauth2-redirect"
    
    # Development rate limiting settings
    RATE_LIMIT_ENABLED: bool = False  # Disable rate limiting in development
    
    # Development health check
    ENABLE_HEALTH_CHECK: bool = True
    
    # Load environment variables from development file
    class Config:
        env_file = os.path.join(BASE_DIR, ".env.development")
        env_file_encoding = "utf-8"
        case_sensitive = True