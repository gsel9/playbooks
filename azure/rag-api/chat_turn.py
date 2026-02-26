"""
Interactive CLI-driven chat loop.
"""

import logging
from typing import Any, List, Tuple
from chat_client import request_chat_response

log = logging.getLogger(__name__)


def output_text(response: Any) -> str:
    """Extract plain output text from a response."""
    return response.choices[0].message.content


def finish_reason(response: Any) -> str:
    """Extract finish reason from a response."""
    return response.choices[0].finish_reason


def chat_turn(
    chat_client: Any, 
    chat_model: str, 
    messages: List[dict], 
    rag_params: Any, 
    user_input: str
) -> Tuple[str, List[dict]]:    
    """
    Single chat turn: take a user_input + history, call model once, return answer + updated history.
    """
    if not user_input:
        log.error("No user input")
        return "Please provide user input", messages
    
    # Add user message
    messages.append({"role": "user", "content": user_input.strip()})        

    try:
        response = request_chat_response(chat_client, chat_model, messages, rag_params)
    except Exception as exc:
        log.error("Error requesting response: %s", exc)
        # Remove the last user message to avoid poisoning the chat history
        messages.pop()
        return "", messages

    if finish_reason(response) != "stop":
        log.error("Agent error: %s", getattr(response, "error", "<no details>"))

    answer = output_text(response)
    # Append the response to an existing conversation
    messages.append({"role": "assistant", "content": answer})

    return answer, messages
