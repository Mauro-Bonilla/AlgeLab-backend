"""
Pydantic models for data validation and serialization.

This module defines the data models used throughout the application
for request/response validation and database interactions.
"""

from datetime import datetime
from typing import Optional, List
from pydantic import BaseModel, Field, EmailStr, HttpUrl


class TokenPayload(BaseModel):
    """Payload data stored in JWT token."""
    sub: str = Field(..., description="Subject (user ID)")
    exp: int = Field(..., description="Expiration timestamp")
    
class TokenResponse(BaseModel):
    """Token information response."""
    user_id: str
    expires_at: int
    
class Token(BaseModel):
    """Token response model."""
    access_token: str
    token_type: str = "bearer"


class UserBase(BaseModel):
    """Base user information shared across requests."""
    username: str
    email: Optional[EmailStr] = None
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class UserCreate(UserBase):
    """User information required for creation."""
    pass


class ProfileBase(BaseModel):
    """Base profile information shared across requests."""
    github_username: Optional[str] = None


class ProfileCreate(ProfileBase):
    """Profile information required for creation."""
    user_id: str


class ProfileUpdate(ProfileBase):
    """Profile information that can be updated."""
    first_name: Optional[str] = None
    last_name: Optional[str] = None


class Profile(ProfileBase):
    """Complete profile information returned to clients."""
    user_id: str
    created_at: datetime
    updated_at: Optional[datetime] = None
    
    @property
    def avatar_url(self) -> Optional[str]:
        """Generate GitHub avatar URL from username."""
        if self.github_username:
            return f"https://github.com/{self.github_username}.png"
        return None
    
    class Config:
        """Pydantic model configuration."""
        orm_mode = True


class User(UserBase):
    """Complete user information returned to clients."""
    id: str
    is_active: bool = True
    profile: Optional[Profile] = None
    
    class Config:
        """Pydantic model configuration."""
        orm_mode = True


class UserInfo(BaseModel):
    """User information returned to the client."""
    user_id: str
    username: str
    first_name: Optional[str] = None
    last_name: Optional[str] = None
    avatar_url: Optional[HttpUrl] = None


class GitHubUser(BaseModel):
    """GitHub user information from the GitHub API."""
    login: str
    id: int
    avatar_url: Optional[HttpUrl] = None
    name: Optional[str] = None
    email: Optional[EmailStr] = None


class GitHubOAuthResponse(BaseModel):
    """GitHub OAuth token response."""
    access_token: str
    token_type: str
    scope: Optional[str] = None


class ErrorResponse(BaseModel):
    """Standard error response model."""
    error: str
    detail: Optional[str] = None
    status_code: int = 400