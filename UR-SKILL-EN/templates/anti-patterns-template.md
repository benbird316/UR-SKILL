# Anti-Patterns File Template

> Purpose: Defines the standard structure for generating a SKILL's anti-patterns.md
> Core Principle: Anti-patterns must explain the complete pedagogical chain of "Good Intention -> Goes Wrong -> Why -> How to Do It Right"
> For design methodology details, see [design-guides/anti-patterns-design-guide.md](../design-guides/anti-patterns-design-guide.md)

---

## 1. Universal Anti-Pattern References

Universal anti-patterns (placeholder residue, specification overreach, example contamination, architecture confusion, checklist omission, blind-spot evasion, risk boundary abuse, dimension stuffing, blind-spot handoff) are handled uniformly by UR-SKILL. This file only lists anti-patterns specific to this SKILL's domain.

> Universal anti-patterns are defined centrally in UR-SKILL's References/anti-patterns.md; do not repeat them when generating a SKILL.

---

## 2. Domain-Specific Anti-Patterns

### Anti-Pattern 1 {Domain-Specific Anti-Pattern Name}

| Dimension | Content |
|:---|:---|
| **Manifestation** | {The specific manifestation of this anti-pattern in the domain} |
| **Why It Occurs** | {The developer's good intention / background reason} |
| **Harm** | {Why this practice is harmful} |
| **Detection Method** | {How to identify it} |
| **Avoidance Strategy** | {The correct approach} |

### Anti-Pattern 2 {Domain-Specific Anti-Pattern Name}

| Dimension | Content |
|:---|:---|
| **Manifestation** | {Specific manifestation} |
| **Why It Occurs** | {The developer's good intention / background reason} |
| **Harm** | {Harm} |
| **Detection Method** | {Detection method} |
| **Avoidance Strategy** | {Avoidance strategy} |

---

## 3. Completeness Checklist

- [ ] Only domain-specific anti-patterns; no universal anti-patterns
- [ ] Each anti-pattern contains Manifestation, Why It Occurs, Harm, Detection Method, Avoidance Strategy
- [ ] Detection methods are specific and executable
- [ ] Avoidance strategies point to the correct approach
- [ ] File < 200 lines
