# Metadata Specification

> Standards compliant: [agentskills.io Specification](https://agentskills.io/specification)
> Core Principle: Minimalist. Interoperable with all platforms, introduce no platform-specific fields.

---

## Field Definitions

| Field | Location | Required | Constraint | Description |
|:---|:---|:---:|:---|:---|
| `name` | Top-level | Yes | 1-64 characters, kebab-case, all lowercase, must match parent directory name | SKILL unique identifier. Required by agentskills.io standard. |
| `description` | Top-level | Yes | 1-1024 characters; recommended to start with `Use when...` | **The only field used for trigger matching.** All platforms use this field to decide whether to load the SKILL. Should cover both capability description and trigger scenarios. |
| `metadata.updated` | Inside metadata | Yes | Format `YYYY-MM-DD` | Last updated date. Two purposes: (1) version change tracking; (2) helps the LLM perceive data freshness and determine whether domain knowledge might be outdated. Required by UR-SKILL convention. |

> **Those three fields, and nothing more.**

---

## Examples

### UR-SKILL Itself

```yaml
---
name: ur-skill-cn
description: "Use whenever the user wants to create, design, standardize, or package a SKILL.md file, AI agent skill, or structured system prompt. Invoke even if they don't explicitly say 'SKILL'. Chinese version."
metadata:
  updated: 2026-07-09
---
```

### General Skill Example

```yaml
---
name: python-code-review
description: "Use when the user wants to review Python code for quality, security, style, or performance. Invoke for code inspection, bug hunting, refactoring suggestions."
metadata:
  updated: 2026-07-14
---
```

### Sub-Skill Example (Inline Invocation)

```yaml
---
name: research-analyst
description: >-
  Use when analyzing user requirements, optimizing existing SKILLs, extracting knowledge from knowledge bases, or localizing external SKILLs.
  Supports four modes (A/B/C/D), outputs a unified pre-analysis report.
  Mode A is typically invoked inline by UR-SKILL; Modes B/C/D can be triggered independently or invoked inline.
metadata:
  updated: 2026-07-09
---
```

---

## Validation Rules

- `name` MUST match the regex `^[a-z0-9]+(?:-[a-z0-9]+)*$`
- `description` length MUST be between 1-1024 characters
- `metadata.updated` MUST be a valid date in `YYYY-MM-DD` format
- No undeclared top-level fields are allowed
