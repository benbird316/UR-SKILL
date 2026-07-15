# Anti-Pattern Detection

> **Purpose**: Define common anti-patterns in SKILL generation and mitigation strategies
> **Core Principle**: Anti-patterns are practices that "appear correct but are actually harmful" — the developer chose an approach with good intentions but the result is worse
> **This file is the UR-SKILL general anti-pattern library. When generating a specific SKILL, reference domain-specific anti-patterns as needed; do not duplicate the contents of this file.**

---

## 1. Anti-Pattern List

### AP-01 Specification Overreach

**Manifestation**: Specification definitions (field constraint tables, format descriptions, metadata specifications) are placed directly into the SKILL.md body instead of being pushed down to references/.

**Why It Occurs**: Developers want information centralized so users can see all rules in one file without jumping between multiple files. They think "the specs are few, it's fine to put them in the body."

**Harm**:
- Body bloats, violating the progressive loading principle
- Information in the middle region is diluted (Lost in the Middle effect)
- Specifications and execution logic are mixed, reducing information density
- During maintenance, modifying specs requires searching the body; modifying logic also requires searching the body — unclear responsibilities

**Detection Method**: Scan the body for typical specification tables like "| Field | Required | Constraint |", "| Facet | Scope |"; count the proportion of table rows in the body.

**Mitigation Strategy**:
- Delete specification tables from the body; push them down to the corresponding file in references/
- Body retains only reference declarations: `Read file: references/xxx-spec.md`
- Place all specification content into dedicated spec reference files (output-spec.md or metadata-spec.md)

---

### AP-02 Placeholder Residue

**Manifestation**: Unfilled placeholder markers such as `[xxx]`, `TODO`, `FIXME`, `{to be filled}`, `TBD`, `___` present in the body.

**Why It Occurs**: Building the skeleton first and filling in content later is an efficient writing practice — developers use placeholders to mark "fill this in later"; or certain content genuinely requires user confirmation before it can be populated.

**Harm**:
- Deliverable is incomplete; the user cannot use it directly
- At runtime, encountering placeholders may cause the model to hallucinate content or silently skip the affected section, producing incomplete output
- Severely undermines the SKILL's professionalism and credibility

**Detection Method**: Regex scan for `\[.*\]`, `TODO`, `FIXME`, `\{.*\}`, `TBD`, `_{3,}`, consecutive ellipsis patterns.

**Mitigation Strategy**:
- Fill all placeholders completely before delivery
- If content genuinely cannot be determined → delete the entire section and record it as a blind spot entry (actions attempted + remaining blind spots + feasibility recommendations)
- Delivery with placeholders is prohibited
- Run `validate_skill.py` for automatic detection

---

### AP-03 Example Contamination

**Manifestation**: Example content from `references/examples.md` is copied and filled directly into the SKILL.md body, resulting in content duplication between the two files.

**Why It Occurs**: Developers think examples are important and placing them in the body makes them more visible to the model; or they worry the model won't proactively read references/, so they stuff examples into the body.

**Harm**:
- Body bloats, violating progressive loading
- Content duplication doubles maintenance cost (changes must be synced across two locations)
- Examples and logic are mixed, reducing body information density
- Model attention is diluted by examples, causing core rules to be ignored

**Detection Method**: Compare body content with `references/examples.md` for text overlap; check for paragraphs with >80% duplication.

**Mitigation Strategy**:
- Reference examples declaratively via paths pointing to references/
- Body retains only reference paths: `Read file: references/examples.md — Purpose: input/output example reference`
- The model loads example files on demand when executing the corresponding step

---

### AP-04 Architecture Confusion (Workflow Step Aliasing)

**Manifestation**: Radiating domains in the capability matrix are aliases for workflow steps — domain names are verbs (analyze/execute/reflect/deliver), domains have strictly linear sequential relationships (A must complete before B, B before C).

**Why It Occurs**: Developers think workflow steps naturally represent capabilities and one-to-one mapping is the clearest and most understandable. When designing, they follow the workflow linearly, naturally using step names as domain names.

**Harm**:
- The capability matrix becomes a mirror of the workflow, losing its identity as an independent knowledge system
- Violates the core design principle "capability domain ≠ workflow step"
- Domain knowledge cannot be invoked across steps, losing architectural flexibility
- Fails all Three-Question Filter checks (Independence / Irreplaceability / Complementarity)

