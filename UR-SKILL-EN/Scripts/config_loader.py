"""配置加载器。

根据 --lang 参数加载对应的 config.{lang}.yaml。
"""

from __future__ import annotations

from pathlib import Path
from typing import Any

try:
    import yaml  # type: ignore
except ImportError:  # pragma: no cover
    raise SystemExit("PyYAML is required. Run: pip install pyyaml") from None


def load_config(lang: str, scripts_dir: Path) -> dict[str, Any]:
    """加载指定语言的配置，回退到默认 config.yaml。"""
    candidates = [
        scripts_dir / f"config.{lang}.yaml",
        scripts_dir / "config.yaml",
    ]
    for path in candidates:
        if path.exists():
            with path.open("r", encoding="utf-8") as f:
                return yaml.safe_load(f) or {}
    raise FileNotFoundError(f"No config found for lang={lang} in {scripts_dir}")
