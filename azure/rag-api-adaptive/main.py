"""
Entry point for the rag-llm CLI.
"""
from typing import List, Dict
import logging

from history_db import is_new_user, schema, create_item, get_prior_messages, append_to_history
from chat_client import create_chat_client, chat_instructions
from chat_turn import chat_turn
from rag import (
    run_vector_search, 
    create_search_client, 
    create_embedding_client,
    create_context_message
)
import config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
log = logging.getLogger("main")


def run_rag(
    item_id: str,
    user_id: str,
    conv_id: str,
    user_input: str,
    use_k_last: int = 10
):
    """
    TODO
    """
    if is_new_user(user_id):
        log.info("Initialize item for new user: %s", user_id)
        create_item(schema(item_id, user_id, conv_id))

        log.info("Starting a new conversation history")
        messages = list(chat_instructions())
    else:
        log.info("Getting existing conversation history")
        messages = get_prior_messages(user_id, conv_id)[0]["messages"]

    if len(messages) > use_k_last:
        log.info("Truncating messages")
        messages = _safe_trucate_messages(messages, use_k_last)

    config.load_config()

    chat_model = config.require_env(config.CHAT_MODEL)
    index_name = config.require_env(config.INDEX_NAME)
    search_key = config.require_env(config.SEARCH_KEY)
    open_ai_key = config.require_env(config.OPEN_AI_KEY)
    embedding_model = config.require_env(config.EMBEDDING_MODEL)
    search_endpoint = config.require_env(config.SEARCH_ENDPOINT)
    open_ai_endpoint = config.require_env(config.OPEN_AI_ENDPOINT)

    chat_client = create_chat_client(open_ai_endpoint, open_ai_key)
    embed_client = create_embedding_client(open_ai_endpoint, open_ai_key)
    search_client = create_search_client(search_endpoint, index_name, search_key)

    # Check retrieval results before calling the chat model
    context = run_vector_search(search_client, embed_client, embedding_model, user_input)
    if bool(context):
        log.info("Inserting context into message history")
        messages = create_context_message(messages, context)
    else:
        log.info("Could not find any relevant context")

    # Append user message
    messages.append({"role": "user", "content": user_input.strip()})

    answer = chat_turn(chat_client, chat_model, messages)
    if answer is None:
        log.warning("Answer failed")
        return
    
    # Append user input to conversation history
    append_to_history(item_id, user_id, conv_id, {"role": "user", "content": user_input})
    # Append model response to conversation history
    append_to_history(item_id, user_id, conv_id, {"role": "system", "content": answer})

    return answer


def _safe_trucate_messages(history: List[Dict], use_k_last: int) -> List[Dict]:
    """
    """
    # Include model instrutions
    messages = list(chat_instructions())
    # Include latest messages
    messages.extend(history[-use_k_last:])
    return messages


if __name__ == "__main__":
    #print(run_rag("000", "user-000", "conv-000", "Give me a one-liner about London"))
    #print(run_rag("000", "user-000", "conv-000", "Please summarize our conversation"))
    #print(run_rag("000", "user-000", "conv-000", "What was the first message I sent you?"))
    # NOTE: Expect this message to fail bc no info in AI Search about Oslo
    # => the retrieval returns no results
    #print(run_rag("000", "user-000", "conv-000", "Tell me about Oslo!"))
    #print(run_rag("002", "user-002", "conv-002", "Tell me about Oslo!"))
    print(run_rag("002", "user-002", "conv-002", "Give me a one-liner about London"))
