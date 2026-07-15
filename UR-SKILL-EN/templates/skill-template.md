# SKILL Template

> **Purpose**: Select output detail level based on the generated SKILL's type (Functional/Creative/Social). All SKILLs share the 11-step workflow framework; sub-Agent invocations can be skipped based on file dependency determination.
> **Core Principle**: Output specification MUST include format type, output structure, issue severity, decision strategy, and user interaction mode.
> **Design Methodology**: See [design-guides/output-design-guide.md](../design-guides/output-design-guide.md)

---

## 1. Common Base Structure (11-Step Workflow)

```yaml
---
name: {kebab-case-name}
description: >-
  Use when [user intent A], [user intent B], or [user intent C].
  Covers requests like '[trigger phrase 1]', '[trigger phrase 2]'.
metadata:
  updated: {YYYY-MM-DD}
---

# {SKILL Name}

## Capability Matrix

(1 core domain + radiating domains determined by task analysis, recommended 3-8, each with 4 layers: Foundation -> Advanced -> Expert -> Extension)

### Core Domain

| Domain | Foundation Layer | Advanced Layer | Expert Layer | Extension Layer |
|:---|:---|:---|:---|:---|
| Core: {Core Domain Name} | ... | ... | ... | ... |

### Radiating Domains

| Domain | Foundation Layer | Advanced Layer | Expert Layer | Extension Layer |
|:---|:---|:---|:---|:---|
| A {Domain 1} | ... | ... | ... | ... |
| B {Domain 2} | ... | ... | ... | ... |

## Capability Facets

(Targeting only the core domain, 6 facets)

- **Facet 1 Efficiency & Cost**: ...
- **Facet 2 Knowledge Deepening**: ...
- **Facet 3 Risk Identification**: ...
- **Facet 4 Quality Inspection**: ...
- **Facet 5 Domain Fusion**: ...
- **Facet 6 System-Wide Perspective**: ...

## Workflow

### 1. Parse (Requirement Analysis)【Non-Critical Node, 3 dims】
- Actions: ...
- Checklist: ...
-> All confirmed -> Proceed to 2

### 2. Coordinate (Task Scheduling)【Non-Critical Node, 3 dims】
- Actions: ...
- Checklist: ...
-> All confirmed -> Proceed to 3

### 3. Dispatch (Delegate Execution)【Non-Critical Node, 3 dims】
- Actions: ...
- Checklist: ...
-> All confirmed -> Proceed to 4

### 4. Research (Domain Knowledge Web Search)【Critical Node, all 6 dims】
- Actions: ...
- Checklist: ...
-> All confirmed -> Proceed to 5

### 5. Planning (Plan Design)【Critical Node, all 6 dims】
- Actions: ...
- Checklist: ...
-> All confirmed -> Proceed to 6/7

### 6. Consolidate (Artifact Merging)【Non-Critical Node, 3 dims】
- Actions: ...
- Checklist: ...
-> All confirmed -> Proceed to 8

### 7. Execute (Core Output)【Non-Critical Node, 3 dims】
- Actions: ...
- Checklist: ...
-> All confirmed -> Proceed to 8

### 8. Verify (Quality Check)【Critical Node, all 6 dims】
- Actions: ...
- Checklist: ...
-> All confirmed -> Proceed to 9

### 9. Validation (Adversarial Testing)【Critical Node, all 6 dims】
- Actions: ...
- Checklist: ...
-> All confirmed -> Proceed to 10

### 10. Loop Decision (Gate)【Critical Node, all 6 dims】
- Actions: ...
- Checklist: ...
-> Pass -> Proceed to 11 / Fail -> Return for Fixes

### 11. Assemble (Final Delivery)【Non-Critical Node, 3 dims】
- Actions: ...
- Checklist: ...
-> Delivery complete

## Output Specification

{Natural language / Structured / Mixed, brief description}

## Rules

### Hard Constraints

- **MUST** ...
- **MUST** ...

### Hard Prohibitions

- **MUST NOT** ...

### Strong Preferences

- **SHOULD** ...
- **SHOULD NOT** ...

### Optional

- **MAY** ...

## Risk Boundary Statements

> Format: see [templates/boundary-template.md](boundary-template.md)

| ID | Statement |
|:---|:---|
| Risk Boundary-01 | {Inviolable safety red line for this SKILL} |
| Risk Boundary-02 | {Inviolable safety red line for this SKILL} |
| Risk Boundary-03 | {Inviolable safety red line for this SKILL} |

## Professional Boundary Statements

> Format: see [templates/boundary-template.md](boundary-template.md)

| ID | Statement |
|:---|:---|
| Professional Boundary-01 | {Professional scope limit this SKILL must not cross} |

## Examples

### Example 1: {Scenario}
**Input**: ...
**Output**: ...
```

---

## 2. Functional Type (+ references/, includes Research + Planning nodes)

