"""
Configuration loading, environment validation, and constants.

NOTE: https://github.com/Azure-Samples/azure-search-python-samples/blob/main/Quickstart-Agentic-Retrieval/quickstart-agentic-retrieval.ipynb
"""

import os
from dotenv import load_dotenv
#aoai_embedding_model = os.environ.get("AOAI_EMBEDDING_MODEL", "text-embedding-3-large")
#aoai_embedding_deployment = os.environ.get("AOAI_EMBEDDING_DEPLOYMENT", "text-embedding-3-large")
#aoai_gpt_model = os.environ.get("AOAI_GPT_MODEL", "gpt-5-mini")
#aoai_gpt_deployment = os.environ.get("AOAI_GPT_DEPLOYMENT", "gpt-5-mini")
#index_name = os.environ.get("INDEX_NAME", "earth-at-night")
#knowledge_source_name = os.environ.get("KNOWLEDGE_SOURCE_NAME", "earth-knowledge-source")
#knowledge_base_name = os.environ.get("KNOWLEDGE_BASE_NAME", "earth-knowledge-base")

#from azure.identity import DefaultAzureCredential, get_bearer_token_provider
#credential = DefaultAzureCredential()
#token_provider = get_bearer_token_provider(credential, "https://search.azure.com/.default")

SEARCH_ENDPOINT = "SEARCH_ENDPOINT"
AOAI_ENDPOINT = "AOAI_ENDPOINT"


def load_config() -> None:
    """Load environment variables from .env"""
    load_dotenv(override=True)


def require_env(name: str) -> str:
    """Return environment variable or raise descriptive error."""
    value = os.getenv(name)
    if not value:
        raise RuntimeError(
            f"Missing required environment variable: {name!r}. "
            "Set it in .env or your environment."
        )
    return value
