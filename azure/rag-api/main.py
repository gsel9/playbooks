"""
Entry point for the rag-llm CLI.
"""

import logging

from chat_client import create_chat_client, chat_instructions, get_rag_params
from chat_loop import chat_loop
import config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
log = logging.getLogger("main")


def run_rag() -> None:
    config.load_config()

    chat_model = config.require_env(config.CHAT_MODEL)
    index_name = config.require_env(config.INDEX_NAME)
    search_key = config.require_env(config.SEARCH_KEY)
    open_ai_key = config.require_env(config.OPEN_AI_KEY)
    embedding_model = config.require_env(config.EMBEDDING_MODEL)
    search_endpoint = config.require_env(config.SEARCH_ENDPOINT)
    open_ai_endpoint = config.require_env(config.OPEN_AI_ENDPOINT)

    chat_client = create_chat_client(open_ai_endpoint, open_ai_key)
    instructions = chat_instructions()

    rag_params = get_rag_params(
        search_endpoint, search_key, index_name, embedding_model
    )

    chat_loop(chat_client, chat_model, instructions, rag_params)


if __name__ == "__main__":
    run_rag()
