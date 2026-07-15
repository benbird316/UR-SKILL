# Troubleshooting

> **Purpose**: Record common failure patterns and remediation actions encountered during UR-SKILL execution
> **Core Principle**: Each issue pairs "Symptom -> Root Cause -> Remediation Action" (Troubleshooting Triad); pure declarative prompts are prohibited

---

## 1. Capability Architecture Issues

### T01 Capability Matrix Written as Workflow Steps

- **Symptom**: Radiating domains read like "Parse requirements -> Retrieve materials -> Evaluate sources -> Generate report -> Quality check -> Deliver output", resembling a pipeline.
- **Root Cause**: Mistaking the execution order of a workflow for independent radiating domains; violating the Sort Test and the Three-Question Filter.
- **Remediation**:
  1. Apply the Sort Test and Three-Question Filter to candidate domains (see [templates/capability-architecture-template.md](../templates/capability-architecture-template.md)).
  2. If not passed -> roll back to the Research step and re-derive the true radiating domains. If passed -> retain.

### T02 Radiating Domain Count Exceeds 8

- **Symptom**: 9+ rows in the capability matrix, information density drops, model attention is diluted.
- **Root Cause**: Domains were not merged, or workflow sub-steps were incorrectly split into standalone domains.
- **Remediation**:
  1. Examine which domains can be merged into higher-level concepts (e.g., "Result Verification" and "Quality Check" -> "Quality Assurance").
  2. Apply the Three-Question Filter to each candidate domain (see [templates/capability-architecture-template.md](../templates/capability-architecture-template.md)), eliminating non-independent or overlapping domains.
  3. Push excess detail down to references/ or merge into sub-capabilities.
  4. Target: keep radiating domains within 3-8.

### T03 Core Domain Overlaps with Radiating Domain

- **Symptom**: The core domain and a radiating domain describe the same type of capability, with blurred definition boundaries.
- **Root Cause**: The core task boundary is unclear, or the radiating domain was not truly independent when split from the core domain.
- **Remediation**:
  1. Redefine the core domain -- the core domain carries capability facets, while radiating domains provide independent supplementary capabilities surrounding the core.
  2. If a radiating domain overlaps heavily with the core domain -> merge the radiating domain back into the core, or redefine the core to distinguish the two.
  3. Verify: the core domain + each radiating domain should describe different capability domains.

---

## 2. Workflow-Related Issues

### T04 Critical Node Checklist Has Fewer Than 6 Dimensions

- **Symptom**: The checklists for Research (Step 4), Planning (Step 5), Verify (Step 10), and Validation (Step 11) contain only 3-4 items, missing certain review dimensions.
- **Root Cause**: Mistakenly treating critical nodes as non-critical nodes; not allocating review dimensions by node type.
- **Remediation**:
  1. Confirm the node type for that step: Research/Planning/Verify/Validation -> Critical Node -> All 6 dimensions enabled.
  2. Fill in the missing checklist items: Goal Alignment, Fact Anchoring, Direction Calibration, Adversarial Validation, Blind Spot Identification, Impact Projection.
  3. All 6 dimensions must appear; none may be skipped.

### T05 Blind Spot Declaration Substitutes for Remediation Action

- **Symptom**: Blind spot identification only states "Limitations noted" or "Be aware of potential blind spots," with no follow-up investigation or resource request.
- **Root Cause**: The three-layer blind spot mechanism was not followed -- jumping directly from Layer 1 to Layer 3 (pure declarative blind spot).
- **Remediation**:
  1. Layer 1: Execute investigation and analysis; attempt self-optimization to fill the blind spot.
  2. Layer 2 (if Layer 1 remains insufficient): Request resource supplementation from the user (e.g., "Please provide reference materials for this domain").
  3. Layer 3 (if both prior layers lack resource supplementation): Output a blind spot handling report -- actions attempted + remaining blind spots + feasibility recommendations.
  4. Pure declarative blind spots (e.g., "may be unknown") are prohibited -- there must be actions attempted.
  > See [templates/workflow-template.md](../templates/workflow-template.md) for details on the three-layer blind spot mechanism.

### T06 Skipping Unconfirmed Checklist Items

