# Output Template

> Purpose: Select the corresponding output structure based on the complexity of the generated SKILL
> Core principle: Output specification MUST include format type, output structure, issue grading, decision strategy, and user interaction mode
> Design methodology: see [design-guides/output-content-design-guide.md](../design-guides/output-content-design-guide.md)

---

## 1. Simple Complexity (Single File, 4 Steps)

```yaml
---
name: {kebab-case-name}
description: "Use when [trigger condition]. [capability description]"
license: {license, e.g. Apache-2.0}
compatibility: {compatibility note, if needed}
allowed-tools: {space-separated tool list, if needed}
metadata:
  updated: {YYYY-MM-DD}
  type: prompt
  whenToUse: When [specific scenario]
---

# {SKILL Name}

## Capability Matrix

(1 core domain + radiating domains determined by task analysis, 4-8 recommended, each with 4 tiers: Foundation -> Intermediate -> Advanced -> Extension)

### Core Domain

| Domain | Foundation Tier | Intermediate Tier | Advanced Tier | Extension Tier |
|:---|:---|:---|:---|:---|
| Core: {Core Domain Name} | ... | ... | ... | ... |

### Radiating Domains

| Domain | Foundation Tier | Intermediate Tier | Advanced Tier | Extension Tier |
|:---|:---|:---|:---|:---|
| A {Domain 1} | ... | ... | ... | ... |
| B {Domain 2} | ... | ... | ... | ... |
| C {Domain 3} | ... | ... | ... | ... |
| ... | ... | ... | ... | ... |

## Capability Facets

(Targeting only the core domain, 6 facets)

- **Facet 1 Efficiency & Cost**: ...
- **Facet 2 Deep Knowledge**: ...
- **Facet 3 Risk Identification**: ...
- **Facet 4 Quality Verification**: ...
- **Facet 5 Domain Integration**: ...
- **Facet 6 System Holistics**: ...

## Workflow

1. Parse (3 dimensions)
   - Actions: ...
   - Checklist: ...
   - Any unconfirmed -> remediate -> return to confirm -> all confirmed -> proceed to 2

2. Execute (3 dimensions)
   - Actions: ...
   - Checklist: ...
   - Any unconfirmed -> remediate -> return to confirm -> all confirmed -> proceed to 3

3. Verify (6 dimensions, critical checkpoint)
   - Actions: ...
   - Checklist: ...
   - Any unconfirmed -> remediate -> return to confirm -> all confirmed -> proceed to 4

4. Deliver (3 dimensions)
   - Actions: ...
   - Checklist: ...
   - Any unconfirmed -> remediate -> return to confirm -> all confirmed -> delivery complete

## Output Specification

{Natural language / Structured / Hybrid, brief description}

## Rules

### Hard Constraints

- **MUST** ...
- **MUST** ...

### Hard Prohibitions

- **MUST NOT** ...
- **MUST NOT** ...

### Strong Preferences

- **SHOULD** ...
- **SHOULD NOT** ...

### Optional

- **MAY** ...

## Risk Boundary Declaration

> Format details: see [templates/boundary-template.md](../templates/boundary-template.md)

| No. | Declaration |
|:---|:---|
| Risk Boundary-01 | {Non-negotiable safety red line for this SKILL} |
| Risk Boundary-02 | {Non-negotiable safety red line for this SKILL} |
| Risk Boundary-03 | {Non-negotiable safety red line for this SKILL} |

## Professional Boundary Declaration

> Format details: see [templates/boundary-template.md](../templates/boundary-template.md)

| No. | Declaration |
|:---|:---|
| Professional Boundary-01 | {Professional domain limitation this SKILL must not cross} |

## Examples

### Example 1: {Scenario}
**Input**: ...
**Output**: ...
```

---

## 2. Medium Complexity (+ references/, 6 Steps)

