from pathlib import Path

from config.env import get_env

# ==========================
# Project Base Directory
# ==========================
#
# Resolves to the root project directory.
#
# Example:
# /home/user/project/
#
BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================
# Security Configuration
# ==========================
#
# Core Django security settings.
#
# SECRET_KEY:
# Required cryptographic secret used by Django.
#
# DEBUG:
# Enables development debugging features.
# Must always be disabled in production.
#
SECRET_KEY = get_env(
    "DJANGO_SECRET_KEY",
    required=True,
)

DEBUG = (
    get_env(
        "DJANGO_DEBUG",
        default="false",
    ).lower()
    == "true"
)

# ==========================
# Allowed Hosts
# ==========================
#
# Comma-separated hosts allowed to serve
# the application.
#
# Example:
# DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost
#
ALLOWED_HOSTS = [
    host.strip()
    for host in get_env(
        "DJANGO_ALLOWED_HOSTS",
        default="127.0.0.1,localhost",
    ).split(",")
    if host.strip()
]

# ==========================
# Installed Applications
# ==========================
#
# Core Django applications enabled
# for the project.
#
INSTALLED_APPS = [
    "jazzmin",
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
    "corsheaders",
    "rest_framework",
    "django_filters",
]

# ==========================
# Middleware
# ==========================
#
# Global request/response middleware stack.
#
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
    "corsheaders.middleware.CorsMiddleware",
    "django.contrib.sessions.middleware.SessionMiddleware",
    "django.middleware.common.CommonMiddleware",
    "django.middleware.csrf.CsrfViewMiddleware",
    "django.contrib.auth.middleware.AuthenticationMiddleware",
    "django.contrib.messages.middleware.MessageMiddleware",
    "django.middleware.clickjacking.XFrameOptionsMiddleware",
]

# ==========================
# URL Configuration
# ==========================

ROOT_URLCONF = "config.urls"

# ==========================
# Template Configuration
# ==========================
#
# Required for Django admin and template
# rendering support.
#
TEMPLATES = [
    {
        "BACKEND": (
            "django.template.backends.django."
            "DjangoTemplates"
        ),
        "DIRS": [],
        "APP_DIRS": True,
        "OPTIONS": {
            "context_processors": [
                (
                    "django.template.context_processors."
                    "request"
                ),
                (
                    "django.contrib.auth.context_processors."
                    "auth"
                ),
                (
                    "django.contrib.messages.context_processors."
                    "messages"
                ),
            ],
        },
    },
]

# ==========================
# WSGI Application
# ==========================

WSGI_APPLICATION = "config.wsgi.application"

# ==========================
# Database Configuration
# ==========================
#
# Supports PostgreSQL by default and SQLite when
# DATABASE_USE_SQLITE is set to true.
#
DATABASE_USE_SQLITE = (
    get_env(
        "DATABASE_USE_SQLITE",
        default="false",
    ).lower()
    == "true"
)

if DATABASE_USE_SQLITE:
    DATABASES = {
        "default": {
            "ENGINE": "django.db.backends.sqlite3",
            "NAME": (
                BASE_DIR
                / get_env(
                    "DATABASE_SQLITE_NAME",
                    default="db.sqlite3",
                )
            ),
        }
    }

else:
    DATABASES = {
        "default": {
            "ENGINE": get_env(
                "DATABASE_ENGINE",
                default="django.db.backends.postgresql",
            ),
            "NAME": get_env(
                "DATABASE_NAME",
                default="rccgmznl",
            ),
            "USER": get_env(
                "DATABASE_USER",
                default="postgres",
            ),
            "PASSWORD": get_env(
                "DATABASE_PASSWORD",
                required=True,
            ),
            "HOST": get_env(
                "DATABASE_HOST",
                default="127.0.0.1",
            ),
            "PORT": get_env(
                "DATABASE_PORT",
                default="5432",
            ),
        }
    }

# ==========================
# API Configuration
# ==========================
#
# Core DRF defaults for response shape, error handling,
# throttling, pagination, filtering, ordering, and
# URL-based versioning.
#
API_DEFAULT_VERSION = get_env(
    "API_DEFAULT_VERSION",
    default="v1",
)

