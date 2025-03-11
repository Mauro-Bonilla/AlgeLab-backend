"""
Custom exceptions for the AlgeLab application.

This module defines custom exceptions used throughout the application
for handling specific error conditions and provides exception handlers
for FastAPI integration.
"""

import logging
from typing import Dict, Any, Optional, Union, List

from fastapi import HTTPException, status, Request
from fastapi.responses import JSONResponse
from fastapi.exceptions import RequestValidationError
from pydantic import ValidationError as PydanticValidationError

logger = logging.getLogger("algelab.exceptions")


class AlgelabException(Exception):
    """Base exception class for all AlgeLab specific exceptions."""
    status_code: int = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_code: str = "internal_error"
    
    def __init__(
        self, 
        detail: str = None, 
        status_code: Optional[int] = None, 
        error_code: Optional[str] = None,
        headers: Optional[Dict[str, Any]] = None
    ):
        self.detail = detail or self.__class__.__doc__ or "An error occurred"
        self.status_code = status_code or self.status_code
        self.error_code = error_code or self.error_code
        self.headers = headers


class ConfigurationError(AlgelabException):
    """Application configuration error."""
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_code = "configuration_error"


class DatabaseError(AlgelabException):
    """Database operation error."""
    status_code = status.HTTP_500_INTERNAL_SERVER_ERROR
    error_code = "database_error"


class AuthenticationError(AlgelabException):
    """Authentication failed."""
    status_code = status.HTTP_401_UNAUTHORIZED
    error_code = "authentication_error"


class NotFoundError(AlgelabException):
    """Requested resource not found."""
    status_code = status.HTTP_404_NOT_FOUND
    error_code = "not_found"


class ValidationError(AlgelabException):
    """Input validation error."""
    status_code = status.HTTP_422_UNPROCESSABLE_ENTITY
    error_code = "validation_error"


class PermissionDeniedError(AlgelabException):
    """Permission denied to access resource."""
    status_code = status.HTTP_403_FORBIDDEN
    error_code = "permission_denied"


class RateLimitError(AlgelabException):
    """Rate limit exceeded."""
    status_code = status.HTTP_429_TOO_MANY_REQUESTS
    error_code = "rate_limit_exceeded"


class ExternalServiceError(AlgelabException):
    """External service (GitHub, etc.) error."""
    status_code = status.HTTP_502_BAD_GATEWAY
    error_code = "external_service_error"


class ConflictError(AlgelabException):
    """Resource conflict (e.g., duplicate entry)."""
    status_code = status.HTTP_409_CONFLICT
    error_code = "conflict"


# Exception Handlers for FastAPI

async def algelab_exception_handler(request: Request, exc: AlgelabException) -> JSONResponse:
    """
    Handle AlgeLab exceptions and convert to standardized JSON response.
    
    Args:
        request: FastAPI request
        exc: AlgeLab exception instance
        
    Returns:
        JSONResponse with error details
    """
    # Log exception based on severity
    if exc.status_code >= 500:
        logger.error(
            f"Internal error: {exc.detail}",
            extra={"path": request.url.path, "error_code": exc.error_code}
        )
    elif exc.status_code >= 400:
        logger.warning(
            f"Client error: {exc.detail}",
            extra={"path": request.url.path, "error_code": exc.error_code}
        )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": exc.error_code,
            "detail": exc.detail,
            "status_code": exc.status_code
        },
        headers=exc.headers
    )


async def http_exception_handler(request: Request, exc: HTTPException) -> JSONResponse:
    """
    Handle FastAPI HTTPExceptions.
    
    Args:
        request: FastAPI request
        exc: HTTPException instance
        
    Returns:
        JSONResponse with error details
    """
    # Map standard HTTP errors to error codes
    error_code_map = {
        status.HTTP_401_UNAUTHORIZED: "unauthorized",
        status.HTTP_403_FORBIDDEN: "forbidden",
        status.HTTP_404_NOT_FOUND: "not_found",
        status.HTTP_405_METHOD_NOT_ALLOWED: "method_not_allowed",
        status.HTTP_422_UNPROCESSABLE_ENTITY: "validation_error",
        status.HTTP_429_TOO_MANY_REQUESTS: "rate_limit_exceeded",
    }
    
    error_code = error_code_map.get(exc.status_code, f"http_{exc.status_code}")
    
    if exc.status_code >= 500:
        logger.error(
            f"HTTP error {exc.status_code}: {exc.detail}",
            extra={"path": request.url.path}
        )
    else:
        logger.warning(
            f"HTTP error {exc.status_code}: {exc.detail}",
            extra={"path": request.url.path}
        )
    
    return JSONResponse(
        status_code=exc.status_code,
        content={
            "error": error_code,
            "detail": exc.detail,
            "status_code": exc.status_code
        },
        headers=exc.headers
    )


async def validation_exception_handler(request: Request, exc: Union[RequestValidationError, PydanticValidationError]) -> JSONResponse:
    """
    Handle Pydantic and FastAPI validation errors.
    
    Args:
        request: FastAPI request
        exc: ValidationError instance
        
    Returns:
        JSONResponse with validation error details
    """
    errors: List[Dict[str, Any]] = []
    
    if isinstance(exc, RequestValidationError):
        validation_errors = exc.errors()
    else:  # PydanticValidationError
        validation_errors = exc.errors()
    
    for error in validation_errors:
        # Format error location (field path)
        loc = error.get('loc', [])
        if isinstance(loc, tuple):
            loc = list(loc)
        
        field_path = " → ".join(str(item) for item in loc)
        
        # Add formatted error
        errors.append({
            "field": field_path,
            "type": error.get('type', 'unknown'),
            "message": error.get('msg', 'Invalid value')
        })
    
    logger.warning(
        f"Validation error: {len(errors)} validation issues",
        extra={"path": request.url.path, "validation_errors": errors}
    )
    
    return JSONResponse(
        status_code=status.HTTP_422_UNPROCESSABLE_ENTITY,
        content={
            "error": "validation_error",
            "detail": "Input validation error",
            "errors": errors,
            "status_code": status.HTTP_422_UNPROCESSABLE_ENTITY
        }
    )


def add_exception_handlers(app):
    """
    Register all exception handlers with the FastAPI application.
    
    Args:
        app: FastAPI application instance
    """
    app.add_exception_handler(AlgelabException, algelab_exception_handler)
    app.add_exception_handler(HTTPException, http_exception_handler)
    app.add_exception_handler(RequestValidationError, validation_exception_handler)
    app.add_exception_handler(PydanticValidationError, validation_exception_handler)
    
    # Register specific exception classes
    exception_classes = [
        ConfigurationError,
        DatabaseError,
        AuthenticationError,
        NotFoundError,
        ValidationError,
        PermissionDeniedError,
        RateLimitError,
        ExternalServiceError,
        ConflictError
    ]
    
    for exc_class in exception_classes:
        app.add_exception_handler(exc_class, algelab_exception_handler)