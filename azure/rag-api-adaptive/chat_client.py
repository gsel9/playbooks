"""
TODO
"""

from openai import AzureOpenAI


def chat_instructions():
    """Initialize prompt with system message."""
    return [{
        "role": "system",
        # System message for travel-related chat solution
        "content": (
            "You are a travel assitant that provides information"
            " on travel services available from Margie's travel."
        )
    }]


def create_chat_client(endpoint, api_key):
    """Create Azure OpenAI chat client."""
    return AzureOpenAI(
        api_version="2024-12-01-preview",
        azure_endpoint=endpoint,
        api_key=api_key
    )


def request_chat_response(chat_client, chat_model, messages):
    """Call chat model"""
    return chat_client.chat.completions.create(
        model=chat_model, messages=messages
    )
