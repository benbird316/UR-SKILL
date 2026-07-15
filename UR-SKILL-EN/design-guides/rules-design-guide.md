# Rules Design Guide

> **Purpose**: Define the design principles for the generated SKILL's rule system (MUST / MUST NOT / SHOULD / SHOULD NOT / MAY)
> **Core Principle**: Rules are verifiable behavioral constraints; gates are process checks, anti-patterns are result checks — the three are complementary, not substitutable

---

## 1. Rule Design Principles

1. Rules must be verifiable behavioral constraints within that SKILL's domain, not assumptions about the target platform or guesses about the user
2. Prohibit abstract rules (e.g., "do good work," "ensure quality")
3. Prohibit self-contradiction: different rules must be logically consistent; MUST A and MUST NOT A cannot appear simultaneously
4. MUST NOT does not repeat the specific content of boundary declarations; declarations are the authoritative source for boundaries

---

## 2. RFC 2119 Keyword Semantics

The rule template follows RFC 2119 (and RFC 8174) standards; keywords have special meanings when in **ALL CAPS** and can be mechanically parsed by tools:

| Keyword | Meaning |
|:---|:---|
| MUST | Mandatory requirement |
| MUST NOT | Absolute prohibition |
| SHOULD | Strong recommendation |
| SHOULD NOT | Strongly not recommended |
| MAY | Optional |

---

## 3. Relationship Between Gates and Anti-Patterns

| Mechanism | Type | Execution Timing | Function |
|:---|:---|:---|:---|
| Gate | Process check | Dynamic, executed per step | Real-time verification of rule compliance |
| Anti-pattern scan | Result check | Static, executed once before delivery | Identifies "seemingly correct but actually harmful" practices |

The two are complementary, not substitutable. Gates check the rule execution process; anti-pattern scanning checks the final deliverable.

---

## 4. Responsibility Separation: Rules, Gates, Anti-Patterns, Risk Boundaries, Professional Boundaries

| Element | Responsibility | Prohibited |
|:---|:---|:---|
| Rules | Verifiable behavioral constraints | Abstract, contradictory, duplicate boundary declarations |
| Gates | Process checkpoints, reference rule numbers | Repeat rule content |
| Anti-patterns | Result checks, identify harmful practices | Include generic anti-patterns (handled uniformly by UR-SKILL) |
| Risk boundaries | Safety red lines | Include scope limitations or capability degradation |
| Professional boundaries | Scope protection | Include safety declarations or capability degradation |

The five elements have separate responsibilities with no overlap.
