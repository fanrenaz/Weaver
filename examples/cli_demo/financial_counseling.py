"""Financial counseling multi-turn demo (Phase 1.2).

This script temporarily implements L3 (runtime/session history) + L4 (app flow).
"""
from __future__ import annotations

from typing import Dict, List
from langchain_core.messages import BaseMessage, HumanMessage

from weaver.core.graph import WeaverGraph

# ------------------ L3 Temporary Session Store ------------------
# In future phases this will move into a persistence layer under runtime/.
session_store: Dict[str, List[BaseMessage]] = {}


def get_session_history(session_id: str) -> List[BaseMessage]:
    return session_store.setdefault(session_id, [])


# ------------------ Helper Function ------------------

def run_turn(app, session_id: str, content: str):
    user_msg = HumanMessage(content=content)
    history = get_session_history(session_id)
    # Build state and invoke graph directly
    state = {"input": history + [user_msg]}
    result_state = app.invoke(state)
    # Update stored history
    history.extend(result_state.get("input", []))
    print("--- USER:", content)
    tool_out = result_state.get("tool_output")
    if tool_out:
        print("[tool_output]", tool_out)
    # The AI message appended is last element of input
    ai_messages = [m for m in result_state.get("input", []) if getattr(m, 'type', '') == "ai"]
    if ai_messages:
        print("AI:", ai_messages[-1].content)
    print()
    return result_state


# ------------------ Main Demo ------------------

def main():
    graph = WeaverGraph()

    session_id = "couple_finance_demo"

    conversation = [
        # Example turns – placeholder; should reflect whitepaper narrative.
        "我们最近在储蓄和花费上经常争吵，我觉得压力很大。",
        "其实我只是想多一些应急储备，但又不想完全放弃娱乐。",
        "我们能不能制定一个双方都舒服的预算计划？",
    ]

    for turn in conversation:
        run_turn(graph.app, session_id, turn)

    print("Session history length:", len(get_session_history(session_id)))


if __name__ == "__main__":
    main()
