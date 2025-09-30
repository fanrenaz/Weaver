"""Tool building blocks (Phase 1.2 prototype).

These functions are intentionally simple; they log their usage and return a
string that becomes the agent's observation. In future phases these will
integrate with persistence, notification systems, etc.
"""

from __future__ import annotations

import logging
from langchain_core.tools import tool

logger = logging.getLogger(__name__)


@tool
def reply_privately(recipient: str, content: str) -> str:  # type: ignore[misc]
    """Send a confidential private reply to a single recipient.

    Parameters:
        recipient: The target user identifier or display name.
        content: The natural language message body to send.

    Returns:
        A short status string confirming the private reply was (simulated) sent.
    """
    logger.info("Executing reply_privately to %s", recipient)
    logger.debug("Private content: %s", content)
    return f"[private -> {recipient}] {content}"  # simple echo for prototype


@tool
def post_to_shared(content: str) -> str:  # type: ignore[misc]
    """Post a message to the shared group-visible conversation space.

    Parameters:
        content: The natural language message body to broadcast.

    Returns:
        A status string representing the broadcast result.
    """
    logger.info("Executing post_to_shared (broadcast)")
    logger.debug("Shared content: %s", content)
    return f"[shared] {content}"


TOOLS = [reply_privately, post_to_shared]

__all__ = ["reply_privately", "post_to_shared", "TOOLS"]
