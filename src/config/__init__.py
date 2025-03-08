"""
Configuration package for AlgeLab.

This module handles environment-specific settings and provides
a centralized way to access configuration throughout the application.
"""

import os
from functools import lru_cache
from pathlib import Path

from src.config.dev import DevSettings
from src.config.prod import ProdSettings
from src.exceptions import ConfigurationError

# Define base project directory
BASE_DIR = Path(__file__).resolve().parent.parent.parent


@lru_cache()
def get_settings():
    """
    Get settings based on environment.
    
    Uses environment variable 'ENVIRONMENT' to determine which settings to load.
    Defaults to development settings if not specified.
    
    Returns:
        Settings object with the appropriate configuration
    
    Raises:
        ConfigurationError: If required environment variables are missing
    """
    env = os.getenv("ENVIRONMENT", "development").lower()
    
    if env == "production":
        return ProdSettings()
    elif env == "development":
        return DevSettings()
    else:
        raise ConfigurationError(f"Unknown environment: {env}")