"""格式层校验器。

负责 frontmatter、body 行数、占位符、未填充模板占位符、已废弃工具名。
"""

from __future__ import annotations

import json
import re
from pathlib import Path
from typing import Any

from common import Finding, SkillContext, strip_code_blocks

# jsonschema 为可选依赖，未安装时跳过 JSON Schema 校验
try:
    import jsonschema  # noqa: F401
    _HAS_JSONSCHEMA = True
except ImportError:
    _HAS_JSONSCHEMA = False
    import sys
    print("[WARNING] jsonschema not installed — JSON Schema validation will be skipped. "
          "Install with: pip install jsonschema", file=sys.stderr)


def validate(ctx: SkillContext, config: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    findings.extend(_validate_frontmatter(ctx, config))
    findings.extend(_validate_body(ctx, config))
    findings.extend(_validate_unresolved_placeholders(ctx, config))
    findings.extend(_validate_deprecated_tools(ctx, config))
    findings.extend(_validate_json_schema(ctx))
    return findings


def _validate_frontmatter(ctx: SkillContext, config: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    fm = ctx.frontmatter
    msgs = config.get("messages", {})
    fm_cfg = config.get("frontmatter", {})

    required = fm_cfg.get("required_fields", {})
    for field, expected_type in required.items():
        if field not in fm:
            findings.append(Finding("missing-frontmatter-field", msgs["frontmatter_missing_field"].format(field=field), "error"))
            continue
        if expected_type == "dict":
            if not isinstance(fm[field], dict):
                findings.append(Finding("frontmatter-type-error", msgs["frontmatter_dict_required"].format(field=field), "error"))
            continue
        py_type = {"str": str, "int": int, "bool": bool}.get(expected_type, str)
        if not isinstance(fm[field], py_type):
            findings.append(Finding("frontmatter-type-error", msgs["frontmatter_wrong_type"].format(field=field, expected=expected_type), "error"))

    if "name" in fm:
        name = fm["name"]
        if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", name):
            findings.append(Finding("name-not-kebab", msgs["name_not_kebab"].format(name=name), "error"))

    thresholds = config.get("thresholds", {})
    min_desc = thresholds.get("min_description_chars", 50)
    max_desc = thresholds.get("max_description_chars", 200)

    if "description" in fm:
        desc = fm["description"]
        if isinstance(desc, str) and (len(desc) < min_desc or len(desc) > max_desc):
            findings.append(Finding("description-length", msgs["description_length"].format(length=len(desc), min=min_desc, max=max_desc), "error"))

    if isinstance(fm.get("metadata"), dict):
        updated = fm["metadata"].get("updated")
        if fm_cfg.get("metadata", {}).get("updated_required", True) and not updated:
            findings.append(Finding("metadata-updated-missing", msgs["metadata_updated_missing"], "error"))
        elif updated:
            fmt = fm_cfg.get("metadata", {}).get("updated_format", "%Y-%m-%d")
            try:
                from datetime import datetime
                datetime.strptime(str(updated), fmt)
            except ValueError:
                findings.append(Finding("metadata-updated-format", msgs["metadata_updated_format"].format(updated=updated), "error"))

    return findings


def _validate_body(ctx: SkillContext, config: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    body = ctx.body
    msgs = config.get("messages", {})
    thresholds = config.get("thresholds", {})

    lines = body.splitlines()
    max_lines = thresholds.get("max_body_lines", 500)
    if len(lines) > max_lines:
        findings.append(Finding("body-too-long", msgs["body_too_long"].format(lines=len(lines), max_lines=max_lines), "error"))

    body_clean = strip_code_blocks(body)
    placeholders_cfg = config.get("placeholders", {})

    known_tools = set(config.get("tools", {}).get("known", []))
    for pattern in placeholders_cfg.get("general_patterns", []):
        matches = set(re.findall(pattern, body_clean, re.IGNORECASE))
        filtered = []
        for m in matches:
            if m in placeholders_cfg.get("allowed_literals", []):
                continue
            if any(re.match(p, m) for p in placeholders_cfg.get("allowed_patterns", [])):
                continue
            # 允许 [ToolName] 这种工具绑定标记
            inner = m.strip("[]")
            if inner in known_tools:
                continue
            filtered.append(m)

        if filtered:
            if pattern == r"\{.*?\}":
                real = [m for m in filtered if not re.match(r'^\{[A-Za-z\u4e00-\u9fff].*\}$', m)]
                real = [m for m in real if m != '{date}']
                if real:
                    findings.append(Finding("placeholder-residue", msgs["placeholder_residue"].format(pattern=pattern, matches=real[:5]), "error"))
            else:
                findings.append(Finding("placeholder-residue", msgs["placeholder_residue"].format(pattern=pattern, matches=filtered[:5]), "error"))

    # UR-SKILL 自身风险边界关键词检查
    is_ur_skill = ctx.frontmatter.get("name") in ("ur-skill", "research-analyst", "ur-skill-cn", "ur-skill-en")
    if is_ur_skill:
        for boundary in config.get("rules", {}).get("risk_boundaries", []):
            if boundary not in body_clean:
                findings.append(Finding("missing-risk-boundary", msgs["missing_risk_boundary"].format(boundary=boundary), "error"))

    return findings


def _validate_unresolved_placeholders(ctx: SkillContext, config: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    msgs = config.get("messages", {})
    body_clean = strip_code_blocks(ctx.body)
    body_no_fm = re.sub(r"^---[\s\S]*?---", "", body_clean)

    for item in config.get("placeholders", {}).get("unresolved_patterns", []):
        pattern = item["pattern"]
        label = item["label"]
        matches = re.findall(pattern, body_no_fm)
        if matches:
            findings.append(Finding("unresolved-placeholder", msgs["unresolved_placeholder"].format(count=len(matches), label=label), "error"))

    return findings


def _validate_deprecated_tools(ctx: SkillContext, config: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    msgs = config.get("messages", {})
    for old, new in config.get("deprecated_tools", {}).items():
        if old in ctx.text:
            findings.append(Finding("deprecated-tool", msgs["deprecated_tool"].format(old=old, new=new), "error"))
    return findings


def _validate_json_schema(ctx: SkillContext) -> list[Finding]:
    """可选的 JSON Schema 校验。依赖 jsonschema 库，未安装时静默跳过。"""
    if not _HAS_JSONSCHEMA:
        return []

    # 查找 skill-schema.json：优先 skill_dir/templates/，其次 scripts_dir/../templates/
    skill_dir = ctx.path.parent if ctx.path else None
    schema_paths = []
    if skill_dir:
        schema_paths.append(skill_dir / "templates" / "skill-schema.json")
    schema_paths.append(Path(__file__).resolve().parent.parent / "templates" / "skill-schema.json")

    schema = None
    for p in schema_paths:
        if p.exists():
            schema = json.loads(p.read_text(encoding="utf-8"))
            break

    if schema is None:
        return [Finding("schema-missing", "JSON Schema file skill-schema.json not found in templates/", "warning")]

    # YAML frontmatter 已经是 dict，但 YAML 会将日期解析为 datetime.date，
    # 需要统一转为字符串后再校验
    frontmatter = _normalize_for_schema(ctx.frontmatter)
    validator = jsonschema.Draft202012Validator(schema)
    errors = sorted(validator.iter_errors(frontmatter), key=lambda e: e.path)

    findings: list[Finding] = []
    for err in errors:
        path = " → ".join(str(p) for p in err.path) if err.path else "(root)"
        findings.append(Finding(
            "schema-violation",
            f"[{path}] {err.message}",
            "error",
        ))

    if not findings:
        findings.append(Finding("schema-valid", "JSON Schema validation passed", "info"))

    return findings


def _normalize_for_schema(data: Any) -> Any:
    """将 YAML 解析产生的非字符串标量（如 date）转为字符串，使其通过 JSON Schema 校验。"""
    import datetime as dt

    if isinstance(data, dict):
        return {k: _normalize_for_schema(v) for k, v in data.items()}
    if isinstance(data, list):
        return [_normalize_for_schema(item) for item in data]
    if isinstance(data, (dt.date, dt.datetime)):
        return data.isoformat()
    if isinstance(data, (int, float, bool)):
        return data
    if isinstance(data, str):
        return data
    return str(data)
