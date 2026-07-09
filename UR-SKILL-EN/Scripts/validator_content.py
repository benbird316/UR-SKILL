"""内容层校验器。

负责风险/专业边界滥用、切面填充、盲区甩锅、第一人称、膨胀头衔、
工作流检查项、RFC2119 规则关键词。
"""

from __future__ import annotations

import re
from typing import Any

from common import Finding, SkillContext, strip_code_blocks


def validate(ctx: SkillContext, config: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    findings.extend(_validate_quality(ctx, config))
    findings.extend(_validate_first_person(ctx, config))
    findings.extend(_validate_identity_title(ctx, config))
    findings.extend(_validate_workflow(ctx, config))
    findings.extend(_validate_rfc2119(ctx, config))
    return findings


def _validate_quality(ctx: SkillContext, config: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    body_clean = strip_code_blocks(ctx.body)
    msgs = config.get("messages", {})
    rules = config.get("rules", {})

    # 风险边界滥用
    rb_lines = re.findall(r'^\s*(?:\|\s*)?风险边界-\d+\s*[:\|]\s*(.+)$', body_clean, re.MULTILINE)
    rb_list = re.findall(r'^\s*[-*]\s*\*\*风险边界-(\d+)\*\*[：:]\s*(.+)$', body_clean, re.MULTILINE)
    for line in rb_lines:
        for kw in rules.get("risk_boundary_abuse_keywords", []):
            if re.search(kw, line):
                findings.append(Finding("risk-boundary-abuse", msgs["risk_boundary_abuse"].format(keyword=kw, content=line[:60]), "error"))
                break
    for _, content in rb_list:
        for kw in rules.get("risk_boundary_abuse_keywords", []):
            if re.search(kw, content):
                findings.append(Finding("risk-boundary-abuse", msgs["risk_boundary_abuse"].format(keyword=kw, content=content[:60]), "error"))
                break

    # 专业边界滥用
    pb_lines = re.findall(r'^\s*(?:\|\s*)?专业边界-\d+\s*[:\|]\s*(.+)$', body_clean, re.MULTILINE)
    pb_list = re.findall(r'^\s*[-*]\s*\*\*专业边界-(\d+)\*\*[：:]\s*(.+)$', body_clean, re.MULTILINE)
    for line in pb_lines:
        for kw in rules.get("professional_boundary_abuse_keywords", []):
            if re.search(kw, line):
                findings.append(Finding("professional-boundary-abuse", msgs["professional_boundary_abuse"].format(keyword=kw, content=line[:60]), "error"))
                break
    for _, content in pb_list:
        for kw in rules.get("professional_boundary_abuse_keywords", []):
            if re.search(kw, content):
                findings.append(Finding("professional-boundary-abuse", msgs["professional_boundary_abuse"].format(keyword=kw, content=content[:60]), "error"))
                break

    # 切面填充
    facet_lines = re.findall(
        r'^\s*(?:\|\s*)?切面(\d)\s*(?:\|.*?\||\*\*切面\d[^:]*\*\*[：:]\s*)(.+?)(?:\||$)',
        body_clean,
        re.MULTILINE,
    )
    if not facet_lines:
        facet_lines = re.findall(r'切面(\d)\s*[：:]\s*(.+?)(?:\n|$)', body_clean)

    for num, content in facet_lines:
        content_clean = content.strip()
        for pattern in rules.get("facet_filler_patterns", []):
            if re.search(pattern, content_clean):
                if len(content_clean) >= 25:
                    continue
                findings.append(Finding("facet-filler", msgs["facet_filler"].format(facet=num, content=content_clean[:60]), "error"))
                break

    # 盲区甩锅
    blind_sections = re.findall(
        r'盲区[：:]\s*(.+?)(?=\n\n|\n#|\Z)',
        body_clean,
        re.DOTALL,
    )
    for section in blind_sections:
        section_clean = section.strip()
        has_dump = any(re.search(kw, section_clean) for kw in rules.get("blind_dump_keywords", []))
        has_attempt = "已尝试" in section_clean
        if has_dump and not has_attempt:
            findings.append(Finding("blind-spot-dumping", msgs["blind_spot_dumping"], "error"))

    return findings


def _validate_first_person(ctx: SkillContext, config: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    msgs = config.get("messages", {})
    body_clean = strip_code_blocks(ctx.body)

    for i, line in enumerate(body_clean.splitlines(), 1):
        if '我' in line:
            stripped = line.strip()
            if stripped:
                findings.append(Finding("first-person", msgs["first_person"].format(line=i, content=stripped[:80]), "error", i))

    desc = ctx.frontmatter.get("description", "")
    if isinstance(desc, str) and '我' in desc:
        findings.append(Finding("first-person-description", msgs["first_person_description"].format(content=desc[:80]), "error"))

    return findings


def _validate_identity_title(ctx: SkillContext, config: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    msgs = config.get("messages", {})
    identity_cfg = config.get("identity", {})
    inflated_titles = identity_cfg.get("inflated_titles", [])
    experience_patterns = identity_cfg.get("experience_patterns", [])
    identity_keywords = identity_cfg.get("identity_keywords", [])

    for i, line in enumerate(ctx.body.split("\n"), 1):
        stripped = line.strip()
        if any(keyword in stripped for keyword in identity_keywords):
            for title in inflated_titles:
                if title in stripped:
                    findings.append(Finding("inflated-title", msgs["inflated_title_body"].format(line=i, title=title), "error", i))
                    break
            for pattern in experience_patterns:
                m = re.search(pattern, stripped)
                if m:
                    findings.append(Finding("fabricated-years", msgs["fabricated_years_body"].format(line=i, years=m.group()), "error", i))
                    break

    desc = ctx.frontmatter.get("description", "")
    if isinstance(desc, str):
        for title in inflated_titles:
            if title in desc:
                findings.append(Finding("inflated-title-description", msgs["inflated_title_description"].format(title=title), "error"))
                break
        for pattern in experience_patterns:
            m = re.search(pattern, desc)
            if m:
                findings.append(Finding("fabricated-years-description", msgs["fabricated_years_description"].format(years=m.group()), "error"))
                break

    return findings


def _validate_workflow(ctx: SkillContext, config: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    msgs = config.get("messages", {})
    wf_cfg = config.get("workflow", {})
    body = ctx.body

    step_pattern = re.compile(wf_cfg.get("step_heading_pattern", r"^#{2,4}\s*\d+\.\s*(\S+?)\s*[（(].*?[）)].*?维.*$"), re.MULTILINE)

    for match in step_pattern.finditer(body):
        step_name = match.group(1)
        start = match.end()
        next_match = step_pattern.search(body, start)
        end = next_match.start() if next_match else len(body)
        section = body[start:end]

        check_count = section.count("- [ ]") + section.count("- [x]")
        expected = wf_cfg.get("expected_checks", {}).get(step_name)
        if expected is not None and check_count != expected:
            findings.append(Finding("workflow-step-count", msgs["workflow_step_count"].format(step=step_name, actual=check_count, expected=expected), "error"))

        checklist_items = re.findall(r"- \[[ x]\]\s*(.+?)(?=\n- \[|$)", section, re.DOTALL)
        covered = set()
        for item in checklist_items:
            item_text = item.strip().split("\n")[0]
            clean_text = re.sub(r"\*\*(.+?)\*\*", r"\1", item_text)
            for dim in wf_cfg.get("required_dimensions", []) + wf_cfg.get("critical_only_dimensions", []):
                if dim in clean_text:
                    covered.add(dim)

        for dim in wf_cfg.get("required_dimensions", []):
            if dim not in covered:
                findings.append(Finding("workflow-missing-dimension", msgs["workflow_missing_dimension"].format(step=step_name, dimension=dim), "error"))

        if step_name in wf_cfg.get("critical_steps", []):
            for dim in wf_cfg.get("critical_only_dimensions", []):
                if dim not in covered:
                    findings.append(Finding("workflow-critical-missing-dimension", msgs["workflow_critical_missing_dimension"].format(step=step_name, dimension=dim), "error"))

    return findings


def _validate_rfc2119(ctx: SkillContext, config: dict[str, Any]) -> list[Finding]:
    findings: list[Finding] = []
    msgs = config.get("messages", {})
    body = ctx.body
    keywords = config.get("rules", {}).get("rfc2119_keywords", ["MUST", "MUST NOT", "SHOULD", "SHOULD NOT", "MAY"])

    rules_heading = config.get("rules", {}).get("rules_heading_pattern", r"^#{2,3}\s*(?:\d+\.?\s*)?(?:[Rr]ules|规则)")
    rules_match = re.search(rules_heading, body, re.MULTILINE)
    if not rules_match:
        findings.append(Finding("rules-block-not-found", msgs["rules_block_not_found"], "error"))
        return findings

    start = rules_match.end()
    level = len(rules_match.group(0)) - len(rules_match.group(0).lstrip('#'))
    next_section = re.search(r"^#{%d,%d}\s+(?:\d+\.?\s*)?(?![Rr]ules).*?\n" % (level, level), body[start:], re.MULTILINE)
    end = start + next_section.start() if next_section else len(body)
    rules_section = body[start:end]

    rule_lines = re.findall(
        r"^\s*[-*]\s+(?:\*\*)?(?:规则\d+\s+|Rule\d+\s+)?(.+?)(?:\*\*)?(?:\s|$)",
        rules_section,
        re.MULTILINE,
    )

    if not rule_lines:
        rule_lines = re.findall(
            r"^\s*[-*]\s+.*?(MUST NOT|MUST|SHOULD NOT|SHOULD|MAY)\s",
            rules_section,
            re.MULTILINE,
        )

    if not rule_lines:
        findings.append(Finding("rules-no-entries", msgs["rules_no_entries"], "error"))
        return findings

    for idx, item in enumerate(rule_lines, 1):
        item_clean = re.sub(r"\*\*", "", item).strip()
        has_keyword = any(item_clean.upper().startswith(kw) for kw in keywords)
        if not has_keyword:
            findings.append(Finding("rule-no-rfc2119", msgs["rule_no_rfc2119"].format(index=idx, content=item_clean[:60]), "error"))

    return findings
