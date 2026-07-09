# Anti-Pattern File Design Guide

> Purpose: Define the standard format, content requirements, and design methodology for anti-pattern files
> Core principle: Anti-patterns are practices that "seem correct but are actually harmful" -- you must explain "why it's wrong" and "why the alternative is right"

---

## 1. Why Anti-Pattern Files Are Needed

Anti-pattern is a standard term in software engineering. Unlike "errors," anti-patterns are cases of "good intentions gone wrong" -- a developer chooses a practice with good intent, but the outcome is harmful.

If anti-patterns are not documented:
- LLMs will repeatedly generate practices proven to be harmful
- Users cannot distinguish "correct practice" from "practice that seems correct but is actually harmful"
- Quality checks cannot identify structural problems (they can only catch syntax errors)

The anti-pattern file is an **instructional reference file** (L3), loaded on demand. When an LLM generates SKILL content, it loads the anti-pattern file for static scanning to identify potential issues.

---

## 2. Standard Format of Anti-Patterns

### 2.1 Six Required Elements

| Element | Description | Why It's Required |
|:---|:---|:---|
| **Name** | Concise, precise naming | Enables reference and retrieval |
| **Manifestation** | When it occurs, how to identify it | Allows users to self-diagnose |
| **Why It Occurs** | The good intention (good faith) | Anti-patterns are not errors, they are "good intentions gone wrong"; without explaining the good intention, users cannot understand why this mistake was made |
| **Harm** | Why it's wrong (adverse outcome) | Helps users understand consequences, driving correction |
| **Detection Method** | How to identify it automatically or manually | Lowers inspection cost, increases coverage |
| **Avoidance Strategy** | Alternative approach + why it's correct | Merely saying "don't do X" is insufficient; you must say "do Y instead"; you must explain why Y is correct |

> Why six elements: Fewer than six cannot fully convey the instructional chain of "good intention → adverse outcome → why → what to do correctly." More than six reduces information density and dilutes attention.

### 2.2 Format Example

```markdown
## {Number} {Name}

**Manifestation**: {When it occurs, how to identify}

**Why It Occurs**: {The good intention, why the developer would choose this practice}

**Harm**: {Why it's wrong, specific consequences}

**Detection Method**: {How to identify automatically or manually}

**Avoidance Strategy**: {Alternative approach} → {Why it's correct}
```

---

## 3. Generation Method (ur-skill Special Notes)

> This SKILL is a "SKILL for designing SKILLs" (ur-skill) and has no historical project accumulation.
> Therefore, anti-patterns are not "collected from historical projects" but "dynamically researched and generated based on the core scenarios of the generated SKILL."

### 3.1 Generation Based on Web Research

When using this SKILL to generate a specific SKILL, follow these steps to generate anti-patterns:

1. **Identify core scenarios**: Extract the SKILL's core use cases from user requirements (e.g., "Python code inspection," "REST API design")
2. **Research industry pain points via web search**: Search for common errors, anti-examples of best practices, and high-frequency Stack Overflow issues in that scenario
3. **Identify anti-patterns**: Extract practices that "seem correct but are actually harmful" from the research results
4. **Validate anti-patterns**:
   - [ ] Not an isolated error: The practice recurs across multiple scenarios
   - [ ] Has good intention: Can explain why the developer chose this practice
   - [ ] Has clear harm: Can describe specific consequences
   - [ ] Has alternative: Can provide the correct alternative approach

### 3.2 Generation Based on User Instructions

If the user provides specific scenarios or existing materials:

1. **Analyze user materials**: Extract common errors, pain points, and failure cases from user descriptions
2. **Identify anti-patterns**: Convert user descriptions into the anti-pattern structure of "Manifestation → Harm → Avoidance Strategy"
3. **Supplement with research**: For scenarios not covered by the user, supplement via web research
4. **Validate completeness**:
   - [ ] Covers all pain points mentioned by the user
   - [ ] Supplements anti-patterns not mentioned by the user but common in the industry
   - [ ] Anti-pattern count matches complexity (simple 3-4, medium 5-6, complex 7-8)

