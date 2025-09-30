"""MemoryCoordinator: first pass implementation for multi-perspective context.

Phase 2.1 keeps logic minimal: gather history for a given space and optionally
merge across participants if policy implies a "god view" (future flag).
"""

from __future__ import annotations

from typing import Dict, List
from langchain_core.messages import BaseMessage


class MemoryCoordinator:
    """Coordinates retrieval/assembly of contextual message history.

    For v0.1 we assume a single shared history per space. Future versions can
    maintain per-user private threads and perform selective projection.
    """

    def __init__(self, space_histories: Dict[str, List[BaseMessage]]):
        self._space_histories = space_histories

    def prepare_context(self, space_id: str, current_user_id: str) -> List[BaseMessage]:
        """Return the message list used as context for the next invocation.

        Parameters:
            space_id: Logical identifier for the collaborative space.
            current_user_id: The user sending the new event (reserved for future use,
                e.g. perspective filtering).
        """
        return self._space_histories.setdefault(space_id, [])

    def append(self, space_id: str, messages: List[BaseMessage]) -> None:
        history = self._space_histories.setdefault(space_id, [])
        history.extend(messages)


__all__ = ["MemoryCoordinator"]
