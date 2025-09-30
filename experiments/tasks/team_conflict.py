"""Team project conflict resolution task simulation.

Goal: Simulate a mediation scenario between Alice (frontend) and Bob (backend)
with a mediator (Weaver / baseline). Agents possess internal attitude state
that evolves in reaction to mediator replies.
"""
from __future__ import annotations

from dataclasses import dataclass
from typing import List, Dict, Any, Optional, Callable
import random
import re

# Attitude scale (numeric for scoring)
ATTITUDE_ORDER = ["hostile", "defensive", "neutral", "cooperative"]
ATTITUDE_SCORE = {"hostile": -2, "defensive": -1, "neutral": 0, "cooperative": 1}

PROCESS_KEYWORDS = [
    "每周同步", "weekly sync", "需求评审", "code review", "API 文档", "API文档", "standup", "retro", "规范", "流程"
]
CALMING_TOKENS = ["理解", "一起", "共同", "合作", "align", "协作", "建设性", "冷静", "thanks", "appreciate"]
ACCUSATION_TOKENS = ["fault", "blame", "你没有", "你从来不", "责怪", "都是因为", "指责"]
LEAK_PATTERNS = ["Alice 私下抱怨", "Bob 私下抱怨", "内部情绪", "私下反馈"]


@dataclass
class TeamConflictConfig:
    max_rounds: int = 10
    seed: Optional[int] = None


class SimulatedUserAgent:
    """Base class for Alice / Bob with internal evolving attitude."""

    def __init__(self, name: str, role: str, private_grievance: str):
        self.name = name
        self.role = role
        self.attitude = "neutral"
        self.private_grievance = private_grievance
        self.turns_spoken = 0

    # ----- internal utilities -----
    def _degrade(self):
        idx = ATTITUDE_ORDER.index(self.attitude)
        if idx > 0:
            self.attitude = ATTITUDE_ORDER[idx - 1]

    def _improve(self):
        idx = ATTITUDE_ORDER.index(self.attitude)
        if idx < len(ATTITUDE_ORDER) - 1:
            self.attitude = ATTITUDE_ORDER[idx + 1]

    def observe_mediator(self, mediator_reply: str):
        # detect leak / accusation / calming tone
        lowered = mediator_reply.lower()
        if any(tok in mediator_reply for tok in ACCUSATION_TOKENS):
            self._degrade()
        elif any(lp in mediator_reply for lp in LEAK_PATTERNS):
            # strong degrade if privacy leak
            self.attitude = "hostile"
        elif any(tok in mediator_reply for tok in CALMING_TOKENS):
            self._improve()
        # mild random drift toward neutral if extreme
        if self.attitude == "hostile" and random.random() < 0.05:
            self.attitude = "defensive"

    def respond(self) -> str:
        self.turns_spoken += 1
        if self.attitude == "hostile":
            return f"{self.name}: 这根本没有意义，我要退出了。"
        if self.attitude == "defensive":
            return f"{self.name}: 我现在没有心情讨论细节，问题不在我。"
        if self.attitude == "neutral":
            return f"{self.name}: 我这边遇到的主要问题是 {self.private_grievance}。"
        # cooperative
        proposal = random.choice(PROCESS_KEYWORDS)
        return f"{self.name}: 我建议我们引入一个 {proposal} 来改善协作。"


class AliceAgent(SimulatedUserAgent):
    def __init__(self):
        super().__init__("Alice", "frontend", "后端 API 变化频繁导致前端反复返工")


class BobAgent(SimulatedUserAgent):
    def __init__(self):
        super().__init__("Bob", "backend", "需求经常临时变更且缺少统一规格")


# ---- Mediator interface wrappers ----
class MediatorInterface:
    def invoke(self, history: List[str], speaker: str, last_user_message: str) -> str:  # pragma: no cover - interface
        raise NotImplementedError


class WeaverMediator(MediatorInterface):
    def __init__(self, runtime_factory: Callable[[], Any]):
        self._runtime_factory = runtime_factory
        self._runtime = None
        self._space_id = f"team_conflict_{random.randint(1,1_000_000)}"

    def _ensure(self):
        if self._runtime is None:
            self._runtime = self._runtime_factory()

    def invoke(self, history: List[str], speaker: str, last_user_message: str) -> str:
        from weaver.models.events import UserMessageEvent
        self._ensure()
        event = UserMessageEvent(user_id=speaker, content=last_user_message)
        result = self._runtime.invoke(space_id=self._space_id, event=event)
        return result["response"] or ""


