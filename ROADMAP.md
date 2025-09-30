# Weaver 项目开发路线图 (ROADMAP)

本文档追踪 Weaver 项目从概念到成熟的开发步骤。请按照阶段顺序完成任务。

---

##  Phase 0: 奠基与设计 (Foundation & Design)

*目标：完成所有前期思考和设计工作，为编码做好充分准备。*

- [x] ~~**项目命名与愿景确立**：确定项目代号为 `Weaver`，明确其“协作谐和者”的核心愿景。~~
- [x] ~~**核心价值主张提炼**：完成“电梯演讲”，定义项目的独特性。~~
- [x. ] ~~**“魔法时刻”场景设计**：构思并打磨出“夫妻财务咨询”这个核心演示场景。~~
- [x] ~~**项目定位与比较分析**：明确与LangChain等框架的正交互补关系。~~
- [x] ~~**撰写并最终确定白皮书 v1.0**：完成一份完整的、可作为项目“宪法”的Markdown文档。~~

---

## Phase 1: 核心原型冲刺 (Core Prototype Sprint)

*目标：构建一个最小但完整的内部原型，用于验证核心思想和支撑未来实验。**此阶段不追求代码的通用性和完美性。** (预计时间: 2-3个月)*

### 1.1 环境与脚手架搭建 (Setup & Scaffolding)

- [ ] **创建Git仓库和项目结构**:
    - [ ] 初始化 `git` 仓库。
    - [ ] 创建 `src/weaver/`, `examples/`, `tests/` 等目录结构。
    - [ ] 将白皮书内容复制到 `README.md`。
- [ ] **配置开发环境**:
    - [ ] 创建并激活Python虚拟环境 (e.g., `.venv`)。
    - [ ] 创建 `pyproject.toml` 文件。
    - [ ] 安装第一批核心依赖: `langchain`, `langgraph`, `openai`, `pydantic`, `python-dotenv`。
    - [ ] 安装开发依赖: `pytest`, `ruff`, `black`。
- [ ] **运行 "Hello, Graph!"**:
    - [ ] 在 `examples/` 目录下创建一个简单的LangGraph示例（可从官方文档复制），确保整个环境和依赖能正常工作。

### **Phase 1.2 (重制版): 核心原型切片实现 (Core Prototype Slice)**

*目标：遵循新架构，自下而上地实现第一个完整的、驱动“杀手级Demo”的垂直功能切片。*

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

### 1.3 “杀手级Demo”脚本 (The Killer Demo)

- [ ] **编写Demo脚本 (`examples/financial_counseling_demo.py`)**:
    - [ ] 实例化核心 `graph` 和 `MemoryManager`。
    - [ ] **模拟回合一**: 模拟Jane发送私密消息，调用 `graph.stream()`，并验证AI对Jane的私密回复是否符合预期。
    - [ ] **模拟回合二**: 模拟John发送无关的私密消息，再次调用 `graph.stream()`，并验证AI对John的“思想植入”式回复是否如白皮书中所述。
    - [ ] **模拟回合三**: 模拟John在公开场合发起新话题，验证AI的公开引导回复。
    - [ ] *目标：让这个脚本的输出与白皮书中的对话示例完全一致。*

---

## Phase 2: 学术研究与论文撰写 (Research & Paper)

*目标：将原型提升为科学实验，并撰写一篇达到顶会标准的学术论文。 (预计时间: 1-2个月)*

- [ ] **设计实验环境与任务**:
    - [ ] 实现“商业谈判”和“囚徒困境”等模拟环境。
    - [ ] 编码实现用于对比的基线模型 (Zero-shot, Broadcast Agent等)。
- [ ] **定义并实现评估指标**:
    - [ ] 编写用于计算“任务成功率”、“信息泄露率”等的评测函数。
- [ ] **执行大规模实验**:
    - [ ] 运行数千次模拟，收集实验数据。
    - [ ] 进行消融研究和参数敏感性分析。
- [ ] **撰写论文**:
    - [ ] 完成论文的初稿，包含模型形式化、实验设置、结果分析和结论。
    - [ ] 提交到ArXiv，并根据目标会议的DDL进行投稿。

---

## Phase 3: 开源发布与社区启动 (Open Source & Community)

*目标：将经过验证和打磨的项目，作为一个高质量的开源产品发布给世界。 (预计时间: 长期)*

- [ ] **API重构与SDK打包**:
    - [ ] 将硬编码的逻辑（如Policy）抽象为可配置的类。
    - [ ] 优化API，使其更通用和优雅。
    - [ ] 将项目打包并发布到PyPI。
- [ ] **完善开发者文档**:
    - [ ] 撰写详细的安装指南、快速入门教程和API参考。
    *   为核心概念（Space, Policy）编写深入的解释文档。
- [ ] **启动社区**:
    *   创建Discord/Slack频道。
    *   撰写并发布项目启动的技术博客。
    *   在GitHub上建立清晰的`CONTRIBUTING.md`和Issue模板。

---