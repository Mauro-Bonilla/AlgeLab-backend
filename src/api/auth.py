"""
Authentication endpoints for the API.

This module contains routes for handling user authentication
including GitHub OAuth flow.
"""

import logging
from typing import Dict, Any
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException, Request, Response, status
from fastapi.responses import RedirectResponse, JSONResponse

from src.auth.jwt import create_access_token, get_current_user, decode_token
from src.auth.github import (
    get_github_login_url, get_github_oauth_token, get_github_user,
    create_or_get_user_from_github, GitHubAuthError
)
from src.config import get_settings
from src.config.constants import JWT_TOKEN_COOKIE_NAME
from src.schemas.models import  ErrorResponse

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
    response.delete_cookie(
        key=JWT_TOKEN_COOKIE_NAME,
        path="/",
        secure=settings.COOKIE_SECURE,
        httponly=settings.COOKIE_HTTPONLY,
        samesite=settings.COOKIE_SAMESITE
    )
    
    return {"message": "Successfully logged out"}


@router.post("/validate-token", status_code=200)
async def validate_token(request: Request):
    """
    Validate JWT token from cookie.
    
    Args:
        request: FastAPI request object
        
    Returns:
        Validation result
    """
    token = request.cookies.get(JWT_TOKEN_COOKIE_NAME)
    
    if not token:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"valid": False, "error": "No token provided"}
        )
    
    try:
        decode_token(token)
        return {"valid": True}
    except HTTPException as e:
        return JSONResponse(
            status_code=status.HTTP_401_UNAUTHORIZED,
            content={"valid": False, "error": e.detail}
        )