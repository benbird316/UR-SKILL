# Output Design Guide

> Only teaches how to design the SKILL's output. Answers "what to output, in what form, and how to deliver it to the user."
> For determining whether output design is needed, see skill-package-design-guide.md §2.

---

## §1 Design Thinking: 4-Question Framework

Before designing the output, answer the following 4 questions one by one.

### Q1: Output Form — What is the deliverable's format?

Choose from the following 6 high-level categories (11 specific format weapons in §2):

| Category | Applicable Scenario |
|:---|:---|
| Plain Text / Markdown | Analysis reports, narrative content, creative discussions |
| Structured Tables | Issue lists, scorecards, comparative analysis |
| Mermaid Diagrams | Process visualization, state transitions, component relationships |
| Code Blocks | Code generation, configuration output, scripts |
| JSON/YAML Structured Data | Output requiring downstream system parsing |
| Mixed | Most SKILLs — text + tables + code blocks |

When uncertain, default to `Mixed (Markdown body + structured tables + code blocks)`.

### Q2: Output Structure — In what order should it be organized?

General pattern: **Conclusion first -> Body expansion -> Recommendations to close**.

```
1. Conclusion/Summary    — Let the reader know the result in 5 seconds
2. Body Content          — Detailed analysis, data, evidence
3. Positive Feedback     — Not only negative (when applicable)
4. Recommendations/Next Steps — Actionable items
```

Each section declares "what the content includes," not "this section is about that topic."

### Q3: Quality Standard (Win Metric) — What counts as "good"?

Derived from the FLOW framework's core insight: define the **real-world tests** the output must pass — not abstract adjectives.

| SKILL Type | Win Metric Example |
|:---|:---|
| Code Review | "A junior developer can independently fix each comment without follow-up questions" |
| Security Audit | "The operations team can determine from the report whether an emergency rollback is needed" |
| Story Outline | "The user can start writing after just one follow-up question, without re-explaining the setting" |
| Chat Companion | "No unsafe content in 5 consecutive dialogue turns, and the user did not end the conversation due to inappropriate tone" |
| Data Analysis | "The CFO can read through it in 3 minutes and make a yes/no decision" |

Each Win Metric must be concrete and verifiable. Hollow terms like "high quality" or "excellent" are prohibited.

**Graded Failure Modes** (when output fails to meet the Win Metric):

| Failure Type | Applicable SKILL | Strategy |
|:---|:---|:---|
| Functional | Code review, security audit, data analysis | Define precise quantitative criteria (e.g., "vulnerability detection rate > 85%") |
| Creative | Novel writing, content generation | Provide style consistency criteria (e.g., "no character breaking," "consistent tone") |
| Social | Chat companion, emotional support | Provide safety/appropriateness criteria (e.g., "no discriminatory language," "don't overstep by providing psychological counseling") |

### Q4: Delivery Mode — How is it delivered to the user?

4 modes, chosen based on SKILL nature:

| Mode | Applicable Scenario | Description |
|:---|:---|:---|
| **One-time output** | Query, generation, translation | Completed in a single interaction |
| **Confirm-Fix-Verify Cycle** | Review, diagnosis, iterative improvement | Maximum N rounds; user confirms/modifies then re-validates each round |
| **Phased delivery** | Architecture design, multi-step planning | Phase 1 -> Confirm -> Phase 2 |
| **Interactive dialogue** | Consultation, companion, creative discussion | No fixed round limit, progresses naturally based on dialogue flow |

Cyclic modes must specify the maximum number of cycles. It is recommended to specify exit keywords (e.g., "end when user says 'no thanks'").

---

## §2 Format Type Taxonomy

First understand what weapons are available, then decide which to use.

| Format Type | Applicable Scenario | Advantages | Disadvantages |
|:---|:---|:---|:---|
| **Markdown Table** | Data comparison, issue lists, graded results | Clear structure, sortable | Cannot express process logic |
| **Mermaid Flowchart** | Business processes, call chains, data flows | Process and relationships immediately visible | Static diagram, non-interactive |
| **Mermaid Sequence Diagram** | API call chains, request-response flows | Clear temporal relationships | Verbose with many nodes |
| **Mermaid State Diagram** | State machines, workflow transitions | State transitions visualized | Only applies to state-driven scenarios |
| **Code Block** | Fix solutions, example code | Directly copyable | Language must be specified |
| **Checklist** | Verification items, self-check items, task lists | Verifiable item by item | Lacks contextual explanation |
| **Executive Summary** | High-level conclusions, decision recommendations | Quick to read | Lacks detail |
| **Severity Grading Table** | Security vulnerabilities, quality issues | Clear priorities | Requires precise grade definitions |
| **Comparison Matrix** | Solution selection, tool comparison | Multi-dimensional intuitive comparison | Becomes complex with more dimensions |
| **Narrative Report** | Analysis conclusions, research investigations | Rich context | Verbose, hard to quickly locate information |
| **Decision Conclusion** | Clear action decisions | Directly actionable | Binary judgment may be oversimplified |

