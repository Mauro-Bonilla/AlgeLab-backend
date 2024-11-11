# Environment Variables Configuration Guide

This guide explains all necessary environment variables required for development and production environments in the AlgeLab project.

## Table of Contents
- [Getting Started](#getting-started)
- [Environment Files](#environment-files)
- [Required Variables](#required-variables)
- [GitHub SSO Configuration](#github-sso-configuration)
- [Contact Information](#contact-information)

## Getting Started

The project uses two environment files:
- `.env.development` - Development environment configuration
- `.env.production` - Production environment configuration

## Environment Files

### `.env.development`
```env
# Debug Settings
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1

# Database (Default SQLite3, no configuration needed)
# For PostgreSQL, uncomment and configure:
# DB_ENGINE=django.db.backends.postgresql
# DB_NAME=your_dev_db_name
# DB_USER=your_dev_user
# DB_PASSWORD=your_dev_password
# DB_HOST=localhost
# DB_PORT=5432

# Frontend URL
FRONTEND_URL=http://localhost:5173

# Cookie Settings
SESSION_COOKIE_SECURE=False
CSRF_COOKIE_SECURE=False
JWT_COOKIE_SECURE=False
JWT_COOKIE_SAMESITE=Lax

# GitHub OAuth Settings (Required for SSO)
GITHUB_APP_ID=your_github_app_id
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
GITHUB_REDIRECT_URI=http://localhost:8000/api/auth/github/callback
GITHUB_PRIVATE_KEY_PATH=./algelab-sso.2024-10-02.private-key.pem

# CORS and CSRF Settings
CORS_ALLOWED_ORIGINS=http://localhost:5173
CSRF_TRUSTED_ORIGINS=http://localhost:5173

# Swagger Settings
SWAGGER_API_URL=http://localhost:8000
```

### `.env.production`
```env
# Debug Settings
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com

# Database Configuration
DB_ENGINE=django.db.backends.postgresql
DB_NAME=your_prod_db_name
DB_USER=your_prod_user
DB_PASSWORD=your_secure_password
DB_HOST=your.database.host
DB_PORT=5432

# Frontend URL
FRONTEND_URL=https://your-frontend-domain.com

# Cookie Settings
SESSION_COOKIE_SECURE=True
CSRF_COOKIE_SECURE=True
JWT_COOKIE_SECURE=True
JWT_COOKIE_SAMESITE=Lax

# GitHub OAuth Settings
GITHUB_APP_ID=your_github_app_id
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
GITHUB_REDIRECT_URI=https://your-domain.com/api/auth/github/callback
GITHUB_PRIVATE_KEY_PATH=./algelab-sso.2024-10-02.private-key.pem

# CORS and CSRF Settings
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
CSRF_TRUSTED_ORIGINS=https://your-frontend-domain.com

# Swagger Settings
SWAGGER_API_URL=https://your-domain.com
```

## Required Variables

### GitHub SSO Configuration
| Variable | Description | Required |
|----------|-------------|----------|
| `GITHUB_APP_ID` | GitHub App ID | Yes |
| `GITHUB_CLIENT_ID` | OAuth App Client ID | Yes |
| `GITHUB_CLIENT_SECRET` | OAuth App Client Secret | Yes |
| `GITHUB_REDIRECT_URI` | OAuth callback URL | Yes |
| `GITHUB_PRIVATE_KEY_PATH` | Path to GitHub App private key | Yes |

### Security Settings
| Variable | Description | Required |
|----------|-------------|----------|
| `SECRET_KEY` | Django secret key | Yes |
| `DEBUG` | Debug mode flag | Yes |
| `ALLOWED_HOSTS` | Allowed host domains | Yes |

### Database Settings (Production)
| Variable | Description | Required |
|----------|-------------|----------|
| `DB_ENGINE` | Database backend | Yes |
| `DB_NAME` | Database name | Yes |
| `DB_USER` | Database username | Yes |
| `DB_PASSWORD` | Database password | Yes |
| `DB_HOST` | Database host | Yes |
| `DB_PORT` | Database port | Yes |

## GitHub SSO Configuration

### Required Files
The project requires the GitHub App private key file:
```
algelab-sso.2024-10-02.private-key.pem
```

This file should be placed in your project root directory.

### Setting Up GitHub OAuth App

1. Go to GitHub Developer Settings
2. Create a new OAuth App
3. Set Authorization callback URL to:
   - Development: `http://localhost:8000/api/auth/github/callback`
   - Production: `https://your-domain.com/api/auth/github/callback`
4. After creation, you'll get:
   - Client ID
   - Client Secret (generate one if needed)

### Setting Up GitHub App

1. Go to GitHub Developer Settings
2. Create a new GitHub App
3. Generate a private key
4. Save the private key as `algelab-sso.2024-10-02.private-key.pem`
5. Note the App ID

## Contact Information

To obtain the necessary environment variables and GitHub SSO configuration:

### Email Contact
Contact Mauro Bonilla at:
```
mauro.bonillaol@anahuac.mx
```

### Discord Support
Join the Discord server and contact admins at:
```
https://discord.gg/Q8F6xm7U
```

## Security Notes

- Keep all environment variables secret
- Never commit `.env` files or the private key file to version control
- Use strong, unique values for all secrets
- Regularly rotate credentials and secrets
- Follow security best practices for handling sensitive information

## Need Help?

If you need assistance setting up your environment variables or GitHub SSO:

1. First, check if you have all required files and variables
2. Verify your GitHub OAuth and App configurations
3. Contact the team through the provided channels if you need access to official credentials

Remember: Some credentials are restricted and require explicit permission from the project maintainers.