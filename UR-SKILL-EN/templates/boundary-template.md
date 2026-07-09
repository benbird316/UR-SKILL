# Boundary Declaration Template

> Purpose: Defines the standard fill-in format for SKILL risk boundary declarations and professional boundary declarations
> Core principle: Risk boundaries are safety red lines; professional boundaries are cross-domain protections; neither is capability degradation
> Design methodology: see [design-guides/boundary-design-guide.md](../design-guides/boundary-design-guide.md)

---

## 1. Risk Boundary Declaration

Risk boundary declarations are the non-negotiable safety red lines of a SKILL. Triggering any red line results in immediate task termination.

**Core constraints**:
- Risk boundaries are safety brakes, declaring only safety red lines -- not doing harmful things.
- Risk boundary numbering starts consecutively from `Risk Boundary-01`; the quantity is determined by domain safety requirements (typically 3-5 entries).

**Positive Example (Generic Template)**:

| No. | Declaration |
|:---|:---|
| Risk Boundary-01 | {A non-negotiable safety red line for this domain, e.g., "Do not generate executable malicious code"} |
| Risk Boundary-02 | {A non-negotiable safety red line for this domain} |
| Risk Boundary-03 | {A non-negotiable safety red line for this domain} |

**Negative Example (Risk Boundary Abuse -> Anti-pattern 7)**:

| Abusive Wording | Problem |
|:---|:---|
| Risk Boundary-01: Not responsible for security review | Capability degradation, not a safety scenario |
| Risk Boundary-02: Only perform intent recognition | Capability degradation, not a safety scenario |

---

## 2. Professional Boundary Declaration

Professional boundary declarations are the non-crossable professional limitations of a SKILL. Triggering any one halts the boundary-crossing behavior and explicitly notifies the user.

**Core constraints**:
- Professional boundaries prevent the SKILL from crossing into domains requiring professional qualifications (medical, legal, financial services, etc.).
- Professional boundary numbering starts consecutively from `Professional Boundary-01`; the quantity is determined by domain scope (typically 1-3 entries).

**Positive Example (By Domain)**:

| No. | Declaration | Applicable Domain |
|:---|:---|:---|
| Professional Boundary-01 | Provides condition analysis reference only; cannot replace a doctor's prescription or diagnosis | Medical |
| Professional Boundary-02 | Output is risk assessment reference; does not include specific buy/sell timing and price points | Financial |
| Professional Boundary-03 | Provides legal knowledge explanation only; does not constitute formal legal opinion | Legal |

**Negative Example (Capability Degradation Disguised as Professional Boundary)**:

| Abusive Wording | Problem |
|:---|:---|
| Professional Boundary-01: Only do security review, not quality checks | Capability degradation (code errors found during security review should still be reported) |
| Professional Boundary-02: Only check code style, do not analyze functional correctness | Capability degradation (functional issues found during style checks should still be flagged) |

---

## 3. Completeness Checklist

- [ ] All risk boundary declarations are safety red lines (no scope limitations or capability degradation); trigger results in termination
- [ ] Risk boundary numbering starts consecutively from `Risk Boundary-01`
- [ ] All professional boundary declarations are cross-domain protections (no safety declarations or capability degradation); trigger halts the boundary-crossing behavior
- [ ] Professional boundary numbering starts consecutively from `Professional Boundary-01`
- [ ] Risk boundaries and professional boundaries have no overlapping entries
- [ ] No placeholder residue
