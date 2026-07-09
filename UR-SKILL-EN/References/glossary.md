# Glossary

> Purpose: The conceptual anchor of the UR-SKILL system, unifying term semantics across all files
> Core principle: The glossary is the "semantic contract" within the system -- the same term points to the same concept across all files (SKILL.md body, templates/, design-guides/, References/)

---

## 1. Architecture Domain

### G01 Capability Matrix

- **Definition**: A structured expression of capabilities consisting of 1 core domain + 3-8 radiating domains x 4 tiers of depth (Foundation -> Advanced -> Expert -> Extension)
- **Domain**: Architecture Domain
- **Example**: UR-SKILL's capability matrix includes "Core: SKILL Generation Engineering" + 6 radiating domains (Requirements Engineering & Business Translation, SKILL Architecture Design, Prompt Systems Engineering, Quality Engineering, Ethics & Safety, Iterative Improvement), each with 4 tiers

### G02 Core Domain

- **Definition**: The professional dimension of the task, carrying capability facets (Facets 1-6); the only mandatory domain in the capability matrix
- **Domain**: Architecture Domain
- **Example**: UR-SKILL's core domain is "SKILL Generation Engineering"; Facet 2 Deep Knowledge declares "Master Prompt Engineering, Markdown specifications"

### G03 Radiating Domain

- **Definition**: Independent professional capability dimensions surrounding the core domain; each domain is an independent capability domain rather than a workflow step
- **Domain**: Architecture Domain
- **Example**: UR-SKILL's 6 radiating domains: Requirements Engineering & Business Translation, SKILL Architecture Design, Prompt Systems Engineering, Quality Engineering, Ethics & Safety, Iterative Improvement

### G04 Capability Facet

- **Definition**: 6 capability dimensions targeting only the core domain (Efficiency & Cost, Deep Knowledge, Risk Identification, Quality Verification, Domain Integration, System Holistics), characterizing the capability attributes the core domain must possess
- **Domain**: Architecture Domain
- **Example**: Facet 3 Risk Identification declares "Sniff out anti-patterns and architecture confusion in SKILL generation"

### G05 Capability Depth (4 Tiers)

- **Definition**: 4 progressive tiers for each capability domain (Foundation Tier -> Advanced Tier -> Expert Tier -> Extension Tier); all complexity levels MUST have 4 tiers, no deletion permitted
- **Domain**: Architecture Domain
- **Example**: Core domain's 4 tiers: Extract goals/domain/delivery format -> Infer implicit requirements/determine complexity -> Prioritize requirements/multi-source fusion -> Infer requirement patterns

### G06 Ordering Test

- **Definition**: A method to verify whether radiating domains are workflow steps -- reorder the candidate domains; if the logic collapses after reordering, they are workflow steps rather than independent capability domains
- **Domain**: Architecture Domain / Quality Domain
- **Example**: Candidate domains A "Parse Requirements" -> B "Retrieve Materials" -> C "Generate Report"; reordering to C -> A -> B causes logic collapse -> they are workflow steps

### G07 Three-Question Screening

- **Definition**: A method to validate candidate capability domains -- Independence (can it exist independently), Irreplaceability (can it not be replaced by other domains), Complementarity (does it complement other domains without overlap)
- **Domain**: Architecture Domain / Quality Domain
- **Example**: Questioning the "Security Audit" candidate domain: Can it exist independently? (Yes) Irreplaceable by other domains? (Yes) Complementary with existing domains? (Yes) -> Pass

---

#### 1.1 Capability Domain Names

### G32 SKILL Generation Engineering

- **Definition**: The core domain of the UR-SKILL main SKILL -- transforming vague requirements into standardized, executable, verifiable SKILL.md file packages. Carries 6 capability facets (Efficiency & Cost, Deep Knowledge, Risk Identification, Quality Verification, Domain Integration, System Holistics)
- **Domain**: Architecture Domain
- **Example**: User proposes a vague requirement "make a code review SKILL" -> SKILL Generation Engineering transforms it into a standardized SKILL.md file package containing a capability matrix, 6-step workflow, and rule system

### G33 Requirements Engineering & Business Translation

- **Definition**: One of UR-SKILL main SKILL's radiating domains -- transforms vague intentions into structured requirements, maps business goals to SKILL capabilities, identifies implicit assumptions and undeclared constraints
- **Domain**: Architecture Domain
- **Example**: User says "help me build a tool that checks code quality" -> Requirements Engineering & Business Translation identifies implicit assumptions (target language, review scope, output format), maps to the quality review capability domain

### G34 SKILL Architecture Design

- **Definition**: One of UR-SKILL main SKILL's radiating domains -- capability matrix design, domain independence verification (Ordering Test + Three-Question Screening), conflict identification, niche analysis, architectural extensibility
- **Domain**: Architecture Domain
- **Example**: Execute Ordering Test and Three-Question Screening on the candidate radiating domain "Code Style Check" to determine whether it is an independent capability domain rather than a workflow step

