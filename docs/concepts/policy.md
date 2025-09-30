# Policy

`Policy` 将“角色 + 原则”显式建模为结构化数据，并生成系统提示：

```python
from weaver.runtime.policy import MediationPolicy
print(MediationPolicy.default().format_system_prompt())
```

扩展策略：继承 `BasePolicy`，添加字段并重写 `format_system_prompt()`。

设计要点：
* 明确语气与边界
* 强调价值观而非硬指令
* 保持可组合（不同场景可复用原则子集）
