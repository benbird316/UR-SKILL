# Anti-Pattern Detection

> Purpose: Defines common anti-patterns in SKILL generation and mitigation strategies
> Core principle: Anti-patterns are practices that "appear correct but are actually harmful" and must be proactively sniffed out

---

## 1. 10 Anti-Patterns

| No. | Anti-Pattern | Manifestation | Harm | Detection Method | Mitigation Strategy |
|:---|:---|:---|:---|:---|:---|
| Anti-pattern 1 | Specification Overreach | Specification definitions (field constraints, format descriptions) placed directly into the body | Body bloat, violates progressive loading, reduces information density | Scan for specification tables like "| Field | Required | Constraint |", "| Facet | Scope |" | Delete specification tables, move them to references/; body retains only reference paths. 详见 [spec-design-guide.md](../design-guides/spec-design-guide.md) |
| Anti-pattern 2 | Placeholder Residue | Unfilled content such as [xxx], TODO, FIXME, {to be filled} present in the body | Incomplete deliverable; user cannot use directly | Regex scan for \[.*\]\|TODO\|FIXME\|\{.*\} | Fill all completely, or delete the section and mark as blind spot. 详见 [spec-design-guide.md](../design-guides/spec-design-guide.md) |
| Anti-pattern 3 | Example Pollution | Copying examples from references/ directly into the body | Body bloat, examples duplicate body content, violates progressive loading | Compare body content with references/examples.md; check for paragraphs with >80% duplication | Reference examples declaratively via paths to references/; body retains only reference declarations. 详见 [examples-design-guide.md](../design-guides/examples-design-guide.md) |
| Anti-pattern 4 | Architecture Confusion | The capability matrix's radiating domains are aliases for workflow steps (e.g., mapping workflow steps A->B->C->D->E->F directly as "Domain 1->Domain 2->...") | Capability matrix becomes a mirror of the workflow, losing its identity as an independent knowledge system; SKILL structure is fundamentally wrong | Check if radiating domain names can be mapped to workflow step numbers; check if radiating domains have linear sequential relationships | Radiating domains in the capability matrix should be independent knowledge systems (e.g., "Requirements Engineering," "Role Capability Analysis," "Professional Risk Identification," "Professional Ethics," "System Awareness"), decoupled from workflow steps |

