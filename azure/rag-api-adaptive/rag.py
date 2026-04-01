"""
"""
from typing import List, Dict, Any, Tuple, Optional

from azure.core.credentials import AzureKeyCredential
from azure.search.documents import SearchClient
from azure.search.documents.models import VectorizedQuery

from openai import AzureOpenAI


def create_search_client(search_endpoint, index_name, search_key):
    """
    """
    search_client = SearchClient(
        endpoint=search_endpoint,
        index_name=index_name,
        credential=AzureKeyCredential(search_key)
    )
    return search_client


def create_embedding_client(openai_endpoint: str, openai_key: str) -> AzureOpenAI:
    """
    Create an Azure OpenAI client for embeddings.
    """
    return AzureOpenAI(
        api_key=openai_key,
        api_version="2024-10-21",  # use the API version you deployed
        azure_endpoint=openai_endpoint
    )


# TODO: see https://github.com/Azure/azure-sdk-for-python/blob/main/sdk/search/azure-search-documents/README.md
def run_vector_search(
    search_client: Any,
    embedding_client: Any,
    embedding_model: str,
    query: str
) -> str:
    """
    Executes a vector search against Azure AI Search.

    Returns the top k results.
    """
    # Embedding for the user query
    embedding = embedding_client.embeddings.create(
        model=embedding_model,
        input=query
    ).data[0].embedding

    # Create vector query
    vector_query = VectorizedQuery(
        vector=embedding,
        k_nearest_neighbors=5,     # Number of similar documents to return
        fields="text_vector"  # Name of the vector field in your index
    )
    
    # Execute vector search. You can also add "search_text=query" for HYBRID search (kwarg + vector)
    results_iter = search_client.search(
        search_text=None,  # None for pure vector search
        vector_queries=[vector_query],
        top=5
    )
    
    # Collect results and apply threshold
    results: List[Dict[str, Any]] = []
    for doc in results_iter:
        if doc.get("@search.score", 0.0) < 0.6:
            continue

        results.append(doc["chunk"])
        
    return "\n".join(results)
    

def create_context_message(messages: List[Dict], context: str) -> List:
    """
    Add retrieved context to (local) message history.
    """
    system_context_msg = {
        "role": "system",
        "content": (
            "Here is relevant information from your knowledge base:"
            f"\n\n{context}\n\n"
            "Use it to answer the user query."
        )
    }
    messages.append(system_context_msg)

    return messages


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