### G35 Prompt Systems Engineering

- **Definition**: One of UR-SKILL main SKILL's radiating domains -- information architecture (Primacy/Recency), RFC 2119 rule system, attention management, tool binding syntax, progressive loading strategy
- **Domain**: Architecture Domain
- **Example**: When designing the body structure, place MUST-level constraints in the Primacy Zone (first 20%), Double Prompting rule reiteration in the Recency Zone (last 20%), and indexes/paths in the middle 60%

### G36 Quality Engineering

- **Definition**: One of UR-SKILL main SKILL's radiating domains -- anti-pattern detection, boundary verification, completeness check, cross-reference consistency, generated code/script executability verification
- **Domain**: Architecture Domain
- **Example**: The Verify step (Step 5) performs an 11-item anti-pattern scan on the generated SKILL (Specification Overreach, Example Pollution, Architecture Confusion, etc.); if not passed, return for remediation

### G37 Ethics & Safety

- **Definition**: One of UR-SKILL main SKILL's radiating domains -- risk boundaries (illegal/discrimination/injection), profession-specific risk lineage, professional boundaries, safety guardrail design
- **Domain**: Architecture Domain
- **Example**: User requests generating a "Medical Diagnosis SKILL" -> Ethics & Safety identifies that the requirement touches a professional boundary (requires medical practitioner qualification), marks as Professional Boundary-01 and sets guardrails

### G38 Iterative Improvement

- **Definition**: One of UR-SKILL main SKILL's radiating domains -- platform adaptation, blind spot feedback self-repair, metadata optimization, model-specific format adaptation, version evolution and backward compatibility
- **Domain**: Architecture Domain
- **Example**: Generated SKILL tested on the Claude platform reveals XML tag nesting too deep -> Iterative Improvement adjusts tag structure while preserving semantics

### G39 Pre-Analysis Engineering

- **Definition**: The core domain of the pre-analysis SKILL (pre-analysis-engineer) -- automatically completes requirements parsing, profession mapping, complexity determination, file dependency decisions, outputs a pre-analysis report. Carries 6 capability facets
- **Domain**: Architecture Domain
- **Example**: User inputs "I want a lawyer assistant SKILL" -> Pre-Analysis Engineering completes profession mapping (lawyer), complexity determination (medium), file dependency decisions (requires B1 professional ethics file), outputs pre-analysis report

### G40 Requirements Engineering

- **Definition**: One of the pre-analysis SKILL's radiating domains -- identifies core task goals and problem domain boundaries, extracts structured information, identifies implicit assumptions, predicts requirement evolution paths. Distinguished from the main SKILL's "Requirements Engineering & Business Translation": one analyzes requirement structure, the other translates requirements into SKILL architecture
- **Domain**: Architecture Domain
- **Example**: For the "code review SKILL" requirement, Requirements Engineering extracts: core goal = quality gating, problem domain boundary = incremental code review, implicit assumption = user already has code repository access

### G41 Job Capability Analysis

- **Definition**: One of the pre-analysis SKILL's radiating domains -- analyzes the target profession's core capability domains and work characteristics based on the KSAO model (Knowledge/Skills/Abilities/Other characteristics), determines cross-domain capability dependencies, provides a professional anchor for capability domain derivation
- **Domain**: Architecture Domain
- **Example**: Analyzing the "Software Architect" role -> Core KSAO: system design knowledge, trade-off decision skills, cross-team communication ability -> Derived radiating domains: architecture patterns, technology selection, quality attributes

### G42 Capability Domain Information Evaluation

- **Definition**: One of the pre-analysis SKILL's radiating domains -- distinguishes information source types and authority (official standards/community content/AI-generated), evaluates timeliness and domain applicability, detects AI-generated content and conflicts of interest. The theoretical foundation of Three-Tier Source Anchoring
- **Domain**: Architecture Domain
- **Example**: Retrieving Python coding standards -> Source evaluation: PEP 8 (official standard/L1 authoritative) > Real Python tutorial (community/L2 reference) > AI-generated coding standard summary (L3 fallback)

### G43 Professional Risk Identification

- **Definition**: One of the pre-analysis SKILL's radiating domains -- analyzes the target profession's unique risk lineage (physical/psychological/social/ethical/technical), evaluates probability and severity, constructs early warning and mitigation strategies
- **Domain**: Architecture Domain
- **Example**: Target profession "Psychological Counselor" -> Risk lineage: psychological (client suicide risk assessment), ethical (confidentiality boundaries), social (multiple relationship conflicts) -> Early warning: self-harm risk triggered -> MUST refer

### G44 Professional Ethics Norms