```yaml
---
name: {kebab-case-name}
description: "Use when [trigger condition]. [capability description]"
license: {license, e.g. Apache-2.0}
compatibility: {compatibility note, if needed}
allowed-tools: {space-separated tool list, if needed}
metadata:
  updated: {YYYY-MM-DD}
  type: prompt
  whenToUse: When [specific scenario]
---

# {SKILL Name}

## Capability Matrix

(1 core domain + radiating domains determined by task analysis, 4-8 recommended, each with 4 tiers)

## Capability Facets

(Targeting only the core domain, 6 facets)

## Workflow

1. Parse (3 dimensions)
2. Research (6 dimensions, critical checkpoint)
3. Architect (6 dimensions, critical checkpoint)
4. Execute (3 dimensions)
5. Verify (6 dimensions, critical checkpoint)
6. Deliver (3 dimensions)

## Output Specification

> Refer to ../design-guides/output-content-design-guide.md for output content design

### Output Format
- **Format Type**: {Issue table + Executive summary / Mermaid flowchart + Table / Checklist / ...}
- **Mandatory Visualization**: {Yes/No}

### Output Structure
1. Executive Summary (verdict + risk level + key findings)
2. {Main output block}
3. {Positive observations / Recommended actions}

### Issue Grading
| Level | Label | Definition | Action |
|:---|:---|:---|:---:|
| Critical | [Critical] | Security vulnerability / data loss / destructive bug | Block merge |
| High | [High] | Major functional defect | Must fix before merge |
| Medium | [Medium] | Obvious code smell / architectural issue | Recommend fix before merge |
| Low | [Low] | Minor improvement suggestion | Can optimize later |

### Decision Strategy
Refer to ../design-guides/output-content-design-guide.md section 4.3

### User Interaction
- **Mode**: {One-shot report / Confirm-fix-verify loop / ...}
- **Loop Rounds**: {N}

### Output File
- **Path**: {`docs/{type}/{scope}-{date}.md`}

## Rules

Hard constraints + Hard prohibitions + Strong preferences + Optional + Risk boundary declaration

## Risk Boundary Declaration

> Format details: see [templates/boundary-template.md](../templates/boundary-template.md)

| No. | Declaration |
|:---|:---|
| Risk Boundary-01 | {Non-negotiable safety red line for this SKILL} |
| Risk Boundary-02 | {Non-negotiable safety red line for this SKILL} |
| Risk Boundary-03 | {Non-negotiable safety red line for this SKILL} |

## Professional Boundary Declaration

> Format details: see [templates/boundary-template.md](../templates/boundary-template.md)

| No. | Declaration |
|:---|:---|
| Professional Boundary-01 | {Professional domain limitation this SKILL must not cross} |
| Professional Boundary-02 | {Professional domain limitation this SKILL must not cross} |

## Reference Citations

- Output template: ../templates/output-template.md
- Output content design guide: ../design-guides/output-content-design-guide.md
- Examples: ../examples/examples.md
- Anti-patterns: ../References/anti-patterns.md
- Troubleshooting: ../References/troubleshooting.md

## Tool Reference

> Tools used by this SKILL and invocation examples (must be included for medium complexity):

| Step | Tool | Invocation Example | Purpose |
|:---|:---|:---|:---|
| N. {Step Name} | `{Tool Name}` | `{Example params}` | {Purpose description} |
```

---

## 3. Complex Complexity (+ references/ + scripts/ + assets/, 7+ Steps)

```yaml
---
name: {kebab-case-name}
description: "Use when [trigger condition]. [capability description]"
license: {license, e.g. Apache-2.0}
compatibility: {compatibility note, if needed}
allowed-tools: {space-separated tool list, if needed}
metadata:
  updated: {YYYY-MM-DD}
  type: prompt
  whenToUse: When [specific scenario]
---

# {SKILL Name}

## Capability Matrix

(1 core domain + radiating domains determined by task analysis, 4-8 recommended, each with 4 tiers)

## Capability Facets

(Targeting only the core domain, 6 facets)

## Workflow

1. Parse (3 dimensions)
2. Research (6 dimensions, critical checkpoint)
3. Architect (6 dimensions, critical checkpoint)
4. Execute (3 dimensions)
5. Verify (6 dimensions, critical checkpoint)
6. Validate (6 dimensions, critical checkpoint)
7. Deliver (3 dimensions)

## Output Specification

> Refer to ../design-guides/output-content-design-guide.md for output content design

### Output Format
- **Format Type**: {Issue table + Executive summary + Mermaid diagram + Code block / ...}
- **Mandatory Visualization**: {Yes/No} -> Require Mermaid diagram when conditions are met

### Visualization Requirements (if mandatory)
- **Mermaid {Type}**: Display {content} ({flowchart / sequenceDiagram / stateDiagram})
- **Minimum {N} Diagrams**: Complex scenarios append {additional diagram types}
- **Color Scheme**: `fill:#{fill color},color:#{text color}` explicitly specified per node

### Output Structure
1. Executive Summary (verdict + risk level + key findings)
2. {Main output block} (Table / Diagram / Graded checklist)
3. Positive Observations (at least 1)
4. Recommended Actions (Pre-merge must / Post-merge suggestion / Further optimization)

