### **Weaver 项目核心工程架构蓝图 (Master Blueprint)**

**版本: 1.0**

#### **1. 哲学与指导原则**

本架构遵循“**分层与解耦**”的核心思想，将Weaver系统划分为四个逻辑层次。每一层都有清晰的职责，并通过定义良好的接口与相邻层交互。这种设计旨在实现高内聚、低耦合，确保框架的模块化、可测试性和未来可扩展性。

*   **上层**专注于“**业务与策略 (What & Why)**”，定义协作的规则和目标。
*   **下层**专注于“**能力与执行 (How)**”，提供通用的、可复用的基础能力。
*   **Weaver的核心创新**体现在中间的“**运行时/编排层**”，它作为“神经系统”，连接了上层的策略和下层的能力。

#### **2. 分层架构图 (The Layered Architecture)**

```
+-------------------------------------------------------------+
|    Layer 4: 应用/API层 (Application/API Layer)              |
|  [创新区]                                                   |
|  职责：对外暴露接口，管理Space生命周期。                    |
|  示例：FastAPI Server, WebSocket Gateway, CLI Interface     |
+-------------------------------------------------------------+
                        | (调用)
                        v
+-------------------------------------------------------------+
|    Layer 3: 运行时/编排层 (Runtime & Orchestration Layer)   |
|  [创新区 - Weaver的灵魂]                                    |
|  职责：编排完整的协作流程，执行策略，协调记忆。             |
|  核心组件：WeaverRuntime, Space, Policy, MemoryCoordinator  |
+-------------------------------------------------------------+
                        | (委托)
                        v
+-------------------------------------------------------------+
|    Layer 2: AI核心能力层 (Core AI Capability Layer)         |
|  [复用区]                                                   |
|  职责：提供核心的推理、规划和工具使用能力。                 |
|  核心组件：LangGraph (执行引擎), Agent (推理核心)           |
+-------------------------------------------------------------+
                        | (使用)
                        v
+-------------------------------------------------------------+
|    Layer 1: 基础设施/集成层 (Infrastructure & Integration Layer)|
|  [复用区]                                                   |
|  职责：与外部世界交互，提供基础构建块。                     |
|  核心组件：LLM Clients, Tool Definitions, Memory Backends   |
+-------------------------------------------------------------+
```

---

#### **3. 各层详细设计与边界定义**

##### **Layer 1: 基础设施/集成层 (The "Plumbing")**

*   **职责**: 提供所有基础的、可插拔的构建块。这是Weaver与外部世界（LLMs, 数据库, API）的连接点。
*   **实现**: **完全复用** LangChain 生态。
    *   **LLM客户端**: 通过`langchain_openai`, `langchain_anthropic`等库与模型服务交互。
    *   **工具定义**: 使用`@tool`装饰器将任意Python函数封装为Agent可用的工具。
    *   **记忆后端**: 使用`ChatMessageHistory`及其各种数据库实现 (`RedisChatMessageHistory`, `SQLChatMessageHistory`等)，作为最底层的持久化单元。
*   **边界**: 这一层**不包含任何与“协作”相关的逻辑**。它只提供原子化的能力。

##### **Layer 2: AI核心能力层 (The "Engine")**

*   **职责**: 提供一个能“思考”和“行动”的大脑。这个大脑接收上下文，进行推理，并决定要采取的行动（直接回复或调用工具）。
*   **实现**: **主要复用** LangGraph。
    *   **执行引擎**: `langgraph.graph.StateGraph`。我们用它来构建一个标准的ReAct（思考-行动-观察）循环。这个图的结构在项目初期会比较固定。
    - **推理核心**: 一个由`ChatPromptTemplate`和绑定了工具的`ChatLLM`组成的`Runnable`。它构成了图中的`agent`节点。
*   **边界**: 这一层**不关心上下文从何而来，也不关心行动的结果如何被分发**。它是一个纯粹的“信息处理单元”，接收输入，产生决策。

##### **Layer 3: 运行时/编排层 (The "Nervous System" - Weaver's Core Innovation)**

