# Specification-Type File Design Guide

> Purpose: Define the standard format and design methodology for specification-type reference files (metadata-spec.md, rules-template.md, etc.)
> Core principle: Specification-type files are "standard definitions" -- precise, unambiguous, and verifiable

---

## 1. Why a Specification-Type File Design Guide Is Needed

Specification-type files define standard formats (frontmatter fields, rule keywords, table structures). They differ from knowledge-type files:
- Specification-type files are **constraint definitions**, not knowledge transfer
- Specification-type files must be **precise and unambiguous**, not vague
- Specification-type files must be **verifiable** and automatable

If specification-type files are not defined:
- Generated SKILLs have inconsistent formats
- Frontmatter parsing fails
- Rule statements are chaotic and unenforceable

Specification-type files are **specification-type reference files** (L3), loaded on demand. When generating a SKILL, specification-type files are loaded to ensure format compliance.

---

## 2. Standard Format of Specification-Type Files

### 2.1 Three Required Elements

| Element | Description | Why It's Required |
|:---|:---|:---|
| **Field Constraint Table** | Each field's name, type, required status, scope, and example | Precise constraints, unambiguous; foundation for automated verification |
| **Format Validation Rules** | How to verify format compliance | Enables automated checks, reducing manual review costs |
| **Version Compatibility Notes** | Version change log, compatibility requirements | When the specification evolves, users know which changes require adaptation |

> Why three elements: The Field Constraint Table defines "what it is," the Format Validation Rules define "how to check," and the Version Compatibility Notes define "how to evolve." Fewer than three cannot fully define a specification; more than three reduces information density.

### 2.2 Format Example

```markdown
## Field Specification

| Field | Required | Type | Constraint | Example |
|:---|:---:|:---|:---|:---|
| name | MUST | string | <= 64 chars, kebab-case, a-z/0-9/- | python-code-inspector |
| description | MUST | string | <= 1024 chars, starts with "Use when..." | Use when reviewing Python code... |
| type | MUST | string | Fixed value "prompt" | prompt |

## Format Validation Rules

- **MUST** validate name conforms to kebab-case: regex `^[a-z0-9]+(-[a-z0-9]+)*$`
- **MUST** validate description <= 1024 chars: `len(description) <= 1024`
- **MUST** validate frontmatter is at the very top of the file, no blank lines before `---`

## Version Compatibility

| Version | Change Description | Compatibility |
|:---|:---|:---:|
| v1.0 | Initial version | -- |
| v1.1 | Added compatibility field | Backward-compatible |
| v2.0 | Removed type field, now auto-inferred | Incompatible, upgrade required |
```

---

## 3. Generation Method (ur-skill Special Notes)

> This SKILL is a "SKILL for designing SKILLs" (ur-skill) and has no historical project accumulation.
> Therefore, specification-type files are not "collected from historical specifications" but "dynamically researched and generated based on the core scenarios of the generated SKILL."

### 3.1 Generation Based on Web Research

When using this SKILL to generate a specific SKILL, follow these steps to generate specifications:

1. **Identify the specification domain**: Extract the domain requiring standardization from user requirements (e.g., frontmatter, API interfaces, data formats)
2. **Research industry standards via web search**: Search for standard specifications, best practices, and official documentation in that domain
   - Example: Generating a REST API SKILL → Research OpenAPI specifications, RESTful API design best practices
   - Example: Generating a Python code SKILL → Research PEP 8, Google Python Style Guide

3. **Design the field constraint table**:
   - Field names: Named based on industry standards
   - Required/Optional: Determined by usage frequency
   - Type: Determined by data type
   - Constraints: Determined by industry standards (e.g., kebab-case, <= 64 chars)
   - Examples: Determined by common use cases

4. **Validate the specification**:
   - [ ] Each field has constraint conditions
   - [ ] Each constraint is verifiable (regex, count, enum, range)
   - [ ] Each constraint has a validation method
   - [ ] Version changes include compatibility notes

### 3.2 Generation Based on User Instructions

If the user provides specific specifications or existing standards:

1. **Analyze user specifications**: Extract fields, constraints, and format requirements from user descriptions
2. **Design the field constraint table**: Convert user descriptions into the "Field Name + Required + Type + Constraint + Example" structure
3. **Supplement with research**: For fields not covered by the user, supplement via web research on industry standards
4. **Validate completeness**:
   - [ ] Covers all fields mentioned by the user
   - [ ] Supplements fields not mentioned by the user but required by industry standards
   - [ ] Constraints are verifiable with no vague statements

### 3.3 ur-skill Specification Library

The specification-type files used by ur-skill itself are as follows (these are reference files for ur-skill, not reference files for the generated SKILL):

