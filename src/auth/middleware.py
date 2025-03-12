"""
Authentication middleware for handling JWT token validation.

This middleware extracts JWT tokens from requests and attaches
user information to the request state for easier access.
"""

import logging
from typing import Optional

from fastapi import Request
from starlette.middleware.base import BaseHTTPMiddleware
from starlette.responses import Response

from src.auth.jwt import get_token_from_request, decode_token
from src.config.constants import JWT_TOKEN_COOKIE_NAME

logger = logging.getLogger("algelab.middleware.auth")


class AuthMiddleware(BaseHTTPMiddleware):
    """
    Middleware to process JWT tokens and attach user info to request.
    """
    
    async def dispatch(self, request: Request, call_next) -> Response:
        """
        Process request, extract token, and attach user info.
        
        Args:
            request: The incoming request
            call_next: The next middleware/endpoint handler
            
        Returns:
            The response from downstream handlers
        """
        # Skip auth processing for certain paths
        path = request.url.path
        skip_paths = [
            "/health",
            "/api/auth/github",
            "/api/auth/github/callback",
            "/swagger",
            "/redoc",
            "/docs",
            "/openapi.json",
        ]
        
        if any(path.startswith(skip_path) for skip_path in skip_paths):
            return await call_next(request)
        
        # Extract token
        token = get_token_from_request(request)
        
        # Attach user info to request state if token is valid
        if token:
            try:
                payload = decode_token(token)
                # Set user info in request state for easy access
                request.state.user = {"user_id": payload["sub"]}
                request.state.authenticated = True
                
                # Check if token will expire soon (within 10 minutes)
                import time
                current_time = int(time.time())
                if payload["exp"] - current_time < 600:  # 10 minutes
                    request.state.token_expiring_soon = True
                    logger.debug(f"Token for user {payload['sub']} expiring soon")
                
            except Exception as e:
                # Don't fail the request, just log the issue
                logger.debug(f"Invalid token: {str(e)}")
                request.state.user = None
                request.state.authenticated = False
        else:
            request.state.user = None
            request.state.authenticated = False
        
        # Continue processing the request
        response = await call_next(request)
        
        # Auto-refresh expiring tokens
        if (
            hasattr(request.state, "token_expiring_soon") 
            and request.state.token_expiring_soon 
            and request.state.authenticated
            and response.status_code < 400  # Only refresh on successful responses
        ):
            from src.auth.jwt import create_access_token
            from datetime import timedelta
            from src.config import get_settings
            
            settings = get_settings()
            
            # Create new token
            user_id = request.state.user["user_id"]
            new_token = create_access_token(
                subject=user_id,
                expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
            )
            
            # Set refreshed token in response
            response.set_cookie(
                key=JWT_TOKEN_COOKIE_NAME,
                value=new_token,
                max_age=settings.COOKIE_MAX_AGE,
                httponly=settings.COOKIE_HTTPONLY,
                secure=settings.COOKIE_SECURE,
                samesite=settings.COOKIE_SAMESITE,
                path="/",
            )
            
            logger.debug(f"Auto-refreshed token for user {user_id}")
        
        return response