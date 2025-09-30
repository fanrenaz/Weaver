"""Pydantic models defining Actions that the agent can execute.

Each action corresponds to an available tool. They are intentionally simple in Phase 1.2.
"""

from __future__ import annotations

from typing import Literal
from pydantic import BaseModel, Field


class ReplyPrivateAction(BaseModel):
    """Represents the agent replying privately to a single recipient.

    This action should be chosen when the model wants to send a confidential
    message visible only to the specified recipient.
    """

    type: Literal["reply_private"] = Field(
        description="Discriminator identifying this action type.",
        default="reply_private",
    )
    recipient: str = Field(
        description="Target user id / name to receive the private reply."
    )
    content: str = Field(description="Natural language content of the private reply.")


class PostToSharedAction(BaseModel):
    """Represents the agent posting a message to the shared space (group-visible)."""

    type: Literal["post_to_shared"] = Field(
        description="Discriminator identifying this action type.",
        default="post_to_shared",
    )
    content: str = Field(
        description="Message content to broadcast to the shared space."
    )


ActionUnion = ReplyPrivateAction | PostToSharedAction

__all__ = [
    "ReplyPrivateAction",
    "PostToSharedAction",
    "ActionUnion",
]
