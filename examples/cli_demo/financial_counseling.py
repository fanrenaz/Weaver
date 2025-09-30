"""Financial counseling multi-turn demo (Phase 1.3).

Demonstrates integration with RunnableWithMessageHistory via adapter chain.
"""
from __future__ import annotations

from typing import Dict
from langchain_core.messages import BaseMessage, HumanMessage
from langchain_core.runnables.history import RunnableWithMessageHistory
from langchain_core.chat_history import InMemoryChatMessageHistory
from weaver.core.chains import create_weaver_chain

# ------------------ L3 Temporary Session Store ------------------
session_store: Dict[str, InMemoryChatMessageHistory] = {}


def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    return session_store.setdefault(session_id, InMemoryChatMessageHistory())


# ------------------ Helper Function ------------------

def run_turn(app_with_history, session_id: str, content: str):
    user_msg = HumanMessage(content=content)
    result_state = app_with_history.invoke(
        {"input": [user_msg]},
        config={"configurable": {"session_id": session_id}},
    )
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
    chain = create_weaver_chain()
    app_with_history = RunnableWithMessageHistory(
        chain,
        lambda session_id: get_session_history(session_id),
        input_messages_key="input",
        history_messages_key="input",
    )

    session_id = "couple_finance_demo"

    conversation = [
        # Example turns – placeholder; should reflect whitepaper narrative.
        "我们最近在储蓄和花费上经常争吵，我觉得压力很大。",
        "其实我只是想多一些应急储备，但又不想完全放弃娱乐。",
        "我们能不能制定一个双方都舒服的预算计划？",
    ]

    for turn in conversation:
        run_turn(app_with_history, session_id, turn)

    # Validate isolation with different session ids
    run_turn(app_with_history, "jane_session", "我担心我们的储蓄速度不够。")
    run_turn(app_with_history, "john_session", "我觉得我们可以稍微多花一点在体验上。")

    print("Jane history size:", len(get_session_history("jane_session").messages))
    print("John history size:", len(get_session_history("john_session").messages))

    print("Shared session (god view) history length:", len(get_session_history(session_id).messages))


if __name__ == "__main__":
    main()
