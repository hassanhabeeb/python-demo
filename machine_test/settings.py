import os
import datetime
from pathlib import Path
from django.core.exceptions import ImproperlyConfigured

# Load all SSM parameters into environment variables
from ssm_loader import fetch_all_ssm_parameters
fetch_all_ssm_parameters()  # Loads all parameters under the prefix into os.environ

# Build paths
BASE_DIR = Path(__file__).resolve().parent.parent

# Helpers
def get_list(value, default=""):
    return [v.strip() for v in os.getenv(value, default).split(",")]

def get_bool(value, default=False):
    return os.getenv(value, str(default)).lower() in ("true", "1", "yes")

def get_env(name, default=None, required=False):
    val = os.getenv(name, default)
    if required and val is None:
        raise ImproperlyConfigured(f"The environment variable {name} is required but not set.")
    return val

# Security
SECRET_KEY = get_env("SECRET_KEY", required=True)
DEBUG = get_bool("DEBUG", False)
ENVIRONMENT = get_env("ENVIRONMENT", "local")
ALLOWED_HOSTS = get_list("ALLOWED_HOSTS", "127.0.0.1,localhost")

# CSRF & CORS
CSRF_TRUSTED_ORIGINS = get_list("CSRF_TRUSTED_ORIGINS", "http://localhost:3000")
CORS_ALLOWED_ORIGINS = get_list("CORS_ALLOWED_ORIGINS", "http://localhost:3000")
CORS_ORIGIN_WHITELIST = get_list("CORS_ORIGIN_WHITELIST", "http://localhost:3000")

# Internal IPs
INTERNAL_IPS = get_list("INTERNAL_IPS", "127.0.0.1")

# Installed apps
DJANGO_APPS = [
    'django.contrib.admin',
    'django.contrib.auth',
    'django.contrib.contenttypes',
    'django.contrib.sessions',
    'django.contrib.messages',
    'django.contrib.staticfiles',
]

THIRD_PARTY_APPS = [
    'corsheaders',
    'debug_toolbar',
    'rest_framework',
    'drf_spectacular',
    'drf_yasg',
    'django_filters',
]

LOCAL_APPS = [
    'apps.products',  # Adjust as needed
]

INSTALLED_APPS = DJANGO_APPS + THIRD_PARTY_APPS + LOCAL_APPS

# Middleware
MIDDLEWARE = [
    'django.middleware.security.SecurityMiddleware',
    'django.contrib.sessions.middleware.SessionMiddleware',
    'corsheaders.middleware.CorsMiddleware',
    'django.middleware.common.CommonMiddleware',
    'django.middleware.csrf.CsrfViewMiddleware',
    'django.contrib.auth.middleware.AuthenticationMiddleware',
    'django.contrib.messages.middleware.MessageMiddleware',
    'django.middleware.clickjacking.XFrameOptionsMiddleware',
    'debug_toolbar.middleware.DebugToolbarMiddleware',
]

ROOT_URLCONF = 'machine_test.urls'

TEMPLATES = [
    {
        'BACKEND': 'django.template.backends.django.DjangoTemplates',
        'DIRS': [os.path.join(BASE_DIR, 'templates')],
        'APP_DIRS': True,
        'OPTIONS': {
            'context_processors': [
                'django.template.context_processors.request',
                'django.contrib.auth.context_processors.auth',
                'django.contrib.messages.context_processors.messages',
            ],
        },
    },
]

WSGI_APPLICATION = 'machine_test.wsgi.application'

# Database
DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.postgresql',
        'NAME': get_env("DATABASE_NAME", required=True),
        'USER': get_env("DATABASE_USER", required=True),
        'PASSWORD': get_env("DATABASE_PASSWORD", required=True),
        'HOST': get_env("DATABASE_HOST", "localhost"),
        'PORT': get_env("DATABASE_PORT", "5432"),
        'CONN_MAX_AGE': int(get_env("DB_CONN_MAX_AGE", 60)),
        'OPTIONS': {
            'sslmode': get_env("DB_SSLMODE", "prefer")
        },
    }
}

# Static files
STATIC_URL = '/static/'
STATIC_ROOT = os.path.join(BASE_DIR, 'staticfiles')

# Media files (optional)
MEDIA_URL = '/media/'
MEDIA_ROOT = os.path.join(BASE_DIR, 'media')

# Auth
AUTH_PASSWORD_VALIDATORS = [
    {'NAME': 'django.contrib.auth.password_validation.UserAttributeSimilarityValidator'},
    {'NAME': 'django.contrib.auth.password_validation.MinimumLengthValidator'},
    {'NAME': 'django.contrib.auth.password_validation.CommonPasswordValidator'},
    {'NAME': 'django.contrib.auth.password_validation.NumericPasswordValidator'},
]

# Internationalization
LANGUAGE_CODE = 'en-us'
TIME_ZONE = 'UTC'
USE_I18N = True
USE_TZ = True
DEFAULT_AUTO_FIELD = 'django.db.models.BigAutoField'
APPEND_SLASH = False
ATOMIC_REQUESTS = True
DATA_UPLOAD_MAX_NUMBER_FIELDS = 10000

# DRF
REST_FRAMEWORK = {
    'DEFAULT_SCHEMA_CLASS': 'drf_spectacular.openapi.AutoSchema',
    'DEFAULT_PAGINATION_CLASS': 'rest_framework.pagination.PageNumberPagination',
    'PAGE_SIZE': 10,
    'DEFAULT_AUTHENTICATION_CLASSES': (
        'rest_framework.authentication.TokenAuthentication',
        'rest_framework_simplejwt.authentication.JWTAuthentication',
    ),
    'DEFAULT_FILTER_BACKENDS': [
        'django_filters.rest_framework.DjangoFilterBackend',
        'rest_framework.filters.SearchFilter',
        'rest_framework.filters.OrderingFilter',
    ],
}

# JWT config
SIMPLE_JWT = {
    'ACCESS_TOKEN_LIFETIME': datetime.timedelta(days=20),
    'REFRESH_TOKEN_LIFETIME': datetime.timedelta(days=50),
    'ALGORITHM': 'HS256',
    'SIGNING_KEY': SECRET_KEY,
    'AUTH_HEADER_TYPES': ('Bearer',),
    'AUTH_HEADER_NAME': 'HTTP_AUTHORIZATION',
    'USER_ID_FIELD': 'id',
    'USER_ID_CLAIM': 'user_id',
}

# Spectacular (OpenAPI)
SPECTACULAR_SETTINGS = {
    'TITLE': 'Machine Test API',
    'DESCRIPTION': 'Auto-generated API documentation',
    'VERSION': '1.0.0',
    'SERVE_INCLUDE_SCHEMA': False,
    'COMPONENT_SPLIT_REQUEST': True,
    'SWAGGER_UI_SETTINGS': {
        'deepLinking': True,
        'displayOperationId': True,
        'persistAuthorization': True,
    },
    'SECURITY': [{'BearerAuth': []}],
}
