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
mediation_policy = MediationPolicy(
    role="你是一名专业的关系调解员。你的目标不是做出裁决，而是通过中立的提问和引导，帮助参与者建立信任、理解彼此并自行找到解决方案。",
    principles=[
        "优先验证情感，而非评判事实。",
        "通过抽象和类比，在不泄露隐私的前提下传递洞察。",
        "总是将对话的主导权交还给参与者。"
    ]
)

# 2. 创建一个协调空间
coordination_space = Space(
    participants=["user_A", "user_B"],
    policy=mediation_policy
)
```

开发者不再是编写具体逻辑的“程序员”，而是定义高级原则的“哲学家”。

### 2.3 涌现的智慧：一次“调解式”引导的解剖

让我们通过一个精炼的示例，来感受Weaver的哲学。这个场景是“夫妻财务咨询”，参与者是丈夫John、妻子Jane，以及由`MediationPolicy`驱动的AI调解员。

#### **回合一：私密信息的接收 (Receiving Private Information)**

对话始于妻子Jane向AI表达了她的私下担忧。

```python
# Jane发起了一次私密对话
financial_space.send(
    user="jane", 
    message="我其实很担心，因为John上个月有一笔不小的信用卡账单，我不知道他买了什么。我怕他有财务压力，或者对我不够坦诚。"
)
```

> **AI对Jane的私密回复 (仅Jane可见):**
> > 我完全理解你的担忧。财务的透明度是建立信任的基石。感谢你首先选择与我沟通。
> >
> > 请给我一点时间。我会寻找一个自然、温和的机会，来引导John讨论关于家庭财务规划和沟通的话题。请放心，我绝不会提及你今天的谈话或具体的账单问题。

> **Weaver的洞察:**
> AI接收了关键信息，并向Jane做出了一个**行动承诺**。`MediationPolicy`指导AI将“解决Jane的担忧”作为一个**后台任务**。现在，AI进入了“潜伏”和“等待时机”的状态。

#### **回合二：无关话题中的“植入” (Seeding in an Unrelated Context)**

几天后，John因为另一个完全不相干的话题，主动找到了AI进行私聊。

```python
# John发起了一次新的私密对话
financial_space.send(
    user="john",
    message="嘿，最近工作上有点烦，想找你聊聊。我老板总是不信任我们团队，事事都要插手，让人感觉很压抑。"
)
```

> **AI对John的私密回复 (仅John可见):**
> > 听到你工作上的烦恼，我感到很遗憾。在团队中，当缺乏信任和自主权时，确实会极大地消耗人的精力和创造力。被过度管理的感觉的确不好受。
> >
> > (……此处省略若干对John工作问题的安抚和建议……)
> >
> > **……说起来，这种‘信任’和‘透明’的主题，其实在生活的方方面面都非常重要，无论是工作伙伴，还是家庭伴侣之间。**
> >
> > **有时候，主动、开放地分享一些信息和规划，比如‘我最近在忙什么’或者‘我下个月有个什么计划’，反而能建立起更深的信任感，让对方感到安心和被尊重，从而给予我们更多的空间和支持。这只是我由你的工作问题引发的一些联想，希望能对你有所启发。**

> **Weaver的洞奇 (The Magic Moment):**
> 这就是整个示例中最精妙的“魔法时刻”！
> 1.  **绝口不提**: AI完全没有提到“钱”、“账单”、“Jane”等任何敏感词。
> 2.  **主题升华**: 它从John的“工作抱怨”中，敏锐地抽象出了“**信任、透明、过度管理**”这个核心主题。
> 3.  **无缝迁移**: 它将这个主题从“工作场景”**无缝地、比喻性地迁移**到了“家庭场景”。
> 4.  **思想植入**: 它没有给出任何指令，而是以一种“个人感悟”和“启发”的方式，向John的潜意识里植入了一个思想种子：“**主动分享规划，可以建立信任，换取空间**”。
>
> 这个操作的难度极高，它要求AI不仅能理解对话的表层含义，更能进行深度的**主题抽象和类比推理**。而Weaver的`MediationPolicy`正是被设计来引导LLM进行此类高级推理的。

#### **回合三：行为的改变与问题的解决 (Behavioral Change & Resolution)**

几天后，被植入了“思想种子”的John，在公开对话中采取了主动。

```python
# John在公开对话中主动开启了一个新话题
financial_space.send(
    user="john",
    message="嘿，Jane。我最近在想，我们是不是可以像管理公司项目一样，每个月也同步一下我们的‘家庭项目’？比如大的开销计划或者各自的财务状况，这样彼此都更清楚，也更安心。"
)
```

> **AI的公开回复 (John和Jane均可见):**
> > John，这是一个非常棒的提议！主动建立沟通机制，是伙伴关系走向成熟和健康的标志。Jane，你对John这个想法感觉如何？

> **Weaver的洞察:**
> AI的“潜伏”任务成功了。它没有去“灭火”，而是通过巧妙的引导，让John自己**“防火”**。问题被参与者自己主动地、以一种更健康的方式解决了。AI此时的角色，从一个中介，升华为一个**“关系促进者”**。最后，它再次将舞台交给Jane，让对话自然地在夫妻之间流动。

## 3. 架构与实现方案 (Architecture & Implementation)

### 3.1 范式转变：从“以Agent为中心”到“以对话为中心”

为了实现“谐和者”的哲学，Weaver在架构上采取了**“以对话为中心 (Dialogue-Centric)”**的设计。框架的最高抽象是**“协作空间 (Space)”**，它代表了关系和对话本身。Agent和人类都是这个空间中的平等参与者，服务于空间的整体健康，而非将Agent作为宇宙中心。

### 3.2 架构演进：从“原子化API”到“持久化会话服务”

支撑这一范式的是Weaver作为**持久化协作会话服务器 (Persistent, Stateful Session Server)**的架构定位。每个`Space`都是一个后端的长生命周期对象，使其能真正理解和管理对话的完整历史与状态，从而做出有远见的、非侵入式的引导，而不是仅仅对单次请求做出被动反应。我们计划采用**LangGraph**作为核心引擎，以状态机模型来体现这种对话的演化。

## 4. 与现有工作的比较 (Comparison with Existing Work)

Weaver与LangChain等通用工具链是**正交互补**的。LangChain提供了强大的“能力积木”（如模型接口、工具定义），而Weaver则专注于提供一个全新的“应用哲学和架构”：**一个用于构建和托管“调解式”协作AI的、有状态的后端框架。** 它为强大的Agent提供了一个能发挥其最高智慧——促进人类协作——的舞台。

## 5. 路线图与未来展望 (Roadmap & Future Work)

Weaver的旅程将是不断探索“AI如何更好地促进人类协作”的过程。我们的路线图包括：

1.  **原型验证 (v0.1-v0.3)**: 实现核心的“调解式”引导机制。
2.  **框架开源 (v0.4-v0.7)**: 发布一个包含核心API和完整文档的健壮SDK。
3.  **生态深化 (v1.0+)**: 建立一个`Policy`库，分享不同场景下的“调解策略”，并与学术界合作，深入研究计算调解学(Computational Mediation)的理论与实践。

我们相信，AI的终极价值不在于替代人类，而在于放大人类自身的智慧与善意。Weaver，正是朝着这个方向迈出的一小步。

## 附录：Phase 1.3 进展摘要

在 Phase 1.3 中，我们引入了一个适配器链：

```
create_state_adapter_runnable() -> WeaverGraph().app -> output normalizer
```

它允许使用标准 `RunnableWithMessageHistory` 进行会话记忆管理，无需让外部调用者了解内部 `SpaceState` 结构。示例脚本 `examples/cli_demo/financial_counseling.py` 展示了多会话隔离与“上帝视角”会话的上下文累积。

## 附录：Phase 2.1 运行时框架化

引入 `Policy` (`MediationPolicy`)、`MemoryCoordinator` 与 `WeaverRuntime`：

```python
from weaver.runtime.policy import MediationPolicy
from weaver.runtime.runtime import WeaverRuntime
from weaver.models.events import UserMessageEvent

