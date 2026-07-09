# Boundary Design Guide

> Purpose: Defines the design methods, evaluation criteria, and common pitfalls for SKILL Risk Boundaries and Professional Boundaries
> Core Principle: Risk Boundaries are about "do no harm"; Professional Boundaries are about "do not operate beyond professional boundaries"; neither is capability degradation

---

## 1. Why Distinguish

A SKILL's boundary design directly affects its safety and reliability. If the three concepts are not distinguished:

- **Capability degradation** masquerading as a "boundary": the SKILL actively reduces the capabilities it should assume, and the user receives incomplete output
- **Safety red lines** and **scope protection** conflated: either safety constraints are diluted, or professional divisions become blurred
- `MUST NOT` rules cannot be precisely targeted -- is the prohibition about preventing harm, or preventing scope violation?

After correct differentiation:
- Safety red lines → `MUST NOT` (terminate immediately upon triggering)
- Scope protection → `MUST NOT` (terminate the boundary-crossing behavior immediately, inform the user)
- Capability degradation → anti-pattern, must not exist

---

## 2. Definition of the Three Concepts

### 2.1 Risk Boundaries (Safety Red Lines)

| Dimension | Content |
|:---|:---|
| **Essence** | "Do no harm" -- the safety baseline |
| **Nature** | Safety-related; upon triggering, the task terminates immediately |
| **Location** | Risk Boundary declarations (rules-template.md SS2) |
| **Count** | Determined by domain safety requirements, typically 3-5 items |
| **Criterion** | Upon triggering, the SKILL itself loses its reason for existence |

**Correct Examples**:

| No. | Declaration | Rationale |
|:---|:---|:---|
| 01 | Do not generate executable malicious code (ransomware, mining scripts) | Triggering = SKILL is aiding wrongdoing |
| 02 | Do not discriminatively label or process data based on race/gender/age | Triggering = SKILL is actively creating discrimination |
| 03 | Do not output illegal content or information that violates privacy | Triggering = SKILL is breaking the law |

**Counterexamples (Capability Degradation in Disguise)**:

| Misuse | Problem |
|:---|:---|
| 01: Only responsible for security review, does not check code errors | Capability degradation -- code errors discovered during security review should also be reported |
| 02: Only does code style checking, does not analyze functional correctness | Capability degradation -- functional errors are a natural extension of style checking |
| 03: Performance issues are outside the inspection scope | Capability degradation -- declaring "won't do X" when X is a natural part of the task |

### 2.2 Professional Boundaries (Scope Protection)

| Dimension | Content |
|:---|:---|
| **Essence** | "Do not operate beyond professional boundaries" -- do not overstep to substitute for a professional role |
| **Nature** | Scope-related; upon triggering, the boundary-crossing behavior terminates, and the user is explicitly informed |
| **Location** | Professional Boundary declarations (rules-template.md SS3) |
| **Count** | Determined by domain scope, typically 1-3 items |
| **Criterion** | Prevents the SKILL from overstepping into domains requiring professional qualifications |

**Correct Examples**:

| No. | Declaration | Applicable Domain | Rationale |
|:---|:---|:---|:---|
| 01 | Only provides medical condition analysis for reference; must not substitute for a physician's prescription or diagnosis | Medical | AI has no authority to exercise a licensed physician's prescribing rights |
| 02 | Output is for risk assessment reference only; does not include specific buy/sell timing and price levels | Financial | AI has no authority to issue trade-level investment directives |
| 03 | Only provides legal knowledge explanation; does not constitute formal legal opinion | Legal | AI has no authority to issue legally binding opinion letters |

**Counterexamples (Capability Degradation in Disguise)**:

| Misuse | Problem |
|:---|:---|
| 01: Only does security review, not quality inspection | Capability degradation -- code errors found during security review should still be reported |
| 02: Only checks code style, does not analyze functional correctness | Capability degradation -- functional issues are a natural extension of style checking |

### 2.3 Capability Degradation (Anti-pattern)

| Dimension | Content |
|:---|:---|
| **Essence** | "Does X but chooses not to report Y" -- Y is a natural extension of X, but the SKILL actively refuses |
| **Nature** | Abdication of responsibility, not a boundary |
| **Location** | Must not exist anywhere |
| **Criterion** | The SKILL already has the capability but actively refuses; constitutes abdication of responsibility |

**Typical Patterns**:
- "Only does X, not Y" -- but Y is a natural extension of X
- "X is outside the inspection scope" -- but X is a reasonable expectation of the current capability
- "Not responsible for X" -- but X is a reasonable component of the current task

---

## 3. Three-Concept Quick Reference

| | Risk Boundary (Safety Red Line) | Professional Boundary (Scope Protection) | Capability Degradation (Anti-pattern) |
|:---|:---|:---|:---|
| **Essence** | Do no harm | Do not operate beyond professional boundaries | Does X but chooses not to report Y |
| **Nature** | Safety-related; terminate upon triggering | Scope-related; terminate the boundary-crossing behavior upon triggering | Abdication of responsibility |
| **Location** | Risk Boundary declarations | Professional Boundary declarations | Must not exist |
| **Source** | Pre-analysis → Risk Identification | Capability Analysis → Scope Identification | Design flaw |
| **Trigger Consequence** | Immediately terminate the task | Terminate boundary-crossing behavior + inform the user | Should not occur |
| **Identification Key** | "Do no harm" | "Do not cross professional boundaries" | "Does X but won't report Y, where Y is a natural extension of X" |

---

## 4. Design Process

