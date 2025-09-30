# Space & Runtime

`WeaverRuntime` 是一个高层编排器：输入事件 -> 组装上下文 -> 调用 LangGraph -> 写回记忆。

最小交互：

```python
from weaver.runtime.policy import MediationPolicy
from weaver.runtime.runtime import WeaverRuntime
from weaver.models.events import UserMessageEvent

rt = WeaverRuntime(MediationPolicy.default())
rt.invoke("room42", UserMessageEvent(user_id="u1", content="hello"))
```

核心阶段：
1. prepare_context (MemoryCoordinator)
2. system prompt 注入 (来自 Policy)
3. LangGraph ReAct 循环 (agent + tools)
4. 结果持久化

未来的 Space 抽象将：
* 追踪参与者 / 权限
* 暴露事件流订阅接口
* 支持私域 + 公域混合上下文投影
