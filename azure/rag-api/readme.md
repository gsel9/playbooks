# Grounding a LLM with RAG via an API

Extends the `rag-cli` with 
1. An API endpoint for access the grounded LLM
2. A Azure Cosmos DB to store user conversations

This pipeline forces RAG always. This means that unrelated questions, querying topics not foudn in the search DB, will result in a standard reply, since the retrieval returns no results.
  - When Azure AI Search cannot find semantically similar documents, RAG returns an empty context, so the model generates the generic message: “The requested information is not found in the retrieved data…”

This solution supports a multi-turn LLM conversation, but not multi-turn retrieval. Only the latest user message is embedded and used for Azure AI Search. 

## Setup 
1. Create a resource group (e.g., rg-seel, Sweden central)
2. Create a storage account (storageseel01, Sweden central)
  - Preferred storage type: Blobl storage
  - Redundancy: LRS
  - Allow enabling anonymous access on containers 
3. Create AZ AI Search
  - Pricing tier: Basic
4. Create a Foundry resrouce 
5. In storage account/data storage/containers
  - create a data container
  - upload data (eg, pdf files) to this container
5. In Foundry, model catalog
  - deploy an embedding model (eg, text-embedding-3-small, max 50 token/minute)
  - deploy a chat model (eg, gpt-4o)
6. In AZ AI Search, click import data (new)
  - Select blob storage -> RAG
  - Vectorize your text: kind = MS Foudnry
  - Run indexer to create index
7. Test index in AI Search/Search management/Indexes 
8. Create a AZ Cosmos DB 
  - Select Cosmos DB for NoSQL
  - Database: "history", container: "chat"
  - Add container (PK: /userID)
9. Update .env in code repo
10. Run main.py using python

Tutorials for configuring vector search:
- [Link](https://learn.microsoft.com/en-us/azure/search/search-get-started-portal-import-vectors?tabs=sample-data-storage%2Cmodel-aoai%2Cconnect-data-storage%2Cvectorize-text-aoai%2Cvectorize-images) for portal configuration 
- [Link](https://learn.microsoft.com/en-us/azure/search/search-get-started-vector?pivots=python) for programmatic configuration 
