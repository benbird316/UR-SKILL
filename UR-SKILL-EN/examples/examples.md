# Examples

> Purpose: Showcase the output forms of UR-SKILL at different complexity levels
> Core Principle: Examples only display structure and key design decisions; they do not replace templates in references/

---

## Example 1: Simple SKILL (no references/)

**User Input**:
> Write a SKILL that converts natural language descriptions into Python function names.

**Core Task**: Identifier Generation Engineering

**Output Structure**:

```yaml
---
name: pythonize-name
description: "Use when converting a natural language description into a valid Python function or variable name. Invoke for naming helpers, refactoring suggestions, or API method naming."
type: prompt
whenToUse: Use when the user wants to convert a natural language description into a valid Python function or variable name
metadata:
  updated: 2026-07-09
---
```

```markdown
# pythonize-name

> Role: You are a Python naming engineer. Convert natural language descriptions into PEP 8 compliant function/variable names.

## Capability Matrix

**Core Domain**: Identifier Generation Engineering

| Domain | Foundational | Advanced | Expert | Extended |
|:---|:---|:---|:---|:---|
| Core: Identifier Generation Engineering | Identify keywords | Remove stop words & abbreviate | Handle polysemy & ambiguity | Infer project naming style |

**Radiating Domains**:

| Domain | Foundational | Advanced | Expert | Extended |
|:---|:---|:---|:---|:---|
| Requirements Parsing | Extract actions & objects | Identify implicit parameters | Handle negation & conditions | Infer true user intent |
| B Naming Standards | Master PEP 8 | Distinguish public/private | Handle abbreviations & acronyms | Adapt to team conventions |
| C Format Constraints | Convert to lowercase/underscores | Handle special characters | Truncate overly long names | Ensure readability |

## Workflow

1. Parse (3 dimensions): Extract raw description and constraints
2. Execute (3 dimensions): Generate candidate names
3. Verify (6 dimensions): Check PEP 8, readability, uniqueness
4. Deliver (3 dimensions): Output sorted candidate list

## Rules

- **MUST** output lowercase underscore format
- **MUST NOT** use Python reserved words
- **SHOULD** prefer verb-first naming

## Risk Boundary Declaration

| ID | Declaration |
|:---|:---|
| Risk Boundary-01 | Must not generate insulting, discriminatory, or illegal names |
| Risk Boundary-02 | Must not generate names that could cause security confusion |
| Risk Boundary-03 | Must not execute any external code |
```

**Rationale**: A simple SKILL has a single core task (name conversion). 3 radiating domains suffice for coverage. No external knowledge base or standalone references/ needed. Workflow simplified to 4 steps, only 3 rules, all inlined in the body.

**Boundary Notes**: This example assumes user input is Chinese/English natural language with output as Python identifiers; it does not handle naming conventions for other programming languages.

---

## Example 2: Medium SKILL (+ references/)

**User Input**:
> Write a SKILL for Kubernetes container security baseline research, referencing official documentation and NSA/CISA guidelines.

**Core Task**: Web Research Analysis Report Engineering

**Output Structure Highlights**:

- `references/source-evaluation-guide.md`: Source grading standards
- `references/output-template.md`: Report structure template
- `references/examples.md`: More examples
- Body retains: capability matrix, workflow, rules, risk boundaries

**Capability Matrix Design Highlights**:

| Type | Example |
|:---|:---|
| Core Domain | Web Research Analysis Engineering |
| Radiating Domains | Research Methodology, Information Retrieval Engineering, Source Evaluation, Evidence Synthesis, Report Design, Quality Governance |

Note: Radiating domains are independent professional capabilities, not a pipeline of "parse -> retrieve -> evaluate -> write."

**Rationale**: A medium-complexity SKILL depends on external knowledge bases (NSA/CISA guidelines, Kubernetes official documentation) and requires source grading, report structure, and further examples to be sunk into references/ to avoid the body exceeding 500 lines. 6 radiating domains cover the complete chain of research analysis.

**Boundary Notes**: This example focuses on container security baseline research and does not cover runtime intrusion detection, vulnerability exploit verification, or environment-specific configuration deployment.

---

## Example 3: Complex SKILL (+ references/ + scripts/ + assets/)

**User Input**:
> Create a Python code review SKILL capable of invoking pylint/mypy for static analysis and outputting Markdown reports with line numbers.

**Core Task**: Python Code Quality Assurance Engineering

**Output Structure Highlights**:

- `scripts/run_linters.py`: Invoke pylint/mypy and parse output
- `assets/report-template.md`: Report template
- `references/domain-knowledge/`: Python security vulnerability patterns, PEP 8 specifications
- Body retains: capability matrix, workflow, rules, risk boundaries, script invocation instructions

**Rationale**: A complex SKILL requires calling external executable scripts (pylint/mypy), using static report templates, and depends on extensive domain knowledge (PEP 8, OWASP Python Top 10). These resources must be split into scripts/, assets/, references/ to achieve progressive loading.

**Boundary Notes**: This example focuses on static code review; it does not execute the code under review, nor does it substitute for security penetration testing or manual code review.

---

## Common Error Examples

### Error: Capability Matrix Written as Workflow

```markdown
**Radiating Domains**:
| A Parse Requirements | ... |
| B Retrieve Materials | ... |
| C Evaluate Sources | ... |
| D Generate Report | ... |
```

**Problem**: These are chronologically ordered workflow steps, not independent capability domains. Reordering would break the logic.

**Fix**: Replace with independent professional capabilities, e.g., "Research Methodology," "Information Retrieval Engineering," "Source Evaluation Science," "Knowledge Synthesis," "Report Design."
