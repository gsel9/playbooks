"""
Agent, conversation, and response creation helpers.
"""

import logging
from typing import Any

from azure.ai.projects import AIProjectClient
from azure.ai.projects.models import PromptAgentDefinition

log = logging.getLogger(__name__)


def agent_instructions() -> str:
    """Agent behavioral instructions."""
    return (
        "You are a technical support agent with capabilities:\n"
        "1. Analyzing uploaded file data.\n"
        "2. Helping users with technical issues.\n"
        "When users submit issues, extract email, address, and description.\n"
        "Use Python for any numeric/statistical computation.\n"
        "Use the support ticket tool when relevant.\n"
        "If a file is saved, tell the user the file name.\n"
    )


def create_agent(
    project_client: AIProjectClient,
    model_deployment: str,
    tools: list[Any],
) -> Any:
    """Create and return an agent version configured with tools."""
    agent = project_client.agents.create_version(
        agent_name="support-agent",
        definition=PromptAgentDefinition(
            model=model_deployment,
            instructions=agent_instructions(),
            tools=tools,
        ),
    )
    log.info("Created agent %s v%s", agent.name, agent.version)
    return agent


def create_conversation(openai_client: Any) -> Any:
    """Create a new conversation thread."""
    conversation = openai_client.conversations.create()
    log.info("Conversation created: %s", conversation.id)
    return conversation


def append_user_message(
    openai_client: Any, conversation_id: str, text: str
) -> None:
    """Append a user message to an existing conversation."""
    openai_client.conversations.items.create(
        conversation_id=conversation_id,
        items=[{"type": "message", "role": "user", "content": text}],
    )


def request_agent_response(
    openai_client: Any, conversation_id: str, agent: Any
) -> Any:
    """Request a response from the agent."""
    return openai_client.responses.create(
        conversation=conversation_id,
        input="",
        extra_body={"agent": {"name": agent.name, "type": "agent_reference"}},
    )
