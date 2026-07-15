# Identity Design Guide

> Only teaches how to write the SKILL's identity declaration. The identity declaration is the first component of the system prompt, determining the model's knowledge domain activation, style positioning, and behavioral patterns.
> For determining identity design needs, see skill-package-design-guide.md §2.

---

## §1 Identity Declaration Structure

The identity declaration only needs Role + Task + optional Professional Background. Capabilities, tools, style, and boundaries each belong in their corresponding templates and are not repeated in the identity.

```markdown
You are a [Role Name]; your core task is to [one-sentence task].
```

Optional brief professional background:
```markdown
You specialize in [specific domain], following [methodology/system].
```

---

## §2 Identity Gradient

Identity precision is divided into 5 levels; generated SKILLs must reach at least Level 3:

| Level | Structure | Example |
|:---:|:---|:---|
| 0 | No identity | "Generate a code review report" |
| 1 | Simple role | "You are a code review engineer" |
| 2 | Role + Domain expertise | "You are a code review engineer, specializing in security vulnerability detection and OWASP Top 10" |
| 3 | Role + Domain expertise + Methodology | "You are a code review engineer, specializing in OWASP vulnerabilities and injection attack detection. You follow the CWE classification system for systematic inspection" |
| 4 | Role + Domain expertise + Methodology + Style | "You are a code review engineer, specializing in OWASP vulnerability detection. Review style: first identify risk level, then provide fix suggestions for each item" |
| 5 | Role + Domain expertise + Methodology + Style + Tool constraints | "You are a code review engineer... Use [文件读取] to read code, [文本搜索] to search for vulnerability patterns" |

> Generated SKILLs must reach at least Level 3 (Role + Domain expertise + Methodology). Review/analysis-type SKILLs should reach Level 4 or 5.

---

## §3 DOs

| Principle | Description | Example |
|:---|:---|:---|
| **Specific role name** | Use concrete roles like engineer/analyst/reviewer/translator | `Code Security Review Engineer` |
| **Specific methodology** | Use methodology/system names to anchor depth | `Following CWE classification methodology` |
| **Specific domain** | Narrow the knowledge domain scope | `Specializing in OWASP injection attacks` |
| **Specific style** | Use behavioral descriptions rather than adjectives | `First identify risk level, then provide fix suggestions for each item` |
| **Positive statements** | Say what it can do, not what it cannot do | `You can read code and search for vulnerability patterns` |
| **Uncertainty handling** | Clearly state "what to do when unsure" | `Mark uncertain items as "pending confirmation," do not force a judgment` |

---

## §4 DON'Ts

| Principle | Incorrect Example |
|:---|:---|
| **Vague title** | `You are the world's top Python expert` |
| **Fabricated years of experience** | `You have 5 years of security review experience` |
| **Empty adjectives** | `Senior / Professional / Top-tier` |
| **Generic role** | `You are a helpful AI assistant` |
| **Self-created abbreviations** | `You are a CRT engineer` |
| **Emoji** | `You are a code reviewer :shield:` |
| **Negative identity** | `You are a junior programmer` |
| **Disclaimer statements** | `You only do syntax checking, not logic review` |
| **Identity duplicated with MUST NOT** | Identity says "You don't do X," MUST NOT also says "Prohibit X" |

---

## §5 Metadata Activation Design

### 5.1 description Design Specification

**MUST** Use imperative mood, telling the Agent when to invoke:

```yaml
# Poor — trigger rate < 30%
description: "This is a code review skill for finding bugs."

# Good — trigger rate > 85%
description: >-
  Use when the user asks to review, audit, or analyze code for security
  vulnerabilities, bugs, or quality issues. MUST invoke if the user mentions
  'security review', 'code audit', '漏洞审查', or '安全检查', even if they
  don't explicitly name 'OWASP' or 'vulnerability'. Trigger examples:
  '审查这段代码的安全性', 'check my code for vulnerabilities'.
  Do NOT invoke for code style formatting or documentation generation.
```

| Principle | Description | Example |
|:---|:---|:---|
| **Imperative mood** | Start with "Use when..." to instruct the Agent to act | `Use when the user asks to...` |
| **Focus on user intent** | Describe what the user wants to do, not the SKILL's internal implementation | `Use when analyzing spreadsheet data` |
| **Pushy tone** | Actively declare the trigger scope, include "even if" as safety net | `even if they don't explicitly mention "security"` |
| **Capitalized keywords** | MUST/ALWAYS increase attention weight | `MUST invoke when...` |
| **Trigger examples** | 1-2 user query examples | `Trigger: "审查这段代码的安全性"` |
| **Negative exclusion** | Clearly state when NOT to trigger | `Do NOT invoke for general code style questions` |
| **<= 1024 characters** | agentskills.io hard limit | Exceeding will be truncated |

### 5.2 whenToUse Design Specification

`whenToUse` is the Chinese trigger description, complementing `description`:

```yaml
# Good
metadata:
  whenToUse: 当用户需要代码安全审查、OWASP 漏洞检测或认证逻辑审计时

# Poor — exact duplicate of description
metadata:
  whenToUse: Use when reviewing code for security.
```

---

## §6 Checklist

- [ ] Has a clear role name (engineer/analyst/reviewer/translator), not "expert" or "assistant"
- [ ] One-sentence task description is clear, does not contain capability/tool/style content
- [ ] Professional background (optional) has specific domains and methodology systems, no fabricated years of experience
- [ ] No vague titles (expert, professor, master, guru)
- [ ] No self-created abbreviations
- [ ] No emoji
- [ ] Capabilities/tools/style from the identity have been placed into corresponding templates, not repeated in the identity
- [ ] description starts with "Use when..." or "Invoke ONLY when..." (imperative mood)
- [ ] description describes user intent (what the user wants to do), not SKILL internal implementation
- [ ] description contains 1-2 trigger examples
- [ ] description contains negative exclusion instructions (when NOT to trigger)
- [ ] description <= 1024 characters
- [ ] whenToUse is a Chinese scenario description, complementing description
