# Model Format Adaptation Design Guide

> Purpose: Guides the adaptation of SKILL output format to the structural preferences of different LLM platforms (Claude, ChatGPT, Gemini, etc.). When the user specifies a target platform, adjust the SKILL's structural syntax accordingly; when unspecified, use the default Markdown format.

---

## 1. Why Format Adaptation Matters

Different LLMs were trained on different token patterns and respond differently to structural markers. The same prompt can perform 30-50% differently across models purely due to format mismatch — not content quality. A prompt scoring 92% on Claude can drop to 78% on GPT-4 if XML tags are used instead of Markdown fences.

**Root cause**: Each model provider made deliberate choices about training data structure conventions:
- **Anthropic** explicitly trained Claude on XML-tagged content as structural anchors
- **OpenAI** built training data with heavy Markdown and JSON schema densities
- **Google** optimized Gemini for multi-modal inputs with clear context separators

This is not about "correct" syntax — all modern LLMs understand all formats. It's about matching training data patterns so the model's learned associations fire correctly.

**Applicable scope**: This guide applies to Mode A (Generate from Scratch) and Mode B1 (External SKILL Optimization). For Mode B2 (Internal Optimization) and Mode C (Knowledge Extraction), format adaptation is typically unnecessary.

---

## 2. UR-SKILL's Default Format: Markdown

UR-SKILL uses **Markdown** as its default output format. This is the format used when:
- The user has not specified a target platform
- The target platform is unknown
- The generated SKILL is intended for cross-model portability

**Markdown was chosen as the default because**:
1. It is the safest cross-model fallback — all major models process Markdown competently
2. It has the broadest ecosystem support
3. It is human-readable and tool-parseable
4. UR-SKILL's own SKILL.md files are written in Markdown, ensuring format consistency

**Default Markdown conventions used by UR-SKILL**:
| Element | Convention | Rationale |
|:---|:---|:---|
| Section headings | `#`, `##`, `###` (ATX-style) | Universal across all Markdown renderers |
| Key constraints | `**MUST**`, `**SHOULD**`, `**MAY**` (RFC 2119) | Machine-parseable, semantically precise |
| Two-dimensional data | Markdown tables `\| col \| col \|` | Clear at a glance for comparisons |
| Sequential steps | `1. → 2. → 3.` numbered lists | Explicit order guarantees |
| Checklists | `- [ ]` / `- [x]` | Standard task list syntax |
| Code/structured data | Triple backticks with language tag | Required by all models for code blocks |
| Blockquotes | `>` prefix | Clear semantic separation |
| Module separators | `---` horizontal rules | YAML frontmatter + logical section breaks |
| No emoji | Not used as constraint markers | Avoids encoding risks and parsing ambiguity |

---

## 3. Model-Specific Format Profiles

### 3.1 Claude (Anthropic)

**Primary preference**: XML tag structure
**Secondary preference**: Clean text with explicit labeling
**Avoid**: Heavy Markdown formatting when XML would be clearer

**Key characteristics**:
- XML tags are a "superpower" — Anthropic's official documentation confirms Claude was specifically trained to interpret XML tags as structural metadata
- Internal testing shows 20-40% consistency improvement with XML-structured prompts vs. prose equivalents
- Document placement matters: put reference material at the **top**, instructions and questions **below** — this improves response quality by up to 30%
- Literal instruction-following: "does exactly what you ask, nothing more, nothing less"
- Anti-examples are powerful ("Do not include disclaimers. Do not hedge your conclusions.")
- 3-5 few-shot examples dramatically improve consistency

**Recommended structural tags**:

| Tag | Purpose | Priority |
|:---|:---|:---|
| `<role>` | Claude's persona/identity | Required |
| `<context>` | Background, audience, constraints | Recommended |
| `<task>` | What to do, in actionable language | Required |
| `<instructions>` | Step-by-step guidance | Recommended |
| `<examples>` | Few-shot output samples | Recommended |
| `<documents>` / `<document>` | Reference material with `<source>` metadata | Recommended |
| `<output_format>` | Expected output shape | Recommended |
| `<thinking>` | Internal reasoning (only when extended thinking is OFF) | Situational |