- **Definition**: One of the pre-analysis SKILL's radiating domains -- consults the target profession's ethical norm system, distinguishes positive obligations from negative constraints, defines practice boundaries (what can be done, what must be referred)
- **Domain**: Architecture Domain
- **Example**: Lawyer professional ethics: positive obligations (diligence, confidentiality), negative constraints (no conflict of interest representation) -> Practice boundary: may provide legal information, may not issue legal opinions

### G45 System Cognition

- **Definition**: One of the pre-analysis SKILL's radiating domains -- internalizes UR-SKILL core methodology (Complexity Decision Tree / Anti-Patterns / RFC 2119 / Checklists), detects anti-patterns and distinguishes capability domains from workflow aliases. Among the 6 domains, the only one oriented toward the UR-SKILL internal system
- **Domain**: Architecture Domain
- **Example**: Detects that a generated SKILL writes the workflow step "Research" as a radiating domain -> System Cognition triggers Anti-Pattern 4 (Architecture Confusion) alert, marks and requires remediation

---

#### 1.2 File Type Classification

### G46 K1 Domain Knowledge

- **Definition**: First subtype of knowledge-type reference files -- concepts, rules, methodologies, containing no executable code
- **Domain**: Architecture Domain
- **Example**: `references/domain-knowledge.md` contains the target profession's core concepts, industry terminology, and standard workflows

### G47 K2 API/CLI Reference

- **Definition**: Second subtype of knowledge-type reference files -- structured reference of interface parameters, command syntax, configuration options
- **Domain**: Architecture Domain
- **Example**: `references/api-reference.md` contains Python `ast` module node type tables, `subprocess.run()` parameter descriptions

### G48 K3 Configuration/Policy Documents

- **Definition**: Third subtype of knowledge-type reference files -- organization-specific rules, policies, conventions
- **Domain**: Architecture Domain
- **Example**: `references/coding-standards.md` contains team-agreed naming conventions, directory structures, and Git commit message formats

### G49 K4 Design Patterns

- **Definition**: Fourth subtype of knowledge-type reference files -- reusable code/architecture patterns, templates
- **Domain**: Architecture Domain
- **Example**: `references/design-patterns.md` contains common code review patterns (e.g., "Security Review Five-Step Method") and architecture review templates

---

## 2. Workflow Domain

### G08 Review Dimension

- **Definition**: 6 review dimensions for workflow steps -- Goal Alignment, Fact Anchoring, Direction Calibration, Adversarial Validation, Blind Spot Identification, Impact Projection
- **Domain**: Workflow Domain
- **Example**: Critical checkpoints use all 6 dimensions; non-critical checkpoints use 3 dimensions (Goal Alignment, Fact Anchoring, Blind Spot Identification)

### G09 Critical Checkpoint

- **Definition**: Workflow steps where 6-dimension review is executed -- Research (Step 2), Architecture (Step 3), Verification (Step 5), Validation (Step 6)
- **Domain**: Workflow Domain
- **Example**: The Verify step (Step 5) is a verification checkpoint and MUST use all 6 dimensions regardless of complexity

### G10 Non-Critical Checkpoint

- **Definition**: Workflow steps where 3-dimension review is executed -- Pre-Analysis (Step 1), Execution (Step 4), Delivery (Step 7)
- **Domain**: Workflow Domain
- **Example**: The Pre-Analysis step only requires 3 review items: Goal Alignment, Fact Anchoring, Blind Spot Identification

### G11 Blind Spot Three-Tier Mechanism

- **Definition**: A progressive method for handling blind spots -- Tier 1 (Investigate and analyze -> Self-optimize), Tier 2 (Request resources -> Resource supplementation), Tier 3 (Output blind spot report -> Feasibility recommendations). Skipping tiers is prohibited
- **Domain**: Workflow Domain
- **Example**: Discovery of a capability domain gap -> Tier 1: web search industry standards -> Still insufficient -> Tier 2: request domain materials from user -> Still insufficient -> Tier 3 report: Actions attempted + Remaining blind spots + Feasibility recommendations

### G12 Loop Principle

- **Definition**: Workflow step checklist items not passed -> Execute remediation actions -> Re-inspect -> Proceed after passing. Skipping unconfirmed items is prohibited
- **Domain**: Workflow Domain
- **Example**: Anti-pattern scan of the Verify step fails -> Fix violating anti-patterns -> Re-scan -> Proceed to Validate step after passing

### G13 Gate

- **Definition**: Inspection checkpoint between workflow steps, composed of core command + checklist; release upon full confirmation
- **Domain**: Workflow Domain
- **Example**: Gating for the Parse step: Confirm that the information is sufficient to support complexity determination + all 4 checklist items passed -> Proceed to Research

### G14 Progressive Loading

- **Definition**: Three-layer loading strategy -- L1 Metadata (name+description, ~100 tokens / always loaded), L2 Body (loaded on activation, <5000 tokens), L3 Reference files (loaded on demand), controlling context window consumption
- **Domain**: Workflow Domain
- **Example**: UR-SKILL loads only frontmatter at startup -> loads body when user requests SKILL generation -> loads references/anti-patterns.md during verification

