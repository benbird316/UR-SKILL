# Identity Declaration Template

> Purpose: Defines the standard fill-in format for generating SKILL identity declarations (system prompt role definitions)
> Core principle: Identity only answers "who am I and what do I do"; capability, tools, style, and boundaries each have their own place
> Design methodology: see [design-guides/identity-design-guide.md](../design-guides/identity-design-guide.md)

---

## 1. Identity Declaration Template

```
You are a [role name], and your core task is [one-sentence task description].
{Optional: You focus on [specific domain], following the [methodology/system name].}
```

---

## 2. Fill-in Specification

| Element | Specification | Example |
|:---|:---|:---|
| Role name | Specific job title, not "expert"/"assistant" | Code Security Audit Engineer, Market Demand Analyst |
| Task description | One sentence describing the core task | Detect security vulnerabilities in code and provide remediation suggestions |
| Professional background | Optional; requires specific domain + methodology system | Focuses on OWASP Top 10 security auditing, following the CWE classification methodology |

---

## 3. Positive and Negative Examples

| Type | Example | Notes |
|:---|:---|:---|
| Positive | You are a code security audit engineer, and your core task is detecting security vulnerabilities in code and providing remediation suggestions. | Role + task, no extraneous content |
| Negative | You are a world-class Python expert proficient in all programming languages. | Identity inflation, vacuous titles |
| Negative | You only perform syntax checks and are not responsible for logic review. | Capability Degradation mixed into identity |
| Negative | You are a code reviewer :shield: | Contains emoji |

---

## 4. Completeness Checklist

- [ ] Identity contains only role + task (+ optional brief professional background), no capability, tools, style, or boundary content
- [ ] Role name is specific (Engineer/Analyst/Auditor/Researcher/Converter), not "expert"/"assistant"
- [ ] One-sentence task description is clear
- [ ] No vacuous titles (expert/professor/master/guru/senior)
- [ ] No self-coined abbreviations
- [ ] No emoji
- [ ] No Capability Degradation or scope limitation statements

---

## 5. Metadata Design (YAML Frontmatter)

> Metadata (name / description / whenToUse) is the sole entry point for SKILL discovery by the Agent. Design methodology: see [design-guides/identity-design-guide.md section 10](../design-guides/identity-design-guide.md).

### 5.1 Metadata Template

```yaml
---
name: {kebab-case-name}
description: >-
  Use when [user's desired goal A], [goal B], or [goal C].
  MUST invoke if the user mentions [keyword 1], [keyword 2], or [keyword 3],
  even if they don't explicitly name [domain]. Trigger examples:
  '[user query example 1]', '[user query example 2]'.
  Do NOT invoke for [exclusion scenario 1] or [exclusion scenario 2].
metadata:
  updated: {YYYY-MM-DD}
  type: prompt
  whenToUse: When [Chinese scenario description, complementary to description]
---
```

### 5.2 Fill-in Specification

| Field | Specification | Required |
|:---|:---|:---|
| name | kebab-case, includes domain keyword, <= 64 characters | Yes |
| description | Imperative "Use when...", <= 1024 characters, includes trigger examples + negative exclusions | Yes |
| metadata.type | Fixed value `prompt` | Yes |
| metadata.whenToUse | Chinese scenario description, complementary to description without duplication | Yes |
| metadata.updated | YYYY-MM-DD format | Yes |

### 5.3 Good vs. Bad Comparison

```yaml
# Bad -- low trigger rate (descriptive, no examples, no exclusions)
description: "This is a skill for code security review."
metadata:
  whenToUse: Code review

# Good -- high trigger rate (imperative, with examples, with exclusions)
description: >-
  Use when the user asks to review, audit, or analyze code for security
  vulnerabilities, bugs, or quality issues. MUST invoke if the user mentions
  'security review', 'code audit', 'vulnerability review', or 'security check', even if they
  don't explicitly name 'OWASP'. Trigger examples:
  'Review this code for security issues', 'check my code for vulnerabilities'.
  Do NOT invoke for code style formatting or documentation generation.
metadata:
  whenToUse: When the user needs code security review, OWASP vulnerability detection, or authentication logic auditing
```

### 5.4 Common Metadata Anti-Patterns

| Anti-pattern | Incorrect Example | Correction |
|:---|:---|:---|
| Descriptive instead of imperative | `"This skill helps with..."` | `"Use when the user needs to..."` |
| Missing trigger examples | Pure rule description without queries | Add `Trigger examples: '...'` |
| Missing negative exclusions | May be falsely triggered | Add `Do NOT invoke for...` |
| Duplicating body content | description = first paragraph of body | description writes only trigger conditions |
| whenToUse copies description | Chinese and English are identical | whenToUse writes complementary Chinese scenario |

---

## 6. Multi-Platform Metadata Templates

> UR-SKILL uses **Claude Code native SKILL.md** as the baseline format. The following 4 templates cover major domestic and international platforms; select the appropriate template for the target platform upon delivery.

### 6.1 Platform Comparison Overview

