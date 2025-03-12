"""
Supabase client for database operations.

This module provides a singleton Supabase client for database operations
and utility functions for database interactions.
"""

import os
from typing import Optional, Dict, Any
import logging
from supabase import create_client, Client
from functools import lru_cache

from src.config import get_settings

logger = logging.getLogger("algelab.db")
settings = get_settings()


class SupabaseClientError(Exception):
    """Exception raised for Supabase client errors."""
    pass


class SupabaseClient:
    """Singleton Supabase client for database operations."""
    
    _instance: Optional['SupabaseClient'] = None
    _client: Optional[Client] = None
    
    def __new__(cls):
        if cls._instance is None:
            cls._instance = super(SupabaseClient, cls).__new__(cls)
            cls._instance._initialize_client()
        return cls._instance
    
    def _initialize_client(self) -> None:
        """Initialize the Supabase client with settings."""
        try:
            self._client = create_client(
                settings.NEXT_PUBLIC_SUPABASE_URL,
                settings.SUPABASE_SERVICE_ROLE_KEY
            )
            logger.info(f"Initialized Supabase client with URL: {settings.NEXT_PUBLIC_SUPABASE_URL}")
        except Exception as e:
            logger.error(f"Failed to initialize Supabase client: {str(e)}")
            raise SupabaseClientError(f"Failed to initialize Supabase client: {str(e)}")
    
    @property
    def client(self) -> Client:
        """Get the Supabase client instance."""
        if self._client is None:
            self._initialize_client()
        return self._client
    
    def get_user(self, user_id: str) -> Dict[str, Any]:
        """
        Get user by ID from the profiles table.
        
        Args:
            user_id: The user ID to look up
            
        Returns:
            Dict containing user profile information
            
        Raises:
            SupabaseClientError: If the operation fails
        """
        try:
            response = self.client.table('profiles').select('*').eq('user_id', user_id).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error fetching user {user_id}: {str(e)}")
            raise SupabaseClientError(f"Error fetching user: {str(e)}")
    
    def create_or_update_user(self, user_id: str, user_data: Dict[str, Any]) -> Dict[str, Any]:
        """
        Create or update user in the profiles table.
        
        Args:
            user_id: The user ID
            user_data: User data to insert/update
            
        Returns:
            Dict containing the created/updated user
            
        Raises:
            SupabaseClientError: If the operation fails
        """
        try:
            # Check if user exists
            existing_user = self.get_user(user_id)
            
            if existing_user:
                # Update user
                response = self.client.table('profiles').update(user_data).eq('user_id', user_id).execute()
            else:
                # Create user
                user_data['user_id'] = user_id
                response = self.client.table('profiles').insert(user_data).execute()
            
            if response.data:
                return response.data[0]
            raise SupabaseClientError("Failed to create or update user")
        except Exception as e:
            logger.error(f"Error creating/updating user {user_id}: {str(e)}")
            raise SupabaseClientError(f"Error creating/updating user: {str(e)}")
    
    def get_user_by_github_username(self, github_username: str) -> Dict[str, Any]:
        """
        Get user by GitHub username.
        
        Args:
            github_username: The GitHub username to look up
            
        Returns:
            Dict containing user profile information or None if not found
            
        Raises:
            SupabaseClientError: If the operation fails
        """
        try:
            response = self.client.table('profiles').select('*').eq('github_username', github_username).execute()
            if response.data:
                return response.data[0]
            return None
        except Exception as e:
            logger.error(f"Error fetching user by GitHub username {github_username}: {str(e)}")
            raise SupabaseClientError(f"Error fetching user by GitHub username: {str(e)}")


@lru_cache()
def get_db_client() -> SupabaseClient:
    """
    Get or create Supabase client instance.
    
    Returns:
        Singleton SupabaseClient instance
    """
    return SupabaseClient()