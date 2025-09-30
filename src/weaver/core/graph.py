"""Core WeaverGraph implementation constructing the ReAct-style Tool loop.

Phase 1.2 focuses on a minimal agent with two tools:
- reply_privately
- post_to_shared
"""

from __future__ import annotations

import os
import logging
from typing import Any, Dict, Optional

from langchain_openai import ChatOpenAI
from langchain_core.language_models.fake import FakeListLLM
from langchain_core.runnables import Runnable
from langchain_core.messages import SystemMessage, AIMessage
from langgraph.graph import StateGraph, END
from langgraph.prebuilt import ToolNode

from weaver.models.state import SpaceState
from dotenv import load_dotenv
from weaver.building_blocks.tools import TOOLS
from weaver.exceptions import ConfigurationError, ToolExecutionError

# Load environment variables from a local .env file if present (Phase 2.2+ runtime convenience)
load_dotenv()

logger = logging.getLogger(__name__)

DEFAULT_SYSTEM_PROMPT = (
    "You are Weaver, a neutral financial mediation assistant facilitating "
    "constructive, empathetic dialogue between partners about finances. "
    "You choose tools to either privately reassure/probe or to broadcast "
    "balanced summaries to the shared space. Always be fair, factual, and "
    "emotionally intelligent."
)


class WeaverGraph:
    """Builds and compiles the LangGraph state machine for the agent."""

    def __init__(
        self, system_prompt: str | None = None, llm: Optional[Any] = None
    ) -> None:
        # Allow injection (for tests) else configure from environment.
        if llm is None:
            llm_model = os.getenv("WEAVER_MODEL", "gpt-5-mini")
            api_key = os.getenv("OPENAI_API_KEY")  # rely on user environment
            api_base = os.getenv("OPENAI_API_BASE") or os.getenv("OPENAI_BASE_URL")
            if api_key:
                try:
                    extra_kwargs: Dict[str, Any] = {}
                    if api_base:
                        extra_kwargs["openai_api_base"] = api_base
                    extra_kwargs["api_key"] = api_key
                    llm = ChatOpenAI(model=llm_model, **extra_kwargs)
                except Exception as e:  # pragma: no cover
                    logger.warning(
                        "Failed to initialize ChatOpenAI (%s); falling back to FakeListLLM",
                        e,
                    )
                    llm = self._build_fallback_llm()
            else:
                logger.warning(
                    "OPENAI_API_KEY absent; using FakeListLLM fallback (set in .env or env vars to enable real LLM)."
                )
                llm = self._build_fallback_llm()
        self._llm = llm  # type: ignore[assignment]
        self._system_prompt = system_prompt or DEFAULT_SYSTEM_PROMPT
        self.app = self._build_graph()

    # ---------------- Agent Node -----------------
    def _agent_node(self, state: SpaceState) -> Dict[str, Any]:  # type: ignore[override]
        """Decide next action using the LLM bound with available tools.

        Returns a partial state update containing either a planned tool call(s)
        or None signaling the loop should end.
        """
        try:
            bound_llm = self._llm.bind_tools(TOOLS)
            messages = [SystemMessage(content=self._system_prompt)] + state.get(
                "input", []
            )
            response = bound_llm.invoke(messages)
        except ConfigurationError:
            raise
        except Exception as e:  # pragma: no cover - defensive
            logger.exception("LLM/tool invocation error")
            raise ToolExecutionError(str(e)) from e
        if not isinstance(response, AIMessage):
            logger.warning("Agent response not AIMessage: %s", type(response))
            tool_calls = None
        else:
            tool_calls = response.tool_calls or None
        return {
            "input": [response],  # append AI message to history
            "action_to_execute": tool_calls,
        }

    # --------------- Graph Construction ---------------
    def _build_graph(self):
        workflow = StateGraph(SpaceState)
        workflow.add_node("agent", self._agent_node)
        tool_node = ToolNode(TOOLS, messages_key="input")
        workflow.add_node("tools", tool_node)

        workflow.set_entry_point("agent")
        workflow.add_conditional_edges(
            "agent", _should_continue_node, {"tools": "tools", "end": END}
        )
        workflow.add_edge("tools", "agent")  # ReAct loop
        return workflow.compile()

    @staticmethod
    def _build_fallback_llm():
        """Construct a deterministic fallback LLM for offline / missing key scenarios."""
        base_fake = FakeListLLM(  # type: ignore[call-arg]
            responses=[
                "(模拟) 我理解你在财务沟通上的压力。你可以进一步说明彼此的主要关切点吗？",
                "(模拟) 你希望建立更大的应急储备，而同时保持一定的生活质量。",
                "(模拟) 建议：共同制定一个包含储蓄、必要支出和灵活娱乐额度的三段式预算。你们觉得可行吗？",
            ]
        )

        class _WrappedFake(Runnable):  # type: ignore[misc]
            def invoke(self, messages, config=None):  # type: ignore[override]
                text = base_fake.invoke(messages)
                return AIMessage(content=text)

            def bind_tools(self, tools):  # mimic ChatOpenAI API
                return self

        return _WrappedFake()


# --------------- Conditional Router ---------------


def _should_continue_node(state: SpaceState) -> str:
    calls = state.get("action_to_execute")
    if calls:
        return "tools"
    return "end"


__all__ = ["WeaverGraph", "_should_continue_node"]
