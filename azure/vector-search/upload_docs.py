"""
This notebook uses data from NASA's Earth at Night e-book. 
The data is retrieved from the azure-search-sample-data 
repository on GitHub and passed to the search client for indexing.

NOTE: https://github.com/Azure-Samples/azure-search-python-samples/blob/main/Quickstart-Agentic-Retrieval/quickstart-agentic-retrieval.ipynb

Currently, the earth-at-night index is empty. The following code populates the index with JSON documents from NASA's Earth at Night e-book. As required by Azure AI Search, each document conforms to the fields and data types defined in the index schema.
"""

import requests
from azure.search.documents import SearchIndexingBufferedSender

url = "https://raw.githubusercontent.com/Azure-Samples/azure-search-sample-data/refs/heads/main/nasa-e-book/earth-at-night-json/documents.json"
documents = requests.get(url).json()

with SearchIndexingBufferedSender(endpoint=search_endpoint, index_name=index_name, credential=credential) as client:
    client.upload_documents(documents=documents)

print(f"Documents uploaded to index '{index_name}' successfully.")