API_ALLOWED_VERSIONS = [
    version.strip()
    for version in get_env(
        "API_ALLOWED_VERSIONS",
        default="v1",
    ).split(",")
    if version.strip()
]

API_PAGE_SIZE = int(
    get_env(
        "API_PAGE_SIZE",
        default="20",
    )
)

API_THROTTLE_ANON_RATE = get_env(
    "API_THROTTLE_ANON_RATE",
    default="100/hour",
)

API_THROTTLE_USER_RATE = get_env(
    "API_THROTTLE_USER_RATE",
    default="1000/hour",
)

DEFAULT_RENDERER_CLASSES = [
    "config.api_renderers.StandardizedJSONRenderer",
]

if DEBUG:
    DEFAULT_RENDERER_CLASSES.append(
        "rest_framework.renderers.BrowsableAPIRenderer"
    )

REST_FRAMEWORK = {
    "EXCEPTION_HANDLER": (
        "config.api_exceptions.custom_exception_handler"
    ),
    "DEFAULT_RENDERER_CLASSES": DEFAULT_RENDERER_CLASSES,
    "DEFAULT_VERSIONING_CLASS": (
        "rest_framework.versioning.URLPathVersioning"
    ),
    "DEFAULT_VERSION": API_DEFAULT_VERSION,
    "ALLOWED_VERSIONS": API_ALLOWED_VERSIONS,
    "DEFAULT_THROTTLE_CLASSES": [
        "rest_framework.throttling.AnonRateThrottle",
        "rest_framework.throttling.UserRateThrottle",
    ],
    "DEFAULT_THROTTLE_RATES": {
        "anon": API_THROTTLE_ANON_RATE,
        "user": API_THROTTLE_USER_RATE,
    },
    "DEFAULT_PAGINATION_CLASS": (
        "rest_framework.pagination.PageNumberPagination"
    ),
    "PAGE_SIZE": API_PAGE_SIZE,
    "DEFAULT_FILTER_BACKENDS": [
        (
            "django_filters.rest_framework."
            "DjangoFilterBackend"
        ),
        "rest_framework.filters.SearchFilter",
        "rest_framework.filters.OrderingFilter",
    ],
}

# ==========================
# CORS Configuration
# ==========================
#
# Comma-separated list of allowed frontend origins.
#
CORS_ALLOWED_ORIGINS = [
    origin.strip()
    for origin in get_env(
        "CORS_ALLOWED_ORIGINS",
        default="http://localhost:3000,http://127.0.0.1:3000",
    ).split(",")
    if origin.strip()
]

CORS_ALLOW_CREDENTIALS = (
    get_env(
        "CORS_ALLOW_CREDENTIALS",
        default="true",
    ).lower()
    == "true"
)

# ==========================
# Password Validation
# ==========================
#
# Built-in Django password validation.
#
AUTH_PASSWORD_VALIDATORS = [
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "UserAttributeSimilarityValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "MinimumLengthValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "CommonPasswordValidator"
        ),
    },
    {
        "NAME": (
            "django.contrib.auth.password_validation."
            "NumericPasswordValidator"
        ),
    },
]

# ==========================
# Internationalization
# ==========================
#
# Localization and timezone settings.
#
LANGUAGE_CODE = get_env(
    "DJANGO_LANGUAGE_CODE",
    default="en-us",
)

TIME_ZONE = get_env(
    "DJANGO_TIME_ZONE",
    default="UTC",
)

USE_I18N = (
    get_env(
        "DJANGO_USE_I18N",
        default="true",
    ).lower()
    == "true"
)

USE_TZ = (
    get_env(
        "DJANGO_USE_TZ",
        default="true",
    ).lower()
    == "true"
)

# ==========================
# Static Files
# ==========================
#
# Static asset configuration.
#
STATIC_URL = "static/"

STATIC_ROOT = (
    BASE_DIR / "staticfiles"
)

# ==========================
# Default Primary Key Type
# ==========================
#
# Default auto-generated model primary key.
#
DEFAULT_AUTO_FIELD = (
    "django.db.models.BigAutoField"
)
