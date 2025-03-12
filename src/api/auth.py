"""
Authentication endpoints for the API.

This module contains routes for handling user authentication
including GitHub OAuth flow.
"""

import logging
from typing import Dict, Any
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status, Cookie
from fastapi.responses import RedirectResponse, JSONResponse

from src.auth.jwt import create_access_token, get_current_user, decode_token, get_token_from_request
from src.auth.github import (
    get_github_login_url, get_github_oauth_token, get_github_user,
    create_or_get_user_from_github, GitHubAuthError
)
from src.config import get_settings
from src.config.constants import JWT_TOKEN_COOKIE_NAME
from src.schemas.models import ErrorResponse, TokenResponse

settings = get_settings()
logger = logging.getLogger("algelab.api.auth")

router = APIRouter(
    tags=["authentication"],
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    }
)


@router.get("/github", status_code=200, response_model=Dict[str, str])
async def github_login():
    """
    Get GitHub OAuth login URL.
    
    Returns:
        Dict with login URL for GitHub OAuth
    """
    login_url = get_github_login_url()
    return {"login_url": login_url}


@router.get("/github/callback")
async def github_callback(code: str, request: Request):
    """
    Handle GitHub OAuth callback.
    
    Args:
        code: Authorization code from GitHub
        request: FastAPI request object
        
    Returns:
        Redirect to frontend with JWT token set as cookie
    """
    try:
        # Exchange code for GitHub access token
        github_token = await get_github_oauth_token(code)
        
        # Get GitHub user information
        github_user = await get_github_user(github_token.access_token)
        
        # Create or get user from database
        user = await create_or_get_user_from_github(github_user)
        
        # Create JWT token
        token = create_access_token(
            subject=user["user_id"],
            expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
        )
        
        # Create response with redirect
        response = RedirectResponse(url=f"{settings.FRONTEND_URL}/anh-algelab")
        
        # Set JWT token as cookie
        response.set_cookie(
            key=JWT_TOKEN_COOKIE_NAME,
            value=token,
            max_age=settings.COOKIE_MAX_AGE,
            httponly=settings.COOKIE_HTTPONLY,
            secure=settings.COOKIE_SECURE,
            samesite=settings.COOKIE_SAMESITE,
            path="/",
        )
        
        # Log successful authentication
        logger.info(f"User {user['user_id']} authenticated successfully via GitHub")
        
        return response
        
    except GitHubAuthError as e:
        logger.error(f"GitHub authentication error: {str(e)}")
        return RedirectResponse(
            url=f"{settings.FRONTEND_URL}/auth-error?error={str(e)}",
            status_code=status.HTTP_302_FOUND
        )
    except Exception as e:
        logger.exception(f"Unexpected error in GitHub callback: {str(e)}")
        return RedirectResponse(
            url=f"{settings.FRONTEND_URL}/auth-error?error=Authentication+failed",
            status_code=status.HTTP_302_FOUND
        )


@router.post("/logout", status_code=200)
async def logout(
    response: Response,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Logout user by clearing the JWT token cookie.
    
    Args:
        response: FastAPI response object
        current_user: Current authenticated user
        
    Returns:
        Success message
    """
    logger.info(f"User {current_user['user_id']} logged out")
    
    response.delete_cookie(
        key=JWT_TOKEN_COOKIE_NAME,
        path="/",
        secure=settings.COOKIE_SECURE,
        httponly=settings.COOKIE_HTTPONLY,
        samesite=settings.COOKIE_SAMESITE
    )
    
    return {"message": "Successfully logged out"}


@router.get("/token", response_model=TokenResponse)
async def get_token(request: Request):
    """
    Get current JWT token information.
    
    Args:
        request: FastAPI request object
        
    Returns:
        Token information if valid
    """
    token = get_token_from_request(request)
    
    if not token:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="No authentication token found"
        )
    
    try:
        payload = decode_token(token)
        return TokenResponse(
            user_id=payload["sub"],
            expires_at=payload["exp"]
        )
    except HTTPException as e:
        raise e


@router.post("/validate-token", status_code=200)
async def validate_token(request: Request):
    """
    Validate JWT token from cookie or header.
    
    Args:
        request: FastAPI request object
        
    Returns:
        Validation result
    """
    token = get_token_from_request(request)
    
    if not token:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"valid": False, "error": "No token provided"}
        )
    
    try:
        payload = decode_token(token)
        return {"valid": True, "user_id": payload["sub"]}
    except HTTPException as e:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"valid": False, "error": e.detail}
        )


@router.post("/refresh-token", status_code=200)
async def refresh_token(
    request: Request,
    response: Response,
    current_user: Dict[str, Any] = Depends(get_current_user)
):
    """
    Refresh JWT token.
    
    Args:
        request: FastAPI request object
        response: FastAPI response object
        current_user: Current authenticated user
        
    Returns:
        Success message with new token expiration
    """
    # Create new token
    new_token = create_access_token(
        subject=current_user["user_id"],
        expires_delta=timedelta(minutes=settings.ACCESS_TOKEN_EXPIRE_MINUTES)
    )
    
    # Set new cookie
    response.set_cookie(
        key=JWT_TOKEN_COOKIE_NAME,
        value=new_token,
        max_age=settings.COOKIE_MAX_AGE,
        httponly=settings.COOKIE_HTTPONLY,
        secure=settings.COOKIE_SECURE,
        samesite=settings.COOKIE_SAMESITE,
        path="/",
    )
    
    # Decode token to get expiration
    payload = decode_token(new_token)
    
    return {
        "message": "Token refreshed successfully",
        "expires_at": payload["exp"]
    }