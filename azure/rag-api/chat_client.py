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


def get_rag_params(search_url, search_key, index_name, embedding_model):
    """Return the RAG parameters for Azure AI Search."""
    return {
        "data_sources": [
            {
                "type": "azure_search",
                "parameters": {
                    "endpoint": search_url,
                    "index_name": index_name,
                    "authentication": {
                        "type": "api_key",
                        "key": search_key
                    },
                    "query_type": "vector",
                    "embedding_dependency": {
                        "type": "deployment_name",
                        "deployment_name": embedding_model
                    }
                }
            }
        ]
    }


def request_chat_response(chat_client, chat_model, messages, rag_params):
    """Call chat model"""
    return chat_client.chat.completions.create(
        model=chat_model,
        messages=messages,
        #extra_body=rag_params
    )
