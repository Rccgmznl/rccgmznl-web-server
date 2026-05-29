# RCCG MZNL Server

Backend server for RCCG MZNL.

Built using Django and Python.

---

# MUST READ

Before contributing or committing any code, please read:

* [Git Workflow](docs/git-flow.md)
* [Environment Variables](docs/env.md)
* [Pyenv Setup](docs/pyenv.md)
* [Docker Setup](docs/docker.md)

### Which setup should I use?

**Docker (recommended)**

Use Docker if you want the standard development environment used by the team, including PostgreSQL and other project services.

**Pyenv / Virtual Environment**

Use this approach if you prefer running the application directly on your machine, want a lightweight setup, are experimenting locally, or do not need the full Docker environment. This setup can also be used with SQLite for quick development workflows. See the environment variable documentation for database configuration options.

Reading these documents helps keep the repository history clean and reduces merge conflicts during development.

---

## Requirements

Required:

* Python 3.12.12
* Docker
* Docker Compose

Optional:

* pyenv
* pip
* venv

---

# Python Setup (Pyenv)

See the [Pyenv Setup](docs/pyenv.md) documentation for installation instructions.

You may also refer to the official documentation links listed in [References](docs/references.md).

## Install Python Version

```bash
pyenv install 3.12.12
```

## Set Local Python Version

Run inside the project root:

```bash
pyenv local 3.12.12
```

This creates:

```txt
.python-version
```

## Verify Python Version

```bash
python --version
```

Expected:

```txt
Python 3.12.12
```

---

# Virtual Environment

## Create Virtual Environment

```bash
python -m venv .venv
```

## Activate Virtual Environment

Linux / macOS:

```bash
source .venv/bin/activate
```

Windows (PowerShell):

```powershell
.venv\Scripts\Activate.ps1
```

## Install Dependencies

```bash
pip install -r requirements.txt
```

---

# Environment Variables

Copy:

```bash
cp .env.example .env
```

Update the values inside `.env`.

See:

* [Environment Variables Documentation](docs/env.md)

for configuration details.

---

# Run Development Server

```bash
python manage.py migrate
python manage.py runserver 8000
```

---

# Docker Development

The repository includes a development Docker Compose setup with:

* PostgreSQL
* Django application container
* Source code volume mounts for development

## 1. Configure Environment Variables

Copy:

```bash
cp .env.example .env
```

Review the environment variable documentation for configuration details:

* [Environment Variables Documentation](docs/env.md)

## 2. Build and Start Services

```bash
docker compose -f docker-compose.dev.yml up --build
```

## 3. Access Services

* Django: http://localhost:8000
* PostgreSQL: localhost:5432

## 4. Create Django Superuser

```bash
docker compose -f docker-compose.dev.yml exec web python manage.py createsuperuser
```

## 5. Stop Services

```bash
docker compose -f docker-compose.dev.yml down
```

---

# Documentation

Project-specific documentation is located in `docs/`.

Available documentation:

* [Git Workflow](docs/git-flow.md)
* [Environment Variables](docs/env.md)
* [Pyenv Setup](docs/pyenv.md)
* [Docker Setup](docs/docker.md)
* [References](docs/references.md)

---

# Notes

* `.venv/` should not be committed
* `.python-version` should be committed
* Environment variables are loaded from `.env`
* Django migrations are committed and version controlled
* Restart your shell if pyenv changes are not detected

---

# License

See `LICENSE`.
