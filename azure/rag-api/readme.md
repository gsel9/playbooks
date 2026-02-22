# Grounding a LLM 

Though language models are trained on a vast amount of data, they may not have access to the knowledge you want to make available to your users. To ensure that an agent is grounded on specific data to provide accurate and domain-specific responses, you can use Retrieval Augmented Generation (RAG).

## RAG
In general terms, the RAG pattern incorporates the following steps:
1. Retrieve grounding data based on the initial user-entered prompt
2. Augment the prompt with grounding data
3. Use a language model to generate a grounded response 

## Azure Data Storage
* Azure Blob Storage
    - Use if unstructured data (PDFs, text, bianries)
    - Cheaper, flexible, and no analytics needed 
* Azure Data Lake Storage (ADLS) Gen2
    - Built on Blob Storage
    - Adds capabilities for big-data analytics and hierarchical namespaces
    - Large-scale analytics workloads (Spark, Datbricks, Hadoop, Synapse)
    - Hierarchical org of directories + files 
    - Enterprise-scale data lakes, ML pipelines, batch ETL/ELT workloads
* Microsoft OneLake 
    - Part of Fabric, acting as a tenant-wide, governed, single logical data lake built on top og Azure Data Lake Storage Gen2
    - Centralizing all enterprise analytics data in one governed hub
    - Creating Lakehouses, Warehouses, Real-Time Analytics and sharing the sae underlying storage
    - Storing structured/unstructured data, with all tabular data saved as Delta Parquet by default 

## Making Data Searchable
Integrate with *Azure AI Search* to retrieve relevant context for your chat flow:
 - Azure AI Search: Is a retriever that you can include when building a language model application with prompt flow. 
 - Azure AI Search: Allows you to bring your own data, index your data, and query the index to retrieve any information you need.

## Creating A Vector Search Index Via Foundry

1. https://ai.azure.com/managementCenter/allResources
2. Create new AI Hub resource. This will automatically create 
    - Storage account 
    - Key Vault 
3. In Storage Account (portal.azure), add data to Blob container 
5. In azure Portal, create an AI Search resource 
4. In Foundry, deploy an embedding model (eg, text-embedding-ada-002)
6. In Foundry, create a new index (use existing Blob storage, AI Search and embedding model)
    - The index is stored in AI Search/Indexes and can be tested there
    
## Creating A RAG CLI Solution

1. In Foundry, deploy a chat model (eg, gpt-4o)
2. Create virtual env
```
python -m venv labenv
./labenv/bin/Activate.ps1
pip install -r requirements.txt openai
```
3. Manage configs in `./env`

## Converting the CLI to a Dockerized API

1. Install Docker
2. Start Docker Daemon and test locally
```
docker build -t rag-api .
docker run -p 8000:8000 rag-api
```
3. In the Foundry portal, create a Container Registry resource


4. Log in to your registry
```
az login
az acr login --name myragapp
```
3. Pull and tag your image


### Parking Lot


### Creating A Search Index Via AZ Portal

Two options:
- Via Storage account (requires AI Search resource)
- Via AZ Search (connected to data from Storage Account)

#### Starting from Storage Account
- See Data Management tab (left) -> AZ AI Search
- Select AI Search service 
- Connect to data from storage container
- Add cognitive skills (requires AZ AI Services deployed in same region)
- This will create an index and skills.

#### Starting from AZ AI Search
- Create an index, eg
    - field: id; type: string; retrievable
    - field: content; type: string; retrievable; searchable
    - field: contentVector; type: SingleCollection; retrievable; searchable
        - Create a search profile
        - Create a (requires creating an Azure OpenAI resource and deploying an embedding model)
    - field: url; type: string; retrievable
    - field: filepath; type: string; retrievable
    - field: title; type: string; retrievable; searchable
    - field: meta_json_string; type: string; retrievable
- Create a skillset
    - 
- Create an indexer 


A search index describes how your content is organized to make it searchable.
An index defines *how* the data will be stored and searched, including
* id (key)
* content (extracted text from, eg, PDFs)
* ContentVector (filename, URL, page numer last modified, etc.)

If using integrated vectorization, you must also define
* vectorSearch section 
* A vector field with same dimension as embedding model




## Implement RAG in a prompt flow
After uploading data to Microsoft Foundry and creating an index on your data using the integration with Azure AI Search, you can implement the RAG pattern with Prompt Flow to build a generative AI application.

- Prompt Flow is a development framework for defining flows that orchestrate interactions with an LLM.

A flow begins with one or more inputs, usually a question or prompt entered by a user, and in the case of iterative conversations the chat history to this point. The flow is then defined as a series of connected tools, each of which performs a specific operation on the inputs and other environmental variables. 

