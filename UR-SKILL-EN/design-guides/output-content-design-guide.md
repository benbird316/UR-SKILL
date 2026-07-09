# Output Content Design Guide

> Purpose: Guides UR-SKILL in defining the **format types, visualization requirements, structural hierarchy, interaction strategies, and decision strategies** for output content when generating SKILLs. Answers the question "What exactly does the SKILL output after execution?"

---

## 1. Why Output Content Design Is Needed

**Problem 1: Single output format**

Currently, `../templates/output-template.md` only defines the skeleton of a Markdown file (capability matrix + workflow + rules), but does not define **runtime output** -- what the result presented to the user after the Agent executes the SKILL looks like.

Taking TRAE-code-review as an example, it explicitly requires in Step 4 of SKILL.md:

> **Always provide** at least one mermaid diagram to summarize the key changes.

But the quality and security SKILLs have no such specification requirements at all -- they only define the structural template of the SKILL itself, not the output content format when the SKILL is used by the Agent.

**Problem 2: No decision matrix for output types**

When `generate` creates a SKILL, it doesn't know when the SKILL should output a Mermaid diagram vs. a table vs. a checklist vs. a narrative report. All SKILLs uniformly output Markdown body text, lacking the ability to match output formats to task types.

**Solution**: This guide defines the design dimensions of output content -- format types, mandatory visualization rules, structural hierarchy specifications, decision strategies, and user interaction modes.

---

## 2. Output Format Type Overview

### 2.1 Type Classification

| Format Type | Applicable Scenario | Advantages | Disadvantages |
|:---|:---|:---|:---|
| **Markdown Table** | Data comparison, issue lists, graded results | Clear structure, sortable | Cannot express process logic |
| **Mermaid Flowchart** | Business processes, call chains, data flows | Processes and relationships visible at a glance | Static diagram, non-interactive |
| **Mermaid Sequence Diagram** | API call chains, request-response flows | Clear temporal relationships | Too long with many nodes |
| **Mermaid State Diagram** | State machines, workflow transitions | State transitions visualized | Only applicable to state-driven scenarios |
| **Code Block** | Displaying fixes, example code | Directly copyable | Language must be annotated |
| **Checklist** | Verification items, self-check items, task lists | Item-by-item verifiable | No contextual explanation |
| **Executive Summary** | High-level conclusions, decision recommendations | Quick reading | Lacks detail |
| **Severity Grading Table** | Security vulnerabilities, quality issues | Clear priority | Requires accurate level definitions |
| **Comparison Matrix** | Solution selection, tool comparison | Intuitive multi-dimensional comparison | Becomes complex as dimensions increase |
| **Narrative Report** | Analysis conclusions, research investigation | Rich context | Verbose, hard to locate quickly |
| **Judgment Verdict** | Merge/Reject/Modify | Gives clear action decision | Binary judgment may be overly simplistic |

### 2.2 Format Selection Decision Matrix

| Task Type | Preferred Format | Mandatory Visualization | Notes |
|:---|:---|:---:|:---|
| **Code Review** | Issue table + Mermaid flowchart | Yes | Flowchart shows business flow and technical flow of changes |
| **Security Audit** | Severity grading table + Executive summary + Code blocks | Optional | Table sorted by severity descending, code blocks show vulnerability locations |
| **Architecture Review** | Mermaid architecture diagram + Comparison matrix | Yes | Architecture diagram shows component relationships, matrix compares solutions |
| **Test Analysis** | Checklist + Table | Optional | Checklist item-by-item, table for coverage statistics |
| **Requirements Analysis** | Executive summary + Narrative report | Optional | Summary for decision-makers, report for implementers |
| **Research Investigation** | Executive summary + Narrative report + Table + Code blocks | Optional | Multi-format combination: summary + report + source credibility table + evidence annotation |
| **Deployment Inspection** | Checklist + Status table | Optional | Item-by-item inspection, pass/fail status annotation |
| **Troubleshooting** | Executive summary + Timeline narrative + Code blocks | Recommended | Summary for management, narrative shows investigation process, code blocks show root cause |
| **Performance Analysis** | Table + Optional charts | Recommended | Table compares metrics, Mermaid charts show bottlenecks |

---

## 3. Mandatory Visualization Rules

### 3.1 What "Mandatory Mermaid" Means

When a SKILL's task type is marked as **mandatory visualization**, the output content must include at least one Mermaid diagram.

**Mandatory conditions** (triggered if any one is met):

1. The task involves **process/logic chain** descriptions (code review, business process analysis)
2. The task involves **multi-component interaction** (architecture review, API call analysis)
3. The task involves **state transitions** (workflow design, state machines)
4. The task complexity is **medium or above**, with a clear "change-to-impact" relationship

