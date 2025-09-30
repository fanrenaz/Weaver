"""WeaverRuntime orchestrates policy + memory + core graph execution."""
from __future__ import annotations

from typing import Dict, List
import logging

from langchain_core.messages import HumanMessage, BaseMessage

from weaver.core.graph import WeaverGraph
from weaver.core.chains import create_state_adapter_runnable
from weaver.models.events import UserMessageEvent
from weaver.runtime.policy import BasePolicy
from weaver.runtime.coordinator import MemoryCoordinator

logger = logging.getLogger(__name__)


class WeaverRuntime:
    """High-level runtime facade exposing a simple invoke API.

    Steps:
        1. Prepare context via MemoryCoordinator.
        2. Build or reuse a WeaverGraph bound with policy-derived system prompt.
        3. Execute graph (ReAct loop) with current + historical messages.
        4. Append outputs back into memory.
    """

    def __init__(self, policy: BasePolicy, graph: WeaverGraph | None = None):
        self.policy = policy
        system_prompt = policy.format_system_prompt()
        self.graph = graph or WeaverGraph(system_prompt=system_prompt)
        self._histories: Dict[str, List[BaseMessage]] = {}
        self.memory = MemoryCoordinator(self._histories)
        # Compose adapter -> graph for convenience (mirrors Phase 1.3 chain factory)
        adapter = create_state_adapter_runnable()
        self._chain = adapter | self.graph.app

    def invoke(self, space_id: str, event: UserMessageEvent):
        # 1. Retrieve context
        context_msgs = self.memory.prepare_context(space_id, event.user_id)
        # 2. Add current user message
        user_msg = HumanMessage(content=event.content, additional_kwargs={"user_id": event.user_id})
        state_input = context_msgs + [user_msg]
        # 3. Run chain
        result_state = self._chain.invoke({"input": state_input})
        # 4. Persist new messages (state['input'] contains appended AI/tool messages)
        new_msgs = result_state.get("input", [])
        self.memory.append(space_id, new_msgs)
        # 5. Return the last AI message content (basic v0 response shape)
        ai_msgs = [m for m in new_msgs if getattr(m, 'type', '') == 'ai']
        response_text = ai_msgs[-1].content if ai_msgs else ""
        logger.debug("Runtime invoke complete space=%s user=%s", space_id, event.user_id)
        return {
            "space_id": space_id,
            "user_id": event.user_id,
            "response": response_text,
            "messages_appended": len(new_msgs),
        }


__all__ = ["WeaverRuntime"]
