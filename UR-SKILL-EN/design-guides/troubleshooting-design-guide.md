# Troubleshooting File Design Guide

> Purpose: Defines the standard format, content requirements, and design methodology for troubleshooting reference files (troubleshooting.md)
> Core Principle: Every fault must pair "Symptom → Root Cause → Fix Action"; pure declarative hints are prohibited

---

## 1. Why Troubleshooting Files Are Needed

Troubleshooting files record recurring failure patterns encountered during execution. Unlike anti-patterns:
- **Anti-patterns** are about "what was done wrong at design time" -- preventive
- **Troubleshooting** is about "what to do when it breaks at runtime" -- corrective

Without recording troubleshooting:
- The same fault is encountered repeatedly, diagnosed from scratch each time, consuming tokens and time
- Fault resolution methods are inconsistent -- different LLM sessions may give different (or even conflicting) fix actions
- Team knowledge cannot be accumulated -- pitfalls that veteran members have experienced are encountered again by new SKILLs

Troubleshooting files are **operational reference files** (L3), loaded on demand. When the LLM encounters an exception during workflow execution, it loads the troubleshooting file to match symptoms → obtain fix actions.

---

## 2. Standard Format for Troubleshooting

### 2.1 Three Required Elements

| Element | Description | Why Required |
|:---|:---|:---|
| **Symptom** | Concrete observable manifestation for users/LLM | Entry point for diagnosis; imprecise symptom descriptions prevent the LLM from matching the correct fault entry |
| **Root Cause** | The underlying reason causing the symptom | Fixing only the symptom without the root cause → it will break again; only understood fixes are sustainable |
| **Fix Action** | Specific, executable operation steps | Knowing "why it broke" but not "how to fix" = no troubleshooting value |

> Why three elements: Symptom → Root Cause → Fix Action is the standard triad in the troubleshooting domain (ITIL, Google SRE, DNS Troubleshooting Playbook). Fewer than three breaks the diagnostic chain; more than three dilutes attention.

### 2.2 Format Template

```markdown
### {Number} {Fault Name}

- **Symptom**: {Concrete observable manifestation for user/LLM, using specific error messages and behavioral anomaly descriptions}
- **Root Cause**: {The underlying reason causing the symptom, explaining "why this happens"}
- **Fix Action**:
  1. {Specific step 1}
  2. {Specific step 2}
  3. {Specific step 3}
```

### 2.3 Grouping by Domain

Faults are grouped by **fault domain** (corresponding to workflow steps or capability domains), making it easy for the LLM to quickly locate by context.

```
## 1. Capability Matrix Related Faults
## 2. Workflow Related Faults
## 3. Content and Format Related Faults
## 4. Quality and Security Related Faults
```

> Why group by fault domain: When the LLM encounters an exception during a specific workflow step, it naturally knows to look in the "Workflow Related Faults" domain, rather than traversing all entries. Grouping by domain is better suited for "query on demand" usage than sorting by priority.

### 2.4 Numbering System

Each fault entry is assigned a **T{SequenceNumber}** number (T = Troubleshooting), enabling cross-file referencing.

```markdown
### T01 Capability Matrix Written as Workflow Steps
```

> Why numbering: Consistent with anti-pattern numbering (Anti-Pattern 1) and rule numbering (Rule 01), following the UR-SKILL numbering system. The SKILL.md body can directly reference the number without repeating fault content.

---

## 3. Content Requirements for Troubleshooting

### 3.1 Content That Must Be Present

- **Symptoms must be concrete and identifiable**: Don't write "output is wrong" but instead "radiating domain direction is 'parse requirements → retrieve materials → evaluate sources'".
- **Root cause must explain "why"**: Don't write "design error" but instead "mistook execution order for an independent capability domain".
- **Fix actions must be executable**: Don't write "optimize the design" but instead "execute ordering test; if logic breaks, return to research and re-derive".

### 3.2 Prohibited Content

- **Prohibit pure declarative hints**: Such as "this issue needs attention" -- no root cause, no fix action.
- **Prohibit fixes without root cause**: Such as only writing "restart to fix" -- without knowing why it broke, variant faults cannot be generalized next time.
- **Prohibit non-executable fixes**: Such as "improve the design" or "enhance quality" -- verbs too abstract for the LLM to translate into concrete operations.
- **Prohibit unnumbered entries**: Fault entries must be numbered, otherwise they cannot be referenced by the SKILL.md body.

### 3.3 Symptom Description Quality Standards

