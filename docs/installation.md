# 安装 (Installation)

当前版本尚未发布到 PyPI，你可以预先假设未来安装方式：

```bash
pip install weaver-ai
```

在源码模式下 (editable)：

```bash
git clone https://github.com/fanrenaz/Weaver.git
cd Weaver
pip install -e .[dev]
```

## 环境变量配置

创建一个 `.env` 文件（可复制下面模板为 `.env.example`）：

```dotenv
# LLM 基础配置
OPENAI_API_KEY=sk-xxx               # 真实 Key 或留空使用 Fake LLM 回退
# OPENAI_API_BASE=https://api.openai.com/v1  # 可选: 自定义 API Base

# Weaver 运行时
WEAVER_MODEL=gpt-4o-mini            # 或任意兼容模型名
LOG_LEVEL=INFO
```

如果不提供 `OPENAI_API_KEY`，Weaver 会自动使用内置的 Fake LLM，保证开发/测试不受阻塞。

## 快速验证

```bash
python examples/cli_demo/financial_counseling.py
```

如需最低可行试运行：

```bash
python - <<'PY'
from weaver.runtime.policy import MediationPolicy
from weaver.runtime.runtime import WeaverRuntime
from weaver.models.events import UserMessageEvent

rt = WeaverRuntime(MediationPolicy.default())
r = rt.invoke("demo_space", UserMessageEvent(user_id="u1", content="我们需要一个预算方案"))
print(r)
PY
```

---
问题反馈请提交 GitHub Issue。