**Detection Method**:
1. Check if radiating domain names can be directly mapped to workflow step numbers
2. Check if radiating domains have linear sequential dependency relationships
3. Sort Test: if reordering the domain order breaks the logic → anti-pattern

**Mitigation Strategy**:
- Radiating domains should be independent knowledge bodies (nouns), not workflow steps (verbs)
- Each domain must pass the Three-Question Filter: Independence / Irreplaceability / Complementarity
- Any workflow step may invoke any radiating domain — no temporal dependencies

> **Classic Case 1 (Anti-pattern 4)**: The UR-SKILL master SKILL once directly listed the following workflow steps as radiating domains:
>
> | Incorrect Radiating Domain (Workflow Alias) | Actual Corresponding Workflow Step |
> |:---|:---|
> | A Semantic Parsing | Step 1 Parse |
> | B Knowledge Retrieval | Step 2 Research |
> | C Architecture Design | Step 3 Architecture |
> | D Content Engineering | Step 4 Execute (Module Assembly) |
> | E Quality Assurance | Step 5 Verify |
> | F Delivery Management | Step 7 Deliver |
>
> > **Classic Case 2 (Anti-pattern 4)**: The research-analyst sub-SKILL once directly listed the following workflow steps as radiating domains:
> >
> > | Incorrect Radiating Domain (Workflow Alias) | Actual Corresponding Workflow Step |
> > |:---|:---|
> > | A Semantic Parsing | Step 1 Parse |
> > | B Task Domain Research | Step 2 Research |
> > | C Capability Domain Derivation | Step 3 Architecture |
> > | D Complexity Determination | Step 4 Execute (Complexity Determination) |
> > | E File Dependency Decision | Step 4 Execute (File Dependency Decision) |
> > | F Output Structuring | Step 7 Deliver |
>
> **Detection Signal**: Radiating domains A→B→C→D→E→F strictly correspond one-to-one with workflow steps 1→2→3→4→5→6→7, and the domains have linear sequential relationships (B can only proceed after A completes). Correct radiating domains should be independent of each other with no temporal dependencies.
>
> **Correct Approach**: Radiating domains should be independent knowledge bodies (nouns), not workflow steps (verbs). The UR-SKILL master SKILL's 6 domains: Requirements Engineering & Business Translation, SKILL Architecture Design, Prompt System Engineering, Quality Engineering, Ethics & Safety, Iterative Improvement. The research-analyst sub-SKILL's 6 domains: Requirements Engineering (requirement parsing & implicit assumption identification), Job Competency Analysis (KSAO model mapping), Information Source Assessment (three-level source anchoring), Occupational Risk Identification, Professional Ethics, System Cognition (UR-SKILL methodology internalization). Domain selection rationale: see [../design-rationale/design-rationale.md §10-§12](../design-rationale/design-rationale.md).

---

### AP-05 Review Deficiency

**Manifestation**: Critical node checklists (Research, Planning, Verify, Validation) contain fewer than 6 review dimensions — only 3-4 dimensions such as Goal Alignment and Fact Anchoring are checked, and others are skipped.

**Why It Occurs**: Developers think non-critical steps don't need so many checks, or want to speed things up with "good enough." Alternatively, they misjudge which nodes are critical.

**Harm**:
- Quality gates fail; key decision points lack sufficient review
- Prone to "good enough" delivery, with no lower quality boundary
- Blind spots, direction deviations, and factual errors slip through at critical nodes, amplifying downstream

**Detection Method**: Scan each workflow step's checklist; cross-reference the node type (critical/non-critical) to verify the number of review dimensions matches.

**Mitigation Strategy**:
- Critical nodes (Research/Planning/Verify/Validation/Loop Decision): all 6 dimensions enabled — Goal Alignment, Fact Anchoring, Direction Calibration, Adversarial Validation, Blind Spot Identification, Impact Projection
- Non-critical nodes (Parse/Coordinate/Dispatch/Consolidate/Execute/Assemble): 3 dimensions — Goal Alignment, Fact Anchoring, Blind Spot Identification
- All 6 dimensions must appear; none may be skipped

