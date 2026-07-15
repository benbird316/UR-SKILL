# Capability Architecture Design Guide

> Only teaches how to design the capability matrix, capability facets, and boundary declarations. The capability matrix consists of capability domains, not workflow steps; capability facets target only the core domain; boundary declarations are divided into safety red lines and scope protection.
> For determining capability architecture design needs, see skill-package-design-guide.md §2.

---

## §1 Capability Matrix is Capability Domains, Not Workflow Steps

### 1.1 Key Distinction Methods

**Sort Test**: Rearrange the candidate radiating domains; if the logic breaks, they are workflow steps.

**Three-Question Filter**: Ask each candidate domain:
1. **Independence**: Can it be defined independently from other domains?
2. **Irreplaceability**: Would the core task fail to complete without it?
3. **Complementarity**: Is it in a parallel collaboration relationship with other domains, rather than a sequential dependency?

**Counterexample**: Candidate domains A Parse Requirements -> B Retrieve Information -> C Generate Report; after reordering, logic breaks -> they are workflow steps.
**Positive Example**: A Static Analysis / B Security Audit / C Performance Diagnostics; still valid after reordering -> they are capability domains.

> Pure reasoning-type capabilities are mapped to `[Cognitive Operation]`; see tool-invocation-design-guide.md §1 for details.

### 1.2 Number of Domains Determined by Task Analysis

The recommended number of radiating domains is **3-8**, determined by task analysis. Use the Sort Test and Three-Question Filter to ensure each radiating domain is an independent and complementary capability domain, not a workflow step.

---

## §2 Capability Matrix Depth: Fixed at 4 Layers

Each domain has a fixed **4-layer depth** (Foundation, Advanced, Expert, Extension); no layer may be omitted. When filling, ensure each layer has a concrete description of the corresponding capability level for that domain.

---

## §3 Capability Facets Target Only the Core Domain

Capability facets describe the capability dimensions that the core domain must possess; they are not redundantly built for every radiating domain.

| Facet | Core Question |
|:---|:---|
| Efficiency & Cost | Is resource investment reasonable? |
| Knowledge Deepening | Is knowledge coverage complete? |
| Risk Identification | What are the potential risks? |
| Quality Inspection | Is output quality reliable? |
| Domain Fusion | Do the domains collaborate effectively? |
| System-Wide Perspective | Has the global impact been considered? |

**Task Anchoring Requirement**: Each facet must contain concrete knowledge specific to the core domain; generic boilerplate such as "master relevant domain knowledge" or "identify potential risks" is not acceptable.

**Verification Method**: Cover the task name in the facet content; if you can still identify the task -> unqualified; if you cannot -> qualified.

---

## §4 Three-Level Relationship

| Level | Form | Question Answered |
|:---|:---|:---|
| Capability Matrix | Matrix (Core Domain + Radiating Domains x 4 Layers) | "What capabilities exist?" / "How deep are the capabilities?" |
| Capability Facets | List (6 facets, targeting only the core domain) | "What capability dimensions must the core domain possess?" |
| Workflow | Vertical progression (Step -> Action -> Checklist) | "How to execute?" |

The three levels do not substitute for each other. If capability facets overlap with the capability matrix, the capability facet design is wrong; if the capability matrix overlaps with workflow steps, the capability matrix design is wrong (Anti-pattern 4: Architecture Confusion).

---

## §5 Boundary Declarations

For full definitions, format specifications, and positive/negative examples of boundary declarations, see [boundary-design-guide.md](boundary-design-guide.md).

---

## §6 Common Errors

| Error | Problem | Correction |
|:---|:---|:---|
| Disguising workflow steps as capability domains | Capability matrix becomes execution order | Execute Sort Test and Three-Question Filter, rename to professional domain names |
| Writing 6 facets for every radiating domain | Information explosion, attention dilution | Capability facets target only the core domain |
| Risk boundary written as capability degradation | Safety brake becomes disclaimer | Only declare safety red lines; "don't do X, don't do Y" goes into capability scope description or is deleted |
| Facets filled with generic boilerplate | Loses task anchoring | Each facet includes concrete tool names / specification names / vulnerability types |

---

## §7 Checklist

- [ ] Capability matrix covers all core requirements
- [ ] Radiating domains pass the Sort Test and Three-Question Filter
- [ ] Capability matrix is not an alias for workflow steps
- [ ] Each domain has all 4 layers complete
- [ ] 6 capability facets, targeting only the core domain
- [ ] Each facet has task anchoring, no generic boilerplate
- [ ] Risk boundaries are safety red lines, no capability degradation
- [ ] Professional boundaries are scope protection, no capability degradation
