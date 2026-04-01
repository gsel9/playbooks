"""
This step creates a knowledge base, which acts as a wrapper 
for your knowledge source and LLM deployment.

EXTRACTIVE_DATA is the default modality and returns 
content from your knowledge sources without generative 
alteration. However, this quickstart uses the 
ANSWER_SYNTHESIS modality for LLM-generated answers 
that cite the retrieved content.

NOTE: https://github.com/Azure-Samples/azure-search-python-samples/blob/main/Quickstart-Agentic-Retrieval/quickstart-agentic-retrieval.ipynb

To target earth-knowledge-source and your gpt-5-mini deployment at query time, you need a knowledge base. The following code defines a knowledge base named earth-knowledge-base.

output_mode is set to ANSWER_SYNTHESIS, enabling natural-language answers that cite the retrieved documents and follow the provided answer_instructions.
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