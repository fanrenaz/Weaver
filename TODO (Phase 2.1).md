#### **Phase 2.1: 运行时提炼与框架化 (Runtime Refinement & Frameworkization)**

*目标：将Demo脚本中的“临时L3逻辑”正式化，创建`WeaverRuntime`和`Policy`对象，让框架的API变得声明式和优雅。*

**TODO LIST:**

- [ ] **1. 设计并实现 `Policy` 类**
    - [ ] 在`src/weaver/runtime/policy.py`中，创建一个`BasePolicy`抽象类（或Pydantic `BaseModel`）。
    - [ ] 它至少应包含`role: str`和`principles: List[str]`等字段。
    - [ ] 创建`MediationPolicy`作为其具体实现。
    - [ ] **关键**: 为`Policy`类添加一个`format_system_prompt()`方法，它能根据`role`和`principles`生成我们在`_agent_node`中使用的那个系统Prompt。

- [ ] **2. 设计并实现 `MemoryCoordinator` (初版)**
    - [ ] 在`src/weaver/runtime/coordinator.py`中，创建`MemoryCoordinator`类。
    - [ ] **关键**: 实现一个`prepare_context(space_id: str, current_user_id: str) -> List[BaseMessage]`方法。在v0.1中，它的逻辑可以很简单：根据`Policy`，如果需要“上帝视角”，就从`session_store`中获取并合并所有相关用户的历史记录。
    - *这将是我们“多视角记忆”创新的第一次代码化实现。*

- [ ] **3. 设计并实现 `WeaverRuntime`**
    - [ ] 在`src/weaver/runtime/runtime.py`中，创建核心的`WeaverRuntime`类。
    - [ ] `__init__`方法接收一个`Policy`对象和一个`WeaverGraph`实例。
    - [ ] **关键**: 实现一个`invoke(space_id: str, event: UserMessageEvent)`方法。这个方法将编排整个流程：
        1.  调用`MemoryCoordinator`准备上下文。
        2.  调用核心`WeaverGraph`执行思考。
        3.  （未来）调用`Policy`进行后处理。
        4.  更新记忆。

- [ ] **4. 重构Demo脚本，迎接新API**
    - [ ] 再次重构`financial_counseling.py`。
    - [ ] 现在，它应该极其简单：
        ```python
        from weaver.runtime import WeaverRuntime, MediationPolicy
        
        # 1. 创建策略
        policy = MediationPolicy(...)
        # 2. 创建运行时
        runtime = WeaverRuntime(policy=policy)
        # 3. 驱动对话
        event = UserMessageEvent(user_id="jane", content="...")
        response = runtime.invoke(space_id="counseling_123", event=event)
        print(response)
        ```
    - **验收标准**: 新的Demo脚本能以更少的代码、更声明式的方式，复现和Phase 1.3完全一样的结果。

完成后更新README记录。