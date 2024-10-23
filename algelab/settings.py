import os
from pathlib import Path
from dotenv import load_dotenv
from datetime import timedelta

BASE_DIR = Path(__file__).resolve().parent.parent

# Load environment variables from the appropriate .env file
ENVIRONMENT = os.getenv('ENVIRONMENT', 'development')

if ENVIRONMENT == 'production':
    dotenv_file = os.path.join(BASE_DIR, '.env.production')
else:
    dotenv_file = os.path.join(BASE_DIR, '.env.development')

load_dotenv(dotenv_file)

# Now you can access your environment variables
SECRET_KEY = os.environ.get('SECRET_KEY', 'your-default-secret-key')
DEBUG = True
ALLOWED_HOSTS = os.environ.get('ALLOWED_HOSTS', 'localhost,127.0.0.1').split(',')

# Application definition
INSTALLED_APPS = [
    # Default apps...
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
    # Third-party apps
    'rest_framework',
    'corsheaders',
    'drf_yasg',
    # Your app
    'algelabApp',
]

MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware', 
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    # Authentication middleware
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
]

# CORS settings
CORS_ALLOWED_ORIGINS = os.environ.get('CORS_ALLOWED_ORIGINS', 'http://localhost:5173').split(',')
CORS_ALLOW_CREDENTIALS = True

# CSRF settings
CSRF_TRUSTED_ORIGINS = os.environ.get('CSRF_TRUSTED_ORIGINS', 'http://localhost:5173').split(',')

# settings.py

SESSION_COOKIE_SECURE = os.environ.get('SESSION_COOKIE_SECURE', 'False') == 'True'
CSRF_COOKIE_SECURE = os.environ.get('CSRF_COOKIE_SECURE', 'False') == 'True'
JWT_COOKIE_SECURE = os.environ.get('JWT_COOKIE_SECURE', 'False') == 'True'
JWT_COOKIE_SAMESITE = os.environ.get('JWT_COOKIE_SAMESITE', 'Lax')


CSRF_COOKIE_SAMESITE = os.environ.get('CSRF_COOKIE_SAMESITE', 'Lax')
CSRF_COOKIE_SECURE = os.environ.get('CSRF_COOKIE_SECURE', 'False') == 'True'

ROOT_URLCONF = 'algelab.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [],  # Add your templates directory if you have one
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                # Default context processors...
                'django.template.context_processors.debug',
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'algelab.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.sqlite3',  # Use SQLite for simplicity
        'NAME': BASE_DIR / 'db.sqlite3',
    }
}

# Password validation
AUTH_PASSWORD_VALIDATORS = [
    # Default validators...
    {
        'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator',
    },
    # ... add other validators as needed
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = BASE_DIR / 'staticfiles'

# Default primary key field type
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'

# REST Framework settings
REST_FRAMEWORK = {
    'DEFAULT_AUTHENTICATION_CLASSES': [
        'algelabApp.authentication.CookieJWTAuthentication',
        'rest_framework.authentication.SessionAuthentication',
    ],
    'DEFAULT_PERMISSION_CLASSES': [
        'rest_framework.permissions.IsAuthenticated',
    ],
}

# JWT settings
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': timedelta(minutes=60),
    'REFRESH_TOKEN_LIFETIME': timedelta(days=1),
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    # ... other settings
}

# Swagger settings
SWAGGER_SETTINGS = {
    'USE_SESSION_AUTH': False,
    'SECURITY_DEFINITIONS': {
        'Bearer': {
            'type': 'apiKey',
            'name': 'Authorization',
            'in': 'header'
        }
    },
    'DEFAULT_API_URL': os.environ.get('SWAGGER_API_URL', 'http://localhost:8000')
}

# Frontend URL
FRONTEND_URL = os.environ.get('FRONTEND_URL', 'http://localhost:5173')

# GitHub OAuth Settings
GITHUB_APP_ID = os.environ.get('GITHUB_APP_ID')
GITHUB_CLIENT_ID = os.environ.get('GITHUB_CLIENT_ID')
GITHUB_CLIENT_SECRET = os.environ.get('GITHUB_CLIENT_SECRET')
GITHUB_REDIRECT_URI = os.environ.get('GITHUB_REDIRECT_URI', 'http://localhost:8000/api/auth/github/callback')

# GitHub App Private Key
GITHUB_PRIVATE_KEY_PATH = os.environ.get('GITHUB_PRIVATE_KEY_PATH', './algelab-sso.2024-10-02.private-key.pem')

try:
    with open(GITHUB_PRIVATE_KEY_PATH, 'r') as key_file:
        GITHUB_PRIVATE_KEY = key_file.read()
except FileNotFoundError:
    GITHUB_PRIVATE_KEY = None
    print(f"WARNING: GitHub private key file not found at {GITHUB_PRIVATE_KEY_PATH}. GitHub App authentication will not work.")
