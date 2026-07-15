# Pattern Ref Design Guide

> Only teaches how to write pattern ref files. Pattern refs answer "How to do it?" — correct/incorrect patterns + fix strategies + verification steps.
> To determine whether a pattern ref file is needed, see skill-package-design-guide.md §2.

---

## §1 Format Template

```markdown
> Loading Phase: Step 4

## {Problem Type}

**Incorrect Pattern**:
```code
{Incorrect code/configuration/operation}
```
- Problem: {Why it causes issues}
- Impact: {Scope/severity of impact}

**Correct Pattern**:
```code
{Correct code/configuration/operation}
```
- Principle: {Why it is correct}
- Notes: {Boundary conditions when applying}

**Verification**: {How to verify after fixing — specific to commands or check items}
```

---

## §2 Rules

- **MUST** include a side-by-side comparison of incorrect pattern + correct pattern — providing only the correct pattern is insufficient
- **MUST** include a quantitative description of impact (which dimension, to what degree); generic labels are prohibited
- **MUST** make verification steps concrete and executable (commands/check items), not "confirmed OK"
- **MUST NOT** mix in analysis or fix content (that is the concern of other ref types)
- **SHOULD** <= 150 lines. Each pattern is typically 15-25 lines, with 4-6 patterns being appropriate.

---

## §3 Anti-Pattern File (Three Bottom Lines Scope, NOT a Pattern Ref)

> Note: The anti-pattern file (anti-patterns.md) belongs to the **three bottom lines** (SKILL quality assurance), not to domain knowledge pattern refs. The two are in different categories.

The anti-pattern file specifically documents practices that are "seemingly correct but actually harmful," used for quality issue scanning during the validation phase.

### 3.1 Six Required Elements

| Element | Description | Why Mandatory |
|:---|:---|:---|
| **Name** | Concise, precise naming | Easy to reference and retrieve |
| **Manifestation** | How it appears, how to identify it | Enables self-diagnosis by the user |
| **Why It Occurs** | Good intentions (the "well-intentioned" part) | Anti-patterns are not errors; they are "good intentions gone wrong" |
| **Harm** | Why it is wrong (the "harmful" part) | Helps the user understand the consequences |
| **Detection Method** | How to identify it automatically/manually | Lowers inspection cost |
| **Avoidance Strategy** | Alternative approach + why it's correct | Saying "don't do X" is not enough; must say "do Y instead" |

### 3.2 File-Level Structure

The anti-pattern file has two layers:
1. **Common Anti-Pattern Reference** (fixed): Declares that common anti-patterns (placeholder residue, specification overreach, example contamination, etc.) are handled uniformly by UR-SKILL; repeated enumeration in generated SKILLs is prohibited
2. **Domain-Specific Anti-Patterns** (on demand): Lists only anti-patterns unique to that SKILL's domain

### 3.3 Single Anti-Pattern Format Template

```markdown
## {Number} {Name}

**Manifestation**: {How it appears, how to identify it}

**Why It Occurs**: {Good intentions — why a developer might choose this approach}

**Harm**: {Why it is wrong, specific consequences}

**Detection Method**: {How to identify it automatically or manually}

**Avoidance Strategy**: {Alternative approach} → {Why it is correct}
```

### 3.4 Detection Priority

Scan order (high priority → low priority):

| Priority | Anti-Pattern | Rationale |
|:---|:---|:---|
| Critical | Placeholder Residue | Deliverable is incomplete |
| High | Specification Overreach, Risk Boundary Abuse, Step Name Inconsistency, IDE Tool Binding, Blind Spot Buck-Passing, Capability Degradation | Directly affects safety/professionalism |
| Medium | Architecture Confusion, Facet Filler, Example Contamination, Check Deficiency | Directly affects quality depth |
| Low | Blind Spot Evasion | Affects continuous improvement |

### 3.5 ur-skill Self-Inspection Checklist

When ur-skill designs a SKILL, it must self-inspect the following anti-patterns:

| Anti-Pattern | Manifestation | Avoidance Strategy |
|:---|:---|:---|
| Specification Overreach | Placing specification definitions directly in the body | Remove specification tables, push down to references/ |
| Placeholder Residue | Presence of [xxx], TODO, FIXME, etc. in the body | Fill all completely, or remove and mark as blind spot |
| Example Contamination | Directly copying examples from references/ into the body | Examples reference references/ via declarative references |
| Architecture Confusion | Capability matrix direction follows workflow steps | Rename to professional domain names (e.g., "Static Analysis") |
| Check Deficiency | Insufficient number of review checks | Allocate per node type: critical nodes 6 dimensions, non-critical nodes 3 dimensions |
| Blind Spot Evasion | Blind spot identification only writes "limitations noted" | Enforce execution per the three-layer mechanism |

---

## §4 Checklist

- [ ] Each pattern includes incorrect pattern + correct pattern + verification
- [ ] Each anti-pattern includes six elements (Name, Manifestation, Why It Occurs, Harm, Detection, Avoidance)
- [ ] Anti-pattern has "Why It Occurs" (good intentions)
- [ ] Anti-pattern has "Avoidance Strategy" (alternative + why correct)
- [ ] Anti-patterns sorted by detection priority
- [ ] File < 200 lines; split if exceeded
- [ ] No placeholder residue (must not violate anti-patterns itself)
