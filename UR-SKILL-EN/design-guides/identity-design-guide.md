# Identity Design Guide

> Purpose: Guides the identity design of SKILLs, ensuring generated SKILLs have clear, effective identity declarations.

---

## 1. Why Identity Matters

The body of SKILL.md is the system prompt itself. The identity declaration is the first component of the system prompt and determines the model's knowledge domain activation, style positioning, and behavioral patterns.

**Consequences of not distinguishing:**

- No identity → the model degrades to a general-purpose assistant, producing generic, untargeted output
- Hollow identity ("you are an expert") → cognitive drift, factual accuracy decline (USC 2026.3: knowledge retrieval dropped from 71.6% to 66.3%)
- Exaggerated identity ("world-class professor") → overconfidence, fabrication of information (Wharton UPenn 2025.12)

**Benefits of correct design:**

- Precisely activates domain knowledge subsets
- Stabilizes output style and reasoning depth
- Experience filling effect: specific background descriptions trigger the model to automatically recall niche knowledge

---

## 2. Identity Gradient Model

Identity precision is divided into 5 levels. Each level increase brings a significant improvement in output quality and domain targeting:

```
Level 0: No Identity
 "Generate a code review report."
 → Output: generic, templated, unremarkable

Level 1: Simple Role
 "You are a code review engineer."
 → Output: more structured than Level 0, still somewhat generic

Level 2: Role + Domain Expertise
 "You are a code review engineer specializing in security vulnerability detection and the OWASP Top 10 analysis methodology."
 → Output: strong domain targeting

Level 3: Role + Domain Expertise + Methodology
 "You are a code review engineer specializing in OWASP vulnerabilities and injection attack detection. You inspect layer by layer following the CWE classification system, first identifying risk levels, then providing remediation suggestions item by item."
 → Output: significantly deeper

Level 4: Role + Domain Expertise + Methodology + Style
 "You are a code review engineer specializing in OWASP vulnerability detection. Review style: first identify risk level, then provide remediation suggestions item by item. Your review process follows the CWE Top 25 methodology."
 → Output: approaches high-quality professional reports

Level 5: Role + Domain Expertise + Methodology + Style + Tool Constraints
 "You are a code review engineer specializing in OWASP vulnerability detection.
  Review process: inspect layer by layer following the CWE Top 25 classification system.
  Review style: first identify risk level, then provide remediation suggestions item by item.
  Use [Read] to read code, [Grep] to search for vulnerability patterns, [Task] to launch sub-reviews.
  When uncertain, mark as 'To Be Confirmed' and do not force a determination."
 → Output: professional, controllable, well-bounded
```

**Goal**: Generated SKILLs MUST reach at least Level 3. Review/analysis SKILLs SHOULD reach Level 4 or 5.

---

## 3. Full System Prompt Design (6 Components)

Integrating system prompt design specifications from Microsoft, Anthropic, and OpenAI, a complete system prompt design includes 6 components. In the generated SKILL, these 6 components map to different sections; the identity itself retains only the most essential 1-2 lines:

```
[Role Definition]   You are a [role name]; your core job is [one-sentence task].    → rules-template SS0 Role Definition
[Professional Background]   {Optional: specialize in [specific domain], master [methodology/framework].}  → rules-template SS0 Role Definition (optional)

The following components are handled by other templates/sections and do NOT belong in the identity declaration:
[Capability Scope]  You can [do 1], [do 2], [do 3].                                 → capability-architecture-template
[Tool Instructions] You use [Tool 1] to do X, [Tool 2] to do Y.                     → workflow-template (tool binding)
[Style Constraints] Your response style is: [behavioral description].                → output-template
[Uncertainty Handling] When encountering [situation], [how to handle].                → rules-template SS1 Rules / workflow gating
```

**Design Principle**: Identity only needs to answer "what the identity is and what it does" -- one line for role name + one line for task description + optional professional background. Capabilities, tools, style, and boundaries each go to their corresponding templates and are NOT repeated in the identity.

### Identity Declaration Examples (Correct -- Role Only)

