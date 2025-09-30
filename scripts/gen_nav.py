"""MkDocs gen-files hook to auto build an index or future aggregated pages.

Currently minimal: can be extended to scan modules or generate changelog.
Placed under scripts/ and invoked implicitly by mkdocs-gen-files plugin.
"""
from __future__ import annotations

from pathlib import Path
import textwrap

try:
    from mkdocs_gen_files import open as gen_open  # type: ignore
except Exception:  # pragma: no cover
    raise SystemExit("mkdocs-gen-files not available during build")

root = Path(__file__).parent.parent / "docs"

# Example: Generate an aggregated simple index for legacy docs
legacy = root / "legacy"
if legacy.exists():
    legacy_files = [p.name for p in legacy.glob("*.md")]
    content = "\n".join(f"- [{name}](legacy/{name})" for name in sorted(legacy_files))
    with gen_open("legacy/_index.md", "w") as f:  # type: ignore
        f.write("# 归档文档索引\n\n" + content + "\n")

# Placeholder for future dynamic API index (e.g., auto enumerating packages)
with gen_open("reference/_auto_index.md", "w") as f:  # type: ignore
    f.write(textwrap.dedent(
        """
        # 自动索引 (预留)

        该页面由 gen_nav.py 自动生成，将来可扩展为：
        * 动态列出所有模块
        * 根据 docstring 标签组织章节
        * 生成按层次分组的 API 入口
        """
    ))