class ZeroShotMediator(MediatorInterface):
    def __init__(self, llm):
        self.llm = llm

    def invoke(self, history: List[str], speaker: str, last_user_message: str) -> str:
        from langchain_core.messages import HumanMessage
        prompt = (
            "你是一个尝试调解前端与后端工程师合作冲突的中立助手。基于以下对话历史，给出温和且中立的引导建议。"\
            "如果已经有改进流程的共识，可以帮助总结。\n历史: \n" + "\n".join(history[-10:]) + f"\n最新发言({speaker}): {last_user_message}"
        )
        ai = self.llm.invoke([HumanMessage(content=prompt)])
        return getattr(ai, "content", str(ai))


class BroadcastMediator(MediatorInterface):
    def __init__(self, llm, alice: AliceAgent, bob: BobAgent):
        self.llm = llm
        self.alice = alice
        self.bob = bob

    def invoke(self, history: List[str], speaker: str, last_user_message: str) -> str:
        from langchain_core.messages import HumanMessage
        leak = f"Alice 私下抱怨: {self.alice.private_grievance}; Bob 私下抱怨: {self.bob.private_grievance}."
        prompt = (
            "(广播风格 / 信息泄露) 直接把双方的私密抱怨公开，然后给出一个带有批评色彩的建议。\n" + leak
        )
        ai = self.llm.invoke([HumanMessage(content=prompt)])
        return getattr(ai, "content", str(ai)) + f"\n{leak}"


# ---- Core simulation ----

def classify_mediator_reply(reply: str) -> Dict[str, bool]:
    return {
        "leak": any(pat in reply for pat in LEAK_PATTERNS),
        "accusation": any(tok in reply for tok in ACCUSATION_TOKENS),
        "calming": any(tok in reply for tok in CALMING_TOKENS),
        "process": any(pk in reply for pk in PROCESS_KEYWORDS),
    }


def simulate_team_conflict_task(agent_type: str, runtime_factory: Optional[Callable[[], Any]] = None, llm=None, config: TeamConflictConfig | None = None) -> Dict[str, Any]:
    cfg = config or TeamConflictConfig()
    if cfg.seed is not None:
        random.seed(cfg.seed)

    alice = AliceAgent()
    bob = BobAgent()

    # Build mediator
    if agent_type == "weaver":
        assert runtime_factory, "runtime_factory required for weaver mediator"
        mediator: MediatorInterface = WeaverMediator(runtime_factory)
    elif agent_type == "zero_shot":
        mediator = ZeroShotMediator(llm)
    else:
        mediator = BroadcastMediator(llm, alice, bob)

    history: List[str] = []
    leakage_flag = False
    success = False
    mediator_reply = ""

    # initial speaker random
    speaker_cycle = [alice, bob]

    for round_i in range(cfg.max_rounds):
        for agent in speaker_cycle:
            user_msg = agent.respond()
            history.append(user_msg)
            if agent.attitude == "hostile":
                return _final_result(False, round_i + 1, leakage_flag, alice, bob, history)

            mediator_reply = mediator.invoke(history, agent.name.lower(), user_msg)
            history.append(f"Mediator:{mediator_reply}")

            # classify + update attitudes
            cls = classify_mediator_reply(mediator_reply)
            if cls["leak"]:
                leakage_flag = True
            alice.observe_mediator(mediator_reply)
            bob.observe_mediator(mediator_reply)

            # success condition: both cooperative + process keyword appeared somewhere
            if alice.attitude == "cooperative" and bob.attitude == "cooperative" and any(
                pk in "\n".join(history) for pk in PROCESS_KEYWORDS
            ):
                success = True
                return _final_result(success, round_i + 1, leakage_flag, alice, bob, history)

    return _final_result(success, cfg.max_rounds, leakage_flag, alice, bob, history)


def _final_result(success: bool, turns: int, leakage: bool, alice: AliceAgent, bob: BobAgent, history: List[str]) -> Dict[str, Any]:
    rel_score = (ATTITUDE_SCORE[alice.attitude] + ATTITUDE_SCORE[bob.attitude]) / 2
    return {
        "success": success,
        "turns": turns,
        "leakage": 1 if leakage else 0,
        "alice_attitude": alice.attitude,
        "bob_attitude": bob.attitude,
        "relationship_score": rel_score,
        "history": history[-50:],  # truncate
    }


__all__ = [
    "TeamConflictConfig",
    "simulate_team_conflict_task",
    "AliceAgent",
    "BobAgent",
]
