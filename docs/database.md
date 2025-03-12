# Database Configuration Guide

This guide explains how to configure and manage database connections for AlgeLab's FastAPI application using Supabase as a PostgreSQL service provider.

## Table of Contents
- [Supabase Setup](#supabase-setup)
- [Environment Configuration](#environment-configuration)
- [Database Schema](#database-schema)
- [Local Development](#local-development)
- [VS Code Debugging](#vs-code-debugging)
- [Common Issues](#common-issues)
- [Contributing](#contributing)

## Supabase Setup

AlgeLab uses [Supabase](https://supabase.io/) as a managed PostgreSQL database service. Here's how to set it up:

### 1. Create a Supabase Project

1. Sign up for an account at [Supabase](https://supabase.io/)
2. Create a new project
3. Note the project URL and API keys

### 2. Obtain Connection Details

From your Supabase project dashboard, collect the following information:

- **Project URL** (`NEXT_PUBLIC_SUPABASE_URL`)
- **Service Role Key** (`SUPABASE_SERVICE_ROLE_KEY`)
- **Anonymous Key** (`NEXT_PUBLIC_SUPABASE_ANON_KEY`)
- **PostgreSQL Connection String** (`POSTGRES_URL`)

### 3. Create Required Tables

Execute the following SQL in the Supabase SQL Editor:

```sql
-- Create profiles table
CREATE TABLE IF NOT EXISTS profiles (
    user_id TEXT PRIMARY KEY,
    github_username TEXT UNIQUE,
    first_name TEXT,
    last_name TEXT,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT NOW(),
    updated_at TIMESTAMP WITH TIME ZONE
);

-- Create an index on github_username for faster lookups
CREATE INDEX IF NOT EXISTS idx_github_username ON profiles(github_username);
```

## Environment Configuration

### Development Environment

Create a `.env.development` file in your project root with your Supabase credentials:

```env
# Supabase Configuration
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

# Debug Settings
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Production Environment

Create a `.env.production` file with secure production credentials:

```env
# Supabase Configuration 
SUPABASE_URL=your_production_supabase_url
POSTGRES_URL=your_production_postgres_url
POSTGRES_PRISMA_URL=your_production_postgres_prisma_url
NEXT_PUBLIC_SUPABASE_URL=your_production_public_supabase_url
POSTGRES_URL_NON_POOLING=your_production_postgres_url_non_pooling
SUPABASE_JWT_SECRET=your_production_supabase_jwt_secret
POSTGRES_USER=postgres
NEXT_PUBLIC_SUPABASE_ANON_KEY=your_production_supabase_anon_key
POSTGRES_PASSWORD=your_production_postgres_password
POSTGRES_DATABASE=postgres
SUPABASE_SERVICE_ROLE_KEY=your_production_supabase_service_role_key
POSTGRES_HOST=your_production_postgres_host

# Security Settings
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```

## Database Schema

### Core Tables

#### Profiles Table

Stores user profile information linked to GitHub accounts:

| Column | Type | Description |
|--------|------|-------------|
| `user_id` | TEXT | Primary key (format: `github_{github_id}`) |
| `github_username` | TEXT | GitHub username (unique) |
| `first_name` | TEXT | User's first name (optional) |
| `last_name` | TEXT | User's last name (optional) |
| `created_at` | TIMESTAMP WITH TIME ZONE | Account creation timestamp |
| `updated_at` | TIMESTAMP WITH TIME ZONE | Last update timestamp |

## Local Development

For local development, you have two options:

### Option 1: Use Supabase Cloud (Recommended)

- Create a development project in Supabase
- Configure your `.env.development` with the cloud project credentials
- This ensures consistency with production environment

### Option 2: Run Supabase Locally

1. Install [Docker](https://docs.docker.com/get-docker/)
2. Install [Supabase CLI](https://supabase.com/docs/guides/cli/getting-started)
3. Initialize Supabase project:
   ```bash
   supabase init
   ```
4. Start local Supabase instance:
   ```bash
   supabase start
   ```
5. Update your `.env.development` with local credentials
6. Create required tables using provided SQL scripts

## VS Code Debugging

### Launch Configuration

The project includes a `launch.json` configuration for VS Code that enables debugging:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python Debugger: FastAPI",
            "type": "debugpy",
            "request": "launch",
            "program": "${workspaceFolder}/src/main.py",
            "console": "integratedTerminal",
            "justMyCode": false,
            "env": {
                "PYTHONPATH": "${workspaceFolder}"
            }
        }
    ]
}
```

### Using the Debugger

1. Open VS Code Command Palette (Ctrl+Shift+P / Cmd+Shift+P)
2. Select "Debug: Start Debugging" or press F5
3. Set breakpoints in your code as needed

## Common Issues

### Database Connection Issues

1. **Supabase Authentication**
   - Verify service role key is correct
   - Check if the project URL is correct
   - Ensure IP address is allowed in Supabase