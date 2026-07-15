# SKILL Package Design Guide

> Core Principle: SKILL.md is the "brain" (<500 lines); all details are offloaded to subdirectories.
> This guide determines which non-body files the target SKILL requires.

---

## §1 Directory Structure Standard

```
skill-name/
├── SKILL.md              ← Required. Main body file, <500 lines
├── references/           ← Optional. Reference documents, loaded on demand
├── scripts/              ← Optional. Executable scripts, executed on demand
└── assets/               ← Optional. Static resources, loaded on demand
```

**MUST** SKILL.md < 500 lines. If exceeded, content must be split into references/.
**MUST** Files under references/ remain at a single depth level; nested subdirectories are prohibited.
**MUST** File references use relative paths (`references/xxx.md`); absolute paths are prohibited.
**MUST NOT** Create human-readable files (README.md, CHANGELOG.md, INSTALLATION_GUIDE.md).

---

## §2 File Trigger Decision (Three Principles)

Decision order: Principle 1 → Principle 2 → Principle 3

### 2.1 Principle 1: User Intent-Driven (First Priority)

Does the user explicitly require a specific standard/style/methodology?

| User Intent Signal | File Needed | Storage Location | Example |
|:---|:---|:---|:---|
| "Follow XX standard/specification" | Classification ref | references/classification.md | "Follow PEP 8" → Python coding standard classification |
| "Avoid XX issue" | Pattern ref / Anti-patterns file | references/fix-patterns.md / references/anti-patterns.md | "Avoid colloquial language" → Anti-pattern: verbose speech |
| "Output must include XX grading" | Output spec ref | references/output-spec.md | "Issue grading" → Grading criteria |
| "Need executable script" | Script | scripts/*.py | "Automated validation" → validate.py |
| "Need output template" | Asset file | assets/* | "Output with brand template" → template.md |
| "Involves multi-domain terminology" | Glossary | references/glossary.md | "Finance + Law" → Glossary |
| "Give me example references" | Examples file | references/examples.md | "Reference excellent cases" → Examples |

**MUST** User intent signals are mandatory triggers. Once hit, the corresponding file must be created regardless of SKILL size.

### 2.2 Principle 2: Body Capacity Test (Second Priority)

| Capacity Status | Action |
|:---|:---|
| Body < 500 lines, content complete | No split needed, keep single file |
| Body >= 500 lines, or content overflows | Must split: push specification tables, examples, detailed rules down to references/ |
| Body < 500 lines, but information density too low | Check for redundancy, delete formulaic filler |

**MUST** The body capacity test is a hard constraint, not an optional rule.

### 2.3 Principle 3: Domain Depth Correction (Third Priority)

After Principles 1 and 2, use domain depth to revise file types and quantity.

| Level | Judgment | Corrective Action |
|:---|:---|:---|
| General Domain | Widely present in LLM training data | No additional ref needed |
| General Domain + Depth | User requires specific standard/style | Covered by Principle 1 |
| Professional Domain | LLM may know but not precisely | Add classification ref (term definitions, classification systems) |
| Professional Domain + Refinement | Operational methods needed | Add detection methods + verification refs |
| Deep Professional Domain | Rapidly evolving knowledge / internal standards | Add all types |

> **Knowledge File Split Granularity**: One radiating domain → at most one knowledge file. If a radiating domain's knowledge content is small (< 50 lines), merging with adjacent domains is allowed; if it exceeds 200 lines (ref-types-design-guide.md §4 hard constraint), split by sub-topic within the domain with numbering (e.g., `classification-domain1.md`).

---

### 2.4 Ref File Type Reference (Heuristic Starting Point, Not Mandatory)

The following are default recommendations by SKILL type. **Final decisions are based on the research-analyst's domain investigation results and the user's explicit requirements** — if the domain investigation finds no anti-patterns are needed, or the user explicitly says "no glossary," this table is overridden.

| Ref File Type | Functional | Creative | Social | Trigger Condition |
|:---|:---:|:---:|:---:|:---|
| Classification ref | Recommended | Optional | — | Only when the domain has a professional classification system |
| Detection methods ref | Recommended | — | — | Only when the domain has right/wrong criteria or detection methods |
| Verification ref | Recommended | — | — | Only when the domain has known fault patterns |
| Pattern ref | Recommended | Optional | — | Only when the domain has "good intentions, bad outcomes" anti-patterns |
| Output spec ref | Recommended | Recommended | Optional | Needed for almost all SKILLs, varying only in detail |
| Glossary | Recommended | Optional | — | Only when the domain has 10+ terms requiring precise definition |
| Examples | Recommended | Recommended | Recommended | All three types need them, varying only in quantity and nature |
| Scripts | Optional | — | — | Only when automated detection/validation is needed |
| Asset files | Optional | Optional | — | Only when output templates / brand assets are needed |

> Override rule: The domain investigation in research-analyst Step 2 (best practices + common incorrect practices) can override any default recommendation in this table. This table only provides a starting point for "what is typically needed," not a final decision.

### 2.5 Decision Quick Reference: From Criteria to Files

The following analyzes **why each is needed** by asset type, and provides a single testable criterion. The research-analyst uses this table directly in the file dependency analysis phase.

#### Three Bottom Lines (Threshold Files)

Any non-single-file SKILL (content cannot be fully inlined into body) must create:

| File | Why Needed | Criterion |
|:---|:---|:---|
| **references/examples.md** | Users need to see concrete input -> output mappings, otherwise they cannot understand the SKILL's behavior boundaries | Always needed (only purely tool-type single-file SKILLs may omit examples) |
| **references/anti-patterns.md** | Without anti-patterns, the model will systematically repeat the same type of errors — "how to write" needs "how NOT to write" as a counterpoint | Always needed (collect >=3 common error patterns from domain investigation) |
| **references/troubleshooting.md** | Edge cases inevitably arise at runtime; without a fault recovery guide, every error starts from scratch | Always needed (collect >=3 typical fault scenarios from domain investigation) |

> Three Bottom Lines Exceptions:
> 1. Single-file SKILLs (all logic < 500 lines, no external knowledge dependencies, no self-created terminology) may condense the three bottom lines into a `## Notes` subsection within the body, without requiring separate files.
> 2. When the user explicitly states that no reference files are needed, they may be omitted.
> 3. When the user only requests a **system prompt** (not a complete SKILL package), the three bottom lines files may be omitted.

#### On-Demand Files

| File | Why Needed | Criterion (Single Question) | Typical Trigger Scenarios |
|:---|:---|:---|:---|
| **knowledge-reference (5 types)** | LLM training data has a knowledge cutoff and may be imprecise — external standards, platform specifications, API interfaces, and academic theories need reliable citation sources | **Can LLM training data stably cover this domain's knowledge?**<br>No -> Needed<br>Divided by purpose into: classification/detection-methods/verification/pattern/specification | OWASP/CWE (security, classification), PEP 8 (Python, classification), Xiaohongshu formatting specs (platform, classification), React API signatures (interface, detection-methods) |
| **glossary** | The same term has different meanings across domains (e.g., "model" in AI/architecture/finance); without precise definitions, ambiguity accumulates across downstream steps | **Does it introduce >=5 self-created terms, or span >=2 professional domains?**<br>Yes -> Needed | Methodology terms (KSAO, Three-Question Filter), platform-specific concepts (grassroots/content), cross-domain scenarios (finance + law) |
| **scripts/** | Manual validation cannot scale — code formatting, output structure, and compliance checks need repeatable programmatic verification | **Is programmatic validation/detection/generation needed?**<br>Yes -> Needed | Security audit (validate_findings.py), code generation (check_syntax.py), output format validation |
| **assets/** | Users need reusable output templates or brand assets, not hand-written from scratch each time | **Are static templates/configurations/assets needed?**<br>Yes -> Needed | Report templates (report_template.md), brand assets, configuration file templates |
| **output-spec** | Output without structural specifications leads to format drift — concepts like "issue grading table" and "severity" vary each time, downstream tools cannot parse | **Does the output need grading/quantification/structuring?**<br>Yes -> Needed | Security review (issue grading P0-P3 + Mermaid diagram), code review (severity/type/fix suggestions), test reports |

#### Boundary Scenario Decision Guide

| Scenario | Criterion | Conclusion |
|:---|:---|:---|
| Xiaohongshu content creation | Platform formatting specs, category terminology, topic strategy -> LLM unstable coverage | **Needs knowledge-reference** (platform specs K1 + category terminology K4) |
| General creative writing | Rhetoric/narrative/structure are general knowledge, LLM training data is sufficient | **Does not need** knowledge-reference |
| WeChat Official Account formatting | Platform has specific formatting specs (font size/spacing/image rules) | **Needs** knowledge-reference K1 |
| Python basic coding | PEP 8 is a public standard and present in training data | Boundary — lightweight classification ref recommended, non-mandatory K-level reference |
| REST API design | API signatures/endpoints change with versions, unreliable | **Needs** knowledge-reference K2 |
| Personal diary writing | No platform binding, no standard constraints | Single-file SKILL, three bottom lines can be inlined as body subsections |

> Override rule: The domain investigation in research-analyst Step 2 (best practices + common incorrect practices) can override any default recommendation in this table. This table only provides a starting point for "what is typically needed," not a final decision.

---

## §3 File Type Quick Reference Table

| File Type | Storage Location | Trigger Condition (any one met) | Design Guide |
|:---|:---|:---|:---|
| Classification ref | references/classification.md | User requires specific standard/classification system | classification-ref-design-guide.md |
| Detection methods ref | references/detection-methods.md | Operational detection/tracing methods needed | detection-ref-design-guide.md |
| Verification ref | references/verification-patterns.md | Verification/calibration of true/false issues needed | fault-ref-design-guide.md |
| Pattern ref | references/fix-patterns.md | Positive/negative pattern comparison needed | pattern-ref-design-guide.md |
| Output spec ref | references/output-spec.md | Output needs grading/quantification standards | output-design-guide.md |
| Anti-patterns file | references/anti-patterns.md | Common error pattern identification needed | pattern-ref-design-guide.md §Anti-patterns |
| Troubleshooting file | references/troubleshooting.md | Runtime fault repair needed | fault-ref-design-guide.md §Troubleshooting |
| Glossary | references/glossary.md | >=5 self-created terms, or multi-domain intersection | glossary-design-guide.md |
| Examples file | references/examples.md | User requests examples, or task pattern is complex | examples-design-guide.md |
| Scripts | scripts/*.py | Automated detection/validation/generation needed | scripts-design-guide.md |
| Asset files | assets/* | Output templates/configuration files/brand assets needed | assets-design-guide.md |

---

## §4 Decision Checklist

```markdown
## File Dependency Decision Checklist

### Principle 1: User Intent Signal
- [ ] Does the user require a specific standard/specification? -> Needs classification ref
- [ ] Does the user require avoiding specific issues? -> Needs pattern ref / anti-patterns file
- [ ] Does the user require output grading/quantification? -> Needs output spec ref
- [ ] Does the user require executable scripts? -> Needs scripts/
- [ ] Does the user require output templates? -> Needs assets/
- [ ] Does the user involve multi-domain terminology? -> Needs glossary
- [ ] Does the user require example references? -> Needs examples file

### Principle 2: Body Capacity Test
- [ ] SKILL.md body estimated lines < 500?
- [ ] If >= 500, which content needs to be pushed down to references/?

### Principle 3: Domain Depth Correction
- [ ] Domain depth: General Domain / General+Depth / Professional / Professional+Refinement / Deep Professional
- [ ] Correction: Add/remove which file types?

### Final Decision
| File Type | Needed | Quantity | Design Guide |
|:---|:---:|:---:|:---|
| ... | ... | ... | ... |
```

---

## §5 Checklist

- [ ] Directory structure conforms to standard (SKILL.md + references/ + scripts/ + assets/)
- [ ] File references use relative paths, single depth level
- [ ] Decision follows the three-principle order (Intent -> Capacity -> Depth)
- [ ] User intent signals are mandatory trigger conditions, not dependent on three-tier complexity labels
- [ ] SKILL.md < 500 lines (hard constraint)


---

## §A Platform Adaptation Appendix (Loaded Only When User Specifies Target Platform)

> This appendix provides platform-specific frontmatter field differences, format preferences, tool mappings, and constraint data.
> Loaded only when the user explicitly requests "for XX platform" / "dedicated to XX" / "deploy to XX."
> When no platform is specified, use the agentskills.io standard format (§A.1).

---

### A.1 Frontmatter Field Compatibility Matrix

Different platforms/tools have varying levels of support for frontmatter fields. The following are empirical findings:

| Field | agentskills.io | Trae IDE | Claude Code | Codex CLI | Cursor | Notes |
|:---|:---:|:---:|:---:|:---:|:---:|:---|
| `name` | **Required** | **Required** | **Required** | **Required** | **Required** | Universal across all platforms |
| `description` | **Required** | **Required** | **Required** | **Required** | **Required** | Core field for trigger matching |
| `metadata` | Optional | Optional | Optional | Optional | Optional | Arbitrary key-value pairs, platform extension entry point |
| `updated` | Optional | Optional | Optional | Optional | Optional | (1) Version tracking; (2) Lets the LLM perceive data freshness and judge whether domain knowledge may be outdated. UR-SKILL convention: required, placed within `metadata` |

> **Key Conclusions**:
> - **Trigger matching relies on `description`** — all platforms use it to decide whether to load the SKILL
> - `updated` is not a standard field on any platform; it is a **UR-SKILL-specific quality metadata convention**
> - **Default strategy**: Follow agentskills.io standard; place all non-standard fields into `metadata`. This is the safest, most cross-platform-compatible approach.

---

### A.2 Model Format Quick Reference Table

| Platform | Optimal Format | Instruction Position | Structured Output | Few-shot Sensitivity | Context Window | Safe Cross-Model Format |
|:---|:---|:---|:---|:---|:---|:---|
| **Claude** | XML tags | After document (bottom-up) | XML template or tool use | High (3-5 examples) | 200K-500K | Markdown (usable but not optimal) |
| **GPT** | Markdown + separators | Beginning (recency bias at end) | JSON Schema | Medium | 128K-256K | Markdown (optimal) |
| **Gemini** | PTCF framework | Clear segmented separation | Mixed (JSON + flexible format) | High (officially recommended always) | 1M+ | Markdown + explicit tags |
| **Default** | Markdown | — | Markdown tables + code blocks | Medium | — | Markdown (safest fallback) |

**Recommended Structure Tags/Elements**:
- **Claude**: `<role>`, `<context>`, `<task>`, `<instructions>`, `<examples>`, `<output_format>`
- **GPT**: `###` or `"""` separators, `#`/`##`/`###` headings, `**bold**`, language-tagged triple backticks, JSON Schema
- **Gemini**: `role:`/`context:`/`instruction:`/`constraint:`, Few-shot examples

**Format Adaptation Scope**: Only adjusts structural syntax (section headings, separators, output format specifications); does not change the capability matrix, workflow logic, or rule system.

---

### A.3 IDE Tool Mapping Table

SKILL.md uses **generic categories**; the Agent automatically maps them to the current IDE's specific tool names at execution time.

| Generic Category | Trae | Cursor | Claude Code | Windsurf | CodeBuddy | Qoder | Codex CLI |
|:---|:---|:---|:---|:---|:---|:---|:---|
| `[文件读取]` | `view_files` | `read_file` | `Read` | `view_file` | `read_file` | `read_file` | `—` (via `shell`) |
| `[文件写入]` | `write_to_file` | `edit_file` | `Write` | `write_to_file` | `write_to_file` | `create_file` | `apply_patch` |
| `[文件编辑]` | `update_file` | `edit_file` | `Edit` | `replace_file_content` | `replace_in_file` | `search_replace` | `apply_patch` |
| `[文件名搜索]` | `—` (via regex+glob) | `glob_file_search` | `Glob` | `find_by_name` | `list_files` | `search_file` | `—` (via `shell`) |
| `[文本搜索]` | `search_by_regex` | `grep` | `Grep` | `grep_search` | `search_files` | `grep_code` | `—` (via `shell`) |
| `[语义搜索]` | `search_codebase` | `codebase_search` | `—` (via MCP) | `codebase_search` | `—` (via MCP) | `search_codebase` | `—` |
| `[目录浏览]` | `list_dir` | `list_dir` | `LS` | `list_dir` | `list_files` | `list_dir` | `—` (via `shell`) |
| `[联网搜索]` | `web_search` | `web_search` | `WebSearch` | `search_web` | `—` (via MCP) | `search_web` | `—` |
| `[联网抓取]` | `—` | `—` | `WebFetch` | `read_url_content` | `—` (via MCP) | `fetch_content` | `—` |
| `[命令执行]` | `run_command` | `run_terminal_cmd` | `Bash` | `run_command` | `execute_command` | `run_in_terminal` | `shell` |
| `[诊断信息]` | `—` | `read_lints` | `—` | `—` | `—` | `get_problems` | `—` |

> For definitions of generic categories, see [tool-invocation-design-guide.md §1](tool-invocation-design-guide.md). For definitions and invocation rules of semantically self-evident workflow primitives (`[Task]`/`[AskUserQuestion]`/`[Skill]`), see [tool-invocation-design-guide.md §1](tool-invocation-design-guide.md).
>
> Generated SKILLs use generic categories by default; if the target platform can be determined, replace with platform-specific tool names per this table. UR-SKILL's own files must always retain generic categories.

---

### A.4 Platform-Specific Constraints

| Platform | Model-Driven | Sub-Agent Support | Key Constraints |
|:---|:---|:---|:---|
| **Trae** | Multi-model | ✅ Multi-agent system (Coordinator -> Sub -> Specialist); `.trae/agents/` custom | Chinese-native optimization; SOLO/Builder dual modes; snake_case tool naming |
| **Cursor** | GPT-4.1 + Multi-model | ✅ Explore / Bash / Browser + `.cursor/agents/*.md` (max 4 concurrent) | VS Code fork; chatml format; TypeScript namespace definitions |
| **Claude Code** | Claude Sonnet/Haiku | ✅ Agent tools (5 built-in) + `.claude/agents/*.md` custom | CLI-first; strict git safety protocol; PascalCase tool naming |
| **Windsurf** | SWE-1.5 (Devin Local) | ⚠️ Cascade EOL (2026-07-01), Devin Local native parallel | Product renamed to Devin Desktop; ACP protocol supports third-party agents |
| **CodeBuddy** | Tencent Cloud-driven | ✅ Subagents (agentic/manual) + `.codebuddy/agents/` | Three modes (Ask/Craft/Plan); Plan five-step lifecycle |
| **Qoder** | Tongyi LLM | ✅ Experts Mode (Lead + 7 experts) + Quest 2.0 | Formerly Tongyi Lingma; renamed to Qoder CN on 2026-05-20 |
| **Codex CLI** | OpenAI | ✅ MultiAgentV2 + Sandbox approval system | Core only 3 tools; most operations via `shell` indirectly |

---

### A.5 Sub-Agent Deployment Paths

UR-SKILL's 3 sub-agents ([research-analyst](../../agent/research-analyst.md), [tech-documentation](../../agent/tech-documentation.md), [script-engineer](../../agent/script-engineer.md)) are in generic Markdown format using generic tool categories. When deploying to each platform, copy the corresponding `agent/*.md` file to the platform's agent directory:

| Platform | Agent Directory | Deployment Notes |
|:---|:---|:---|
| **Trae** | `.trae/agents/` | Place the 3 `.md` files into `.trae/agents/` at the project root; agents can call each other through the multi-agent system |
| **Cursor** | `.cursor/agents/` | Place into `.cursor/agents/`; the main agent auto-discovers and invokes them, max 4 concurrent |
| **Claude Code** | `.claude/agents/` | Place into `.claude/agents/`; explicitly start via the `Agent` tool, supports concurrency |
| **CodeBuddy** | `.codebuddy/agents/` | Place into `.codebuddy/agents/`; supports agentic auto-delegation or manual switching |
| **Windsurf** | Devin Local native | No user-level agents directory; sub-agents are allocated internally by the engine, no manual deployment needed |
| **Qoder** | Experts Mode built-in | Expert roles are built-in, no external agent files needed; if custom sub-agents are needed, configure via Quest |
| **Codex CLI** | Hook definitions | Triggered via `SubagentStart` Hook events; no static agents directory |

> **Principle**: `agent/` contains generic source code (retaining generic tool categories); when deploying to a platform, copy directly without modifying tool names — the platform automatically maps generic categories to specific tools. Platforms without agents directories (Windsurf/Qoder/Codex CLI) cover sub-agent needs through their respective built-in mechanisms.

---

### A.6 Format Migration Checklist

When adapting a default Markdown SKILL to a specific platform, verify:

- [ ] Identity preserved: role definition and core task unchanged
- [ ] Capability matrix preserved: all domains and layers complete
- [ ] Workflow steps preserved: numbering and logic unchanged
- [ ] RFC 2119 keywords preserved: MUST/SHOULD/MAY intact
- [ ] Checklists preserved: all `- [ ]` items retained
- [ ] Blind spot mechanism preserved: three-layer process intact
- [ ] Only structural syntax adjusted: section headings, separators, output format specifications
- [ ] No content loss: no rules omitted during reformatting
