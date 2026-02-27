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