### 3.3 ur-skill Self-Check List

When ur-skill designs a SKILL, it MUST self-check the following anti-patterns to ensure the generated SKILL does not violate ur-skill specifications (for detailed inspection flow, see the workflow verification steps in ur-skill.md):

| Anti-Pattern | Manifestation | Avoidance Strategy |
|:---|:---|:---|
| Specification Overreach | Placing specification definitions (field constraints, format descriptions) directly into body | Remove spec tables and push them down to references/ |
| Placeholder Residue | The generated SKILL body contains unfilled content such as [xxx], TODO, FIXME | Fill all content completely, or delete and mark as Blind Spot |
| Example Contamination | Copying examples from references/ directly into body | Reference examples declaratively via references/ |
| Architecture Confusion | Capability Matrix direction is workflow steps (e.g., "Parse → Analyze → Execute") | Change to domain naming (e.g., "Static Analysis") |
| Missing Checks | Insufficient Review count in generated SKILL workflow | Allocate by node type: Critical Checkpoints 6 Review Dimensions, Non-Critical Checkpoints 3 Review Dimensions |
| Blind Spot Evasion | Blind Spot identification only states "limitations noted" without following the Blind Spot Three-Tier Mechanism | Enforce the Blind Spot Three-Tier Mechanism: investigate & improve → request resources → Blind Spot report + feasibility suggestions |

> Why ur-skill needs its own anti-patterns: When ur-skill designs a SKILL, it may itself violate its own specifications. ur-skill anti-patterns are a "self-check list" ensuring generated SKILLs do not inherit ur-skill's defects.

---

## 4. Anti-Pattern Design Methodology

### 4.1 Collecting Anti-Patterns

Collect from the following sources:
- Repeated errors in historical projects
- Common issues in code reviews
- Industry-recognized anti-patterns (OWASP, Martin Fowler)
- Violation cases within this system itself (leading by example)

### 4.2 Validating Anti-Patterns

Each anti-pattern must pass the following validation:

- [ ] **Not an isolated error**: The practice recurs across multiple scenarios
- [ ] **Has good intention**: Can explain why the developer would choose this practice
- [ ] **Has clear harm**: Can describe specific consequences, not abstract criticism
- [ ] **Has alternative**: Can provide the correct alternative approach
- [ ] **Detectable**: Can be identified automatically through rules or scripts

### 4.3 Organizing Anti-Patterns

Sort by detection priority:

| Priority | Sorting Criterion | Example |
|:---|:---|:---|
| Critical | Directly affects usability | Anti-pattern 2 Placeholder Residue (incomplete deliverable) |
| High | Directly affects professionalism/security | Anti-pattern 1 Specification Overreach / Anti-pattern 7 Risk Boundary Abuse / Anti-pattern 9 Blind Spot Evasion |
| Medium | Directly affects quality depth | Anti-pattern 3 Example Contamination / Anti-pattern 4 Architecture Confusion / Anti-pattern 5 Missing Checks / Anti-pattern 8 Facet Filler |
| Low | Directly affects continuous improvement | Anti-pattern 6 Blind Spot Evasion (optimization stagnation) |

> Why sort by priority: Higher priority anti-patterns are detected and fixed first. If Critical fails, there is no need to test High through P6.

---

## 5. Anti-Pattern File Content Requirements

### 5.1 Content That Must Be Addressed

- **Each anti-pattern MUST have "Why It Occurs"**: Without explaining the good intention, anti-patterns become a checklist of dogma ("don't do X"), and users don't understand why X is harmful.
- **Each anti-pattern MUST have an "Avoidance Strategy"**: Merely saying "don't do X" is insufficient; you must say "do Y instead."
- **Each avoidance strategy MUST have "Why it's correct"**: Without explaining why Y is correct, the user may choose another wrong alternative.

### 5.2 Prohibited Content

- **Prohibited: Only writing "don't do X"**: An alternative and rationale are required.
- **Prohibited: Abstract criticism**: Such as "this practice is bad" -- must specifically state "why it's bad" and "what the consequences are."
- **Prohibited: No detection method**: Anti-patterns must be detectable, otherwise quality checks cannot be executed.