- **Symptom**: A checklist item in a workflow step is unconfirmed (e.g., the blind spot handling field under blind spot identification is left blank), yet the process advances to the next step.
- **Root Cause**: The Loop Cycle principle was not followed -- when any checklist item is unconfirmed, it must be addressed before advancing.
- **Remediation**:
  1. Roll back to the previous step and locate the unconfirmed checklist item.
  2. Execute the corresponding remediation action (investigate/optimize / request resources / output blind spot report).
  3. Recheck that item; only proceed to the next step once confirmed.
  4. Before delivery, backtrack through the entire checklist to ensure no omissions.

---

## 3. Content and Format Issues

### T07 Insufficient Frontmatter Trigger Rate

- **Symptom**: The model frequently does not trigger this SKILL; the user must use precise wording to activate it.
- **Root Cause**: The `description` field in the YAML frontmatter is too conservative or vague, failing to cover synonymous trigger words and diverse trigger scenarios.
- **Remediation**:
  1. Rewrite `description`: the opening sentence must answer "when to trigger," covering multiple synonymous trigger words.
  2. Include the domain name and task type (e.g., "Use when creating, designing, or packaging a SKILL.md file" rather than "Use when designing SKILLs").
  3. The `description` field is limited to <=1024 characters, but information density should be high -- remove weak trigger words such as "when appropriate" or "as needed."
  4. Verify: test with different synonymous trigger phrasings to confirm they all trigger the SKILL.

### T08 Referenced references/ File Does Not Exist

- **Symptom**: The SKILL.md body references `references/examples.md`, but that file is missing.
- **Root Cause**: Supporting files were omitted when generating the SKILL, or reference paths were copied from another SKILL but the files were not copied.
- **Remediation**:
  1. Check all reference paths in the body that begin with `references/`.
  2. Fill in the missing reference files (create content according to the corresponding design guide).
  3. If the file is not required -> remove the corresponding reference declaration from the body.
  4. Run `scripts/validate_skill.py` to automatically detect reference consistency.

### T09 Body Line Count Exceeds 500

- **Symptom**: The SKILL.md body exceeds 500 lines; information in the middle region is diluted (Lost in the Middle effect).
- **Root Cause**: Explanatory content, specification tables, and examples were not progressively offloaded to references/.
- **Remediation**:
  1. Migrate "why..." explanatory content to `design-rationale/design-rationale.md`.
  2. Push specification tables (field constraints, format descriptions) down to references/; the body retains only reference paths.
  3. Migrate examples to `references/examples.md`.
  4. Final body < 500 lines (per the segmentation strategy in [design-guides/structure-design-guide.md §4.3](../design-guides/structure-design-guide.md)).

### T10 Cross-References Point to UR-SKILL Internal Files

- **Symptom**: The generated SKILL body contains path references beginning with `templates/`, `design-guides/`, `References/`, or `design-rationale/`.
- **Root Cause**: UR-SKILL's reference paths were copied when generating the SKILL and were not replaced with the SKILL's own reference paths.
- **Remediation**:
  1. Grep-scan the generated SKILL body for patterns matching `templates/`, `design-guides/`, `design-rationale/`, `References/`.
  2. Found paths -> replace with inline content, or replace with file paths in that SKILL's own references/.
  3. Before delivery (Step 13 Assembly), Grep-verify again to ensure zero residuals.

---

## 4. Quality and Boundary Issues

### T11 Risk Boundary Written as Capability Degradation

- **Symptom**: Risk boundary declarations contain wording such as "Not responsible for security review" or "Only performs intent recognition," resembling disclaimers rather than safety red lines.
- **Root Cause**: Confusing risk boundaries, professional boundaries, and capability degradation. Risk boundaries should declare safety red lines, not disclaim capabilities the SKILL should rightfully assume.
- **Remediation**:
  1. Distinguish the three concepts: Risk boundary = safety red line (trigger immediate termination), Professional boundary = scope protection (do not do things beyond professional scope), Capability degradation = anti-pattern (does X but chooses not to report Y). See [design-guides/boundary-design-guide.md](../design-guides/boundary-design-guide.md) for details.
  2. Check risk boundary declarations for capability-degradation wording such as "not responsible for," "only does X not Y," "does not fall under" -> remove.
  3. Ensure each risk boundary declaration contains at least 1 safety keyword (illegal / public order and morals / discrimination / attack / injection / jailbreak / malicious).

