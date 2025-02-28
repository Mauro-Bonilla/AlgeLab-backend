# Database Configuration Guide

This guide explains how to configure and manage database connections for development and production environments in this Django REST Framework project.

## Table of Contents
- [Environment Setup](#environment-setup)
- [Database Configuration](#database-configuration)
- [VS Code Debugging](#vs-code-debugging)
- [Common Issues](#common-issues)
- [Contributing](#contributing)

## Environment Setup

### Development Environment (Default SQLite3)

By default, the development environment uses SQLite3, which requires no additional configuration. This is automatically configured in `settings.py` when `ENVIRONMENT` is not 'production':

```python
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

If you want to use PostgreSQL or another database in development, create a `.env.development` file in your project root:

```env
# Optional Database Configuration (if not using default SQLite3)
DB_ENGINE=django.db.backends.postgresql
DB_NAME=your_dev_db_name
DB_USER=your_dev_user
DB_PASSWORD=your_dev_password
DB_HOST=localhost
DB_PORT=5432

# Debug Settings
DEBUG=True
ALLOWED_HOSTS=localhost,127.0.0.1
```

### Production Environment

Create a `.env.production` file in your project root:

```env
# Database Configuration
DB_ENGINE=django.db.backends.postgresql
DB_NAME=your_prod_db_name
DB_USER=your_prod_user
DB_PASSWORD=your_secure_password
DB_HOST=your.database.host
DB_PORT=5432

# Security Settings
DEBUG=False
ALLOWED_HOSTS=your-domain.com,www.your-domain.com
```

## Database Configuration

### Supported Database Engines

This project supports multiple database backends:

#### Default Development Database (SQLite3)
No configuration needed! The project automatically uses SQLite3 in development:
```python
# This is already configured in settings.py for development
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}
```

#### PostgreSQL (Recommended for Production)
```env
DB_ENGINE=django.db.backends.postgresql
```

#### MySQL
```env
DB_ENGINE=django.db.backends.mysql
```

### Connection Settings

The project uses different database configurations based on the environment:

- Development: 
  - Defaults to SQLite3 (no configuration needed)
  - Perfect for local development
  - Database file created automatically at `db.sqlite3`
  - No additional software installation required

- Production: 
  - Uses PostgreSQL (recommended) or other configured database
  - Requires proper environment variables in `.env.production`
  - Supports multiple concurrent connections
  - Better performance and scalability

### Database URL Format

For reference, here's the general format of database URLs (when not using SQLite3):
```
postgresql://USER:PASSWORD@HOST:PORT/DATABASE
mysql://USER:PASSWORD@HOST:PORT/DATABASE
```

## VS Code Debugging

### Launch Configuration

The project includes a `launch.json` configuration for VS Code that enables debugging in both development and production environments:

```json
{
    "version": "0.2.0",
    "configurations": [
        {
            "name": "Python: Django Development",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/manage.py",
            "args": [
                "runserver",
                "0.0.0.0:8000"
            ],
            "django": true,
            "autoStartBrowser": false,
            "env": {
                "ENVIRONMENT": "development"
            },
            "console": "integratedTerminal"
        },
        {
            "name": "Python: Django Production",
            "type": "python",
            "request": "launch",
            "program": "${workspaceFolder}/manage.py",
            "args": [
                "runserver",
                "0.0.0.0:8000"
            ],
            "django": true,
            "autoStartBrowser": false,
            "env": {
                "ENVIRONMENT": "production"
            },
            "console": "integratedTerminal"
        }
    ]
}
```

### Using the Debugger

1. Open VS Code Command Palette (Ctrl+Shift+P / Cmd+Shift+P)
2. Select "Debug: Select and Start Debugging" or press F5
3. Choose either "Python: Django Development" or "Python: Django Production"

## Common Issues

### Database Connection Issues

1. **SQLite3 Issues (Development)**
   - Ensure write permissions in project directory
   - Check if `db.sqlite3` file exists and is not corrupted
   - Verify Django can create/access the database file

2. **Production Database Issues**
   - Verify database service is running
   - Check host and port settings
   - Ensure firewall allows connection
   - Verify username and password
   - Check database user permissions

3. **Database Does Not Exist**
   - For SQLite3: Django will create it automatically
   - For PostgreSQL/MySQL:
     ```sql
     CREATE DATABASE your_db_name;
     ```

### Environment Variables

1. **Missing Environment File**
   - Development: Not needed if using default SQLite3
   - Production: Ensure `.env.production` exists
   - Copy from example files if provided

2. **Invalid Settings**
   - Check for typos in variable names
   - Verify values are properly formatted

## Contributing

### Adding Database Support

To add support for a new database:

1. Install required adapter:
   ```bash
   pip install database-adapter-name
   ```

2. Add configuration to `settings.py`:
   ```python
   DATABASES = {
       'new_db': {
           'ENGINE': 'django.db.backends.new_db',
           # ... other settings
       }
   }
   ```

3. Update documentation

### Testing Database Connections

Run the following command to test your database configuration:
```bash
python manage.py check --database default
```

### Migrations

Always run migrations after database changes:
```bash
python manage.py makemigrations
python manage.py migrate
```

## Security Notes

- Never commit `.env` files or `db.sqlite3` to version control
- Use strong, unique passwords for each environment
- Regularly rotate database credentials
- Use SSL/TLS for production database connections
- Restrict database access to necessary IP addresses
- In production, avoid using SQLite3 as it's not suitable for concurrent access