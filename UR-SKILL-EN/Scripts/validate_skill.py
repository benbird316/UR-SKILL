#!/usr/bin/env python3
"""
SKILL Static Validation Script

Purpose: Automatically check SKILL.md format, content, reference consistency, and anti-patterns before delivery.
Core Principle: All rules must be programmatically verifiable to avoid manual line-by-line inspection.
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path


try:
    import yaml  # type: ignore

    HAS_YAML = True
except ImportError:  # pragma: no cover
    HAS_YAML = False


# ----------------------------- Configuration -----------------------------

MAX_BODY_LINES = 500
MAX_DESCRIPTION_CHARS = 200
MIN_DESCRIPTION_CHARS = 50
PLACEHOLDER_PATTERNS = [
    # Match [xxx] placeholders, but exclude Markdown links [text](url) and legitimate markers [cognitive operation]
    r"\[(?!cognitive operation\])(?![^\]]*\]\()[^\]]*\]",
    r"\{.*?\}",
    r"TODO|FIXME|XXX|HACK",
]

REQUIRED_FRONTMATTER_FIELDS = {
    "name": str,
    "description": str,
    "type": str,
    "whenToUse": str,
    "metadata": dict,
}

VALID_TYPES = {"prompt", "tool", "hybrid"}

# Risk boundary keywords (only applicable to UR-SKILL self-validation;
# risk boundaries of other SKILLs are determined by domain security requirements)
RISK_BOUNDARIES = [
    "illegal",
    "discrimination",
    "malicious injection",
]

# Step name -> Expected number of check items (review dimensions + risk boundary gate)
STEP_EXPECTED_COUNTS = {
    "Parse": 3,
    "Pre-Analysis": 4,
    "Research": 7,
    "Architecture": 7,
    "Execute": 4,
    "Deliver": 4,
    "Verify": 7,
    "Validate": 8,
}

# Steps that have the full 6 review dimensions (critical checkpoints)
CRITICAL_STEPS = {"Research", "Architecture", "Verify", "Validate"}

# 6 review dimensions that critical nodes must cover
REQUIRED_DIMENSIONS = [
    "Goal Alignment",
    "Fact Anchoring",
]

CRITICAL_ONLY_DIMENSIONS = [
    "Direction Calibration",
    "Adversarial Validation",
    "Blind Spot Identification",
    "Impact Projection",
]

# RFC 2119 keywords
RFC2119_KEYWORDS = ["MUST", "MUST NOT", "SHOULD", "SHOULD NOT", "MAY"]

# Risk boundary abuse detection keywords (capability degradation language -- should not appear in risk boundaries)
# Risk boundaries only declare safety red lines; any "not responsible / only does X not Y" is abuse
RB_ABUSE_KEYWORDS = [
    r"not responsible", r"does not belong", r"outside the scope", r"not in charge of", r"does not assume",
    r"only does.*not do", r"limited to", r"does not involve", r"does not include",
]

# Professional boundary abuse detection keywords (capability degradation language -- should not appear in professional boundaries)
# Professional boundaries can describe "does not include X" (e.g., "does not include specific buy/sell prices"),
# but must not be capability degradation ("only does X not Y" where Y is a natural extension of X)
PB_ABUSE_KEYWORDS = [
    r"not responsible", r"only does.*not do", r"not in charge of", r"does not assume",
]

# Facet filler detection patterns (generic boilerplate)
FACET_FILLER_PATTERNS = [
    r"master relevant domain knowledge",
    r"familiar with (?:relevant )?domain (?:knowledge|standards)",
    r"identify potential risks",
    r"ensure output quality",
    r"consider global impact",
    r"optimize resource investment",
    r"analyze task complexity",
    r"ensure.*quality",
]

# Blind spot dumping detection keywords
BLIND_DUMP_KEYWORDS = [
    r"for reference only",
    r"please verify yourself",
    r"there may be.*blind spots",
    r"does not guarantee.*(?:completeness|accuracy)",
    r"please.*(?:check|verify|confirm) before use",
]


# ----------------------------- Tool Binding Detection -----------------------------

# Common Agent tool names (case-insensitive matching)
KNOWN_TOOLS = [
    "Read", "Write", "Edit", "DeleteFile",
    "RunCommand", "CheckCommandStatus", "StopCommand",
    "Grep", "Glob", "LS", "SearchCodebase",
    "WebSearch", "WebFetch",
    "AskUserQuestion", "NotifyUser",
    "Task", "Skill", "run_mcp",
    "TodoWrite", "OpenPreview", "GetDiagnostics",
]

# Review / testing type SKILL keywords
CRT_KEYWORDS = [
    "review", "test", "audit", "scan",
    "code-review", "security-review", "quality",
]

# Output specification mandatory check items
OUTPUT_SPEC_CHECKS = {
    "mermaid": {
        "patterns": [r"mermaid", r"flowchart", r"sequenceDiagram", r"classDiagram", r"stateDiagram"],
        "label": "Mermaid visualization requirement",
    },
    "severity": {
        "patterns": [r"(Critical|High|Medium|Low).*severity", r"(Critical|High|Medium|Low).*level"],
        "label": "Issue severity classification",
    },
    "interaction": {
        "patterns": [r"AskUserQuestion", r"confirm.*fix.*verify.*loop", r"phased delivery", r"user interaction mode"],
        "label": "User interaction mode",
    },
    "decision": {
        "patterns": [r"decision strategy", r"block.*merge", r"suggest.*merge", r"Pass\|Revision Required\|Block"],
        "label": "Decision strategy",
    },
}


# ----------------------------- Utility Functions -----------------------------

def parse_frontmatter(text: str) -> tuple[dict | None, str, list[str]]:
    """Parse YAML frontmatter and body content."""
    errors: list[str] = []
    if not text.startswith("---"):
        errors.append("SKILL.md must start with `---`")
        return None, text, errors

    parts = text.split("---", 2)
    if len(parts) < 3:
        errors.append("Cannot parse frontmatter: missing second `---` delimiter")
        return None, text, errors

    fm_text = parts[1].strip()
    body = parts[2].strip()

    if not HAS_YAML:
        errors.append("PyYAML not installed, skipping frontmatter field type validation (run `pip install pyyaml`)")
        # Simple regex fallback: only check field existence
        fm_data: dict = {}
        for key in REQUIRED_FRONTMATTER_FIELDS:
            if key == "metadata":
                if re.search(rf"^{re.escape(key)}:\s*$", fm_text, re.MULTILINE):
                    fm_data[key] = {}
            else:
                match = re.search(rf"^{re.escape(key)}:\s*(.+)$", fm_text, re.MULTILINE)
                if match:
                    fm_data[key] = match.group(1).strip().strip('"')
        return fm_data, body, errors

    try:
        fm_data = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError as exc:
        errors.append(f"frontmatter YAML parse failed: {exc}")
        return None, body, errors

    return fm_data, body, errors


def validate_frontmatter(fm: dict) -> list[str]:
    """Validate frontmatter fields and format."""
    errors: list[str] = []

    for field, expected_type in REQUIRED_FRONTMATTER_FIELDS.items():
        if field not in fm:
            errors.append(f"frontmatter missing required field: {field}")
            continue
        if expected_type is dict:
            if not isinstance(fm[field], dict):
                errors.append(f"frontmatter field {field} must be a dict")
            continue
        if not isinstance(fm[field], expected_type):
            errors.append(f"frontmatter field {field} wrong type, expected {expected_type.__name__}")

    if "name" in fm:
        name = fm["name"]
        if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", name):
            errors.append(f"name '{name}' is not valid kebab-case")

    if "description" in fm:
        desc = fm["description"]
        if len(desc) < MIN_DESCRIPTION_CHARS or len(desc) > MAX_DESCRIPTION_CHARS:
            errors.append(
                f"description length {len(desc)} not within {MIN_DESCRIPTION_CHARS}-{MAX_DESCRIPTION_CHARS} range"
            )

    if "type" in fm and fm["type"] not in VALID_TYPES:
        errors.append(f"type '{fm['type']}' is not a valid value {VALID_TYPES}")

    if isinstance(fm.get("metadata"), dict):
        updated = fm["metadata"].get("updated")
        if not updated:
            errors.append("metadata.updated missing")
        else:
            try:
                datetime.strptime(str(updated), "%Y-%m-%d")
            except ValueError:
                errors.append(f"metadata.updated '{updated}' is not YYYY-MM-DD format")

    return errors


def validate_quality(body: str) -> list[str]:
    """Validate risk boundary abuse, facet filler, blind spot dumping, and other quality issues."""
    errors: list[str] = []

    # Exclude code block content (counterexample teaching)
    body_clean = re.sub(r'```[\s\S]*?```', '', body)

    # ---- Risk Boundary Abuse Detection ----
    # Extract all Risk Boundary declaration lines
    rb_lines = re.findall(r'^\s*(?:\|\s*)?Risk Boundary-\d+\s*[:\|]\s*(.+)$', body_clean, re.MULTILINE)
    # Also match list format: - **Risk Boundary-01**: xxx
    rb_list = re.findall(r'^\s*[-*]\s*\*\*Risk Boundary-(\d+)\*\*[：:]\s*(.+)$', body_clean, re.MULTILINE)

    # Check risk boundary abuse: risk boundary declarations must not contain disclaimer language
    for line in rb_lines:
        for kw in RB_ABUSE_KEYWORDS:
            if re.search(kw, line):
                errors.append(f"Risk boundary abuse: suspected disclaimer language '{kw}' -> '{line[:60]}...'")
                break

    for _, content in rb_list:
        for kw in RB_ABUSE_KEYWORDS:
            if re.search(kw, content):
                errors.append(f"Risk boundary abuse: suspected disclaimer language '{kw}' -> '{content[:60]}...'")
                break

    # ---- Professional Boundary Abuse Detection ----
    # Extract all Professional Boundary declaration lines
    pb_lines = re.findall(r'^\s*(?:\|\s*)?Professional Boundary-\d+\s*[:\|]\s*(.+)$', body_clean, re.MULTILINE)
    pb_list = re.findall(r'^\s*[-*]\s*\*\*Professional Boundary-(\d+)\*\*[：:]\s*(.+)$', body_clean, re.MULTILINE)

    # Check professional boundary abuse: professional boundary declarations must not contain capability degradation language
    for line in pb_lines:
        for kw in PB_ABUSE_KEYWORDS:
            if re.search(kw, line):
                errors.append(f"Professional boundary abuse: suspected capability degradation '{kw}' -> '{line[:60]}...'")
                break

    for _, content in pb_list:
        for kw in PB_ABUSE_KEYWORDS:
            if re.search(kw, content):
                errors.append(f"Professional boundary abuse: suspected capability degradation '{kw}' -> '{content[:60]}...'")
                break

    # ---- Facet Filler Detection ----
    # Extract all Facet N lines (facet definition lines)
    facet_lines = re.findall(
        r'^\s*(?:\|\s*)?Facet(\d)\s*(?:\|.*?\||\*\*Facet\d[^:]*\*\*[：:]\s*)(.+?)(?:\||$)',
        body_clean,
        re.MULTILINE,
    )
    if not facet_lines:  # Fallback: match more lenient formats
        facet_lines = re.findall(
            r'Facet(\d)\s*[：:]\s*(.+?)(?:\n|$)',
            body_clean,
        )

    for num, content in facet_lines:
        content_clean = content.strip()
        for pattern in FACET_FILLER_PATTERNS:
            if re.search(pattern, content_clean):
                # Rich facet content (> 25 chars) passes even if it contains generic terms (task-anchored)
                if len(content_clean) >= 25:
                    continue
                # Otherwise: too short + matches boilerplate pattern = suspected filler
                errors.append(
                    f"Facet filler: Facet {num} too brief, suspected boilerplate '{content_clean[:60]}'"
                )
                break  # Only report once per facet

    # ---- Blind Spot Dumping Detection ----
    # Locate blind spot related paragraphs
    blind_sections = re.findall(
        r'(?:Blind Spot|blind spot)[：:]\s*(.+?)(?=\n\n|\n#|\Z)',
        body_clean,
        re.DOTALL,
    )
    for section in blind_sections:
        section_clean = section.strip()
        # Check for disclaimer keywords
        has_dump = any(re.search(kw, section_clean) for kw in BLIND_DUMP_KEYWORDS)
        # Check for "attempted" field
        has_attempt = "attempted" in section_clean.lower()
        if has_dump and not has_attempt:
            errors.append(
                f"Blind spot dumping: purely declarative blind spot (no 'attempted actions')"
            )

    return errors


def validate_first_person(body: str, fm: dict | None = None) -> list[str]:
    """Check whether SKILL.md uses the first person "I".

    "I" confuses LLM persona attribution -- system prompts should always use "You are an X" not "I am an X".
    Excludes code block content (may be user example input).
    Also checks frontmatter description for "I".
    """
    errors: list[str] = []
    body_clean = re.sub(r'```[\s\S]*?```', '', body)

    for i, line in enumerate(body_clean.splitlines(), 1):
        if 'I ' in line or line.strip() == 'I' or ' I ' in line or line.startswith('I ') or line.endswith(' I'):
            stripped = line.strip()
            if stripped:
                errors.append(
                    f"First person: line {i} contains 'I', should use 'you' or no subject -> '{stripped[:80]}'"
                )

    # Check frontmatter description
    if fm:
        desc = fm.get("description", "")
        if isinstance(desc, str) and ' I ' in desc:
            errors.append(
                f"First person: frontmatter description contains 'I', should use no subject -> '{desc[:80]}'"
            )

    return errors


def validate_identity_title(body: str, fm: dict | None = None) -> list[str]:
    """Check identity declarations for inflated titles (expert / professor / master / guru etc.).

    Research basis:
    - USC 2026.3: Hollow identities cause knowledge retrieval to drop from 71.6% to 66.3%
    - Wharton 2025.12: Exaggerated identities lead to overconfidence and fabrication
    """
    errors: list[str] = []
    inflated_titles = [
        "expert", "professor", "master", "guru", "veteran", "senior", "top-tier", "leading",
    ]
    experience_patterns = [
        r"\d+\s*years.*experience",  # "5 years of experience", "10+ years"
        r"\d+\+?\s*years.*experience",
    ]

    # Check identity lines and description paragraphs in body
    for i, line in enumerate(body.split("\n"), 1):
        stripped = line.strip()
        # Identify identity declaration lines or related descriptions
        if any(keyword in stripped for keyword in ("**Identity**:", "**Role**:", "Identity:", "Role:")):
            # Check inflated titles
            for title in inflated_titles:
                if title.lower() in stripped.lower():
                    errors.append(
                        f"Inflated title: body line {i} contains '{title}', "
                        f"should use specific profession name (engineer / analyst / reviewer), not hollow title"
                    )
                    break
            # Check fabricated experience years
            for pattern in experience_patterns:
                m = re.search(pattern, stripped, re.IGNORECASE)
                if m:
                    errors.append(
                        f"Fabricated years: body line {i} contains '{m.group()}', "
                        f"LLMs have no concept of 'years of experience', should use domain / methodology description instead"
                    )
                    break

    # Check frontmatter description
    if fm:
        desc = fm.get("description", "")
        for title in inflated_titles:
            if title.lower() in desc.lower():
                errors.append(
                    f"Inflated title: frontmatter description contains '{title}', "
                    f"should use specific profession name"
                )
                break
        for pattern in experience_patterns:
            m = re.search(pattern, desc, re.IGNORECASE)
            if m:
                errors.append(
                    f"Fabricated years: frontmatter description contains '{m.group()}', "
                    f"LLMs have no concept of 'years of experience', should use domain / methodology description instead"
                )
                break

    return errors


def validate_tool_name_migration(body: str) -> list[str]:
    """Check for deprecated tool names (e.g., SearchReplace should be Edit)."""
    errors: list[str] = []
    if "SearchReplace" in body:
        errors.append("Tool name migration: found 'SearchReplace', should use 'Edit' instead")
    return errors


def validate_body(body: str, fm: dict | None = None) -> list[str]:
    """Validate body content."""
    errors: list[str] = []
    lines = body.splitlines()

    # Exclude placeholder false positives from code blocks and Mermaid blocks
    body_clean = re.sub(r'```[\s\S]*?```', '', body)

    if len(lines) > MAX_BODY_LINES:
        errors.append(f"body line count {len(lines)} exceeds threshold {MAX_BODY_LINES}")

    for pattern in PLACEHOLDER_PATTERNS:
        matches = set(re.findall(pattern, body_clean, re.IGNORECASE))
        filtered = []
        for m in matches:
            # Skip Markdown checkboxes [ ] / [x]
            if m in ("[ ]", "[x]", "[X]"):
                continue
            # Skip Markdown links [text](url)
            if re.match(r"^\[.*\]\(.*\)$", m):
                continue
            # Skip format specifier placeholder templates like [toolname], [filename] etc.
            if m in ("[toolname]", "[filename]", "[dirname]", "[parameter]", "[operation]"):
                continue
            # Skip workflow node labels: [Critical Checkpoint, ...] / [Non-Critical Checkpoint, ...]
            if re.match(r"^\[(Critical|Non-Critical) (node|Checkpoint)", m):
                continue
            # Skip tool reference format [Read], [Write], [AskUserQuestion] etc.
            if re.match(r"^\[[A-Z][a-zA-Z]+\]$", m):
                continue
            # Skip Mermaid node text ["xxx"] format
            if re.match(r'^\[".*"\]$', m):
                continue
            # Skip Mermaid node nesting ["[xxx] ..."] format
            if re.match(r'^\["\[.*\].*"\]$', m):
                continue
            # Skip tool invocation format [xxx] appearing anywhere
            if re.match(r'^\[(Read|Write|AskUserQuestion|NotifyUser|RunCommand|Grep|Glob|Task|Skill|DeleteFile|Edit|TodoWrite)\b', m):
                continue
            # Skip Mermaid node fragments ["[xxx] (starting with bracket but not closed)
            if m.startswith('["[') or m.startswith('["') :
                continue
            filtered.append(m)
        if filtered:
            should_report = True
            # For {} patterns: skip template variable format
            if pattern == r"\{.*?\}":
                real_placeholders = [m for m in filtered if not re.match(r'^\{[A-Za-z\u4e00-\u9fff].*\}$', m)]
                real_placeholders = [m for m in real_placeholders if m != '{date}']
                if real_placeholders:
                    errors.append(f"Suspected placeholder residue ({pattern}): {real_placeholders[:5]}")
                should_report = False  # Already handled by branch above
            if should_report:
                errors.append(f"Suspected placeholder residue ({pattern}): {filtered[:5]}")

    # RISK_BOUNDARIES keyword check only applies to UR-SKILL itself
    # Risk boundaries of other SKILLs are determined by domain security requirements and should not be hardcoded
    is_UR_SKILL = fm and fm.get("name", "") == "ur-skill"
    if is_UR_SKILL:
        for rb in RISK_BOUNDARIES:
            if rb not in body_clean:
                errors.append(f"Missing risk boundary declaration: {rb}")

    return errors


def validate_tool_binding(body: str, fm: dict | None = None) -> list[str]:
    """Validate whether actions in workflow steps are bound to concrete tools.

    Format requirement: each executable action contains `[ToolName] operation -> output` format tool calls.
    UR-SKILL itself is exempt from this check (its tool calls are outside the body).
    """
    errors: list[str] = []

    # UR-SKILL's own SKILL does not apply to this check
    if fm and fm.get("name") in ("ur-skill", "pre-analysis-engineer"):
        return errors

    # Locate the workflow block (adapted for "## Workflow", "## 3. Workflow" etc. formats)
    workflow_match = re.search(r"^#{2,3}\s*(?:\d+\.?\s*)?(?:Workflow|[Ww]orkflow)", body, re.MULTILINE)
    if not workflow_match:
        return errors  # Non-runtime SKILL, skip

    wf_start = workflow_match.end()
    next_section = re.search(r"^#{2,3}\s+(?!\d|Workflow|[Ww]orkflow).*?\n", body[wf_start:], re.MULTILINE)
    wf_end = wf_start + next_section.start() if next_section else len(body)
    workflow_body = body[wf_start:wf_end]

    # Extract all action lines (numbered list items)
    action_lines = re.findall(
        r"^\s*\d+\.\s+(.+)",
        workflow_body,
        re.MULTILINE,
    )

    tool_pattern = re.compile(r"\[([A-Za-z_][A-Za-z0-9_]*)\]")

    has_any_tool = False
    unbound_lines = []

    for i, line in enumerate(action_lines):
        line_clean = line.strip()
        # Skip pure description lines (non-actions)
        if line_clean.lower().startswith(("read", "confirm", "check", "assemble", "summarize", "simulate", "populate")):
            # These are UR-SKILL's own meta-operations, tool binding not enforced
            continue
        # Handle [cognitive operation]: pure cognitive operations (no external tools) are skipped;
        # lines mixed with real tools continue to check
        if "cognitive operation" in line_clean.lower():
            remaining = re.sub(r"\[cognitive operation\]", "", line_clean, flags=re.IGNORECASE)
            other_tools = tool_pattern.findall(remaining)
            if not other_tools:
                continue  # Pure cognitive operation, no external tool binding
            # Has cognitive operation + external tools -> continue through tool binding check below
        # Skip "why", "design rationale" etc. explanatory lines
        if re.match(r"(why|design rationale|note|explanation)", line_clean.lower()):
            continue

        matches = tool_pattern.findall(line_clean)
        if matches:
            has_any_tool = True
            # Verify tool names are in the known list
            for tool_name in matches:
                if tool_name not in KNOWN_TOOLS:
                    # Not a known tool but not a fatal error -- may be a custom tool
                    pass
        else:
            # Only report lines that look like actions (contain verbs)
            if re.search(r"(read|call|execute|run|search|create|write|edit|delete|open)", line_clean.lower()):
                unbound_lines.append(f"  L{i+1}: {line_clean[:60]}...")

    # Only report error when there are tool-bound actions elsewhere but some actions lack tool binding
    if has_any_tool and unbound_lines:
        errors.append(
            f"Tool binding missing: the following actions are not bound to tools (format [ToolName] operation -> output), "
            f"but other actions in the same SKILL are bound to tools:\n" + "\n".join(unbound_lines[:5])
        )
    elif not has_any_tool and action_lines:
        # No explicit tool bindings but has actions -- this is characteristic of the FL system (relies on built-in tools)
        # Do not enforce error, only provide info
        pass

    return errors


def validate_output_spec(body: str, fm: dict | None) -> list[str]:
    """Check whether review / testing type SKILLs include necessary output specifications.

    Review / testing type = Code Review / Test / Security Audit type SKILLs.
    Check items: Mermaid visualization, issue severity classification, decision strategy, user interaction mode.
    """
    errors: list[str] = []

    if fm is None:
        return errors

    name = str(fm.get("name", "")).lower()
    desc = str(fm.get("description", "")).lower()

    # Determine if this is a review / testing type SKILL
    is_crt = any(kw in name for kw in CRT_KEYWORDS) or any(kw in desc for kw in CRT_KEYWORDS)
    if not is_crt:
        return errors

    # Review / testing type SKILL: check 4 output specification items
    for key, spec in OUTPUT_SPEC_CHECKS.items():
        found = any(re.search(pat, body) for pat in spec["patterns"])
        if not found:
            errors.append(
                f"Review / testing type SKILL missing {spec['label']}: "
                f"did not detect patterns related to {spec['patterns'][:2]}"
            )

    return errors


def validate_workflow(body: str) -> list[str]:
    """Validate workflow node check item count and content dimensions."""
    errors: list[str] = []

    # Match the title and checklist of each workflow step
    # Adapts to English headings: "## 1. Research (Critical Node, 6 dimensions)"
    step_pattern = re.compile(
        r"^#{2,4}\s*\d+\.\s*(\S+?)\s*\(.*?\).*?(?:dimension|dimensions).*$",
        re.MULTILINE,
    )

    for match in step_pattern.finditer(body):
        step_name = match.group(1)
        # From current match position to before the next same-level heading
        start = match.end()
        next_match = step_pattern.search(body, start)
        end = next_match.start() if next_match else len(body)
        section = body[start:end]

        check_count = section.count("- [ ]") + section.count("- [x]")

        if step_name in STEP_EXPECTED_COUNTS:
            expected = STEP_EXPECTED_COUNTS[step_name]
            if check_count != expected:
                errors.append(
                    f"Step '{step_name}' check item count {check_count}, expected {expected}"
                )

        # ------ Check Item Dimension Content Validation ------
        # Extract all check item texts in this step
        checklist_items = re.findall(
            r"- \[[ x]\]\s*(.+?)(?=\n- \[|$)",
            section,
            re.DOTALL,
        )

        # Collect dimension names covered by this step
        covered = set()
        for item in checklist_items:
            item_text = item.strip().split("\n")[0]  # Only take the first line of the check item title
            # Remove Markdown bold markers for matching
            clean_text = re.sub(r"\*\*(.+?)\*\*", r"\1", item_text)
            for dim in REQUIRED_DIMENSIONS + CRITICAL_ONLY_DIMENSIONS:
                if dim in clean_text:
                    covered.add(dim)

        # All steps must cover these 2 dimensions
        for dim in REQUIRED_DIMENSIONS:
            if dim not in covered:
                errors.append(
                    f"Node '{step_name}' missing required dimension: {dim}"
                )

        # Critical nodes additionally cover 4 dimensions
        if step_name in CRITICAL_STEPS:
            for dim in CRITICAL_ONLY_DIMENSIONS:
                if dim not in covered:
                    errors.append(
                        f"Critical node '{step_name}' missing dimension: {dim}"
                    )

    return errors


# ----------------------------- UR-SKILL File Leak Detection -----------------------------

def _discover_UR_SKILL_files() -> set[str]:
    """Dynamically discover all files belonging to UR-SKILL itself (relative path set)."""
    script_dir = Path(__file__).resolve().parent
    UR_SKILL_root = script_dir.parent
    files: set[str] = set()
    for f in UR_SKILL_root.rglob("*"):
        if f.is_file() and not f.name.startswith("."):
            rel = f.relative_to(UR_SKILL_root).as_posix()
            # Only record files under UR-SKILL-specific directories (won't appear in generated SKILLs)
            if any(
                rel.startswith(prefix)
                for prefix in ("design-guides/", "templates/", "design-rationale/", "Scripts/")
            ):
                files.add(rel)
            # Specific References files (non-generic names)
            elif rel in ("References/pre-analysis.md",):  # Migrated to design-rationale, backward compatible
                files.add(rel)
            # Sub-SKILL files
            elif rel in ("agent/SKILL.md",):
                files.add(rel)
    return files


# Cache
_UR_SKILL_FILES: set[str] | None = None


def _get_UR_SKILL_files() -> set[str]:
    """Get UR-SKILL's own file list (cached)."""
    global _UR_SKILL_FILES
    if _UR_SKILL_FILES is None:
        _UR_SKILL_FILES = _discover_UR_SKILL_files()
    return _UR_SKILL_FILES


