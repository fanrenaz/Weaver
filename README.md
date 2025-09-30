# Weaver: 一个用于构建协作式AI的原生框架

**项目代号：Weaver**  
**版本：1.0 (概念白皮书)**  
**作者：REN Yifan**  
**日期：2025/09/30**

## 摘要 (Abstract)

我们提出 **Weaver**，一个旨在将AI从“指令执行者”提升为“协作谐和者”的全新开源框架。现有的Agent开发范式在处理多方协作时，常陷入“完全公开”或“完全隔离”的困境，难以驾驭复杂的社交动态。Weaver通过引入**“交互策略 (Interaction Policies)”**和**“多视角记忆 (Multi-Perspective Memory)”**两大核心机制，构建了一个全新的“以对话为中心”的编程模型。它使AI不再是直接干预问题的“信息中介”，而是成为一个能够通过巧妙、非侵入式引导来促进参与者达成共识的“调解者”。使用Weaver，开发者可以高效地构建出如AI商业调解员、AI团队协调员等真正具备社交智慧和协调能力的下一代AI应用。

## 1. 引言 (Introduction)

大语言模型（LLM）开启了AI Agent的时代，但其智慧大多局限于人机之间的“问答”或“任务执行”。当Agent进入由多个自然人组成的、充满微妙动态的协作场域时，一个根本性的挑战浮现：我们究竟希望AI扮演何种角色？

现行框架往往将AI定位为一个**“信息中介”**。然而，这种定位导致了“广播或树洞”的二元困境：要么信息全盘公开，牺牲隐私与策略；要么会话完全隔离，丧失全局洞察与引导的价值。这种机械的干预模式，无法真正促进协作关系的健康发展。

我们相信，更高级的AI应该扮演一个**“谐和者 (Harmonizer)”**的角色。它不直接“评判”冲突，而是通过微妙的引导“化解”分歧；它不直接“给出”方案，而是通过智慧的提问“促进”参与者自己找到共识。

为了实现这一愿景，我们推出了 **Weaver**。其核心隐喻是，AI应如同一位技艺高超的**“织工(Weaver)”**，它不创造线，而是将参与者各自的“思想线索”巧妙地编织在一起，形成一幅和谐而坚韧的“协作织锦”。Weaver提供了一套全新的编程范式，让开发者能够从“指令式干预”的思维中解放出来，专注于设计一个能促进积极涌现的“协作生态系统”。

## 2. 核心概念与设计哲学 (Core Concepts & Philosophy)

### 2.1 核心范式：从“行为指令”到“空间协调”

Weaver的哲学核心是从指令AI“做什么”，转变为构建一个让智慧“能发生”的环境。

*   **传统范式：行为指令 (Behavioral Instruction)**
    开发者如同木偶师，通过复杂的Prompt或逻辑链，试图精确控制AI的每一步言行。这种方式脆弱且限制了AI的潜力。

*   **Weaver范式：空间协调 (Spatial Coordination)**
    开发者如同生态设计师，通过定义一个具备规则的**“协作空间 (Space)”**，来创造一个“微气候”。AI在这个“气候”中，其富有智慧和情商的调解行为得以**自然涌现 (Emerge)**，而非被刻板地规定。

### 2.2 签名级API：`Space` 与 `Policy`

Weaver的API设计旨在体现“空间协调”的哲学。开发者通过声明式的`Policy`来为`Space`注入“价值观”和“行为准则”。

```python
from weaver import Space
from weaver.policies import MediationPolicy

# 1. 定义一个“调解式”交互策略
<div align="center">

# Weaver AI

_协作式 / 调解式智能体运行时框架_

[![CI](https://img.shields.io/badge/CI-passing-brightgreen)](./) [![Docs](https://img.shields.io/badge/docs-mkdocs--material-blue)](./) [![License](https://img.shields.io/badge/license-Apache%202.0-lightgrey)](LICENSE)

</div>

Weaver 帮助你构建“有情境 + 会协调”的智能体：它不是简单回答，而是**引导关系与共识形成**。

## 特性速览

* Policy 驱动：显式建模角色与原则，稳定可维护
* 多视角记忆蓝图：未来支持私域/公域上下文投影
* LangGraph 状态图：可视化 + 可扩展 ReAct 循环
* 离线友好：无 Key 自动 Fake LLM 回退
* 测试 & CI：内建基本单元 / 集成测试 + GitHub Actions

## 最小示例

```python
from weaver.runtime.policy import MediationPolicy
from weaver.runtime.runtime import WeaverRuntime
from weaver.models.events import UserMessageEvent

runtime = WeaverRuntime(MediationPolicy.default())
out = runtime.invoke("demo", UserMessageEvent(user_id="alice", content="我们需要一个预算计划"))
print(out["response"])
```

## 安装 & 文档

参考 docs: `installation.md`, `getting_started.md`。

## 生态定位

与 LangChain/ LangGraph 互补：它们负责“能力”，Weaver 负责“协作语义 + 编排”。

## 路线图 (节选)

- ✅ 基础运行时 / Policy / 工具示例
- 🔄 多视角记忆（设计中）
- 🧩 可插拔策略生态
- 🌐 FastAPI / WebSocket 参考层

完整详见 文档站 “设计文档 / 白皮书” 与 “API 参考” 章节。

## 许可

Apache 2.0 (见 LICENSE)。

## 贡献

欢迎 Issue / PR。详见 `CONTRIBUTING.md`。

---
© 2025 Weaver Project

## 4. 与现有工作的比较 (Comparison with Existing Work)

Weaver与LangChain等通用工具链是**正交互补**的。LangChain提供了强大的“能力积木”（如模型接口、工具定义），而Weaver则专注于提供一个全新的“应用哲学和架构”：**一个用于构建和托管“调解式”协作AI的、有状态的后端框架。** 它为强大的Agent提供了一个能发挥其最高智慧——促进人类协作——的舞台。

## 5. 路线图与未来展望 (Roadmap & Future Work)

Weaver的旅程将是不断探索“AI如何更好地促进人类协作”的过程。我们的路线图包括：

1.  **原型验证 (v0.1-v0.3)**: 实现核心的“调解式”引导机制。
2.  **框架开源 (v0.4-v0.7)**: 发布一个包含核心API和完整文档的健壮SDK。
3.  **生态深化 (v1.0+)**: 建立一个`Policy`库，分享不同场景下的“调解策略”，并与学术界合作，深入研究计算调解学(Computational Mediation)的理论与实践。

我们相信，AI的终极价值不在于替代人类，而在于放大人类自身的智慧与善意。Weaver，正是朝着这个方向迈出的一小步。