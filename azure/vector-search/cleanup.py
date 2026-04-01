# Delete the knowledge base
index_client = SearchIndexClient(endpoint=search_endpoint, credential=credential)
index_client.delete_knowledge_base(knowledge_base_name)
print(f"Knowledge base '{knowledge_base_name}' deleted successfully.")

# Delete the knowledge source
index_client = SearchIndexClient(endpoint=search_endpoint, credential=credential)
index_client.delete_knowledge_source(knowledge_source=knowledge_source_name)
print(f"Knowledge source '{knowledge_source_name}' deleted successfully.")

# Delete the search index
index_client = SearchIndexClient(endpoint=search_endpoint, credential=credential)
index_client.delete_index(index_name)
print(f"Index '{index_name}' deleted successfully.")
