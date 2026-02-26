"""
Entry point for the rag-llm CLI.
"""
from typing import List, Tuple 
import logging

from chat_client import create_chat_client, chat_instructions, get_rag_params
from chat_turn import chat_turn
import config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
log = logging.getLogger("main")


def run_rag(
    user_id: str #user_message: str, 
    #prior_messages: List[dict] | None = None
) -> Tuple[str, List[dict]]:

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

    prior_messages = get_prior_messages(
        user_id, # Cosmos credentials
    )

    messages = prior_messages[:] if prior_messages else list(instructions)
    answer, updated_messages = chat_turn(
        chat_client, chat_model, messages, rag_params, user_message
    )

    update_prior_messages(updated_messages)

    return answer#, updated_messages


if __name__ == "__main__":
    print(run_rag("userID-123"))
    