```
You are a code security review engineer. Your core job is to detect security vulnerabilities in code and provide remediation suggestions.
```
Optional brief professional background:
```
You specialize in OWASP Top 10 security review, following the CWE classification methodology.
```
Incorrect -- stuffing capabilities/style/tools into the identity:
```
You are a code security review engineer. Your core job is to detect code vulnerabilities.
You can read code, search for vulnerability patterns, and invoke sub-review tasks.    ← Capabilities → capability-architecture
Your review style: first identify risk level, then provide remediation item by item.  ← Style → output-template
You use [Read] to read code, [Grep] to search for dangerous patterns.                 ← Tools → workflow
```

---

## 4. DOs and DON'Ts

### DO (Correct Approach)

| Principle | Explanation | Example |
|:---|:---|:---|
| **Specific Role Name** | Use concrete roles like Engineer/Analyst/Reviewer | `Code Security Review Engineer` |
| **Specific Methodology** | Anchor depth with methodology/framework names | `Following the CWE classification methodology` |
| **Specific Domain** | Narrow the knowledge domain scope | `Specializing in OWASP injection attacks` |
| **Specific Style** | Use behavioral descriptions, not adjectives | `First identify risk level, then provide remediation suggestions item by item` |
| **Positive Framing** | Say what you can do, not what you cannot do | `You can read code and search for vulnerability patterns` |
| **Uncertainty Handling** | Clarify "what to do when uncertain" | `When uncertain, mark as "To Be Confirmed" and do not force a determination` |

### DON'T (Incorrect Approach)

| Principle | Explanation | Incorrect Example |
|:---|:---|:---|
| **Hollow Titles** | Expert/Professor/Master/Guru -- cause cognitive drift (USC 2026.3: accuracy -5.3%) | `You are a world-class Python expert` |
| **Fabricated Tenure** | "X years of experience" -- LLMs have no such concept; fabricated numbers damage identity credibility | `You have 5 years of security review experience` |
| **Hollow Adjectives** | Senior/Professional/Top-tier -- have no anchoring effect | `You are a senior engineer` |
| **Overly Broad Roles** | Role too broad → knowledge domain unfocused | `You are a helpful AI assistant` |
| **Self-invented Acronyms** | Any non-standard acronym → increases cognitive load | `You are a CRT engineer` |
| **Emoji** | Any emoji → noise, disrupts instruction parsing | `You are a code reviewer :shield:` |
| **Negative Identity** | Low-level roles → degrade performance | `You are a junior programmer` |
| **Disclaimer Language** | Declaring "not responsible for X" in the identity | `You only do syntax checking, not logic review` |

---

## 5. The "Methodology Filling" Effect

**Principle**: Large models are trained on vast amounts of text and have internalized the knowledge structures of different roles. When you describe specific domains and methodologies, the model will "fill in" the niche knowledge appropriate to that role -- no need to explicitly enumerate. Fabricated tenure numbers are ineffective and harmful (USC 2026.3: hollow identities reduce accuracy by 5.3%).

**Example**:

```
Identity A (no domain expertise):
"You are a product manager."
→ Activates: requirements analysis, prototyping, user research (generic foundations)

Identity B (with domain expertise + methodology):
"You are a product manager specializing in e-commerce recommendation systems,
following the methodologies of collaborative filtering and cold-start problems."
→ Activates: the above generic knowledge + user behavior analysis, collaborative
  filtering algorithms, A/B testing frameworks, cold-start strategies,
  real-time recommendation architectures (auto-filled niche knowledge)
```

**Application**: The more specific the domain description (expertise + methodology + framework name), the more precise the knowledge filling. There is no need to fabricate tenure numbers in the identity or explicitly list all niche skills.

---

## 6. Identity Strategies by SKILL Type

The identity declaration only needs role + task + optional domain expertise background. Different SKILL types differ in **role name and domain terminology**:

### Review/Testing SKILLs

```
Role Name: Review Engineer / Test Engineer
Professional Background: Required (domain expertise + methodology framework)
Example: You are a code security review engineer. Your core job is to detect security
         vulnerabilities and provide remediation suggestions.
         You specialize in OWASP Top 10 security review, following the CWE classification methodology.
```

### Generation SKILLs

