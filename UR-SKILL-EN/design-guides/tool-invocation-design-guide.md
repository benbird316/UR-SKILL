# Tool Invocation Design Guide

> Only teaches how to map abstract "actions" to specific tool invocations. Actions are "what to do"; tools are "what to use."
> For determining tool binding needs, see skill-package-design-guide.md §2.

---

## §1 Cross-IDE Generic Tool Categories

Generated SKILL.md uses "generic categories" by default. If the target platform can be determined, replace with platform-specific tool names according to the mapping table in [skill-package-design-guide.md §A.2](skill-package-design-guide.md). UR-SKILL's own files (SKILL.md, agent/*.md) **MUST** always retain generic categories (cross-platform source code).

| Generic Category | Function | Input Requirements |
|:---|:---|:---|
| `[文件读取]` | Read content from a known file path | Absolute path |
| `[文件写入]` | Create or overwrite a file | Path + Content |
| `[文件编辑]` | Precisely replace file content | Path + old_str + new_str |
| `[文件名搜索]` | Search for files by glob pattern | Glob pattern |
| `[文本搜索]` | Search file content by regex | Regex + Path |
| `[语义搜索]` | Search code by intent/concept | Natural language question |
| `[目录浏览]` | List directory structure | Absolute path |
| `[联网搜索]` | Search the web for real-time information | Search keywords |
| `[联网抓取]` | Fetch content from a specified URL | URL |
| `[命令执行]` | Run shell commands | Command string |
| `[诊断信息]` | Get IDE diagnostics/lint results | File URI (optional) |

**Semantically Self-Evident Workflow Primitives** (no conversion needed):

| Primitive | Function |
|:---|:---|
| `[Task]` | Delegate a complex sub-task to a sub-agent for independent execution |
| `[AskUserQuestion]` | Interrupt execution to ask the user a question |
| `[Skill]` | Invoke another specialized SKILL |

Semantically self-evident, no conversion needed. When generating a SKILL, if the target platform is known and has a corresponding sub-agent/sub-SKILL mechanism, the platform's native invocation method may be used; otherwise, keep the primitive format.

---

## §2 Selection Decision Matrix

| User Requirement | Recommended Category | Secondary Category | Not Recommended |
|:---|:---|:---|:---|
| Search for implementation of a class | `[语义搜索]` | `[文本搜索]` | `[文件名搜索]` |
| Find all `.ts` files | `[文件名搜索]` | `[目录浏览]` | `[文本搜索]` |
| Read a known file | `[文件读取]` | — | `[文本搜索]` / `[命令执行] cat` |
| Search for string "todo" | `[文本搜索]` | — | `[语义搜索]` |
| Understand codebase architecture | `[语义搜索]` | `[文件名搜索]` + `[文件读取]` | `[文本搜索]` |
| Get latest external information | `[联网搜索]` | `[联网抓取]` | — |
| Run tests/build/lint | `[命令执行]` | — | — |
| Get git diff | `[命令执行]` (`git diff`) | — | — |
| Modify code | `[文件编辑]` | `[文件写入]` | — |
| List project structure | `[目录浏览]` | `[文件名搜索]` | `[命令执行] ls` |

---

## §3 Action-Tool Mapping Specification

### 3.1 Standard Mapping Format

```
Actions:
1. [文件读取] Read user requirement description -> Extract task type and target system
2. [命令执行] git diff origin/HEAD... -> Get code change list
3. [文件名搜索] **/*.py Enumerate changed files -> Determine review scope
4. [语义搜索] "where is input validation located?" -> Locate existing validators
```

**Incorrect Example** (only abstract description):
```
Actions:
1. Read user requirements, extract task type
2. Get code change list
3. Determine review scope
4. Locate existing validators
```

### 3.2 Parameterization Specification

| Action Description | Tool Category | Example Parameters |
|:---|:---|:---|
| Get current branch changes | `[命令执行]` | `git diff --name-only origin/HEAD...` |
| Search for injection vulnerability patterns | `[文本搜索]` | `pattern:"execute\(|eval\(|exec\(" glob:"*.py"` |
| Web research on industry standards | `[联网搜索]` | `query:"OWASP Top 10 2026"` |
| Understand module responsibility | `[语义搜索]` | `"What is the responsibility of AuthService?"` |

### 3.3 Combined Invocation Pattern

