# Asset-Type File Design Guide

> Purpose: Define the design methodology for static assets (templates, schemas, brand materials) under the assets/ directory
> Core principle: Asset-type files are copyable, fillable, version-consistent static content

---

## 1. Why an Asset-Type File Design Guide Is Needed

The assets/ directory stores static resources:
- Output templates (JSON schema, XML templates, Markdown templates)
- Brand materials (logos, color schemes, typography specifications)
- Configuration files (YAML configs, JSON configs, environment variable templates)

Unlike scripts, asset-type files:
- **Non-executable**: No logic, only data
- **Fillable**: Contain placeholders, filled at runtime
- **Copyable**: Reusable across multiple SKILLs

If asset-type files are not defined:
- Output formats are inconsistent
- Brand style is chaotic
- Configurations are redundantly defined

Asset-type files are **asset-type reference files** (L3), loaded on demand. When generating SKILL output, asset-type files are loaded and their content filled.

---

## 2. Standard Format of Asset-Type Files

### 2.1 Three Required Elements

| Element | Description | Why It's Required |
|:---|:---|:---|
| **Template Structure** | The overall structure of the file | Defines output format, ensures consistency |
| **Placeholder Definitions** | Fillable variables/placeholders | Defines which parts can be dynamically filled |
| **Fill Rules** | Rules for filling placeholders | Defines constraints and validation during filling |

> Why three elements: The Template Structure defines "what it looks like," the Placeholder Definitions define "what can vary," and the Fill Rules define "how it varies." Fewer than three cannot fully define the asset; more than three reduces information density.

### 2.2 Format Example

```markdown
# {Asset Name} Template

> Purpose: {One-sentence description of purpose}
> Version: {Version Number}
> Last Updated: {Date}

---

## Template Structure

```json
{
  "name": "{{name}}",
  "description": "{{description}}",
  "type": "{{type}}",
  "metadata": {
    "updated": "{{updated}}"
  }
}
```

## Placeholder Definitions

| Placeholder | Type | Constraint | Required |
|:---|:---|:---|:---:|
| `{{name}}` | string | kebab-case, <= 64 chars | MUST |
| `{{description}}` | string | <= 1024 chars, starts with "Use when..." | MUST |
| `{{type}}` | string | Fixed value "prompt" | MUST |
| `{{updated}}` | string | YYYY-MM-DD format | MUST |

## Fill Rules

- **MUST** fill all MUST placeholders; output is invalid if unfilled
- **MUST** validate that filled values conform to constraints (e.g., name conforms to kebab-case)
- **MAY** fill optional placeholders; retain default if unfilled
- **MUST NOT** fill illegal values (e.g., name containing uppercase letters)
```

---

## 3. Generation Method (ur-skill Special Notes)

> This SKILL is a "SKILL for designing SKILLs" (ur-skill) and has no historical project accumulation.
> Therefore, asset-type files are not "collected from historical templates" but "dynamically designed based on the core scenarios of the generated SKILL."

### 3.1 Generation Based on Scenario Requirements

When using this SKILL to generate a specific SKILL, follow these steps to generate asset-type files:

1. **Determine asset requirements**: Extract whether templates, schemas, and configuration files are needed from user requirements
   - Simple SKILL: Usually no asset-type files needed (output format simple, no templates required)
   - Medium SKILL: May need 1-2 templates (JSON schema, Markdown template)
   - Complex SKILL: May need 3-5 assets (multiple output formats, brand materials, configuration files)

2. **Design template structure**:
   - Determine output format (JSON / XML / YAML / Markdown)
   - Design overall template structure (fields, nesting, arrays)
   - Define placeholders (which parts can be dynamically filled)

3. **Define fill rules**:
   - Required placeholders: output invalid if unfilled
   - Optional placeholders: retain default if unfilled
   - Validation rules: filled values must conform to constraints (e.g., kebab-case, <= 64 chars)

4. **Validate asset-type files**:
   - [ ] Template structure is verifiable (JSON Schema / XML Schema / YAML Lint)
   - [ ] All placeholders have definitions (name, type, constraint, required)
   - [ ] Placeholder naming conforms to conventions (double curly braces, kebab-case, semantic)
   - [ ] Fill rules are clear (required/optional, validation method, default values)

### 3.2 Generation Based on User Instructions

If the user provides specific templates or existing assets:

1. **Analyze user assets**: Extract template structure, placeholders, and fill rules from user descriptions
2. **Design asset-type files**: Convert user descriptions into the "Template Structure + Placeholder Definitions + Fill Rules" structure
3. **Supplement design**: For placeholders not covered by the user, supplement based on the scenario
4. **Validate completeness**:
   - [ ] Covers all placeholders mentioned by the user
   - [ ] Supplements placeholders not mentioned by the user but needed by the scenario
   - [ ] Template has a version number for tracking changes