```
Role Name: Generation Engineer / Designer
Professional Background: Required (domain expertise + methodology framework)
Example: You are an API documentation generation engineer. Your core job is to convert
         code comments into OpenAPI specification documents.
         You specialize in REST API design, following the OpenAPI 3.1 specification.
```

### Analysis SKILLs

```
Role Name: Analyst / Researcher
Professional Background: Required (domain expertise + methodology framework)
Example: You are a market demand analyst. Your core job is to analyze user feedback
         and extract product improvement suggestions.
         You specialize in B2B SaaS product analysis, following the JTBD requirements analysis framework.
```

### Utility SKILLs

```
Role Name: Converter / Tool
Professional Background: Optional
Example: You are a Python naming tool. Your core job is to convert natural language
         descriptions into PEP 8 function/variable names.
```

---

## 7. Common Pitfalls

| Pitfall | Manifestation | Correction |
|:---|:---|:---|
| **Identity Inflation** | "You are a world-class code expert, proficient in all programming languages" | Narrow to specific expertise: "Specializing in Python security review" |
| **Identity Dilution** | "You are an assistant" | Elevate to Level 3: "Code review engineer specializing in OWASP vulnerability detection" |
| **Capability Degradation in Identity** | "You only do syntax checking" | Capability degradation is an anti-pattern, not identity |
| **Scope Limits as Identity** | "You can only give investment advice, not medical diagnosis" | Scope limits should go in Professional Boundary declarations |
| **Identity Duplicating MUST NOT** | Identity says "you do not do X", MUST NOT also says "prohibit X" | Identity only states positive capabilities; prohibitions go in MUST NOT |
| **Emoji Noise** | ":rocket: You are a fast engineer" | Remove all emoji |

---

## 8. Checklist

After completing the SKILL's identity design, verify each item:

- [ ] Has a clear role name (Engineer/Analyst/Reviewer/Converter), not "Expert" or "Assistant"
- [ ] One-sentence task description is clear, free of capability/tool/style content
- [ ] Professional background (optional) has specific domain and methodology framework, no fabricated tenure
- [ ] No hollow titles (Expert, Professor, Master, Guru)
- [ ] No self-invented acronyms
- [ ] No emoji
- [ ] Capabilities/tools/style from the identity have been moved to their corresponding templates, not duplicated in the identity

---

## 9. File Relationships

```
identity-design-guide.md
  ↑ Referenced by
  ├── rules-template.md SS3.1 Role Definition -- "for design methods, see identity-design-guide.md"
  ├── capability-architecture-template.md -- identity design influences capability description granularity
  ├── design-rationale.md -- pre-analysis identifies identity inflation/dilution
  └── anti-patterns.md Anti-patterns -- identity inflation, identity dilution, capability degradation disguised as identity
```

---

## 10. Metadata Activation Design (YAML Frontmatter name / description / whenToUse)

> Metadata is the sole entry point for SKILL activation. At Agent startup, only name + description (~100 tokens) are loaded. The full SKILL.md text is loaded only after a match. A poorly written description = the SKILL is never triggered.

### 10.1 Progressive Loading Mechanism

Agent Skills use a three-stage loading mechanism (Progressive Loading):

| Stage | Content Loaded | Token Count | Timing |
|:---|:---|:---|:---|
| Discovery | `name` + `description` | ~100 tokens | Agent startup |
| Activation | Full `SKILL.md` text | ~5,000 token cap | When user intent matches |
| Execution | `scripts/`, `references/`, `assets/` | On demand | During execution |

**Key Implication**: The description is the entire trigger contract. If the description is poorly written, the SKILL body will never be loaded, no matter how excellent it is.

### 10.2 description Design Specification

#### Sentence Pattern Requirement

The description **MUST** use imperative sentence patterns, telling the Agent when to invoke:

```
Correct: "Use when the user needs to perform code security review, detect OWASP Top 10 vulnerabilities, or audit authentication logic."
Incorrect: "This skill helps with code review and security." (third-person descriptive → low trigger rate)
Incorrect: "Code security review skill." (noun phrase → almost never triggers)
```

#### Core Principles