**Claude-specific SKILL structure template**:

```xml
<role>
[identity declaration: role + core task]
</role>

<context>
[background information, audience, constraints]
</context>

<task>
[core instruction]
</task>

<instructions>
1. [step 1]
2. [step 2]
3. [step 3]
</instructions>

<examples>
<example>
[positive example of desired output]
</example>
</examples>

<output_format>
[structure, length, style specification]
</output_format>
```

**Important**:
- Nest tags hierarchically to establish precedence (e.g., `<critical_rules>` inside `<system>`)
- Do NOT use `<thinking>` tags when extended thinking API is enabled — they conflict
- Place `system` parameter (role, stable directives) via the API's `system` field, not inline XML
- Use tool use for structured output rather than XML coercion when possible
- If user input is spliced into XML, sanitize — users can inject closing tags like `</instructions>`

### 3.2 ChatGPT / GPT (OpenAI)

**Primary preference**: Markdown with explicit delimiters
**Secondary preference**: JSON schemas for structured output
**Avoid**: XML-only prompts without Markdown wrappers

**Key characteristics**:
- Put instructions at the **beginning** of the prompt, use `###` or `"""` to separate instruction from context
- Sensitive to recency bias — content at the end of the prompt carries more weight
- GPT-5+ series default: API responses do NOT use Markdown by default; you must explicitly request Markdown formatting
- For long conversations, append Markdown formatting instructions every 3-5 messages to maintain adherence
- JSON schemas work best for structured output (function calling, structured outputs API)
- Natural language reasoning requests ("Think through this step by step") work better than XML thinking tags
- Use `reasoning_effort` parameter to control thinking depth (low/medium/high)
- Use `verbosity` parameter to control response length

**Recommended structural elements**:

| Element | Purpose | Priority |
|:---|:---|:---|
| `###` or `"""` delimiters | Separate instruction from context | Required |
| `#` / `##` / `###` headings | Section structure | Recommended |
| `**Bold**` | Key constraints and emphasis | Recommended |
| Triple backticks with language tag | Code blocks and structured data | Required |
| JSON schema | Output format specification | Recommended |
| Numbered lists | Sequential instructions | Recommended |
| Leading words (`import`, `SELECT`) | Nudge code generation pattern | Situational |

**GPT-specific SKILL structure template**:

```markdown
### Identity
You are a [role]. Your core job is [task].

### Context
[background information, constraints]

### Task
[core instruction]

### Instructions
1. [step 1]
2. [step 2]
3. [step 3]

### Output Format
Respond with JSON matching this schema:
{
  "field1": "type",
  "field2": "type"
}

### Examples
**Example 1**:
[positive example]

**Example 2**:
[positive example]
```

