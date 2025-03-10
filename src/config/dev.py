"""
Development settings for the AlgeLab application.

This module defines settings that are specific to the development environment.
These settings override the base settings when running in development mode.
"""

from typing import List, Optional, Union

from src.config.base import Settings
from pydantic import Field, field_validator

class DevSettings(Settings):
    """
    Development-specific settings.
    
    Inherits from base Settings and overrides values
    suitable for local development.
    """
    # Enable debug mode
     # Environment and Debugging
    ENVIRONMENT: str = "development"
    DEBUG: bool = False

    # Security
    SECRET_KEY: str = Field(..., description="Secret key for cryptographic operations")
    ALLOWED_HOSTS: List[str] = ["localhost", "127.0.0.1"]

    # CORS and CSRF
    CORS_ALLOWED_ORIGINS: List[str] = ["http://localhost:5173", "http://localhost:3000", "http://127.0.0.1:5173", "http://127.0.0.1:3000"]
    CSRF_TRUSTED_ORIGINS: List[str] = ["http://localhost:5173"]

    # Cookie Settings
    SESSION_COOKIE_SECURE: bool = False
    CSRF_COOKIE_SECURE: bool = False
    JWT_COOKIE_SECURE: bool = False
    JWT_COOKIE_SAMESITE: str = "Lax"

    # Frontend URL
    FRONTEND_URL: str = "http://localhost:5173"

    # GitHub OAuth
    GITHUB_APP_ID: Optional[str] = None
    GITHUB_CLIENT_ID: Optional[str] = None
    GITHUB_CLIENT_SECRET: Optional[str] = None
    GITHUB_REDIRECT_URI: Optional[str] = None
    GITHUB_PRIVATE_KEY: Optional[str] = None

    # Swagger/API Documentation
    SWAGGER_API_URL: str = "http://localhost:8000"

    # Database (Postgres/Supabase)
    POSTGRES_URL: Optional[str] = None
    POSTGRES_PRISMA_URL: Optional[str] = None
    NEXT_PUBLIC_SUPABASE_URL: Optional[str] = None
    POSTGRES_URL_NON_POOLING: Optional[str] = None
    SUPABASE_JWT_SECRET: Optional[str] = None
    POSTGRES_USER: str = "postgres"
    NEXT_PUBLIC_SUPABASE_ANON_KEY: Optional[str] = None
    POSTGRES_PASSWORD: Optional[str] = None
    POSTGRES_DATABASE: str = "postgres"
    SUPABASE_SERVICE_ROLE_KEY: Optional[str] = None
    POSTGRES_HOST: Optional[str] = None

    # Custom validators for CORS_ALLOWED_ORIGINS
    @field_validator("CORS_ALLOWED_ORIGINS", mode="before")
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        """Parse CORS_ALLOWED_ORIGINS from string to list."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError("CORS_ALLOWED_ORIGINS must be a list or a comma-separated string")

    # Pydantic configuration
    class Config:
        env_file = ".env.development"
        env_file_encoding = "utf-8"
        case_sensitive = True