"""Financial counseling demo (Phase 2.1 runtime API).

Now uses WeaverRuntime + MediationPolicy for a declarative flow.
"""

from __future__ import annotations

from typing import Dict
from langchain_core.chat_history import InMemoryChatMessageHistory
from weaver.runtime.policy import MediationPolicy
from weaver.runtime.runtime import WeaverRuntime
from weaver.models.events import UserMessageEvent

session_store: Dict[str, InMemoryChatMessageHistory] = {}


def get_session_history(session_id: str) -> InMemoryChatMessageHistory:
    return session_store.setdefault(session_id, InMemoryChatMessageHistory())


# ------------------ Helper Function ------------------


def run_turn(runtime: WeaverRuntime, space_id: str, user_id: str, content: str):
    event = UserMessageEvent(user_id=user_id, content=content)
    result = runtime.invoke(space_id=space_id, event=event)
    print(f"[{user_id}] {content}")
    print("AI:", result["response"])
    print()
    return result


# ------------------ Main Demo ------------------


def main():
    policy = MediationPolicy.default()
    runtime = WeaverRuntime(policy=policy)
    space_id = "counseling_123"

    conversation = [
        # Example turns – placeholder; should reflect whitepaper narrative.
        "我们最近在储蓄和花费上经常争吵，我觉得压力很大。",
        "其实我只是想多一些应急储备，但又不想完全放弃娱乐。",
        "我们能不能制定一个双方都舒服的预算计划？",
    ]

    for turn in conversation:
        run_turn(
            runtime, space_id, "jane", turn
        )  # simulate jane speaking all for brevity

    # Additional participants
    run_turn(runtime, space_id, "john", "我觉得我们可以稍微多花一点在体验上。")
    run_turn(runtime, space_id, "jane", "那我们能否先明确一个每月基础储蓄下限？")
    print("(Internal) total messages stored:", len(runtime._histories[space_id]))


if __name__ == "__main__":
    main()
