"""
"""
from typing import Any 
from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery
from openai import OpenAI


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


def create_rag_client(search_endpoint, search_index_name, search_key):
    """
    """
    search_client = SearchClient(
        endpoint=search_endpoint,
        index_name=search_index_name,
        credential=AzureKeyCredential(search_key)
    )
    return search_client


def request_embedding_response(open_ai_endpoint, open_ai_key, user_query, embedding_model):
    """
    """
    open_ai_endpoint = "https://aiservicesswe01.cognitiveservices.azure.com/openai/v1/"

    embed_client = OpenAI(
        api_key=open_ai_key,
        base_url=open_ai_endpoint  # Must be your Azure AI Foundry endpoint
    )

    embedding = embed_client.embeddings.create(
        model=embedding_model,
        input=user_query
    )
    return embedding.data[0].embedding


# TODO: see https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/README.md
def rag_search(search_client: Any, embedding: Any) -> str:
    """
    """
    # Create vector query
    vector_query = VectorizedQuery(
        vector=embedding,
        k_nearest_neighbors=5,  # Number of similar documents to return
        fields="text_vector"  # Name of the vector field in your index
    )
    
    # Perform search
    results = search_client.search(
        search_text=None,  # None for pure vector search
        vector_queries=[vector_query],
        select=["chunk_id", "chunk"]  # <---- TODO WHAT ARE THESE FIELDS?
    )
    chunks = [doc["chunk"] for doc in results]
    return "\n\n".join(chunks)


def build_messages(conversation_history, user_query, rag_context):
    messages = []

    messages.append({
        "role": "system",
        "content": "You are a helpful assistant using provided context when relevant."
    })

    # Add conversation history from Cosmos DB
    messages.extend(conversation_history)

    # Add retrieved RAG context
    if rag_context:
        messages.append({
            "role": "system",
            "content": f"Relevant retrieved context:\n{rag_context}"
        })

    # Add the user's new question
    messages.append({
        "role": "user",
        "content": user_query
    })

    return messages