def validate_UR_SKILL_file_leaks(body: str, fm: dict | None = None) -> list[str]:
    """Check whether the generated SKILL leaks UR-SKILL internal file references.

    Self-containment rule: generated SKILLs MUST NOT reference UR-SKILL's own files (content under
    design-guides/, templates/, design-rationale/, Scripts/ directories).
    Skip check when fm.name is 'ur-skill' or 'pre-analysis-engineer'.
    """
    errors: list[str] = []

    # UR-SKILL's own SKILL necessarily references internal files, skip
    if fm and fm.get("name") in ("ur-skill", "pre-analysis-engineer"):
        return errors

    # Exclude code block content (avoid false positives from paths in example code)
    body_clean = re.sub(r'```[\s\S]*?```', '', body)

    UR_SKILL_files = _get_UR_SKILL_files()
    if not UR_SKILL_files:
        return errors  # Cannot discover UR-SKILL files, skip

    # Scan body for references to UR-SKILL files
    leaked: set[str] = set()
    for sb_file in UR_SKILL_files:
        escaped = re.escape(sb_file)
        # Match various reference formats: [text](path), bare path, ./path, ../path, /path
        patterns = [
            rf'\b{escaped}\b',               # Bare path: design-guides/xxx.md
            rf'\./{escaped}\b',             # ./ prefix
            rf'\.\.\/{escaped}\b',          # ../ prefix
        ]
        for pat in patterns:
            if re.search(pat, body_clean):
                leaked.add(sb_file)
                break  # Only report once per file

    for f in sorted(leaked):
        errors.append(
            f"UR-SKILL file reference leak: generated SKILL references '{f}', "
            f"violating self-containment rule (MUST NOT reference UR-SKILL internal files)"
        )

    return errors


