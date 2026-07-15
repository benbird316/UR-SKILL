# Examples Design Guide

> Only teaches how to write references/examples.md. Examples are the core of few-shot learning and must explain "why this output."
> To determine whether an examples file is needed, see skill-package-design-guide.md §2.

---

## §1 Standard Format

### 1.1 Five Required Elements

| Element | Description | Why Mandatory |
|:---|:---|:---|
| **Scenario** | The context in which this example applies | Lets the LLM understand the scope of applicability |
| **Input** | User input | Defines the input format and content |
| **Output** | Expected output | Defines the output format and content |
| **Rationale** | Why this is the output | Core of teaching; without Rationale, the example becomes a simple mapping |
| **Boundary Notes** | Why not other outputs | Lets the LLM understand under what conditions a particular output should NOT be produced |

### 1.2 Format Template

```markdown
## Example 1: {Scenario Description}

**Input**:
```
{User Input Content}
```

**Output**:
```
{Expected Output Content}
```

**Rationale**: {Why this is the output, core judgment logic}

**Boundary Notes**: {Under what conditions this output should NOT be produced, common mistakes}
```

### 1.3 Three Example Types

| Type | Description | Requirements |
|:---|:---|:---|
| **Typical Scenario** | Basic use case, demonstrates core behavior | All SKILLs MUST have at least 1 |
| **Boundary Scenario** | Edge case handling, demonstrates behavior transition points | Output format MUST be identical to typical examples, no new structural elements |
| **Error Scenario** | Handling of erroneous input, demonstrates rejection or repair logic | Functional SKILLs MUST have, creative SKILLs recommended |

---

## §2 Number of Examples

The number of examples is derived from the research-analyst's investigation and analysis results; there is no fixed number.

> Quality over quantity: 1 high-quality example > 3 low-quality examples.

---

## §3 Checklist

- [ ] Number of examples derived from research-analyst investigation and analysis results
- [ ] Each example includes five elements (Scenario, Input, Output, Rationale, Boundary Notes)
- [ ] Each example has a Rationale (why this is the output)
- [ ] Boundary/Error examples have Boundary Notes (why not other outputs)
- [ ] Example Output is complete with no placeholders
- [ ] Examples do not duplicate the body (examples in references/, body only references them)
- [ ] File < 200 lines; split if exceeded
