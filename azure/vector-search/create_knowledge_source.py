"""
This step creates a knowledge source that targets the 
index you previously created. In the next step, you 
create a knowledge base that uses the knowledge source 
to orchestrate agentic retrieval.

NOTE: https://github.com/Azure-Samples/azure-search-python-samples/blob/main/Quickstart-Agentic-Retrieval/quickstart-agentic-retrieval.ipynb

A knowledge source is a reusable reference to source data. The following code defines a knowledge source named earth-knowledge-source that targets the earth-at-night index.

source_data_fields specifies which index fields are included in citation references. This example includes only human-readable fields to avoid lengthy, uninterpretable embeddings in responses.
"""

from azure.search.documents.indexes.models import SearchIndexKnowledgeSource, SearchIndexKnowledgeSourceParameters, SearchIndexFieldReference
from azure.search.documents.indexes import SearchIndexClient

ks = SearchIndexKnowledgeSource(
    name=knowledge_source_name,
    description="Knowledge source for Earth at night data",
    search_index_parameters=SearchIndexKnowledgeSourceParameters(
        search_index_name=index_name,
        source_data_fields=[SearchIndexFieldReference(name="id"), SearchIndexFieldReference(name="page_number")]
    ),
)

index_client = SearchIndexClient(endpoint=search_endpoint, credential=credential)
index_client.create_or_update_knowledge_source(knowledge_source=ks)
print(f"Knowledge source '{knowledge_source_name}' created or updated successfully.")