### Issue Grading
| Level | Label | Definition | Action |
|:---|:---|:---|:---|
| Critical | [Critical] | Security vulnerability / data loss / destructive bug | Block merge |
| High | [High] | Major functional defect | Must fix before merge |
| Medium | [Medium] | Obvious code smell / architectural issue | Recommend fix before merge |
| Low | [Low] | Minor improvement suggestion | Can optimize later |

### Decision Strategy
| Critical | High | Verdict |
|:---|:---|:---|
| > 0 | Any | Reject |
| 0 | > 3 | Changes Required |
| 0 | 1-3 | Conditionally Approved |
| 0 | 0 | Approved |

### User Interaction
- **Mode**: {Confirm-fix-verify loop / Phased delivery / ...}
- **Interaction Tool**: {AskUserQuestion} -> Provide [{Option A}/{Option B}/{Option C}] choices
- **Loop Rounds**: Maximum {N} rounds

### Output File
- **Path**: {`docs/{type}/{scope}-{date}.md`}
- **Format**: Markdown, UTF-8

## Rules

Hard constraints + Hard prohibitions + Strong preferences + Optional + Risk boundary declaration + Professional boundary declaration + Domain-specific rules

## Risk Boundary Declaration

> Format details: see [templates/boundary-template.md](../templates/boundary-template.md)

| No. | Declaration |
|:---|:---|
| Risk Boundary-01 | {Non-negotiable safety red line for this SKILL} |
| Risk Boundary-02 | {Non-negotiable safety red line for this SKILL} |
| Risk Boundary-03 | {Non-negotiable safety red line for this SKILL} |

## Professional Boundary Declaration

> Format details: see [templates/boundary-template.md](../templates/boundary-template.md)

| No. | Declaration |
|:---|:---|
| Professional Boundary-01 | {Professional domain limitation this SKILL must not cross} |
| Professional Boundary-02 | {Professional domain limitation this SKILL must not cross} |

## Reference Citations

- Output template: ../templates/output-template.md
- Output content design guide: ../design-guides/output-content-design-guide.md
- Examples: ../examples/examples.md
- Anti-patterns: ../References/anti-patterns.md
- Troubleshooting: ../References/troubleshooting.md
- Executable scripts: scripts/
- Static assets: assets/

## Tool Reference

> Tools used by this SKILL and invocation examples (must be included for complex complexity, including fallback paths):

| Step | Tool | Invocation Example | Purpose | Fallback |
|:---|:---|:---|:---|:---|
| N. {Step Name} | `{Tool Name}` | `{Example params}` | {Purpose description} | `-> {Fallback Tool}` |
```

---

## 4. Output Constraints (General)

- Body MUST be < 500 lines
- YAML frontmatter MUST be complete (name, description, metadata.updated, metadata.type, metadata.whenToUse)
- description strongly recommended to begin with "Use when..."
- MUST NOT inline references/ content directly into body
- Directory names use plural form: references/, scripts/, assets/
- The verification checkpoint MUST use all 6 dimensions regardless of complexity
- Critical checkpoints (Research, Architect, Verify, Validate) use all 6 dimensions
- Non-critical checkpoints (Parse, Execute, Deliver) use 3 dimensions
- Capability matrix: 1 core domain, number of radiating domains determined by task analysis (4-8 recommended, minimum 3, maximum 8), independent of complexity
- Capability matrix: Each domain has 4-tier depth (Foundation -> Intermediate -> Advanced -> Extension), across all complexity levels
- Capability facets: Targeting only the core domain, 6 facets
- Risk boundary declaration: Safety red lines (quantity determined by domain safety requirements, typically 3-5)
- Professional boundary declaration: Cross-boundary protection (quantity determined by domain scope, typically 1-3)
- SKILLs of medium complexity or above with `type` of `hybrid` or `tool`: MUST include a centralized tool reference table
- Executable action format: `[Tool Name] Action -> Output` (`prompt` type SKILLs exempt)
- Review/testing type SKILLs (review/audit/test/inspection type) output specification: MUST include output format type, mandatory visualization check, issue grading (Critical/High/Medium/Low), decision strategy, user interaction mode (refer to ../design-guides/output-content-design-guide.md)
- SKILLs triggering mandatory visualization: Mermaid diagram colors MUST be explicitly specified (`fill:#xxx,color:#xxx`), must not rely on theme defaults
- Review-type SKILLs: Output structure MUST include executive summary + positive observations + recommended actions
