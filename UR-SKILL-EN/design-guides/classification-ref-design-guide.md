# Classification Ref Design Guide

> Only teaches how to write classification ref files. Classification refs answer "What is this?" — the domain classification system + characteristics of each class + judgment criteria.

## Format

```markdown
> Loading Phase: Step 1

## {Classification Name}

**Definition**: {One-sentence definition}

**Characteristics**:
- {Observable distinguishing characteristic 1}
- {Observable distinguishing characteristic 2}

**Judgment Criteria**: {Conditions under which it is classified as this type}

**Priority**: {Severity/processing order for this classification, e.g., P0/P1/P2}

**Common Misclassifications**:
- Typical ambiguous cases where "X looks like Y but is actually Y"
- How to judge boundary gray areas

**Related Standards/Sources**: {External knowledge source and acquisition date, e.g., K1 — OWASP 2024}
```

## Rules

- MUST list **observable** distinguishing characteristics — not descriptions, but concrete indicators that enable binary decisions
- Classifications must be mutually exclusive + collectively exhaustive (MECE)
- Do not write detection methods (that is the Detection Ref's concern), do not write fix strategies (that is the Pattern Ref's concern)
- If sub-classifications are needed under each classification, they must also follow MECE
- MUST include **Common Misclassifications** — the ambiguous boundary between this classification and its "close relatives"
- MUST include **Related Standards/Sources** (K-type + source + acquisition date), following the timeliness principle in ref-types-design-guide.md §1.2

## Length

<= 150 lines. Analysis-phase knowledge is typically the lightest. If exceeded, check whether methodology or fix content has been mixed in.