# ----------------------------- Unresolved Placeholder Detection -----------------------------

# Placeholder patterns from output-template.md (must be filled)
UNRESOLVED_PLACEHOLDER_PATTERNS: list[tuple[str, str]] = [
    # Basic placeholders
    (r'\{kebab-case-name\}', 'name placeholder'),
    (r'\{SKILL name\}', 'title placeholder'),
    (r'\{YYYY-MM-DD\}', 'date placeholder'),
    # Capability architecture placeholders
    (r'\{core domain name\}', 'core domain name placeholder'),
    (r'\{domain\d\}', 'radiating domain name placeholder'),
    # Boundary placeholders
    (r'\{This SKILL (?:must not cross|does not cross).*(?:safety red line|professional domain boundary)\}', 'boundary declaration placeholder'),
    # Output specification placeholders
    (r'\{natural language/structured/hybrid[,，]\s*brief description\}', 'output format description placeholder'),
    (r'\{format type\}', 'output format type placeholder'),
    (r'\{Mermaid \{type\}\}', 'Mermaid type placeholder'),
    (r'\{N\}', 'loop round count placeholder'),
    (r'\{fill color\}', 'Mermaid fill color placeholder'),
    (r'\{text color\}', 'Mermaid text color placeholder'),
    # Example placeholders
    (r'\{scenario\}', 'example scenario placeholder'),
    (r'\{user input content\}', 'example input placeholder'),
    (r'\{expected output content[^}]*\}', 'example output placeholder'),
    # General placeholders
    (r'\{N months\}', 'review period placeholder'),
    (r'\{MAJOR\.MINOR\.PATCH\}', 'semantic version placeholder'),
]