```yaml
---
name: {kebab-case-name}
description: >-
  Use when [user intent A], [user intent B] are present.
  Covers requests like '[trigger phrase 1]', '[trigger phrase 2]'.
metadata:
  updated: {YYYY-MM-DD}
---

# {SKILL Name}

## Capability Matrix

(1 core domain + 3-8 radiating domains, each with 4 layers)

## Capability Facets

(Targeting only the core domain, 6 facets)

## Workflow

### 1. Parse (Requirement Analysis)【Non-Critical Node, 3 dims】
### 2. Coordinate (Task Scheduling)【Non-Critical Node, 3 dims】
### 4. Research (Domain Knowledge Web Search)【Critical Node, all 6 dims】
### 5. Planning (Plan Design)【Critical Node, all 6 dims】
### 7. Execute (Core Output)【Non-Critical Node, 3 dims】
### 8. Verify (Quality Check)【Critical Node, all 6 dims】
### 9. Validation (Adversarial Testing)【Critical Node, all 6 dims】
### 10. Loop Decision (Gate)【Critical Node, all 6 dims】
### 11. Assemble (Final Delivery)【Non-Critical Node, 3 dims】

## Output Specification

> Refer to ../design-guides/output-design-guide.md for output content design

### Output Format
- **Format Type**: {Issue table + Executive summary / Mermaid flowchart + Table / Checklist / ...}
- **Mandatory Visualization**: {Yes/No}

### Output Structure
1. Executive summary (Judgment + Risk level + Key findings)
2. {Main output section}
3. {Positive observations / Recommended actions}

### Issue Severity
| Level | Label | Definition | Action |
|:---|:---|:---|:---:|
| Critical | [Critical] | Security vulnerability / Data loss / Destructive bug | Block merge |
| High | [High] | Major functional defect | Must fix before merge |
| Medium | [Medium] | Notable code smell / Architecture issue | Fix recommended before merge |
| Low | [Low] | Minor improvement suggestion | Can optimize later |

### Decision Strategy
| Critical | High | Decision |
|:---|:---|:---|
| > 0 | Any | Rejected |
| 0 | > 3 | Needs modification |
| 0 | 1-3 | Conditionally approved |
| 0 | 0 | Approved |

### User Interaction
- **Mode**: {One-shot report / Confirm-Fix-Verify cycle / ...}
- **Cycle Count**: {N}

### Output File
- **Path**: {`docs/{type}/{scope}-{date}.md`}

## Rules

Hard Constraints + Hard Prohibitions + Strong Preferences + Optional + Risk Boundary Statements

## Risk Boundary Statements

> Format: see [templates/boundary-template.md](boundary-template.md)

| ID | Statement |
|:---|:---|
| Risk Boundary-01 | {Safety red line} |
| Risk Boundary-02 | {Safety red line} |
| Risk Boundary-03 | {Safety red line} |

## Professional Boundary Statements

> Format: see [templates/boundary-template.md](boundary-template.md)

| ID | Statement |
|:---|:---|
| Professional Boundary-01 | {Scope protection} |
| Professional Boundary-02 | {Scope protection} |

## Reference Index

- Examples: references/examples.md
- Anti-patterns: references/anti-patterns.md
- Troubleshooting: references/troubleshooting.md

## Tool Reference

> Tools used by this SKILL and invocation examples (MUST include this table when there are 3+ executable actions):

| Step | Tool | Invocation Example | Purpose |
|:---|:---|:---|:---|
| N. {Step Name} | `{Tool Name}` | `{Example parameters}` | {Purpose description} |
```

---

## 3. Full-Featured Functional Type (+ references/ + scripts/ + assets/, includes sub-Agent invocation)

```yaml
---
name: {kebab-case-name}
description: >-
  Use when [user intent A], [user intent B] are present.
  Covers requests like '[trigger phrase 1]', '[trigger phrase 2]'.
metadata:
  updated: {YYYY-MM-DD}
---

# {SKILL Name}

## Capability Matrix

(1 core domain + radiating domains determined by task analysis, recommended 3-8, each with 4 layers)

## Capability Facets

(Targeting only the core domain, 6 facets)

## Workflow

### 1. Parse (Requirement Analysis)【Non-Critical Node, 3 dims】
### 2. Coordinate (Task Scheduling)【Non-Critical Node, 3 dims】
### 3. Dispatch (Delegate Execution)【Non-Critical Node, 3 dims】
### 4. Research (Domain Knowledge Web Search)【Critical Node, all 6 dims】
### 5. Planning (Plan Design)【Critical Node, all 6 dims】
### 6. Consolidate (Artifact Merging)【Non-Critical Node, 3 dims】
### 7. Execute (Core Output)【Non-Critical Node, 3 dims】
### 8. Verify (Quality Check)【Critical Node, all 6 dims】
### 9. Validation (Adversarial Testing)【Critical Node, all 6 dims】
### 10. Loop Decision (Gate)【Critical Node, all 6 dims】
### 11. Assemble (Final Delivery)【Non-Critical Node, 3 dims】

> Step 3 Dispatch and Step 6 Consolidate invoke sub-Agents via the [Task] primitive. If the findings from Step 4 Research determine that scripts/ and assets/ are unnecessary, Step 6 is skipped.
> Sub-Agent invocation and skipping logic: see [workflow-template.md](workflow-template.md).

## Output Specification

> Refer to ../design-guides/output-design-guide.md for output content design

### Output Format
- **Format Type**: {Issue table + Executive summary + Mermaid diagram + Code block / ...}
- **Mandatory Visualization**: {Yes/No} -> Mermaid diagrams required when conditions are met

### Visualization Requirements (if mandatory)
- **Mermaid {Type}**: Show {content} ({flowchart / sequenceDiagram / stateDiagram})
- **Minimum {N} diagrams**: Complex scenarios add {additional diagram type}
- **Colors**: `fill:#{fill_color},color:#{text_color}` explicitly specified for each node