---

### AP-06 Blind Spot Evasion

**Manifestation**: Blind spot identification only states "limitations noted" or "deficiencies exist," with no follow-up action — identified blind spots are left unaddressed as the process moves to the next step.

**Why It Occurs**: Developers think identifying the blind spot is sufficient notification, and the user can handle it. Or they don't know how to address the blind spot, so they mark it and skip.

**Harm**:
- Blind spots become disclaimers rather than drivers for capability improvement
- Every encounter with the same blind spot results in no progress, preventing iterative improvement
- Delivery quality stagnates at the current level with no growth path

**Detection Method**: Check whether blind spot identification contains only declarative statements without "actions attempted," "resource requests," or "feasibility recommendations."

**Mitigation Strategy**:
- Enforce the three-layer blind spot mechanism:
  1. Layer 1: Investigate and analyze; attempt self-optimization to fill the blind spot
  2. Layer 2: If still insufficient → request resource supplementation from the user
  3. Layer 3: If no resources available → output a blind spot handling report (actions attempted + remaining blind spots + feasibility recommendations)
- Pure declarative blind spots are prohibited

---

### AP-07 Risk Boundary Abuse

**Manifestation**: Risk boundary declarations are written as capability degradation — containing phrasing like "not responsible for security review," "only performs intent recognition," "does not provide professional advice"; or professional boundary content is placed into risk boundaries.

**Why It Occurs**: Developers want to draw clear boundaries and avoid liability, thinking the more conservative the safer. Or they confuse "safety red lines" with "capability scope," putting everything they'd rather not do into risk boundaries.

**Harm**:
- Risk boundaries shift from safety brakes to disclaimers
- Blurs the distinction between safety red lines and professional boundaries
- Critical safety red lines are left unclear, while capabilities that should not be restricted are cut

**Detection Method**: Check risk boundary declarations for capability degradation phrasing ("not responsible for," "only does X not Y," "does not fall under"); check whether they contain professional scope descriptions.

**Mitigation Strategy**:
- Risk boundaries only declare safety red lines: illegal activity, public order and morals, discrimination, attack, injection, jailbreak, malicious use, etc.
- Professional scope goes into a separate "Professional Boundary" declaration
- Each risk boundary declaration must contain at least 1 safety keyword

---

### AP-08 Facet Filler

**Manifestation**: Capability facets are filled with generic boilerplate, such as "Facet 2 Knowledge Deepening: Master relevant domain knowledge," "Facet 3 Risk Identification: Identify potential risks" — covering the task name, you cannot tell what SKILL this is for.

**Why It Occurs**: Rapid template filling — developers think "roughly the right idea is fine," or they don't know what specific content to write and use generic descriptions as a fallback.

**Harm**:
- Facets lose specificity; they apply to any SKILL, making them effectively unwritten
- The capability matrix has no task anchoring, resulting in insufficient quality depth
- The model receives no domain knowledge guidance from the facets during execution

**Detection Method**: Veil Test — cover the facet content; can you infer the core task of this SKILL? If not → facet filler anti-pattern.

**Mitigation Strategy**:
- Each facet MUST include the specific knowledge stack for that core domain
- Positive example: "Master OWASP Python Top 10, PEP 8 conventions, CWE Top 25"
- Negative example: "Master relevant domain knowledge"

---

### AP-09 Blind Spot Buck-Passing

**Manifestation**: Blind spot declarations jump directly from Layer 1 to Layer 3 (purely declarative), writing "blind spots may exist; results are for reference only," "please verify before use," "accuracy not guaranteed" — buck-passing language.

**Why It Occurs**: Developers want to honestly disclose limitations, fear misleading users or taking responsibility, and think writing "for reference only" fulfills their duty.

**Harm**:
- Blind spot declarations become disclaimer clauses rather than drivers for capability improvement
- Every time, the blind spot is passed off without ever attempting optimization
- User trust declines, feeling the SKILL is unreliable

**Detection Method**: Check whether blind spot declarations lack an "actions attempted" field; check for buck-passing language like "for reference only," "please verify yourself," "may exist," "no guarantee."

