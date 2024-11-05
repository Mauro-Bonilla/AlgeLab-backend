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
    && touch /app/logs/django.log \
    && touch /app/logs/security.log \
    && chmod -R 755 /app/logs

# Make migrations directory writable
RUN chmod -R 755 /app/algelabApp/migrations

# Create a non-root user and adjust permissions for all files
RUN useradd -m appuser && chown -R appuser:appuser /app

# Switch to non-root user
USER appuser

# Expose port
EXPOSE 8000

# Run the application using Gunicorn
CMD ["gunicorn", "--bind", "0.0.0.0:8000", "algelab.wsgi:application"]
