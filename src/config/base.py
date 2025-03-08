import os
from typing import List, Optional, Union
from pydantic import BaseSettings, field_validator, EmailStr, Field

from src.config import BASE_DIR


class Settings(BaseSettings):
    """
    Base settings for the application

    This settings are used to configure all the aplication.
    Enviroment specific settings will override this settings.
    """
    # Project metadata
    PROJECT_NAME: str = "AlgeLab"
    PROJECT_DESCRIPTION: str = "An open-source web platform for linear algebra learning"
    VERSION: str = "1.0.0"
    
    # Debugging
    DEBUG: bool = False
    
    # API prefix
    API_PREFIX: str = "/api"
    
    # Security
    SECRET_KEY: str = Field(..., description="Used for JWT token signing and other security features")
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60
    RESET_TOKEN_EXPIRE_MINUTES: int = 30
    
    # CORS settings
    CORS_ALLOWED_ORIGINS: List[str] = ["http://localhost:5173"]
    CORS_ALLOW_CREDENTIALS: bool = True
    CORS_ALLOW_METHODS: List[str] = ["*"]
    CORS_ALLOW_HEADERS: List[str] = ["*"]
    
    # Supabase settings
    SUPABASE_URL: str = Field(..., description="Supabase project URL")
    SUPABASE_KEY: str = Field(..., description="Supabase anon/public key")
    SUPABASE_SERVICE_KEY: Optional[str] = Field(None, description="Supabase service role key")
    
    # GitHub OAuth
    GITHUB_APP_ID: Optional[str] = None
    GITHUB_CLIENT_ID: str = Field(..., description="GitHub OAuth App client ID")
    GITHUB_CLIENT_SECRET: str = Field(..., description="GitHub OAuth App client secret")
    GITHUB_REDIRECT_URI: str = "http://localhost:8000/api/auth/github/callback"
    GITHUB_PRIVATE_KEY_PATH: str = "./algelab-sso.2024-10-02.private-key.pem"
    
    # Frontend URL
    FRONTEND_URL: str = "http://localhost:5173"
    
    # Cookie settings
    COOKIE_SECURE: bool = False
    COOKIE_HTTPONLY: bool = True
    COOKIE_SAMESITE: str = "lax"
    COOKIE_MAX_AGE: int = 3600  # 1 hour
    
    # Logging
    LOG_LEVEL: str = "INFO"
    LOG_FORMAT: str = "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
    LOG_FILE: str = os.path.join(BASE_DIR, "logs", "app.log")
    
    # Rate limiting
    RATE_LIMIT_ENABLED: bool = True
    RATE_LIMIT_REQUESTS: int = 100
    RATE_LIMIT_PERIOD: int = 60  # 1 minute
    
    # Email notifications (optional for later use)
    EMAIL_ENABLED: bool = False
    EMAIL_SENDER: Optional[EmailStr] = None
    EMAIL_SENDER_NAME: Optional[str] = None
    
    # Custom validators
    @field_validator("CORS_ALLOWED_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> List[str]:
        """Parse CORS_ALLOWED_ORIGINS from string to list."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)
    
    @field_validator("GITHUB_PRIVATE_KEY_PATH")
    def validate_private_key_path(cls, v: str) -> str:
        """Validate that the GitHub private key file exists."""
        path = os.path.join(BASE_DIR, v) if not v.startswith("/") else v
        if not os.path.isfile(path):
            raise ValueError(f"GitHub private key not found at {path}")
        return v
    
    # Priority order for settings: env vars > env file > defaults
    class Config:
        env_file = os.path.join(BASE_DIR, ".env.development")
        env_file_encoding = "utf-8"
        case_sensitive = True
        
