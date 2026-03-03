# Grounding a LLM with RAG

The RAG pattern incorporates the following steps:
1. Retrieve grounding data based on the initial user-entered prompt
2. Augment the prompt with grounding data
3. Use a language model to generate a grounded response 

## Making Data Serachable
A typical workflow to make data searchable is:
1. Create a data source - define connection details and authentication
2. Populate the data source
3. Configure a search mechanism to query the data source 

### Storage solutions
* Azure Blob Storage
    - Use if unstructured data (PDFs, text, binaries)
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

### Azure AI Search
Is a retriever that you can include when building a language model application with prompt flow. Allows you to bring your own data, index your data, and query the index to retrieve any information you need. In Azure AI Search, a data source serves as a connection point for indexers. It provides the necessary connection details to enable on-demand or scheduled data refreshes for a target index, pulling data from supported Azure data sources.

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

To use Azure AI Search, we need to create an index, indexer, data source, and skillset:
* Indexer
  - An indexer automates the process of indexing data from supported Azure data sources, such as Azure Storage, Azure SQL Database, and Azure Cosmos DB, among others.
  - It leverages a predefined data source and index to create an indexing pipeline that extracts, transforms, and serializes the source data before passing it to the search service for ingestion.
  - Additionally, for AI enrichment of images and unstructured text, indexers can incorporate a skillset, which defines the AI processing tasks to be applied during indexing.
* Index
  - A search index represents your searchable content, making it available to the search engine for various operations such as indexing, full-text search, vector search, hybrid search, and filtered queries.
  - The index is defined by a schema, which specifies the structure of the data, including fields, types, and attributes.
  - Once the schema is defined and saved to the Azure AI Search service, data import occurs as a subsequent step to populate the index with content.
  - A search index describes how your content is organized to make it searchable. It defines *how* the data will be stored and searched, including
    * id (key)
    * content (extracted text from, eg, PDFs)
    * ContentVector (filename, URL, page numer last modified, etc.)
  - If using integrated vectorization, you must also define
    * vectorSearch section 
    * A vector field with same dimension as embedding model
    * Vector Index Steps
* Skillset
  - A skillset in Azure AI Search is a reusable object that is linked to an indexer.
  - It consists of one or more skills, which apply built-in AI capabilities (such as OCR, natural language processing, or entity recognition) or invoke external custom processing to enrich documents retrieved from an external data source.
  - Skillsets allow you to enhance raw data by extracting meaningful information, transforming it into searchable content, and enabling advanced search and analysis capabilities.
 
Process:
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

There are several ways that information can be queried in an index:
- Keyword search: Identifies relevant documents or passages based on specific keywords or terms provided as input.
- Semantic search: Retrieves documents or passages by understanding the meaning of the query and matching it with semantically related content rather than relying solely on exact keyword matches.
- Vector search: Uses mathematical representations of text (vectors) to find similar documents or passages based on their semantic meaning or context.
- Hybrid search: Combines different search techniques.

## Setup 
1. Create a resource group (e.g., rg-seel, Sweden central)
2. Create a storage account (storageseel01, Sweden central)
    - Preferred storage type: Blob storage
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
8. Update .env in code repo
9. Run main.py using python

Tutorials for configuring vector search:
- [Link](https://learn.microsoft.com/en-us/azure/search/search-get-started-portal-import-vectors?tabs=sample-data-storage%2Cmodel-aoai%2Cconnect-data-storage%2Cvectorize-text-aoai%2Cvectorize-images) for portal configuration 
- [Link](https://learn.microsoft.com/en-us/azure/search/search-get-started-vector?pivots=python) for programmatic configuration 
