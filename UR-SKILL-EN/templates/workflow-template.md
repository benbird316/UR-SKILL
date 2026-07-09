# Workflow Template

> Purpose: Defines the standard fill-in format for SKILL workflow steps
> Core principle: Each step contains actions, a checklist, and reference files; actions bind to specific tools; checklist is based on review dimensions
> Design methodology: see [design-guides/tool-invocation-design-guide.md](../design-guides/tool-invocation-design-guide.md)
> Review dimension definitions: see [design-rationale/design-rationale.md section 4](../design-rationale/design-rationale.md)

---

## 1. Step Structure Template

```markdown
#### {N}. {Step Name}【{Checkpoint Type}, {N} dimensions】

**Actions**:
1. [{Tool Name}] {Operation description} -> Declare **{Radiating Domain} - {Tier}**: {Output artifact}
2. [Cognitive Op] {Cognitive operation description} -> Activate **{Radiating Domain} - {Tier}**: {Specific output}
3. [{Tool Name} (-> {Fallback Tool})] {Operation description} -> Declare **{Radiating Domain} - {Tier}**: {Output artifact}

**Core Command**: Confirm...

**Checklist**:
- [ ] Goal Alignment: ...
- [ ] Fact Anchoring: ...
- [ ] Direction Calibration: ... (applicable to critical checkpoints)
- [ ] Adversarial Validation: ... (applicable to critical checkpoints)
- [ ] Blind Spot Identification: ...
  - Blind Spot Handling: (Actions attempted) / (Remaining blind spots) / (Feasibility recommendations)
- [ ] Impact Projection: ... (applicable to critical checkpoints)
- [ ] Risk Boundary Triggered: (Yes/No) -> Yes -> Terminate

-> Any unconfirmed -> Remediate -> Return to confirm -> All confirmed -> Proceed to {N+1}

**Reference Files**: {references/...}
```

> Checkpoint types and review dimensions: Critical checkpoints (Research, Architect, Verify, Validate) use all 6 dimensions; Non-critical checkpoints (Parse, Execute, Deliver) use 3 dimensions (Goal Alignment, Fact Anchoring, Blind Spot Identification). See [design-rationale/design-rationale.md section 4](../design-rationale/design-rationale.md).

---

## 2. Action Format

| Action Type | Format | Example |
|:---|:---|:---|
| Tool operation | `[{Tool Name}] {Operation} -> {Output}` | `[Read] Read requirement input -> Extract task type` |
| Cognitive operation | `[Cognitive Op] {Description} -> Activate **{Domain} - {Tier}**: {Output}` | `[Cognitive Op] Extract Prompt based on Schema design -> Activate **B Entity Extraction - Advanced Tier**: Output triples` |
| Fallback operation | `[{Tool Name} (-> {Fallback})] {Operation} -> {Output}` | `[WebSearch (-> WebFetch)] Search industry standards -> Obtain domain knowledge` |

> Tool binding specification: see [design-guides/tool-invocation-design-guide.md](../design-guides/tool-invocation-design-guide.md).

---

## 3. Complexity and Step Count

| Complexity | Step Count |
|:---|:---:|
| Simple | 3-5 steps |
| Medium | 5-7 steps |
| Complex | 7+ steps |

> The difference between Simple and Medium is the step count, not the review dimensions.

---

## 4. Blind Spot Three-Tier Mechanism

After blind spot identification, the following mechanism MUST be applied progressively:

| Tier | Action | Output |
|:---|:---|:---|
| Tier 1 | Investigate and analyze -> Self-optimize and fill | Optimization complete, return to confirm |
| Tier 2 | Still insufficient -> Request resources | Continue optimizing after resource supplementation, return to confirm |
| Tier 3 | No resource supplementation -> Output blind spot handling report | Actions attempted + Remaining blind spots + Feasibility recommendations, return to confirm |

> Jumping directly from Tier 1 to Tier 3 is prohibited. See [design-rationale/design-rationale.md section 7](../design-rationale/design-rationale.md).

---

## 5. Fill-in Specification

| Element | Specification | Example |
|:---|:---|:---|
| Step name | Begins with a verb, no more than 8 characters | Parse, Research, Architect, Execute, Verify, Validate, Deliver |
| Action | Begins with a verb, has an output artifact; executable actions MUST bind to a tool or be labeled as a cognitive operation, and declare capability domain - tier | `[Read] Read user requirements -> Declare **Requirements Engineering - Foundation Tier**: Requirements summary` |
| Core command | Imperative sentence, "Confirm..." | Confirm that the information is sufficient to support complexity determination |
| Reference files | Plural form references/ | design-rationale/design-rationale.md |

---

## 6. Completeness Checklist

- [ ] Each step contains the three elements: actions, checklist, reference files
- [ ] Each step has only 1 core command
- [ ] Simple SKILL: 3-5 steps, Medium: 5-7 steps, Complex: 7+ steps
- [ ] Review dimensions are allocated by checkpoint type (critical checkpoints: 6 dimensions, non-critical: 3 dimensions)
- [ ] Executable actions are bound to at least one specific tool (format: `[Tool Name] Operation -> Declare **{Domain} - {Tier}**: Output`) or labeled as `[Cognitive Op] -> Activate **{Domain} - {Tier}**: Output`
- [ ] Critical tool invocations have fallback paths documented
- [ ] Blind spot identification is followed by concrete action (Investigate and optimize / Request resources / Blind spot report + Feasibility recommendations)
- [ ] When unconfirmed, execute remediation actions; forcibly proceeding to the next step is prohibited
- [ ] Reference file paths use plural form (references/)
