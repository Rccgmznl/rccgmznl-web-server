# Environment Configuration

Environment variables are managed through the centralized environment loader located at:

```txt
config/env.py
```

---

# Philosophy

The environment configuration system intentionally avoids unnecessary abstraction and hidden behavior.

The goal is to keep configuration:

* explicit
* readable
* debuggable
* predictable

Environment variables are loaded centrally, while parsing remains close to where values are used.

Examples:

* boolean parsing is handled inline
* list parsing is handled inline
* environment-specific behavior is handled explicitly

This keeps configuration easy to trace and reduces unnecessary complexity during development.

---

# Environment Loading

Environment variables are loaded from:

```txt
.env
```

during application startup.

A `.env` file is required for local development.

Create one from the example template:

```bash
cp .env.example .env
```

---

# Environment Files

## `.env`

Local runtime configuration.

Should never be committed to version control.

---

## `.env.example`

Template containing all required environment variables.

Safe to commit.

Used for:

* onboarding
* deployment setup
* configuration reference

---

# Database Configuration

The project supports both SQLite and PostgreSQL.

## SQLite Development

Recommended for:

* quick experimentation
* feature development
* contributors who do not need Docker
* contributors who do not need a shared PostgreSQL environment

Example:

```env
DATABASE_USE_SQLITE=true
DATABASE_SQLITE_NAME=db.sqlite3
```

When SQLite is enabled, PostgreSQL configuration is ignored.

---

## PostgreSQL Development

Recommended for:

* Docker development
* testing production-like behavior
* validating migrations
* team development

Example:

```env
DATABASE_USE_SQLITE=false

DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=rccgmznl
DATABASE_USER=postgres
DATABASE_PASSWORD=<set-a-local-secret>
DATABASE_HOST=127.0.0.1
DATABASE_PORT=5432
```

For Docker Compose development:

```env
DATABASE_USE_SQLITE=false

DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=rccgmznl
DATABASE_USER=postgres
DATABASE_PASSWORD=<set-a-local-secret>
DATABASE_HOST=db
DATABASE_PORT=5432
```

The Docker network exposes the database service using the hostname:

```txt
db
```

instead of:

```txt
127.0.0.1
```

---

# Example Configuration

```env
DJANGO_DEBUG=true

DJANGO_SECRET_KEY=

DJANGO_ALLOWED_HOSTS=127.0.0.1,localhost

DJANGO_LANGUAGE_CODE=en-us
DJANGO_TIME_ZONE=UTC
DJANGO_USE_I18N=true
DJANGO_USE_TZ=true

DATABASE_USE_SQLITE=false
DATABASE_SQLITE_NAME=db.sqlite3

DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=rccgmznl
DATABASE_USER=postgres
DATABASE_PASSWORD=<set-a-local-secret>
DATABASE_HOST=127.0.0.1
DATABASE_PORT=5432
```

---

# Accessing Environment Variables

Environment variables should be accessed through:

```python
from config.env import get_env
```

Example:

```python
DEBUG = (
    get_env(
        "DJANGO_DEBUG",
        default="false",
    ).lower()
    == "true"
)
```

Avoid direct access to:

```python
os.getenv(...)
```

throughout the codebase.

---

# Notes

* All environment variables are loaded as strings
* Parsing is intentionally handled explicitly
* Environment access should be centralized through `config/env.py`
* SQLite is intended primarily for local development
* PostgreSQL should be used when validating deployment-related behavior

---

# Security

Never commit:

```txt
.env
```

to version control.

Sensitive values such as:

* Django secret keys
* database credentials
* API keys
* third-party service credentials

must remain private.

Use `.env.example` as the public reference for required configuration.