Combine RAG and a language model in your application:
1. Combine user input with chat history 
2. Get top *n* context results from the Index Lookup tool, running a query against the search index to find relevant information from your data source
3. The output from the Index Lookup tool, containing the retrieved context, must be parsed into a more suitable format to be used in the prompt you send to the LLM
4. When constructing the prompt you want to sent to the LLM, you can use variants to represent different prompt contents. 
5. Finally, you use an LLM node to send the prompt to a language model to generate a response using the relevant context retrieved from your data source. The response from this node is also the output of the entire flow. 

This flow can be deployed and integrated with an application to offer users an agentic experience.

## Adapting to Enterprise Version

The core building blocks of AI Search are:
- Data source: Blob, SQL DB; Cosmos DB, Sharepoint via connectors
- Index: Searchable knowledge base used at query time
    - Fields (content/chunked text etc.)
    - Key field (unique ID)
    - Searchable fields 
    - Filterable/sortable fields
    - Vector fields (for embeddings)
    - Semantic configuration (for semantic ranking)
- Skillset: A sequence of AI enrichment operations applied during document indexing
    - Defines "cognitive/AI skills" applied during indexing
    - Examples are extract text (OCR), chunk content, entity recognition, generate embeddings
- Indexer: Orchestrates pulling data from source, applies skillset, writes results into index
    - Can run on schedule
    - Flow: Data Source → Indexer → Skillset → Index
- Vector/hybrid query: 
    - Vector search algorithm (HNSW), similarity metric (cosine), vector profiles
    - Hybrid search combines vector search, keyword search and semantic ranking


Note: Creating a Foundry resource in portal.azure is *not* a prerequisite for creating a Foundry AI Hub resource. A Foundry resource acts as a shared model provider for all projects under the hub, including Azure OpenAI, Speech services, Content Safety, shared endpoints for AI models within the hub.

Analogy:
- Azure AI Hub: The office building (centralized security, identity management, networking)
- Azure AI Project: A department (workspace for building, e.g., apps)
- Connections: Utility lines, linking to external resources like Azure OpenAI, AI Search, Blob Storage

When creating a Foundry resource, you build the office building. A resource group shuold be dedicated to AI assets, itolating them from production web apps.

In an enterprise setting, you might want to link an AI Hub to existing services such ass 
- Storage Account for raw data and artifacts
- Key vault for secrets and API keys
- Application Insights for monitoring 
- Container Registry, required for using Prompt Flow with custom environments



Common components in a RAG app are 
- Azure AI Foundry Hub: Central governance unit
- Storage Account: Used for datasets, promptflow artifacts, project assets
- Azure AI Search: Enterprise RAG search index engine
- Azure OpenAI (optional): Base model resource connected to hub
- Azure Key Vault: Credential/secret store for hub and projects 
- App Insights/Log Analytics: Central logging + monitoring
- Container Registry: For custom skills, model deployments


Subscription: contoso-prod-ai-subscription
|
└── Resource Group: rg-contoso-ai-hub-eus2
    |
    ├── Azure AI Hub: contoso-ai-hub
    |
    ├── Storage Account: stcontosoaihubeus2
    |     ├── container: enterprise-docs
    |     └── container: project-assets
    |
    ├── Azure AI Search: search-contoso-ai
    |
    ├── Azure OpenAI (Foundry Resource): aoai-contoso
    |
    ├── Key Vault: kv-contoso-ai
    |
    ├── Application Insights: appinsights-contoso-ai
    |
    ├── Container Registry (optional): acr-contoso
    |
    └── Projects (created inside Hub via portal)
          ├── Project HR-RAG
          ├── Project IT-RAG
          └── Project Agents-CS


Deployed two LLMs:
- An embedding model
- A chat completion model 

- Upload data to assets
- Configure vector index
- Create Azure AI Search Service (data will be ingested into an index in Azure AI Search)
- Create vector index (connected to data assets, search service)

**Vector Index Steps**
- Crack, chunk, and embed the tokens from uploaded data
    - Cracking: Extracts raw text & metadata from PDFs/Word/etc. 
    - Chunking: Splits large documents into overlapping chunks to support embeddings. 
    - Embedding: Use an embedding model to convert each chunk into high‑dimensional semantic vectors
- Create an Azure Search index
    - Stores text, metadata and vectors in an Azure Search index with a vector field.
- Register the index asset


File formats supported by index for cracking and chunking:
```
'.txt', '.md', '.html', '.htm', '.py', '.pdf', '.ppt', '.pptx', '.doc', '.docx', '.xls', '.xlsx', '.csv', '.json'
```