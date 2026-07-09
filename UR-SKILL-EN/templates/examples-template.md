# Examples File Template

> Purpose: Defines the standard structure for generating a SKILL's examples.md
> For design methodology details, see [design-guides/examples-design-guide.md](../design-guides/examples-design-guide.md)

---

## Example 1: {Typical Scenario}

**Input**:
```
{User input content}
```

**Output**:
```
{Expected output content, complete with no placeholders}
```

**Rationale**: {Why this is the output; core decision logic}

**Boundary Note**: {Under what circumstances this output cannot be produced; common errors}

---

## Example 2: {Edge-Case Scenario}

**Input**:
```
{Boundary condition input}
```

**Output**:
```
{Expected output under boundary conditions}
```

**Rationale**: {Why this is the output; boundary handling logic}

**Boundary Note**: {Under what circumstances it would go to another branch}

---

## Example 3: {Error Scenario} (Required for complex complexity)

**Input**:
```
{Erroneous input}
```

**Output**:
```
{Error handling output; explicitly reject or provide fix suggestions}
```

**Rationale**: {Why the literal execution is not possible; what the potential risks are}

**Boundary Note**: {Key differentiating point from the correct example}

---

## Completeness Checklist

- [ ] Example count matches complexity (simple: 1-2, medium: 2-3, complex: 3+)
- [ ] Each example contains five elements: Scenario, Input, Output, Rationale, Boundary Note
- [ ] Output is complete with no placeholders
- [ ] Examples do not duplicate body content
- [ ] File < 200 lines
