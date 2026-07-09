# Examples File Design Guide

> Purpose: Define the standard format, content requirements, and design methodology for example files (examples.md)
> Core principle: Examples are the core of Few-Shot Learning -- you must explain "why this output"

---

## 1. Why Example Files Are Needed

Example files are a standard practice in Prompt Engineering. LLMs learn task patterns through examples more effectively than through pure instructions.

If examples are not provided:
- LLM understanding of output format has large deviations
- Edge case handling is inconsistent
- Error scenarios cannot be identified

The example file is an **instructional reference file** (L3), loaded on demand. When an LLM generates SKILL content, it loads the example file to understand the expected output format.

---

## 2. Standard Format of Example Files

### 2.1 Five Required Elements

| Element | Description | Why It's Required |
|:---|:---|:---|
| **Scenario** | Under what circumstances this example is used | Helps the LLM understand the example's applicable scope |
| **Input** | The user input | Defines input format and content |
| **Output** | The expected output | Defines output format and content |
| **Rationale** | Why this is the output | The instructional core; without Rationale, examples become simple mappings, and the LLM cannot generalize to new scenarios |
| **Boundary Note** | Why it is NOT another output | Required for boundary/error examples; helps the LLM understand when a certain output must NOT be produced |

> Why five elements: LangChain FewShotPromptTemplate requires example_prompt to define input_variables and template. Rationale corresponds to the instructional need of "why this output." Fewer than five turns examples into simple mappings; more than five reduces information density.

### 2.2 Format Example

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

**Rationale**: {Why this is the output, core reasoning logic}

**Boundary Note**: {When this output must NOT be produced, common errors}
```

---

## 3. Generation Method (ur-skill Special Notes)

> This SKILL is a "SKILL for designing SKILLs" (ur-skill) and has no historical project accumulation.
> Therefore, examples are not "collected from historical projects" but "dynamically researched and generated based on the core scenarios of the generated SKILL."

### 3.1 Generation Based on Web Research

When using this SKILL to generate a specific SKILL, follow these steps to generate examples:

1. **Identify core scenarios**: Extract the SKILL's core use cases from user requirements
2. **Research typical use cases via web search**: Search for typical input/output pairs, tutorials, and best practice cases in that scenario
3. **Design examples**:
   - Typical scenarios: Search for the 1-2 most common use cases
   - Boundary scenarios: Search for boundary conditions, exceptional inputs, limit value handling
   - Error scenarios: Search for common error input and error output patterns
4. **Validate examples**:
   - [ ] Input is complete and unambiguous
   - [ ] Output is complete with no placeholders
   - [ ] Rationale is clearly explained (why this output)
   - [ ] Boundary Note covers common errors (why not another output)

### 3.2 Generation Based on User Instructions

If the user provides specific scenarios or existing materials:

1. **Analyze user materials**: Extract typical use cases, boundary cases, and error cases from user descriptions
2. **Design examples**: Convert user descriptions into the "Input → Output → Rationale → Boundary Note" structure
3. **Supplement with research**: For scenarios not covered by the user, supplement via web research on typical/boundary/error examples
4. **Validate completeness**:
   - [ ] Covers all use cases mentioned by the user
   - [ ] Supplements boundary scenarios not mentioned by the user but common in the industry
   - [ ] Example count matches complexity (simple 1-2, medium 2-3, complex 3+)

### 3.3 ur-skill Generation Examples

When ur-skill designs a SKILL, it references the following example templates (for detailed generation flow, see ur-skill.md workflow execution steps):

**Example 1: Generating a Simple SKILL (Python Code Inspection)**

**Input**:
```
User requirement: Need a SKILL to check Python code quality
```

**Output**:
```yaml
---
name: python-code-inspector
description: "Use when reviewing Python code for quality issues..."
metadata:
  updated: 2026-07-09
  type: prompt
  whenToUse: Use when reviewing Python code quality
---

# Python Code Inspector

