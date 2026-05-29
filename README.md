# Rccgmznl Server

Backend server for RCCG MZNL.

Built using Django and Python.

---

# MUST READ

Before contributing or committing any code, please read:

- [Git Workflow](docs/git-flow.md)
- [Environment Variables](docs/env.md)

This helps keep the repository history clean and reduces merge conflicts during development.

---

## Requirements

- Python 3.12.12
- pyenv
- pip
- venv
- Docker
- Docker Compose

---

# Python Setup

This project uses `pyenv` to manage and lock the Python version.

## Install pyenv

### Linux

#### Arch Linux

```bash
sudo pacman -S pyenv
```

#### Ubuntu / Debian

```bash
curl https://pyenv.run | bash
```

---

### macOS

Using Homebrew:

```bash
brew install pyenv
```

---

### Windows

Install:

- pyenv-win

Using PowerShell:

```powershell
Invoke-WebRequest -UseBasicParsing `
https://pyenv-win.github.io/pyenv-win/install.ps1 `
| Invoke-Expression
```

Repository:

- https://github.com/pyenv-win/pyenv-win

---

## Install Python Version

```bash
pyenv install 3.12.12
```

---

## Set Local Python Version

Run inside the project root:

```bash
pyenv local 3.12.12
```

This creates:

```txt
.python-version
```

---

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

---

## Activate Virtual Environment

### Linux / macOS

```bash
source .venv/bin/activate
```

### Windows (PowerShell)

```powershell
.venv\\Scripts\\Activate.ps1
```

---

# Install Dependencies

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

- [Environment Variables Documentation](docs/env.md)

for environment configuration details.

---

# Run Development Server

```bash
python manage.py runserver 8000
```

---

# Docker Compose Development

The repository includes a development compose setup with:

- PostgreSQL service
- Web service built from this project
- Source code volume mount for live code changes

## 1. Ensure Environment Variables

Set the database values in `.env` to match the docker-compose defaults:

```env
DATABASE_ENGINE=django.db.backends.postgresql
DATABASE_NAME=rccgmznl
DATABASE_USER=postgres
DATABASE_PASSWORD=<set-a-local-secret>
DATABASE_HOST=db
DATABASE_PORT=5432
```

`DATABASE_PASSWORD` is required and must be set locally in `.env`.
Do not commit real passwords to version control.

## 2. Build and Start Services

```bash
docker compose -f docker-compose.dev.yml up --build
```

## 3. Access Application

- Django: http://localhost:8000
- PostgreSQL: localhost:5432

## 4. Stop Services

```bash
docker compose -f docker-compose.dev.yml down
```

## 5. Create Django Superuser

Run this after the containers are up:

```bash
docker compose -f docker-compose.dev.yml exec web python manage.py createsuperuser
```

For non-docker local development:

```bash
python manage.py createsuperuser
```

---

# Documentation

Project-specific documentation is located in `docs/`.

## Available Docs

- [Git Workflow](docs/git-flow.md)
- [Environment Variables](docs/env.md)
- [References](docs/references.md)

---

# Notes

- `.venv/` should not be committed
- `.python-version` should be committed
- Environment variables are loaded from `.env`
- Restart the shell after installing new Python versions if pyenv is not detected
- Django migrations are committed and version controlled

---

# License

See:

```txt
./LICENSE
```
