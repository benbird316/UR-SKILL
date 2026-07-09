# Structure Guideline

> Purpose: Define format symbols, information organization methods, and attention management strategies for SKILL.md and its companion files
> Core principle: Specifications are "how to" not "what the goal is"; follow RFC 2119; align with industry Markdown standards

---

## 1. Common Format Symbols

The format symbols used in this document are all derived from Markdown standards or RFC 2119, with no proprietary symbols introduced.

### 1.1 Constraint Level Symbols (RFC 2119)

| Symbol | Meaning | Source | Deviation Handling |
|:---|:---|:---|:---|
| **MUST** | Absolute requirement | RFC 2119 | Violation = incompatible with specification |
| **MUST NOT** | Absolute prohibition | RFC 2119 | Violation = incompatible with specification |
| **SHOULD** | Strongly recommended | RFC 2119 | Deviation requires documented justification |
| **SHOULD NOT** | Discouraged | RFC 2119 | Deviation requires documented justification |
| **MAY** | Truly optional | RFC 2119 | No deviation concept |

> For core principles, see [design-rationale/design-rationale.md Section 6](../design-rationale/design-rationale.md#L75). In brief: RFC 2119 keywords in ALL CAPS carry precise semantics and can be mechanically parsed by tools.

### 1.2 Check Symbols

| Symbol | Meaning | Usage Scenario |
|:---|:---|:---|
| `- [ ]` | Unchecked | Checklist, inspection items |
| `- [x]` | Checked | Checklist completion marker |
| `1.` `2.` `3.` | Step numbering | Workflow sequence |
| `Rule01` `Rule02` | Rule numbering | Rule references |
| `Anti-pattern1` `Anti-pattern2` | Anti-pattern numbering | Anti-pattern references |
| `Gate1` `Gate2` | Gate numbering | Gate checkpoint references |
| `Risk Boundary-01` | Risk boundary numbering | Risk boundary declaration references |

> Why use a numbering system: Enables cross-section referencing; gate checks reference rule numbers rather than duplicating content.

### 1.3 Emphasis Symbols

| Symbol | Meaning | Usage Scenario |
|:---|:---|:---|
| `**Bold**` | Key constraint | Rule keywords, core words in check items |
| `> Blockquote` | Core principle | Principled content requiring emphasis |
| `` `Inline Code` `` | Format example | File paths, configuration items |
| ` ``` ` Code Block | Full example | YAML frontmatter, configuration templates |
| `---` | Module separator | YAML frontmatter delimiter, section separator |

### 1.4 Symbols Not Used

The following symbols are NOT used in this system, to avoid increasing cognitive load and encoding risk:

- **No emoji (red circle, yellow circle, green circle) as constraint markers**: Cannot be parsed by all terminals; no unified semantics
- **No Unicode special symbols (e.g., lozenge)**: Encoding risk, no industry correspondence, cannot be parsed by tools
- **No ASCII art table lines (box-drawing characters)**: Standard Markdown tables `|` are sufficient; ASCII art adds noise

---

## 2. Information Organization Methods

### 2.1 One-Dimensional Information Uses Lists

**What is one-dimensional information**: Step sequences, rule declarations, checklists, single-attribute lists.

**How to do it**:
- Rule declarations: bullet list, each item independent, starting with RFC 2119 keywords
- Step sequences: numbered list `1. → 2. → 3.`
- Checklists: `- [ ]` checkboxes

**Why**: Tables add format noise (separator lines, alignment lines, etc. occupy a significant proportion); lists have higher information density and are the Markdown standard.

### 2.2 Two-Dimensional Information Uses Tables

**What is two-dimensional information**: Mapping relationships between two dimensions, such as comparisons, gate mappings, and budget allocations.

**How to do it**: Use standard Markdown tables `| col1 | col2 | col3 |`.

**Why**: Two-dimensional relationships are clear at a glance with tables, but this only applies to truly two-dimensional information. Forcing one-dimensional information into tables reduces density.

**Lead by example**: Section 1.1 of this document presents constraint levels as two-dimensional (symbol x meaning) using a table; Section 2.1's list practices are explanatory text using a bullet list.

### 2.3 Hierarchical Progression

**How to do it**:
- L1 Overview: 1-2 opening sentences stating file purpose and core principles
- L2 Modules: `##` second-level headings dividing independent topics
- L3 Items: Lists or tables, specific specification entries
- L4 Details: Moved into `references/`, not expanded in body

**Why**: Progressive loading -- body retains only the skeleton, details loaded on demand, controlling token consumption.

---

## 3. Positive Formulation

### 3.1 Hard Constraints

**How to do it**: Start with **MUST** / **MUST NOT**, specific and actionable, avoid abstraction.

**Counterexample → Correct Example**:

| Counterexample (Negative/Abstract) | Correct Example (Positive/Specific) |
|:---|:---|
| Do not lose the original semantics | **MUST** preserve the original semantics |
| Prohibit generating executable code | **MUST NOT** embed executable code in body |
| Cannot directly fill in examples | **MUST NOT** copy examples directly into body |
| Internal terminology must not appear | **MUST NOT** use internal terminology in body |

### 3.2 Strong Preferences

**How to do it**: Start with **SHOULD** / **SHOULD NOT**, document justification for exceptions.

**Counterexample → Correct Example**:

| Counterexample | Correct Example |
|:---|:---|
| Avoid format conflicts | **SHOULD** ensure format consistency |
| Do not skip any steps | **SHOULD** execute each step in order |
| Avoid information redundancy | **SHOULD** control information density, remove patterned fillers |
| Do not over-infer | **SHOULD NOT** infer beyond user input |

### 3.3 Optional

**How to do it**: Start with **MAY**, truly optional, no obligation and no impact.

---

## 4. Attention Management Strategies

### 4.1 Position Strategy (Countering Lost in the Middle)

> For core principles, see [design-rationale/design-rationale.md Section 5](../design-rationale/design-rationale.md#L64)

**How to do it**:
- File opening: Place core capability summary + key constraints
- File closing: Place checklists + key limitations + version information
- Avoid: Placing critical rules in the middle of the body

### 4.2 Repetition Strategy (Countering Attention Dilution)

**How to do it**:
- Core rules are declared in the rules section and referenced by number in the workflow
- Key output formats are defined in specifications and demonstrated in examples
- Use different phrasing, avoid verbatim repetition

**Why**: Key information appearing in different positions and different forms increases the probability of capture, while avoiding the attention fatigue caused by verbatim repetition.

### 4.3 Segmentation Strategy (Countering Context Rot)

> For core principles, see [design-rationale/design-rationale.md Section 5](../design-rationale/design-rationale.md#L64)

**How to do it**:
- Body exceeds 500 lines → split content into `references/`
- `references/` file exceeds 200 lines → split into multiple smaller files
- A single table has too many rows → split into multiple tables or groups
- A single list has too many items → group or split into sublists

> The 500-line / 200-line thresholds correspond to the L2 / L3 token budget thresholds in design-rationale/design-rationale.md.

### 4.4 Signal Reinforcement

**How to do it**:
- Key constraints use `**bold**`
- Core principles use `> blockquote`
- Format examples use ` ``` ` code blocks
- Rules / Gates / Anti-patterns use numbering systems (Rule01, Gate1, Anti-pattern1)

**Why**: Standardized markers reduce cognitive load and improve parsability. Bold and blockquote are Markdown standards renderable on any platform.

### 4.5 Recommended Body Block Ordering (Dual Anchoring Strategy)

Leveraging the LLM's U-shaped attention curve (primacy effect + recency effect), body content is allocated by attention zone:

| Zone | Position | What to Place | Reason |
|:---|:---|:---|:---|
| **Primacy Zone** | First 20% of body | Role declaration, task definition, core constraints (MUST/MUST NOT) | Highest attention, sets the model's behavioral tone |
| **Middle Zone** | Middle 60% of body | Capability Matrix, Capability Facets, workflow steps | Lost in the Middle risk zone; place indexes and reference paths |
| **Recency Zone** | Last 20% of body | Output format contract, key rule summary (Double Prompting), risk boundary declarations, reference paths | Second-highest attention; repeating core rules at the end increases capture probability |

**Double Prompting Strategy** (zero-cost enhancement):
- In the Recency Zone, **repeat with different phrasing** the core constraints from the Primacy Zone (do not write verbatim copies)
- Example: Primacy Zone states "MUST NOT confuse Capability Matrix with workflow steps," Recency Zone states "Rule Rule15: Prohibit Architecture Confusion (Anti-pattern4)"

> For core principles, see [design-rationale/design-rationale.md Section 5](../design-rationale/design-rationale.md#L64)

**Counterexample**:
- Wrong: Placing rules (MUST/MUST NOT) in the middle of the body → the zone most prone to loss
- Wrong: Placing Capability Matrix details in the Primacy Zone → consumes valuable attention resources
- Wrong: Ending with only "References" without repeating core constraints → wastes the Recency Zone

> References: Liu et al., "Lost in the Middle" (ACL 2024); Google Research, "Double Prompting" (2025)

---

## 5. Information Density

### 5.1 Principle

Maintain high information density: remove patterned fillers, avoid redundant declarations, ensure each sentence conveys independent information.

### 5.2 Detection Methods

- Remove patterned prefixes such as "as we all know," "it should be noted that"
- Remove duplicate declarations (e.g., rules whose content is repeated verbatim in the workflow -- reference by number instead)
- Remove transitional sentences with no information increment
- Check whether each paragraph has independent informational value

### 5.3 Why Not Use Numeric Thresholds

Information density is a design principle, not a quantifiable metric. There are no universally accepted calculation formulas in the text domain (entropy methods, compression ratios, and effective-word ratios are all influenced by format and corpus). Qualitative descriptions are more reliable than arbitrary numbers.

---

## 6. Structure Checklist

After generating a SKILL, check each item:

- [ ] Rules use RFC 2119 keywords (MUST / MUST NOT / SHOULD / SHOULD NOT / MAY)
- [ ] One-dimensional information uses lists, two-dimensional information uses tables
- [ ] Hierarchical progression: L1 Overview → L2 Modules → L3 Items → L4 Details
- [ ] No proprietary symbols (emoji, Unicode special symbols, ASCII art table lines)
- [ ] Positive formulation: MUST / SHOULD / MAY replace "do not / prohibit / must"
- [ ] Key information repeated or referenced in opening and closing sections
- [ ] No abstract rules (e.g., "do good work")
- [ ] No contradictory rules (e.g., Rule01 says MUST A, Rule02 says MUST NOT A)
- [ ] Rules, Gates, Anti-patterns, and Risk Boundaries have separated responsibilities with no overlap
- [ ] Gate checks reference rule numbers, not duplicate rule content
