# Workflow Template

> **Purpose**: Define the standard filling format for SKILL workflow steps
> **Core Principle**: The workflow consists of 4 master nodes; sub-nodes are selected on demand. Each step includes actions, a checklist, and reference files.
> **Design Methodology**: See [design-guides/workflow-design-guide.md](../design-guides/workflow-design-guide.md)

---

## 1. Workflow Skeleton

```markdown
## Workflow

### Analyze

{Select on demand: Parse, Coordinate, Research, Planning}

### Execute

{MUST include the "Execute" sub-node; select on demand: Dispatch, Consolidate}

### Reflect

{MUST include the "Decide" sub-node; select on demand: Verify, Validation}

### Deliver

{Direct action, no sub-nodes}
```

---

## 2. Sub-Step Template

Each sub-step (including Delivery) is filled in using the following format:

```markdown
#### {N}. {Step Name}【{Gate/Execute}, {N} dims】

**Actions**:
1. [{Tool Name}] {Operation description} -> Declare **{Radiating Domain}·{Layer}**: {Deliverable}

**Core Command**: Confirm {check item}

**Checklist**:
- [ ] Goal Alignment: {Whether the step's goal has been achieved}
- [ ] Fact Anchoring: {Whether the referenced information is real and traceable}
{Gate nodes append the following 4 items:}
- [ ] Direction Calibration: {Whether the plan aligns with the initial goal}
- [ ] Adversarial Validation: {Whether there are counterexamples or edge cases}
- [ ] Impact Projection: {The cascading impact of the current decision on subsequent steps}
- [ ] Blind Spot Identification: ...
  - Blind Spot Handling: (Actions attempted) / (Remaining blind spots) / (Feasibility recommendations)

-> Any unconfirmed -> Remediate -> Re-check -> All confirmed -> Proceed to Step {N+1}

**Reference Files**: {references/...}
```

---

## 3. Filling Guidelines

| Element | Guideline | Example |
|:---|:---|:---|
| Step name | Verb-first, no more than 4 characters in Chinese (or concise English) | Parse, Research, Planning, Execute, Verify, Validation, Decide |
| Actions | Verb-first, has a deliverable; executable actions bind a tool or annotate `[Cognitive Operation]`, declare domain·layer | `[Read] Read requirement input -> Declare **Requirements Engineering·Foundation Layer**: Requirement summary` |
| Core Command | Imperative, "Confirm..." | Confirm information is sufficient to support plan design |
| Checklist | Gate nodes fill all 6 items; execution nodes fill only Goal Alignment, Fact Anchoring, Blind Spot Identification (3 items) | -- |
| Reference Files | Plural form `references/` | references/verification-patterns.md |

---

## 4. Action Format

| Action Type | Format | Example |
|:---|:---|:---|
| Tool operation | `[{Tool Name}] {Operation} -> {Output}` | `[Read] Read requirement input -> Extract task type` |
| Cognitive operation | `[Cognitive Operation] {Description} -> Activate **{Domain}·{Layer}**: {Output}` | `[Cognitive Operation] Extract Prompt from Schema -> Activate **Entity Extraction·Expert Layer**: Triplets` |
| Degradation operation | `[{Tool Name} (↘ {Degradation})] {Operation} -> {Output}` | `[WebSearch (↘ WebFetch)] Search industry standards -> Obtain domain knowledge` |

---

## 5. Examples

### 5.1 Full-Featured Example (Meta-SKILL)

