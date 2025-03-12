# Environment Variables Configuration Guide

This guide explains all necessary environment variables required for development and production environments in the AlgeLab FastAPI project.

## Table of Contents
- [Getting Started](#getting-started)
- [Environment Files](#environment-files)
- [Required Variables](#required-variables)
- [GitHub SSO Configuration](#github-sso-configuration)
- [Database Configuration](#database-configuration)
- [Contact Information](#contact-information)

## Getting Started

The project uses two environment files:
- `.env.development` - Development environment configuration
- `.env.production` - Production environment configuration

## Environment Files

### `.env.development`
```env
# Project Metadata
PROJECT_NAME="AlgeLab"
PROJECT_DESCRIPTION="An open-source web platform for linear algebra learning"
VERSION="1.0.0"

# Environment and Debugging
ENVIRONMENT="development"
DEBUG=True
SHOW_SWAGGER=True

# Security
SECRET_KEY=your_secret_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1400
RESET_TOKEN_EXPIRE_MINUTES=1400
ALLOWED_HOSTS=localhost,127.0.0.1

# CORS and CSRF
CORS_ALLOWED_ORIGINS=http://localhost:5173,http://localhost:3000
CORS_ALLOW_CREDENTIALS=True
CORS_ALLOW_METHODS=*
CORS_ALLOW_HEADERS=*
CSRF_TRUSTED_ORIGINS=http://localhost:5173

# Cookie Settings
COOKIE_SECURE=False
COOKIE_HTTPONLY=True
COOKIE_SAMESITE=lax
COOKIE_MAX_AGE=3600

# Frontend URL
FRONTEND_URL=http://localhost:5173

# GitHub OAuth Settings
GITHUB_APP_ID=your_github_app_id
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
GITHUB_REDIRECT_URI=http://localhost:8000/api/auth/github/callback
GITHUB_PRIVATE_KEY_PATH=./algelab-sso.2024-10-02.private-key.pem

# Supabase Settings
SUPABASE_URL=your_supabase_url
POSTGRES_URL=your_postgres_url
POSTGRES_PRISMA_URL=your_postgres_prisma_url
NEXT_PUBLIC_SUPABASE_URL=your_public_supabase_url
POSTGRES_URL_NON_POOLING=your_postgres_url_non_pooling
SUPABASE_JWT_SECRET=your_supabase_jwt_secret
POSTGRES_USER=postgres
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DATABASE=postgres
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
POSTGRES_HOST=your_postgres_host

# Logging
LOG_LEVEL=INFO
LOG_FORMAT="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE=logs/app.log

# Rate Limiting
RATE_LIMIT_ENABLED=False
RATE_LIMIT_REQUESTS=100
RATE_LIMIT_PERIOD=60

# Swagger Settings
SWAGGER_API_URL=http://localhost:8000
```

### `.env.production`
```env
# Project Metadata
PROJECT_NAME="AlgeLab"
PROJECT_DESCRIPTION="An open-source web platform for linear algebra learning"
VERSION="1.0.0"

# Environment and Debugging
ENVIRONMENT="production"
DEBUG=False
SHOW_SWAGGER=False

# Security
SECRET_KEY=your_secure_production_key
ALGORITHM=HS256
ACCESS_TOKEN_EXPIRE_MINUTES=1400
RESET_TOKEN_EXPIRE_MINUTES=1400
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
TRUSTED_HOSTS=your-domain.com,www.your-domain.com

# Security Headers
SECURITY_HEADERS={"X-Content-Type-Options":"nosniff","X-Frame-Options":"DENY","X-XSS-Protection":"1; mode=block","Strict-Transport-Security":"max-age=31536000; includeSubDomains","Content-Security-Policy":"default-src 'self'; frame-ancestors 'none';","Referrer-Policy":"strict-origin-when-cross-origin"}

# CORS and CSRF
CORS_ALLOWED_ORIGINS=https://your-frontend-domain.com
CORS_ALLOW_CREDENTIALS=True
CORS_ALLOW_METHODS=*
CORS_ALLOW_HEADERS=*
CSRF_TRUSTED_ORIGINS=https://your-frontend-domain.com

# Cookie Settings
COOKIE_SECURE=True
COOKIE_HTTPONLY=True
COOKIE_SAMESITE=lax
COOKIE_MAX_AGE=3600

# Frontend URL
FRONTEND_URL=https://your-frontend-domain.com

# GitHub OAuth Settings
GITHUB_APP_ID=your_github_app_id
GITHUB_CLIENT_ID=your_github_client_id
GITHUB_CLIENT_SECRET=your_github_client_secret
GITHUB_REDIRECT_URI=https://your-domain.com/api/auth/github/callback
GITHUB_PRIVATE_KEY_PATH=./algelab-sso.2024-10-02.private-key.pem

# Supabase Settings
SUPABASE_URL=your_supabase_url
POSTGRES_URL=your_postgres_url
POSTGRES_PRISMA_URL=your_postgres_prisma_url
NEXT_PUBLIC_SUPABASE_URL=your_public_supabase_url
POSTGRES_URL_NON_POOLING=your_postgres_url_non_pooling
SUPABASE_JWT_SECRET=your_supabase_jwt_secret
POSTGRES_USER=postgres
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_supabase_anon_key
POSTGRES_PASSWORD=your_postgres_password
POSTGRES_DATABASE=postgres
SUPABASE_SERVICE_ROLE_KEY=your_supabase_service_role_key
POSTGRES_HOST=your_postgres_host

# Logging
LOG_LEVEL=INFO
LOG_FORMAT="%(asctime)s - %(name)s - %(levelname)s - %(message)s"
LOG_FILE=logs/app.log

# Rate Limiting
RATE_LIMIT_ENABLED=True
RATE_LIMIT_REQUESTS=60
RATE_LIMIT_PERIOD=60
```

## Required Variables

### Core Application Settings
| Variable | Description | Required |
|----------|-------------|----------|
| `ENVIRONMENT` | Environment mode (`development` or `production`) | Yes |
| `SECRET_KEY` | Secret key for cryptographic operations | Yes |
| `DEBUG` | Enable debug mode | Yes |
| `ALLOWED_HOSTS` | Comma-separated list of allowed host domains | Yes |

### GitHub SSO Configuration
| Variable | Description | Required |
|----------|-------------|----------|
| `GITHUB_APP_ID` | GitHub App ID | Yes |
| `GITHUB_CLIENT_ID` | OAuth App Client ID | Yes |
| `GITHUB_CLIENT_SECRET` | OAuth App Client Secret | Yes |
| `GITHUB_REDIRECT_URI` | OAuth callback URL | Yes |
| `GITHUB_PRIVATE_KEY_PATH` | Path to GitHub App private key | Yes |

### Supabase Settings
| Variable | Description | Required |
|----------|-------------|----------|
| `SUPABASE_URL` | Supabase project URL | Yes |
| `SUPABASE_SERVICE_ROLE_KEY` | Supabase service role key | Yes |
| `NEXT_PUBLIC_SUPABASE_URL` | Public Supabase URL for client-side | Yes |
| `NEXT_PUBLIC_SUPABASE_ANON_KEY` | Anonymous key for Supabase | Yes |

### Frontend Configuration
| Variable | Description | Required |
|----------|-------------|----------|
| `FRONTEND_URL` | URL of the frontend application | Yes |
| `CORS_ALLOWED_ORIGINS` | Comma-separated list of allowed CORS origins | Yes |

### Cookie Settings
| Variable | Description | Required |
|----------|-------------|----------|
| `COOKIE_SECURE` | Set cookies as secure (HTTPS only) | Yes |
| `COOKIE_HTTPONLY` | Set cookies as HTTP only | Yes |
| `COOKIE_SAMESITE` | SameSite cookie policy (Lax, Strict, None) | Yes |
| `COOKIE_MAX_AGE` | Cookie lifetime in seconds | Yes |

## GitHub SSO Configuration

### Required Files
The project requires the GitHub App private key file:
```
algelab-sso.2024-10-02.private-key.pem
```

This file should be placed in your project root directory with appropriate permissions:
```bash
chmod 600 algelab-sso.2024-10-02.private-key.pem
```

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

## Database Configuration

The project uses Supabase as a managed PostgreSQL service. You need to configure:

1. Create a Supabase project
2. Create a `profiles` table with these fields:
   - `user_id` (text, primary key)
   - `github_username` (text)
   - `first_name` (text, nullable)
   - `last_name` (text, nullable)
   - `created_at` (timestamp with timezone, default: now())
   - `updated_at` (timestamp with timezone, nullable)

3. Get your Supabase credentials from the project settings
4. Add these credentials to your environment files

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