"""
JWT token handling for user authentication.

This module provides functions for creating, validating, and handling
JWT tokens for user authentication.
"""

import logging
from datetime import datetime, timedelta
from typing import Any, Dict, Optional

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer
from jwt.exceptions import InvalidTokenError, ExpiredSignatureError

from src.config import get_settings
from src.config.constants import JWT_TOKEN_COOKIE_NAME
from src.schemas.models import TokenPayload

settings = get_settings()
logger = logging.getLogger("algelab.security")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="api/auth/token", auto_error=False)


def create_access_token(subject: str, expires_delta: Optional[timedelta] = None) -> str:
    """
    Create a new JWT access token.
    
    Args:
        subject: Token subject (typically user ID)
        expires_delta: Optional custom expiration time
        
    Returns:
        JWT token string
    """
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    
    to_encode = {"sub": subject, "exp": expire, "iat": datetime.utcnow()}
    
    try:
        encoded_jwt = jwt.encode(to_encode, settings.SECRET_KEY, algorithm=settings.ALGORITHM)
        logger.debug(f"Created JWT token for user {subject}")
        return encoded_jwt
    except Exception as e:
        logger.error(f"Error creating JWT token: {str(e)}")
        raise


def decode_token(token: str) -> Dict[str, Any]:
    """
    Decode and validate a JWT token.
    
    Args:
        token: JWT token to decode
        
    Returns:
        Dict containing decoded token payload
        
    Raises:
        HTTPException: If token is invalid or expired
    """
    try:
        # Decode the JWT token
        payload = jwt.decode(
            token,
            settings.SECRET_KEY,
            algorithms=[settings.ALGORITHM]
        )
        
        # Parse token data
        token_data = TokenPayload(**payload)
        
        # Check if token has expired
        if datetime.fromtimestamp(token_data.exp) < datetime.utcnow():
            logger.warning(f"Expired token attempt for user {token_data.sub}")
            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Token expired",
                headers={"WWW-Authenticate": "Bearer"},
            )
        
        return payload
    
    except ExpiredSignatureError:
        logger.warning("Token has expired")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Token expired",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except InvalidTokenError as e:
        logger.warning(f"Invalid token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate credentials",
            headers={"WWW-Authenticate": "Bearer"},
        )
    except Exception as e:
        logger.error(f"Error decoding token: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication error",
            headers={"WWW-Authenticate": "Bearer"},
        )


def get_token_from_request(request: Request) -> Optional[str]:
    """
    Extract JWT token from request (either from cookie or Authorization header).
    
    Args:
        request: FastAPI request object
        
    Returns:
        JWT token or None if not found
    """
    # Try to get token from cookie first
    token = request.cookies.get(JWT_TOKEN_COOKIE_NAME)
    
    # If not in cookie, try Authorization header
    if not token and 'Authorization' in request.headers:
        auth_header = request.headers.get('Authorization')
        if auth_header and auth_header.startswith('Bearer '):
            token = auth_header.replace('Bearer ', '')
    
    return token


async def get_current_user_optional(request: Request = None, token: str = Depends(oauth2_scheme)) -> Optional[Dict[str, Any]]:
    """
    Get current user from token (if provided).
    
    Args:
        request: FastAPI request
        token: JWT token from Authorization header (via Depends)
        
    Returns:
        Dict containing user information or None if no token
    """
    # Try to get token from request if not provided via Depends
    if not token and request:
        token = get_token_from_request(request)
    
    if not token:
        return None
    
    try:
        payload = decode_token(token)
        return {"user_id": payload["sub"]}
    except HTTPException:
        return None


async def get_current_user(request: Request = None, token: str = Depends(oauth2_scheme)) -> Dict[str, Any]:
    """
    Get current user from token (required).
    
    Args:
        request: FastAPI request
        token: JWT token from Authorization header (via Depends)
        
    Returns:
        Dict containing user information
        
    Raises:
        HTTPException: If no token or token is invalid
    """
    # Try to get token from request if not provided via Depends
    if not token and request:
        token = get_token_from_request(request)
    
    if not token:
        logger.warning("Authentication attempt without token")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Not authenticated",
            headers={"WWW-Authenticate": "Bearer"},
        )
    
    try:
        payload = decode_token(token)
        logger.debug(f"Successfully authenticated user {payload['sub']}")
        return {"user_id": payload["sub"]}
    except HTTPException as e:
        # Re-raise the exception from decode_token
        raise e
    except Exception as e:
        logger.error(f"Unexpected error in authentication: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Authentication error",
            headers={"WWW-Authenticate": "Bearer"},
        )