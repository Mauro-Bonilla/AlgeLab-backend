# Deployment Guide

This guide explains how to deploy the AlgeLab FastAPI application using Docker, with specific instructions for Azure deployment and general guidance for other platforms.

## Table of Contents
- [Prerequisites](#prerequisites)
- [Docker Configuration](#docker-configuration)
- [Azure Deployment](#azure-deployment)
- [Alternative Deployment Options](#alternative-deployment-options)
- [Environment Configuration](#environment-configuration)
- [Monitoring and Maintenance](#monitoring-and-maintenance)

## Prerequisites

Before deploying, ensure you have:

- Docker installed locally
- Azure CLI (for Azure deployment)
- Required environment variables (see `env_vars.md`)
- GitHub SSO private key file
- Access to a container registry

## Docker Configuration

### Dockerfile Overview

```dockerfile
# Use Python 3.11 slim image as base
FROM python:3.11-slim

# Set environment variables for production
ENV PYTHONDONTWRITEBYTECODE=1 \
    PYTHONUNBUFFERED=1 \
    DEBIAN_FRONTEND=noninteractive

# Set work directory
WORKDIR /app

# Install system dependencies
RUN apt-get update \
    && apt-get install -y --no-install-recommends \
        gcc \
        python3-dev \
        libpq-dev \
        unixodbc-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements first to leverage Docker cache
COPY requirements.txt ./
RUN pip install --no-cache-dir -r requirements.txt

# Copy project files and set permissions for the private key
COPY . ./
COPY algelab-sso.2024-10-02.private-key.pem /app/algelab-sso.2024-10-02.private-key.pem
RUN chmod 600 /app/algelab-sso.2024-10-02.private-key.pem

# Create directories for logs and set permissions
RUN mkdir -p /app/logs \
    && touch /app/logs/app.log \
    && touch /app/logs/security.log \
    && chmod -R 755 /app/logs

# Create a non-root user and adjust permissions for all files
RUN useradd -m appuser && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Run the application using Uvicorn
CMD ["uvicorn", "src.main:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Building the Docker Image Locally

```bash
# Build the image
docker build -t algelab-api .

# Test locally
docker run -p 8000:8000 --env-file .env.production algelab-api
```

## Azure Deployment

### 1. Azure Container Registry (ACR) Setup

```bash
# Login to Azure
az login

# Create a resource group
az group create --name algelab-rg --location eastus

# Create container registry
az acr create --name algealabregistry --resource-group algelab-rg --sku Standard --admin-enabled true

# Get registry credentials
az acr credential show --name algealabregistry
```

### 2. Push Image to ACR

```bash
# Login to ACR
az acr login --name algealabregistry

# Tag the image
docker tag algelab-api algealabregistry.azurecr.io/algelab-api:latest

# Push to ACR
docker push algealabregistry.azurecr.io/algelab-api:latest
```

### 3. Deploy to Azure Web App

```bash
# Create App Service plan
az appservice plan create \
    --name algelab-plan \
    --resource-group algelab-rg \
    --sku B1 \
    --is-linux

# Create Web App
az webapp create \
    --resource-group algelab-rg \
    --plan algelab-plan \
    --name algelab-api \
    --deployment-container-image-name algealabregistry.azurecr.io/algelab-api:latest

# Configure Web App settings
az webapp config appsettings set \
    --resource-group algelab-rg \
    --name algelab-api \
    --settings @env-settings.json
```

### 4. Configure Environment Variables

Create an `env-settings.json` file:
```json
[
  {
    "name": "ENVIRONMENT",
    "value": "production"
  },
  {
    "name": "WEBSITES_PORT",
    "value": "8000"
  }
]
```

### 5. Set up Continuous Deployment (Optional)

```bash
# Enable continuous deployment
az webapp deployment container config \
    --resource-group algelab-rg \
    --name algelab-api \
    --enable-cd true
```

## Alternative Deployment Options

### Self-Hosted / On-Premise Server

1. Install Docker on your server
2. Clone the repository
3. Build and run the container:
```bash
docker build -t algelab-api .
docker run -d -p 8000:8000 --env-file .env.production algelab-api
```

### Other Cloud Providers

The Docker configuration works with any cloud provider supporting container deployment:

- **Google Cloud Run**
- **AWS Elastic Container Service (ECS)**
- **DigitalOcean App Platform**
- **Heroku Container Registry**

## Environment Configuration

### Production Environment Variables

Ensure these are configured in your deployment platform:

1. Create a production environment configuration
2. Set all required environment variables (see `env_vars.md`)
3. Configure Supabase connection settings
4. Set up GitHub SSO credentials

### SSL/TLS Configuration

For production deployments:

1. Enable HTTPS
2. Configure SSL certificates
3. Set security headers
4. Enable HSTS

## FastAPI-Specific Configuration

### Gunicorn for Production

In production, consider using Gunicorn as a process manager with Uvicorn workers:

```bash
gunicorn src.main:app --workers 4 --worker-class uvicorn.workers.UvicornWorker --bind 0.0.0.0:8000
```

Add to Dockerfile:
```dockerfile
# Install Gunicorn
RUN pip install gunicorn

# Run with Gunicorn
CMD ["gunicorn", "src.main:app", "--workers", "4", "--worker-class", "uvicorn.workers.UvicornWorker", "--bind", "0.0.0.0:8000"]
```

### API Documentation

FastAPI automatically generates documentation:

- Swagger UI: `/swagger`
- ReDoc: `/redoc`

You can disable these in production by setting `SHOW_SWAGGER=False` in your environment variables.

## Monitoring and Maintenance

### Health Checks

Monitor the health check endpoint:

- `/health` - Application health status

### Logging

Logs are stored in:
```
/app/logs/app.log
/app/logs/security.log
```

### Maintenance Tasks

Regular maintenance checklist:

1. Database backups
2. Log rotation
3. Security updates
4. Performance monitoring
5. Error tracking

## Security Considerations

1. Keep the GitHub private key secure
2. Store sensitive data in secure key vaults
3. Enable firewall rules
4. Configure CORS properly
5. Set up WAF (Web Application Firewall)
6. Enable monitoring and alerting

## Troubleshooting

Common issues and solutions:

1. **Container fails to start**
   - Check environment variables
   - Verify Supabase connectivity
   - Check log files

2. **Database connection issues**
   - Verify Supabase connection strings
   - Check network/firewall rules
   - Validate database credentials

3. **GitHub SSO problems**
   - Verify private key permissions
   - Check OAuth configurations
   - Validate callback URLs

## Need Help?

For deployment assistance:
1. Check the project documentation
2. Contact the development team
3. Join our Discord server [![Discord](https://img.shields.io/discord/1234567890?color=7289da&label=Discord&logo=discord&logoColor=white)](https://discord.gg/Q8F6xm7U)

Remember to never commit sensitive information or credentials to version control.