---

## 6. Scan Script Design

Anti-pattern files may include scan scripts for automated detection.

### 6.1 Script Requirements

- **Read-only**: Scripts only detect, do not modify files
- **Idempotent**: Multiple executions produce consistent results
- **Self-contained**: No external environment dependencies
- **Structured output**: Output format is uniform and parseable

### 6.2 Script Example

```python
# Placeholder Residue Detection
PLACEHOLDER_PATTERN = r'\[.*?\]|TODO|FIXME|\{.*?\}'
matches = re.findall(PLACEHOLDER_PATTERN, body_content)
if matches:
    report(f"Anti-pattern 2 Placeholder Residue: {matches}")
```

### 6.3 Additional Anti-Pattern Scan Examples

```python
# Anti-pattern 5 Missing Checks Scan
for step in workflow_steps:
    check_count = step.count("- [ ]")
    if step.is_critical and check_count < 6:
        report(f"Anti-pattern 5 Missing Checks: Critical step {step.name} has only {check_count} checks")

# Anti-pattern 7 Risk Boundary Abuse Scan
CAPABILITY_DEGRADE_KEYWORDS = [
    "不负责", "不属于", "不在.*范围", "不管", "不承担",
    "只做.*不做", "仅限于", "不涉及", "不包含"
]
rb_lines = re.findall(r'\|\s*风险边界-\d+\s*\|\s*(.+?)\s*\|', body_content)
for line in rb_lines:
    for kw in CAPABILITY_DEGRADE_KEYWORDS:
        if re.search(kw, line):
            report(f"Anti-pattern 7 Risk Boundary Abuse: Suspected capability degradation '{kw}' -> '{line.strip()[:60]}'")

SAFETY_KEYWORDS = ["违法", "公序良俗", "歧视", "攻击", "注入", "越狱", "恶意", "漏洞", "爬取", "侵犯"]
has_safety = any(re.search(kw, body_section_of_risk_boundaries) for kw in SAFETY_KEYWORDS)
if not has_safety:
    report(f"Anti-pattern 7 Risk Boundary Abuse: Risk boundary declaration lacks safety semantics, suspected scope-only description")

# Anti-pattern 8 Facet Filler Scan
FACET_FILLER_PATTERNS = [
    r"掌握相关领域知识",
    r"识别潜在风险",
    r"保证输出质量",
    r"考虑全局影响",
    r"优化资源投入",
]
for pattern in FACET_FILLER_PATTERNS:
    if re.search(pattern, body_content):
        report(f"Anti-pattern 8 Facet Filler: Suspected generic boilerplate '{pattern}'")

# Anti-pattern 9 Blind Spot Evasion Scan
BLIND_DUMP_KEYWORDS = ["仅供参考", "请自行验证", "可能存在.*盲区", "不保证"]
blind_sections = re.findall(r'盲区[：:](.*?)(?=\n\n|\Z)', body_content, re.DOTALL)
for section in blind_sections:
    if any(re.search(kw, section) for kw in BLIND_DUMP_KEYWORDS):
        if "已尝试" not in section:
            report(f"Anti-pattern 9 Blind Spot Evasion: Declaration-only blind spot, no action attempted")
```

> Why scripts only detect and never modify: Modification operations carry high risk and should only be performed after human confirmation. Detection scripts can be integrated into CI/CD pipelines to automatically intercept issues.

---

## 7. Completeness Checklist

When designing an anti-pattern file, check each item:

- [ ] Each anti-pattern contains six elements (Name, Manifestation, Why It Occurs, Harm, Detection Method, Avoidance Strategy)
- [ ] Each anti-pattern has "Why It Occurs" (good intention)
- [ ] Each anti-pattern has an "Avoidance Strategy" (alternative + why it's correct)
- [ ] Anti-patterns are sorted by detection priority
- [ ] Anti-patterns are not isolated errors but recurring patterns
- [ ] Scan scripts are read-only, idempotent, and self-contained
- [ ] File < 200 lines; split if exceeded
- [ ] No placeholder residue (the file itself must not violate the anti-pattern)
