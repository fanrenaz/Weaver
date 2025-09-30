### **Phase 1.2: 核心原型切片实现 (Core Prototype Slice)**

- [ ] **1. L1 & Models: 定义基础构建块和数据结构**
    - [ ] **`src/weaver/models/`**:
        - [ ] 在 `actions.py` 中定义 `ReplyPrivateAction`, `PostToSharedAction` 等Pydantic模型。
        - [ ] 在 `events.py` 中定义 `UserMessageEvent` Pydantic模型。
        - [ ] 在 `state.py` 中定义 `SpaceState` TypedDict（包含`input`, `action_to_execute`等）。
    - [ ] **`src/weaver/building_blocks/tools.py`**:
        - [ ] 使用 `@tool` 装饰器定义 `reply_privately` 和 `post_to_shared` 两个工具函数（实现暂时只需`print`）。
    - [ ] 提交 L1 和模型层: `git commit -m "Feat(L1,Models): Define data models and tool building blocks"`

- [ ] **2. L2: 实现核心Agent图**
    - [ ] **`src/weaver/core/graph.py`**:
        - [ ] 创建 `WeaverGraph` 类。
        - [ ] 在类中，导入`tools.py`中定义的工具。
        - [ ] 实现 `_agent_node`，它将使用绑定了这些工具的LLM进行决策。
        - [ ] 在 `_build_graph` 方法中，使用`ToolNode`和条件路由，构建标准的ReAct循环图。
        - [ ] 编译图并将其作为类的公共属性（如 `self.app`）。
    - [ ] 提交 L2 核心图: `git commit -m "Feat(L2): Implement core agent graph with ReAct loop"`

- [ ] **3. L4 & L3 (临时实现): 编写并运行Demo脚本**
    - [ ] **`examples/cli_demo/financial_counseling.py`**:
        - [ ] **作为临时的 L3 (Runtime)**: 在这个脚本的顶部，临时实现 `get_session_history` 逻辑和 `session_store` 字典。
        - [ ] **作为 L4 (Application)**: 编写主函数，负责：
            1.  实例化 `WeaverGraph`。
            2.  使用 `RunnableWithMessageHistory` 包装核心图 `app`。
            3.  按顺序模拟 “夫妻财务咨询” 的多回合对话。
            4.  在每次调用时，构造 `UserMessageEvent`，并传入正确的 `session_id` 到 `config` 中。
            5.  打印每次调用的结果，并验证其是否符合白皮书中的预期。
    - [ ] 提交 L4/L3 Demo实现: `git commit -m "Feat(L3,L4): Implement and run financial counseling demo script"`

### **技术规范文档 v3.0：Weaver Phase 1.2 - 核心原型切片实现**

**版本：1.0**
**生效日期：[当前日期]**

#### **1. 总体指导原则**

*   **单一职责原则**: 每个文件、每个类、每个函数都应只做一件事，并把它做好。
*   **自下而上构建**: 遵循 `L1 & Models -> L2 -> L4/L3` 的顺序进行开发，确保底层稳定后再构建上层。
*   **接口而非实现**: 模块间的交互应尽可能通过稳定的接口（如函数签名、Pydantic模型）进行，而不是依赖具体的实现细节。
*   **拥抱类型提示**: 100%的代码覆盖率。所有函数参数、返回值和重要变量都必须有明确的类型注解。
*   **日志优于`print`**: 在核心库代码 (`src/weaver/`) 中，使用Python的`logging`模块进行信息输出，而不是`print()`。这便于未来进行日志级别控制和管理。`print()`只应用于`examples/`目录下的演示脚本。

---

#### **2. `L1 & Models` 开发规范**

##### **2.1 `src/weaver/models/` 目录**

*   **文件职责**:
    *   `actions.py`: **只**定义Agent可以执行的动作（`Action`）的Pydantic模型。
    *   `events.py`: **只**定义外部输入的事件（`Event`）的Pydantic模型。
    *   `state.py`: **只**定义LangGraph内部使用的`State` TypedDict。
*   **Pydantic V2 规范**:
    *   所有模型**必须**继承自 `pydantic.BaseModel`。
    *   **必须**使用`Field(description="...")`为所有字段添加文档。
    *   推荐使用`Literal`来定义有固定值的字段，如`type`。
