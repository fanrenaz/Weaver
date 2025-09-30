#### **Phase 1.3: 最终集成与演示 (Final Integration & Demonstration)**

*目标：通过引入“适配器”层，实现与`RunnableWithMessageHistory`的优雅集成，并完成最终的、可展示的“杀手级Demo”。*

- [ ] **1. 创建适配器Runnable**
    - [ ] 在 `src/weaver/core/graph.py` 中，或者一个新文件 `src/weaver/core/chains.py` 中，创建一个名为 `create_state_adapter_runnable` 的函数。
    - [ ] 这个函数内部，使用 `@chain` 装饰器或 `RunnableLambda` 来实现我们上述讨论的适配器逻辑：接收字典 -> 创建并返回 `SpaceState`。
    - [ ] 确保这个Runnable有正确的输入和输出类型注解（`Dict -> SpaceState`）。

- [ ] **2. 组装最终的可执行链**
    - [ ] 在你的`WeaverGraph`类之外（或者在一个新的工厂函数中），使用LCEL将适配器和核心图连接起来。
      ```python
      # in graph.py or chains.py
      from .graph import WeaverGraph
      
      def create_weaver_chain():
          adapter = create_state_adapter_runnable()
          core_graph = WeaverGraph().app
          return adapter | core_graph
      ```

- [ ] **3. 重构Demo脚本 (`examples/cli_demo/financial_counseling.py`)**
    - [ ] **移除所有手动管理history的代码。** 这是关键！
    - [ ] 从你的新模块中导入`create_weaver_chain`，并调用它来获取最终的、兼容的`chain`。
    - [ ] 定义`get_session_history`函数和`session_store`字典（这部分逻辑不变）。
    - [ ] 使用`RunnableWithMessageHistory`来包装你新创建的`chain`。
    - [ ] **验证**:
        - [ ] 使用**不同**的`session_id`来模拟Jane和John的对话，验证历史记录是**隔离**的。
        - [ ] 使用**相同**的`session_id`，验证“上帝视角”的模拟是成功的，并且多轮对话的上下文是正确累积的。
        - [ ] 运行完整的“夫妻财务咨询”剧本，确保最终输出与白皮书完全一致。

- [ ] **4. （可选）代码清理与文档更新**
    - [ ] 为你新创建的适配器和链工厂函数添加清晰的文档字符串，解释它们为什么存在。
    - [ ] 更新 `README.md` 或相关文档，说明Weaver现在已经实现了与LangChain标准记忆组件的完全集成。