### Output Structure
1. Executive summary (Judgment + Risk level + Key findings)
2. {Main output section} (Table / Diagram / Severity-ranked list)
3. Positive observations (at least 1)
4. Recommended actions (Must fix before merge / Should fix after merge / Can optimize later)

### Issue Severity
| Level | Label | Definition | Action |
|:---|:---|:---|:---|
| Critical | [Critical] | Security vulnerability / Data loss / Destructive bug | Block merge |
| High | [High] | Major functional defect | Must fix before merge |
| Medium | [Medium] | Notable code smell / Architecture issue | Fix recommended before merge |
| Low | [Low] | Minor improvement suggestion | Can optimize later |

### Decision Strategy
| Critical | High | Decision |
|:---|:---|:---|
| > 0 | Any | Rejected |
| 0 | > 3 | Needs modification |
| 0 | 1-3 | Conditionally approved |
| 0 | 0 | Approved |

### User Interaction
- **Mode**: {Confirm-Fix-Verify cycle / Phased delivery / ...}
- **Interaction Tool**: [AskUserQuestion] -> Provide [{Option A}/{Option B}/{Option C}] options
- **Cycle Count**: Max {N} cycles

### Output File
- **Path**: {`docs/{type}/{scope}-{date}.md`}
- **Format**: Markdown, UTF-8

## Rules

Hard Constraints + Hard Prohibitions + Strong Preferences + Optional + Risk Boundary Statements + Professional Boundary Statements

## Risk Boundary Statements

> Format: see [templates/boundary-template.md](boundary-template.md)

| ID | Statement |
|:---|:---|
| Risk Boundary-01 | {Safety red line} |
| Risk Boundary-02 | {Safety red line} |
| Risk Boundary-03 | {Safety red line} |

## Professional Boundary Statements

> Format: see [templates/boundary-template.md](boundary-template.md)

| ID | Statement |
|:---|:---|
| Professional Boundary-01 | {Scope protection} |
| Professional Boundary-02 | {Scope protection} |

## Reference Index

- Examples: references/examples.md
- Anti-patterns: references/anti-patterns.md
- Troubleshooting: references/troubleshooting.md
- Executable scripts: scripts/
- Static assets: assets/

## Tool Reference

> Tools used by this SKILL and invocation examples (including degradation paths):

| Step | Tool | Invocation Example | Purpose | Degradation |
|:---|:---|:---|:---|:---|
| N. {Step Name} | `{Tool Name}` | `{Example parameters}` | {Purpose description} | `↘ {Degradation tool}` |
```

---

## 4. Output Constraints (General)

- Body MUST be < 500 lines
- YAML frontmatter MUST contain 3 fields: name, description, metadata.updated
- description is the **only trigger field**, MUST include trigger phrases
- Must not fill references/ content directly into the body
- Directory names use plural form: references/, scripts/, assets/
- Gate nodes (Research, Planning, Verify, Validation, Loop Decision): all 6 dims
- Execution nodes (Parse, Coordinate, Dispatch, Consolidate, Execute, Assemble): 3 dims
- Capability matrix: 1 core domain, radiating domain count determined by task analysis (recommended 3-8)
- Capability matrix: each domain has 4 layers of depth (Foundation -> Advanced -> Expert -> Extension)
- Capability facets: targeting only the core domain, 6 facets
- Risk boundary statements: safety red lines (typically 3-5)
- Professional boundary statements: scope protection (typically 1-3)
- Review/test type SKILLs: output specification MUST include format type, mandatory visualization, issue severity (Critical/High/Medium/Low), decision strategy, user interaction mode
- SKILLs with mandatory visualization: Mermaid diagram colors MUST be explicitly specified, must not rely on theme default colors
- Review type SKILLs: output structure MUST include executive summary + positive observations + recommended actions