---

## §3 Visualization Rules

### 3.1 Trigger Conditions (any one met)

1. Output involves **process/logic chain** description
2. Output involves **multi-component interaction**
3. Output involves **state transition**

### 3.2 Mandatory Rules

| Rule | Description |
|:---|:---|
| At least 1 diagram | When trigger conditions are met, must include at least 1 Mermaid diagram |
| Prefer flowcharts and sequence diagrams | `flowchart` or `sequenceDiagram`, showing process/call/data flows |
| No pure classification block diagrams | Block diagrams that only group without flow relationships are not allowed |
| Mandatory color specification | Fill colors and text colors must be explicitly specified to ensure readability in both light and dark themes |
| Diagram type matching | Architecture -> `graph TD`, calls -> `sequenceDiagram`, states -> `stateDiagram` |

### 3.3 Exemption Conditions

- Output content is pure text analysis (no flow relationships)
- Output content is a single conclusion (e.g., "Pass/Fail")

---

## §4 Output Structure General Pattern

### 4.1 Conclusion/Summary Layer

```markdown
## Conclusion

**Core Judgment**: {one-sentence conclusion}
**Key Findings**:
1. [Most important finding]
2. [Second most important finding]
```

### 4.2 Body Content Layer

Organized by logical groups; format determined by the weapon selection from §2. Each group declares "what is presented here" rather than "what this is called."

### 4.3 Positive Feedback (Recommended)

```markdown
## Positive Observations

- ✅ [Aspect worth acknowledging]
- ✅ [Well-done aspect]
```

### 4.4 Recommendations / Next Steps

```markdown
## Recommendations

### Priority Actions
- [ ] [Action item]

### Future Considerations
- [ ] [Action item]
```

---

## §5 User Interaction Modes

| Mode | Applicable Scenario | Example |
|:---|:---|:---|
| **One-time report** | Simple queries, research investigation | End after outputting complete report |
| **Confirm-Fix-Verify Cycle** | Review, diagnostic | Output issues -> User confirms -> Fix and verify -> Confirm |
| **Phased delivery** | Complex analysis | Summary first -> User confirms -> Detailed report |
| **Asynchronous scheduled** | Periodic inspection | Scheduled execution -> Auto-push to designated location/channel |

---

## §6 Format Skeleton

The following is the generic fill-in structure for references/output-spec.md:

```markdown
> Loading phase: Step 5

## Output Form
- **Category**: {Plain Text / Structured Table / Mermaid Diagram / Code Block / JSON / Mixed}
- **Visualization**: {Yes/No} -> If yes, need {flowchart / sequenceDiagram / stateDiagram}, colors explicitly specified

## Output Structure
1. {Section name} — {Content description}
2. {Section name} — {Content description}

## Delivery Mode
- **Mode**: {One-time / Confirm-Fix-Verify / Phased / Interactive}
- **Cycle Limit**: {N rounds, if applicable}
- **Exit Keyword**: {If applicable}

## Output File Path
- **Path**: `{directory}/{filename}-{date}.md`
- **Format**: Markdown, UTF-8 encoding

## Delivery Checklist
- [ ] {Verifiable check item}
- [ ] {Verifiable check item}
```

---

## §7 Rules

- Grading criteria must be quantified — vague words like "severe" or "important" are prohibited; trigger conditions must be written
- Each item in the delivery checklist must be binary verifiable (yes/no) — vague wording like "ensure quality" is prohibited
- Output structure ordered by user reading sequence (Conclusion -> Body -> Recommendations)
- Win Metrics must be concrete and verifiable; hollow adjectives are prohibited
- Delivery mode must specify cycle limit or exit keyword
- When visualization is triggered, must include a Mermaid diagram with explicitly specified colors

---

## §8 Checklist

- [ ] Each of the 4 questions in the framework has been clearly answered
- [ ] Output content defines at least 1 format type
- [ ] If mandatory visualization is triggered -> Mermaid requirements are included (at least 1 diagram)
- [ ] Positive observation section is included (if applicable)
- [ ] User interaction mode is specified
- [ ] Output file path is specified
- [ ] Visualization diagram colors are explicitly specified (if Mermaid is used)
- [ ] No pure classification block diagram used as a substitute for flowcharts
- [ ] Win Metrics are concrete and verifiable, no hollow adjectives

---

## §9 Length Constraint

references/output-spec.md <= 120 lines. Output specifications should be concise — do not mix in analysis or fix content.
