# Assets Design Guide

> Only teaches how to write static resources under assets/. Asset files are static content that is reproducible, fillable, and version-consistent.
> To determine whether an asset file is needed, see skill-package-design-guide.md §2.

---

## §1 Standard Format

### 1.1 Three Required Elements

| Element | Description | Why Mandatory |
|:---|:---|:---|
| **Template Structure** | The overall structure of the file | Defines the output format and ensures consistency |
| **Placeholder Definitions** | Fillable variables/placeholders | Defines which parts can be dynamically filled |
| **Fill Rules** | Rules for filling placeholders | Defines the constraints and validation when filling |

### 1.2 Format Template

```markdown
# {Resource Name} Template

> Purpose: {One-line description of purpose}
> Version: {Version Number}
> Last Updated: {Date}

---

## Template Structure

```json
{
  "name": "{{name}}",
  "description": "{{description}}"
}
```

## Placeholder Definitions

| Placeholder | Type | Constraint | Required |
|:---|:---|:---|:---:|
| `{{name}}` | string | kebab-case, <= 64 characters | MUST |
| `{{description}}` | string | <= 1024 characters | MUST |

## Fill Rules

- **MUST** fill all MUST placeholders; unfilled placeholders render the output invalid
- **MUST** validate that fill values satisfy constraints
- **MAY** fill optional placeholders; unfilled placeholders retain default values
- **MUST NOT** fill illegal values
```

---

## §2 Placeholder Design

| Naming Convention | Description | Example |
|:---|:---|:---|
| **Double Braces** | `{{placeholder}}` | Compatible with Mustache / Handlebars |
| **kebab-case** | Lowercase + hyphens | `{{output-format}}` |
| **Semantic** | Name reflects content | `{{name}}` not `{{n}}` |
| **Uniqueness** | No duplicate definitions | Do not define two `{{name}}` in the same template |

---

## §3 Version Control

| Version Strategy | Description | Applicable Scenarios |
|:---|:---|:---|
| **Semantic Versioning** | MAJOR.MINOR.PATCH | Complex resources, frequent changes |
| **Date Versioning** | YYYY-MM-DD | Simple resources, low-frequency changes |
| **Hash Versioning** | Git commit hash | Resources under development, frequent iteration |

---

## §4 Checklist

- [ ] Template structure is verifiable (JSON Schema / XML Schema / YAML Lint)
- [ ] All placeholders have definitions (name, type, constraint, required)
- [ ] Placeholder naming follows conventions (double braces, kebab-case, semantic, unique)
- [ ] Fill rules are explicit (required/optional, validation method, default values)
- [ ] Template has a version number (semantic versioning / date versioning / hash versioning)
- [ ] No nested placeholders
- [ ] No logical expressions
- [ ] File < 200 lines; split if exceeded
