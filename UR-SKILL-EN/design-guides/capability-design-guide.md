# Capability Architecture Design Guide

> Purpose: Explains how to design capability matrices, capability facets, and boundary declarations. Answers "why design it this way" and "how to determine if the design is correct."
> Core Principle: The capability matrix represents capability domains, not workflow steps; capability facets apply only to the core domain; boundary declarations are divided into safety red lines and scope protection.

---

## 1. The Capability Matrix Represents Capability Domains, Not Workflow Steps

> Core rationale: see [design-rationale/design-rationale.md SS1](../design-rationale/design-rationale.md#L8)

### 1.1 Key Differentiation Method

Use the Ordering Test and Three-Question Screening to determine whether a candidate domain is a capability domain or a workflow step.

**Ordering Test**: Rearrange the candidate radiating domains. If the logic collapses, they are workflow steps.

**Three-Question Screening**: For each candidate domain, ask:
1. **Independence**: Can it be defined in isolation from other domains?
2. **Irreplaceability**: Would its absence prevent the core task from being completed?
3. **Complementarity**: Does it have a parallel, collaborative relationship with other domains, rather than a sequential dependency?

**Counterexample**: Candidate domains A Parse Requirements → B Retrieve Materials → C Generate Report. After reordering, the logic collapses → they are workflow steps.
**Correct Example**: A Static Analysis / B Security Audit / C Performance Diagnosis. After reordering, they still hold → they are capability domains.

### 1.2 Domain Count Is Determined by Task Analysis

> Core rationale and complete determination method: see [design-rationale/design-rationale.md SS2](../design-rationale/design-rationale.md#L16)

The recommended number of radiating domains is **3-8**. The specific count is determined by task analysis. Use the Ordering Test and Three-Question Screening to ensure each radiating domain is an independent and complementary capability domain, not a workflow step.

---

## 2. Capability Matrix Depth Is Fixed at 4 Layers

> Core rationale: see [design-rationale/design-rationale.md SS3](../design-rationale/design-rationale.md#L32)

Each domain is fixed at **4 layers of depth** (Foundation, Advanced, Expert, Extension), not tied to SKILL complexity. When filling in, ensure each layer has specific descriptions of the corresponding capability level for that domain.

---

## 3. Capability Facets Apply Only to the Core Domain

Capability facets characterize the capability dimensions the core domain needs to possess. They are not duplicated for every radiating domain.

| Facet | Core Question |
|:---|:---|
| Efficiency & Cost | Is the resource investment reasonable? |
| Deep Knowledge | Is knowledge coverage complete? |
| Risk Identification | What are the potential risks? |
| Quality Verification | Is the output quality reliable? |
| Domain Integration | Are the domains coordinated with each other? |
| Global System | Has the global impact been considered? |

**Task Anchoring Requirement**: Each facet MUST contain specific knowledge for that core domain. Generic boilerplate like "master relevant domain knowledge" or "identify potential risks" is not acceptable.

**Verification Method**: Cover up the task name in the facet content. If you can still determine which task it belongs to → unqualified. If you cannot determine it after covering → qualified.

---

## 4. Three-Layer Relationship

| Layer | Form | Question Answered |
|:---|:---|:---|
| Capability Matrix | Matrix (core domain + radiating domains x 4 depth layers) | "What capabilities are there" / "How deep are the capabilities" |
| Capability Facets | List (6 facets, core domain only) | "What capability dimensions does the core domain need" |
| Workflow | Vertical progression (steps → actions → checklists) | "How to execute" |

The three are not interchangeable. If capability facets overlap with the capability matrix, the facet design is wrong. If the capability matrix overlaps with workflow steps, the matrix design is wrong (Anti-pattern 4: architectural confusion).

---

## 5. Boundary Declarations

Boundary declarations are divided into Risk Boundaries (safety red lines) and Professional Boundaries (scope protection). For detailed design methods, see [design-guides/boundary-design-guide.md](../design-guides/boundary-design-guide.md).

### 5.1 Risk Boundaries

- **Essence**: "Do no harm"
- **Nature**: Safety-related; upon triggering, the task terminates immediately
- **Count**: Determined by domain safety requirements, typically 3-5 items

### 5.2 Professional Boundaries

- **Essence**: "Do not operate beyond professional boundaries"
- **Nature**: Scope-related; upon triggering, the boundary-crossing behavior terminates and the user is informed
- **Count**: Determined by domain scope, typically 1-3 items

---

## 6. Common Errors

| Error | Problem | Correction |
|:---|:---|:---|
| Disguising workflow steps as capability domains | The capability matrix becomes an execution sequence | Run the Ordering Test and Three-Question Screening; rename to professional domain names |
| Writing 6 facets for every radiating domain | Information overload, diluted attention | Capability facets apply only to the core domain |
| Writing risk boundaries as capability degradation | Safety brakes become disclaimers | Only declare safety red lines. Move "won't do X/Y" into capability scope description or delete |
| Filling facets with generic boilerplate | Loses task anchoring | Each facet must include specific tool names/standard names/vulnerability types |

---

## 7. Checklist

- [ ] Capability matrix covers all core requirements
- [ ] Radiating domains pass the Ordering Test and Three-Question Screening
- [ ] Capability matrix is NOT an alias for workflow steps
- [ ] Each domain has complete 4-layer depth
- [ ] 6 capability facets, core domain only
- [ ] Each facet is task-anchored, free of generic boilerplate
- [ ] Risk boundaries are safety red lines, free of capability degradation
- [ ] Professional boundaries are scope protection, free of capability degradation