### T12 Incomplete Blind Spot Declaration Format

- **Symptom**: Blind spot declarations lack the "Actions Attempted" field; the format reads "Potential blind spots may exist; results are for reference only; please verify before use."
- **Root Cause**: Blind spot declarations have become disclaimers ("buck-passing") rather than capability-improvement measures driven by the three-layer blind spot mechanism.
- **Remediation**:
  1. Revise blind spot declarations to the three-layer format: Actions Attempted (what was done to fill the blind spot) + Remaining Blind Spots (what is still unknown) + Feasibility Recommendations (suggested resolution path).
  2. Remove buck-passing wording such as "for reference only," "please verify yourself," "potential blind spots may exist," "no guarantee."
  3. Even if it is truly Layer 3 (no resource supplementation), "Actions Attempted" must still be written first, followed by "Remaining Blind Spots + Feasibility Recommendations."
  > See [templates/workflow-template.md](../templates/workflow-template.md) for details on the three-layer blind spot mechanism.

### T13 Capability Facets Written as Generic Platitudes

- **Symptom**: Capability facets state "Mastery of relevant domain knowledge" or "Identify potential risks" -- when the content is masked, it is impossible to tell what task this SKILL performs.
- **Root Cause**: The Veil Test was not applied -- facets were filled with generic platitudes that apply to any SKILL, rendering them meaningless.
- **Remediation**:
  1. Apply the Veil Test to each facet: with the facet content masked, can one infer the task of this SKILL?
  2. If not passed -> rewrite the facet, incorporating the specific knowledge stack of the core domain (e.g., tool names, specification names, vulnerability types).
  3. Example: "Master Python 3.x syntax, PEP 8, OWASP Python Top 10" (pass) vs. "Master relevant domain knowledge" (fail).

### T14 Global Rule Node List Contradicts Step Headings

- **Symptom**: During execution, the model applies unexpected review dimensions to a step. For example, a non-critical step (3 dims) receives 6-dimension deep review, wasting tokens and slowing delivery; or a critical step receives only 3 dimensions, skipping mandatory quality gates.
- **Root Cause**: The global execution rule's critical/non-critical node list is out of sync with actual step heading labels. In UR-SKILL's own history, research-analyst's global rule listed "Parse" as a Critical node (6 dims), but the Parse step heading declared itself as Non-Critical (3 dims) -- the model may follow whichever rule it reads last, producing inconsistent behavior.
- **Remediation**:
  1. **Locate the contradiction**: Cross-reference each step heading's `[xxx Node, n dims]` label against the global rule's critical/non-critical node list. Find nodes that are listed as Critical in the global rule but Non-Critical in the step heading (or vice versa).
  2. **Align to step headings**: The step heading is the source of truth -- update the global rule to match. If the step heading says Non-Critical (3 dims), the global rule must list it as Non-Critical.
  3. **Verify node names match**: Every node name in the global rule MUST appear verbatim as a step heading label (e.g., if the step heading is "Parse (Input Recognition + Requirement Extraction)", the global rule node name should be "Parse" not "Analyze").
  4. **Re-validate**: After fixing, run `validate_skill.py` to confirm check item counts are correct for each node type.

### T15 Professional Boundary Written as Capability Degradation

- **Symptom**: The generated SKILL's professional boundary declarations contain wording like "only review incremental code, not legacy," "only identify, do not analyze," "do not handle complex scenarios" -- at runtime, the model cites its own boundaries to refuse tasks it should perform, self-neutering delivery quality.
- **Root Cause**: Professional boundary declarations confuse "operation attribution" with "capability reduction." Professional boundaries should declare "I do not perform fixes" (attribution), not "I only review incremental, ignore legacy" (degradation). The latter amputates the review scope that should have been delivered.
- **Remediation**:
  1. **Identify degradation wording**: Scan professional boundary declarations for capability-reduction keywords like "only do X not Y," "do not handle," "not responsible for," "limited to."
  2. **Restore to operation attribution**: Rewrite capability degradation as pure operation attribution. E.g., "only review incremental code" -> "do not perform code fixes or patch authoring." Attribution does not constrain review scope.
  3. **Redirect degraded content to blind spots**: If genuinely out-of-scope task scenarios exist (e.g., complex scenarios), do not abandon them in the boundary -- output to the blind spot report (tracking analysis + root cause + recommendations) and continue delivering the rest.
  4. **Cross-check**: After fixing, verify against [design-guides/boundary-design-guide.md](../design-guides/boundary-design-guide.md) that no capability-degradation wording remains in professional boundaries.

