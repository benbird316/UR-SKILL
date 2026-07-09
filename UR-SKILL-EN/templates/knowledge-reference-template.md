# Knowledge Reference File Template

> Purpose: Defines the standard structure for generating a SKILL's knowledge reference files
> Core Principle: Knowledge files represent "what to know," not "how to do" or "what not to do"
> For design methodology details, see [design-guides/knowledge-reference-design-guide.md](../design-guides/knowledge-reference-design-guide.md)
> Subtypes: K1 Domain Knowledge / K2 API & CLI Reference / K3 Configuration & Policy / K4 Design Patterns

---

## K1 Domain Knowledge Template

### {Concept Name}

**Definition**: {One-sentence precise definition}

**Rules**:
- {Rule 1}
- {Rule 2}
- {Rule 3}

**Priority**: When {Rule A} conflicts with {Rule B} -> {Decision rule}

> **Source**: {Source} | **Validity**: {Long-term / Needs periodic update} | **Review Cycle**: {N months}

---

## K2 API / CLI Reference Template

### {Tool / API Name}

#### Call Signature
`{command_signature}` or `{method_signature}`

#### Parameters

| Parameter | Type | Required | Default | Description |
|:---|:---|:---:|:---|:---|
| {param1} | {type} | {MUST/SHOULD} | {default} | {Description} |

#### Return Value
- Success: {Format and example}
- Failure: {Error format and common error codes}

---

## K3 Configuration / Policy Template

### {Policy Name}

**Rule**: {Policy content}

**Scope**:
- Applicable: {Scenario A, Scenario B}
- Not applicable: {Scenario C}

**Violation Handling**: {Specific action upon violation}

---

## K4 Design Pattern Template

### {Pattern Name}

**Context**: {Under what requirements/constraints to use}

**Solution**: {Specific approach, with code/configuration examples}

**Trade-offs**:
- Advantages: {Benefits}
- Costs: {Costs}

**Non-applicable Scenarios**: {When not to use}

---

## Completeness Checklist

- [ ] Subtype selected (K1/K2/K3/K4)
- [ ] Meets subtype element requirements
- [ ] One file, one topic
- [ ] Each rule/constraint is numbered
- [ ] Knowledge entries have source and validity annotations
- [ ] Body does not duplicate content from this file
- [ ] File < 200 lines