| Specification File | Specification Content |
|:---|:---|
| ../templates/metadata-spec.md | YAML frontmatter field specification |
| ../templates/rules-template.md | Rule format specification (MUST/SHOULD/MAY) |
| ../design-guides/structure-guideline.md | Information density, attention management, positive formulation |
| ../templates/workflow-template.md | Workflow steps, gates, driving directives |
| ../templates/capability-architecture-template.md | Capability Matrix, Capability Facets, three-layer relationships |
| ../design-rationale/design-rationale.md | Complexity determination, progressive loading, example-driven |
| ../templates/output-template.md | Output structure, complexity correspondence, format constraints |

> Why ur-skill needs specification-type files: When ur-skill designs a SKILL, it needs a unified standard format. These specification-type files are ur-skill's "standard library," ensuring all generated SKILLs have consistent formatting.

---

## 4. Specification-Type File Design Methodology

### 4.1 Field Constraint Table Design

Each field must include:

| Attribute | Description | Example |
|:---|:---|:---|
| **Field Name** | Field identifier | name, description, type |
| **Required** | MUST / MAY (RFC 2119) | MUST = required, MAY = optional |
| **Type** | Data type | string, number, boolean, array, object |
| **Constraint** | Precise constraint conditions | <= 64 chars, kebab-case, fixed value |
| **Example** | Valid example value | python-code-inspector |

> Why five attributes: Field name identifies the field, required defines mandatory status, type defines data structure, constraint defines valid range, and example demonstrates valid values. Fewer than five leaves constraints incomplete; more than five reduces information density.

### 4.2 Constraint Condition Design

Constraint conditions must be **verifiable**:

| Constraint Type | Verification Method | Example |
|:---|:---|:---|
| **Length Constraint** | Character count | `len(name) <= 64` |
| **Format Constraint** | Regular expression | `^[a-z0-9]+(-[a-z0-9]+)*$` |
| **Value Constraint** | Enumeration check | `type in ['prompt', 'skill', 'agent']` |
| **Range Constraint** | Numeric comparison | `0 <= priority <= 100` |
| **Structure Constraint** | Nested validation | `metadata.updated` must conform to YYYY-MM-DD |

> Why verifiable: Non-verifiable constraints (e.g., "well-formatted") are vague constraints that cannot be automatically checked. Verifiable constraints (e.g., "regex match") can be automatically verified by scripts.

### 4.3 Version Compatibility Design

Version changes must be annotated with compatibility:

| Compatibility | Description | Handling |
|:---|:---|:---|
| **Backward-Compatible** | New fields added, old fields unchanged | Old SKILLs need no modification |
| **Forward-Compatible** | Fields deleted or constraints modified | Old SKILLs must be upgraded |
| **Incompatible** | Fields renamed or types changed | Old SKILLs must be refactored |

> Why annotate compatibility: Specification-type files evolve. Without compatibility annotations, users don't know whether existing SKILLs need upgrading.

---

## 5. Specification-Type File Content Requirements

### 5.1 Content That Must Be Addressed

- **Each field MUST have constraint conditions**: Without constraints, field values cannot be validated.
- **Each constraint MUST be verifiable**: Non-verifiable constraints are vague and cannot be automatically checked.
- **Each version change MUST have a compatibility note**: Without compatibility notes, users cannot determine if upgrading is necessary.

### 5.2 Prohibited Content

- **Prohibited: Vague constraints**: Such as "well-formatted" or "appropriate length" -- must be specific, e.g., "regex match" or "<= 64 chars."
- **Prohibited: Constraints without examples**: Without examples, users don't know what a valid value looks like.
- **Prohibited: Specifications without version control**: Specifications evolve; version numbers and change logs are required.

---

## 6. Relationship with Template Files

The relationship between specification-type files and template files:

| File Type | Responsibility | Relationship |
|:---|:---|:---|
| **Specification-Type File** (metadata-spec.md) | Defines standard formats | Source: Defines "what should be done" |
| **Template File** (rules-template.md) | References specification-type files | Consumer: References constraints from specification-type files |
| **Execution File** (ur-skill.md) | Executes the specification | Executor: Generates SKILLs per specification-type files |

> Why layered: Specification-type files define standards, template files reference standards, and execution files enforce standards. When specification-type files change, template and execution files synchronize their updates.

---

## 7. Completeness Checklist

When designing a specification-type file, check each item:

- [ ] Each field has five attributes (Field Name, Required, Type, Constraint, Example)
- [ ] Each constraint is verifiable (regex, count, enum, range, structure)
- [ ] Each constraint has a validation method (script-automatable check)
- [ ] Each version change has a compatibility note (backward-compatible / forward-compatible / incompatible)
- [ ] No vague constraints (e.g., "well-formatted," "appropriate length")
- [ ] No constraints without examples
- [ ] File < 200 lines; split if exceeded
- [ ] Uses standard Markdown tables, no ASCII art lines