def validate_unresolved_placeholders(body: str) -> list[str]:
    """Check whether generated SKILL has residual unfilled template placeholders.

    Only checks specific placeholder patterns from output-template.md to avoid false positives from generic {} usage.
    """
    errors: list[str] = []

    # Exclude code blocks (placeholders in examples are for teaching)
    body_clean = re.sub(r'```[\s\S]*?```', '', body)
    # Also exclude YAML frontmatter
    body_no_fm = re.sub(r'^---[\s\S]*?---', '', body_clean)

    for pattern, label in UNRESOLVED_PLACEHOLDER_PATTERNS:
        matches = re.findall(pattern, body_no_fm)
        if matches:
            errors.append(
                f"Placeholder unfilled: found {len(matches)} occurrence(s) of '{label}'"
            )

    return errors


def _check_ref_exists(rel_path: str, skill_dir: Path) -> bool:
    """Check whether the referenced file exists in skill_dir or its parent directory (for subdirectory example SKILLs)."""
    # Standard location
    if (skill_dir / rel_path).exists():
        return True
    # Subdirectory example SKILLs may reference project root directory files
    if skill_dir.parent and (skill_dir.parent / rel_path).exists():
        return True
    return False


def validate_references(body: str, skill_dir: Path) -> list[str]:
    """Validate whether files referenced in the body under references/, scripts/, assets/, design-guides/, templates/ exist."""
    errors: list[str] = []
    refs = re.findall(r"[Rr]eferences/([a-zA-Z0-9_\-\./]+)", body)
    scr = re.findall(r"[Ss]cripts/([a-zA-Z0-9_\-\./]+)", body)
    ast = re.findall(r"assets/([a-zA-Z0-9_\-\./]+)", body)
    dg = re.findall(r"[Dd]esign-[Gg]uides/([a-zA-Z0-9_\-\./]+)", body)
    tpl = re.findall(r"[Tt]emplates/([a-zA-Z0-9_\-\./]+)", body)

    for ref in set(refs):
        if not _check_ref_exists(f"References/{ref}", skill_dir):
            errors.append(f"Referenced reference file does not exist: References/{ref}")

    for script in set(scr):
        if not _check_ref_exists(f"Scripts/{script}", skill_dir):
            errors.append(f"Referenced script file does not exist: Scripts/{script}")

    for asset in set(ast):
        if not _check_ref_exists(f"assets/{asset}", skill_dir):
            errors.append(f"Referenced asset file does not exist: assets/{asset}")

    for guide in set(dg):
        if not _check_ref_exists(f"design-guides/{guide}", skill_dir):
            errors.append(f"Referenced design-guide file does not exist: design-guides/{guide}")

    for template in set(tpl):
        if not _check_ref_exists(f"templates/{template}", skill_dir):
            errors.append(f"Referenced template file does not exist: templates/{template}")

    return errors