**Mitigation Strategy**:
- Blind spots must first be investigated and optimized (Layer 1); if still insufficient, request resources (Layer 2); if no resources are available, report (Layer 3)
- Layer 3 report format: actions attempted + remaining blind spots + feasibility recommendations
- Remove all buck-passing language

---

### AP-10 Capability Degradation

**Manifestation**: Professional boundary declarations are written as capability reduction — containing phrasing like "only review incremental code, not legacy," "only identify, do not analyze," "do not handle complex scenarios" — at runtime, the model cites its own boundaries to refuse tasks it should perform.

**Why It Occurs**: Developers want to simplify the delivery process and avoid wasting resources; or they fear poorly handling complex scenarios and directly exclude them in the boundary to avoid errors.

**Harm**:
- SKILL delivery quality is self-neutered by its own boundary declarations
- Issues that should have been found are concealed due to "boundary limitations," leading to hidden bugs and technical debt accumulation
- Professional boundaries shift from "cross-boundary protection" to "self-limitation"

**Detection Method**: Scan professional boundary declarations for capability reduction keywords: "only does X not Y," "does not handle," "not responsible for," "limited to."

**Mitigation Strategy**:
- Professional boundaries only declare **operation attribution** (e.g., "do not perform code fixes or patch authoring"), without limiting the review scope
- If genuinely out-of-scope scenarios exist → output to the blind spot report (tracking analysis + root cause + recommendations) and continue delivering the rest
- Do not lower delivery quality due to boundary declarations

---

### AP-11 Step Name Mismatch in Global Rules

**Manifestation**: Node names listed in the global execution rules (e.g., "Verify") do not match the actual step headings (e.g., "Step 10: Quality Check") — the node name does not appear verbatim in the step heading, preventing rule binding.

**Why It Occurs**: When step headings are modified, the global rule list is not synced; or developers think "roughly the same meaning is fine," without awareness of exact matching.

**Harm**:
- The model applies the wrong review dimensions to a step: non-critical nodes receive 6-dimension review (wasting tokens), or critical nodes receive 3-dimension review (missing quality gates)
- Global rules become ineffective, failing to provide unified constraints
- Review quality varies unevenly across steps

**Detection Method**:
1. Cross-reference each step heading's `[xxx Node]` label against the global rule's node list
2. Check if any node name in the global rule does not appear verbatim in a step heading
3. Check if any node appears in both critical and non-critical lists

**Mitigation Strategy**:
- Every node name in the global rule MUST exactly match the step heading label (verbatim)
- No node should appear in both critical and non-critical lists simultaneously
- After fixing, re-validate with `validate_skill.py`

---

## 2. Detection Priority

Scan order (high priority → low priority):

| Priority | Anti-Pattern | Severity | Rationale |
|:---:|:---|:---:|:---|
| 1 | AP-02 Placeholder Residue | Critical | Directly impacts usability; deliverable incomplete |
| 2 | AP-01 Specification Overreach | High | Directly impacts architectural correctness; body bloat |
| 3 | AP-07 Risk Boundary Abuse | High | Directly impacts security design; boundary confusion |
| 4 | AP-09 Blind Spot Buck-Passing | High | Directly impacts delivery credibility; disclaimer-like declarations |
| 5 | AP-10 Capability Degradation | High | Directly impacts delivery quality; self-neutering |
| 6 | AP-04 Architecture Confusion | Medium | Directly impacts structural correctness; capability matrix fails |
| 7 | AP-08 Facet Filler | Medium | Directly impacts quality depth; capabilities unanchored |
| 8 | AP-03 Example Contamination | Medium | Directly impacts loading efficiency; content duplication |
| 9 | AP-05 Review Deficiency | Medium | Directly impacts quality checks; gate failure |
| 10 | AP-11 Step Name Mismatch | Medium | Directly impacts rule binding; review dimension misalignment |
| 11 | AP-06 Blind Spot Evasion | Low | Directly impacts continuous optimization; iteration stagnation |

> Priority logic: Usability impact > Safety/professionalism impact > Quality depth impact > Continuous optimization impact.

---

## 3. Scan Script

Automated scan implementation: see [scripts/validate_skill.py](../Scripts/validate_skill.py); script design specification: see [design-guides/pattern-ref-design-guide.md §3](../design-guides/pattern-ref-design-guide.md).