```
Actions:
1. Determine review scope:
   a. [命令执行] git diff --merge-base origin/HEAD -> Get diff
   b. [命令执行] git diff --name-only origin/HEAD... -> Enumerate changed files
   c. If a fails -> [命令执行] git diff HEAD~1 (degradation plan)
2. Review each changed file:
   a. [文件读取] Read file full content -> Identify change context
   b. [语义搜索] "what validators exist in this project?" -> Get project validation patterns
```

---

## §4 Degradation and Fault Tolerance Design

| Tool | Preferred | Degradation 1 | Degradation 2 | Last Resort |
|:---|:---|:---|:---|:---|
| Get diff | `git diff --merge-base origin/HEAD` | `git diff origin/HEAD...` | `git diff HEAD~1` | `AskUserQuestion` to request scope specification |
| Code search | `[语义搜索]` | `[文本搜索]` | `[文件名搜索]` + `[文件读取]` | Declare information boundary |
| Web research | `[联网搜索]` | `[联网抓取]` | Declare knowledge cutoff date | Request user supplementation |
| File reading | `[文件读取]` | — | — | Declare inaccessible |

**Non-degradable Baseline Operations** (failure MUST terminate current step):
- `[命令执行]` executing git operations to get diff
- `[文件读取]` reading code files

---

## §5 Tool Binding by Workflow Node Type

| Node Type | Core Tool Categories | Example |
|:---|:---|:---|
| **Parse Node** | `[文件读取]`, `AskUserQuestion` | `[文件读取] Read user requirement input -> Extract task type` |
| **Research Node** | `[联网搜索]`, `[语义搜索]`, `[文件名搜索]` | `[联网搜索] query="{keyword}" -> Get industry standard` |
| **Execution Node** | `[命令执行]`, `[文件读取]`, `[语义搜索]`, `[文本搜索]` | `[命令执行] git diff --merge-base origin/HEAD -> Get changes` |
| **Validation Node** | `[文本搜索]` (placeholder scan), `[文件读取]` (cross-validation) | `[文本搜索] pattern="\{.*\}" Scan output -> Check for placeholder residue` |
| **Delivery Node** | `[文件写入]`, `[文件编辑]` | `[文件写入] Generate final SKILL.md -> Path {output_path}` |

---

## §6 Declaration Strategy

The declaration strategy is derived by research-analyst based on the SKILL's actual tool invocation density; there is no fixed template:

- SKILLs with few tool invocations: Inline declaration (write `[Tool Category]` directly in actions)
- SKILLs with many tool invocations: Inline + Centralized (add tool reference table at the end)
- SKILLs with scripts/ + assets/: Centralized primarily, inline as supplement

---

## §7 Anti-Patterns

| ID | Anti-Pattern | Manifestation | Correction |
|:---:|:---|:---|:---|
| 1 | No tool binding | Actions only write "read code" without specifying `[文件读取]` or `[命令执行] cat` | Every action must start with `[Tool Category]` |
| 2 | Tool mismatch | Using `[联网搜索]` to search local code, using `[文本搜索]` for semantic understanding | Refer to §2 Selection Decision Matrix |
| 3 | No degradation path | Tool invocation has no fallback; single point of failure causes entire step to fail | Provide at least 1 degradation path for critical tool invocations |
| 4 | Mixing dedicated tools with Shell | Actions include both `[文件读取]` and `cat`, `grep` | Always use dedicated tool categories |
| 5 | Empty parameters | Writing `[联网搜索] query:"search relevant content"` without concrete keywords | Parameters must be specific |
| 6 | Binding specific tool names without platform identification | Writing `Read`, `RunCommand` in SKILL.md when the target platform is uncertain | Default to generic categories; replace with platform-specific names per mapping table when platform is confirmed (see skill-package §A.2) |

---

## §8 Checklist

- [ ] Each workflow step's action includes at least 1 tool category invocation
- [ ] Tool invocations use generic category format (e.g., `[文件读取]`), **not** specific IDE tool names
- [ ] Tool invocations conform to the Selection Decision Matrix (§2), no cross-category mixing
- [ ] Critical tool invocations have degradation paths
- [ ] No shell commands used as substitutes for dedicated tool categories
- [ ] Parameters are specific, not empty placeholders
- [ ] SKILLs with high tool invocation density include a centralized tool reference table
- [ ] Non-degradable baseline operations are marked (failure = terminate)
- [ ] When `AskUserQuestion` is used as the last resort, specific options are provided
