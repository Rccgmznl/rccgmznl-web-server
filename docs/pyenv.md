# Pyenv Setup

This project uses `pyenv` to manage and lock the Python version used during development.

If you already have pyenv installed, return to the main README and continue with the project setup instructions.

---

# Linux

## Arch Linux

```bash
sudo pacman -S pyenv
```

---

## Ubuntu / Debian

```bash
curl https://pyenv.run | bash
```

After installation, follow the pyenv shell configuration instructions from the official documentation.

---

# macOS

Using Homebrew:

```bash
brew install pyenv
```

After installation, follow the pyenv shell configuration instructions from the official documentation.

---

# Windows

Install:

* pyenv-win

Using PowerShell:

```powershell
Invoke-WebRequest -UseBasicParsing `
https://pyenv-win.github.io/pyenv-win/install.ps1 `
| Invoke-Expression
```

Repository:

* https://github.com/pyenv-win/pyenv-win

---

# Verify Installation

Restart your terminal and run:

```bash
pyenv --version
```

Expected output:

```txt
pyenv <version>
```

---

# Install Project Python Version

```bash
pyenv install 3.12.12
```

---

# References

Official documentation:

* https://github.com/pyenv/pyenv
* https://github.com/pyenv-win/pyenv-win

Return to the main project README after completing installation.
--
