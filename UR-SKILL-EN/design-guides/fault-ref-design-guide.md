# Verification Ref Design Guide

> Only teaches how to write verification ref files. Verification refs answer "Is it real?" — true/false positive patterns + boundary cases + verification methodology.
> To determine whether a verification ref file is needed, see skill-package-design-guide.md §2.

---

## §1 Format Template

```markdown
> Loading Phase: Step 3

## {Pattern Name}

**True Positive** (real issues):
- Characteristics: {Observable characteristics}
- Example: {Code/scenario snippet}

**False Positive** (not real issues):
- Patterns that are easily mistaken for problems but are normal
- Differentiation method: {Specific signal/metric that distinguishes}

**Boundary Case**: {Gray area requiring human judgment + default recommendation}
```

---

## §2 Rules

- **MUST** include both true positive and false positive — without either side, the Agent cannot calibrate
- **MUST** make the differentiation method specific to observable signals; "please judge manually" is prohibited
- **MUST** provide a default recommendation for boundary cases (leaning toward true or false)
- **MUST NOT** write fix methods (that is the Pattern Ref's concern)
- **SHOULD** <= 180 lines. Verification refs are typically the most content-rich. If exceeded, check whether fix strategies or methodological elaboration have been mixed in.

---

## §3 Troubleshooting File (Three Bottom Lines Scope, NOT a Verification Ref)

> Note: The troubleshooting file (troubleshooting.md) belongs to the **three bottom lines** (SKILL runtime quality assurance), not to domain knowledge verification refs. The two are in different categories.

The troubleshooting file documents recurring failure patterns encountered during SKILL execution and their fix methods.

### 3.1 Three Required Elements

| Element | Description | Why Mandatory |
|:---|:---|:---|
| **Symptom** | Specific observable manifestation by the user/LLM | Entry point for diagnosis |
| **Root Cause** | The underlying cause of the symptom | Fixing only the symptom without fixing the root cause → recurrence |
| **Fix Action** | Specific, executable operation steps | Knowing "why it's broken" without knowing "how to fix it" = no value |

### 3.2 Format Template

```markdown
### {Number} {Fault Name}

- **Symptom**: {Specific observable manifestation by the user/LLM, using concrete error messages and behavioral anomaly descriptions}
- **Root Cause**: {The underlying cause of the symptom, explaining "why this happens"}
- **Fix Action**:
  1. {Specific step 1}
  2. {Specific step 2}
  3. {Specific step 3}
```

### 3.3 Grouping by Domain

Faults are grouped by **fault domain** (corresponding to workflow steps or capability domains) to enable fast context-based lookups by the LLM.

```
## 1. Capability Matrix-Related Faults
## 2. Workflow-Related Faults
## 3. Content and Format-Related Faults
## 4. Quality and Safety-Related Faults
```

### 3.4 Numbering System

Each fault entry is assigned a **T{number}** identifier (T = Troubleshooting) for cross-file referencing.
Example:
```markdown
### T01 Capability matrix written as workflow steps
```

### 3.5 Relationship with Anti-Patterns

| Dimension | Anti-Pattern (anti-patterns.md) | Troubleshooting (troubleshooting.md) |
|:---|:---|:---|
| Phase | Design time (prevention) | Runtime (fix) |
| Trigger | Static scan at validation step | Anomaly matching during execution |
| Focus | "What is wrong to do" | "How to fix when broken" |
| Causal Direction | Practice → Harm | Symptom → Root Cause → Fix |

**Mapping**: An anti-pattern may correspond to zero or more fault entries. Not every anti-pattern needs a fault entry — only those anti-patterns that necessarily lead to observable symptoms require one.

---

## §4 Checklist

- [ ] Each verification pattern includes both true positive and false positive
- [ ] Differentiation method is specific to observable signals
- [ ] Boundary cases have default recommendations
- [ ] No fix methods mixed in (fixes belong to Pattern Ref)
- [ ] File <= 180 lines; split if exceeded
