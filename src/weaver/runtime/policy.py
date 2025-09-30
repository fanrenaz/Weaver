"""Policy abstractions defining system role + guiding principles.

Phase 2.1 introduces a simple mediation policy that can format the system
prompt consumed by the core graph.
"""

from __future__ import annotations

from typing import List
from pydantic import BaseModel, Field


class BasePolicy(BaseModel):
    """Abstract base policy describing role + principles.

    Subclasses should override/extend as needed. For now we only implement a
    simple formatter for the system prompt.
    """

    role: str = Field(description="High-level role description for the assistant.")
    principles: List[str] = Field(
        description="List of guiding principles used to steer conversational tone and strategy."
    )

    def format_system_prompt(self) -> str:
        bullet_points = "\n".join(f"- {p}" for p in self.principles)
        return (
            f"{self.role.strip()}\n\nCore Principles:\n{bullet_points}\n\n"
            "When responding: apply the principles, be concise, empathetic, factual, and tool-aware."
        )


class MediationPolicy(BasePolicy):
    """Concrete mediation-oriented policy with a default template."""

    @classmethod
    def default(cls) -> "MediationPolicy":  # convenience
        return cls(
            role=(
                "你是一名中立的财务调解助理。你的目标是通过引导与反思，帮助参与者建立信任、澄清意图、并共同制定可执行的财务协作策略。"
            ),
            principles=[
                "优先验证情绪，再探讨方案",
                "避免偏袒，使用中性、结构化语言",
                "必要时将复杂分歧抽象为高层主题再引导讨论",
                "逐步共建：鼓励双方提出小步试验性的改进而非一次性彻底重构",
            ],
        )


__all__ = ["BasePolicy", "MediationPolicy"]
