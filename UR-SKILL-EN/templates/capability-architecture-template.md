# Capability Architecture Template

> **Purpose**: Define the standard filling format for SKILL capability matrix and capability facets
> **Core Principle**: The capability matrix consists of capability domains, not workflow steps; capability facets target only the core domain
> **Design Methodology**: See [design-guides/capability-design-guide.md](../design-guides/capability-design-guide.md)

---

## 1. Capability Matrix

### 1.1 Core Domain

| Domain | Foundation Layer | Advanced Layer | Expert Layer | Extension Layer |
|:---|:---|:---|:---|:---|
| Core: {Core Domain Name} | {Core capability} | {Proficient application} | {Deep optimization} | {Contextual reasoning} |

### 1.2 Radiating Domains

| Domain | Foundation Layer | Advanced Layer | Expert Layer | Extension Layer |
|:---|:---|:---|:---|:---|
| A {Domain 1} | {Core capability} | {Proficient application} | {Deep optimization} | {Contextual reasoning} |
| B {Domain 2} | {Core capability} | {Proficient application} | {Deep optimization} | {Contextual reasoning} |
| C {Domain 3} | {Core capability} | {Proficient application} | {Deep optimization} | {Contextual reasoning} |
| ... | ... | ... | ... | ... |

> The number of radiating domains is determined by task analysis; recommended 3-8. See [design-guides/capability-design-guide.md §1.2](../design-guides/capability-design-guide.md).

### 1.3 Correct and Incorrect Examples

| Type | Example | Notes |
|:---|:---|:---|
| Correct | A Static Analysis / B Security Audit / C Performance Diagnosis | Professional domains; still valid after reordering |
| Incorrect | A Parse Requirements / B Retrieve Materials / C Generate Report | Workflow steps; see [design-guides/capability-design-guide.md §1.1](../design-guides/capability-design-guide.md) |

---

## 2. Capability Facets

### 2.1 Generic Template

| No. | Facet | Definition | Core Question |
|:---:|:---|:---|:---|
| Facet 1 | Efficiency & Cost | {Specific resource constraints and regulation strategy for this task} | Is the resource investment reasonable? |
| Facet 2 | Knowledge Deepening | {Specific knowledge stack required for this task -- tool names, specification names, vulnerability types, standard numbers} | Is the knowledge coverage complete? |
| Facet 3 | Risk Identification | {Specific anti-patterns and risk scenarios that may occur in this task} | What are the potential risks? |
| Facet 4 | Quality Inspection | {Specific acceptance criteria for this task's output} | Is the output quality reliable? |
| Facet 5 | Domain Fusion | {How the radiating domains complement each other without overlap in this task} | Do the domains work together? |
| Facet 6 | System-Wide Perspective | {Compatibility considerations between this task's output and upstream/downstream systems or platforms} | Has the global impact been considered? |

### 2.2 Filling Format

```
Capability Facets (Targeting Core Domain: {Core Domain Name})

Facet 1 Efficiency & Cost: {Specific resource constraints and regulation strategy for this task}
Facet 2 Knowledge Deepening: {Specific knowledge stack required for this task -- tool names, specification names, vulnerability types, standard numbers}
Facet 3 Risk Identification: {Specific anti-patterns and risk scenarios that may occur in this task}
Facet 4 Quality Inspection: {Specific acceptance criteria for this task's output}
Facet 5 Domain Fusion: {How the radiating domains complement each other without overlap in this task}
Facet 6 System-Wide Perspective: {Compatibility considerations between this task's output and upstream/downstream systems or platforms}
```

> Task anchoring requirement: Each facet MUST include specific knowledge from the core domain; generic platitudes are not allowed. See [design-guides/capability-design-guide.md §3](../design-guides/capability-design-guide.md).

### 2.3 Correct and Incorrect Examples

| Type | Example | Notes |
|:---|:---|:---|
| Correct | Facet 2 Knowledge Deepening: Master Python 3.x syntax, PEP 8 conventions, OWASP Python Top 10 | Task anchored |
| Incorrect | Facet 2 Knowledge Deepening: Master relevant domain knowledge | Generic platitude; see [design-guides/capability-design-guide.md §6](../design-guides/capability-design-guide.md) |

---

## 3. Completeness Checklist

- [ ] Capability matrix: 1 core domain, 3-8 radiating domains, determined by task analysis
- [ ] Capability matrix: Each domain has all 4 layers complete (Foundation -> Advanced -> Expert -> Extension)
- [ ] Capability matrix: Domains are capability domains, not workflow steps
- [ ] Capability matrix: Core domain and radiating domains are independent and complementary
- [ ] Capability facets: 6 facets, targeting only the core domain, not duplicated into radiating domains
- [ ] Capability facets: Each facet has a specific definition and core question
- [ ] Capability facets: Each facet is task-anchored, no generic platitudes
- [ ] No placeholder residue
- [ ] Capability matrix is not an alias for workflow steps
- [ ] Capability facets are not a substitute for capability domains