def validate_file_dependency_decision(body: str) -> list[str]:
    """Validate whether the file dependency decision is executed in the workflow.

    Checks whether the workflow block contains "file dependency decision" or "pre-analysis.md section 2" or "design-rationale.md section 9" instructions.
    SKILLs with "Medium" or "Complex" complexity MUST execute this decision before creating references/ etc. files.
    """
    errors: list[str] = []

    # Locate the workflow block
    workflow_match = re.search(r"^#{2,3}\s*(?:\d+\.?\s*)?(?:Workflow|[Ww]orkflow)", body, re.MULTILINE)
    if not workflow_match:
        return errors

    wf_start = workflow_match.end()
    next_section = re.search(r"^#{2,3}\s+(?!\d|Workflow|[Ww]orkflow).*?\n", body[wf_start:], re.MULTILINE)
    wf_end = wf_start + next_section.start() if next_section else len(body)
    workflow_section = body[wf_start:wf_end]

    has_decision = (
        "file dependency decision" in workflow_section.lower()
        or "pre-analysis.md section 2" in workflow_section.lower()
        or "pre-analysis.md#2" in workflow_section
        or "design-rationale.md section 9" in workflow_section.lower()
        or "design-rationale.md#9" in workflow_section
    )
    if not has_decision:
        errors.append(
            "File dependency decision missing: no 'file dependency decision' instruction found in workflow"
            " (should add 'file dependency decision' or reference pre-analysis.md section 2 or design-rationale.md section 9)"
        )

    return errors