```markdown
## Workflow

### Analyze

#### 1. Parse (Requirement Analysis)【Execute, 3 dims】
**Actions**:
1. [Read] Read user input -> Declare **Requirements Engineering·Foundation Layer**: Task summary (type/domain/delivery form)
**Core Command**: Confirm task type and domain are clear
**Checklist**:
- [ ] Goal Alignment: Extracted task type, domain, delivery form
- [ ] Fact Anchoring: Input information is real and traceable
- [ ] Blind Spot Identification: No ambiguity, no supplementation needed
-> All confirmed -> Proceed to 2
**Reference Files**: --

#### 2. Coordinate (Task Decomposition)【Execute, 3 dims】
...

#### 3. Research (Domain Knowledge)【Gate, 6 dims】
...

#### 4. Planning (Plan Design)【Gate, 6 dims】
...

### Execute

#### 5. Dispatch (Delegate to Sub-Agent)【Execute, 3 dims】
...

#### 6. Execute (Core Output)【Execute, 3 dims】
...

#### 7. Consolidate (Artifact Merging)【Execute, 3 dims】
...

### Reflect

#### 8. Verify (Quality Check)【Gate, 6 dims】
...

#### 9. Validation (Adversarial Testing)【Gate, 6 dims】
...

#### 10. Decide (Gate Decision)【Gate, 6 dims】
**Actions**:
1. [Cognitive Operation] Check verification and validation results item by item -> Activate **Quality Engineering·Expert Layer**: Pass/Fail judgment
**Core Command**: Confirm all gate conditions are satisfied
**Checklist**:
- [ ] Goal Alignment: Output matches initial requirements
- [ ] Fact Anchoring: Sources referenced are traceable
- [ ] Direction Calibration: Plan has not deviated
- [ ] Adversarial Validation: Edge cases have been covered
- [ ] Blind Spot Identification: Blind spots and their handling outcomes declared
- [ ] Impact Projection: No residual risk after delivery
-> Pass -> Proceed to Deliver / Fail -> Return for Fixes
**Reference Files**: references/anti-patterns.md

### Deliver

#### 11. Deliver (Final Output)【Execute, 3 dims】
**Actions**:
1. [Write] Write final file per output template -> Declare **Output Engineering·Foundation Layer**: Artifact file
**Core Command**: Confirm output is complete and correctly formatted
**Checklist**:
- [ ] Goal Alignment: Output structure matches output specification
- [ ] Fact Anchoring: Content based on previously confirmed information
- [ ] Blind Spot Identification: No omissions
-> Delivery complete
**Reference Files**: references/output-spec.md
```

### 5.2 Simplified Example (Dialogue-Guided SKILL)

```markdown
## Workflow

### Analyze

#### 1. Parse Intent【Execute, 3 dims】
**Actions**:
1. [Cognitive Operation] Analyze user input -> Activate **Dialogue Engineering·Foundation Layer**: Intent classification
**Core Command**: Confirm user intent is clear
**Checklist**:
- [ ] Goal Alignment: Intent classification is correct
- [ ] Fact Anchoring: Based on actual input
- [ ] Blind Spot Identification: No ambiguity
-> All confirmed -> Proceed to 2
**Reference Files**: --

### Execute

#### 2. Generate Response【Execute, 3 dims】
**Actions**:
1. [Cognitive Operation] Generate response based on intent type -> Activate **Dialogue Engineering·Advanced Layer**: Response draft
**Core Command**: Confirm response matches intent
**Checklist**:
- [ ] Goal Alignment: Response matches intent
- [ ] Fact Anchoring: Content is substantiated
- [ ] Blind Spot Identification: No unsafe content
-> All confirmed -> Proceed to 3
**Reference Files**: --

### Reflect

#### 3. Decide (Safety Review)【Gate, 6 dims】
**Actions**:
1. [Cognitive Operation] Scan response content -> Activate **Safety Engineering·Foundation Layer**: Safety determination
**Core Command**: Confirm no unsafe content
**Checklist**:
- [ ] Goal Alignment: Intent is not distorted
- [ ] Fact Anchoring: References are accurate
- [ ] Direction Calibration: Response has not gone off course
- [ ] Adversarial Validation: Malicious input has been blocked
- [ ] Blind Spot Identification: No residual risks
- [ ] Impact Projection: Output has no safety concerns
-> Pass -> Deliver / Fail -> Return for regeneration
**Reference Files**: references/content-safety.md

### Deliver

#### 4. Output Response【Execute, 3 dims】
**Actions**:
1. [Cognitive Operation] Output final response -> Activate **Dialogue Engineering·Foundation Layer**: User-visible response
**Core Command**: Confirm output is complete
**Checklist**:
- [ ] Goal Alignment: Output is the final response
- [ ] Fact Anchoring: Content has been validated
- [ ] Blind Spot Identification: No omissions
-> Delivery complete
**Reference Files**: --
```

---

## 6. Completeness Checklist

- [ ] All 4 master nodes complete (Analyze, Execute, Reflect, Deliver)
- [ ] Execute master node contains the "Execute" sub-node (required)
- [ ] Reflect master node contains the "Decide" sub-node (required)
- [ ] Remaining sub-nodes selected on demand (check against [workflow-design-guide.md §2](../design-guides/workflow-design-guide.md#2-子节点按需选配) conditions item by item)
- [ ] Gate nodes (Research, Planning, Verify, Validation, Decide) have all 6 dimensions open
- [ ] Execution nodes (Parse, Coordinate, Dispatch, Execute, Consolidate, Deliver) have 3 dimensions
- [ ] Each step has Actions, Core Command, Checklist, Reference Files
- [ ] Each step has only 1 Core Command
- [ ] Executable actions are bound to a tool or annotated as Cognitive Operation
- [ ] Gate node blind spot items include three-layer handling actions
- [ ] Reference file paths use the plural form
