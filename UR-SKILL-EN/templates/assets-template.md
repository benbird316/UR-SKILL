# Asset File Template

> **Purpose**: Define the standard structure for static resource files under the generated SKILL's assets/ directory
> **Core Principle**: Asset files are static content that can be copied, filled, and version-consistent; they are not executable
> **Design Methodology**: See [design-guides/assets-design-guide.md](../design-guides/assets-design-guide.md)

---

## 1. Asset Header Information

```markdown
# {Resource Name} Template

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
| `{{name}}` | string | kebab-case, <= 64 characters | MUST |
| `{{description}}` | string | <= 1024 characters, start with "Use when..." | MUST |
| `{{type}}` | string | Fixed "prompt" / "tool" / "hybrid" | MUST |
| `{{updated}}` | string | YYYY-MM-DD format | MUST |

---

## 4. Filling Rules

- **MUST** fill all MUST placeholders; unfilled output is invalid
- **MUST** validate that filled values meet constraints
- **MAY** fill optional placeholders; unfilled ones retain default values
- **MUST NOT** fill illegal values

---

## 5. Version Control

| Version Strategy | Format | Applicable Scenario |
|:---|:---|:---|
| Semantic versioning | MAJOR.MINOR.PATCH | Complex resources, frequent changes |
| Date versioning | YYYY-MM-DD | Simple resources, low-frequency changes |

---

## 6. Completeness Checklist

- [ ] Template structure is validatable (JSON Schema / XML Schema / YAML Lint)
- [ ] All placeholders have definitions (name, type, constraint, required)
- [ ] Placeholder naming follows conventions (double curly braces, kebab-case, semantic, unique)
- [ ] Filling rules are clear (required/optional, validation method, default values)
- [ ] Template has a version number
- [ ] No nested placeholders
- [ ] No logical expressions
- [ ] File < 200 lines
