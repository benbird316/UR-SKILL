# Structure Design Guide

> Only teaches how to organize the format symbols, information organization methods, and attention counter-strategies for SKILL.md and its companion files.
> For determining structure specification needs, see skill-package-design-guide.md §2.

---

## §1 General Format Symbols

### 1.1 Constraint Level Symbols (RFC 2119)

| Symbol | Meaning | Deviation Handling |
|:---|:---|:---|
| **MUST** | Absolute requirement | Violation = incompatible with specification |
| **MUST NOT** | Absolute prohibition | Violation = incompatible with specification |
| **SHOULD** | Strong recommendation | Deviation requires documented reason |
| **SHOULD NOT** | Not recommended | Deviation requires documented reason |
| **MAY** | Truly optional | No "deviation" concept |

### 1.2 Checklist Symbols

| Symbol | Meaning | Usage Scenario |
|:---|:---|:---|
| `- [ ]` | Unchecked | Checklists, review items |
| `- [x]` | Checked | Checklist completion marker |
| `1. 2. 3.` | Step numbering | Workflow sequences |
| `Rule 01` | Rule numbering | Rule references |
| `Anti-pattern 1` | Anti-pattern numbering | Anti-pattern references |
| `Risk Boundary-01` | Risk boundary numbering | Risk boundary declaration references |

### 1.3 Emphasis Symbols

| Symbol | Meaning | Usage Scenario |
|:---|:---|:---|
| `**bold**` | Key constraints | Rule keywords, checklist core terms |
| `> Blockquote` | Core principles | Principle content that needs emphasis |
| `` `inline code` `` | Format examples | File paths, configuration items |
| ` ``` ` Code block | Full examples | YAML frontmatter, configuration templates |
| `---` | Section separator | YAML frontmatter separator, section division |

### 1.4 Symbols NOT Used

- **No emoji** as constraint markers (in rule keywords, checklist core terms, gate conditions) — cannot be parsed by all terminals
- **SHOULD** use emoji on demand in output templates/report examples (e.g., issue grading 🔴🟠🟡🟢) to improve visual distinction, but MUST NOT use in constraint rules
- **No Unicode special symbols** (e.g., ◈): encoding risk, no industry counterpart
- **No ASCII art table lines** (├ ┌ ┬): Markdown standard tables `|` suffice

---

## §2 Information Organization Methods

### 2.1 One-Dimensional Information: Use Lists

- Rule declarations: bullet list, each item independent, starting with RFC 2119 keyword
- Step sequences: numbered list `1. -> 2. -> 3.`
- Checklists: `- [ ]` checkboxes

### 2.2 Two-Dimensional Information: Use Tables

Two-dimensional relationships (comparisons, mappings, budget allocations) use standard Markdown tables `| col1 | col2 | col3 |`.

### 2.3 Hierarchical Progression

- **L1 Overview**: 1-2 sentences at paragraph start, stating file purpose and core principles
- **L2 Module**: `##` level-2 headings, dividing independent topics
- **L3 Entry**: Lists or tables, specific specification entries
- **L4 Detail**: Moved into `references/`, not expanded in the body

---

## §3 Positive Statements

| Counterexample (Negative/Abstract) | Positive Example (Affirmative/Concrete) |
|:---|:---|
| Must not lose original semantics | **MUST** preserve original semantics |
| Prohibit generating executable code | **MUST NOT** embed executable code in body |
| Cannot directly fill in examples | **MUST NOT** copy examples directly into the body |
| Must not use internal terminology | **MUST NOT** use internal terminology in the body |

---

## §4 Attention Counter-Strategies

### 4.1 Positioning Strategy (Countering Lost in the Middle)

- File opening: Place core capability summary + key constraints
- File ending: Place checklist + key limitations + version information
- Avoid: Placing key rules in the middle section of the body

### 4.2 Repetition Strategy (Countering Attention Dilution)

- Core rules declared in the rules section, referenced by number in the workflow
- Key output formats defined in specifications, demonstrated in examples
- Different phrasing, avoid verbatim repetition

### 4.3 Signal Reinforcement

- Key constraints use `**bold**`
- Core principles use `> Blockquote`
- Format examples use ` ``` ` code blocks
- Rules / gates / anti-patterns use numbering system

### 4.4 Body Section Recommended Order (Dual Anchoring Strategy)

| Section | Position | Content | Reason |
|:---|:---|:---|:---|
| **Primacy Zone** | Body first 20% | Role declaration, task definition, core constraints (MUST/MUST NOT) | Highest attention, determines behavioral baseline |
| **Middle Zone** | Body middle 60% | Capability matrix, workflow steps | Lost in the Middle risk zone, place indexes and reference paths |
| **Recency Zone** | Body last 20% | Output format contract, key rule summary, risk boundary declarations, reference paths | Second-highest attention, core rule repetition increases capture probability |

**Double Prompting Strategy**: In the recency zone, **rephrase** (not verbatim copy) the core constraints from the primacy zone using different wording.

---

## §5 Information Density

Maintain high information density: delete formulaic filler, avoid redundant declarations, each sentence conveys independent information.

**Detection Methods**:
- Delete formulaic prefixes like "It is well known that," "It should be noted that"
- Delete duplicate declarations (e.g., rules written out in full in the workflow should reference the number instead)
- Delete transitional sentences with no information increment
- Check whether every paragraph has independent information value

**No Numerical Threshold**: Information density is a design principle; use inspection methods instead of imprecise numerical thresholds.

---

## §6 Checklist

- [ ] Rules use RFC 2119 keywords (MUST / MUST NOT / SHOULD / SHOULD NOT / MAY)
- [ ] One-dimensional information uses lists, two-dimensional information uses tables
- [ ] Hierarchical progression: L1 Overview -> L2 Module -> L3 Entry -> L4 Detail
- [ ] No self-created symbols (emoji, Unicode special symbols, ASCII art table lines)
- [ ] Positive statements: MUST / SHOULD / MAY replace "must not / prohibit / must"
- [ ] Key information repeated or referenced at the beginning and end
- [ ] No abstract rules (e.g., "do good work")
- [ ] No contradictory rules (e.g., Rule 01 says MUST A, Rule 02 says MUST NOT A)
- [ ] Rules, gates, anti-patterns, risk boundaries, and professional boundaries have separate responsibilities with no overlap
- [ ] Gate check items reference rule numbers, do not repeat rule content