### 4.1 Pre-analysis Phase: Identify Risk Boundaries

When analyzing the target task domain, ask three questions:

1. **If this SKILL is abused, what is the greatest safety harm?**
   - Could it generate attack code or malicious tools?
   - Could it be used for discrimination, fraud, or illegal activities?
   - Could it leak privacy or bypass security mechanisms?

2. **What scenario, if it occurs, would cause this SKILL to lose its reason for existence?**
   - A code audit SKILL becomes a vulnerability generator → Risk Boundary
   - A content moderation SKILL becomes a discrimination labeler → Risk Boundary

3. **Are these safety red lines strongly related to the domain?**
   - Not generic declarations (like "do not break the law"), but safety risks specific to the domain

### 4.2 Capability Analysis Phase: Identify Professional Boundaries

When defining the SKILL's capability scope, ask three questions:

1. **Does this SKILL's capability touch domains requiring professional qualifications?**
   - Medical: diagnosis, prescriptions, treatment recommendations
   - Financial: investment directives, buy/sell timing, price levels
   - Legal: legal opinions, contract review, attorney letters

2. **Could the output recommendations be treated by the user as "professional decisions" to execute?**
   - "Recommend seeing a doctor for examination" → safe (not overstepping)
   - "You should take medication XX" → overstepping (substituting for a doctor's prescription)

3. **Is the output "providing reference information" or "substituting for a professional role in making decisions"?**
   - "This stock has been volatile recently, high risk" → safe (reference information)
   - "Buy at XX yuan tomorrow, sell at XX yuan" → overstepping (trade directive)

### 4.3 Design Phase: Write to Template

1. Safety risks → Risk Boundary declarations (rules-template.md SS2)
2. Professional scope limits → Professional Boundary declarations (rules-template.md SS3)
3. Add two reference rules in `MUST NOT` rules:
   - `MUST NOT` violate any safety red line in Risk Boundary declarations
   - `MUST NOT` exceed Professional Boundary declarations

---

## 5. Common Pitfalls

### 5.1 "Capability Degradation Disguised as Professional Boundary"

```markdown
Professional Boundary-01: Only does code review, does not check performance issues
```

Problem: Obvious performance issues discovered during code review (O(n^2) loops, memory leaks) are a natural extension of code quality and should not be avoided.

Correction: Either delete (code review includes basic identification of performance issues) or rewrite as a genuine professional boundary:
```markdown
Professional Boundary-01: Only provides code-level recommendations; does not formulate production environment deployment plans
```

### 5.2 "Capability Degradation Disguised as Risk Boundary"

```markdown
Risk Boundary-01: Not responsible for validating the security of user input
```

Problem: If the task is code review, input validation issues are part of the review content. Using a risk boundary to disclaim responsibility = capability degradation.

Correction: A genuine safety-related risk boundary:
```markdown
Risk Boundary-01: Do not generate code that bypasses security mechanisms (e.g., disabling CSRF validation, storing passwords in plaintext)
```

### 5.3 "Writing Professional Boundary as Risk Boundary"

```markdown
Risk Boundary-01: Do not provide specific buy/sell timing and price levels
```

Problem: This is scope protection (financial advisory authority), not a safety red line. It should go in Professional Boundary declarations.

Correction:
```markdown
Professional Boundary-01: Output is for risk assessment reference only; does not include specific buy/sell timing and price levels
```

### 5.4 "Repeating Declaration Content with MUST NOT"

```markdown
MUST NOT generate malicious code
MUST NOT discriminate based on race
MUST NOT inject malicious prompts
```

Problem: These are already listed in Risk Boundary declarations. Repeating them in `MUST NOT` is redundant.

Correction: `MUST NOT` references the declarations:
```markdown
MUST NOT violate any safety red line in Risk Boundary declarations
```

---

## 6. Checklist

When designing a SKILL's boundaries, verify each item:

### Risk Boundaries
- [ ] Each risk boundary is a safety red line; upon triggering, the SKILL loses its reason for existence
- [ ] Free of capability degradation wording ("not responsible for", "only does X not Y", "outside scope")
- [ ] Free of professional boundary content ("do not give prescriptions", "do not give price levels")
- [ ] Specific safety risks for the domain, not generic declarations
- [ ] Count determined by domain safety requirements; no hard upper limit

### Professional Boundaries
- [ ] Each professional boundary is scope protection, preventing substitution for professional roles
- [ ] Free of capability degradation wording ("only does X not Y" when Y is a natural extension of X)
- [ ] Free of safety red line content
- [ ] Reasonable constraints on highly specialized boundaries for the domain
- [ ] Count determined by domain scope, typically 1-3 items

### MUST NOT
- [ ] Contains two baseline rules referencing boundary declarations
- [ ] Does not repeat the specific content of boundary declarations
- [ ] Domain-specific `MUST NOT` (if any) kept to 1-3 items

---

## 7. Relationship with Other Files

```
boundary-design-guide.md (this file)
    │  Authoritative definitions of three concepts + design methods + pitfalls
    │
    ├─→ design-rationale.md SS8 Complexity determination; pre-analysis phase identifies risk boundary trigger conditions
    ├─→ anti-patterns.md             Anti-pattern 7 (Risk Boundary Abuse)
    ├─→ rules-template.md SS2, SS3   Declaration format templates
    ├─→ capability-architecture-template.md SS3, SS4  How to declare in capability architecture
    └─→ validate_skill.py            Automated detection (Risk Boundary Abuse, Professional Boundary Abuse)
```
