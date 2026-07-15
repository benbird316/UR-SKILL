# Boundary Design Guide

> Only teaches how to write the SKILL's Risk Boundaries and Professional Boundaries. Risk Boundaries are "don't do harmful things"; Professional Boundaries are "don't exceed professional scope"; neither is capability degradation.
> For determining boundary design needs, see skill-package-design-guide.md §2.

---

## §1 Definition of Three Concepts

### 1.1 Risk Boundary (Safety Red Line)

| Dimension | Content |
|:---|:---|
| **Essence** | "Don't do harmful things" — safety baseline |
| **Nature** | Safety-related; if triggered, terminate the task |
| **Quantity** | Determined by domain safety requirements, typically 3-5 items |
| **Judgment** | If triggered, the SKILL itself loses its raison d'etre |

**Positive Examples**:

| ID | Declaration | Rationale |
|:---|:---|:---|
| 01 | Do not generate executable malicious code (ransomware, mining scripts) | Triggered = SKILL is aiding wrongdoing |
| 02 | Do not discriminately label or process data based on race/gender/age | Triggered = SKILL is actively creating discrimination |
| 03 | Do not output illegal content or information that violates privacy | Triggered = SKILL is breaking the law |

**Counterexamples (Disguised Capability Degradation)**:

| Abusive Wording | Problem |
|:---|:---|
| Only responsible for security review, does not check code errors | Capability degradation — code errors found during security review should also be reported |
| Only does code style checking, does not analyze functional correctness | Capability degradation — functional errors are a natural extension of style checking |
| Performance issues are not within the review scope | Capability degradation — declaring "won't do X" when X is a natural part of the task |

### 1.2 Professional Boundary (Scope Protection)

| Dimension | Content |
|:---|:---|
| **Essence** | "Don't exceed professional scope" — do not overstep to replace professional roles |
| **Nature** | Scope-related; if triggered, terminate the overstepping behavior and clearly inform the user |
| **Quantity** | Determined by domain scope, typically 1-3 items |
| **Judgment** | Prevents the SKILL from overstepping into areas requiring professional qualifications |

**Positive Examples**:

| ID | Declaration | Applicable Domain | Rationale |
|:---|:---|:---|:---|
| 01 | Only provides condition analysis reference, cannot replace a doctor's prescription or diagnosis | Medical | AI does not have the authority to exercise a medical practitioner's prescription rights |
| 02 | Output is a risk assessment reference, does not include specific buy/sell timing or price points | Financial | AI does not have the authority to give trading-level investment instructions |
| 03 | Only provides legal knowledge explanations, does not constitute formal legal advice | Legal | AI does not have the authority to issue legally binding opinions |

### 1.3 Capability Degradation (Anti-pattern)

| Dimension | Content |
|:---|:---|
| **Essence** | "Do X but choose not to report Y" — Y is a natural extension of X, but the SKILL actively refuses |
| **Nature** | Shifting responsibility, not a boundary |
| **Judgment** | The SKILL has the capability but actively refuses; this is shirking responsibility |

**Typical Patterns**:
- "Only do X, not Y" — but Y is a natural extension of X
- "X is not within the review scope" — but X is a reasonable expectation of the current capability
- "Not responsible for X" — but X is a reasonable part of the current task

---

## §2 Three-Concept Quick Reference Table

| | Risk Boundary (Safety Red Line) | Professional Boundary (Scope Protection) | Capability Degradation (Anti-pattern) |
|:---|:---|:---|:---|
| **Essence** | Don't do harmful things | Don't exceed professional scope | Do X but choose not to report Y |
| **Nature** | Safety-related, terminate if triggered | Scope-related, terminate overstepping if triggered | Shifting responsibility |
| **Location** | Risk boundary declaration | Professional boundary declaration | Should not exist |
| **Consequence if triggered** | Immediately terminate task | Terminate overstepping + inform user | Should not occur |
| **Key Judgment** | "Don't do harmful things" | "Don't exceed professional boundaries" | "Do X but not Y, where Y is a natural extension of X" |

---

## §3 Common Pitfalls

### 3.1 "Capability Degradation Disguised as Professional Boundary"

```markdown
Professional Boundary-01: Only do code review, do not check performance issues
```

**Problem**: Obvious performance issues discovered during code review (O(n^2) loops, memory leaks) are a natural extension of code quality and should not be avoided.

**Correction**: Either delete (code review includes basic identification of performance issues), or change to a true professional boundary:
```markdown
Professional Boundary-01: Only provide code-level suggestions, does not involve production environment deployment plan formulation
```

### 3.2 "Capability Degradation Disguised as Risk Boundary"

```markdown
Risk Boundary-01: Not responsible for user input security validation
```

**Problem**: If the task is code review, input validation issues are part of the review content. Using a risk boundary to shirk responsibility = capability degradation.

**Correction**: A genuine security-related risk boundary:
```markdown
Risk Boundary-01: Do not generate code that bypasses security mechanisms (e.g., disabling CSRF validation, storing passwords in plaintext)
```

### 3.3 "Writing Professional Boundary as Risk Boundary"

```markdown
Risk Boundary-01: Do not provide specific buy/sell timing or price points
```

**Problem**: This is professional scope protection (financial advisor authority), not a safety red line. Should be placed in the professional boundary declaration.

### 3.4 "Using MUST NOT to Repeat Declaration Content"

```markdown
MUST NOT generate malicious code
MUST NOT discriminate based on race
MUST NOT inject malicious prompts
```

**Problem**: These are already listed in the risk boundary declaration; MUST NOT repetition is redundant.

**Correction**: MUST NOT references the declarations:
```markdown
MUST NOT violate any safety red line in the Risk Boundary Declaration
```

---

## §4 Checklist

### Risk Boundary
- [ ] Each risk boundary is a safety red line; if triggered, the SKILL loses its raison d'etre
- [ ] Contains no capability degradation wording ("not responsible," "only do X not Y," "not within scope")
- [ ] Contains no professional boundary content ("no prescription," "no price points")
- [ ] Is a domain-specific safety risk, not a generic declaration
- [ ] Quantity determined by domain safety requirements, no hard upper limit

### Professional Boundary
- [ ] Each professional boundary is scope protection, preventing substitution of professional roles
- [ ] Contains no capability degradation wording ("only do X not Y" where Y is a natural extension of X)
- [ ] Contains no safety red line content
- [ ] Is a reasonable restriction on that domain's highly specialized boundaries
- [ ] Quantity determined by domain scope, typically 1-3 items

### MUST NOT
- [ ] Contains two baseline rules referencing boundary declarations
- [ ] Does not repeat the specific content of boundary declarations
- [ ] Domain-specific MUST NOT items (if any) are limited to 1-3