**Important**:
- Be specific about what to do, not just what not to do (OpenAI's official best practice #7)
- Reduce "fluffy" descriptions — "3 to 5 sentences" beats "fairly short, a few sentences"
- GPT-5.2 specifically: explicit `<output_verbosity_spec>` blocks help control verbosity
- Use `reasoning_effort` parameter for complex tasks rather than CoT prompting
- For agentic workflows, define plan tool with milestones (pending/in_progress/done)

### 3.3 Gemini (Google)

**Primary preference**: PTCF framework (Persona + Task + Context + Format)
**Secondary preference**: Numbered lists with clear section labels
**Avoid**: Deeply nested hierarchical structures without explicit labels

**Key characteristics**:
- Google's official guide recommends the 4-element framework: Persona, Task, Context, Format
- Numbered lists and explicit section labels work best for structural organization
- Massive context window (1M+ tokens for Gemini 3 models) — but position still matters
- Uses thinking levels built into the API (not prompt-based CoT)
- Strong on multi-modal inputs (images, audio, video alongside text)
- Label-style format markers: 【Purpose】, 【Information】, 【Format】
- Few-shot examples strongly recommended; zero-shot "may not perform well"

**Recommended structural elements**:

| Element | Purpose | Priority |
|:---|:---|:---|
| `Persona` / `role` | Role definition | Required |
| `Task` / `instruction` | What to do | Required |
| `Context` | Background and constraints | Recommended |
| `Format` / `constraint` | Output shape and limits | Required |
| Few-shot examples | Calibrate output quality | Recommended |
| Chain-of-Thought | Complex reasoning tasks | Situational |
| Search grounding | Time-sensitive real-world information | Situational |

**Gemini-specific SKILL structure template**:

```
role: [identity declaration]
context: [background, audience, constraints]
instruction: [core task description with specific deliverables]
constraint: [output format, length, tone, structural requirements]

Examples:
---
[positive example of desired output]
---
```

Alternative labeled structure (Japanese community practice, equally effective):

```
【Persona】
[identity declaration]

【Task】
[core instruction]

【Context】
[background and constraints]

【Format】
[output specification]
```

**Important**:
- For time-sensitive queries: explicitly instruct the model to use the current date
- Avoid over-fitting with too many few-shot examples
- Use system instructions for stable directives, user messages for dynamic content
- Chain-of-Thought prompting works well for reasoning but Gemini's built-in thinking levels may render it redundant
- Delimiters (`"""`, `---`) help separate context from instruction

---

## 4. Cross-Model Comparison Matrix

| Feature | Claude | GPT | Gemini |
|:---|:---|:---|:---|
| **Optimal format** | XML tags | Markdown + delimiters | PTCF 4-element framework |
| **Instruction placement** | After documents (bottom-up attention) | At the beginning (recency bias at end) | Clear section separation |
| **Structured output** | XML templates or tool use | JSON schema (function calling) | Mixed (JSON + flexible) |
| **Few-shot sensitivity** | High (3-5 examples strongly improve consistency) | Medium (examples help but don't dominate) | High (official recommendation: always use few-shot) |
| **Anti-examples** | Powerful ("Do NOT include X") | Use positive instructions instead | Works but positive framing preferred |
| **Reasoning method** | Extended thinking API or `<thinking>` tag | `reasoning_effort` parameter | Built-in thinking levels |
| **Context window** | 200K-500K tokens | 128K-256K tokens | 1M+ tokens |
| **Document priority** | Top of prompt (first gets most attention) | End of prompt (recency bias) | Section order matters but less extreme |
| **Safe cross-model format** | Markdown (works but suboptimal) | Markdown (optimal) | Markdown + explicit labels |
| **Token economy** | XML tags add ~20-50 tokens overhead | Markdown = most token-efficient | Labeled structure = moderate overhead |

---

## 5. UR-SKILL Adaptation Strategy

### 5.1 Default Principle

> **When the user does not specify a target platform, ALWAYS use the default Markdown format. Do not proactively change the format.**

UR-SKILL's default is Markdown. All SKILL.md files are generated in Markdown by default. Format adaptation is only triggered when the user explicitly requests targeting a specific platform.

### 5.2 Trigger Conditions

Format adaptation SHOULD be triggered in the following scenarios:

| Condition | Action |
|:---|:---|
| User says "for Claude" / "deploy on Claude" / "Claude专用" | Adapt to XML structure |
| User says "for ChatGPT" / "for GPT" / "GPT专用" | Adapt to Markdown + delimiters (already default, verify) |
| User says "for Gemini" / "Gemini专用" | Adapt to PTCF framework |
| User says "cross-platform" / "multiple models" / "通用" | Keep default Markdown (safest fallback) |
| User says nothing about platform | Keep default Markdown |

### 5.3 Adaptation Scope

Format adaptation affects the **structural syntax** of the generated SKILL only. It does NOT change:
- Capability matrix design
- Workflow step logic
- Rule systems (RFC 2119 keywords remain universal)
- Review dimensions
- Blind spot mechanisms
- Content completeness

What changes:
- Section heading style (Markdown `##` vs XML `<section>` vs PTCF labels)
- Delimiter choices (triple backticks vs XML tags vs `role:` labels)
- Output format specification (Markdown table vs JSON schema vs labeled format)
- Instruction placement (top vs bottom depending on model attention patterns)

### 5.4 When NOT to Adapt

Format adaptation SHOULD NOT be applied when:
- The generated SKILL is intended as a UR-SKILL internal sub-SKILL (always use Markdown, as UR-SKILL itself runs on Claude-like platforms that prefer XML but Markdown works well enough)
- The SKILL is a design reference or template (templates stay in Markdown for portability)
- The adaptation would require rewriting more than 30% of the content (diminishing returns, warn the user)

---

## 6. Integration with UR-SKILL Workflow

### 6.1 In Pre-Analysis (Step 1: sub-SKILL)

The `pre-analysis-engineer` SHOULD detect target platform from user input and flag it in the pre-analysis report. When no platform is specified, mark as "Default (Markdown)."

### 6.2 In Execution (Step 4: Module Assembly)

If a non-default platform has been flagged in the pre-analysis report, Step 4 (Execution) MUST additionally:
1. Read `./design-guides/model-format-adaptation-design-guide.md`
2. Select the corresponding format structure per section 3's profile
3. Apply the adaptation per section 5.3's scope limitations
4. Do NOT change capability matrix, workflow logic, or rule systems

### 6.3 In Verification (Step 5: Quality Check)

If format adaptation was applied, the Verification step SHOULD additionally check:
- The adapted format matches the target platform profile (per section 3)
- The adaptation did not alter content semantics
- All RFC 2119 keywords remain intact
- Checklist and review dimension structures are preserved

### 6.4 In Delivery (Step 7: Output Assembly)

If format adaptation was applied, the delivery report MUST include:
- Target platform declaration
- Format adaptation summary (what was changed)
- A note that the SKILL may perform suboptimally on non-target platforms

---

## 7. Format Migration Checklist

When adapting a Markdown-default SKILL to a specific platform, verify:

- [ ] **Identity** preserved: role definition and core task remain unchanged
- [ ] **Capability matrix** preserved: all domains and layers intact
- [ ] **Workflow steps** preserved: numbering and logic unchanged
- [ ] **RFC 2119 keywords** preserved: MUST/SHOULD/MAY declarations intact
- [ ] **Checklists** preserved: `- [ ]` items all present, review dimension structure intact
- [ ] **Blind spot mechanism** preserved: three-tier handling process intact
- [ ] **Structural syntax only**: section headings, delimiters, output format specs adjusted
- [ ] **No content loss**: no rule, check item, or declaration omitted during reformatting

---

## 8. References

- [Anthropic Prompting Best Practices](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering) (May 2026)
- [OpenAI GPT-5.2 Prompting Guide](https://cookbook.openai.com/examples/gpt-5/gpt-5-2_prompting_guide) (Dec 2025)
- [Google Gemini Prompt Design Strategies](https://ai.google.dev/gemini-api/docs/prompting-strategies) (2026)
- [Elnashar et al. "Prompt engineering for structured data" (2025)](https://doi.org/10.55092/aias2025009) — systematic cross-model comparison of 6 prompt styles
- [Claude XML FAQ (claudexml.com)](https://claudexml.com/faq/) — practical XML tag usage guide
- [Structural Conventions Across Models (scalingthoughts.com)](https://scalingthoughts.com/blog/structural-conventions-across-models/) — why Claude loves XML, GPT loves JSON

---

## 8. Subagent Support Across Platforms

### 8.1 Subagent Is Industry Standard, Not Platform-Specific

Subagents (also called sub-agents, child agents, or task agents) are **not a unique feature of any single platform** — they are the industry standard as of 2026. A subagent is an isolated AI worker with its own context window, tool restrictions, and system prompt, launched by a parent agent to handle a specific task and return only the result.

**Why subagents matter for SKILL delegation**:
- **Context isolation**: the subagent's work doesn't pollute the parent's context window
- **Role separation**: each subagent has its own identity, avoiding identity conflicts (two "I am" declarations competing in one context)
- **Parallel execution**: multiple subagents can run simultaneously
- **Independent verification**: a subagent with a fresh perspective provides unbiased review (no confirmation bias from parent's context)

### 8.2 Platform Subagent Capability Matrix

#### International

| Platform | Subagent Support | Mechanism | Context Isolation |
|:---|:---:|:---|:---:|
| **Claude Code** | ✅ Native | Built-in (Explore/Plan/general-purpose) + custom subagents via YAML frontmatter | ✅ Independent context window |
| **Cursor** | ✅ Native | Built-in (Explore/Bash/Browser) + foreground/background modes | ✅ Independent context window |
| **GitHub Copilot** | ✅ Copilot Agents | Copilot Workspace + Agent mode (2025) | ✅ Task isolation |
| **Windsurf** | ✅ Cascade | Agent mode with SWE-grep sub-agents | ✅ Independent context |
| **OpenAI Codex** | ✅ Native | Cloud sandbox subagents, async execution | ✅ Sandbox isolation |

#### China Domestic

| Platform | Subagent Support | Mechanism | Context Isolation |
|:---|:---:|:---|:---:|
| **Trae (ByteDance)** | ✅ SOLO agent | Builder mode + subagent Task tool | ✅ Independent context window |
| **Qoder CN (Alibaba)** | ✅ Native | Quest 2.0 subagent collaboration + Expert panel multi-agent | ✅ Independent context |
| **CodeBuddy (Tencent)** | ✅ Craft mode | Task decomposition + multi-agent collaboration | ✅ Task isolation |
| **Comate (Baidu)** | ✅ Multi-agent | Multi-agent collaborative programming | ✅ Agent isolation |
| **CodeGeeX (Zhipu)** | ⚠️ Limited | Code translation + instruction mode, no explicit subagent API | Partial |

### 8.3 UR-SKILL Subagent Strategy

#### Default (Cross-Platform Safe): `[Skill]` + Explicit Role Switch

UR-SKILL's Step 1 invokes `pre-analysis-engineer` via `[Skill]` and immediately performs a **role switch declaration** afterward:

```
> Role Switch: Pre-analysis phase complete. All subsequent steps use ONLY the UR-SKILL
> main SKILL identity and rules. The pre-analysis-engineer's role definition and rules
> no longer apply.
```

**Why `[Skill]` is the safe default**:
- `[Skill]` is a platform-neutral concept — all agents understand loading a skill file into context
- The explicit role switch declaration prevents identity conflicts and context pollution
- Works on every platform regardless of whether it supports native subagents

#### Upgrade Path: `[Task]` Subagent (Platform-Dependent)

If the user specifies a target platform with verified subagent support (Trae, Claude Code, Cursor, Qoder CN, etc.), the Pre-Analysis Engineer MAY be invoked as a subagent (`[Task]`) instead of `[Skill]`:

| Method | Pros | Cons | When to Use |
|:---|:---|:---|:---|
| `[Skill]` + Role Switch | Cross-platform safe, no syntax differences | Roles briefly coexist in context | Default (user didn't specify platform) |
| `[Task]` Subagent | True context isolation, independent verification | Platform-specific syntax, not portable | User explicitly targets a known subagent platform |

**The recommendation**: default to `[Skill]` + role switch for portability. The adaptation guide's Upgrade Path section records the subagent option as an optimization for users who commit to a specific platform.

### 8.4 Impact on SKILL Design

When the Execution step (Step 4) applies format adaptation for a target platform:

- If the platform supports subagents → include a note in the generated SKILL's workflow: "Platform X supports native subagents. Consider replacing sequential [Skill] calls with parallel [Task] subagent invocations where context isolation is beneficial."
- If the platform does NOT support subagents → the generated SKILL's workflow MUST use role-switch declarations after any embedded skill invocation

This ensures the generated SKILL takes maximum advantage of its target platform's capabilities without creating portability issues.
