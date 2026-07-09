# Metadata Specification

> Purpose: Defines fields, types, constraints, and examples for SKILL.md YAML frontmatter
> Core Principle: Frontmatter is the trigger layer and identity layer of a SKILL; it must be concise, mechanically parsable, and trigger-friendly

---

## Field Definitions

| Field | Type | Required | Constraint | Description |
|:---|:---|:---:|:---|:---|
| `name` | string | Yes | kebab-case, all lowercase, no spaces, length <= 40 | Unique SKILL identifier |
| `description` | string | Yes | 50-200 characters; strongly recommended to start with `Use when...`; covers capability + trigger scenario | Trigger condition and capability description |
| `type` | string | Yes | Enum values: `prompt` / `tool` / `hybrid` | SKILL type |
| `whenToUse` | string | Yes | Chinese, 20-100 characters, specific scenario | Supplementary trigger scenario |
| `metadata.updated` | string (date) | Yes | Format `YYYY-MM-DD` | Last update date |

---

## Constraint Notes

- `description` should be slightly **pushy**: while describing capabilities, proactively cover synonymous expressions users might use, reducing the probability of undertrigger.
- `type` determines the subsequent output structure:
  - `prompt`: Pure prompt SKILL, no scripts/resources.
  - `tool`: Contains executable scripts or MCP calls.
  - `hybrid`: Mixed prompt + scripts/resources.
- Do not introduce undeclared fields in frontmatter to avoid parsing failures.

---

## Example

```yaml
---
name: python-code-review
description: "Use when the user wants to review Python code for quality, security, style, or performance. Invoke for code inspection, bug hunting, refactoring suggestions, or CI-ready linting tasks."
type: prompt
whenToUse: 当用户需要审查 Python 代码质量、安全漏洞、风格或性能时
metadata:
  updated: 2026-07-09
---
```

---

## Validation Rules

- `name` must match regex `^[a-z0-9]+(?:-[a-z0-9]+)*$`
- `description` length must be between 50-200 characters
- `type` must be one of `prompt` / `tool` / `hybrid`
- `metadata.updated` must be a valid date `YYYY-MM-DD`