### G15 Primacy Zone / Recency Zone

- **Definition**: Body block strategy based on the LLM U-shaped attention curve -- Primacy Zone (first 20%) contains core constraints, Middle Zone (60%) contains indexes and paths, Recency Zone (last 20%) contains Double Prompting core rule repetition
- **Domain**: Workflow Domain
- **Example**: UR-SKILL body's Primacy Zone contains MUST/MUST NOT core rules, Recency Zone contains rule reiteration (Double Prompting)

### G50 Core Command

- **Definition**: A single-sentence confirmation statement at the end of each workflow step's action block, summarizing that step's completion-state deliverable; the semantic anchor of the gating mechanism -- the checklist verifies completion against the core command
- **Domain**: Workflow Domain
- **Example**: Step 4 (Execution) core command: "Confirm that a complete SKILL file package has been produced (SKILL.md + all references/ + scripts/ + assets/)"

### G51 Cognitive Operation

- **Definition**: A pure reasoning action marker (format: `[Cognitive Operation]`) that does not appear as a tool call, used to declare that the step is "thinking" rather than "invoking a tool." Parallel to tool actions (`[Read]`/`[Write]`/`[WebSearch]`). Cognitive operations use "Activate" to annotate capability domain tiers
- **Domain**: Workflow Domain
- **Example**: `[Cognitive Operation] Activate Tier 3 (Domain Integration) -> Map Requirements Engineering output to SKILL Architecture Design domain partitioning`

### G52 Complexity Decision Tree

- **Definition**: A decision mechanism that determines SKILL complexity (Simple/Medium/Complex) in the fixed order "Needs scripts -> Needs assets -> Needs multiple rounds -> Needs staging -> Otherwise." Complexity is determined by organizational and maintenance requirements, not by the number of capability domains
- **Domain**: Workflow Domain
- **Example**: Generated SKILL contains executable scripts (`scripts/validator.py`) -> First question "Needs scripts" hits -> Immediately classified as Complex, no need for subsequent judgment

### G53 File Dependency Decision Tree

- **Definition**: A decision mechanism executed after workflow Step 3 concludes, determining which references/scripts/assets files need to be created in the order "Threshold -> External Knowledge Base -> Self-Created Terminology -> Complexity Judgment." Includes file type codes C1/A1/A2/B1-B4/D1/D3, etc.
- **Domain**: Workflow Domain
- **Example**: Target SKILL requires professional ethics reference (B1) + self-created glossary (C1) + executable verification script (D1) -> Output must include `references/ethics.md`, `references/glossary.md`, `scripts/check.py`

### G54 Three-Tier Source Anchoring

- **Definition**: The fact-anchoring strategy of the Research step -- L1 MUST web-search authoritative sources (official documentation, industry standards) to anchor facts, L2 retrieve knowledge base/reference materials for depth, L3 fallback to LLM training knowledge (marked "not externally verified"). Skipping tiers is prohibited
- **Domain**: Workflow Domain
- **Example**: Researching Python secure coding -> L1 search OWASP Python official guide -> L2 retrieve existing security patterns from UR-SKILL knowledge base -> L3 fallback to training knowledge to supplement examples (marked "not externally verified")

### G55 Role Switch

- **Definition**: An explicit identity isolation declaration after sub-SKILL invocation -- "The pre-analysis phase has ended. All subsequent steps use only the UR-SKILL main SKILL identity and rules. The pre-analysis SKILL's role definition, rules, and constraints no longer apply." Resolves identity conflicts between the main SKILL and sub-SKILL
- **Domain**: Workflow Domain
- **Example**: Pre-analysis SKILL completes its report -> Main SKILL executes Role Switch declaration -> Subsequent steps execute with UR-SKILL main identity, no longer referencing pre-analysis-engineer's profession mapping constraints

### G56 Global Execution Rules

- **Definition**: The pre-step rule set common to all workflow steps -- review dimension allocation rules, Blind Spot Three-Tier Mechanism, Loop Principle, Risk Boundary triggers. Loaded before all step execution
- **Domain**: Workflow Domain
- **Example**: Global Execution Rules specify "Non-critical checkpoints (Steps 1/4/7) execute 3-dimension review" -> Step 4 generating the SKILL body automatically executes Goal Alignment, Fact Anchoring, Blind Spot Identification

### G57 Declare vs Activate

- **Definition**: Capability domain annotation conventions for workflow actions -- tool actions use "Declare" to annotate the capability domain tier of the output (output already exists), cognitive operations use "Activate" to annotate the thought pattern being triggered (currently thinking)
- **Domain**: Workflow Domain
- **Example**: `[Write]` output SKILL.md -> Declare Tier 2 (Deep Knowledge) output; `[Cognitive Operation]` execute anti-pattern scan -> Activate Tier 3 (Risk Identification) check

