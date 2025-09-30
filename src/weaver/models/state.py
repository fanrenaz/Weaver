"""TypedDict state definition used internally by the LangGraph workflow.

The state accumulates inputs, intermediate tool execution data and final outputs.
"""

from __future__ import annotations

from typing import Any, List, Optional, TypedDict, Annotated
from operator import add
from langchain_core.messages import BaseMessage


class SpaceState(TypedDict, total=False):
    """State container for one execution loop inside the WeaverGraph.

    Fields:
        input: The running list of messages (User + AI + Tool) forming context.
        action_to_execute: Parsed tool calls chosen by the agent (or None).
        tool_output: Last tool invocation raw output returned to the agent.
    """

    input: Annotated[List[BaseMessage], add]
    action_to_execute: Optional[Any]
    tool_output: Optional[str]


__all__ = ["SpaceState"]