| Standard | Description | Counterexample → Correct Example |
|:---|:---|:---|
| **Observable** | LLM can autonomously identify during execution | "Capability matrix design is unreasonable" → "Radiating domain is 'parse requirements → retrieve materials → generate report'" |
| **Concrete** | Includes specific error forms, values, output samples | "Format is wrong" → "Body exceeds 500 lines" |
| **Distinguishable** | Can distinguish between different fault entries | Symptom descriptions of two fault entries should not make the LLM unable to determine which to match |

---

## 4. Generation Method (UR-SKILL Special Notes)

> This SKILL is a "SKILL that designs SKILLs" (UR-SKILL). It needs its own troubleshooting file; it also provides troubleshooting design capability for generated SKILLs.

### 4.1 Creating Troubleshooting for UR-SKILL Itself

UR-SKILL's fault sources:
- Common failure patterns when executing the UR-SKILL workflow (practical experience)
- Typical issues when generated SKILLs are intercepted by the verification step
- High-frequency violations detected by anti-patterns (mapping from anti-patterns to faults)

Collection methods:
1. **Map from anti-patterns**: Every anti-pattern can potentially trigger a fault. E.g., "Anti-Pattern 4 Architecture Confusion" → "T01 Capability Matrix Written as Workflow Steps"
2. **From verification failure records**: Issues most frequently intercepted in the verification step (Step 5)
3. **From user feedback**: Issues reported by users of generated SKILLs

### 4.2 Creating Troubleshooting for Generated SKILLs

When a generated SKILL includes `references/troubleshooting.md`:

1. **Reverse-derive from anti-patterns**: Every anti-pattern may manifest as a fault at runtime → create corresponding fault entries for high-risk anti-patterns
2. **Predict from workflow steps**: Every workflow step can fail → create at least 1 fault entry per step
3. **Supplement with web research**: Search for common failure patterns in that domain
4. **Control quantity**: 8-15 fault entries, grouped into 3-5 fault domains

### 4.3 Complexity and Troubleshooting (Troubleshooting is one of the 3 baselines; mandatory for medium+ complexity, see design-rationale.md §9)

| Complexity | Troubleshooting File | Rationale |
|:---|:---|:---|
| Simple | Not needed | Simple SKILLs have limited failure modes; can be inlined in body |
| Medium | Needed, 8-12 fault entries | Medium SKILLs have independent workflows; faults need independent recording |
| Complex | Needed, 12-15 fault entries | Complex SKILLs have many workflow steps and fault domains |

---

## 5. Relationship Between Troubleshooting and Anti-Patterns

Troubleshooting and anti-patterns are different reference file types, but have a mapping relationship:

| Dimension | Anti-Patterns (anti-patterns.md) | Troubleshooting (troubleshooting.md) |
|:---|:---|:---|
| Phase | Design time (preventive) | Runtime (corrective) |
| Trigger | Static scan in verification step | Exception matching during execution |
| Focus | "What is the wrong way to do it" | "How to fix it when broken" |
| Causal Direction | Practice → Harm | Symptom → Root Cause → Fix |

**Mapping relationship**: One anti-pattern may correspond to zero or more fault entries. Not every anti-pattern needs a fault entry -- only those that inevitably lead to observable symptoms need one.

| Anti-Pattern | Corresponding Fault Entry | Mapping Rationale |
|:---|:---|:---|
| Anti-Pattern 4 Architecture Confusion | T01 Capability Matrix Written as Workflow Steps | Architecture confusion leads to capability matrix design errors -- observable symptom |
| Anti-Pattern 2 Placeholder Residue | T(Placeholder scan failure) | Placeholder residue causes static scan errors -- observable symptom |
| Anti-Pattern 6 Blind Spot Evasion | T(Blind spot declaration invalid) | Blind spot evasion causes checklist failure -- observable symptom |

---

## 6. Completeness Checklist

When designing troubleshooting files, check item by item:

- [ ] Each fault entry has three elements (symptom, root cause, fix action)
- [ ] Symptoms are concrete and observable; LLM can autonomously identify
- [ ] Root cause explains "why", not merely describes "where it's wrong"
- [ ] Fix actions are executable, with specific step sequences
- [ ] Grouped by fault domain (3-5 domains)
- [ ] Fault entries have T{SequenceNumber} numbering
- [ ] Fault count matches complexity (medium 8-12, complex 12-15)
- [ ] No pure declarative hints (e.g., "needs optimization")
- [ ] No non-executable fixes (e.g., "improve the design")
- [ ] File < 200 lines; if exceeded, split
