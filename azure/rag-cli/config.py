"""
Configuration loading, environment validation, and constants.
"""

import os
from dotenv import load_dotenv

# Name of the chat completion LLM (see asses -> models + endpoints)
CHAT_MODEL = "CHAT_MODEL"
# Name of index under assets in Foundry portal
INDEX_NAME = "INDEX_NAME"
# The Azure AI Search resource API key
SEARCH_KEY = "SEARCH_KEY"
# The Open AI API key at Overview page of the project (Foundry portal)
OPEN_AI_KEY = "OPEN_AI_KEY"
# Name of the embedding model (see asses -> models + endpoints)
EMBEDDING_MODEL = "EMBEDDING_MODEL"
# The Azure AI Search resource URL (see management center in Foundry portal)
SEARCH_ENDPOINT = "SEARCH_ENDPOINT"
# The Open AI endpoint at Overview page of the project (Foundry portal)
OPEN_AI_ENDPOINT = "OPEN_AI_ENDPOINT"


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
