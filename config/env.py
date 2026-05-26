from pathlib import Path
import os

from dotenv import load_dotenv

# ==========================
# Project Base Directory
# ==========================
#
# Resolves to the project root directory.
#
# Example:
# /home/user/project/
#
BASE_DIR = Path(__file__).resolve().parent.parent

# ==========================
# Environment File Path
# ==========================
#
# Centralized .env file location.
#
ENV_PATH = BASE_DIR / ".env"

# ==========================
# Environment Validation
# ==========================
#
# Prevent the application from starting
# if the .env file is missing.
#
if not ENV_PATH.exists():
    raise FileNotFoundError(
        ".env file missing. Server cannot start."
    )

# ==========================
# Load Environment Variables
# ==========================
#
# Loads all variables from the .env file
# into the runtime environment.
#
load_dotenv(ENV_PATH)


def get_env(
    key: str,
    default: str | None = None,
    required: bool = False,
) -> str:
    """
    Retrieve an environment variable.

    Args:
        key:
            Environment variable name.

        default:
            Fallback value if variable is missing.

        required:
            If True, raises an error when
            the variable is missing or empty.

    Returns:
        str:
            Environment variable value.
    """

    value = os.getenv(key, default)

    # ==========================
    # Required Environment Validation
    # ==========================
    #
    # Fail fast if a required variable
    # is missing to prevent invalid
    # application startup.
    #
    if required and not value:
        raise ValueError(
            f"Missing required environment variable: {key}"
        )

    return value
