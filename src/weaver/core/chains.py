"""Factory helpers for composing Weaver graph with standard LangChain history.

Phase 1.3 introduces an adapter runnable so that a plain dict input
{"messages": List[BaseMessage]} can be transformed into the internal
`SpaceState` required by the compiled LangGraph. This allows seamless
use of `RunnableWithMessageHistory`.
"""

from __future__ import annotations

from typing import Dict, Any
from langchain_core.messages import BaseMessage
from langchain_core.runnables import RunnableLambda

from .graph import WeaverGraph
from weaver.models.state import SpaceState


def create_state_adapter_runnable() -> RunnableLambda:
    """Create a runnable that maps a public dict interface to SpaceState.

    Expected external input shape (for integration with history wrappers):
        {"input": List[BaseMessage]}

    Returns:
        RunnableLambda that when invoked returns a SpaceState dict with the
        "input" key populated (other keys omitted until produced downstream).
    """

    def _map(payload: Dict[str, Any]) -> SpaceState:  # type: ignore[override]
        messages = payload.get("input", [])
        if not isinstance(messages, list) or (
            messages and not isinstance(messages[0], BaseMessage)
        ):
            raise TypeError(
                "Adapter expected payload['input'] to be List[BaseMessage], got: "
                f"{type(messages)}"
            )
        return {"input": messages}  # type: ignore[return-value]

    return RunnableLambda(_map)


def create_weaver_chain():
    """Compose adapter + core graph into a single runnable chain.

    Usage:
        chain = create_weaver_chain()
        chain.invoke({"input": [HumanMessage(content="hello")]})

    This chain is now compatible with `RunnableWithMessageHistory` using
    input_messages_key="input" and history_messages_key="input".
    """
    adapter = create_state_adapter_runnable()
    core_graph = WeaverGraph().app

    def _normalize_output(state: SpaceState):  # type: ignore[override]
        # Ensure downstream history wrapper sees the updated message list under same key.
        return {"input": state.get("input", [])}

    normalizer = RunnableLambda(_normalize_output)
    return adapter | core_graph | normalizer


__all__ = ["create_state_adapter_runnable", "create_weaver_chain"]
