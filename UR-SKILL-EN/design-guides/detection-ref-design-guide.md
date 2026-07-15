# Detection Ref Design Guide

> Only teaches how to write detection ref files. Detection refs answer "How to find it?" — location methods + tracing strategies + tools.

## Format

```markdown
> Loading Phase: Step 2

## {Method Name}

**Applicable Scenario**: {When to use this method}

**Prerequisites**: {Conditions that must be met before execution — required permissions, environment, data}

**Input**:
| Parameter | Type | Required | Description |
|:---|:---|:---|:---|
| {Parameter name} | {Type} | Yes/No | {One sentence} |

**Steps**:
1. [{Tool Category}] {Operation} → {Expected Output}
2. [{Tool Category}] {Operation} → {Expected Output}

**Return Value**:
| Output | Type | Description |
|:---|:---|:---|

**Degradation Path**: {Fallback plan when the preferred tool is unavailable}

**Common Errors**:
| Error | Cause | Handling |
|:---|:---|:---|
```

## Rules

- Each step MUST be bound to a tool category (`[Text Search]`, `[Command Execution]`, `[File Read]`, etc.)
- Each operation MUST have an expected output — not "execute X", but "execute X → should satisfy Y"
- MUST include a degradation path — fallback options or manual alternatives for the tool
- Do not write classification definitions (that is the Classification Ref's concern), do not write fix strategies (that is the Pattern Ref's concern)
- MUST define the **input signature** (parameter table with type + required columns, non-omittable) and the **return value table**, following the referencability principle in ref-types-design-guide.md §1.2
- MUST list **Common Errors** and their handling methods — a method cannot self-calibrate without correct/incorrect feedback
- MUST include the **source** of the method/API used (K-type + source + acquisition date), following the timeliness principle

## Length

<= 150 lines. Each method is typically 10-20 lines, with 4-7 methods being appropriate.