| Platform | Format | File Path | Trigger Mechanism | Domestic Popularity |
|:---|:---|:---|:---|:---|
| Claude Code | Native SKILL.md | `.claude/skills/{name}/SKILL.md` | description semantic matching | High |
| Codex CLI | Native SKILL.md | `.agents/skills/{name}/SKILL.md` | description semantic matching | Medium |
| Gemini CLI | Native SKILL.md | `.claude/skills/{name}/SKILL.md` | description semantic matching | Low |
| **TRAE** | Native SKILL.md | `.claude/skills/{name}/SKILL.md` | description semantic matching | **Highest** |
| Tongyi Lingma | Native SKILL.md compatible | Same as Claude Code | description semantic matching | High |
| CodeBuddy | Native SKILL.md compatible | Same as Claude Code | description semantic matching | High |
| **Cursor** | `.cursor/rules/*.mdc` | `.cursor/rules/{name}.mdc` | glob file matching | **Highest** |
| **Windsurf** | `.windsurf/rules/*.md` | `.windsurf/rules/{name}.md` | trigger mode selection | High |
| **GitHub Copilot** | `.github/copilot-instructions.md` | `.github/copilot-instructions.md` | Full load (no progressive) | High |

### 6.2 Template A: Claude Code Native SKILL.md (Baseline Template)

> Applicable: Claude Code / Codex CLI / Gemini CLI / TRAE / Tongyi Lingma / CodeBuddy

```yaml
---
name: {kebab-case-name}
description: >-
  Use when [user's desired goal A], [goal B], or [goal C].
  MUST invoke if the user mentions [keyword 1], [keyword 2], or [keyword 3],
  even if they don't explicitly name [domain]. Trigger examples:
  '[user query example 1]', '[user query example 2]'.
  Do NOT invoke for [exclusion scenario 1] or [exclusion scenario 2].
metadata:
  updated: {YYYY-MM-DD}
  type: prompt
  whenToUse: When [Chinese scenario description, complementary to description]
---
```

**Key differences**: This is the baseline format and requires no conversion. TRAE and Tongyi Lingma natively support this format. `description` is the sole trigger entry and MUST follow the imperative sentence pattern specification in Section 5.1-Section 5.2.

---

### 6.3 Template B: Cursor `.cursor/rules/*.mdc`

> Applicable: Cursor IDE

```
---
description: "{Brief SKILL capability description, used by AI to determine whether to load this rule}"
globs: ["{file matching pattern 1}", "{file matching pattern 2}"]
alwaysApply: false
---

# {SKILL Name}

{Paste the full SKILL.md body content here}
```

**Key differences**:
- Cursor uses **glob file matching** rather than semantic matching -- rules load only when matching files are edited
- `description` is only 1 sentence (for AI relevance judgment), not a complete trigger contract
- `globs` determines when to load (e.g., `"**/*.tsx"`, `"src/api/**/*.ts"`)
- `alwaysApply: true` loads on every message (high token consumption, use only for core conventions)
- The full SKILL.md body must be pasted into the .mdc file body

**Example**:
```
---
description: "Code security review: detect OWASP Top 10 vulnerabilities, injection attacks, hardcoded credentials"
globs: ["**/*.ts", "**/*.js", "**/*.py", "**/*.java", "**/*.go"]
alwaysApply: false
---

# Code Security Review

When reviewing code, always check:
1. SQL injection (string concatenation to construct database queries)
2. Hardcoded secrets (API keys, passwords, tokens)
...
```

---

### 6.4 Template C: Windsurf `.windsurf/rules/*.md`

> Applicable: Windsurf IDE

```
---
trigger: {always_on | model_decision | glob | manual}
description: "{Brief SKILL capability description}"
---

{Paste the full SKILL.md body content here}
```

**Key differences**:
- 4 trigger modes:
  - `always_on` = full injection on every message (6,000 char/file limit, 12,000 total limit)
  - `model_decision` = only description in context, AI decides whether to load full text
  - `glob` = activates when file path matches
  - `manual` = loads only on `@mention`
- No progressive loading; full injection; content must be curated to control tokens
- Total of all rule files <= 12,000 characters

**Example**:
```
---
trigger: model_decision
description: "Code security review rules: OWASP Top 10 vulnerability detection and remediation suggestions"
---

When reviewing code, always check:
1. SQL injection...
...
```

---

### 6.5 Template D: GitHub Copilot `.github/copilot-instructions.md`

> Applicable: GitHub Copilot (VS Code / JetBrains / GitHub.com)

```markdown
# {SKILL Name}

{Paste the full SKILL.md body content here. Remove YAML frontmatter, keep only Markdown body}
```

**Key differences**:
- Pure Markdown, **no YAML frontmatter**
- Full load, no progressive -- all instructions are always in context
- Only one file `.github/copilot-instructions.md`
- Multiple SKILLs must be separated with `##` second-level headings
- Applicable to Copilot Chat, not inline completions

**Example**:
```markdown
# Code Security Review

When reviewing code, always check:
1. SQL injection (string concatenation to construct database queries)
2. Hardcoded secrets (API keys, passwords, tokens)
...

## Project Build Rules

- Use `pnpm build` for building
- Test with `pnpm test`
```

### 6.6 Delivery Checklist

- [ ] Target platform(s) identified (single or multiple selection)
- [ ] Baseline SKILL.md generated (Template A)
- [ ] If Cursor needed -- `.mdc` generated per Template B, globs correctly configured
- [ ] If Windsurf needed -- rule file generated per Template C, trigger mode selected
- [ ] If Copilot needed -- `copilot-instructions.md` generated per Template D
- [ ] Template B/C/D body content consistent with baseline SKILL.md
