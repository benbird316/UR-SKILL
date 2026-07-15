# Workflow Design Guide

> Core principle: The workflow consists of 4 master nodes, with sub-nodes selected on demand within each master node. Gate-type nodes use all 6 dimensions; execution-type nodes use 3 dimensions.
> Each step includes actions, checklist, and reference files; actions are bound to specific tools; checklists are based on review dimensions.
> For tool binding specifications, see [tool-invocation-design-guide.md](tool-invocation-design-guide.md)

---

## §1 Master Nodes (All SKILLs MUST Include, 4 in Total)

The workflow consists of 4 master cognitive stages, each of which can be decomposed into multiple sub-steps as needed.

| Master Node | Responsibility | Gate | Review Dimensions |
|:---|:---|:---:|:---|
| **Analyze** | Parse input, acquire knowledge, design solution | No | Execution - 3 dimensions |
| **Execute** | Call tools, generate content, collect artifacts | No | Execution - 3 dimensions |
| **Reflect** | Quality checks, adversarial validation, gate decisions | Yes: MUST pass before delivery | Gate - All 6 dimensions |
| **Deliver** | Generate/output final artifact | No | Execution - 3 dimensions |

> Master nodes cannot be omitted or merged. For SKILLs with few steps, the master nodes serve directly as workflow steps; for SKILLs with many steps, sub-steps are decomposed within each master node.

---

## §2 Sub-Nodes (Selected on Demand)

Sub-steps = specific operations within a master node, determined based on SKILL type and requirement characteristics.

### 2.1 Analyze Master Node

| Sub-Node | Condition Requiring This Node | Gate | Review Dimensions |
|:---|:---|:---:|:---:|
| Parse | Input requires structured extraction | No | Execution - 3 dimensions |
| Coordinate | Multi-Agent scenario requiring sub-SKILL orchestration | No | Execution - 3 dimensions |
| Research | External knowledge or industry standards needed | Yes | Gate - All 6 dimensions |
| Planning | Design plan or capability domain derivation needed | Yes | Gate - All 6 dimensions |

### 2.2 Execute Master Node

| Sub-Node | Condition Requiring This Node | Gate | Review Dimensions |
|:---|:---|:---:|:---:|
| Dispatch | Multi-Agent scenario, tasks need to be delegated to sub-Agent or sub-SKILL | No | Execution - 3 dimensions |
| Consolidate | Multi-Agent scenario, multiple outputs need merging | No | Execution - 3 dimensions |
| Execute | **Mandatory** (core production step) | No | Execution - 3 dimensions |

