"""Content layer validator.

Handles risk/professional boundary abuse, facet filler, blind spot dumping,
first-person pronouns, inflated titles, workflow check items, RFC 2119 keywords,
capability matrix structure, and positive phrasing.

Bilingual patterns: supports both Chinese (zh-cn) and English (en-us) SKILL content.
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

    Key rule: "MUST NOT confuse capability matrix with workflow steps" (3.2-04).
    """
    findings: list[Finding] = []
    msgs = config.get("messages", {})
    boundary_cfg = config.get("capability_workflow_boundary", {})
    body = ctx.body

    # Locate capability section heading (bilingual: CN + EN)
    cap_match = re.search(
        r'^(#{2,3})\s+(?:\d+\.?\s*)?.*?(?:能力矩阵|能力架构|Capability\s+(?:Matrix|Architecture))',
        body, re.MULTILINE,
    )
    wf_match = re.search(
        r'^(#{2,3})\s+(?:\d+\.?\s*)?(?:工作流|Workflow|工作流程)',
        body, re.MULTILINE,
    )

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
            if re.search(term, cap_section, re.IGNORECASE):
                # Check if ALL occurrences are in negation context (e.g. "非工作流步骤")
                all_negated = True
                for m in re.finditer(term, cap_section, re.IGNORECASE):
                    prefix = cap_section[max(0, m.start()-6):m.start()]
                    if not re.search(r'(?:非|不是|并非|not\s|no\s)', prefix, re.IGNORECASE):
                        all_negated = False
                        break
                if not all_negated:
                    found_terms.append(term)
        if found_terms:
            section_label = "Capability Matrix" if 'Capability' in body[cap_match.start():cap_match.end()] else "\u80fd\u529b\u77e9\u9635"
            findings.append(Finding(
                "capability-workflow-confusion",
                msgs.get("capability_workflow_confused_terms", "").format(
                    section=section_label, count=len(found_terms),
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
            if re.search(term, wf_section, re.IGNORECASE):
                found_terms.append(term)
        if found_terms:
            section_label = "Workflow" if 'Workflow' in body[wf_match.start():wf_match.end()] else "\u5de5\u4f5c\u6d41"
            findings.append(Finding(
                "capability-workflow-confusion",
                msgs.get("capability_workflow_confused_terms", "").format(
                    section=section_label, count=len(found_terms),
                    terms=", ".join(found_terms[:5]),
                ),
                "error",
            ))

    return findings


def _validate_semantic_alignment(ctx: SkillContext, config: dict[str, Any]) -> list[Finding]:
    """Check that capability domain names appear in workflow action descriptions.

    Rule: "MUST ensure action descriptions in generated SKILL workflow are semantically
    aligned with the capability matrix" (3.1-12).
    """
    findings: list[Finding] = []
    msgs = config.get("messages", {})
    body = ctx.body

    # Extract domain names from capability matrix tables (bilingual)
    cap_match = re.search(
        r'(?:###\s+.*?(?:能力矩阵|Capability\s+Matrix)|##\s+.*?(?:能力架构|Capability\s+Architecture))',
        body,
    )
    if not cap_match:
        return findings

    cap_start = cap_match.end()
    next_heading = re.search(r'^#{2,3}\s+[^#]', body[cap_start:], re.MULTILINE)
    cap_end = cap_start + next_heading.start() if next_heading else len(body)
    cap_section = body[cap_start:cap_end]

    # Extract domain names from table rows: | DomainName | ... (bilingual header exclusion)
    domain_names: list[str] = []
    domain_rows = re.findall(
        r'^\|\s*(?!\u9886\u57df|Domain|\u5207\u9762|\u7f16\u53f7|:?--)([^\|\n]+?)\s*\|',
        cap_section,
        re.MULTILINE,
    )
    for d in domain_rows:
        d_clean = d.strip()
        # Skip core domain marker row
        if re.search(r'\u6838\u5fc3[:\uff1a]|Core[:\uff1a]', d_clean):
            continue
        # Extract just the domain name (remove prefixes like "A. ", "B. ", "1. ")
        d_clean = re.sub(r'^[A-H0-9]+[\.\s\)]+\s*', '', d_clean)
        if len(d_clean) >= 2:
            domain_names.append(d_clean)

    if not domain_names:
        return findings

    # Find workflow section (bilingual)
    wf_match = re.search(
        r'(?:#{2,3}\s*(?:\d+\.?\s*)?(?:\u5de5\u4f5c\u6d41|Workflow|\u5de5\u4f5c\u6d41\u7a0b))',
        body, re.MULTILINE,
    )
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
        key_chars = re.sub(r'[\u7684\u4e0e\u548c\u53ca\u4e4b]', '', d)[:3]
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

    # Risk boundary abuse (bilingual)
    rb_lines = re.findall(r'^\s*(?:\|\s*)?(?:\u98ce\u9669\u8fb9\u754c|Risk\s+Boundary)-\d+\s*[:\|]\s*(.+)$', body_clean, re.MULTILINE)
    rb_list = re.findall(r'^\s*[-*]\s*\*\*(?:\u98ce\u9669\u8fb9\u754c|Risk\s+Boundary)-(\d+)\*\*[：:]\s*(.+)$', body_clean, re.MULTILINE)
    for line in rb_lines:
        for kw in rules.get("risk_boundary_abuse_keywords", []):
            if re.search(kw, line, re.IGNORECASE):
                findings.append(Finding("risk-boundary-abuse", msgs["risk_boundary_abuse"].format(keyword=kw, content=line[:60]), "error"))
                break
    for _, content in rb_list:
        for kw in rules.get("risk_boundary_abuse_keywords", []):
            if re.search(kw, content, re.IGNORECASE):
                findings.append(Finding("risk-boundary-abuse", msgs["risk_boundary_abuse"].format(keyword=kw, content=content[:60]), "error"))
                break

    # Professional boundary abuse (bilingual)
    pb_lines = re.findall(r'^\s*(?:\|\s*)?(?:\u4e13\u4e1a\u8fb9\u754c|Professional\s+Boundary)-\d+\s*[:\|]\s*(.+)$', body_clean, re.MULTILINE)
    pb_list = re.findall(r'^\s*[-*]\s*\*\*(?:\u4e13\u4e1a\u8fb9\u754c|Professional\s+Boundary)-(\d+)\*\*[：:]\s*(.+)$', body_clean, re.MULTILINE)
    for line in pb_lines:
        for kw in rules.get("professional_boundary_abuse_keywords", []):
            if re.search(kw, line, re.IGNORECASE):
                findings.append(Finding("professional-boundary-abuse", msgs["professional_boundary_abuse"].format(keyword=kw, content=line[:60]), "error"))
                break
    for _, content in pb_list:
        for kw in rules.get("professional_boundary_abuse_keywords", []):
            if re.search(kw, content, re.IGNORECASE):
                findings.append(Finding("professional-boundary-abuse", msgs["professional_boundary_abuse"].format(keyword=kw, content=content[:60]), "error"))
                break

    # Facet filler (bilingual: \u5207\u9762 = facet)
    facet_lines = re.findall(
        r'^\s*(?:\|\s*)?(?:\u5207\u9762|Facet)(\d)\s*(?:\|.*?\||\*\*(?:\u5207\u9762|Facet)\d[^:]*\*\*[：:]\s*)(.+?)(?:\||$)',
        body_clean,
        re.MULTILINE,
    )
    if not facet_lines:
        facet_lines = re.findall(r'(?:\u5207\u9762|Facet)(\d)\s*[：:]\s*(.+?)(?:\n|$)', body_clean)

    for num, content in facet_lines:
        content_clean = content.strip()
        for pattern in rules.get("facet_filler_patterns", []):
            if re.search(pattern, content_clean, re.IGNORECASE):
                if len(content_clean) >= 25:
                    continue
                findings.append(Finding("facet-filler", msgs["facet_filler"].format(facet=num, content=content_clean[:60]), "error"))
                break

    # Blind spot dumping (bilingual: \u76f2\u533a = blind spot)
    blind_sections = re.findall(
        r'(?:\u76f2\u533a|Blind\s+Spot)[：:]\s*(.+?)(?=\n\n|\n#|\Z)',
        body_clean,
        re.DOTALL,
    )
    for section in blind_sections:
        section_clean = section.strip()
        has_dump = any(re.search(kw, section_clean, re.IGNORECASE) for kw in rules.get("blind_dump_keywords", []))
        has_attempt = "\u5df2\u5c1d\u8bd5" in section_clean or "attempted" in section_clean.lower()
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
        stripped = line.strip()
        if not stripped:
            continue
        # Check Chinese first-person '\u6211' or English 'I' as a word
        has_chinese_wo = '\u6211' in stripped
        has_english_i = bool(re.search(r'\bI\b', stripped)) and not bool(re.search(r'\bI\s+(?:am|will|can|have|need|want|think|believe|do|did|would|should|could|may|might|shall|must|hope|expect|plan|intend|understand|know|see|feel|suggest|recommend|propose|agree|disagree|like|dislike|prefer|choose|decide|determine|create|make|build|write|read|use|apply|follow|implement|develop|design|configure|set|run|execute|perform|start|stop|continue|finish|complete|check|test|verify|validate|confirm|ensure|guarantee|promise|commit|accept|reject|request|ask|answer|respond|reply|tell|speak|talk|say|mention|note|notice|observe|watch|look|listen|hear|smell|taste|touch|feel|try|attempt)\b', stripped, re.IGNORECASE) or re.search(r'\bmy\b|\bme\b|\bmyself\b', stripped, re.IGNORECASE))
        if has_chinese_wo or has_english_i:
            real_line = i + fm_lines
            findings.append(Finding("first-person", msgs["first_person"].format(line=real_line, content=stripped[:80]), "error", real_line))

    desc = ctx.frontmatter.get("description", "")
    if isinstance(desc, str):
        has_chinese_wo = '\u6211' in desc
        has_english_i = bool(re.search(r'\bI\b', desc)) and not bool(re.search(r'\bI\s+(?:am|will|can|have|need|want|think|believe|do|did)\b', desc, re.IGNORECASE))
        if has_chinese_wo or has_english_i:
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
                m = re.search(pattern, stripped, re.IGNORECASE)
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
            m = re.search(pattern, desc, re.IGNORECASE)
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

    rules_heading = config.get("rules", {}).get("rules_heading_pattern", r"^#{2,3}\s*(?:\d+\.?\s*)?(?:[\u89c4\u5219]|[Rr]ules)")
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
        r"^\s*[-*]\s+(?:\*\*)?(?:\u89c4\u5219\d+\s+|Rule\d+\s+)?(.+?)(?:\*\*)?(?:\s|$)",
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
    Bilingual: works with both Chinese and English SKILL content.
    """
    findings: list[Finding] = []
    msgs = config.get("messages", {})
    body = ctx.body

    # Bilingual core patterns
    core_patterns = [
        r'\u6838\u5fc3[:\uff1a]', r'\u6838\u5fc3\u9886\u57df', r'\u6838\u5fc3\u57df',
        r'Core Domain', r'Core[:\uff1a]',
    ]
    has_core = any(re.search(p, body) for p in core_patterns)
    if not has_core:
        findings.append(Finding("capability-no-core", msgs.get("capability_no_core", "Capability matrix missing core domain definition"), "error"))
        return findings

    # --- Format A: letter-prefixed domain entries (A./B./C.) ---
    radiant_patterns = [r'\|\s*%s[\.\s]+\S+' % c for c in 'ABCDEFGH']
    format_a_count = sum(1 for p in radiant_patterns if re.search(p, body, re.MULTILINE))
    domain_headers = re.findall(r'^#{2,4}\s*(?:A|B|C|D|E|F|G|H)\s+[^\n]+', body, re.MULTILINE)
    format_a_count = max(format_a_count, len(domain_headers))

    # --- Format B: table rows in capability section (no prefix, bilingual) ---
    format_b_count = 0
    cap_match = re.search(
        r'(?:###\s+.*?(?:\u80fd\u529b\u77e9\u9635|Capability\s+Matrix)|##\s+.*?(?:\u80fd\u529b\u77e9\u9635|Capability\s+Matrix))',
        body,
    )
    if cap_match:
        cap_start = cap_match.end()
        next_section = re.search(r'^#{2,3}\s+[^#]', body[cap_start:], re.MULTILINE)
        cap_end = cap_start + next_section.start() if next_section else len(body)
        cap_section = body[cap_start:cap_end]
        # Count data rows in tables (skip header rows like "| \u9886\u57df |..." or "|:---|...")
        data_rows = re.findall(
            r'^\|\s*(?!(?:\u9886\u57df|Domain|\u5207\u9762|\u7f16\u53f7|:?--))[^\|\n]+\|.*?\|.*?\|.*?\|',
            cap_section, re.MULTILINE,
        )
        core_rows = [r for r in data_rows if re.search(r'\u6838\u5fc3[:\uff1a]|Core[:\uff1a]', r)]
        radiant_rows = [r for r in data_rows if r not in core_rows]
        format_b_count = len(radiant_rows)

    radiant_count = max(format_a_count, format_b_count)

    if radiant_count < 3:
        findings.append(Finding("capability-few-domains",
            msgs.get("capability_few_domains", "Radiating domains insufficient (min 3, got {count})").format(count=radiant_count),
            "error"))
    elif radiant_count > 8:
        findings.append(Finding("capability-too-many-domains",
            msgs.get("capability_too_many_domains", "Radiating domains too many (max 8, got {count})").format(count=radiant_count),
            "warning"))

    # Check for 4 depth layers (bilingual)
    layer_patterns = [
        r'\u57fa\u7840\u5c42|Foundation',
        r'\u8fdb\u9636\u5c42|Advanced',
        r'\u9ad8\u9636\u5c42|Expert',
        r'\u62d3\u5c55\u5c42|Extension',
    ]
    layer_count = sum(1 for p in layer_patterns if re.search(p, body))
    if layer_count < 4:
        findings.append(Finding("capability-layers-missing",
            msgs.get("capability_layers_missing", "Capability matrix missing 4 depth layers (Foundation/Advanced/Expert/Extension)"),
            "warning"))

    return findings


def _validate_positive_phrasing(ctx: SkillContext, config: dict[str, Any]) -> list[Finding]:
    """Check SHOULD-level rules use positive phrasing (not negative/forbidden phrasing)."""
    findings: list[Finding] = []
    msgs = config.get("messages", {})
    body = ctx.body

    # Locate SHOULD section (bilingual: \u5f3a\u504f\u597d / Strong Preferences / SHOULD)
    should_pattern = r'(?:#{2,4}\s*(?:\d+\.?\s*)?(?:\u5f3a\u504f\u597d|SHOULD|Strong\s+Preferences).*?\n)(.*?)(?=#{2,4}\s|\Z)'
    should_match = re.search(should_pattern, body, re.DOTALL)
    if not should_match:
        return findings

    should_section = should_match.group(1)
    # Negative phrasing patterns (bilingual)
    negative_patterns = [
        r'\u4e0d\u5f97', r'\u7981\u6b62', r'\u4e25\u7981', r'\u5fc5\u987b', r'\u5fc5\u9700',
        r'do not', r"don't", r'shall not', r'must not', r'should not',
    ]
    for i, line in enumerate(should_section.splitlines(), 1):
        stripped = line.strip()
        for np_pattern in negative_patterns:
            if re.search(np_pattern, stripped, re.IGNORECASE):
                findings.append(Finding(
                    "negative-phrasing-in-should",
                    msgs.get("negative_phrasing_in_should", "SHOULD rule contains negative phrasing '{word}': '{content}'").format(word=np_pattern, content=stripped[:80]),
                    "warning",
                ))
                break

    return findings
