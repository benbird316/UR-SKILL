# Capability Architecture Template

> Purpose: Defines the standard fill-in format for SKILL capability matrix and capability facets
> Core principle: The capability matrix contains capability domains, not workflow steps; capability facets apply only to the core domain
> Design methodology: see [design-guides/capability-design-guide.md](../design-guides/capability-design-guide.md)

---

## 1. Capability Matrix

### 1.1 Core Domain

| Domain | Foundation Tier | Intermediate Tier | Advanced Tier | Extension Tier |
|:---|:---|:---|:---|:---|
| Core: {Core Domain Name} | {Core capability} | {Proficient application} | {Deep optimization} | {Contextual reasoning} |

### 1.2 Radiating Domains

| Domain | Foundation Tier | Intermediate Tier | Advanced Tier | Extension Tier |
|:---|:---|:---|:---|:---|
| A {Domain 1} | {Core capability} | {Proficient application} | {Deep optimization} | {Contextual reasoning} |
| B {Domain 2} | {Core capability} | {Proficient application} | {Deep optimization} | {Contextual reasoning} |
| C {Domain 3} | {Core capability} | {Proficient application} | {Deep optimization} | {Contextual reasoning} |
| ... | ... | ... | ... | ... |

> The number of radiating domains is determined by task analysis; 3-8 recommended. See [design-guides/capability-design-guide.md section 1.2](../design-guides/capability-design-guide.md).

### 1.3 Positive and Negative Examples

| Type | Example | Notes |
|:---|:---|:---|
| Positive | A Static Analysis / B Security Audit / C Performance Diagnostics | Professional domains; still valid when reordered |
| Negative | A Parse Requirements / B Retrieve Materials / C Generate Report | Workflow steps; see [design-guides/capability-design-guide.md section 1.1](../design-guides/capability-design-guide.md) |

---

## 2. Capability Facets

### 2.1 Generic Template

| No. | Facet | Definition | Core Question |
|:---:|:---|:---|:---|
| Facet 1 | Efficiency & Cost | {Specific resource constraints and adjustment strategies for this task} | Is the resource investment reasonable? |
| Facet 2 | Deep Knowledge | {Specific knowledge stack required for this task -- tool names, spec names, vulnerability types, standard numbers} | Is the knowledge coverage complete? |
| Facet 3 | Risk Identification | {Specific anti-patterns and risk scenarios that may arise in this task} | What are the potential risks? |
| Facet 4 | Quality Verification | {Specific acceptance criteria for this task's output} | Is the output quality reliable? |
| Facet 5 | Domain Integration | {How the radiating domains for this task complement each other without overlap} | Are the domains synergistic? |
| Facet 6 | System Holistics | {Compatibility considerations for this task's output with upstream/downstream systems and platforms} | Has the global impact been considered? |

### 2.2 Fill-in Format

```
Capability Facets (targeting core domain: {Core Domain Name})

Facet 1 Efficiency & Cost: {Specific resource constraints and adjustment strategies for this task}
Facet 2 Deep Knowledge: {Specific knowledge stack required for this task -- tool names, spec names, vulnerability types, standard numbers}
Facet 3 Risk Identification: {Specific anti-patterns and risk scenarios that may arise in this task}
Facet 4 Quality Verification: {Specific acceptance criteria for this task's output}
Facet 5 Domain Integration: {How the radiating domains for this task complement each other without overlap}
Facet 6 System Holistics: {Compatibility considerations for this task's output with upstream/downstream systems and platforms}
```

> Task-anchoring requirement: Each facet MUST contain specific knowledge for the core domain; cannot use only generic boilerplate. See [design-guides/capability-design-guide.md section 3](../design-guides/capability-design-guide.md).

### 2.3 Positive and Negative Examples

| Type | Example | Notes |
|:---|:---|:---|
| Positive | Facet 2 Deep Knowledge: Master Python 3.x syntax, PEP 8 conventions, OWASP Python Top 10 | Task-anchored |
| Negative | Facet 2 Deep Knowledge: Master relevant domain knowledge | Generic boilerplate; see [design-guides/capability-design-guide.md section 6](../design-guides/capability-design-guide.md) |

---

## 3. Completeness Checklist

- [ ] Capability matrix: 1 core domain, 3-8 radiating domains, determined by task analysis
- [ ] Capability matrix: Each domain has all 4 tiers complete (Foundation -> Intermediate -> Advanced -> Extension)
- [ ] Capability matrix: Domains are capability domains, not workflow steps
- [ ] Capability matrix: Core domain and radiating domains are independent yet complementary
- [ ] Capability facets: 6 facets, targeting only the core domain, not duplicated across radiating domains
- [ ] Capability facets: Each facet has a specific definition and core question
- [ ] Capability facets: Each facet is task-anchored, free of generic boilerplate
- [ ] No placeholder residue
- [ ] Capability matrix is not an alias for workflow steps
- [ ] Capability facets are not a substitute for capability domains
