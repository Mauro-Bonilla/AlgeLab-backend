"""
Custom exceptions for the AlgeLab application.

This module defines application-specific exceptions that can be
raised and handled throughout the codebase.
"""

class AlgeLabError(Exception):
    """Base class for all exceptions in algelab."""
    def __init__(self, message: str):
        self.message = message
        super().__init__(self.message)

class ConfigurationError(AlgeLabError):
    """Exception raised for configuration errors."""
    def __init__(self, message: str = "Configuration error"):
        super().__init__(f"Configuration error: {message}")


class DatabaseError(AlgeLabError):
    """Raised when there is an error with database operations."""
    
    def __init__(self, message: str = "Database error"):
        super().__init__(f"Database error: {message}")


class AuthenticationError(AlgeLabError):
    """Raised when there is an error with authentication."""
    
    def __init__(self, message: str = "Authentication error"):
        super().__init__(f"Authentication error: {message}")


class PermissionError(AlgeLabError):
    """Raised when a user attempts an action they don't have permission for."""
    
    def __init__(self, message: str = "Permission denied"):
        super().__init__(f"Permission denied: {message}")


class ResourceNotFoundError(AlgeLabError):
    """Raised when a requested resource is not found."""
    
    def __init__(self, resource_type: str = "resource", resource_id: str = None):
        message = f"{resource_type.capitalize()} not found"
        if resource_id:
            message += f": {resource_id}"
        super().__init__(message)


class ValidationError(AlgeLabError):
    """Raised when input data fails validation."""
    
    def __init__(self, message: str = "Validation error", field: str = None):
        error_msg = f"Validation error"
        if field:
            error_msg += f" in field '{field}'"
        if message:
            error_msg += f": {message}"
        super().__init__(error_msg)


class ExternalServiceError(AlgeLabError):
    """Raised when there is an error with an external service."""
    
    def __init__(self, service: str = "external service", message: str = "Service error"):
        super().__init__(f"Error from {service}: {message}")


class RateLimitError(AlgeLabError):
    """Raised when a user exceeds rate limits."""
    
    def __init__(self, limit: int = None, reset_time: int = None):
        message = "Rate limit exceeded"
        if limit:
            message += f", limit: {limit}"
        if reset_time:
            message += f", try again after {reset_time} seconds"
        super().__init__(message)