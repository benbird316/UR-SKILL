"""内容层校验器。

负责风险/专业边界滥用、切面填充、盲区甩锅、第一人称、膨胀头衔、
工作流检查项、RFC2119 规则关键词、能力矩阵结构、正向表述。
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
    findings.extend(_validate_capability_structure(ctx, config))
    findings.extend(_validate_positive_phrasing(ctx, config))
    findings.extend(_validate_capability_workflow_confusion(ctx, config))
    findings.extend(_validate_semantic_alignment(ctx, config))
    return findings


def _validate_capability_workflow_confusion(ctx: SkillContext, config: dict[str, Any]) -> list[Finding]:
    """Detect capability matrix terminology leaking into workflow section, and vice versa.

    Key rule: "MUST NOT 将能力矩阵与工作流步骤混淆" (3.2-04).
    """
    findings: list[Finding] = []
    msgs = config.get("messages", {})
    boundary_cfg = config.get("capability_workflow_boundary", {})
    body = ctx.body

    # Locate capability section heading
    cap_match = re.search(r'^(#{2,3})\s+(?:\d+\.?\s*)?.*?(?:能力矩阵|能力架构)', body, re.MULTILINE)
    wf_match = re.search(r'^(#{2,3})\s+(?:\d+\.?\s*)?(?:工作流|Workflow|工作流程)', body, re.MULTILINE)

    # Check capability section for workflow terminology
    if cap_match:
        cap_level = len(cap_match.group(1))
        cap_start = cap_match.end()
        next_heading = re.search(
            rf'^#{{{1},{cap_level}}}\s+[^#]', body[cap_start:], re.MULTILINE,
        )
        cap_end = cap_start + next_heading.start() if next_heading else len(body)
        cap_section = body[cap_start:cap_end]

        forbidden = boundary_cfg.get("capability_forbidden_terms", [])
        found_terms: list[str] = []
        for term in forbidden:
            if re.search(term, cap_section):
                # Check if ALL occurrences are in negation context (e.g. "非工作流步骤")
                all_negated = True
                for m in re.finditer(term, cap_section):
                    prefix = cap_section[max(0, m.start()-6):m.start()]
                    if not re.search(r'(?:非|不是|并非|not\s|no\s)', prefix, re.IGNORECASE):
                        all_negated = False
                        break
                if not all_negated:
                    found_terms.append(term)
        if found_terms:
            findings.append(Finding(
                "capability-workflow-confusion",
                msgs.get("capability_workflow_confused_terms", "").format(
                    section="能力矩阵", count=len(found_terms),
                    terms=", ".join(found_terms[:5]),
                ),
                "error",
            ))

    # Check workflow section for capability terminology
    if wf_match:
        wf_level = len(wf_match.group(1))
        wf_start = wf_match.end()
        next_heading = re.search(
            rf'^#{{{1},{wf_level}}}\s+[^#]', body[wf_start:], re.MULTILINE,
        )
        wf_end = wf_start + next_heading.start() if next_heading else len(body)
        wf_section = body[wf_start:wf_end]

        forbidden = boundary_cfg.get("workflow_forbidden_terms", [])
        found_terms: list[str] = []
        for term in forbidden:
            if re.search(term, wf_section):
                found_terms.append(term)
        if found_terms:
            findings.append(Finding(
                "capability-workflow-confusion",
                msgs.get("capability_workflow_confused_terms", "").format(
                    section="工作流", count=len(found_terms),
                    terms=", ".join(found_terms[:5]),
                ),
                "error",
            ))

    return findings


def _validate_semantic_alignment(ctx: SkillContext, config: dict[str, Any]) -> list[Finding]:
    """Check that capability domain names appear in workflow action descriptions.

    Rule: "MUST 生成的 SKILL 工作流中，动作描述与能力矩阵语义对齐" (3.1-12).
    """
    findings: list[Finding] = []
    msgs = config.get("messages", {})
    body = ctx.body

    # Extract domain names from capability matrix tables
    cap_match = re.search(r'(?:###\s+.*?能力矩阵|##\s+.*?能力架构)', body)
    if not cap_match:
        return findings

    cap_start = cap_match.end()
    next_heading = re.search(r'^#{2,3}\s+[^#]', body[cap_start:], re.MULTILINE)
    cap_end = cap_start + next_heading.start() if next_heading else len(body)
    cap_section = body[cap_start:cap_end]

    # Extract domain names from table rows: | DomainName | ...
    domain_names: list[str] = []
    domain_rows = re.findall(
        r'^\|\s*(?!领域|Domain|切面|编号|:?--)([^\|\n]+?)\s*\|',
        cap_section,
        re.MULTILINE,
    )
    for d in domain_rows:
        d_clean = d.strip()
        # Skip core domain marker row
        if re.search(r'核心[:：]|Core[:：]', d_clean):
            continue
        # Extract just the domain name (remove prefixes like "A. ", "B. ", "1. ")
        d_clean = re.sub(r'^[A-H0-9]+[\.\s\)]+\s*', '', d_clean)
        if len(d_clean) >= 2:
            domain_names.append(d_clean)

    if not domain_names:
        return findings

    # Find workflow section
    wf_match = re.search(r'(?:#{2,3}\s*(?:\d+\.?\s*)?(?:工作流|Workflow|工作流程))', body, re.MULTILINE)
    if not wf_match:
        return findings

    wf_start = wf_match.end()
    next_heading = re.search(r'^#{2,3}\s+[^#]', body[wf_start:], re.MULTILINE)
    wf_end = wf_start + next_heading.start() if next_heading else len(body)
    wf_section = body[wf_start:wf_end]

    # Check each domain name appears (as substring or semantic match) in workflow
    min_matched = config.get("semantic_alignment", {}).get("min_matched_domains", 1)
    matched = 0
    unmatched: list[str] = []
    for d in domain_names:
        # Try exact match first
        if d in wf_section:
            matched += 1
            continue
        # Try keyword match (take first 2-3 meaningful chars as search term)
        key_chars = re.sub(r'[的与和及之]', '', d)[:3]
        if len(key_chars) >= 2 and key_chars in wf_section:
            matched += 1
            continue
        unmatched.append(d)

    if matched < min_matched and unmatched:
        findings.append(Finding(
            "semantic-alignment-weak",
            msgs.get("semantic_alignment_weak", "").format(
                matched=matched, total=len(domain_names),
                unmatched=", ".join(unmatched[:3]),
            ),
            "warning",
        ))

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

    # Compute frontmatter line offset for accurate line number reporting
    parts = ctx.text.split("---", 2)
    fm_lines = ctx.text[:len(parts[0]) + 3 + len(parts[1]) + 3].count('\n') if len(parts) >= 3 and ctx.text.startswith("---") else 0

    for i, line in enumerate(body_clean.splitlines(), 1):
        if '我' in line:
            stripped = line.strip()
            if stripped:
                real_line = i + fm_lines
                findings.append(Finding("first-person", msgs["first_person"].format(line=real_line, content=stripped[:80]), "error", real_line))

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


def _validate_capability_structure(ctx: SkillContext, config: dict[str, Any]) -> list[Finding]:
    """Check capability matrix has core domain + 3-8 radiating domains with 4 layers each.

    Supports two formats:
      A) Generated SKILLs: domain rows prefixed with A./B./C. in tables or headings
      B) UR-SKILL own format: domain rows in capability section tables (no letter prefix)
    """
    findings: list[Finding] = []
    msgs = config.get("messages", {})
    body = ctx.body

    core_patterns = [r'核心[：:]', r'核心领域', r'核心域', r'Core Domain', r'Core[:：]']
    has_core = any(re.search(p, body) for p in core_patterns)
    if not has_core:
        findings.append(Finding("capability-no-core", msgs.get("capability_no_core", "能力矩阵缺少核心领域定义"), "error"))
        return findings

    # --- Format A: letter-prefixed domain entries (A./B./C.) ---
    radiant_patterns = [r'\|\s*%s[\.\s]+\S+' % c for c in 'ABCDEFGH']
    format_a_count = sum(1 for p in radiant_patterns if re.search(p, body, re.MULTILINE))
    domain_headers = re.findall(r'^#{2,4}\s*(?:A|B|C|D|E|F|G|H)\s+[^\n]+', body, re.MULTILINE)
    format_a_count = max(format_a_count, len(domain_headers))

    # --- Format B: table rows in capability section (no prefix) ---
    format_b_count = 0
    cap_match = re.search(
        r'(?:###\s+.*?(?:能力矩阵|Capability\s+Matrix)|##\s+.*?(?:能力矩阵|Capability\s+Matrix))',
        body,
    )
    if cap_match:
        cap_start = cap_match.end()
        next_section = re.search(r'^#{2,3}\s+[^#]', body[cap_start:], re.MULTILINE)
        cap_end = cap_start + next_section.start() if next_section else len(body)
        cap_section = body[cap_start:cap_end]
        # Count data rows in tables (skip header rows like "| 领域 |..." or "|:---|...")
        data_rows = re.findall(
            r'^\|\s*(?!领域|Domain|切面|编号|:?--)[^\|\n]+\|.*?\|.*?\|.*?\|',
            cap_section, re.MULTILINE,
        )
        core_rows = [r for r in data_rows if re.search(r'核心[:：]|Core[:：]', r)]
        radiant_rows = [r for r in data_rows if r not in core_rows]
        format_b_count = len(radiant_rows)

    radiant_count = max(format_a_count, format_b_count)

    if radiant_count < 3:
        findings.append(Finding("capability-few-domains",
            msgs.get("capability_few_domains", "辐射领域不足（最少3个，当前{count}个）").format(count=radiant_count),
            "error"))
    elif radiant_count > 8:
        findings.append(Finding("capability-too-many-domains",
            msgs.get("capability_too_many_domains", "辐射领域过多（最多8个，当前{count}个）").format(count=radiant_count),
            "warning"))

    # Check for 4 depth layers
    layer_patterns = [r'基础层|Foundation', r'进阶层|Advanced', r'高阶层|Expert', r'拓展层|Extension']
    layer_count = sum(1 for p in layer_patterns if re.search(p, body))
    if layer_count < 4:
        findings.append(Finding("capability-layers-missing",
            msgs.get("capability_layers_missing", "能力矩阵缺少4层深度（基础/进阶/高阶/拓展）"),
            "warning"))

    return findings


def _validate_positive_phrasing(ctx: SkillContext, config: dict[str, Any]) -> list[Finding]:
    """Check SHOULD-level rules use positive phrasing (not 不得/禁止/必须)."""
    findings: list[Finding] = []
    msgs = config.get("messages", {})
    body = ctx.body

    # Locate SHOULD section
    should_pattern = r'(?:#{2,4}\s*(?:\d+\.?\s*)?(?:强偏好|SHOULD).*?\n)(.*?)(?=#{2,4}\s|\Z)'
    should_match = re.search(should_pattern, body, re.DOTALL)
    if not should_match:
        return findings

    should_section = should_match.group(1)
    negative_patterns = [r'不得', r'禁止', r'严禁', r'必须', r'必需']
    for i, line in enumerate(should_section.splitlines(), 1):
        stripped = line.strip()
        for np_pattern in negative_patterns:
            if re.search(np_pattern, stripped):
                findings.append(Finding(
                    "negative-phrasing-in-should",
                    msgs.get("negative_phrasing_in_should", "SHOULD 规则含反向表述 '{word}'：'{content}'").format(word=np_pattern, content=stripped[:80]),
                    "warning",
                ))
                break

    return findings
