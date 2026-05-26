# Rccgmznl Server

Backend server for RCCG MZNL.

Built using Django and Python.

---

## Requirements

- Python 3.12.12
- pyenv
- pip
- venv

---

# Python Setup

This project uses `pyenv` to manage and lock the Python version.

## Install pyenv

### Linux

#### Arch Linux

```bash
sudo pacman -S pyenv
````

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

* pyenv-win

Using PowerShell:

```powershell
Invoke-WebRequest -UseBasicParsing `
https://pyenv-win.github.io/pyenv-win/install.ps1 `
| Invoke-Expression
```

Repository:

* [https://github.com/pyenv-win/pyenv-win](https://github.com/pyenv-win/pyenv-win)

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

```txt
docs/env.md
```

for environment configuration details.

---

# Run Development Server

```bash
python manage.py runserver 6969
```

---

# Documentation

Project-specific documentation is located in `docs/`.

## Available Docs

* Environment Variables
  `docs/env.md`

---

# Notes

* `.venv/` should not be committed
* `.python-version` should be committed
* Environment variables are loaded from `.env`
* Restart the shell after installing new Python versions if pyenv is not detected
* SQLite database files are ignored from version control
* Django migrations are committed and version controlled

---

# License
    `./LICENSE`
