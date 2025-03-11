"""
Constants used throughout the AlgeLab application.

This module defines project-wide constants such as paths
and application-specific values.
"""

import os
import pathlib

# Base directory of the project
BASE_DIR = os.path.dirname(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))

# Project paths
LOGS_DIR = os.path.join(BASE_DIR, "logs")
DOCS_DIR = os.path.join(BASE_DIR, "docs")

# API versions
API_V1_STR = "/api"

# JWT related
JWT_TOKEN_COOKIE_NAME = "jwt_token"
JWT_REFRESH_COOKIE_NAME = "refresh_token"

# GitHub auth
GITHUB_API_URL = "https://api.github.com"
GITHUB_AUTH_URL = "https://github.com/login/oauth/authorize"
GITHUB_TOKEN_URL = "https://github.com/login/oauth/access_token"

# Other constants
DEFAULT_PAGE_SIZE = 20
MAX_PAGE_SIZE = 100