*   **`state.py` 规范**:
    *   `SpaceState` **必须**继承自 `typing.TypedDict`。
    - 字段**必须**与最终架构保持一致：`input: List[BaseMessage]`, `action_to_execute: Optional[Any]`, `tool_output: Optional[str]` 等。
    *   对于需要在Graph运行中累积的列表（如中间步骤），**必须**使用`Annotated[List[...], operator.add]`。

##### **2.2 `src/weaver/building_blocks/tools.py` 目录**

*   **工具定义**:
    *   所有工具函数**必须**使用`@tool`装饰器（从`langchain_core.tools`导入）。
    *   每个工具函数的**docstring**至关重要，它将直接被LLM用作工具的功能描述。docstring**必须**清晰、准确地描述该工具做什么、需要什么参数。
    *   函数签名中的参数**必须**有明确的类型注解，例如 `recipient: str, content: str`。LangChain会利用这些注解进行参数解析。
*   **工具实现 (Phase 1.2)**:
    *   在此阶段，工具的实现**应该**尽可能简单。
    *   **必须**使用`logging.info()`或`logging.debug()`来输出执行信息，例如`logging.info(f"Executing reply_privately to {recipient}")`。
    *   函数的返回值**应该**是一个简单的、描述执行结果的字符串，例如`"Private message has been sent successfully."`。这个返回值将被送回给Agent，作为它的“观察”结果。

---

#### **3. `L2` 开发规范 (`src/weaver/core/graph.py`)**

*   **`WeaverGraph` 类**:
    *   **必须**只负责构建和编译`StateGraph`。不应包含任何业务逻辑或状态。
    *   `__init__`中初始化的`ChatOpenAI`实例**必须**从环境变量中读取配置（`api_base`, `api_key`等），以保持可移植性。
*   **`_agent_node` 方法**:
    *   **Prompt**: 系统Prompt应作为一个独立的、定义在文件顶部的`SYSTEM_PROMPT`常量，内容与白皮书中的“调解员”角色和原则保持一致。
    - **工具绑定**: **必须**使用`llm.bind_tools(tools)`方法，其中`tools`是从`tools.py`导入的工具列表。
    - **逻辑**: 此节点的核心逻辑是将`state['input']`和绑定的LLM组合成`Runnable`并调用。
    - **输出解析**: Agent的输出是一个`AIMessage`对象，其`.tool_calls`属性包含了需要执行的工具调用。此节点需要解析`.tool_calls`，并将其（或`None`）放入返回字典的`action_to_execute`键中。
*   **`_should_continue_node` (条件路由)**:
    *   这是一个独立的函数，不属于`WeaverGraph`类。
    - **必须**接收`state: SpaceState`作为参数。
    - **必须**检查`state.get("action_to_execute")`是否为空或列表为空。
        *   如果不为空，返回`"tools"`。
        *   如果为空，返回`"end"`。
*   **图的构建 (`_build_graph`方法)**:
    *   **必须**实例化`ToolNode`：`tool_node = ToolNode(tools)`。
    *   **必须**严格遵循`agent -> conditional_router -> (tools | end)`的逻辑。
    *   `tools`节点的输出**必须**连回到`agent`节点，以形成ReAct循环。`workflow.add_edge("tools", "agent")`。

---

#### **4. `L4 & L3 (临时)` 开发规范 (`examples/cli_demo/financial_counseling.py`)**

*   **职责清晰**: 这个脚本虽然是临时的，但也要有清晰的职责划分。
    *   **顶部区域 (L3模拟)**: 定义`session_store`字典和`get_session_history`函数。这部分逻辑未来将被迁移到`src/weaver/runtime/`。
    *   **主函数区域 (L4实现)**: 负责模拟完整的用户交互流程。
*   **`RunnableWithMessageHistory`的使用**:
    *   **必须**使用它来包装`WeaverGraph().app`。
    *   **必须**正确配置`input_messages_key`和`history_messages_key`，使其与`SpaceState`的定义匹配。
*   **交互模拟**:
    - **必须**定义一个`run_turn`之类的辅助函数，它接收`app_with_history`, `session_id`, 和用户输入的`content`，然后负责构造输入字典、调用`.invoke()`并打印结果。这能让主流程代码更清晰。
    - 模拟的对话**必须**与白皮书v3版本中的多回合流程完全一致，以达到最佳的演示效果。
    - **必须**在每次调用时都传入正确的`config={"configurable": {"session_id": ...}}`。