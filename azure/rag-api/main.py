"""
Entry point for the rag-llm CLI.
"""
from typing import List, Tuple 
import logging

from history_db import is_new_user, get_prior_messages, update_message_history
from chat_client import create_chat_client, chat_instructions, get_rag_params
from rag import create_rag_client, request_embedding_response, rag_search
from chat_turn import chat_turn
import config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
log = logging.getLogger("main")


def run_rag(
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

    rag_client = create_rag_client(search_endpoint, index_name, search_key)
    embedding = request_embedding_response(open_ai_endpoint, open_ai_key, user_input, embedding_model)
    retrieved_docs = rag_search(rag_client, embedding)
    print(retrieved_docs)
    assert asf 

    #rag_params = get_rag_params(
    #    search_endpoint, search_key, index_name, embedding_model
    #)

    if is_new_user(user_id):
        messages = list(instructions)
    else:
        messages = get_prior_messages(user_id, conv_id)[0]["messages"]

    # Truncate chat history to include only k last messages
    messages = messages[-use_k_last:]
    
    # Append user message
    messages.append({"role": "user", "content": user_input.strip()})

    rag_client = create_rag_client(search_endpoint, index_name, search_key)
    embedding = request_embedding_response(open_ai_endpoint, open_ai_key, user_input, embedding_model)
    print(embedding)
    retrieved_docs = rag_search(rag_client, embedding)
    print(retrieved_docs)

    if retrieved_docs is not None:
        messages.append({
            "role": "assistant",
            "content": f"Retrieved context:\n{retrieved_docs}"
        })

    answer = chat_turn(chat_client, chat_model, messages, rag_params)
    if answer is None:
        return

    # Append model response to conversation history
    update_message_history("000", user_id, conv_id, messages[-1])
    # Append model response to conversation history
    update_message_history("000", user_id, conv_id, {"role": "system", "content": answer})

    return answer 


if __name__ == "__main__":
    """
    No conversation history because because your LLM is only seeing the RAG‑retrieved 
    documents—not the actual conversation messages—when it tries to summarize the 
    conversation.

    So when you say “summarize our conversation,” your pipeline does this:
    1. Create embedding of the question (“summarize our conversation”)
    2. Retrieve documents relevant to that query
    3. RAG returns nothing (because nothing in your vector store looks like a “conversation summary”)
    4. LLM produces the fallback message:
        “The requested information is not found in the retrieved data…”

    This is a retrieval problem, not an LLM problem.

    Current flow: User question → embed → search → retrieved docs → LLM

    """
    #print(run_rag("user-000", "conv-000", "Give me a one-liner about London"))
    print(run_rag("user-000", "conv-000", "Please summarize our conversation"))
