# Rules Template

> Purpose: Structural template for defining domain behavioral constraints for generated SKILLs.
> Usage Notes: Based on task analysis results, replace the placeholders in this template with target-domain-specific rules. Rules only declare constraints; enforcement verification is handled by workflow gates.
> Core Principle: Rules, gates, anti-patterns, risk boundaries, and professional boundaries have separated responsibilities; this template only contains rules, gates, and domain-specific anti-patterns
> For design methodology details, see [design-guides/rules-design-guide.md](../design-guides/rules-design-guide.md)
>
> Related Templates:
> - Identity Declaration: [templates/identity-template.md](../templates/identity-template.md)
> - Boundary Declaration: [templates/boundary-template.md](../templates/boundary-template.md)

---

## 1. Rules

### 1.1 Hard Constraints (MUST)

Each rule in this section describes a behavior the SKILL MUST perform. Rule count: 3-8 rules. Each rule MUST include an explicit action and trigger condition.

- **Rule01 MUST** {Action requirement}. {Trigger condition or scope limitation}
- **Rule02 MUST** {Action requirement}. {Trigger condition or scope limitation}

### 1.2 Hard Prohibitions (MUST NOT, prefer fewer over more)

MUST NOT is an absolute prohibition, used only for behaviors that cause actual harm. For other scenarios, prefer positive MUST or SHOULD NOT.

The following two are boundary reference rules that **every SKILL MUST include**; they do not repeat the specific content of the boundary declarations:

- **RuleN MUST NOT** violate any Safety Red Line in the risk boundary declaration (see [templates/boundary-template.md](../templates/boundary-template.md))
- **RuleN+1 MUST NOT** exceed any professional boundary in the professional boundary declaration (see [templates/boundary-template.md](../templates/boundary-template.md))

Additional domain-specific MUST NOT rules may be added (limit: 1-3):

- **RuleN+2 MUST NOT** {Domain-specific prohibited behavior}. {Trigger condition}

### 1.3 Strong Preferences (SHOULD / SHOULD NOT)

Each rule in this section describes a behavior the SKILL strongly recommends or strongly discourages. Rule count: 2-4 rules.

- **RuleN SHOULD** {Recommended action}
- **RuleN SHOULD NOT** {Discouraged action}

### 1.4 Optional (MAY)

Each rule in this section describes a behavior the SKILL may optionally perform. Rule count: 1-3 rules.

- **RuleN MAY** {Optional action}

---

## 2. Gate Checkpoints

Gates dynamically verify rule compliance during workflow execution. Check items reference rule numbers; if not passed, the specified action is executed.

| Checkpoint | Check Item (Rule Reference) | Failure Action |
|:---|:---|:---|
| {Gate Name} | {Referenced rule number} | {Roll back to which stage, execute what corrective action} |

> For gate design principles, see [design-guides/rules-design-guide.md section 3](../design-guides/rules-design-guide.md).

---

## 3. Anti-Pattern Scanning (Static Check)

Anti-pattern scanning is executed once before delivery, identifying practices that "appear correct but are actually harmful." Only list anti-patterns specific to this SKILL's domain.

| No. | Anti-Pattern | Detection Method | Fix Strategy |
|:---|:---|:---|:---|
| Anti-Pattern 1 | {Anti-pattern name} | {Specific detection method} | {Fix strategy} |
| Anti-Pattern 2 | {Anti-pattern name} | {Specific detection method} | {Fix strategy} |

> For anti-pattern scanning design principles, see [design-guides/anti-patterns-design-guide.md](../design-guides/anti-patterns-design-guide.md).

---

## 4. Completeness Checklist

- [ ] Rules use RFC 2119 keywords (MUST / MUST NOT / SHOULD / SHOULD NOT / MAY)
- [ ] Hard constraint count: 3-8 (MUST)
- [ ] Hard prohibitions (MUST NOT) include the two boundary reference rules, without repeating specific boundary declaration content
- [ ] Strong preference count: 2-4 (SHOULD / SHOULD NOT)
- [ ] Optional count: 1-3 (MAY)
- [ ] No abstract rules (e.g., "do a good job")
- [ ] No contradictory rules (e.g., Rule01 says MUST A, Rule02 says MUST NOT A)
- [ ] Gate checkpoints reference rule numbers, not repeating rule content
- [ ] Anti-patterns only list domain-specific ones, excluding universal anti-patterns
- [ ] Rules, gates, anti-patterns, risk boundaries, and professional boundaries have separated responsibilities, no overlap
- [ ] Specific content of risk boundaries and professional boundaries is not duplicated in this template; handled by [templates/boundary-template.md](../templates/boundary-template.md)
