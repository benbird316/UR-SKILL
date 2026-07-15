# Reference File Design Guide

> Core Principle: One ref file = knowledge support for one workflow step. The Agent loads on demand and releases after use.
> This guide only defines format rules for five types of ref files. For determining whether a ref file is needed, see skill-package-design-guide.md §2.

---

## §0 Prelude: Where the 5 Ref Types Fit in the File Hierarchy

**5 types of ref ≠ all reference files.** They are a sub-classification of "domain knowledge reference files," categorized by workflow stage and purpose.

The entire SKILL deliverable's reference file hierarchy is divided into:

| Tier | File Type | Description |
|:---|:---|:---|
| **Three Baseline Files** | example.md / anti-patterns.md / troubleshooting.md | Present in almost every complete SKILL (exceptions: single-file SKILLs, prompt-only SKILLs, user explicitly states not needed) |
| **5 Types of Domain Knowledge Refs** | Classification / Detection Methods / Verification / Pattern / Output Spec | Added on demand, targeting specific domain knowledge, mapped one-to-one with workflow stages |
| **Other Independent Files** | glossary.md | Added when many custom terms or cross-domain needs arise |

**Common Distinctions to Note:**
- "Verification ref" (verification-patterns.md) = verifies the truth of domain knowledge — belongs to **domain knowledge** scope
- "Troubleshooting file" (troubleshooting.md) = how to fix issues when the SKILL runs — belongs to **three baseline files** scope
- "Pattern ref" (fix-patterns.md) = positive solution patterns — belongs to **domain knowledge** scope
- "Anti-pattern file" (anti-patterns.md) = negative error patterns — belongs to **three baseline files** scope

---

## §1 Five Types of Ref Files

> The storage location, trigger conditions, and design guide mapping for the 5 ref types are detailed in [skill-package-design-guide.md §3](skill-package-design-guide.md) File Type Quick Reference Table. This section only supplements the workflow stage and semantic description of "what it answers."

| Type | Workflow Stage | Answers |
|:---|:---|:---|
| Classification | Analysis/Parse | "What is this?" |
| Detection Methods | Scan/Identify | "How to find it?" |
| Verification | Verify/Calibrate | "Is it real?" |
| Pattern | Fix/Execute | "How to do it?" |
| Output Spec | Output/Deliver | "How to output?" |

---

## §1.1 Knowledge Source Classification (K1-K4, for research-analyst determination)

When research-analyst investigates knowledge sources, they are divided into four types by content type. The same knowledge source type may fall into different ref types depending on **purpose**:

| K Class | Knowledge Source Type | Typical Example | Maps to Which Ref (Depends on Purpose) |
|:---|:---|:---|:---|
| **K1** Domain Knowledge | Concept systems, rules, methodologies, best practices | OWASP (security), PEP 8 (Python), Xiaohongshu formatting specs | Classification ("What is this?") **or** Detection Methods ("How to find violations?") |
| **K2** API/Tool Reference | API signatures, CLI commands, function parameters | React API, AWS CLI, PostgreSQL syntax | Detection Methods — "How to call? What are the parameters?" |
| **K3** Configuration/Policy | Compliance requirements, security policies, enterprise standards | SOC 2 policies, GDPR clauses, internal coding standards | Classification — "What are the rules/boundaries?" |
| **K4** Design Patterns/Architecture | Reusable solutions, paradigms, architecture patterns | Microservices architecture, state machine patterns, MVC | Pattern — "How to do it? Positive/negative comparison?" |

> **Decision Rule**: One knowledge source = one K class. For the same K1 knowledge (e.g., OWASP SQL injection), if the purpose is "let the LLM understand the concept" -> Classification ref; if the purpose is "teach the LLM to locate SQL injection in code" -> Detection Methods ref. K2 naturally leans toward Detection Methods, K3 toward Classification, K4 toward Pattern. K1 requires research-analyst to clarify the purpose before classification.

## §1.2 Three Principles of Reference File Design

All 5 types of ref files share the following design principles:

| Principle | Content | Unqualified Example |
|:---|:---|:---|
| **Atomicity** | One entry = one unit topic, no internal cross-references | "See §2.3.1" (file-internal self-reference, requiring jumping while reading) |
| **Referencability** | Each entry has a unique path-based identifier (e.g., `T01`, `AP-01`); workflow can reference directly | Unnumbered plain headings; can only say "roughly in the middle section" |
| **Timeliness** | Each entry marks the source + acquisition date; domains with unstable knowledge sources require periodic refresh | "According to the latest research..." (no date, cannot determine if outdated) |

> Atomicity: The Agent reads only one entry at a time and should not need to look back at previous content due to a reference.
> Referencability: SKILL.md writes "see ref §T03"; the Agent can jump precisely.
> Timeliness: The LLM can judge whether knowledge may be outdated based on the date.

## §2 Step Binding

Each workflow step corresponds to 0-1 ref files. Steps and ref types are bound one-to-one:

```
Step 1 (Analyze)   -> Classification -> classification.md
Step 2 (Scan)      -> Detection Methods -> detection-methods.md
Step 3 (Verify)    -> Verification    -> verification-patterns.md
Step 4 (Fix)       -> Pattern        -> fix-patterns.md
Step 5 (Output)    -> Output Spec    -> output-spec.md
```

**MUST** Use the workflow stage name for naming; knowledge topic naming (e.g., `rca-methodology.md`) is prohibited.
**MUST** When adjacent steps cannot be cleanly separated, merge and name `phase-{N}-{M}-{purpose}.md`, with the file header specifying the loading step range.

---

## §3 Progressive Loading Contract

Agent execution mode: **One step at a time, one file per concern**.

```
Enter Step 1 -> Load classification.md -> Complete -> Release
Enter Step 2 -> Load detection-methods.md -> Complete -> Release
...
```

**Ref file header contract declaration** (required):
```markdown
> Loading phase: Step {N} | Load when entering Step N, release after completion
```

**Workflow step reference** (required):
```markdown
**Read File**: `references/{filename}.md` — Purpose: {one sentence}
```

**MUST NOT** Use vague declarations ("read all files under references/").
**MUST NOT** Step 1 loads Step 4's ref.
**MUST NOT** Ref content spans multiple steps (e.g., classification.md mixed with fix strategies).

---

## §4 Length Constraint

- Single ref **MUST** be <= 200 lines
- Exceeded -> Check if it crosses step boundaries (primary root cause)
- Confirmed no boundary crossing but still exceeded -> Split by sub-topic within the step: `classification-p1.md`
- **MUST NOT** `phase-01-all.md` cramming all step knowledge into one file

---

## §5 Checklist

- [ ] Does each step have a corresponding ref (or annotated as "no ref needed")?
- [ ] Are refs named according to the 5 types (classification/detection-methods/verification/pattern/output-spec)?
- [ ] Does each ref header have a loading phase declaration?
- [ ] Does each workflow step declare `**Read File**` with a specific filename?
- [ ] Does ref content strictly correspond to a single step?
- [ ] Is each ref <= 200 lines?