**Mandatory visualization rules**:

| Rule | Description |
|:---|:---|
| Minimum 1 diagram | Every output must include at least 1 Mermaid diagram |
| 2 diagrams for complex changes | Significant changes require both business flow and technical flow diagrams |
| Prefer flowcharts and sequence diagrams | `flowchart` or `sequenceDiagram`, showing process / call / data flow |
| No pure classification box diagrams | Box diagrams that only show grouping without directional relationships are not allowed |
| Mandatory color scheme | Fill color and text color must be explicitly specified to ensure readability in both light and dark themes |
| Diagram type matching | Architecture → `graph TD`, calls → `sequenceDiagram`, states → `stateDiagram`, classes → `classDiagram` |

### 3.2 Visualization Exemption Conditions

The following conditions exempt mandatory visualization:

- Task type is pure text analysis (no process relationships)
- Output content is a single conclusion (e.g., "Pass/Fail")
- SKILL complexity is **simple** (single file, no references)

### 3.3 Declaring Visualization Rules in SKILLs

In the output specification block, use the following format:

```
## Output Specification

### Mandatory Visualization
- **Mermaid Flowchart**: Shows the business logic chain of the reviewed code (flowchart TD/LR)
- **Mermaid Sequence Diagram** (complex changes): Shows the call chain of key functions (sequenceDiagram)
- **Color Requirements**: Fill color #eee (light) / #333 (dark), text color #333 (light) / #eee (dark)
```

---

## 4. Output Structural Hierarchy Specification

### 4.1 Executive Summary (Required, Medium Complexity and Above)

Immediately after the title, for decision-makers to quickly understand the overall picture:

```
## Executive Summary

**Overall Verdict**: Pass | Conditional Pass | Needs Modification | Rejected

**Risk Level**: Low | Medium | High | Critical

**Key Findings**:
1. [Most important finding, one sentence]
2. [Second most important finding]
3. [Third most important finding]
```

### 4.2 Issue Grading (Required, Review-Type SKILLs)

All issues must be annotated with severity:

| Level | Indicator | Definition | Action |
|:---|:---|:---|:---|
| **Critical** | Critical | Security vulnerabilities, data loss risk, destructive bugs | Must fix immediately, otherwise block merge |
| **High** | High | Major defects affecting core functionality | Must fix before merge |
| **Medium** | Medium | Obvious issues, recommended fix | Recommended fix before merge |
| **Low** | Low | Minor suggestions, optional fix | Can optimize later |

### 4.3 Decision Strategy (Required, Review-Type SKILLs)

Automatically issue verdicts based on issue distribution:

| Critical | High | Verdict |
|:---|:---|:---|
| > 0 | Any | Rejected |
| 0 | > 3 | Needs Modification |
| 0 | 1-3 | Conditional Pass |
| 0 | 0 | Pass (only Medium/Low recorded) |

### 4.4 Recommended Actions (Required, Review-Type SKILLs)

Based on the verdict, provide concrete action items:

```
## Recommended Actions

### Must Before Merge (Critical + High)
- [ ] [Action item description]
- [ ] [Action item description]

### Suggested After Merge (Medium)
- [ ] [Action item description]

### Future Optimization (Low)
- [ ] [Action item description]
```

### 4.5 Positive Observations (Recommended, All Review-Type SKILLs)

Not only report issues but also acknowledge what was done well:

```
## Positive Observations

- [Code organization is clear]
- [Error handling is thorough]
- [Test coverage is sufficient]
```

---

## 5. User Interaction Modes

### 5.1 Four Interaction Modes

| Mode | Applicable Scenario | Example |
|:---|:---|:---|
| **One-shot Report** | Simple queries, research investigations | Output complete report then end |
| **Confirm-Fix-Verify Loop** | Code review, issue diagnosis | Output issues → User selects fixes → Verify after fix → Confirm |
| **Phased Delivery** | Complex analysis | First output summary → User confirms → Output detailed report |
| **Async Scheduled** | Periodic inspections | Scheduled execution → Auto-push to designated location/channel |

### 5.2 Interaction Mode Declaration Format

In the SKILL's output specification, use the following format:

```
### User Interaction
- **Mode**: Confirm-Fix-Verify Loop
- **Interaction Tool**: AskUserQuestion (preferred), Text options (fallback)
- **Loop Count**: Maximum 3 rounds of fix-verify
- **Termination Condition**: User confirms pass / All issues fixed / Maximum rounds reached
```

---

## 6. Output File Path Specification

### 6.1 Output Path Rules

Review/analysis type SKILLs should specify file save paths in the output specification:

