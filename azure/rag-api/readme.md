# NOTE:

Extends rag-cli with 
1. An API endpoint for access the grounded LLM
2. A Azure Cosmos DB to store user conversations

This pipeline forces RAG always. This means that unrelated questions, querying topics not foudn in the search DB, will result in a standard reply, since the retrieval returns no results.

When Azure AI Search cannot find semantically similar documents, RAG returns an empty context, so the model generates the generic message:

“The requested information is not found in the retrieved data…”

This solution supports a multi-turn LLM conversation, but not multi-turn retrieval. Only the latest user message is embedded and used for Azure AI Search. 
To add a multi-step conversational RAG, add a rewrite step/conversation summarization/agent loop.

# Setup

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

# Agentic RAG chat app

## Setup 
Tutorials for configuring vector search:
- [Link](https://learn.microsoft.com/en-us/azure/search/search-get-started-portal-import-vectors?tabs=sample-data-storage%2Cmodel-aoai%2Cconnect-data-storage%2Cvectorize-text-aoai%2Cvectorize-images) for portal configuration 
- [Link](https://learn.microsoft.com/en-us/azure/search/search-get-started-vector?pivots=python) for programmatic configuration 

## Managing conversation History

Create a Azure Cosmos DB resource. 
Supports:
- Schema-less (great for flexible chat messages)
- Global distribution
- Low latency
- Built-in scaling
- Native JSON storage

Go to: https://cosmos.azure.com/

After deployment:
- Open your Cosmos DB account
- Go to Data Explorer
- Click New Database
  - Database ID: chatdb
- Click New Container
  - Container ID: conversations
  - Partition key: /userId (recommended)

Test querying the conversation database by adding an item
```
{
  "id": "conv-123",
  "userId": "user-456",
  "messages": [
    { "role": "user", "message": "Hi" },
    { "role": "assistant", "message": "Hello!" }
  ],
  "lastUpdated": "2026-02-26T10:00:00Z"
}
```

## Deploy FastAPI to Azure Container Apps

Azure Container Apps (ACA) is ideal because it:
- Runs any container (including FastAPI + Uvicorn)
- Auto-scales
- Gives you a public HTTPS URL
- Requires no VM management
- Integrates cleanly with CI/CD

### Build and push your image to Azure Container Registry 
```
az acr create -n <ACR_NAME> -g <RESOURCE_GROUP> --sku Basic
az acr login -n <ACR_NAME>

docker build -t <ACR_NAME>.azurecr.io/fastapi:latest .
docker push <ACR_NAME>.azurecr.io/fastapi:latest
```

### Deploy to Azure Container Apps
```
az containerapp env create \
  --name fastapi-env \
  --resource-group <RESOURCE_GROUP> \
  --location westeurope

az containerapp create \
  --name fastapi-api \
  --resource-group <RESOURCE_GROUP> \
  --environment fastapi-env \
  --image <ACR_NAME>.azurecr.io/fastapi:latest \
  --ingress external \
  --target-port 8000
```

### After deployment
You get a public URL
```
az containerapp show -n fastapi-api -g <RESOURCE_GROUP> --query properties.configuration.ingress.fqdn
```