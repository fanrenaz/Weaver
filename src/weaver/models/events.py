"""Event models representing external inputs entering the system."""

from __future__ import annotations

from pydantic import BaseModel, Field
from typing import Literal


class UserMessageEvent(BaseModel):
    """Represents a user sending a message into the space.

    The `role` is fixed to `user` for clarity; future versions may extend this.
    """

    type: Literal["user_message"] = Field(
        description="Event discriminator identifying a user message event.",
        default="user_message",
    )
    user_id: str = Field(description="Unique identifier (or display name) of the user.")
    content: str = Field(description="Plain text content of the user's message.")


__all__ = ["UserMessageEvent"]