def validate_rfc2119(body: str) -> list[str]:
    """Validate whether the rules block uses RFC 2119 keywords."""
    errors: list[str] = []

    # Locate the rules block (search by heading name, not dependent on fixed numbering)
    # Match "## Rules", "## 5. Rules" etc. formats
    rules_match = re.search(r"^#{2,3}\s*(?:\d+\.?\s*)?[Rr]ules\s*$", body, re.MULTILINE)
    if not rules_match:
        errors.append("Rules block not found (heading should contain 'Rules')")
        return errors

    start = rules_match.end()
    # Find the next same-level (same # count) heading as the end
    level = len(rules_match.group(0)) - len(rules_match.group(0).lstrip('#'))
    next_section = re.search(r"^#{%d,%d}\s+(?:\d+\.?\s*)?(?!Rules|[Rr]ules).*?\n" % (level, level), body[start:], re.MULTILINE)
    end = start + next_section.start() if next_section else len(body)
    rules_section = body[start:end]

    # Extract all rule entries
    # Adapt to format: "- **Rule01 MUST** ..." or "- **Rule01 MUST NOT** ..."
    # After extracting full entry content, skip the numbering prefix and check if it starts with RFC2119 keywords
    rule_lines = re.findall(
        r"^\s*[-*]\s+(?:\*\*)?(?:Rule\d+\s+)?(.+?)(?:\*\*)?(?:\s|$)",
        rules_section,
        re.MULTILINE,
    )

    if not rule_lines:
        # Fallback: more lenient matching
        rule_lines = re.findall(
            r"^\s*[-*]\s+.*?(MUST NOT|MUST|SHOULD NOT|SHOULD|MAY)\s",
            rules_section,
            re.MULTILINE,
        )

    if not rule_lines:
        errors.append("No rule entries found in rules block (bullet list)")
        return errors

    # Check whether each rule starts with an RFC 2119 keyword
    for idx, item in enumerate(rule_lines, 1):
        item_clean = re.sub(r"\*\*", "", item).strip()
        has_keyword = any(
            item_clean.upper().startswith(kw) for kw in RFC2119_KEYWORDS
        )
        if not has_keyword:
            errors.append(
                f"Rule{idx:02d} does not use RFC 2119 keyword: '{item_clean[:60]}...'"
            )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="Validate SKILL.md quality")
    parser.add_argument(
        "--skill-dir",
        type=Path,
        default=Path("."),
        help="SKILL directory (contains SKILL.md and references/)",
    )
    args = parser.parse_args()

    skill_file = args.skill_dir / "SKILL.md"
    if not skill_file.exists():
        print(f"Error: {skill_file} not found", file=sys.stderr)
        return 1

    text = skill_file.read_text(encoding="utf-8")
    fm, body, fm_parse_errors = parse_frontmatter(text)
    all_errors = list(fm_parse_errors)

    if fm is not None:
        all_errors.extend(validate_frontmatter(fm))

    all_errors.extend(validate_body(body, fm))
    all_errors.extend(validate_tool_name_migration(body))
    all_errors.extend(validate_workflow(body))
    all_errors.extend(validate_references(body, args.skill_dir))
    all_errors.extend(validate_rfc2119(body))
    all_errors.extend(validate_quality(body))
    all_errors.extend(validate_first_person(body, fm))
    all_errors.extend(validate_tool_binding(body, fm))
    all_errors.extend(validate_output_spec(body, fm))
    all_errors.extend(validate_file_dependency_decision(body))
    all_errors.extend(validate_UR_SKILL_file_leaks(body, fm))
    all_errors.extend(validate_unresolved_placeholders(body))
    all_errors.extend(validate_identity_title(body, fm))

    if all_errors:
        print(f"Validation failed: {len(all_errors)} issue(s) found\n")
        for idx, err in enumerate(all_errors, 1):
            print(f"{idx}. {err}")
        return 1

    body_lines = len(body.splitlines())
    print(
        f"Validation passed: {skill_file}\n"
        f"  - frontmatter fields complete\n"
        f"  - body line count {body_lines}/{MAX_BODY_LINES}\n"
        f"  - no placeholders\n"
        f"  - risk boundary declarations complete\n"
        f"  - professional boundary declarations complete\n"
        f"  - workflow check item counts correct\n"
        f"  - all referenced files exist\n"
        f"  - tool binding check passed\n"
        f"  - output specification check passed"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
