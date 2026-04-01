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
    messages: List[dict]
) -> str:
    """
    Single chat turn: call model once and return the answer
    """
    try:
        response = request_chat_response(chat_client, chat_model, messages)
    except Exception as exc:
        log.error("Error requesting response: %s", exc)
        # Remove the last user message to avoid poisoning the chat history
        messages.pop()
        return

    if finish_reason(response) != "stop":
        log.error("Agent error: %s", getattr(response, "error", "<no details>"))
        return 

    return output_text(response)
