"""
TODO
"""

from azure.identity import DefaultAzureCredential
from azure.keyvault.secrets import SecretClient

from config import load_config, require_env, KEY_VAULT_URL


def create_secrets_client():
    """
    Store these items in your Key Vault:
    Required secrets:

    AZURE_OPENAI_ENDPOINT
    AZURE_OPENAI_KEY  (if not using managed identity)
    AI_SEARCH_ENDPOINT
    AI_SEARCH_KEY
    AZURE_STORAGE_CONNECTION_STRING

    Optional:

    Embedding model deployment name
    Chat model deployment name
    Index name

    Azure AI Foundry itself allows using Key Vault to store credentials:
    """
    load_config()

    credential = DefaultAzureCredential()
    vault_url = require_env(KEY_VAULT_URL) #"https://<your-vault-name>.vault.azure.net/"
    secret_client = SecretClient(vault_url=vault_url, credential=credential)

    return secret_client

    #openai_endpoint = secret_client.get_secret("AZURE_OPENAI_ENDPOINT").value
    #openai_key = secret_client.get_secret("AZURE_OPENAI_KEY").value
    #search_endpoint = secret_client.get_secret("AI_SEARCH_ENDPOINT").value
    #search_key = secret_client.get_secret("AI_SEARCH_KEY").value
    #storage_conn_str = secret_client.get_secret("AZURE_STORAGE_CONNECTION_STRING").value
