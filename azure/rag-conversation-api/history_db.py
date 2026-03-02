"""
Conversation history

Schema
------
{
    "id": "conv-000",
    "userId": "user-000",
    "messages": []
}
"""
from typing import List, Dict, Any, Optional
import logging
from datetime import datetime

from azure.cosmos import CosmosClient
import config

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
log = logging.getLogger("main")

config.load_config()
cosmos_endpoint = config.require_env(config.COSMOS_ENDPOINT)
cosmos_key = config.require_env(config.COSMOS_KEY)

client = CosmosClient(cosmos_endpoint, cosmos_key)
container_name = config.require_env(config.CONTAINER)
db_name = config.require_env(config.DATABASE)


def is_new_user(user_id: str) -> bool:
    """
    Checks if the user ID exists in the database.
    """
    query = """
        SELECT VALUE c.userID
        FROM c
        WHERE c.userID = @userID
    """
    params = [
        {"name": "@userID", "value": user_id}
    ]
    database = client.get_database_client(container_name)
    container = database.get_container_client(db_name)
    
    match_user_id = list(container.query_items(
        query=query,
        parameters=params,
        enable_cross_partition_query=True
    ))

    if bool(match_user_id):
        return False
    return True


def schema(
    item_id: str = "000",
    user_id: str = "user-000",
    conv_id: str = "conv-000",
    messages: Optional[List[Dict[str, Any]]] = None
) -> Dict[str, Any]:
    """
    Schema of the conversation history.
    """
    if messages is None:
        messages = []
    return {
        "id": item_id,
        "convID": conv_id,
        "userID": user_id,
        "messages": messages
    }


def create_item(item: Dict, overwrite: bool = False) -> None:
    """
    Initialize
    """
    database = client.get_database_client(container_name)
    container = database.get_container_client(db_name)

    if overwrite:
        # TODO: Assumes item already exists
        response = container.upsert_item(item)
    else:
        response = container.create_item(body=item)

    print("Inserted item:", response["id"])


def get_prior_messages(user_id: str, conv_id: str) -> List[dict]:
    """
    Retrieve full conversation history.
    """
    database = client.get_database_client(container_name)
    container = database.get_container_client(db_name)

    query = """
        SELECT *
        FROM c
        WHERE c.userID = @userID
        AND c.convID = @convID
    """

    parameters = [
        {"name": "@userID", "value": user_id},
        {"name": "@convID", "value": conv_id}
    ]

    response = container.query_items(
        query=query,
        parameters=parameters,
        enable_cross_partition_query=True
    )
    return list(response)


def append_to_history(
    item_id: str,
    user_id: str,
    conv_id: str,
    message: dict 
) -> None:
    """

    """
    database = client.get_database_client(container_name)
    container = database.get_container_client(db_name)

    container.patch_item(
        item=item_id,
        partition_key=[user_id],
        patch_operations=[
            {
                "op": "add",
                "path": "/messages/-",   # "-" means append to array
                "value": message
            }
        ]
    )

    print("Message appended successfully")


if __name__ == "__main__":
    print(is_new_user("user-000"))
    messages = [
        {"role": "system", "content": "You are a helpful AI assistant."},
        {"role": "user", "content": "Hello! Who are you?"},
        {"role": "assistant", "content": "I'm an AI assistant here to help you."}
    ]
    s = schema(messages=messages)
    create_item(s, overwrite=True)
    print(is_new_user("user-000"))
    print(get_prior_messages("user-000", "conv-000")[0]["messages"])
