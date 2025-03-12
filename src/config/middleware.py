"""
Middleware configuration for the AlgeLab application.

This module defines middleware functions for security, logging,
and other application-wide concerns.
"""

import time
import logging
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.requests import Request
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.middleware.trustedhost import TrustedHostMiddleware
from fastapi.middleware.gzip import GZipMiddleware

from src.config import get_settings
from src.config.logging import configure_logging
from src.auth.middleware import AuthMiddleware

settings = get_settings()

loggers = configure_logging()
logger = logging.getLogger("algelab.middleware")


def setup_middleware(app: FastAPI):
    """
    Configure middleware for the FastAPI application.
    
    Args:
        app: FastAPI application instance
    """
    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ALLOWED_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )
    
    # Add authentication middleware
    app.add_middleware(AuthMiddleware)
    # Add request logging middleware
    app.add_middleware(RequestLoggingMiddleware)
    
    # Add security headers middleware in production
    if not settings.DEBUG:
        app.add_middleware(SecurityHeadersMiddleware)
        
        # Add trusted host middleware in production
        if hasattr(settings, 'TRUSTED_HOSTS'):
            app.add_middleware(
                TrustedHostMiddleware, 
                allowed_hosts=settings.TRUSTED_HOSTS
            )
    
    # Add gzip compression
    app.add_middleware(GZipMiddleware, minimum_size=1000)



class RequestLoggingMiddleware(BaseHTTPMiddleware):
    """Middleware for logging request information and timing."""
    
    async def dispatch(self, request: Request, call_next):
        start_time = time.time()
        path = request.url.path
        
        # Skip logging for health check endpoints
        if path == "/health" or path == "/api/health":
            return await call_next(request)
        
        # Process the request
        try:
            response = await call_next(request)
            process_time = time.time() - start_time
            status_code = response.status_code
            
            # Log request details
            logger.info(
                f"{request.method} {path} {status_code} {process_time:.4f}s"
            )
            
            # Add timing header to response
            response.headers["X-Process-Time"] = str(process_time)
            return response
        except Exception as e:
            process_time = time.time() - start_time
            logger.exception(
                f"Error during {request.method} {path}: {str(e)} {process_time:.4f}s"
            )
            raise


class SecurityHeadersMiddleware(BaseHTTPMiddleware):
    """Middleware for adding security headers to responses."""
    
    async def dispatch(self, request: Request, call_next):
        response = await call_next(request)
        
        # Add security headers from settings
        if hasattr(settings, 'SECURITY_HEADERS'):
            for header_name, header_value in settings.SECURITY_HEADERS.items():
                response.headers[header_name] = header_value
        
        return response