> **Dispatch invocation**: `[Task]` spawns a sub-Agent (independent worker that reads `agent/*.md` methodology files and executes the full workflow) — suitable for subtasks requiring independent investigation/writing/scripting; `[Skill]` invokes a sub-SKILL (loads contextual instructions, executes inline within the caller's environment) — suitable for scenarios requiring specialized capability enhancement. UR-SKILL's 3 sub-Agents (research-analyst, tech-documentation, script-engineer) are all invoked via `[Task]`.
>
> **Sub-Agent dispatching mechanisms across platforms** (from a SKILL design perspective):
>
> | Platform | Sub-Agent Primitive | Dispatching Approach | Built-in Sub-Agents | Degradation Path |
> |:---|:---|:---|:---|:---|
> | **Trae** | No explicit primitives; `todo_write` task decomposition | Multi-agent architecture (Coordinator → Main → Sub → Specialist); Agents can mutually invoke and delegate | Built-in Agent + Custom Agent (Rules/MCP) | Builder mode serial `todo_write` tracking |
> | **Cursor** | Auto-dispatch | Main Agent autonomously invokes built-in sub-agents (Explore/Bash/Browser); supports `.cursor/agents/*.md` custom agents, up to 4 concurrent | Explore, Bash, Browser | Main Agent calls tools directly |
> | **Claude Code** | `Agent` (formerly `Task`) | Explicit launch, supports concurrency; 5 built-in + `.claude/agents/*.md` custom | Explore, Plan, general-purpose, statusline-setup, claude-code-guide | Simple operations use `Read`/`Glob`/`Grep` directly |
> | **Windsurf** | No explicit sub-agent primitives | AI Flow paradigm (continuous tool calls + `update_plan` + memory system); Warning: Cascade EOL (2026-07-01), replaced by Devin Local | No traditional sub-agents; Devin Local intrinsic parallelism | Devin Local internal optimization |
> | **CodeBuddy** | Mode switching + Subagents | Three modes (Ask/Craft/Plan) + `.codebuddy/agents/` custom; agentic auto-delegation / manual mode switch | Plan Mode, Explore | Craft Mode direct execution |
> | **Codex CLI** | `MultiAgentV2` | Sandbox isolation + approval system + sub-agent prompts; `SubagentStart` Hook triggers | Review Agent (auto_review) | Sandbox isolation (read-only/workspace-write/danger-full-access) |
> | **Qoder** | Quest | Agent Mode (single agent) + Experts Mode (Lead Agent orchestrates multiple experts) | Researcher, Full-Stack Engineer, QA, Code Reviewer, UI Operator, Debug Engineer | Quest Action (v1.0 background agent) |
>
> **SKILL design does not need to concern itself with platform differences** — write `[Task]` / `[Skill]` generic primitives, and each platform maps them automatically. If confirmation of a specific platform's dispatching capability is needed, refer to the table above.

### 2.3 Reflect Master Node

| Sub-Node | Condition Requiring This Node | Gate | Review Dimensions |
|:---|:---|:---:|:---:|
| Validation | Output is checkable via automated scripts or manual rules | Yes | Gate - All 6 dimensions |
| Verification | Output has pass/fail or quality standards requiring adversarial testing | Yes | Gate - All 6 dimensions |

> **Common validation methods**: anti-pattern scan (against anti-patterns.md), placeholder residue check (`{...}` scan), structural compliance check (against templates), terminology consistency check, automated validation scripts (e.g., `validate_skill.py`). Scripts can be placed in either the validation step or the verification step — validation focuses on format and rule compliance, verification focuses on logical correctness and adversarial testing.
| Decision | **Mandatory** (gate decision: pass → deliver / fail → rollback) | Yes | Gate - All 6 dimensions |

### 2.4 Deliver Master Node

No sub-nodes. Delivery is a single action: generate/output the final artifact.

---

## §3 Step Structure Template

```markdown
#### {N}. {Step Name}【{Node Type}，{N} Dimensions】

**Actions**:
1. [{Tool Name}] {Operation Description} → Declare **{Radiating Domain}·{Level}**: {Deliverable}
2. [Cognitive Operation] {Cognitive Operation Description} → Activate **{Radiating Domain}·{Level}**: {Specific Output}
3. [{Tool Name} (↘ {Degradation Tool})] {Operation Description} → Declare **{Radiating Domain}·{Level}**: {Deliverable}

**Core Command**: Confirmed...

**Checklist**:
- [ ] Goal Alignment: ...
- [ ] Fact Anchoring: ...
- [ ] Direction Calibration: ... (applicable to gate-type nodes)
- [ ] Adversarial Validation: ... (applicable to gate-type nodes)
- [ ] Blind Spot Identification: ...
  - Blind Spot Handling: ({Actions attempted}) / ({Remaining blind spots}) / ({Feasibility recommendations})
- [ ] Impact Projection: ... (applicable to gate-type nodes)
- [ ] Risk Boundary Triggered: (Yes/No) → Yes → Terminate

→ Any unconfirmed → Complete → Confirm again → All confirmed → Proceed to {N+1}

**Reference Files**: {references/...}
```

> Gate-type nodes (steps involving decision or gate) use all 6 dimensions; execution-type nodes (execution steps) use 3 dimensions.

---

## §4 Action Format

| Action Type | Format | Example |
|:---|:---|:---|
| Tool Action | `[{Tool Name}] {Operation} → {Output}` | `[File Read] Read requirement input → Extract task type` |
| Cognitive Operation | `[Cognitive Operation] {Description} → Activate **{Domain}·{Level}**: {Output}` | `[Cognitive Operation] Extract prompt based on Schema design → Activate **B Entity Extraction·Advanced Level**: Output triples` |
| Degradation Operation | `[{Tool Name} (↘ {Degradation})] {Operation} → {Output}` | `[WebSearch (↘ WebFetch)] Search industry standards → Acquire domain knowledge` |

> For tool binding specifications, see [tool-invocation-design-guide.md](tool-invocation-design-guide.md).

---

## §5 Review Dimension Assignment Rules

| Node Type | Dimensions | Includes |
|:---|:---:|:---|
| Gate-Type Node | All 6 dimensions | Goal Alignment, Fact Anchoring, Direction Calibration, Adversarial Validation, Blind Spot Identification, Impact Projection |
| Execution-Type Node | 3 dimensions | Goal Alignment, Fact Anchoring, Blind Spot Identification |

> Sub-nodes involving decisions (Research/Planning) or gates (Validation/Verification/Decision) = Gate-type - All 6 dimensions; purely execution sub-nodes = Execution-type - 3 dimensions.

---

## §6 Blind Spot Three-Layer Mechanism

After blind spot identification, the following progressive mechanism must be executed:

| Layer | Action | Output |
|:---|:---|:---|
| Layer 1 | Investigate and analyze → self-optimize and fill | Optimization complete, return confirmation |
| Layer 2 | Still insufficient → request resources | Resources supplemented, continue optimization, return confirmation |
| Layer 3 | No resources available → output blind spot handling report | Actions attempted + remaining blind spots + feasibility recommendations, return confirmation |

> Skipping directly from Layer 1 to Layer 3 is prohibited.

---

## §7 Reference Examples

**Full example**: A Meta-SKILL that generates other SKILLs. Analyze includes Parse + Research + Planning + Coordinate; Execute includes Dispatch + Execute + Consolidate; Reflect includes Validation + Verification + Decision; Deliver outputs directly.

**Minimal example**: A conversation-guiding SKILL. Analyze = parse user intent, Execute = generate response, Reflect = Validation + Decision (content safety review), Deliver = output response. No sub-node decomposition.

---

## §8 Writing Conventions

| Element | Convention | Example |
|:---|:---|:---|
| Step Name | Verb-started, no more than 4 characters | Parse, Research, Planning, Execute, Validation, Verification, Decision |
| Action | Verb-started with deliverable; executable actions must bind a tool or be marked as Cognitive Operation, and declare domain-level | `[File Read] Read user requirements → Declare **Requirements Engineering·Foundation Level**: Requirement Summary` |
| Core Command | Imperative sentence, "Confirmed..." | Confirmed that the information is sufficient to support file dependency decisions |
| Reference Files | Plural form references/ | references/verification-patterns.md |

---

## §9 Completeness Checklist

- [ ] Each step includes three elements: Actions, Checklist, Reference Files
- [ ] Each step has only 1 Core Command
- [ ] All 4 master nodes are complete; sub-nodes are selected on demand (refer to §2 condition columns for item-by-item determination)
- [ ] Reflect master node is marked as Gate (Gate - All 6 dimensions)
- [ ] Review dimensions are assigned per node type (gate-type nodes: 6 dimensions; execution-type nodes: 3 dimensions)
- [ ] Executable actions are bound to at least one specific tool (format: `[Tool Name] Operation → Declare **{Domain}·{Level}**: Output`) or marked as `[Cognitive Operation] → Activate **{Domain}·{Level}**: Output`
- [ ] Key tool invocations have degradation paths annotated
- [ ] Blind spot identification must be followed by concrete actions (investigate and optimize / request resources / blind spot report + feasibility recommendations)
- [ ] Unconfirmed items execute completion actions; forcibly proceeding to the next step is prohibited
- [ ] Reference file paths use plural form (references/)