### T16 Placeholder Residue in Generated SKILL

- **Symptom**: The generated SKILL contains unfilled placeholder markers such as `[TODO]`, `[FIXME]`, `[WIP]`, `TBD`, `___`, `...`, or empty template slots. At runtime, the model interprets these as undefined behavior zones and either hallucinates content or silently skips the affected section, producing incomplete output.
- **Root Cause**: The generation workflow completed Step 9 (Execute) without verifying template integrity. Anti-pattern 2 is the highest-priority scan item and should block Step 9 from proceeding.
- **Remediation**:
  1. **Scan for residue patterns**: Search the generated SKILL for placeholder markers (`[TODO]`, `[FIXME]`, `[WIP]`, `TBD`, `___`, consecutive ellipses, empty template slots).
  2. **Decision: Fill or Remove**: For each found placeholder -- if content is determinable, fill with definitive content from the pre-analysis report; if genuinely undecidable, delete the entire section and record it as a blind spot entry.
  3. **Validate template integrity**: Re-run `validate_skill.py` against the fixed SKILL to confirm zero placeholder residues.
  4. **Cross-check**: Verify against [spec-design-guide.md](../design-guides/spec-design-guide.md) and [metadata-spec.md](../templates/metadata-spec.md) that all required fields are populated.

### T17 Generated Code Scripts Never Tested for Executability

- **Symptom**: The generated SKILL contains code scripts (e.g., validate_skill.py) but no runtime testing was performed before delivery. The user runs the script for the first time and it fails immediately (syntax error, missing dependency, logic defect), degrading the credibility of the entire generated SKILL.
- **Root Cause**: The generation workflow skipped script executability verification at Step 11 (Validation). The model assumed "the code looks right" equals "it runs," failing to gate delivery on actual script execution and output verification.
- **Remediation**:
  1. **List script inventory**: Scan the generated SKILL's Scripts/ directory and enumerate all script files requiring verification.
  2. **Execute each script**: For each script, run `python <script> --help` or the minimal equivalent command to confirm no syntax errors or import errors.
  3. **Verify output correctness**: If the script produces standard output (e.g., validate_skill.py's validation results), check against known-valid input that the output matches expectations.
  4. **Re-validate**: After all scripts pass execution and output checks, re-run validate_skill.py to confirm SKILL structural integrity is unaffected by the fixes.

---

## 5. Reference Index

| Issue ID | Involved Anti-Pattern | Involved Workflow Steps |
|:---|:---|:---|
| T01 | Anti-pattern 4 Architecture Confusion | Step 4 Research, Step 5 Planning |
| T02 | Anti-pattern 4 Architecture Confusion | Step 5 Planning |
| T03 | Anti-pattern 4 Architecture Confusion | Step 5 Planning |
| T04 | Anti-pattern 5 Review Deficiency | Step 4/5/10/11 |
| T05 | Anti-pattern 6 Blind Spot Evasion, Anti-pattern 9 Blind Spot Buck-Passing | Blind spot identification in all steps |
| T06 | Anti-pattern 5 Review Deficiency | Loop Cycle in all steps |
| T07 | -- | Step 9 Execute (YAML frontmatter) |
| T08 | -- | Step 9 Execute, Step 13 Assembly |
| T09 | Anti-pattern 1 Specification Overreach, Anti-pattern 3 Example Pollution | Step 9 Execute |
| T10 | -- | Step 9 Cross-reference check, Step 13 Assembly |
| T11 | Anti-pattern 7 Risk Boundary Abuse | Step 9 Execute |
| T12 | Anti-pattern 9 Blind Spot Buck-Passing | Blind spot identification in all steps |
| T13 | Anti-pattern 8 Facet Filler | Step 5 Planning |
| T14 | Anti-pattern 11 Step Name Inconsistency | Step 2 Coordination |
| T15 | Anti-pattern 10 Capability Degradation | Step 9 Execute |
| T16 | Anti-pattern 2 Placeholder Residue | Step 9 Execute, Step 10 Verify |
| T17 | -- | Step 11 Validation |

---