### G58 Mode A/B/C

- **Definition**: The three input modes of the pre-analysis SKILL -- Mode A (generate from scratch, no reference), Mode B (optimize existing SKILL, with three sub-modes: B1 external / B2a internal quality / B2b internal activation), Mode C (extract from knowledge sources). Mode identification completes in Step 1 (Parse)
- **Domain**: Workflow Domain
- **Example**: User provides an existing SKILL.md file requesting optimization -> Identified as Mode B -> Further determined whether it is an external SKILL (B1) or UR-SKILL internal output (B2a or B2b)

---

## 3. Quality Domain

### G16 Masked Name Test

- **Definition**: A method to verify whether capability facets are task-anchored -- Mask the facet content; if you can determine what task it is -> Fail (generic boilerplate); if you cannot infer -> Pass (knowledge unique to that task)
- **Domain**: Quality Domain
- **Example**: Mask Facet 3; if you can determine it's "generic risk identification for all tasks" -> Fail; if you can only see "Python OWASP Top 10 specific vulnerabilities" -> Pass

### G17 Anti-Pattern

- **Definition**: Standard software engineering term referring to practices that "appear correct but are actually harmful" -- the developer chose a practice with good intent, but the result is harmful. Distinct from "error"
- **Domain**: Quality Domain
- **Example**: Anti-pattern 4 Architecture Confusion -- with the good intent of "clearly expressing the task flow," workflow steps are written as radiating domains, causing capability matrix and workflow confusion

### G18 Placeholder Residue

- **Definition**: The presence of unfilled content such as `[xxx]`, `TODO`, `FIXME`, `{to be filled}` in the generated SKILL body, resulting in an incomplete deliverable
- **Domain**: Quality Domain
- **Example**: `[Insert review rules here]` appears in the body -> Anti-pattern 2 Placeholder Residue

### G19 Cross-Reference Self-Containment

- **Definition**: All "see...", "refer to...", "cf..." reference targets in the generated SKILL MUST exist within that SKILL's own file package; referencing UR-SKILL internal files (templates/, design-guides/, References/, design-rationale/) is prohibited
- **Domain**: Quality Domain
- **Example**: The generated SKILL body contains "see templates/capability-architecture-template.md" -> Violates self-containment rule; must be replaced with inline content from that SKILL's own references/

### G59 Capability Completeness Scan

- **Definition**: The core action of the Step 5 Verify phase -- domain-by-domain check of whether Step 4 output reaches the designed capability tier depth for each domain (Foundation -> Advanced -> Expert -> Extension), marks degradation causes, returns to Step 4 for remediation if designed depth is not met
- **Domain**: Quality Domain
- **Example**: Radiating domain "Quality Engineering" designed depth is Tier 3 (Expert) -> Step 4 output only covers Tier 2 (Advanced) -> Mark degradation "missing executable verification script" -> Return to Step 4

### G60 Domain Fusion Check

- **Definition**: The core action of the Step 5 Verify phase -- checks whether radiating domain outputs are complementary without overlap, cover the complete chain, and have clear boundaries between adjacent domains
- **Domain**: Quality Domain
- **Example**: "Requirements Engineering & Business Translation" output and "SKILL Architecture Design" output show capability coverage overlap (both describe workflow steps) -> Domain Fusion Check triggers boundary ambiguity warning

### G61 Mandatory Visualization

- **Definition**: A mandatory rule that when a SKILL task type triggers specific conditions (involving workflows/multi-component interaction/state transitions/Medium+ complexity), the output MUST include at least 1 Mermaid diagram
- **Domain**: Quality Domain
- **Example**: Generating a "Code Review SKILL" containing a 5-step workflow + 3 state transitions -> Mandatory output of workflow flowchart and state transition diagram

### G62 Decision Strategy

- **Definition**: Output specification for review-type SKILLs -- a decision table that automatically produces a verdict of "Reject / Needs Modification / Conditional Pass / Pass" based on the count of critical/high-severity issues
- **Domain**: Quality Domain
- **Example**: Security review finds 1 critical (SQL injection) -> Decision Strategy automatically outputs "Reject"; finds 2 high, 0 critical -> "Needs Modification"

### G63 Confirm-Fix-Verify Loop

- **Definition**: User interaction pattern for review/diagnostic SKILLs -- output issues -> user selects fixes -> verify after fix -> confirm, maximum 3 rounds
- **Domain**: Quality Domain
- **Example**: Code review finds 5 issues -> User fixes 3 high-severity -> Re-review verification -> Confirm pass or enter round 2 (max 3 rounds)

### G64 Troubleshooting Triad

