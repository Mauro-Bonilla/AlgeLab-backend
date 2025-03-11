"""
GitHub OAuth integration for user authentication.

This module provides utilities for handling GitHub OAuth authentication
including login flow, callback processing, and user creation.
"""

import logging
from typing import Dict, Any
import requests

from fastapi import HTTPException, status

from src.config import get_settings
from src.config.constants import GITHUB_AUTH_URL, GITHUB_TOKEN_URL, GITHUB_API_URL
from src.schemas.models import GitHubOAuthResponse, GitHubUser
from src.db.client import get_db_client
from src.auth.exceptions import GitHubAuthError

settings = get_settings()
logger = logging.getLogger("algelab.auth.github")
db_client = get_db_client()


def get_github_login_url() -> str:
    """
    Generate GitHub OAuth login URL.
    
    Returns:
        GitHub OAuth authorization URL
    """
    return (
        f"{GITHUB_AUTH_URL}"
        f"?client_id={settings.GITHUB_CLIENT_ID}"
        f"&redirect_uri={settings.GITHUB_REDIRECT_URI}"
        f"&scope=user"
    )


async def get_github_oauth_token(code: str) -> GitHubOAuthResponse:
    """
    Exchange OAuth code for GitHub access token.
    
    Args:
        code: OAuth authorization code from GitHub
        
    Returns:
        GitHubOAuthResponse with access token
        
    Raises:
        GitHubAuthError: If token exchange fails
    """
    try:
        response = requests.post(
            GITHUB_TOKEN_URL,
            data={
                'client_id': settings.GITHUB_CLIENT_ID,
                'client_secret': settings.GITHUB_CLIENT_SECRET,
                'code': code,
                'redirect_uri': settings.GITHUB_REDIRECT_URI,
            },
            headers={'Accept': 'application/json'}
        )
        
        response.raise_for_status()
        response_data = response.json()
        
        # Check for error response
        if "error" in response_data:
            logger.error(f"GitHub OAuth error: {response_data.get('error_description', 'Unknown error')}")
            raise GitHubAuthError(response_data.get("error_description", "Failed to obtain access token"))
        
        # Validate required fields
        if "access_token" not in response_data:
            raise GitHubAuthError("No access token in GitHub response")
        
        return GitHubOAuthResponse(**response_data)
    
    except requests.RequestException as e:
        logger.error(f"GitHub OAuth token request failed: {str(e)}")
        raise GitHubAuthError(f"Failed to obtain GitHub token: {str(e)}")


async def get_github_user(access_token: str) -> GitHubUser:
    """
    Fetch GitHub user information using access token.
    
    Args:
        access_token: GitHub OAuth access token
        
    Returns:
        GitHubUser with user profile information
        
    Raises:
        GitHubAuthError: If user data fetch fails
    """
    try:
        response = requests.get(
            f"{GITHUB_API_URL}/user",
            headers={
                'Authorization': f'token {access_token}',
                'Accept': 'application/json'
            }
        )
        
        response.raise_for_status()
        user_data = response.json()
        
        # Get additional email information if not provided in profile
        if not user_data.get("email"):
            try:
                emails_response = requests.get(
                    f"{GITHUB_API_URL}/user/emails",
                    headers={
                        'Authorization': f'token {access_token}',
                        'Accept': 'application/json'
                    }
                )
                
                if emails_response.status_code == 200:
                    emails = emails_response.json()
                    primary_email = next((email for email in emails if email.get("primary")), None)
                    if primary_email:
                        user_data["email"] = primary_email.get("email")
            except Exception as e:
                logger.warning(f"Failed to fetch GitHub user emails: {str(e)}")
        
        return GitHubUser(**user_data)
    
    except requests.RequestException as e:
        logger.error(f"GitHub user request failed: {str(e)}")
        raise GitHubAuthError(f"Failed to fetch GitHub user: {str(e)}")


async def create_or_get_user_from_github(github_user: GitHubUser) -> Dict[str, Any]:
    """
    Create or update user from GitHub profile information.
    
    Args:
        github_user: GitHub user information
        
    Returns:
        Dict containing user information from database
        
    Raises:
        HTTPException: If user creation/update fails
    """
    try:
        # Check if user exists by GitHub username
        existing_user = db_client.get_user_by_github_username(github_user.login)
        
        # Create user data
        user_data = {
            "github_username": github_user.login,
            "first_name": github_user.name.split()[0] if github_user.name else None,
            "last_name": github_user.name.split(maxsplit=1)[1] if github_user.name and len(github_user.name.split()) > 1 else None,
        }
        
        if existing_user:
            # Update existing user
            user = db_client.create_or_update_user(existing_user["user_id"], user_data)
        else:
            # Create new user ID (using GitHub ID as reference)
            user_id = f"github_{github_user.id}"
            user = db_client.create_or_update_user(user_id, user_data)
        
        return user
    
    except Exception as e:
        logger.error(f"Failed to create or update user from GitHub: {str(e)}")
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail=f"Failed to create or update user: {str(e)}"
        )