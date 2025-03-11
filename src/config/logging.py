"""
Logging configuration for the AlgeLab application.

This module sets up logging for the application based on
environment-specific settings.
"""

import os
import logging
import logging.handlers
from pathlib import Path

from src.config import get_settings
from src.config.constants import BASE_DIR

settings = get_settings()


def configure_logging():
    """
    Configure logging settings for the application.
    
    - Creates log directory if it doesn't exist
    - Sets up file and console handlers
    - Configures log levels based on settings
    - Sets up format and handlers for different loggers
    """
    # Create logs directory if it doesn't exist
    log_dir = os.path.join(BASE_DIR, "logs")
    Path(log_dir).mkdir(parents=True, exist_ok=True)
    
    # Get log level from settings
    log_level = getattr(logging, settings.LOG_LEVEL.upper(), logging.INFO)
    
    # Configure root logger
    logging.getLogger("watchfiles").setLevel(logging.WARNING)
    root_logger = logging.getLogger()
    root_logger.setLevel(log_level)
    
    # Clear existing handlers
    for handler in root_logger.handlers:
        root_logger.removeHandler(handler)
    
    # Create formatters
    standard_formatter = logging.Formatter(
        settings.LOG_FORMAT
    )
    
    # Create file handler
    file_handler = logging.handlers.RotatingFileHandler(
        settings.LOG_FILE,
        maxBytes=10485760,  # 10MB
        backupCount=5,
        encoding="utf-8",
    )
    file_handler.setLevel(log_level)
    file_handler.setFormatter(standard_formatter)
    
    # Create console handler
    console_handler = logging.StreamHandler()
    console_handler.setLevel(log_level)
    console_handler.setFormatter(standard_formatter)
    
    # Add handlers to root logger
    root_logger.addHandler(file_handler)
    root_logger.addHandler(console_handler)
    
    # Set log levels for third-party libraries
    logging.getLogger("uvicorn").setLevel(logging.INFO)
    logging.getLogger("fastapi").setLevel(logging.INFO)
    
    # Security logger (for auth and security events)
    security_logger = logging.getLogger("algelab.security")
    security_log_file = os.path.join(log_dir, "security.log")
    
    security_handler = logging.handlers.RotatingFileHandler(
        security_log_file,
        maxBytes=10485760,  # 10MB
        backupCount=10,
        encoding="utf-8",
    )
    security_handler.setFormatter(standard_formatter)
    security_logger.addHandler(security_handler)
    security_logger.setLevel(logging.INFO)
    
    return {
        "root": root_logger,
        "security": security_logger,
    }