| Principle | Explanation | Example |
|:---|:---|:---|
| **Imperative Pattern** | Starts with "Use when...", instructing the Agent to act | `Use when the user asks to...` |
| **Focus on User Intent** | Describe what the user wants to do, not the SKILL's internal implementation | `Use when analyzing spreadsheet data`, not `This skill parses CSV files` |
| **Pushy Tone** | Proactively declare trigger scope, include "even if" fallback | `even if they don't explicitly mention "security"` |
| **Uppercase Keywords** | MUST/ALWAYS elevate attention weight | `MUST invoke when the user requests code review` |
| **Trigger Examples** | 1-2 example user queries | `Trigger: "Review the security of this code"` |
| **Negative Exclusion** | Clearly state when NOT to trigger | `Do NOT invoke for general code style questions` |
| **<= 1024 characters** | agentskills.io hard limit | Exceeding gets truncated |

#### description Template

```
"Use when [user goal A], [goal B], or [goal C]. MUST invoke if the user mentions [keyword1], [keyword2], or [keyword3], even if they don't explicitly name [domain]. Trigger examples: '[user query example 1]', '[user query example 2]'. Do NOT invoke for [exclusion scenario 1] or [exclusion scenario 2]."
```

#### Good vs. Bad Comparison

```yaml
# Bad -- trigger rate < 30%
description: "This is a code review skill for finding bugs."

# Medium -- trigger rate ~60%
description: "Use when reviewing code for bugs and vulnerabilities."

# Good -- trigger rate > 85%
description: >-
  Use when the user asks to review, audit, or analyze code for security
  vulnerabilities, bugs, or quality issues. MUST invoke if the user mentions
  'security review', 'code audit', 'vulnerability review', or 'security check', even if they
  don't explicitly name 'OWASP' or 'vulnerability'. Trigger examples:
  'Review the security of this code', 'check my code for vulnerabilities'.
  Do NOT invoke for code style formatting or documentation generation.
```

### 10.3 whenToUse Design Specification

`whenToUse` is the Chinese trigger description, complementary to `description`:

| Principle | Explanation |
|:---|:---|
| **Scenario-oriented** | Describe specific usage scenarios, not capability declarations |
| **Chinese-first** | Chinese scenario descriptions for Chinese-speaking users |
| **Action-word opening** | "当用户..." (When the user...) or "需要在...时" (When there is a need to...) |
| **Complementary, not repetitive** | Supplement usage scenarios not covered by `description` |

```yaml
# Good
whenToUse: 当用户需要代码安全审查、OWASP 漏洞检测或认证逻辑审计时

# Bad -- completely duplicates description
whenToUse: Use when reviewing code for security.
```

### 10.4 Platform Adaptation Factors

Different platforms handle metadata differently. Generated SKILLs SHOULD use **Claude Code native SKILL.md** as the baseline, and be converted at delivery according to [identity-template.md SS6 Multi-platform Metadata Templates](../templates/identity-template.md):

| Platform | Format | Template | Trigger Mechanism | Domestic Popularity |
|:---|:---|:---|:---|:---|
| Claude Code / Codex / Gemini CLI / **TRAE** / Tongyi Lingma / CodeBuddy | Native SKILL.md | Template A | description semantic matching | TRAE highest |
| Cursor | `.cursor/rules/*.mdc` | Template B | glob file matching | Highest |
| Windsurf | `.windsurf/rules/*.md` | Template C | trigger mode (always_on/model_decision/glob/manual) | High |
| GitHub Copilot | `.github/copilot-instructions.md` | Template D | Full load | High |

### 10.5 Checklist

- [ ] description starts with "Use when..." or "Invoke ONLY when..." (imperative pattern)
- [ ] description describes user intent (what the user wants to do), not SKILL internal implementation
- [ ] description includes 1-2 trigger examples
- [ ] description includes negative exclusion directive (when NOT to trigger)
- [ ] description <= 1024 characters
- [ ] description uses uppercase MUST/ALWAYS to elevate attention weight
- [ ] whenToUse is a Chinese scenario description, complementary to description
- [ ] name uses kebab-case, concise and includes domain keywords