- **Definition**: The mandatory three-element structure of troubleshooting entries -- Symptom (observable phenomenon), Root Cause (deep cause), Fix Action (executable steps). Pure declarative prompts are prohibited
- **Domain**: Quality Domain
- **Example**: T01: Symptom = generated SKILL's capability matrix identified as a workflow by GPT; Root Cause = radiating domain names use verb phrases ("Parse Requirements" instead of "Requirements Engineering"); Fix = rename radiating domains to noun phrases + execute Ordering Test

### G65 Fault Numbering

- **Definition**: The T{number} numbering system for fault diagnosis (e.g., T01, T02), parallel to anti-pattern numbering and rule numbering, facilitating cross-file referencing. Currently contains T01-T17
- **Domain**: Quality Domain
- **Example**: SKILL.md body writes "If capability domain confusion is encountered, see troubleshooting.md T04" -> Directly locates the target entry via the number

### G66 Specification Overreach (Anti-Pattern 1)

- **Definition**: The generated SKILL's capability declarations exceed its actual deliverable scope, resulting in runtime inability to fulfill promises
- **Domain**: Quality Domain
- **Example**: Declared capability includes "auto-fix all security vulnerabilities," but the actual workflow only contains static analysis and recommendations -- specification far exceeds implementation

### G67 Example Pollution (Anti-Pattern 3)

- **Definition**: Example content contains insecure patterns, outdated practices, or code contradicting the rule system, causing the model to learn incorrect behavior
- **Domain**: Quality Domain
- **Example**: SKILL example uses `eval()` to process user input, but the SKILL rule system explicitly prohibits dynamic execution -- example contradicts the rules

### G68 Architecture Confusion (Anti-Pattern 4)

- **Definition**: The capability matrix's radiating domains are aliases for workflow steps, causing the capability matrix to become a mirror of the workflow. The number one anti-pattern of UR-SKILL
- **Domain**: Quality Domain
- **Example**: Radiating domain list is "Parse -> Research -> Design -> Generate -> Verify -> Deliver," mapping one-to-one with the 6 workflow steps -- classic Architecture Confusion

### G69 Review Deficiency (Anti-Pattern 5)

- **Definition**: The generated SKILL workflow has an insufficient number of review checks -- critical checkpoints have fewer than 6 dimensions, quality checks are ineffective
- **Domain**: Quality Domain
- **Example**: Generated SKILL's critical checkpoint (Verify step) only contains 3 review dimensions (Goal Alignment, Fact Anchoring, Blind Spot Identification), missing Direction Calibration, Adversarial Validation, Impact Projection

### G70 Blind Spot Evasion (Anti-Pattern 6)

- **Definition**: Blind spot identification only writes "limitations noted" without executing investigation per the Three-Tier Mechanism -- jumps directly from Tier 1 to Tier 3 (purely declarative)
- **Domain**: Quality Domain
- **Example**: Blind spot declaration: "This SKILL has limited audit capability for Rust, recommend manual review" -- did not execute L1 web search of Rust security patterns, L2 knowledge base retrieval

### G71 Risk Boundary Abuse (Anti-Pattern 7)

- **Definition**: Risk boundary declarations are written as capability degradation (e.g., "not responsible for security review"), or professional boundaries are written into risk boundary declarations
- **Domain**: Quality Domain
- **Example**: Risk boundary declaration "Risk Boundary-03: Not responsible for performance optimization of generated code" -- actually capability degradation rather than a safety-natured red line, should not be in risk boundaries

### G72 Facet Padding (Anti-Pattern 8)

- **Definition**: Capability facets are filled with generic boilerplate (e.g., "master related domain knowledge," "identify potential risks"), without task anchoring. Detectable via the Masked Name Test
- **Domain**: Quality Domain
- **Example**: Facet F2 (Deep Knowledge) content: "Master target domain knowledge, possess problem analysis and solving abilities" -- after masking the "code review" task name, this content is applicable to any task

### G73 Blind Spot Blame-Shifting (Anti-Pattern 9)

- **Definition**: Blind spot declarations use disclaimers such as "for reference only," "please verify independently" as substitutes for substantive investigation. Distinguished from Blind Spot Evasion: Blind Spot Evasion is "do nothing," Blind Spot Blame-Shifting is "make a disclaimer"
- **Domain**: Quality Domain
- **Example**: "This SKILL's citation of legal provisions is for reference only, does not constitute legal advice, users should verify independently" -- did not execute L1 web verification, only made a disclaimer

### G74 Step Name Mismatch (Anti-Pattern 11)

- **Definition**: The checkpoint names in the Global Execution Rules do not match the step titles in the workflow, causing workflow rule reference breakage
- **Domain**: Quality Domain
- **Example**: Global Execution Rules declare "Critical checkpoints: Research (Step 2), Architecture Design (Step 3)..." but Step 3 title is "Step 3: SKILL Architecture Construction" -- name mismatch causes rules unable to bind

