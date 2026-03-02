"""
Entry point for the rag-llm CLI.
"""
from typing import List, Tuple 
import logging

from history_db import is_new_user, get_prior_messages, append_to_history
from chat_client import create_chat_client, chat_instructions
from chat_turn import chat_turn
from rag import run_vector_search, create_search_client, create_embedding_client
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

    if is_new_user(user_id):
        messages = list(instructions)
    else:
        messages = get_prior_messages(user_id, conv_id)[0]["messages"]
    # Truncate chat history to include only k last messages
    messages_trunc = messages[-use_k_last:]

    # Append user message
    messages_trunc.append({"role": "user", "content": user_input.strip()})

    search_client = create_search_client(search_endpoint, index_name, search_key)
    embed_client = create_embedding_client(open_ai_endpoint, open_ai_key)

    # Check retrieval results before calling the chat model
    results = run_vector_search(search_client, embed_client, embedding_model, user_input)

    assert False, "TODO"

    if bool(results):
        rag_context = format_docs_for_context(retrieved_docs)
        messages_trunc.append({
            "role": "system",
            "content": f"Use the following information to answer:\n\n{rag_context}"
        })
        answer = chat_turn(chat_client, chat_model, messages_trunc, extra_body=None)
    else:
        # fallback: general knowledge answer
        answer = chat_turn(chat_client, chat_model, messages_trunc, extra_body=None)


    if use_rag:
        # Not enough context: only LLM answering
        answer = chat_turn_with_rag(chat_client, chat_model, messages_trunc)
    else:
        # Useful context found: use RAG
        answer = chat_turn_without_rag(chat_client, chat_model, messages_trunc)

    if answer is None:
        return

    # Append user input to conversation history
    append_to_history(item_id, user_id, conv_id, messages_trunc[-1])
    # Append model response to conversation history
    append_to_history(item_id, user_id, conv_id, {"role": "system", "content": answer})

    return answer


if __name__ == "__main__":
    print(run_rag("000", "user-000", "conv-000", "Give me a one-liner about London"))
    #print(run_rag("000", "user-000", "conv-000", "Please summarize our conversation"))
    #print(run_rag("000", "user-000", "conv-000", "What was the first message I sent you?"))
    # NOTE: Expect this message to fail bc no info in AI Search about Oslo
    # => the retrieval returns no results
    #print(run_rag("000", "user-000", "conv-000", "Tell me about Oslo!"))
