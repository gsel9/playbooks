"""
Conversation history

Schema
------
{
    "id": "conv-000",
    "userId": "user-000",
    "messages": [
        {
            "role": "assistant",
            "message": "How can I help you?",
            "timestamp": "2026-02-26T15:26:02.002363"
        },
        {
            "role": "assistant",
            "message": "This is another message",
            "timestamp": "2026-02-26T15:28:47.421995"
        }
    ],
    "lastUpdated": "2026-02-26T15:28:48.216720",
    "_rid": "bFRqAKkR3VECAAAAAAAAAA==",
    "_self": "dbs/bFRqAA==/colls/bFRqAKkR3VE=/docs/bFRqAKkR3VECAAAAAAAAAA==/",
    "_etag": "\"3e006401-0000-4700-0000-69a066b00000\"",
    "_attachments": "attachments/",
    "_ts": 1772119728
}
"""
from typing import List, Tuple 
import logging

from azure.cosmos import CosmosClient
import config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
log = logging.getLogger("main")


def create_history_thread(user_id, conv_id):

    config.load_config()

    cosmos_endpoint = config.require_env(config.COSMOS_ENDPOINT)
    cosmos_key = config.require_env(config.COSMOS_KEY)

    client = CosmosClient(cosmos_endpoint, cosmos_key)
    database = client.get_database_client("chatdb")
    container = database.get_container_client("conversations")

    from datetime import datetime

    new_conversation = {
        "id": conv_id,
        "userId": user_id,
        "messages": [],
        "lastUpdated": datetime.utcnow().isoformat()
    }

    response = container.create_item(body=new_conversation)

    print("Inserted item:", response["id"])


def update_history(user_id, conv_id, message):

    config.load_config()

    cosmos_endpoint = config.require_env(config.COSMOS_ENDPOINT)
    cosmos_key = config.require_env(config.COSMOS_KEY)

    client = CosmosClient(cosmos_endpoint, cosmos_key)
    database = client.get_database_client("chatdb")
    container = database.get_container_client("conversations")

    from datetime import datetime
    container.patch_item(
        item=conv_id,
        partition_key=user_id,  # must match partition key
        patch_operations=[
            {
                "op": "add",
                "path": "/messages/-",   # "-" means append to array
                "value": message
            },
            {
                "op": "set",
                "path": "/lastUpdated",
                "value": datetime.utcnow().isoformat()
            }
        ]
    )

    print("Message appended successfully")


def get_prior_messages(user_id: str, conv_id: str) -> List[dict]:

    config.load_config()

    cosmos_endpoint = config.require_env(config.COSMOS_ENDPOINT)
    cosmos_key = config.require_env(config.COSMOS_KEY)

    client = CosmosClient(cosmos_endpoint, cosmos_key)

    database = client.get_database_client("chatdb")
    container = database.get_container_client("conversations")

    query = """
    SELECT * FROM c
    WHERE c.id = @id AND c.userId = @userId
    ORDER BY c.messages.timestamp ASC
    """

    parameters = [
        {"name": "@id", "value": conv_id},
        {"name": "@userId", "value": user_id}
    ]

    messages = container.query_items(
        query=query,
        parameters=parameters,
        partition_key=user_id
    )
    return list(messages)


if __name__ == "__main__":
    # TODO: Should create items based on user ID and have different conversation threads 
    # per user rahter than indexing on the conversation ID
    #create_history_thread("user-000", "conv-000")
    from datetime import datetime
    #update_history(
    #    "user-000", 
    #    "conv-000", 
    #    message={
    #        "role": "assistant",
    #        "message": "How can I help you?",
    #        "timestamp": datetime.utcnow().isoformat()
    #    }
    #)
    #update_history(
    #    "user-000", 
    #    "conv-000", 
    #    message={
    #        "role": "assistant",
    #        "message": "This is another message",
    #        "timestamp": datetime.utcnow().isoformat()
    #    }
    #)
    print(get_prior_messages("user-000", "conv-000")[0]["messages"])
