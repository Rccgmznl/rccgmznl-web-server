# Environment Configuration

Environment variables are managed using a centralized environment loader located in:

```txt
config/env.py
````

---

# Philosophy

The environment configuration system intentionally avoids unnecessary abstraction and hidden behavior.

The goal is to keep configuration:

* explicit
* readable
* debuggable
* predictable

Environment variables are loaded centrally, but parsing behavior remains close to where values are used.

Examples:

* boolean parsing is handled inline
* list parsing is handled inline
* environment-specific behavior is handled explicitly

This avoids introducing unnecessary helper abstractions early in development.

---

# Environment Loading

The application loads environment variables from:

```txt 
.env
```

during startup.

If the `.env` file is missing, the server will fail to start.

This ensures required runtime configuration is always available.

---

# Environment Files

## `.env`

Local runtime environment configuration.

Should never be committed.

---

## `.env.example`

Template containing all required environment variables.

Safe to commit.

Used for:

* onboarding
* deployment setup
* configuration reference

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

# Database
DATABASE_USE_SQLITE=true

DATABASE_ENGINE=django.db.backends.sqlite3
DATABASE_NAME=db.sqlite3

DATABASE_USER=
DATABASE_PASSWORD=
DATABASE_HOST=
DATABASE_PORT=
```

---

# Accessing Environment Variables

Environment variables are accessed using:

```py 
from config.env import get_env
```

Example:

```py 
DEBUG = (
    get_env(
        "DJANGO_DEBUG",
        default="false",
    ).lower()
    == "true"
)
```

---

# Notes

* All environment variables are loaded as strings
* Parsing is intentionally handled explicitly
* Avoid directly accessing `os.getenv()` throughout the application
* Centralize environment access through `config/env.py`

---

# Security

Never commit:

```txt 
.env
```

to version control.

Sensitive values such as:

* secret keys
* database credentials
* API keys

must remain private.
