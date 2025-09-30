# 快速入门 (Getting Started)

本指南通过两个最小示例帮助你在 5 分钟内理解 Weaver 的核心用法。

## 1. Echo Bot（最小可运行）

```python
from weaver.runtime.policy import MediationPolicy
from weaver.runtime.runtime import WeaverRuntime
from weaver.models.events import UserMessageEvent

runtime = WeaverRuntime(MediationPolicy.default())
while True:
    text = input("You: ")
    if text.strip().lower() in {"exit", "quit"}: break
    event = UserMessageEvent(user_id="you", content=text)
    out = runtime.invoke(space_id="echo_space", event=event)
    print("AI:", out["response"][:200])
```

> 没有 API Key？直接运行。系统会使用 Fake LLM 回退，确保交互流程完整。

## 2. 调解式对话微示例

```python
from weaver.runtime.policy import MediationPolicy
from weaver.runtime.runtime import WeaverRuntime
from weaver.models.events import UserMessageEvent

policy = MediationPolicy.default()
runtime = WeaverRuntime(policy)

users = [
    ("alice", "我觉得我们最近花钱太随意了"),
    ("bob", "我只是想保持一点生活质量"),
]

for uid, content in users:
    r = runtime.invoke("budget_space", UserMessageEvent(user_id=uid, content=content))
    print(uid, "=>", r["response"])  # AI 会基于上下文逐步给出调解式措辞
```

## 3. 深入下一步

| 目标 | 资源 |
|------|------|
| 理解运行时结构 | `concepts/space.md` |
| 自定义策略 | `concepts/policy.md` |
| 记忆机制 | `concepts/memory.md` |

---
遇到问题？提交 Issue 或发起讨论。
