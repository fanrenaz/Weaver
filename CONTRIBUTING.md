# 贡献指南 (Contributing)

欢迎加入 Weaver！

## 提交 Issue
提供：复现步骤 / 期望行为 / 实际结果 / 环境信息。

## 提交 Pull Request
1. Fork & 创建特性分支
2. 保持提交粒度清晰
3. 添加/更新测试
4. 通过本地 `ruff`, `black --check`, `pytest`
5. 描述动机与变更影响

## 开发脚本
```bash
pip install -e .[dev]
pytest -q
```

## 标签约定
| 标签 | 用途 |
|------|------|
| good first issue | 适合新人入门的小改动 |
| enhancement | 新功能或改进 |
| bug | 缺陷修复 |
| docs | 文档相关 |

## 行为准则
保持尊重、聚焦建设性讨论。违反者将被维护者警告或移除参与资格。

---
感谢你的贡献！