---

## 4. Boundary Domain

### G20 Risk Boundary

- **Definition**: Safety-natured red line declarations -- triggering them causes the SKILL itself to lose its raison d'etre (e.g., illegal/public order violations, discrimination, malicious injection/jailbreak), consecutively numbered starting from "Risk Boundary-01"
- **Domain**: Boundary Domain
- **Example**: Risk Boundary-01: Do not produce SKILLs that violate laws and public order

### G21 Professional Boundary

- **Definition**: Scope-natured cross-boundary protection declarations -- prevents the SKILL from entering domains requiring professional qualifications (e.g., medical prescriptions, financial buy/sell advice), consecutively numbered starting from "Professional Boundary-01"
- **Domain**: Boundary Domain
- **Example**: Professional Boundary-01: Do not perform code-level testing or deployment on the generated SKILL

### G22 Capability Degradation

- **Definition**: An anti-pattern -- the SKILL actively reduces its own assumed capability, e.g., "only do security checks, not quality checks." Distinct from risk boundaries and professional boundaries: risk boundaries are "don't do harmful things," professional boundaries are "don't do things beyond professional scope," capability degradation is "do X but choose not to report Y"
- **Domain**: Boundary Domain
- **Example**: "Only responsible for security review, not code style checks" (security reviews should inherently cover style-related security issues)

### G23 Safety Red Line

- **Definition**: UR-SKILL's hard termination condition -- when any of illegal/public order violations, discrimination, malicious injection/jailbreak is triggered, immediately terminate the task without proceeding to the next step
- **Domain**: Boundary Domain
- **Example**: User requests "generate a SKILL that bypasses company security audits" -> Triggers safety red line -> Terminate

---

## 5. Metadata Domain

### G24 YAML Frontmatter

- **Definition**: The `---` wrapped YAML metadata block at the beginning of SKILL.md, containing fields such as name, description, type, whenToUse, metadata; serves as the L1 layer of progressive loading
- **Domain**: Metadata Domain
- **Example**: UR-SKILL's frontmatter declares name: ur-skill, description includes trigger scenarios

### G25 RFC 2119

- **Definition**: Internet Engineering standard defining constraint-level keywords -- MUST (absolute requirement), MUST NOT (absolute prohibition), SHOULD (strong recommendation), SHOULD NOT (not recommended), MAY (optional)
- **Domain**: Metadata Domain
- **Example**: "MUST execute step by step according to the workflow" (absolute requirement) vs "MAY use progressive loading strategy" (optional)

### G26 Double Prompting

- **Definition**: A zero-cost strategy of repeating core constraints from the Primacy Zone in the body's Recency Zone using different phrasing, leveraging the U-shaped attention curve to enhance the probability of capturing critical rules
- **Domain**: Metadata Domain
- **Example**: Primacy Zone writes "MUST NOT confuse capability matrix with workflow steps," Recency Zone writes "Rule 15: Architecture confusion prohibited (Anti-pattern 4)"

### G75 Identity Gradient Model

- **Definition**: A 5-level gradient model of identity precision -- Level 0 (no identity) to Level 5 (Role + Domain Expertise + Methodology + Style + Tool Constraints); the generated SKILL MUST reach at least Level 3 (Role + Domain Expertise + Methodology)
- **Domain**: Metadata Domain
- **Example**: Level 3 identity declaration: "You are a Python Security Audit Expert (Role), proficient in OWASP Top 10 and CWE (Domain Expertise), following the Black-box -> Gray-box -> White-box progressive audit methodology (Methodology)"

### G76 Methodology Filling Effect

- **Definition**: When specific domains and methodologies are described in the identity declaration, the LLM automatically "fills in" the subdivided knowledge that the role should possess -- no need to explicitly enumerate all skills. Fabricating years of experience has the opposite effect
- **Domain**: Metadata Domain
- **Example**: Declaring "You are a security architect with incident response experience" -> LLM automatically fills in threat modeling, attack chain analysis, etc.; no need to add "You master STRIDE, MITRE ATT&CK..."

### G77 Dual Anchoring Strategy

- **Definition**: A body block strategy leveraging the LLM U-shaped attention curve -- Primacy Zone (first 20%) contains core constraints, Middle Zone (60%) contains indexes and paths, Recency Zone (last 20%) contains Double Prompting rule repetition
- **Domain**: Metadata Domain
- **Example**: UR-SKILL body Primacy Zone contains MUST/MUST NOT core constraints -> Middle Zone contains step workflow -> Recency Zone repeats core constraints in different phrasing (Double Prompting)

### G78 Lost in the Middle Effect

- **Definition**: The phenomenon where LLM information capture rate for content in the middle of a context is significantly lower than at the two ends -- the foundational assumption behind Progressive Loading (G14), Primacy/Recency Zones (G15), Double Prompting (G26), and the body 500-line cap
- **Domain**: Metadata Domain
- **Example**: Placing key constraints in the body middle (lines 200-300) -> Due to the Lost in the Middle Effect, the LLM's compliance rate for those constraints is significantly lower than the same constraints placed in the Primacy or Recency Zone

