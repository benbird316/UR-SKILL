# Boundary Declaration Template

> **Purpose**: Define the standard format for SKILL risk boundary and professional boundary declarations
> **Core Principle**: Risk boundaries are safety red lines; professional boundaries are scope protection; neither is capability degradation
> **Design Methodology**: See [design-guides/boundary-design-guide.md](../design-guides/boundary-design-guide.md)

---

## 1. Risk Boundary Declaration

Risk boundary declarations are the SKILL's inviolable safety red lines. Touching any red line immediately terminates the task.

**Core Constraints**:
- Risk boundaries are safety brakes; they only declare safety red lines -- don't do harmful things.
- Risk boundaries are numbered consecutively starting from `Risk Boundary-01`; the count is determined by domain safety requirements (typically 3-5 items).

**Correct Example (Generic Template)**:

| ID | Statement |
|:---|:---|
| Risk Boundary-01 | {Inviolable safety red line for this domain, e.g., "Do not generate executable malicious code"} |
| Risk Boundary-02 | {Inviolable safety red line for this domain} |
| Risk Boundary-03 | {Inviolable safety red line for this domain} |

**Incorrect Example (Risk Boundary Abuse -> Anti-pattern 7)**:

| Abusive Wording | Problem |
|:---|:---|
| Risk Boundary-01: Not responsible for security review | Capability degradation, not a safety scenario |
| Risk Boundary-02: Only perform intent recognition | Capability degradation, not a safety scenario |

---

## 2. Professional Boundary Declaration

Professional boundary declarations are the SKILL's inviolable professional scope limits. Touching any boundary terminates the boundary-crossing behavior and clearly informs the user.

**Core Constraints**:
- Professional boundaries prevent the SKILL from crossing into domains requiring professional qualifications (medical, legal, financial services, etc.).
- Professional boundaries are numbered consecutively starting from `Professional Boundary-01`; the count is determined by domain scope (typically 1-3 items).

**Correct Examples (by Domain)**:

| ID | Statement | Applicable Domain |
|:---|:---|:---|
| Professional Boundary-01 | Provides only condition analysis reference; cannot replace a doctor's prescription or diagnosis | Medical |
| Professional Boundary-02 | Output is a risk assessment reference; does not include specific buy/sell timing or prices | Financial |
| Professional Boundary-03 | Provides only legal knowledge explanation; does not constitute formal legal advice | Legal |

**Incorrect Examples (Capability Degradation Disguised as Professional Boundary)**:

| Abusive Wording | Problem |
|:---|:---|
| Professional Boundary-01: Only perform security review, not quality check | Capability degradation (code errors found during security review should still be reported) |
| Professional Boundary-02: Only check code style, not functional correctness analysis | Capability degradation (functional issues found during style checks should still be flagged) |

---

## 3. Completeness Checklist

- [ ] Risk boundary declarations are all safety red lines (no scope restrictions or capability degradation); termination on touch
- [ ] Risk boundary numbers are consecutive starting from `Risk Boundary-01`
- [ ] Professional boundary declarations are all scope protection (no safety declarations or capability degradation); termination of boundary-crossing behavior on touch
- [ ] Professional boundary numbers are consecutive starting from `Professional Boundary-01`
- [ ] No overlapping items between risk boundaries and professional boundaries
- [ ] No placeholder residue
