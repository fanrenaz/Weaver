# Weaver AI

> 一个用于构建“协作式 / 调解式”智能体 (Mediated, Collaborative AI) 的原生框架。

Weaver 旨在让 AI 从“回答工具”进化为“关系协调者 (Harmonizer)”。它通过 **Policy（交互策略）** + **多视角记忆 (Multi‑Perspective Memory)** + **对话为中心的状态图 (LangGraph)**，帮助你快速搭建具备“情境理解 + 工具调用 + 关系引导”能力的智能体。

## 为什么选择 Weaver？

| 需求 | 传统 Agent 框架痛点 | Weaver 的做法 |
|------|--------------------|---------------|
| 多参与者对话 | 要么全部公开，要么完全隔离 | 空间编排 + 选择性上下文聚合 |
| 价值观/风格一致性 | Prompt 片段散落、难维护 | `Policy` 显式建模角色 & 原则 |
| 工具调用与叙事融合 | ReAct 易碎，难插入策略逻辑 | LangGraph 状态机 + 可编排 Runtime |
| 离线 / 无 API Key 调试 | 初始化失败或行为随机 | 内置 Fake LLM 回退，测试友好 |

## 5 分钟快速一览

```python
from weaver.runtime.policy import MediationPolicy
from weaver.runtime.runtime import WeaverRuntime
from weaver.models.events import UserMessageEvent

policy = MediationPolicy.default()
runtime = WeaverRuntime(policy)

event = UserMessageEvent(user_id="alice", content="我们在家庭预算上争执不休…")
result = runtime.invoke(space_id="session_1", event=event)
print(result["response"])  # => AI 调解式回应
```

更多示例参见 “快速入门”。

## 生态定位

Weaver 并不重复造轮子：LLM 与工具抽象复用 LangChain / LangGraph；创新集中在“运行时编排 + 协作语义建模”层。

## 下一步

* 安装: 参考 `installation.md`
* 跑通第一个 Echo / 调解示例: 见 `getting_started.md`
* 深入理解：阅读 核心概念 / 白皮书

---
© 2025 Weaver Project. Apache 2.0 Licensed.
