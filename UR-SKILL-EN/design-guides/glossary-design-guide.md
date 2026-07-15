# Glossary File Design Guide

> Only teaches how to write references/glossary.md. The glossary serves as the consistency anchor for concepts within the system, eliminating ambiguity and preventing concept drift.
> For determining whether a glossary is needed, see skill-package-design-guide.md §2.

---

## §1 Standard Format

### 1.1 Four Required Elements

| Element | Description | Why Required |
|:---|:---|:---|
| **Term** | Precisely defined name | Unique identifier for retrieval and reference |
| **Definition** | Single-sentence precise definition, no ambiguity | Core; the glossary's sole value |
| **Domain** | Which concept domain the term belongs to | The same term may have different meanings in different domains |
| **Usage Example** | Actual usage within the SKILL system | Bridges abstract and concrete |

### 1.2 Format Template

```markdown
## {Term}

- **Definition**: {One-sentence precise definition, using other defined terms within the domain}
- **Domain**: {Which concept domain this term belongs to}
- **Example**: {Actual usage in SKILL body / references, 1-2 sentences}
```

### 1.3 Organization Method

Terms are grouped by **concept domain**, and within a domain, sorted by **logical dependency** (define foundational terms first, then composite terms that depend on them).

Common concept domain grouping examples:

| Concept Domain Category | Example Group Name | Applicable Scenario |
|:---|:---|:---|
| Core concepts | Core Concepts, System Entities | Define the SKILL's basic terminology |
| Execution | Workflow Steps, Execution Phases | Define process-related terms |
| Quality | Validation Nodes, Quality Standards | Define quality assurance-related terms |
| Output | Output Formats, Deliverables | Define output-related terms |

### 1.4 Numbering System

Each term is assigned a **G{sequence number}** (G = Glossary) for cross-file reference.
Example:
```markdown
## G01 Capability Matrix
...
## G02 Core Domain
...
```

---

## §2 Content Requirements

### 2.1 Required

- Each term must have a "Definition"
- Definitions use already-defined terms within the domain (prefer referencing numbered terms)
- Each term must have an "Example"

### 2.2 Prohibited

- **MUST NOT** Circular definitions (Term A depends on B, B depends on A)
- **MUST NOT** Over-definition (e.g., "a checklist is a list used for checking")
- **MUST NOT** External references replacing definitions (e.g., "see this external link for details")
- **MUST NOT** Vague qualifiers (e.g., "usually," "generally," "in most cases")

---

## §3 Checklist

- [ ] Each term has four elements (Term, Definition, Domain, Example)
- [ ] Definition is completed in one sentence, no tautology
- [ ] No circular dependencies between definitions
- [ ] Definitions of similar terms can distinguish them from each other
- [ ] Grouped by concept domain, sorted by logical dependency within domain
- [ ] Terms have G{sequence number} numbering
- [ ] Number of terms derived from research-analyst investigation analysis results
- [ ] Each term appears at least 2 times in the system (not a one-time-use word)
- [ ] No external references replacing definitions (self-contained)
- [ ] File < 200 lines; if exceeded, split