### 3.3 ur-skill Asset Templates

The asset-type files used by ur-skill itself are as follows (these are reference files for ur-skill, not reference files for the generated SKILL):

| Asset File | Purpose | Complexity |
|:---|:---|:---:|
| YAML frontmatter template in ../templates/output-template.md | Generate SKILL frontmatter structure | All complexity levels |
| Capability Matrix table template in ../templates/capability-architecture-template.md | Generate standard capability matrix format | All complexity levels |
| Workflow step template in ../templates/workflow-template.md | Generate standard workflow format | All complexity levels |
| Rule list template in ../templates/rules-template.md | Generate standard rule format | All complexity levels |
| JSON schema (validate generated SKILL frontmatter) | Automate frontmatter format validation | Complex |

> Why ur-skill needs asset-type files: When ur-skill designs a SKILL, it needs a unified template structure. These asset-type files are ur-skill's "template library," ensuring all generated SKILLs have consistent structure.

---

## 4. Asset-Type File Design Methodology

### 4.1 Template Design

Templates must be **verifiable**:

| Verification Item | Method | Why |
|:---|:---|:---|
| **Structure Verification** | JSON Schema / XML Schema / YAML Lint | Ensures the template itself has correct format |
| **Placeholder Verification** | Regex scan for `{{.*?}}` | Ensures all placeholders have definitions |
| **Fill Verification** | Validate output format after filling | Ensures filled output is valid |
| **Version Verification** | Version number match | Ensures the correct version of the template is used |

### 4.2 Placeholder Design

Placeholder naming conventions:

| Naming Convention | Description | Example |
|:---|:---|:---|
| **Double Curly Braces** | `{{placeholder}}` | Compatible with Mustache / Handlebars template engines |
| **kebab-case** | Lowercase + hyphens | `{{output-format}}` |
| **Semantic** | Name reflects content | `{{name}}` not `{{n}}` |
| **Uniqueness** | No duplicate definitions | Do not define two `{{name}}` in the same template |

> Why double curly braces: Mustache / Handlebars are industry-standard template engines; double curly braces `{{}}` are the standard placeholder syntax. Single curly braces `{}` may be confused with JSON objects.

### 4.3 Version Control

Asset-type files must have version control:

| Version Strategy | Description | Applicable Scenario |
|:---|:---|:---|
| **Semantic Versioning** | MAJOR.MINOR.PATCH | Complex assets, frequent changes |
| **Date Versioning** | YYYY-MM-DD | Simple assets, infrequent changes |
| **Hash Versioning** | Git commit hash | In-development assets, frequent iteration |

> Why version control: Asset-type files evolve. Without version control, users don't know which version to use, which may cause output format errors after filling.

---

## 5. Asset-Type File Content Requirements

### 5.1 Content That Must Be Addressed

- **Each placeholder MUST have constraints**: Without constraints, filled values cannot be validated.
- **Each placeholder MUST have a required/optional marker**: Without markers, users don't know which must be filled.
- **Templates MUST have version numbers**: Without version control, evolution cannot be tracked.

### 5.2 Prohibited Content

- **Prohibited: Placeholders without constraints**: Such as `{{content}}` with no type or length constraints.
- **Prohibited: Nested placeholders**: Such as `{{{{name}}}}`, which increases parsing complexity.
- **Prohibited: Logic expressions**: Asset-type files are static templates and should not contain conditionals, loops, or other logic.

---

## 6. Synergy with Output Templates

The relationship between asset-type files and output-template.md:

| File | Responsibility | Relationship |
|:---|:---|:---|
| **output-template.md** | Defines output structure (simple/medium/complex) | Source: Defines "what assets are needed" |
| **assets/{template}.json** | Provides specific template content | Consumer: Referenced by output-template.md |
| **assets/{schema}.yaml** | Provides validation schema | Validator: Validates filled output compliance |

> Why layered: output-template.md defines "what is needed," and assets/ provides "what specifically it is." When output-template.md changes, assets/ synchronizes its updates.

---

## 7. Completeness Checklist

When designing asset-type files, check each item:

- [ ] Template structure is verifiable (JSON Schema / XML Schema / YAML Lint)
- [ ] All placeholders have definitions (name, type, constraint, required)
- [ ] Placeholder naming conforms to conventions (double curly braces, kebab-case, semantic, unique)
- [ ] Fill rules are clear (required/optional, validation method, default values)
- [ ] Template has version number (semantic versioning / date versioning / hash versioning)
- [ ] No nested placeholders
- [ ] No logic expressions
- [ ] File < 200 lines; split if exceeded
- [ ] Uses standard Markdown tables, no ASCII art lines
