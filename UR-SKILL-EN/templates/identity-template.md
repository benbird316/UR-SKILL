# Identity Declaration Template

> **Purpose**: Define the standard format for the generated SKILL's identity declaration (system prompt role definition)
> **Core Principle**: Identity only answers "what is this role and what does it do"; capabilities, tools, style, and boundaries each have their place
> **Design Methodology**: See [design-guides/identity-design-guide.md](../design-guides/identity-design-guide.md)

---

## 1. Identity Declaration Template

```
You are a [role name], your core work is [one-sentence task].
{Optional: You specialize in [specific domain], following [methodology/system name].}
```

---

## 2. Filling Guidelines

| Element | Guideline | Example |
|:---|:---|:---|
| Role name | Specific occupation name, not "expert" or "assistant" | Code Security Review Engineer, Market Demand Analyst |
| Task description | One sentence describing the core work | Detect security vulnerabilities in code and provide remediation recommendations |
| Professional background | Optional; must specify concrete domain + methodology system | Specializes in OWASP Top 10 security review, following CWE classification methodology |

---

## 3. Correct and Incorrect Examples

| Type | Example | Notes |
|:---|:---|:---|
| Correct | You are a code security review engineer, your core work is detecting security vulnerabilities in code and providing remediation recommendations. | Role + task, no extraneous content |
| Incorrect | You are a world-class Python expert, proficient in all programming languages. | Identity inflation, vague titles |
| Incorrect | You only do syntax checks, not logic review. | Capability degradation mixed into identity |
| Incorrect | You are a code reviewer :shield: | Contains emoji |

---

## 4. Completeness Checklist

- [ ] Identity consists only of role + task (+ optional brief professional background), does not include capabilities, tools, style, or boundaries
- [ ] Role name is specific (engineer/analyst/reviewer/researcher/converter), not "expert"/"assistant"
- [ ] One-sentence task description is clear
- [ ] No vague titles (expert/professor/guru/master/senior)
- [ ] No self-coined abbreviations
- [ ] No emoji
- [ ] No capability degradation or scope-limiting statements

---

## 5. Metadata Design (YAML Frontmatter)

> Metadata is the only entry point for a SKILL to be discovered by an Agent. Follows the agentskills.io open standard: only `name` + `description` are required fields. UR-SKILL convention adds `metadata.updated` as an additional required field.
> See [metadata-spec.md](metadata-spec.md) and [design-guides/skill-package-design-guide.md §A.1](../design-guides/skill-package-design-guide.md).

### 5.1 Metadata Template

```yaml
---
name: {kebab-case-name}
description: >-
  Use when [user intent A], [user intent B], or [user intent C].
  Covers requests like '[trigger phrase 1]', '[trigger phrase 2]'.
  Invoke even if '[domain keyword]' is not explicitly mentioned.
metadata:
  updated: {YYYY-MM-DD}
---
```

### 5.2 Filling Guidelines

| Field | Guideline | Source |
|:---|:---|:---|
| name | kebab-case, includes domain keyword, <= 64 characters | agentskills.io required |
| description | Natural language trigger description, <= 1024 characters, includes trigger phrases + domain keywords | agentskills.io required |
| metadata.updated | YYYY-MM-DD format | UR-SKILL convention required |

### 5.3 description Design Guidelines

`description` is the **only trigger matching field across all platforms**. The Agent determines whether to load this SKILL through semantic matching.

| Principle | Description | Poor | Good |
|:---|:---|:---|:---|
| Imperative/scenario-based | "Use when the user wants X" rather than describing oneself | `"A security review skill"` | `Use when the user needs code security review, vulnerability detection` |
| Include trigger phrases | What users would actually say | Pure rule description without query | `Covers requests like 'review this code', 'help me check for security issues'` |
| Include domain keywords | Improve semantic matching precision | Vague "analysis" | `OWASP, security review, vulnerability detection` |
| Don't copy body | description only writes trigger info | description = body summary | description only writes trigger conditions, not capability descriptions |

### 5.4 Common Anti-Patterns

| Anti-Pattern | Incorrect | Correct |
|:---|:---|:---|
| English description for Chinese SKILL | `"Use when the user wants to..."` | Trigger phrases in the user's language |
| Descriptive rather than trigger-based | `"Helps users review code"` | `Use when the user needs code review` |
| Missing trigger examples | Pure rule description | `Covers requests like 'review this code'` |

---

## 6. Multi-Platform Metadata Template

> UR-SKILL uses **Claude Code native SKILL.md** as the baseline format. Frontmatter fields follow the agentskills.io standard (name + description + metadata), compatible with all platforms.

### 6.1 Platform Comparison Overview

| Platform | Format | File Path | Trigger Mechanism |
|:---|:---|:---|:---|
| Claude Code / TRAE / Tongyi Lingma / CodeBuddy | Native SKILL.md | `.claude/skills/{name}/SKILL.md` | description semantic matching |
| Cursor | `.cursor/rules/*.mdc` | `.cursor/rules/{name}.mdc` | glob file matching |
| Windsurf | `.windsurf/rules/*.md` | `.windsurf/rules/{name}.md` | trigger mode selection |
| GitHub Copilot | `.github/copilot-instructions.md` | `.github/copilot-instructions.md` | Full loading |

### 6.2 Template A: Claude Code Native SKILL.md (Baseline Template)

```yaml
---
name: {kebab-case-name}
description: >-
  Use when [user intent A], [user intent B], or [user intent C].
  Covers requests like '[trigger phrase 1]', '[trigger phrase 2]'.
metadata:
  updated: {YYYY-MM-DD}
---
```

### 6.3 Template B: Cursor `.cursor/rules/*.mdc`

```
---
description: "{SKILL capability summary}"
globs: ["{file matching pattern 1}", "{file matching pattern 2}"]
alwaysApply: false
---

# {SKILL Name}

{Paste all SKILL.md body content here}
```

### 6.4 Template C: Windsurf `.windsurf/rules/*.md`

```
---
trigger: {always_on | model_decision | glob | manual}
description: "{SKILL capability summary}"
---

{Paste all SKILL.md body content here}
```

### 6.5 Template D: GitHub Copilot `.github/copilot-instructions.md`

```markdown
# {SKILL Name}

{Paste all SKILL.md body content here. Remove YAML frontmatter, keep only Markdown body}
```

### 6.6 Delivery Checklist

- [ ] Target platform identified
- [ ] Baseline SKILL.md generated (Template A)
- [ ] If Cursor -> `.mdc` generated per Template B
- [ ] If Windsurf -> Rule file generated per Template C
- [ ] If Copilot -> `copilot-instructions.md` generated per Template D
