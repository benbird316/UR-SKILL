# Metadata Specification

> Purpose: Defines fields, types, constraints, and examples for SKILL.md YAML frontmatter
> Core Principle: Frontmatter is the trigger layer and identity layer of a SKILL; it must be concise, mechanically parsable, and trigger-friendly
> Standards compliant: [agentskills.io Specification](https://agentskills.io/specification)

---

## Field Definitions

### Required Fields (agentskills.io Standard)

| Field | Type | Required | Constraints | Description |
|:---|:---|:---:|:---|:---|
| `name` | string | Yes | 1–64 chars, kebab-case, lowercase only, no spaces; must match parent directory name | Unique SKILL identifier |
| `description` | string | Yes | 1–1024 chars; strongly recommended to start with `Use when...`; covers capability + trigger scenario | Trigger condition and capability description |

### Optional Fields (agentskills.io Standard)

| Field | Type | Required | Constraints | Description |
|:---|:---|:---:|:---|:---|
| `license` | string | No | SPDX identifier or license filename, recommend ≤50 chars | License declaration |
| `compatibility` | string | No | 1–500 chars, declares required environment | Compatibility notes (platform, Python version, etc.) |
| `metadata` | dict | **Yes** | Must contain at least `updated` field | Arbitrary key-value pairs for extensions |
| `allowed-tools` | string | No | Space-separated tool names (experimental field) | Pre-approved tool whitelist |

### UR-SKILL Custom Fields (stored under `metadata`)

| Field | Type | Required | Constraints | Description |
|:---|:---|:---:|:---|:---|
| `metadata.type` | string | Yes | Enum: `prompt` / `tool` / `hybrid` | SKILL type (UR-SKILL custom) |
| `metadata.whenToUse` | string | Yes | English, 20–100 chars, specific scenario | Supplementary trigger scenario (UR-SKILL custom) |
| `metadata.updated` | string (date) | Yes | Format `YYYY-MM-DD` | Last updated date |

> **Design Principle**: The agentskills.io standard only requires `name` and `description`. `metadata` carries UR-SKILL's own extension fields (`type`, `whenToUse`) without affecting standard compliance.

---

## Constraints

- `description` should be slightly **pushy**: while describing capabilities, proactively cover synonymous expressions users might use, reducing undertrigger probability.
- `metadata.type` determines subsequent output structure:
  - `prompt`: Pure prompt SKILL, no scripts/resources.
  - `tool`: Contains executable scripts or MCP calls.
  - `hybrid`: Prompt + scripts/resources hybrid.
- `license`: Recommend using standard SPDX identifiers (e.g., `Apache-2.0`, `MIT`).
- `compatibility`: Only needed when the SKILL has special environment requirements; most SKILLs don't need it.
- Do not introduce undeclared fields in frontmatter to avoid parsing failures.

---

## Examples

### Minimal Example (agentskills.io compliant)

```yaml
---
name: python-code-review
description: "Use when the user wants to review Python code for quality, security, style, or performance. Invoke for code inspection, bug hunting, refactoring suggestions."
---
```

### Full Example (UR-SKILL Recommended)

```yaml
---
name: python-code-review
description: "Use when the user wants to review Python code for quality, security, style, or performance. Invoke for code inspection, bug hunting, refactoring suggestions, or CI-ready linting tasks."
license: Apache-2.0
compatibility: Requires Python 3.12+
allowed-tools: Read Write Grep Glob RunCommand
metadata:
  updated: 2026-07-09
  type: prompt
  whenToUse: When the user needs to review Python code quality, security vulnerabilities, code style, or performance
---
```

---

## Validation Rules

- `name` must match regex `^[a-z0-9]+(?:-[a-z0-9]+)*$`
- `description` length must be 1–1024 characters
- `metadata.type` must be one of `prompt` / `tool` / `hybrid`
- `metadata.updated` must be a valid date `YYYY-MM-DD`