policy = MediationPolicy.default()
runtime = WeaverRuntime(policy=policy)
event = UserMessageEvent(user_id="jane", content="我们最近在储蓄上有争执……")
result = runtime.invoke(space_id="counseling_123", event=event)
print(result["response"])
```

`Policy.format_system_prompt()` 负责将策略语义转化为系统提示；`MemoryCoordinator` 当前为单一共享历史，未来将扩展为多视角选择性拼接；`WeaverRuntime` 对外提供声明式 `invoke` 接口，隐藏底层图与适配器细节。

## 附录：Phase 2.2 实验平台

新增 `experiments/` 目录，支持复现性研究：

结构:
- `experiments/runner.py`: 统一入口，可选择 `weaver|zero_shot|broadcast`。
- `experiments/tasks/negotiation.py`: 商业谈判任务模拟。
- `experiments/baselines.py`: 基线实现（ZeroShot / Broadcast）。
- `experiments/metrics.py`: 指标函数：成功率、信息泄露率、谈判效率。

快速运行示例：
```bash
python -m experiments.runner --agent weaver
python -m experiments.runner --agent zero_shot
python -m experiments.runner --agent broadcast
```
默认配置下（离线 Fake LLM 回退示例输出）可见：
- Weaver: 较高成功率、低泄露
- Broadcast: 高泄露，成功率低
- ZeroShot: 中等表现，常泄露私密区间

生成结果写入 `experiments/out/results_<agent>.json`，便于后续论文数据统计。