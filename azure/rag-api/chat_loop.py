"""
Interactive CLI-driven chat loop.
"""

import logging
from typing import Any, List
from chat_client import request_chat_response

log = logging.getLogger(__name__)


def output_text(response: Any) -> str:
    """Extract plain output text from a response."""
    return response.choices[0].message.content


def finish_reason(response: Any) -> str:
    """Extract finish reason from a response."""
    return response.choices[0].finish_reason


def chat_loop(
    chat_client: Any, chat_model: str, messages: List, rag_params: Any
) -> None:
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
        
        # Add user message
        messages.append({"role": "user", "content": user_input})

        try:
            response = request_chat_response(chat_client, chat_model, messages, rag_params)
        except Exception as exc:
            log.error("Error requesting response: %s", exc)
            # Remove the last user message to avoid poisoning the chat history
            messages.pop()
            continue

        if finish_reason(response) != "stop":
            log.error("Agent error: %s", getattr(response, "error", "<no details>"))
            continue

        response_text = output_text(response)
        
        # Append the response to an existing conversation
        messages.append({"role": "assistant", "content": response_text})
        print(f"Agent: {response_text}")
