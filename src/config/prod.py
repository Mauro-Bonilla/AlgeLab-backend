"""
Production settings for the AlgeLab application.

This module defines settings that are specific to the production environment.
These settings override the base settings when running in production mode.
"""

import os
from typing import List, Dict, Any

from pydantic import Field, field_validator

from src.config.base import Settings
from src.config import BASE_DIR


class ProdSettings(Settings):
    """
    Production-specific settings.
    
    Inherits from base Settings and overrides values
    suitable for production deployment.
    """
    # Disable debug mode
    DEBUG: bool = Field(False, description="Debug mode is always disabled in production")
    
    # Production URL settings
    FRONTEND_URL: str = Field(..., description="URL for the production frontend")
    GITHUB_REDIRECT_URI: str = Field(..., description="GitHub OAuth redirect URI")
    
    # Security settings for production
    COOKIE_SECURE: bool = Field(True, description="Cookies require HTTPS")
    COOKIE_SAMESITE: str = Field("lax", description="Cookie same-site policy")
    
    # CORS settings for production
    CORS_ALLOWED_ORIGINS: List[str] = Field(
        ...,
        description="List of origins allowed to access the API"
    )
    
    # Production log settings
    LOG_LEVEL: str = Field("INFO", description="Default log level for production")
    
    # Documentation settings - disable in production
    SHOW_SWAGGER: bool = Field(False, description="API documentation is disabled in production")
    
    # Rate limiting in production
    RATE_LIMIT_ENABLED: bool = Field(True, description="Enable rate limiting")
    RATE_LIMIT_REQUESTS: int = Field(60, description="Maximum requests per time period")
    RATE_LIMIT_PERIOD: int = Field(60, description="Time period in seconds")
    
    # Security headers
    SECURITY_HEADERS: Dict[str, str] = Field(
        {
            "X-Content-Type-Options": "nosniff",
            "X-Frame-Options": "DENY",
            "X-XSS-Protection": "1; mode=block",
            "Strict-Transport-Security": "max-age=31536000; includeSubDomains",
            "Content-Security-Policy": "default-src 'self'; frame-ancestors 'none';",
            "Referrer-Policy": "strict-origin-when-cross-origin",
        },
        description="HTTP security headers for all responses"
    )
    
    # Trusted hosts
    TRUSTED_HOSTS: List[str] = Field(
        ...,
        description="List of hosts allowed to access the API"
    )
    
    # CORS Origins validator to support comma-separated string from env vars
    @field_validator('CORS_ALLOWED_ORIGINS', pre=True)
    def parse_cors_origins(cls, v):
        """Parse CORS origins from string to list if needed."""
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(',')]
        return v
        
    # Trusted hosts validator to support comma-separated string from env vars
    @field_validator('TRUSTED_HOSTS', pre=True)
    def parse_trusted_hosts(cls, v):
        """Parse trusted hosts from string to list if needed."""
        if isinstance(v, str):
            return [host.strip() for host in v.split(',')]
        return v
    
    # Security headers validator to support JSON string from env vars
    @field_validator('SECURITY_HEADERS', pre=True)
    def parse_security_headers(cls, v):
        """Parse security headers from string to dict if needed."""
        if isinstance(v, str):
            import json
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                # Return default if parsing fails
                return cls.__fields__['SECURITY_HEADERS'].default
        return v
    
    # Load environment variables from production file
    class Config:
        env_file = os.path.join(BASE_DIR, ".env.production")
        env_file_encoding = "utf-8"
        case_sensitive = True