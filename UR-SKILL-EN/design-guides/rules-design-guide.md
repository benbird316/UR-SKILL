# Rules Design Guide

> Purpose: Define the design principles for the rule system (MUST / MUST NOT / SHOULD / SHOULD NOT / MAY) for generating SKILLs
> Core principle: Rules are verifiable behavioral constraints; Gates are process checks, Anti-patterns are result checks -- the three complement each other without substituting

---

## 1. Rule Design Principles

1. Rules MUST be verifiable behavioral constraints within the SKILL domain, not assumptions about the target platform or guesses about the user
2. Abstract rules are prohibited (e.g., "do good work," "ensure quality")
3. Self-contradiction is prohibited: Rules must be logically consistent with each other; MUST A and MUST NOT A cannot coexist
4. MUST NOT rules do not duplicate the specific content of boundary declarations; declarations are the authoritative source of boundaries

---

## 2. RFC 2119 Keyword Semantics

The rule template follows RFC 2119 (and RFC 8174) standards. Keywords in **ALL CAPS** carry special meaning and can be mechanically parsed by tools:

| Keyword | Meaning |
|:---|:---|
| MUST | Absolute requirement |
| MUST NOT | Absolute prohibition |
| SHOULD | Strongly recommended |
| SHOULD NOT | Strongly discouraged |
| MAY | Truly optional |

---

## 3. Relationship Between Gates and Anti-Patterns

| Mechanism | Type | Execution Timing | Function |
|:---|:---|:---|:---|
| Gate | Process check | Dynamic, executed at each step | Real-time rule compliance verification |
| Anti-Pattern Scan | Result check | Static, once before delivery | Identifies practices that "seem correct but are actually harmful" |

The two complement each other without substituting. Gates check the rule execution process, while anti-pattern scans inspect the final deliverable.

---

## 4. Separation of Responsibilities: Rules, Gates, Anti-Patterns, Risk Boundaries, and Professional Boundaries

| Element | Responsibility | Prohibited |
|:---|:---|:---|
| Rules | Verifiable behavioral constraints | Abstraction, contradiction, duplication of boundary declarations |
| Gates | Process checkpoints, referencing rule numbers | Duplicating rule content |
| Anti-Patterns | Result checks, identifying harmful practices | Including universal anti-patterns (handled uniformly by UR-SKILL) |
| Risk Boundaries | Safety red lines | Including scope restrictions or capability degradation |
| Professional Boundaries | Scope-overreach protection | Including safety declarations or capability degradation |

These five elements have separated responsibilities with no overlap.