> **Classic Case 1 (Anti-pattern 4)**: The UR-SKILL master SKILL once directly listed the following workflow steps as radiating domains:
>
> | Incorrect Radiating Domain (Workflow Alias) | Actual Corresponding Workflow Step |
> |:---|:---|
> | A Semantic Parsing | Step 1 Parse |
> | B Knowledge Retrieval | Step 2 Research |
> | C Architecture Design | Step 3 Architect |
> | D Content Engineering | Step 4 Execute (Module Assembly) |
> | E Quality Assurance | Step 5 Verify |
> | F Delivery Management | Step 7 Deliver |
>
> > **Classic Case 2 (Anti-pattern 4)**: pre-analysis-engineer once directly listed the following workflow steps as radiating domains:
> >
> > | Incorrect Radiating Domain (Workflow Alias) | Actual Corresponding Workflow Step |
> > |:---|:---|
> > | A Semantic Parsing | Step 1 Parse |
> > | B Task Domain Research | Step 2 Research |
> > | C Capability Domain Derivation | Step 3 Architect |
> > | D Complexity Determination | Step 4 Execute (Complexity Determination) |
> > | E File Dependency Decision | Step 4 Execute (File Dependency Decision) |
> > | F Output Structuring | Step 7 Deliver |
>
> **Detection Signal**: Radiating domains A->B->C->D->E->F strictly correspond one-to-one with workflow steps 1->2->3->4->5->6->7, and the domains have linear sequential relationships (B can only proceed after A completes). Correct radiating domains should be independent of each other with no temporal dependencies.
>
> **Correct Approach**: Radiating domains should be independent knowledge bodies (nouns), not workflow steps (verbs). The UR-SKILL master SKILL was corrected to 6 domains: Requirements Engineering & Business Translation, SKILL Architecture Design, Prompt System Engineering, Quality Engineering, Ethics & Safety, Iterative Improvement. pre-analysis-engineer was corrected to 6 domains: Requirements Engineering, Role Capability Analysis, Capability Domain Information Evaluation, Professional Risk Identification, Professional Ethics, System Awareness. Domain selection rationale: see [../design-rationale/design-rationale.md sections 10-12](../design-rationale/design-rationale.md).
| Anti-pattern 5 | Review Deficiency | Insufficient review dimension checks in the generated SKILL workflow (fewer than 6 dimensions for critical checkpoints) | Quality checks become ineffective; easy to settle for "good enough" | Scan each workflow step; check whether the number of review dimensions matches the checkpoint type | Allocate review dimensions by checkpoint type: 6 dimensions for critical checkpoints, 3 dimensions for non-critical checkpoints. 详见 [structure-guideline.md](../design-guides/structure-guideline.md) |
| Anti-pattern 6 | Blind Spot Evasion | Blind spot identification only writes "limitations noted" without executing the three-tier mechanism investigation | Blind spots become disclaimers rather than drivers for continued optimization | Check whether blind spot identification includes "actions attempted for remediation and optimization + remaining blind spots + feasibility recommendations" | Enforce the three-tier mechanism: investigate and optimize -> request resources -> blind spot report + feasibility recommendations. 详见 [structure-guideline.md](../design-guides/structure-guideline.md) |
| Anti-pattern 7 | Risk Boundary Abuse | Risk boundary declarations are written as capability degradation (e.g., "not responsible for security review," "only do intent recognition") rather than safety red lines; or professional boundaries are written into risk boundary declarations | Risk boundaries shift from safety brakes to disclaimers, or confuse safety and scope responsibility boundaries | Check whether risk boundary declarations contain capability degradation language ("not responsible for," "only do X not Y") or professional boundary content | Risk boundaries only declare safety red lines (illegal/public order violations, discrimination, attack/injection/jailbreak, etc.); professional boundaries go into a separate professional boundary declaration. 详见 [boundary-design-guide.md](../design-guides/boundary-design-guide.md) |
| Anti-pattern 8 | Facet Padding | Capability facet content uses generic boilerplate without task anchoring (e.g., "Facet 2 Deep Knowledge: Master relevant domain knowledge," "Facet 3 Risk Identification: Identify potential risks") | Facets lose specificity; they apply to any SKILL, making them effectively unwritten | Check whether facet content includes task-specific domain knowledge (e.g., tool names, specification names, vulnerability types) | Each facet MUST include the specific knowledge stack for that core domain, e.g., "Master OWASP Python Top 10," "Proficient in PEP 8 conventions". 详见 [capability-design-guide.md](../design-guides/capability-design-guide.md) |
| Anti-pattern 9 | Blind Spot Blame-Shifting | Blind spot declarations jump directly from Tier 1 to Tier 3 (purely declarative), e.g., "Blind spots may exist; results are for reference only," "Please verify before use" | Blind spot declarations become disclaimer clauses rather than drivers for capability improvement | Check whether blind spot declarations lack the "actions attempted" field; check for blame-shifting language like "for reference only," "please verify yourself" | Blind spots must first be investigated and optimized (Tier 1); if still insufficient, request resources (Tier 2); if no resources are available, report (Tier 3), with report format: "actions attempted + remaining blind spots + feasibility recommendations". 详见 [structure-guideline.md](../design-guides/structure-guideline.md) |
| Anti-pattern 10 | Capability Degradation | Professional boundary declarations are written as capability reduction (e.g., "only review incremental code, not old code," "only identify, do not analyze," "do not handle complex scenarios") rather than defining true professional scope | SKILL delivery quality is constrained and lowered by its own boundary declarations; issues that should have been found are concealed due to "boundary limitations," leading to hidden bugs and technical debt accumulation | Check whether professional boundary declarations contain "only do X not Y" capability reduction language, or abandonment-style descriptions like "do not handle," "not responsible for" | Professional boundaries only declare scope attribution ("do not perform fixes or patch authoring"); do not lower delivery quality due to boundary declarations. Boundary-exceeding tasks identified should undergo tracking analysis, determine root cause, and be output to the blind spot report, rather than being abandoned outright. 详见 [boundary-design-guide.md](../design-guides/boundary-design-guide.md) |
| Anti-pattern 11 | Step Name Mismatch in Global Rules | The global execution rules list node names (e.g., "Parsing") that do not match the actual step headings (e.g., "Pre-Analysis"); designers tend to reuse agent SKILL step names thinking they are equivalent to the main SKILL's delegated function — but they are different structural contexts | The model applies the wrong review dimensions — a step may receive 6-dimension scrutiny intended for Critical nodes (wasting tokens) or 3-dimension review for a Critical node (missing quality gates) | (1) Cross-reference each step heading's `[xxx Checkpoint]` label against the global rule's node list; (2) Check if any name in the global rule list does not appear verbatim as a step heading; (3) Check if any node appears in both Critical and Non-Critical lists | (1) Every node name in the global rule MUST exactly match a step heading label; (2) No node should appear in both lists; (3) After fixing, re-validate with validate_skill.py. 详见 [structure-guideline.md](../design-guides/structure-guideline.md) |

## 2. Detection Priority

Scan order (high priority -> low priority):

1. Anti-pattern 2 Placeholder Residue (directly impacts usability, Critical)
2. Anti-pattern 1 Specification Overreach (directly impacts architectural correctness, High)
3. Anti-pattern 7 Risk Boundary Abuse (directly impacts security design, High)
4. Anti-pattern 9 Blind Spot Blame-Shifting (directly impacts delivery credibility, High)
5. Anti-pattern 10 Capability Degradation (directly impacts delivery quality, High)
6. Anti-pattern 4 Architecture Confusion (directly impacts structural correctness, Medium)
7. Anti-pattern 8 Facet Padding (directly impacts quality depth, Medium)
8. Anti-pattern 3 Example Pollution (directly impacts loading efficiency, Medium)
9. Anti-pattern 5 Review Deficiency (directly impacts quality checks, Medium)
10. Anti-pattern 6 Blind Spot Evasion (directly impacts delivery quality, Low)

> Priority logic: Usability impact > Safety/professionalism impact > Quality depth impact > Continuous optimization impact.

---

## 3. Scan Script

Scan script implementation: see [scripts/validate_skill.py](../Scripts/validate_skill.py); script design specification: see [design-guides/anti-patterns-design-guide.md section 6](../design-guides/anti-patterns-design-guide.md).
