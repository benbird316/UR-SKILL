"""校验器共享基础设施。

提供 SKILL.md 解析、上下文对象、发现项格式与报告输出。
"""

from __future__ import annotations

import json
import re
from dataclasses import dataclass, field
from pathlib import Path
from typing import Any, Callable

try:
    import yaml  # type: ignore

    HAS_YAML = True
except ImportError:  # pragma: no cover
    HAS_YAML = False


@dataclass
class Finding:
    """单个校验发现项。"""

    rule: str
    message: str
    severity: str = "error"  # error / warning / info
    line: int | None = None

    def to_dict(self) -> dict[str, Any]:
        return {
            "rule": self.rule,
            "message": self.message,
            "severity": self.severity,
            "line": self.line,
        }


@dataclass
class SkillContext:
    """SKILL.md 校验上下文。"""

    text: str
    path: Path
    config: dict[str, Any]
    lines: list[str] = field(init=False)
    frontmatter: dict[str, Any] = field(init=False)
    body: str = field(init=False)
    fm_parse_errors: list[str] = field(init=False)

    def __post_init__(self) -> None:
        self.lines = self.text.splitlines()
        self.frontmatter, self.body, self.fm_parse_errors = self._parse_frontmatter()

    def _parse_frontmatter(self) -> tuple[dict[str, Any], str, list[str]]:
        errors: list[str] = []
        if not self.text.startswith("---"):
            errors.append(self._msg("missing_frontmatter_delimiter"))
            return {}, self.text, errors

        parts = self.text.split("---", 2)
        if len(parts) < 3:
            errors.append(self._msg("missing_frontmatter_end"))
            return {}, self.text, errors

        fm_text = parts[1].strip()
        body = parts[2].strip()

        if not HAS_YAML:
            errors.append(self._msg("pyyaml_missing"))
            return {}, body, errors

        try:
            fm_data = yaml.safe_load(fm_text) or {}
        except yaml.YAMLError as exc:
            errors.append(self._msg("frontmatter_yaml_error").format(error=exc))
            return {}, body, errors

        return fm_data, body, errors

    def _msg(self, key: str) -> str:
        return self.config.get("messages", {}).get(key, key)

    def run(self, validator: Callable[[SkillContext, dict[str, Any]], list[Finding]]) -> list[Finding]:
        return validator(self, self.config)

    @property
    def skill_dir(self) -> Path:
        return self.path.parent


class Report:
    """校验报告。"""

    def __init__(self, findings: list[Finding], config: dict[str, Any]):
        self.findings = findings
        self.config = config

    @property
    def has_error(self) -> bool:
        return any(f.severity == "error" for f in self.findings)

    def to_json(self) -> str:
        return json.dumps([f.to_dict() for f in self.findings], ensure_ascii=False, indent=2)

    def to_text(self) -> str:
        msgs = self.config.get("messages", {})
        errors_warnings = [f for f in self.findings if f.severity in ("error", "warning")]
        infos = [f for f in self.findings if f.severity == "info"]

        if not errors_warnings and not infos:
            return msgs.get("validation_passed", "Validation passed")

        lines = []
        if errors_warnings:
            lines.append(msgs.get("validation_failed", "Validation failed").format(count=len(errors_warnings)))
            lines.append("")
        for idx, finding in enumerate(errors_warnings, 1):
            prefix = f"[{finding.severity.upper()}]"
            line_info = f" (L{finding.line})" if finding.line else ""
            lines.append(f"{idx}. {prefix}{line_info} {finding.message}")

        if infos:
            if errors_warnings:
                lines.append("")
            for finding in infos:
                lines.append(f"[{finding.severity.upper()}] {finding.message}")

        return "\n".join(lines)


def strip_code_blocks(text: str) -> str:
    """移除 Markdown 代码块内容，避免示例中的模式触发误报。"""
    return re.sub(r"```[\s\S]*?```", "", text)