*   **职责**: 这是Weaver的**核心创新所在**。它作为“总指挥”，编排L1和L2的能力，以实现L4定义的协作目标。
*   **实现**: **完全由我们自己原创设计和编码**。
    *   **`Space` 对象**: 一个高级API对象，封装了特定协作会话的所有配置（参与者、`Policy`等）和状态。
    *   **`Policy` 对象**: 一个可插拔的、包含规则和高级原则的模块。它在编排流程的关键节点（pre/post processing）被调用。
    *   **`MemoryCoordinator`**: 负责实现复杂的多视角记忆逻辑。它调用L1的`ChatMessageHistory`实例，但其自身的组合和预处理逻辑是原创的。
    *   **`WeaverRuntime`**: 核心的流程控制器。它接收来自L4的事件，驱动整个L3的编排逻辑：调用`MemoryCoordinator`准备上下文 -> 调用`PolicyEngine`进行预处理 -> 委托L2的`Graph`进行思考 -> 调用`PolicyEngine`进行后处理 -> 解析结果并更新`Memory`。
*   **边界**: 这一层是**Weaver的“私有API”和内部逻辑**。它定义了Weaver如何区别于其他框架。

##### **Layer 4: 应用/API层 (The "User Interface")**

*   **职责**: 作为Weaver与最终用户或外部系统交互的“门面”。它将Weaver的核心能力暴露为易于使用的接口。
*   **实现**: **可以是我们自己编写，也可以由框架使用者自行实现**。
    *   **v0.1阶段**: 可以是一个简单的`main`函数或`examples`下的脚本。
    *   **v1.0阶段**: 我们可以提供一个基于`FastAPI`的参考实现，暴露RESTful或WebSocket API。
    *   **未来**: 其他开发者可以使用`Gradio`, `Streamlit`或他们自己的Web后端来构建这一层。
*   **边界**: 这一层**不应包含任何核心的协作逻辑**，它只负责I/O和与`WeaverRuntime`的交互。

#### **Weaver 项目推荐目录结构 (v2.0)**

这个结构旨在将**不同层次的关注点**在物理上分离开来。

```
/weaver-project/
├── .git/
├── .venv/
├── docs/                   # 存放所有设计文档、白皮书、未来教程等
│   ├── a_master_blueprint.md  # 我们的核心工程蓝图
│   └── whitepaper_v1.md       # 我们的白皮书
│
├── examples/               # L4: 应用层的示例实现
│   ├── cli_demo/
│   │   └── financial_counseling.py  # Phase 1.2 的命令行"杀手级Demo"
│   └── api_server/          # (未来) FastAPI等Web服务示例
│       └── main.py
│
├── src/
│   └── weaver/             # 项目的核心源码包
│       ├── __init__.py     # 让weaver成为一个包
│       │
│       ├── runtime/        # L3: 运行时/编排层 (Weaver的核心创新)
│       │   ├── __init__.py
│       │   ├── space.py      # 定义Space对象和其生命周期管理
│       │   ├── policy.py     # 定义BasePolicy和具体的策略实现 (MediationPolicy)
│       │   ├── coordinator.py# 定义MemoryCoordinator
│       │   └── runtime.py    # 定义核心的WeaverRuntime流程控制器
│       │
│       ├── core/           # L2: AI核心能力层
│       │   ├── __init__.py
│       │   └── graph.py      # 我们基于LangGraph构建的核心Agent图 (即之前的core.py)
│       │
│       ├── building_blocks/  # L1: 基础设施/集成层的自定义部分
│       │   ├── __init__.py
│       │   ├── tools.py      # 定义所有用@tool装饰的工具函数
│       │   └── memory.py     # (如果需要) 自定义的ChatMessageHistory后端或管理逻辑
│       │
│       └── models/           # 跨层共享的数据模型
│           ├── __init__.py
│           ├── actions.py    # 定义所有Action Pydantic模型
│           ├── events.py     # 定义所有Event Pydantic模型
│           └── state.py      # 定义LangGraph使用的State TypedDict
│
├── tests/                  # 各个模块的单元测试和集成测试
│   ├── runtime/
│   ├── core/
│   └── building_blocks/
│
├── .gitignore
├── pyproject.toml
└── README.md               # 项目的入口介绍，可以是白皮书的精简版
```