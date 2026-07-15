# Rules Template

> **Purpose**: Provide a structural template for defining domain behavior constraints in generated SKILLs.
> **Usage**: Based on task analysis results, replace placeholders in this template with the target domain's specific rules. Rules only declare constraints; enforcement checks are handled by workflow gates.
> **Core Principle**: Rules, gates, anti-patterns, risk boundaries, and professional boundaries have separated responsibilities; this template contains only rules, gates, and domain-specific anti-patterns.
> **Design Methodology**: See [design-guides/rules-design-guide.md](../design-guides/rules-design-guide.md)
>
> **Related Templates**:
> - Identity Declaration: [templates/identity-template.md](../templates/identity-template.md)
> - Boundary Declaration: [templates/boundary-template.md](../templates/boundary-template.md)

---

## 1. Rules

### 1.1 Hard Constraints (MUST)

Each rule in this section describes behavior the SKILL MUST perform. Rule count: 3-8 items. Each rule MUST include a clear action and trigger condition.

- **Rule 01 MUST** {Action requirement}. {Trigger condition or scope qualification}
- **Rule 02 MUST** {Action requirement}. {Trigger condition or scope qualification}

### 1.2 Hard Prohibitions (MUST NOT; fewer is better)

MUST NOT is an absolute prohibition, used only for behavior that would cause actual harm. For other scenarios, prefer positive MUST or SHOULD NOT.

The following two rules are **boundary reference rules that every SKILL MUST include**; they do not duplicate the specific content of boundary declarations:

- **Rule N MUST NOT** Violate any safety red line in the risk boundary declarations (see [templates/boundary-template.md](../templates/boundary-template.md))
- **Rule N+1 MUST NOT** Exceed any professional boundary in the professional boundary declarations (see [templates/boundary-template.md](../templates/boundary-template.md))

Additional domain-specific MUST NOT rules may be added (keep to 1-3 items):

- **Rule N+2 MUST NOT** {Domain-specific prohibited behavior}. {Trigger condition}

### 1.3 Strong Preferences (SHOULD / SHOULD NOT)

Each rule in this section describes behavior the SKILL is strongly recommended or strongly not recommended to perform. Rule count: 2-4 items.

- **Rule N SHOULD** {Recommended action}
- **Rule N SHOULD NOT** {Not recommended action}

### 1.4 Optional (MAY)

Each rule in this section describes behavior the SKILL may optionally perform. Rule count: 1-3 items.

- **Rule N MAY** {Optional action}

---

## 2. Gate Checkpoints

Gates dynamically validate rule compliance during workflow execution. Check items reference rule numbers; on failure, execute a specified action.

| Checkpoint | Check Item (Rule Reference) | Action on Failure |
|:---|:---|:---|
| {Gate name} | {Referenced rule number(s)} | {Which stage to fall back to, what remediation action to perform} |

> See [design-guides/rules-design-guide.md §3](../design-guides/rules-design-guide.md) for gate design principles.

---

## 3. Anti-Pattern Scan (Static Check)

Anti-patterns are checked once before delivery to identify practices that "appear correct but are actually harmful." Only domain-specific anti-patterns for this SKILL's domain are listed.

| No. | Anti-Pattern | Detection Method | Fix Strategy |
|:---|:---|:---|:---|
| Anti-pattern 1 | {Anti-pattern name} | {Specific detection approach} | {Fix strategy} |
| Anti-pattern 2 | {Anti-pattern name} | {Specific detection approach} | {Fix strategy} |

> See [design-guides/pattern-ref-design-guide.md](../design-guides/pattern-ref-design-guide.md) §3 for anti-pattern scan design principles.

---

## 4. Completeness Checklist

- [ ] Rules use RFC 2119 keywords (MUST / MUST NOT / SHOULD / SHOULD NOT / MAY)
- [ ] Hard constraints count: 3-8 items (MUST)
- [ ] Hard prohibitions (MUST NOT) include two boundary reference rules, do not duplicate specific content of boundary declarations
- [ ] Strong preferences count: 2-4 items (SHOULD / SHOULD NOT)
- [ ] Optional count: 1-3 items (MAY)
- [ ] No abstract rules (e.g., "do a good job")
- [ ] No contradictory rules (e.g., Rule 01 says MUST A, Rule 02 says MUST NOT A)
- [ ] Gate checkpoints reference rule numbers, do not duplicate rule content
- [ ] Anti-patterns only list domain-specific ones, not generic anti-patterns
- [ ] Rules, gates, anti-patterns, risk boundaries, and professional boundaries have separated responsibilities with no overlap
- [ ] Specific content of risk boundaries and professional boundaries is not duplicated in this template; it is handled by [templates/boundary-template.md](../templates/boundary-template.md)
