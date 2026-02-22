"""
Configuration loading, environment validation, and constants.
"""

import os
from dotenv import load_dotenv

PROJECT_ENDPOINT = "PROJECT_ENDPOINT"
MODEL_DEPLOYMENT_ENV = "MODEL_DEPLOYMENT_NAME"

DATA_FILE_NAME = "data.txt"
DATA_PREVIEW_CHARS = 400


def load_config() -> None:
    """Load .env and environment variables."""
    load_dotenv()


def require_env(name: str) -> str:
    """Return environment variable or raise descriptive error."""
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {name!r}. "
            "Set it in .env or your environment."
        )
    return value