## Capability Matrix
...
```

**Rationale**: A simple SKILL only needs a single file, no references/ required. The Capability Matrix has 1 core domain + radiating domains determined by task analysis, and review dimensions are allocated by node type.

**Boundary Note**: If the user requires checking multiple languages, complexity should be upgraded to medium with the addition of a references/ directory.

---

## 4. Example File Design Methodology

### 4.1 Designing Example Count by Complexity

| Complexity | Example Count | Coverage Requirements | Why |
|:---|:---:|:---|:---|
| Simple | 1-2 | Typical scenarios | Simple tasks have a single pattern; too many examples increase token consumption with diminishing returns |
| Medium | 2-3 | Typical scenarios + boundary scenarios | Medium tasks have boundary cases that require demonstrating boundary handling capability |
| Complex | 3+ | Typical scenarios + boundary scenarios + error scenarios + complex scenarios | Complex tasks have diverse patterns and require error scenarios so the LLM learns "what not to do" |

> Why count positively correlates with complexity: Simple tasks have a single pattern; 1 high-quality example is sufficient. Complex tasks have diverse patterns and require multiple examples covering different patterns. But quality matters more than quantity: 1 high-quality example > 3 low-quality examples.

### 4.2 Example Types

| Type | Purpose | Must Include |
|:---|:---|:---:|
| **Typical Scenario** | Demonstrates standard processing capability | Required |
| **Boundary Scenario** | Demonstrates boundary handling capability | Required for medium and above |
| **Error Scenario** | Demonstrates "what not to do" | Required for complex |
| **Complex Scenario** | Demonstrates multi-step/multi-condition handling capability | Required for complex |

> Why error scenarios are needed: LLMs learning "what not to do" from error examples is more effective than learning "how to do" from positive examples (negative sample learning has been proven effective in machine learning).

### 4.3 Steps for Designing Examples

1. **Identify typical scenarios**: The 1-2 most common use scenarios
2. **Identify boundary scenarios**: Inputs near boundary values, ambiguous conditions, multi-condition conflicts
3. **Identify error scenarios**: Common error inputs, common error outputs
4. **Validate example quality**:
   - [ ] Input is complete and unambiguous
   - [ ] Output is complete with no placeholders
   - [ ] Rationale is clearly explained
   - [ ] Boundary Note covers common errors

---

## 5. Example File Content Requirements

### 5.1 Content That Must Be Addressed

- **Each example MUST have a Rationale**: Without Rationale, examples become simple Input→Output mappings that the LLM cannot generalize to new scenarios.
- **Boundary/error examples MUST have a "Boundary Note"**: Without explaining "why not another output," the LLM may repeat the error in similar scenarios.
- **Examples MUST be complete with no placeholders**: `[xxx]`, `{to be filled}`, and other placeholders in the Output violate Anti-pattern 2.

### 5.2 Prohibited Content

- **Prohibited: Examples without Rationale**: Examples without Rationale are "black-box mappings"; the LLM cannot learn the reasoning process.
- **Prohibited: Placeholder residue**: Example Output must be complete and must not contain unfilled content.
- **Prohibited: Examples duplicating body content**: Examples go into ../examples/examples.md; body only retains reference declarations.

---

## 6. Synergy with Capability Architecture

Example files support the capability layers within the capability architecture:

| Capability Layer | Example Type | Function |
|:---|:---|:---|
| Foundation Layer | Typical scenarios | Demonstrates standard processing capability |
| Advanced Layer | Boundary scenarios | Demonstrates boundary handling capability |
| Expert Layer | Error scenarios | Demonstrates error identification and remediation capability |
| Extension Layer | Complex scenarios | Demonstrates multi-step/multi-condition handling capability |

---

## 7. Completeness Checklist

When designing example files, check each item:

- [ ] Example count matches complexity (simple 1-2, medium 2-3, complex 3+)
- [ ] Each example contains five elements (Scenario, Input, Output, Rationale, Boundary Note)
- [ ] Each example has a Rationale (why this output)
- [ ] Boundary/error examples have Boundary Notes (why not another output)
- [ ] Example Output is complete with no placeholders
- [ ] Examples do not duplicate body content (examples in references/, body only references them)
- [ ] File < 200 lines; split if exceeded
- [ ] Examples cover typical + boundary + error (medium and above)
