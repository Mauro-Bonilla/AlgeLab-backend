"""
Custom exceptions for algelab.

This module defines custom exceptions for algelab that are used throughout the application.
"""

class AlgelabException(Exception):
    """Base class for all exceptions in algelab."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class ConfigurationError(AlgelabException):
    """Exception raised for configuration errors."""
    def __init__(self, message: str = "Configuration error"):
        super().__init__(message)