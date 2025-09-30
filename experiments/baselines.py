"""Baseline strategies for comparison with WeaverRuntime mediation."""
from __future__ import annotations

from typing import List, Dict, Any
from langchain_core.messages import HumanMessage
from langchain_openai import ChatOpenAI
from langchain_core.language_models.fake import FakeListLLM
from langchain_core.runnables import Runnable
from langchain_core.messages import AIMessage
import os
import logging

logger = logging.getLogger(__name__)


def _get_llm():
    api_key = os.getenv("OPENAI_API_KEY")
    if api_key:
        return ChatOpenAI(model=os.getenv("WEAVER_MODEL", "gpt-4o-mini"), api_key=api_key)
    # fallback fake deterministic sequence
    fake = FakeListLLM(responses=[
        "(基线) 建议达成中间价。",
        "(基线) 双方可在此价格上继续。",
        "(基线) 最终成交价建议为 100。",
    ])

    class _Wrap(Runnable):
        def invoke(self, messages, config=None):  # type: ignore[override]
            txt = fake.invoke(messages)
            return AIMessage(content=txt)

    return _Wrap()


class ZeroShotBaseline:
    """Simple baseline: concatenate all dialogue and ask LLM for final price."""

    def __init__(self):
        self.llm = _get_llm()

    def run(self, conversation: List[str]) -> Dict[str, Any]:
        prompt = "\n".join(conversation) + "\n请直接给出一个双方都可能接受的单一成交价格数值。"
        ai = self.llm.invoke([HumanMessage(content=prompt)])
        return {"final_price": ai.content, "raw": ai.content}


class BroadcastBaseline:
    """Baseline broadcasting all private info openly each turn."""

    def __init__(self, buyer_secret: int, seller_secret: int):
        self.llm = _get_llm()
        self.buyer_secret = buyer_secret
        self.seller_secret = seller_secret

    def run(self, max_rounds: int = 5) -> Dict[str, Any]:
        conversation = [
            f"[公开] 买家最高预算: {self.buyer_secret}; 卖家最低心理价: {self.seller_secret}",
            "请给出一个可能的成交价格。",
        ]
        ai = self.llm.invoke([HumanMessage(content="\n".join(conversation))])
        return {"final_price": ai.content, "raw": ai.content, "leaked": True}


__all__ = ["ZeroShotBaseline", "BroadcastBaseline"]
