# Spec Design Guide

> Only teaches how to write spec-type reference files. Spec files are "standard definitions" — precise, unambiguous, and verifiable.
> To determine whether a spec file is needed, see skill-package-design-guide.md §2.

---

## §1 Standard Format

### 1.1 Three Required Elements

| Element | Description | Why Mandatory |
|:---|:---|:---|
| **Field Constraint Table** | Each field's name, type, required, range, and example | Precise constraints, foundation for automated validation |
| **Format Validation Rules** | How to verify format compliance | Can be automated via script-based checks |
| **Version Compatibility Notes** | Version change history, compatibility requirements | When the spec evolves, consumers know which changes require adaptation |

### 1.2 Format Template

```markdown
## Field Specification

| Field | Required | Type | Constraint | Example |
|:---|:---:|:---|:---|:---|
| name | MUST | string | <= 64 characters, kebab-case | python-code-inspector |
| description | MUST | string | <= 1024 characters, starts with "Use when..." | Use when reviewing... |
| type | MUST | string | Fixed value: prompt | prompt |

## Format Validation Rules

- **MUST** validate name matches kebab-case: regex `^[a-z0-9]+(-[a-z0-9]+)*$`
- **MUST** validate description <= 1024 characters
- **MUST** validate frontmatter is at the very beginning of the file, no blank lines before `---`

## Version Compatibility

| Version | Changes | Compatibility |
|:---|:---|:---:|
| v1.0 | Initial version | — |
| v1.1 | Added compatibility field | Backward compatible |
| v2.0 | Removed type field | Incompatible, requires upgrade |
```

---

## §2 Field Constraint Table Design

Each field must include five attributes:

| Attribute | Description | Example |
|:---|:---|:---|
| **Field Name** | The field's identifier | name, description |
| **Required** | MUST / MAY (RFC 2119) | MUST = required, MAY = optional |
| **Type** | Data type | string, number, boolean, array |
| **Constraint** | Precise constraint conditions | <= 64 characters, kebab-case, fixed value |
| **Example** | Valid example value | python-code-inspector |

---

## §3 Constraint Condition Design

Constraint conditions must be **verifiable**:

| Constraint Type | Validation Method | Example |
|:---|:---|:---|
| **Length Constraint** | Character count | `len(name) <= 64` |
| **Format Constraint** | Regular expression | `^[a-z0-9]+(-[a-z0-9]+)*$` |
| **Value Constraint** | Enumeration check | `type in ['prompt', 'skill']` |
| **Range Constraint** | Numeric comparison | `0 <= priority <= 100` |
| **Structure Constraint** | Nested validation | `metadata.updated` conforms to YYYY-MM-DD |

---

## §4 Checklist

- [ ] Each field has five attributes (field name, required, type, constraint, example)
- [ ] Each constraint is verifiable (regex, count, enumeration, range, structure)
- [ ] Each constraint has a validation method (can be automated via script)
- [ ] Each version change has a compatibility note (backward compatible / forward compatible / incompatible)
- [ ] No vague constraints (e.g., "well-formed," "reasonable length")
- [ ] No constraints without examples
- [ ] File < 200 lines; split if exceeded
