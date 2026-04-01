Workflow:
    No conversation history because because your LLM is only seeing the RAG‑retrieved 
    documents—not the actual conversation messages—when it tries to summarize the 
    conversation.

    So when you say “summarize our conversation,” your pipeline does this:
    1. Create embedding of the question (“summarize our conversation”)
    2. Retrieve documents relevant to that query
    3. RAG returns nothing (because nothing in your vector store looks like a “conversation summary”)
    4. LLM produces the fallback message:
        “The requested information is not found in the retrieved data…”

    This is a retrieval problem, not an LLM problem.

    Current flow: User question → embed → search → retrieved docs → LLM


You’re seeing exactly the behavior Azure OpenAI’s built‑in RAG produces when retrieval returns no results:
“The requested information is not found in the retrieved data…”

When Azure AI Search cannot find semantically similar documents, RAG returns an empty context, so the model generates the generic message:

“The requested information is not found in the retrieved data…”

Right now your pipeline always forces RAG, even when the vector search result is empty.
To make the model decide intelligently whether to use RAG (retrieval) or skip it, you must explicitly add logic before or inside the LLM call.

Fix: Don’t let RAG run automatically — control when retrieval should happen.

Below are the three reliable patterns for solving this, including code patterns you can drop into your existing flow.

# Agentic RAG chat app

## Setup 
Tutorials for configuring vector search:
- [Link](https://learn.microsoft.com/en-us/azure/search/search-get-started-portal-import-vectors?tabs=sample-data-storage%2Cmodel-aoai%2Cconnect-data-storage%2Cvectorize-text-aoai%2Cvectorize-images) for portal configuration 
- [Link](https://learn.microsoft.com/en-us/azure/search/search-get-started-vector?pivots=python) for programmatic configuration 
