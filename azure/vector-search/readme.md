# Vector Search

Vector search in Azure AI Search is a way to find information based on semantic similarity rather than exact keyword matching. Instead of searching text directly, Azure converts content into numeric vectors (embeddings), then compares those vectors to a query vector to find the most similar items.

## Configure Vector Search 
- [Link](https://learn.microsoft.com/en-us/azure/search/search-get-started-portal-import-vectors?) for portal configuration 
- [link](tabs=sample-data-storage%2Cmodel-aoai%2Cconnect-data-storage%2Cvectorize-text-aoai%2Cvectorize-image) for programmatic configuration

## Setup

**Prerequisites**
- In the Azure portal, create a resource group, a storage account, an Azure OpenAI resource, and an AI Search service
- Create a container in the storage account, and upload documents (PDF and PNG)
- 
- Configure cross-resource access:
  - Storage account: Storage Blob Data Reader
  - OpenAI resource: Cognitive Services OpenAI User
