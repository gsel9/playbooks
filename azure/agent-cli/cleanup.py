"""
Cleanup utilities for conversation and agent teardown.
"""

import logging
from typing import Any, Optional
from azure.ai.projects import AIProjectClient

log = logging.getLogger(__name__)


def cleanup(
    openai_client: Any,
    conversation_id: Optional[str],
    project_client: Optional[AIProjectClient],
    agent: Optional[Any],
) -> None:
    """Safely delete conversation and agent."""
    if conversation_id:
        try:
            openai_client.conversations.delete(conversation_id=conversation_id)
            log.info("Conversation deleted.")
        except Exception as exc:
            log.warning("Failed to delete conversation: %s", exc)

    if project_client and agent:
        try:
            project_client.agents.delete_version(
                agent_name=agent.name,
                agent_version=agent.version,
            )
            log.info("Agent deleted.")
        except Exception as exc:
            log.warning("Failed to delete agent version: %s", exc)