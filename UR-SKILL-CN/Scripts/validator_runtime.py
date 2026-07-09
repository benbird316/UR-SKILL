"""运行时层校验器。

负责引用文件存在性、工具绑定、输出规格、文件依赖决策、
UR-SKILL 文件泄漏检测。
"""

from __future__ import annotations

import re
from pathlib import Path
from typing import Any

from common import Finding, SkillContext, strip_code_blocks


def validate(ctx: SkillContext, config: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    findings.extend(_validate_references(ctx, config))
    findings.extend(_validate_tool_binding(ctx, config))
    findings.extend(_validate_output_spec(ctx, config))
    findings.extend(_validate_file_dependency(ctx, config))
    findings.extend(_validate_ur_skill_leaks(ctx, config))
    return findings


def _check_ref_exists(rel_path: str, skill_dir: Path) -> bool:
    """检查引用文件是否存在，防止路径穿越。

    使用 resolve() + relative_to() 确保目标路径不逃逸 skill_dir。
    """
    try:
        target = (skill_dir / rel_path).resolve()
        target.relative_to(skill_dir.resolve())
    except ValueError:
        return False  # 穿越目录的引用一律视为不存在
    return target.exists()


def _validate_references(ctx: SkillContext, config: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    msgs = config.get("messages", {})
    body = ctx.body
    skill_dir = ctx.skill_dir

    refs = re.findall(r"[Rr]eferences/([a-zA-Z0-9_\-\./]+)", body)
    scr = re.findall(r"[Ss]cripts/([a-zA-Z0-9_\-\./]+)", body)
    ast = re.findall(r"assets/([a-zA-Z0-9_\-\./]+)", body)
    dg = re.findall(r"[Dd]esign-[Gg]uides/([a-zA-Z0-9_\-\./]+)", body)
    tpl = re.findall(r"[Tt]emplates/([a-zA-Z0-9_\-\./]+)", body)

    for ref in set(refs):
        if not _check_ref_exists(f"References/{ref}", skill_dir):
            findings.append(Finding("missing-reference", msgs["reference_missing"].format(path=f"References/{ref}"), "error"))

    for script in set(scr):
        if not _check_ref_exists(f"Scripts/{script}", skill_dir):
            findings.append(Finding("missing-script", msgs["script_missing"].format(path=f"Scripts/{script}"), "error"))

    for asset in set(ast):
        if not _check_ref_exists(f"assets/{asset}", skill_dir):
            findings.append(Finding("missing-asset", msgs["asset_missing"].format(path=f"assets/{asset}"), "error"))

    for guide in set(dg):
        if not _check_ref_exists(f"design-guides/{guide}", skill_dir):
            findings.append(Finding("missing-design-guide", msgs["design_guide_missing"].format(path=f"design-guides/{guide}"), "error"))

    for template in set(tpl):
        if not _check_ref_exists(f"templates/{template}", skill_dir):
            findings.append(Finding("missing-template", msgs["template_missing"].format(path=f"templates/{template}"), "error"))

    return findings


def _validate_tool_binding(ctx: SkillContext, config: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    msgs = config.get("messages", {})
    tools_cfg = config.get("tools", {})
    body = ctx.body

    name = ctx.frontmatter.get("name", "")
    if name in tools_cfg.get("binding_exempt_skills", []):
        return findings

    workflow_match = re.search(r"^#{2,3}\s*(?:\d+\.?\s*)?(?:Workflow|[Ww]orkflow|工作流)", body, re.MULTILINE)
    if not workflow_match:
        return findings

    wf_start = workflow_match.end()
    next_section = re.search(r"^#{2,3}\s+(?!\d|Workflow|[Ww]orkflow|工作流).*?\n", body[wf_start:], re.MULTILINE)
    wf_end = wf_start + next_section.start() if next_section else len(body)
    workflow_body = body[wf_start:wf_end]

    action_lines = re.findall(r"^\s*\d+\.\s+(.+)", workflow_body, re.MULTILINE)
    tool_pattern = re.compile(r"\[([A-Za-z_][A-Za-z0-9_]*)\]")
    known_tools = set(tools_cfg.get("known", []))

    has_any_tool = False
    unbound_lines = []
    exempt_prefixes = [p.lower() for p in tools_cfg.get("exempt_action_prefixes", [])]
    action_verbs = tools_cfg.get("action_verbs", [])

    for i, line in enumerate(action_lines):
        line_clean = line.strip()

        if any(line_clean.lower().startswith(p) for p in exempt_prefixes):
            continue

        if "认知操作" in line_clean or "cognitive operation" in line_clean.lower():
            remaining = re.sub(r"\[认知操作\]|\[cognitive operation\]", "", line_clean, flags=re.IGNORECASE)
            other_tools = tool_pattern.findall(remaining)
            if not other_tools:
                continue

        if re.match(r"(为什么|why|设计原理|design rationale|注意|note|说明|explanation)", line_clean, re.IGNORECASE):
            continue

        matches = tool_pattern.findall(line_clean)
        if matches:
            has_any_tool = True
        else:
            if any(re.search(verb, line_clean, re.IGNORECASE) for verb in action_verbs):
                unbound_lines.append(f"  L{i+1}: {line_clean[:60]}...")

    if has_any_tool and unbound_lines:
        findings.append(Finding("tool-binding-missing", msgs["tool_binding_missing"].format(lines="\n".join(unbound_lines[:5])), "error"))

    return findings


def _validate_output_spec(ctx: SkillContext, config: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    msgs = config.get("messages", {})
    output_cfg = config.get("output_spec", {})

    name = str(ctx.frontmatter.get("name", "")).lower()
    desc = str(ctx.frontmatter.get("description", "")).lower()

    is_crt = any(kw in name for kw in output_cfg.get("keywords", [])) or any(kw in desc for kw in output_cfg.get("keywords", []))
    if not is_crt:
        return findings

    body = ctx.body
    for key, spec in output_cfg.get("checks", {}).items():
        found = any(re.search(pat, body) for pat in spec["patterns"])
        if not found:
            findings.append(Finding("output-spec-missing", msgs["output_spec_missing"].format(label=spec["label"], patterns=spec["patterns"][:2]), "error"))

    return findings


def _validate_file_dependency(ctx: SkillContext, config: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    msgs = config.get("messages", {})
    fd_cfg = config.get("file_dependency", {})
    body = ctx.body

    workflow_match = re.search(fd_cfg.get("workflow_heading", r"^#{2,3}\s*(?:\d+\.?\s*)?工作流"), body, re.MULTILINE)
    if not workflow_match:
        return findings

    wf_start = workflow_match.end()
    next_section = re.search(r"^#{2,3}\s+(?!\d|Workflow|[Ww]orkflow|工作流).*?\n", body[wf_start:], re.MULTILINE)
    wf_end = wf_start + next_section.start() if next_section else len(body)
    workflow_section = body[wf_start:wf_end]

    indicators = fd_cfg.get("indicators", [])
    has_decision = any(ind.lower() in workflow_section.lower() or ind in workflow_section for ind in indicators)
    if not has_decision:
        findings.append(Finding("file-dependency-missing", msgs["file_dependency_missing"], "error"))

    return findings


_UR_SKILL_FILES: set[str] | None = None


def _discover_ur_skill_files(ctx: SkillContext, config: dict[str, Any]) -> set[str]:
    """发现 UR-SKILL 内部文件，用于泄漏检测。

    内置路径沙箱：解析后的 ur_skill_root 必须在 Scripts 目录的父级仓库根目录内。
    """
    script_dir = ctx.path.resolve().parent
    ur_skill_root = script_dir.resolve()

    # 沙箱约束：ur_skill_root 不能逃逸项目根目录
    project_root = Path(__file__).resolve().parent.parent.resolve()  # UR-SKILL-CN/ or UR-SKILL-EN/
    try:
        ur_skill_root.relative_to(project_root)
    except ValueError:
        # skill_dir 在项目根之外（如 Examples/）——不是 UR-SKILL 自身，无需泄漏检测
        return set()

    files: set[str] = set()
    if not ur_skill_root.exists():
        return files
    for f in ur_skill_root.rglob("*"):
        if f.is_symlink():
            continue
        if f.is_file() and not f.name.startswith("."):
            rel = f.relative_to(ur_skill_root).as_posix()
            prefixes = config.get("self_contained", {}).get("forbidden_prefixes", [])
            special = config.get("self_contained", {}).get("special_files", [])
            if any(rel.startswith(prefix) for prefix in prefixes):
                files.add(rel)
            elif rel in special:
                files.add(rel)
    return files


def _validate_ur_skill_leaks(ctx: SkillContext, config: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    msgs = config.get("messages", {})

    name = ctx.frontmatter.get("name", "")
    if name in config.get("self_contained", {}).get("exempt_skills", []):
        return findings

    body_clean = strip_code_blocks(ctx.body)

    global _UR_SKILL_FILES
    if _UR_SKILL_FILES is None:
        _UR_SKILL_FILES = _discover_ur_skill_files(ctx, config)

    if not _UR_SKILL_FILES:
        return findings

    leaked: set[str] = set()
    for sb_file in _UR_SKILL_FILES:
        escaped = re.escape(sb_file)
        patterns = [
            rf'\b{escaped}\b',
            rf'\./{escaped}\b',
            rf'\.\./{escaped}\b',
        ]
        for pat in patterns:
            if re.search(pat, body_clean):
                leaked.add(sb_file)
                break

    for f in sorted(leaked):
        findings.append(Finding("ur-skill-leak", msgs["ur_skill_leak"].format(path=f), "error"))

    return findings