| SKILL Type | Output Path Template |
|:---|:---|
| Code Review | `docs/reviews/{branch-name}-{date}.md` |
| Security Audit | `docs/security-audits/{scope}-{date}.md` |
| Architecture Review | `docs/architecture/{component}-review-{date}.md` |
| Research Investigation | `docs/research/{topic}-{date}.md` |
| Deployment Inspection | `docs/operations/{env}-check-{date}.md` |

### 6.2 Path Declaration Format

At the end of the output specification, use:

```
### Output File
- **Path**: `docs/reviews/{branch-name}-{date}.md`
- **Format**: Markdown, UTF-8 encoding
- **Overwrite Policy**: Do not overwrite existing files; date is precise to the day
```

---

## 7. Combined Example

### Example: Output Content Specification for a Code Review SKILL

```
## Output Specification

### Mandatory Visualization
- **Mermaid Flowchart**: Shows the business logic chain involved in the change (flowchart TD)
- **Mermaid Sequence Diagram** (complex changes, >10 files): Shows the call sequence of key components (sequenceDiagram)
- **Color Requirements**: `fill:#f0f0f0,color:#333` → explicitly specify per node

### Output Structure
1. Executive Summary (verdict + risk level + key findings)
2. Issue Grading List (Markdown table, sorted by severity descending)
3. Positive Observations (at least 1 item)
4. Recommended Actions (split into "Must Before Merge" and "Suggested After Merge")
5. Mermaid Visualization Diagrams

### Issue Grading
- Critical: Security vulnerabilities, data loss, destructive bugs
- High: Major functional defects
- Medium: Obvious code smells
- Low: Minor improvement suggestions

### Decision Strategy
Auto-generate verdict based on Critical + High count: Rejected / Needs Modification / Conditional Pass / Pass

### User Interaction
- **Mode**: Confirm-Fix-Verify Loop
- **Interaction Tool**: AskUserQuestion → provide [Fix all Critical+High / Fix one by one / View only without changes] options
- **Loop Rounds**: Maximum 3 rounds

### Output File
- **Path**: `docs/reviews/{branch-name}-{date}.md`
- **Format**: Markdown
```

---

## 8. Anti-Patterns

| No. | Anti-Pattern | Manifestation | Correction |
|:---:|:---|:---|:---|
| Output Anti-Pattern 1 | No output format definition | SKILL only defines workflow without telling the Agent what to output and how | Define at least 1 format type + output structure |
| Output Anti-Pattern 2 | Pure text wall | Review results described in large blocks of text; users cannot find the key points | Use table + grading + summary structure |
| Output Anti-Pattern 3 | Missing visualization | Content suitable for flowcharts (review process changes / SDK calls) has no diagrams | Check 3.1 mandatory conditions to see if Mermaid is needed |
| Output Anti-Pattern 4 | Missing verdict | Only lists issues without a conclusion; user doesn't know whether to merge | Add decision strategy per 4.3 |
| Output Anti-Pattern 5 | No positive feedback | Only reports issues without acknowledging what was done well | Add positive observations block |
| Output Anti-Pattern 6 | No output path | Output content is not saved to a file; Agent cannot reference it next time | Specify file output path |
| Output Anti-Pattern 7 | No interaction design | One-shot output without user confirmation and fix closure loop | Select interaction mode from 5.1 based on task type |
| Output Anti-Pattern 8 | Classification box instead of flow | Mermaid draws an issue classification box diagram without directional relationships | Use tables for classification info; flowcharts only for content with directional relationships |

---

## 9. Design Process (UR-SKILL Using This Guide)

When UR-SKILL generates a SKILL, design the SKILL's output content following these steps:

1. **Identify task type**: Code Review / Security Audit / Architecture Review / Research Investigation / Deployment Inspection / ...
2. **Check format decision matrix**: Determine preferred format type per 2.2
3. **Determine mandatory visualization**: Check 3.1 to see if Mermaid is needed; if yes, fill in mandatory rules
4. **Choose output structure**: Per 4, determine whether executive summary, issue grading, decision strategy, positive observations are needed
5. **Design user interaction**: Per 5.1, select interaction mode, fill in interaction tool and loop parameters
6. **Specify output path**: Per 6.1, fill in output file path template
7. **Write output specification**: Write the above decisions into the SKILL's "Output Specification" block

---

## 10. Completeness Checklist

- [ ] Output content defines at least 1 format type
- [ ] If task type triggers mandatory visualization → Mermaid requirement is included (minimum 1 diagram)
- [ ] Medium complexity and above → Executive summary structure is included
- [ ] Review-type SKILL → Issue grading + decision strategy is included
- [ ] Positive observations block is included (review type)
- [ ] User interaction mode is specified
- [ ] Output file path is specified
- [ ] Visualization diagram colors are explicitly specified (if Mermaid is used)
- [ ] No pure classification box diagram substituting for flowchart
