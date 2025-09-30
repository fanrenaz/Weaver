<div align="center">

# Weaver

_A native framework for building collaborative / mediation-oriented AI agents_

[![CI](https://github.com/fanrenaz/Weaver/actions/workflows/ci.yml/badge.svg)](https://github.com/fanrenaz/Weaver/actions/workflows/ci.yml)
[![Docs Deploy](https://github.com/fanrenaz/Weaver/actions/workflows/pages.yml/badge.svg)](https://github.com/fanrenaz/Weaver/actions/workflows/pages.yml)
[![PyPI](https://img.shields.io/pypi/v/weaver-ai.svg)](https://pypi.org/project/weaver-ai/)
[![Python Versions](https://img.shields.io/pypi/pyversions/weaver-ai.svg)](https://pypi.org/project/weaver-ai/)
[![License](https://img.shields.io/badge/license-Apache%202.0-lightgrey)](LICENSE)
[![Lint](https://img.shields.io/badge/lint-ruff-informational)](https://github.com/astral-sh/ruff)
[![Code Style](https://img.shields.io/badge/code%20style-black-000000.svg)](https://github.com/psf/black)
[![Coverage](https://img.shields.io/badge/coverage-TBD-lightgrey)](./)
[![Issues](https://img.shields.io/github/issues/fanrenaz/Weaver)](https://github.com/fanrenaz/Weaver/issues)
[![Last Commit](https://img.shields.io/github/last-commit/fanrenaz/Weaver)](https://github.com/fanrenaz/Weaver/commits/main)

</div>

Weaver 让你的智能体从“回答工具”升级为“协作谐和者”：它通过显式的 Policy、结构化记忆与可组合的对话执行图，引导多个参与者逐步走向共识，而不是直接替他们给答案。

---

## 🔍 为什么需要 Weaver

当 AI 进入多人协作（团队对齐、财务讨论、冲突调解等）场景，传统“单轮问答 + 指令式 Prompt”范式会遇到：

| 典型痛点 | 表现 | Weaver 的解决方向 |
| -------- | ---- | ----------------- |
| 信息公开 / 隐私二元化 | 要么所有消息广播，要么完全割裂 | 规划多视角记忆 (public / scoped / derived) |
| Prompt 难维护 | 系统提示不断拼贴扩展 | `Policy` 抽象角色 + 原则 | 
| 协作流程不可见 | ReAct/Tool 链条隐于调用 | LangGraph 可视状态图 | 
| 测试困难 | 难以对“语气/原则一致性”做验证 | Policy 可序列化 + Prompt formatter 可测试 |
---

## 🗺️ 路线图（摘录）

* Policy 驱动：`MediationPolicy` 示例展示如何将“角色 + 原则”转为系统提示
* 统一运行时：`WeaverRuntime` 负责组装 Policy、记忆、执行图（LangGraph）
* 工具编排：示例工具 `reply_privately` / `post_to_shared` 展示私域与共享输出模式
* 可替换 LLM：未配置真实 API 时可使用 Fake / 本地模型（参见测试）
* 可测试性：Policy、Graph、工具均有独立单测
* 渐进式记忆协调：`MemoryCoordinator` 负责为每次调用准备上下文（未来扩展粒度 / 过滤策略）

---

## 🚀 快速开始 (Quick Start)

### 1. 安装（本地开发）

```bash
git clone https://github.com/your-org/weaver.git
python -m venv .venv && source .venv/bin/activate
pip install -e .[dev]
``` 

### 2. 最小示例

```python
from weaver.runtime.policy import MediationPolicy
from weaver.runtime.runtime import WeaverRuntime
from weaver.models.events import UserMessageEvent

runtime = WeaverRuntime(MediationPolicy.default())
result = runtime.invoke(
    space_id="demo_space",
    event=UserMessageEvent(user_id="alice", content="我们需要一个预算计划")
)
print(result["response"])  # AI 回复文本
```

### 3. 运行 CLI 示例

```bash
python examples/cli_demo/financial_counseling.py
```

### 4. （可选）真实 LLM 接入

在项目根目录创建 `.env`：

```
OPENAI_API_KEY=sk-xxx
```

然后运行：

```bash
python examples/hello_graph.py
```

---

## 🧠 核心抽象

| 抽象 | 作用 | 现状 | 未来方向 |
| ---- | ---- | ---- | -------- |
| Policy | 生成系统提示（角色 + 原则） | `MediationPolicy` | 策略生态 / 动态权重 |
| WeaverRuntime | 统一入口：准备上下文 -> 执行图 -> 记忆回写 | 已实现 | 插件化 Pipeline Hook |
| MemoryCoordinator | 聚合 / 提供历史消息 | 简单 in-memory | 多层视角 + 隐私过滤 |
| WeaverGraph | LangGraph 上的对话执行 (ReAct Loop) | 基础节点 | 可视化 UI / 节点市场 |
| Tools | 行为能力（私聊 / 公共广播） | 两个示例 | 权限隔离 / 策略绑定 |

---

## 🧪 测试

项目自带基础单测：

```bash
pytest -q
```

重点示例：
* `tests/runtime/test_policy.py` 验证系统提示格式
* `tests/core/test_graph.py` 使用 Fake LLM 检验 graph 行为
* `tests/building_blocks/test_tools.py` 工具回显逻辑

---

## �️ 路线图（摘录）

短期 (0.x)：
* 多视角记忆：私域 / 公域 / 主题投影
* Policy 插件注册与复合
* FastAPI / WebSocket 参考服务

中期 (1.x)：
* 调解模式模板库（团队冲突 / 预算规划 / 决策协同）
* 记忆裁剪与语义压缩
* 评估指标（介入节奏、情绪缓冲、共识质量）

长期：
* 计算调解（Computational Mediation）研究接口
* 策略学习与自适应微调

完整背景、理念及设计：参见 `docs/whitepaper_v1.md` 与 `docs/design/whitepaper_v1.md`。

---

## 🤝 贡献指南

1. Fork & 创建分支：`feat/xxx` / `fix/yyy`
2. 确保本地 `pytest` 全绿，必要时补充测试
3. 遵循代码风格：
   ```bash
   ruff check . && ruff format .
   ```
4. 提交 PR 时描述动机 + 变更影响

欢迎提交：
* 新策略 (Policy)
* 新工具 (Tool) 示例
* 记忆过滤 / 压缩算法实验

---

## 📄 许可

Apache 2.0，详见 `LICENSE`。

---

## 💬 FAQ（简要）

**Q: 这是 LangChain 的替代吗？** 不是。Weaver 聚焦“社会协作结构”，与 LangChain / LangGraph 协同工作。

**Q: 支持多模型吗？** 运行时只依赖抽象消息接口，可注入任意兼容 LLM（含 Fake for test）。

**Q: 生产可用吗？** 当前为早期实验 (0.0.x)。接口可能变动，请关注 Roadmap。

---

© 2025 Weaver Project. Amplifying human collaborative intelligence.
