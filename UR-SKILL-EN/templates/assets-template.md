# Assets File Template

> Purpose: Defines the standard structure for static resource files under a generated SKILL's assets/ directory
> Core Principle: Asset files are copyable, fillable, version-consistent static content; they are not executable
> For design methodology details, see [design-guides/assets-design-guide.md](../design-guides/assets-design-guide.md)

---

## 1. Asset Header

```markdown
# {Asset Name} Template

> Purpose: {One-sentence description of purpose}
> Version: {Version number / YYYY-MM-DD}
> Last Updated: {YYYY-MM-DD}
```

---

## 2. Template Structure

```{Structure Type}
{
  "name": "{{name}}",
  "description": "{{description}}",
  "type": "{{type}}",
  "metadata": {
    "updated": "{{updated}}"
  }
}
```

> Structure Type: JSON / XML / YAML / Markdown

---

## 3. Placeholder Definitions

| Placeholder | Type | Constraint | Required |
|:---|:---|:---|:---:|
| `{{name}}` | string | kebab-case, <= 64 chars | MUST |
| `{{description}}` | string | <= 1024 chars, starts with "Use when..." | MUST |
| `{{type}}` | string | Fixed: "prompt" / "tool" / "hybrid" | MUST |
| `{{updated}}` | string | YYYY-MM-DD format | MUST |

---

## 4. Fill Rules

- **MUST** fill all MUST placeholders; unfilled = invalid output
- **MUST** validate that filled values meet constraints
- **MAY** fill optional placeholders; unfilled placeholders retain default values
- **MUST NOT** fill invalid values

---

## 5. Version Control

| Version Strategy | Format | Applicable Scenario |
|:---|:---|:---|
| Semantic Versioning | MAJOR.MINOR.PATCH | Complex assets, frequent changes |
| Date Versioning | YYYY-MM-DD | Simple assets, infrequent changes |

---

## 6. Completeness Checklist

- [ ] Template structure is verifiable (JSON Schema / XML Schema / YAML Lint)
- [ ] All placeholders have definitions (name, type, constraint, required)
- [ ] Placeholder names follow conventions (double braces, kebab-case, semantic, unique)
- [ ] Fill rules are explicit (required/optional, validation method, default value)
- [ ] Template has a version number
- [ ] No nested placeholders
- [ ] No logic expressions
- [ ] File < 200 lines
