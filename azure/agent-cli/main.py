"""
Entry point for the support-agent application.
"""

import logging
from azure.identity import DefaultAzureCredential
from azure.ai.projects import AIProjectClient

from config import load_config, require_env, PROJECT_ENDPOINT, MODEL_DEPLOYMENT_ENV
from data_utils import read_data, preview_text
from agent_tools import build_code_interpreter_tool, build_function_tool
from agent_client import create_agent, create_conversation
from chat_loop import chat_loop
from cleanup import cleanup

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s | %(levelname)s | %(name)s | %(message)s",
)
log = logging.getLogger("main")


def main() -> None:
    load_config()

    endpoint = require_env(PROJECT_ENDPOINT)
    model_name = require_env(MODEL_DEPLOYMENT_ENV)

    data, file_path = read_data()
    print("\nData Preview:\n")
    print(preview_text(data))
    print("\n")

    agent = None
    conversation = None

    try:
        with DefaultAzureCredential(
            exclude_environment_credential=True,
            exclude_managed_identity_credential=True,
        ) as credential, AIProjectClient(
            endpoint=endpoint, credential=credential
        ) as project_client, project_client.get_openai_client() as openai_client:

            file_obj = openai_client.files.create(
                file=open(file_path, "rb"),
                purpose="assistants",
            )

            code_tool = build_code_interpreter_tool(file_obj.id)
            func_tool = build_function_tool()

            agent = create_agent(project_client, model_name, [code_tool, func_tool])
            conversation = create_conversation(openai_client)

            chat_loop(openai_client, agent, conversation.id)

            cleanup(openai_client, conversation.id, project_client, agent)
            conversation = None
            agent = None

    finally:
        if "openai_client" in locals():
            cleanup(
                locals().get("openai_client"),
                getattr(conversation, "id", None),
                locals().get("project_client"),
                agent,
            )


if __name__ == "__main__":
    main()