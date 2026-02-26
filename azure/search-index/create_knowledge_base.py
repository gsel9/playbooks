"""
This step creates a knowledge base, which acts as a wrapper 
for your knowledge source and LLM deployment.

EXTRACTIVE_DATA is the default modality and returns 
content from your knowledge sources without generative 
alteration. However, this quickstart uses the 
ANSWER_SYNTHESIS modality for LLM-generated answers 
that cite the retrieved content.

NOTE: https://github.com/Azure-Samples/azure-search-python-samples/blob/main/Quickstart-Agentic-Retrieval/quickstart-agentic-retrieval.ipynb
"""

from azure.search.documents.indexes.models import KnowledgeBase, KnowledgeBaseAzureOpenAIModel, KnowledgeSourceReference, AzureOpenAIVectorizerParameters, KnowledgeRetrievalOutputMode, KnowledgeRetrievalLowReasoningEffort
from azure.search.documents.indexes import SearchIndexClient

aoai_params = AzureOpenAIVectorizerParameters(
    resource_url=aoai_endpoint,
    deployment_name=aoai_gpt_deployment,
    model_name=aoai_gpt_model,
)

knowledge_base = KnowledgeBase(
    name=knowledge_base_name,
    models=[KnowledgeBaseAzureOpenAIModel(azure_open_ai_parameters=aoai_params)],
    knowledge_sources=[
        KnowledgeSourceReference(
            name=knowledge_source_name
        )
    ],
    output_mode=KnowledgeRetrievalOutputMode.ANSWER_SYNTHESIS,
    answer_instructions="Provide a 2 sentence concise and informative answer based on the retrieved documents."
)

index_client = SearchIndexClient(endpoint=search_endpoint, credential=credential)
index_client.create_or_update_knowledge_base(knowledge_base)
print(f"Knowledge base '{knowledge_base_name}' created or updated successfully.")