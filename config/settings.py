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
    "django.contrib.admin",
    "django.contrib.auth",
    "django.contrib.contenttypes",
    "django.contrib.sessions",
    "django.contrib.messages",
    "django.contrib.staticfiles",
]

# ==========================
# Middleware
# ==========================
#
# Global request/response middleware stack.
#
MIDDLEWARE = [
    "django.middleware.security.SecurityMiddleware",
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
# Supports:
# - SQLite for local development
# - External relational databases
#
# SQLite is enabled by default.
#
DATABASE_USE_SQLITE = (
    get_env(
        "DATABASE_USE_SQLITE",
        default="true",
    ).lower()
    == "true"
)

if DATABASE_USE_SQLITE:
    DATABASES = {
        "default": {
            "ENGINE": (
                "django.db.backends.sqlite3"
            ),
            "NAME": (
                BASE_DIR
                / get_env(
                    "DATABASE_NAME",
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
                required=True,
            ),
            "NAME": get_env(
                "DATABASE_NAME",
                required=True,
            ),
            "USER": get_env(
                "DATABASE_USER",
                required=True,
            ),
            "PASSWORD": get_env(
                "DATABASE_PASSWORD",
                required=True,
            ),
            "HOST": get_env(
                "DATABASE_HOST",
                required=True,
            ),
            "PORT": get_env(
                "DATABASE_PORT",
                required=True,
            ),
        }
    }

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
