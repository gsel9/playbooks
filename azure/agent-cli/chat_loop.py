"""
Interactive CLI-driven chat loop.
"""

import logging
from typing import Any

from agent_tools import process_function_calls
from agent_client import append_user_message, request_agent_response

log = logging.getLogger(__name__)


def safe_output_text(response: Any) -> str:
    """Extract plain output text from a response."""
    text = getattr(response, "output_text", None)
    return text or "<no text output available>"


def chat_loop(openai_client: Any, agent: Any, conversation_id: str) -> None:
    """Interactive user loop."""
    while True:
        try:
            user_input = input("Enter a prompt ('quit' to exit): ").strip()
        except (KeyboardInterrupt, EOFError):
            print("\nGoodbye!")
            break

        if user_input.lower() == "quit":
            print("Goodbye!")
            break
        if not user_input:
            print("Please enter a prompt.")
            continue

        append_user_message(openai_client, conversation_id, user_input)

        try:
            response = request_agent_response(openai_client, conversation_id, agent)
        except Exception as exc:
            log.error("Error requesting response: %s", exc)
            continue

        if getattr(response, "status", None) == "failed":
            log.error("Agent error: %s", getattr(response, "error", "<no details>"))
            continue

        response = process_function_calls(response, openai_client, agent)

        print(f"Agent: {safe_output_text(response)}")