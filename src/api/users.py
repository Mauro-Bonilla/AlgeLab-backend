"""
User-related endpoints for the API.

This module contains routes for handling user information
and profile management.
"""

import logging
from typing import Dict, Any

from fastapi import APIRouter, Depends, HTTPException, status

from src.auth.jwt import get_current_user
from src.db.client import get_db_client, SupabaseClientError
from src.schemas.models import UserInfo, ErrorResponse

logger = logging.getLogger("algelab.api.users")
db_client = get_db_client()

router = APIRouter(
    tags=["users"],
    responses={
        401: {"model": ErrorResponse, "description": "Unauthorized"},
        403: {"model": ErrorResponse, "description": "Forbidden"},
        404: {"model": ErrorResponse, "description": "Not Found"},
        500: {"model": ErrorResponse, "description": "Internal Server Error"},
    }
)


@router.get("/", response_model=UserInfo)
async def get_user_info(current_user: Dict[str, Any] = Depends(get_current_user)):
    """
    Get information about the current authenticated user.
    
    Args:
        current_user: Current authenticated user
        
    Returns:
        UserInfo object with user profile information
        
    Raises:
        HTTPException: If user not found or database error
    """
    try:
        user_id = current_user["user_id"]
        user = db_client.get_user(user_id)
        
        if not user:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND,
                detail="User not found"
            )
        
        # Generate avatar URL
        avatar_url = None
        if user.get("github_username"):
            avatar_url = f"https://github.com/{user['github_username']}.png"
        
        # Prepare response
        return UserInfo(
            user_id=user_id,
            username=user.get("github_username", ""),
            first_name=user.get("first_name"),
            last_name=user.get("last_name"),
            avatar_url=avatar_url
        )
        
    except SupabaseClientError as e:
        logger.error(f"Database error when fetching user info: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Database error: {str(e)}"
        )
    except Exception as e:
        logger.exception(f"Unexpected error in get_user_info: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Internal server error: {str(e)}"
        )