---

## 6. Delivery Domain

### G27 Information Density

- **Definition**: The effective information per token in SKILL Markdown content -- removing formulaic padding, avoiding redundant declarations, each sentence conveying independent information. Not quantifiable (no universal formula), but detectable by removing prefixes like "as is well known," "it should be noted that"
- **Domain**: Delivery Domain
- **Example**: Remove "One important thing to note here is that efficiency should be maintained" -> Change to "MUST keep body < 500 lines"

### G28 Complexity

- **Definition**: The organizational and maintenance requirement level of a SKILL -- Simple (single file), Medium (references/ + staged workflow), Complex (scripts/ + assets/ + multi-round iteration), determined by dimensions such as executable scripts, static assets, iteration loops
- **Domain**: Delivery Domain
- **Example**: UR-SKILL determines the target SKILL requires "executable scripts" -> Complex complexity -> Output must include scripts/ + assets/ + references/

### G29 pre-analysis-engineer

- **Definition**: UR-SKILL's mandatory pre-analysis sub-SKILL that automatically completes requirements parsing, domain derivation, complexity determination, and file dependency decisions, outputting a pre-analysis report. Supports three input modes: A (generate from scratch), B (optimize existing SKILL), C (extract from knowledge sources). Capability matrix contains 5 radiating domains (Requirements Engineering / Job Capability Analysis / Professional Risk Identification / Professional Ethics Norms / System Cognition)
- **Domain**: Delivery Domain
- **Example**: Step 1 Parse (Pre-analysis) -> Invoke pre-analysis-engineer to perform three-mode identification, 6-dimension review, output pre-analysis report

### G79 Tool Binding

- **Definition**: A mandatory rule that every executable action in the workflow MUST be syntactically bound to at least one concrete tool (format: `[ToolName] Action -> Output`); abstract action descriptions without tool binding are prohibited
- **Domain**: Delivery Domain
- **Example**: `[Write] Write capability matrix analysis to references/capability-analysis.md -> Output: capability domain partitioning plan`, rather than "save the analysis results"

### G80 Fallback Chain

- **Definition**: The fault-tolerance mechanism for tool calls -- provides a chained fallback scheme of Fallback 1 -> Fallback 2 -> Last Resort for the primary tool. Non-degradable baseline operations (e.g., git diff for code review) terminate on failure
- **Domain**: Delivery Domain
- **Example**: Primary `WebSearch` web search -> Fallback 1: `WebFetch` direct fetch of known URL -> Fallback 2: search local knowledge base -> Last Resort: fallback to training knowledge (marked "not externally verified")

---

## 7. Model Format Domain

### G30 Model Format Adaptation

- **Definition**: Adjusting the structural syntax of a generated SKILL to match the formatting preferences of the target platform (Claude -> XML tags, ChatGPT -> Markdown + delimiters, Gemini -> PTCF framework). Only affects section headings, delimiters, and output format specifications; does NOT change capability matrix, workflow logic, or rule systems.
- **Domain**: Model Format Domain
- **Example**: User says "generate for Claude" -> adapt generated SKILL from default Markdown to XML tag structure (`<role>`, `<instructions>`, `<output_format>`); capability matrix and workflow steps remain unchanged.

### G31 Default Format

- **Definition**: UR-SKILL's baseline output format: standard Markdown (ATX headings `#`, RFC 2119 keywords `**MUST**`, Markdown tables, triple-backtick code blocks, `- [ ]` checklists). Used when the user has not specified a target platform or when cross-model portability is required.
- **Domain**: Model Format Domain
- **Example**: User provides requirement without mentioning target platform -> generate SKILL in default Markdown format. "Claude eats XML, ChatGPT eats Markdown, Gemini eats PTCF" -- when no platform specified, Markdown is the safest default.

---

## Reference Index (by file)

| File | Involved Glossary IDs |
|:---|:---|
| SKILL.md body | G01-G04, G06-G15, G17-G80 |
| templates/capability-architecture-template.md | G01-G07, G39-G45 |
| templates/workflow-template.md | G08-G14, G50-G58, G79-G80 |
| templates/rules-template.md | G20-G22, G25 |
| design-rationale/design-rationale.md | G05, G14, G27, G28, G32-G38 |
| References/anti-patterns.md | G17, G18, G22, G66-G74 |
| References/troubleshooting.md | G01-G03, G17, G64-G65 |
| design-guides/structure-guideline.md | G15, G25-G27, G75-G78 |
| design-guides/boundary-design-guide.md | G20-G23, G71 |
| design-guides/model-format-adaptation-design-guide.md | G30-G31 |
