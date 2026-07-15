# Glossary

> **Purpose**: Conceptual anchor points for the UR-SKILL system — unify term semantics across all files.
> **Core Principle**: The glossary serves as the "semantic protocol" within the system — the same term in all files (SKILL.md body, templates/, design-guides/, References/) points to the same concept.

---

## 1. Architecture Domain

### G01 Capability Matrix

- **Definition**: A structured capability expression consisting of 1 Core Domain + 3-8 Radiating Domains × 4 Depth Layers (Foundation → Advanced → Expert → Extension)
- **Domain**: Architecture Domain
- **Example**: UR-SKILL's capability matrix includes "Core: SKILL Generation Engineering" + 6 radiating domains (Requirements Engineering & Business Translation, SKILL Architecture Design, Prompt System Engineering, Quality Engineering, Ethics & Safety, Iterative Improvement), each with 4 layers

### G02 Core Domain

- **Definition**: The professional dimension of the task, carrying the capability facets (Facet 1-6); the only mandatory domain in the capability matrix
- **Domain**: Architecture Domain
- **Example**: UR-SKILL's core domain is "SKILL Generation Engineering"; Facet 2 Knowledge Deepening declares "Mastery of Prompt Engineering, Markdown standards"

### G03 Radiating Domain

- **Definition**: Independent professional capability dimensions surrounding the core domain; each domain is an independent capability domain, not a workflow step
- **Domain**: Architecture Domain
- **Example**: UR-SKILL's 6 radiating domains: Requirements Engineering & Business Translation, SKILL Architecture Design, Prompt System Engineering, Quality Engineering, Ethics & Safety, Iterative Improvement

### G04 Capability Facet

- **Definition**: 6 capability dimensions targeting only the core domain (Efficiency & Cost, Knowledge Deepening, Risk Identification, Quality Inspection, Domain Fusion, System-Wide Perspective); describe the capability characteristics the core domain must possess
- **Domain**: Architecture Domain
- **Example**: Facet 3 Risk Identification declares "Sniff anti-patterns and architecture confusion in SKILL generation"

### G05 Capability Depth (4 Layers)

- **Definition**: 4 progressive layers for each capability domain (Foundation → Advanced → Expert → Extension); all capabilities must have 4 layers, cannot be reduced
- **Domain**: Architecture Domain
- **Example**: Core domain's 4 layers: Extract goals/domains/delivery forms → Infer implicit requirements/identify domains → Prioritize requirements/multi-source fusion → Infer requirement patterns

### G06 Sort Test

- **Definition**: A method to verify whether a radiating domain is actually a workflow step — rearrange candidate domains; if the logic breaks after reordering, they are workflow steps, not independent capability domains
- **Domain**: Architecture Domain / Quality Domain
- **Example**: Candidate domains A "Parse Requirements" → B "Retrieve Information" → C "Generate Report": reordering to C → A → B breaks logic → they are workflow steps

### G07 Three-Question Filter

- **Definition**: A method to validate candidate capability domains — Independence (can it exist independently?), Irreplaceability (can it be replaced by other domains?), Complementarity (is it complementary with no overlap with other domains?)
- **Domain**: Architecture Domain / Quality Domain
- **Example**: Questioning the "Security Audit" candidate: Can it exist independently? (Yes) Irreplaceable? (Yes) Complementary to existing domains? (Yes) → Passed

---

#### 1.1 Capability Domain Names

### G32 SKILL Generation Engineering

- **Definition**: The core domain of the UR-SKILL master SKILL — transforming vague requirements into standardized, executable, and verifiable SKILL.md file packages. Carries 6 capability facets (Efficiency & Cost, Knowledge Deepening, Risk Identification, Quality Inspection, Domain Fusion, System-Wide Perspective)
- **Domain**: Architecture Domain
- **Example**: User proposes a vague requirement "make a code review SKILL" → SKILL Generation Engineering transforms it into a standardized SKILL.md package with capability matrix, 6-step workflow, and rule system

### G33 Requirements Engineering & Business Translation

- **Definition**: One of UR-SKILL's radiating domains — transforming vague intent into structured requirements, mapping business goals to SKILL capabilities, identifying implicit assumptions and unstated constraints
- **Domain**: Architecture Domain
- **Example**: User says "help me make a tool that checks code quality" → Requirements Engineering identifies implicit assumptions (target language, check scope, output format) and maps to quality review capability domain

### G34 SKILL Architecture Design

- **Definition**: One of UR-SKILL's radiating domains — capability matrix design, domain independence verification (Sort Test + Three-Question Filter), conflict identification, niche analysis, architecture extensibility
- **Domain**: Architecture Domain
- **Example**: Perform Sort Test and Three-Question Filter on candidate radiating domain "Code Style Check" to determine whether it is an independent capability domain or a workflow step

### G35 Prompt System Engineering

- **Definition**: One of UR-SKILL's radiating domains — information architecture (Primacy/Recency), RFC 2119 rule system, attention management, tool binding syntax, progressive loading strategy
- **Domain**: Architecture Domain
- **Example**: When designing body structure, place MUST-level constraints in the primacy zone (first 20%), place double prompting reminders in the recency zone (last 20%), and place indexes and paths in the middle 60%

### G36 Quality Engineering

- **Definition**: One of UR-SKILL's radiating domains — anti-pattern detection, boundary validation, completeness checking, cross-reference consistency, executable script validation
- **Domain**: Architecture Domain
- **Example**: The validation step (Step 10) performs 11 anti-pattern scans on the generated SKILL (specification overreach, example contamination, architecture confusion, etc.); if not passed, return for fixes

### G37 Ethics & Safety

- **Definition**: One of UR-SKILL's radiating domains — risk boundaries (illegal/discriminatory/injection), occupation-specific risk profiling, professional boundaries, safety guardrail design
- **Domain**: Architecture Domain
- **Example**: User requests generation of a "Medical Diagnosis SKILL" → Ethics & Safety recognizes the request touches a professional boundary (requires medical license), flags it as Professional Boundary-01 and sets guardrails

### G38 Iterative Improvement

- **Definition**: One of UR-SKILL's radiating domains — platform adaptation, blind-spot feedback self-healing, metadata optimization, model-specific format adaptation, version evolution and backward compatibility
- **Domain**: Architecture Domain
- **Example**: A generated SKILL tested on the Claude platform reveals excessive XML nesting depth → Iterative Improvement adjusts the tag structure while preserving semantics

### G39 Investigation Analysis & Domain Research Engineering (formerly "Pre-Analysis Engineering")

- **Definition**: The core domain of the research-analyst sub-SKILL — automatically performs requirements parsing, occupation mapping, domain derivation, file dependency decisions, cross-system mapping (Pattern D), and outputs a standardized pre-analysis report. Carries 6 capability facets with 8 radiating domains (A-H)
- **Domain**: Architecture Domain
- **Example**: User inputs "I want to create a lawyer assistant SKILL" → Investigation Analysis completes: occupation mapping (lawyer), 8-domain derivation, file dependency decision (needs B1 professional ethics document), outputs pre-analysis report

### G40 Requirements Engineering

- **Definition**: One of research-analyst's radiating domains — identify core task objectives and problem domain boundaries, extract structured information, identify implicit assumptions, predict requirement evolution paths. Distinguished from the master SKILL's "Requirements Engineering & Business Translation": one analyzes requirement structure, the other translates requirements into SKILL architecture
- **Domain**: Architecture Domain
- **Example**: For a "Code Review SKILL" requirement, Requirements Engineering extracts: core objective = quality gate, problem domain boundary = incremental code review, implicit assumption = user already has code repository access

### G41 Job Competency Analysis

- **Definition**: One of research-analyst's radiating domains — analyzes the target occupation's core competency domains and work characteristics based on the KSAO model (Knowledge/Skills/Abilities/Other characteristics), judges cross-domain capability dependencies, and provides occupational anchor points for domain derivation
- **Domain**: Architecture Domain
- **Example**: Analyzing the "Software Architect" role → core KSAO: system design knowledge, trade-off decision skills, cross-team communication ability → derive radiating domains: architecture patterns, technology selection, quality attributes

### G42 Information Source Assessment

- **Definition**: One of research-analyst's radiating domains — distinguishes information source types and authority levels (official standards/community content/AI-generated), evaluates timeliness and domain applicability, detects AI-generated content and conflicts of interest. Forms the theoretical basis for the three-level source anchoring
- **Domain**: Architecture Domain
- **Example**: Searching for Python coding standards → source assessment: PEP 8 (official standard/L1 authority) > Real Python tutorial (community/L2 reference) > AI-generated coding standard summary (L3 fallback)

### G43 Occupational Risk Identification

- **Definition**: One of research-analyst's radiating domains — analyzes the unique risk spectrum of the target occupation (physical/psychological/social/ethical/technical), assesses probability and severity, constructs warning and mitigation strategies
- **Domain**: Architecture Domain
- **Example**: Target occupation "Psychologist" → risk spectrum: psychological (suicide risk assessment of clients), ethical (confidentiality boundaries), social (multiple relationship conflicts) → warning: self-harm risk detected → MUST refer out

### G44 Professional Ethics Standards

- **Definition**: One of research-analyst's radiating domains — reviews the target occupation's ethics framework, distinguishes positive duties from negative constraints, defines practice boundaries (what can be done vs. what must be referred out)
- **Domain**: Architecture Domain
- **Example**: Lawyer professional ethics: positive duties (diligence, confidentiality), negative constraints (no conflict of interest representation) → practice boundary: can provide legal information, cannot issue legal opinions

### G45 System Cognition

- **Definition**: One of research-analyst's radiating domains — internalizes the UR-SKILL core methodology (anti-patterns/RFC 2119/checklist), detects anti-patterns and distinguishes capability domains from workflow step aliases. The only domain oriented toward UR-SKILL internals among the 6 domains
- **Domain**: Architecture Domain
- **Example**: Detecting that a generated SKILL writes a workflow step "Research" as a radiating domain → System Cognition triggers Anti-pattern 4 (Architecture Confusion) alert, flags and requires fix

---

#### 1.2 File Type Classification

### G46 K1 Domain Knowledge

- **Definition**: The first subtype of knowledge-type reference files — concepts, rules, methodologies; does not contain executable code
- **Domain**: Architecture Domain
- **Example**: `references/domain-knowledge.md` contains the target occupation's core concepts, industry terminology, and standard workflows

### G47 K2 API/CLI Reference

- **Definition**: The second subtype of knowledge-type reference files — structured references for interface parameters, command syntax, configuration options
- **Domain**: Architecture Domain
- **Example**: `references/api-reference.md` contains Python `ast` module node type table, `subprocess.run()` parameter descriptions

### G48 K3 Configuration/Policy Documents

- **Definition**: The third subtype of knowledge-type reference files — organization-specific rules, policies, conventions
- **Domain**: Architecture Domain
- **Example**: `references/coding-standards.md` contains team-agreed naming conventions, directory structure, and Git commit message format

### G49 K4 Design Patterns

- **Definition**: The fourth subtype of knowledge-type reference files — reusable code/architecture patterns, templates
- **Domain**: Architecture Domain
- **Example**: `references/design-patterns.md` contains common code review patterns (e.g., "Security Review Five-Step Method") and architecture review templates

---

## 2. Workflow Domain

### G08 Review Dimension

- **Definition**: 6 inspection dimensions for workflow steps — Goal Alignment, Fact Anchoring, Direction Calibration, Adversarial Validation, Blind Spot Identification, Impact Projection
- **Domain**: Workflow Domain
- **Example**: Critical nodes use all 6 dimensions; non-critical nodes use 3 dimensions (Goal Alignment, Fact Anchoring, Blind Spot Identification)

### G09 Critical Node

- **Definition**: Workflow steps that execute 6-dimension review, divided into two subcategories — decision-type sub-nodes (Research, Planning) and gate-type sub-nodes (Validation, Verification, Loop Decision), all executing all 6 dimensions: Goal Alignment, Fact Anchoring, Direction Calibration, Adversarial Validation, Blind Spot Identification, Impact Projection
- **Domain**: Workflow Domain
- **Example**: The Validation step (Step 10) is a gate-type critical node, must use all 6 dimensions; the Planning step (Step 5) is a decision-type critical node, all 6 dimensions active

### G10 Non-Critical Node

- **Definition**: Workflow steps that execute 3-dimension review — execution-type sub-nodes (Parse, Coordinate, Dispatch, Consolidate, Execute, Assemble), executing 3 dimensions: Goal Alignment, Fact Anchoring, Blind Spot Identification
- **Domain**: Workflow Domain
- **Example**: The Parse step only requires 3 checklist items: Goal Alignment, Fact Anchoring, Blind Spot Identification

### G11 Blind Spot Three-Layer Mechanism

- **Definition**: A progressive method for handling blind spots — Layer 1 (Investigation → self-optimization), Layer 2 (Request resources → resource supplementation), Layer 3 (Output blind-spot report → feasibility recommendations). Skipping layers is prohibited
- **Domain**: Workflow Domain
- **Example**: Capability domain gap found → Layer 1: web research on industry standards → still insufficient → Layer 2: request domain materials from user → still insufficient → Layer 3: report: attempted actions + remaining blind spots + feasibility recommendations

### G12 Loop Cycle Principle

- **Definition**: When a checklist item in a workflow step fails → perform corrective action → re-check → proceed only after passed. Skipping unconfirmed items is prohibited
- **Domain**: Workflow Domain
- **Example**: Anti-pattern scan in Validation step fails → fix the violating anti-pattern → re-scan → proceed to Verification step after passing

### G13 Gate

- **Definition**: Checkpoints between workflow steps, consisting of core commands + checklists; all must be confirmed for passage
- **Domain**: Workflow Domain
- **Example**: Parse step gate: confirm information is sufficient to support domain judgment + all 4 checklist items passed → proceed to Research

### G14 Progressive Loading

- **Definition**: Three-layer loading strategy — L1 metadata (name+description, ~100 tokens/always loaded), L2 body (loaded on activation, <5000 tokens), L3 reference files (on-demand loading); controls context window consumption
- **Domain**: Workflow Domain
- **Example**: UR-SKILL loads only frontmatter on startup → loads body when user requests SKILL generation → loads references/anti-patterns.md during validation

### G15 Dual Anchoring Strategy (Primacy Zone / Recency Zone)

- **Definition**: A body content strategy based on the LLM U-shaped attention curve (see G78 Lost in the Middle Effect) — primacy zone (first 20%) holds core constraints (MUST/MUST NOT), middle zone (60%) holds indexes and paths, recency zone (last 20%) rephrases core constraints from the primacy zone (see G26 Double Prompting), forming "dual anchoring" to ensure key rules are captured at both ends
- **Domain**: Workflow Domain
- **Example**: UR-SKILL body places MUST/MUST NOT core rules in the primacy zone, and rule restatements (Double Prompting) in the recency zone — primacy + recency dual anchoring ensures Lost in the Middle does not lose core constraints

### G50 Core Command

- **Definition**: A single-sentence completion declaration at the end of each workflow step's action block, summarizing the step's deliverable status; serves as the semantic anchor of the gate mechanism — the checklist verifies completeness against the core command
- **Domain**: Workflow Domain
- **Example**: Step 9 (Execute) core command: "Confirmed: complete SKILL file package produced (SKILL.md + all references/ + Scripts/ + assets/)"

### G51 Cognitive Operation

- **Definition**: A pure reasoning action marker that does not appear as a tool call (format: `[Cognitive Operation]`); used to declare that the step is "thinking" rather than "calling a tool". Parallel with tool actions (`[Read]`/`[Write]`/`[WebSearch]`). Cognitive Operations use "activate" to annotate capability domain levels
- **Domain**: Workflow Domain
- **Example**: `[Cognitive Operation] Activate Layer 3 (Domain Fusion) → Map requirements engineering output to SKILL architecture design domain partitioning`

### G52 Tool Action Marker

- **Definition**: An action annotation format parallel to G51 (Cognitive Operation) — `[ToolName] Operation → Output`; used to mark executable actions in the workflow that appear as tool calls. Together with G51 they form the action annotation system: G51 marks "thinking" (Cognitive Operation), G52 marks "calling a tool" (Tool Action)
- **Domain**: Workflow Domain
- **Example**: `[Write] Write capability matrix analysis → Output: capability domain partitioning plan` uses G52 Tool Action Marker; `[Cognitive Operation] Activate Layer 3 → Map requirements to domain partitioning` uses G51 Cognitive Operation

### G53 File Dependency Decision Tree

- **Definition**: A decision mechanism executed in workflow Step 5 (Planning), determining which references/scripts/assets files need to be created, following the order: "threshold → external knowledge base → custom terms → complex judgment". Includes file type codes such as C1/A1/A2/B1-B4/D1/D3
- **Domain**: Workflow Domain
- **Example**: Target SKILL needs professional ethics reference (B1) + custom glossary (C1) + executable validation script (D1) → output must include `references/ethics.md`, `references/glossary.md`, `scripts/check.py`

### G54 Three-Level Source Anchoring

- **Definition**: Fact anchoring strategy for the Research step — L1 MUST web search for authoritative sources (official docs, industry standards) to anchor facts, L2 search knowledge base/reference materials for depth, L3 fallback to LLM training knowledge (annotated "not externally validated"). Skipping levels is prohibited
- **Domain**: Workflow Domain
- **Example**: Researching Python secure coding → L1 search OWASP Python official guide → L2 retrieve UR-SKILL knowledge base for existing security patterns → L3 fallback to training knowledge for supplementary examples (annotated "not externally validated")

### G55 Role Switch

- **Definition**: An explicit identity isolation declaration after sub-SKILL invocation — "Pre-analysis phase complete. All subsequent steps use only the UR-SKILL master SKILL's identity and rules. The research-analyst's role definition, rules, and constraints no longer apply." Resolves identity conflicts between master and sub-SKILLs
- **Domain**: Workflow Domain
- **Example**: After research-analyst completes its report → master SKILL executes role switch declaration → subsequent steps execute using UR-SKILL master identity, no longer referencing research-analyst's occupation mapping constraints

### G56 Global Execution Rules

- **Definition**: A set of pre-rules shared by all workflow steps — review dimension allocation rules, blind-spot three-layer mechanism, Loop cycle principle, risk boundary triggers. Loaded before all step execution
- **Domain**: Workflow Domain
- **Example**: Global execution rules state "execution-type nodes (Parse/Coordinate/Dispatch/Consolidate/Execute/Assemble) execute 3-dimension review" → Step 9 (Generate SKILL body) automatically executes Goal Alignment, Fact Anchoring, Blind Spot Identification

### G57 Declare vs. Activate

- **Definition**: Convention for annotating capability domain levels in workflow actions — tool actions use "declare" to annotate the capability level of the output (output already exists), cognitive operations use "activate" to annotate the triggered thinking pattern (in the process of thinking)
- **Domain**: Workflow Domain
- **Example**: `[Write] Output SKILL.md → Declare Layer 2 (Knowledge Deepening) output; [Cognitive Operation] Execute anti-pattern scan → Activate Layer 3 (Risk Identification) check`

### G58 Pattern A/B/C/D

- **Definition**: Four input modes for research-analyst — Pattern A (Generate from scratch, no reference), Pattern B (Optimize existing SKILL, with sub-patterns B1 external/B2a internal quality/B2b internal activation), Pattern C (Extract from knowledge source), Pattern D (Localization adaptation, converting external non-UR-SKILL system SKILLs into UR-SKILL format). Pattern identification completes in Step 1 (Parse); Pattern D activates Domain H (Cross-System Mapping)
- **Domain**: Workflow Domain
- **Example**: User provides existing SKILL.md requiring optimization → identified as Pattern B → further determine whether external SKILL (B1) or UR-SKILL internal output (B2a or B2b); user provides external Claude Code SKILL → identified as Pattern D (localization adaptation), activates Domain H

---

## 3. Quality Domain

### G16 Veil Test

- **Definition**: A method to verify whether a capability facet has task anchoring — cover the facet content; if you can still identify the task → unqualified (generic boilerplate); if you cannot infer → qualified (task-specific knowledge)
- **Domain**: Quality Domain
- **Example**: Covering Facet F3: if you can identify it as "generic risk identification for all tasks" → unqualified; if you only see "Python OWASP Top 10 specific vulnerabilities" → qualified

### G17 Anti-Pattern

- **Definition**: A standard software engineering term referring to a "seemingly correct but actually harmful" practice — the developer chose an approach with good intentions but the result is harmful. Distinguished from "errors"
- **Domain**: Quality Domain
- **Example**: Anti-pattern 4 Architecture Confusion — with good intentions of "clearly expressing the task flow", workflow steps are written as radiating domains, causing confusion between capability matrix and workflow

### G18 Placeholder Residue

- **Definition**: Unexecuted filler content such as `[xxx]`, `TODO`, `FIXME`, `{to be filled}` present in the generated SKILL body, resulting in incomplete deliverables
- **Domain**: Quality Domain
- **Example**: Body contains `[Insert review rules here]` → Anti-pattern 2 Placeholder Residue

### G19 Cross-Reference Self-Containment

- **Definition**: All targets of "see...", "refer to...", "cf..." references in a generated SKILL must exist within that SKILL's own file package; references to UR-SKILL internal files (templates/, design-guides/, References/, design-rationale/) are prohibited
- **Domain**: Quality Domain
- **Example**: Generated SKILL body contains "see templates/capability-architecture-template.md" → violates self-containment rule, must be replaced with inlined content from that SKILL's own references/

### G59 Capability Completion Scan

- **Definition**: A core action in the Validation step (Step 10) — checks whether Step 9 (Execute) output reaches each domain's designed capability depth (Foundation → Advanced → Expert → Extension), marks downgrade reasons; if design depth is not reached, return to Step 9 for fix
- **Domain**: Quality Domain
- **Example**: Radiating domain "Quality Engineering" designed depth = Layer 3 (Expert) → Step 9 output only covers Layer 2 (Advanced) → mark downgrade "missing executable validation script" → return to Step 9

### G60 Domain Fusion Check

- **Definition**: A core action in the Validation step (Step 10) — checks whether radiating domain outputs are complementary with no overlap, cover the full chain, and have clear boundaries between adjacent domains
- **Domain**: Quality Domain
- **Example**: "Requirements Engineering & Business Translation" output and "SKILL Architecture Design" output show overlapping capability coverage (both describe workflow steps) → Domain Fusion Check triggers boundary ambiguity warning

### G61 Mandatory Visualization

- **Definition**: When the SKILL task type triggers specific conditions (involving processes/multi-component interactions/state transitions), the output must include at least 1 Mermaid diagram by mandatory rule
- **Domain**: Quality Domain
- **Example**: Generating a "Code Review SKILL" with a 5-step workflow + 3 state transitions → mandatory output of workflow flowchart and state transition diagram

### G62 Decision Strategy

- **Definition**: Output specification for review-type SKILLs — a decision table that automatically produces a judgment (Reject/Needs Modification/Conditionally Approved/Approved) based on the count of Critical/High severity issues
- **Domain**: Quality Domain
- **Example**: Security review finds 1 Critical issue (SQL injection) → Decision Strategy automatically gives "Reject"; finds 2 High issues, 0 Critical → "Needs Modification"

### G63 Confirm-Fix-Verify Cycle

- **Definition**: User interaction mode for review/diagnostic SKILLs — output issues → user selects fixes → verify after fix → confirm; maximum 3 cycles
- **Domain**: Quality Domain
- **Example**: Code review finds 5 issues → user fixes 3 High issues → re-verify → confirm pass or enter Cycle 2 (max 3 cycles)

### G64 Troubleshooting Triplet

- **Definition**: The mandatory three-element structure for troubleshooting entries — Symptom (observable phenomenon), Root Cause (underlying cause), Fix Action (executable steps). Pure declarative hints are prohibited
- **Domain**: Quality Domain
- **Example**: T01: Symptom=generated SKILL's capability matrix is recognized by GPT as a workflow; Root Cause=radiating domain names use verb phrases ("Parse Requirements" instead of "Requirements Engineering"); Fix=rename radiating domains to noun phrases + execute Sort Test

### G65 Fault Number

- **Definition**: The T{number} numbering system for troubleshooting (e.g., T01, T02), parallel with anti-pattern numbers and rule numbers, enabling cross-file references. Currently includes T01-T17
- **Domain**: Quality Domain
- **Example**: SKILL.md body writes "for capability domain confusion, see T04 in troubleshooting.md" → directly locate the target entry via number

### G66 Specification Overreach (Anti-pattern 1) (AKA: Spec Overload)

- **Definition**: Specification definitions (field constraints, format descriptions, table specifications) in a generated SKILL are placed directly in the body instead of being pushed down to references/ — causing body bloat, violating progressive loading, and reducing information density
- **Domain**: Quality Domain
- **Example**: Body contains specification tables like "| Field | Required | Constraint |" → triggers Anti-pattern 1 Specification Overreach → remove specification table, push down to references/, keep only reference paths in body

### G67 Example Contamination (Anti-pattern 3)

- **Definition**: Example content contains unsafe patterns, outdated practices, or code that contradicts the rule system, causing the model to learn incorrect behaviors
- **Domain**: Quality Domain
- **Example**: SKILL example uses `eval()` for user input processing, but the SKILL rule system explicitly prohibits dynamic execution — example contradicts rules

### G68 Architecture Confusion (Anti-pattern 4)

- **Definition**: Radiating domains in the capability matrix are aliases for workflow steps, causing the capability matrix to become a mirror of the workflow. This is UR-SKILL's #1 anti-pattern
- **Domain**: Quality Domain
- **Example**: Radiating domain list is "Parse → Research → Design → Generate → Validate → Deliver", one-to-one mapping with 6 workflow steps — classic architecture confusion

### G69 Check Deficiency (Anti-pattern 5)

- **Definition**: Insufficient review checks in the generated SKILL's workflow — critical nodes have fewer than 6 dimensions, quality checks are ineffective
- **Domain**: Quality Domain
- **Example**: Generated SKILL critical node (Validation step) contains only 3 check dimensions (Goal Alignment, Fact Anchoring, Blind Spot Identification), missing Direction Calibration, Adversarial Validation, Impact Projection

### G70 Blind Spot Evasion (Anti-pattern 6)

- **Definition**: Blind spot identification merely states "limitations noted" without executing the three-layer mechanism — jumping directly from Layer 1 to Layer 3 (pure declarative)
- **Domain**: Quality Domain
- **Example**: Blind spot statement: "This SKILL has limited review capability for Rust code; manual review is recommended" — did not execute L1 web research on Rust security patterns or L2 knowledge base retrieval

### G71 Risk Boundary Abuse (Anti-pattern 7)

- **Definition**: Risk boundary statements are written as capability degradation (e.g., "not responsible for security review"), or professional boundaries are placed in risk boundary statements
- **Domain**: Quality Domain
- **Example**: Risk boundary statement "Risk Boundary-03: Not responsible for performance optimization of generated code" — this is capability degradation rather than a safety red line; should not be in risk boundaries

### G72 Facet Filler (Anti-pattern 8)

- **Definition**: Capability facets are filled with generic boilerplate (e.g., "Master relevant domain knowledge", "Identify potential risks") without task anchoring. Detectable via the Veil Test
- **Domain**: Quality Domain
- **Example**: Facet F2 (Knowledge Deepening) content: "Master relevant domain knowledge, possess problem analysis and problem-solving skills" — after covering "Code Review" task name, the content applies to any task

### G73 Blind Spot Buck-Passing (Anti-pattern 9)

- **Definition**: Blind spot statements use disclaimers like "for reference only", "verify yourself" instead of substantive investigation. Distinguished from Blind Spot Evasion: evasion does nothing, buck-passing makes a disclaimer
- **Domain**: Quality Domain
- **Example**: "This SKILL's references to legal provisions are for reference only, do not constitute legal advice; users should verify independently" — did not execute L1 web verification, only disclaimed

### G74 Step Name Inconsistency (Anti-pattern 11)

- **Definition**: Node lists in global execution rules do not match node names in step headings, causing workflow rule reference breaks
- **Domain**: Quality Domain
- **Example**: Global execution rules declare "Critical nodes: Research (Step 4), Planning (Step 5)..." but Step 5 heading is "Step 5: Planning (Capability Matrix + Workflow Design)" — name inconsistency prevents rule binding

---

## 4. Boundary Domain

### G20 Risk Boundary

- **Definition**: Safety-related red-line declarations — if triggered, the SKILL itself loses its raison d'être (e.g., illegality/public order, discrimination, malicious injection/jailbreaking), numbered consecutively starting from "Risk Boundary-01"
- **Domain**: Boundary Domain
- **Example**: Risk Boundary-01: Do not produce SKILLs that violate laws or public order and morals

### G21 Professional Boundary

- **Definition**: Scope-related boundary protection declarations — prevent the SKILL from entering domains requiring professional qualifications (e.g., medical prescriptions, financial trading advice), numbered consecutively starting from "Professional Boundary-01"
- **Domain**: Boundary Domain
- **Example**: Professional Boundary-01: Do not perform code-level testing or deployment of the generated SKILL

### G22 Capability Degradation

- **Definition**: An anti-pattern — the SKILL proactively reduces its own capabilities, e.g., "only do security checks, not quality checks". Distinguished from Risk Boundary/Professional Boundary: Risk Boundary = "don't do harmful things", Professional Boundary = "don't go beyond professional scope", Capability Degradation = "do X but choose not to report Y"
- **Domain**: Boundary Domain
- **Example**: "Only responsible for security review, not code style check" (security review should inherently cover style-related security issues)

### G23 Safety Red Line

- **Definition**: UR-SKILL's hard termination condition — when any of illegality/public order, discrimination, malicious injection/jailbreaking is triggered, terminate immediately without proceeding to the next step
- **Domain**: Boundary Domain
- **Example**: User requests "generate a SKILL that bypasses company security review" → touches Safety Red Line → terminate

---

## 5. Metadata Domain

### G24 YAML Frontmatter

- **Definition**: The YAML metadata block wrapped by `---` at the start of SKILL.md, containing fields such as name, description, type, whenToUse, metadata; serves as the L1 layer of progressive loading
- **Domain**: Metadata Domain
- **Example**: UR-SKILL's frontmatter declares name: ur-skill, description includes trigger scenarios

### G25 RFC 2119

- **Definition**: An Internet Engineering standard defining constraint-level keywords — MUST (absolute requirement), MUST NOT (absolute prohibition), SHOULD (strong recommendation), SHOULD NOT (not recommended), MAY (optional)
- **Domain**: Metadata Domain
- **Example**: "MUST execute step-by-step according to the workflow" (absolute requirement) vs. "MAY use progressive loading strategy" (optional)

### G26 Double Prompting

- **Definition**: A zero-cost strategy that rephrases core constraints from the primacy zone in the recency zone of the body, leveraging the U-shaped attention curve to enhance key rule capture probability
- **Domain**: Metadata Domain
- **Example**: Primacy zone: "MUST NOT confuse capability matrix with workflow steps"; recency zone: "Rule 15: Architecture Confusion prohibited (Anti-pattern 4)"

### G75 Identity Gradient Model

- **Definition**: A 5-level gradient model for identity precision — Level 0 (No identity) to Level 5 (Role + domain expertise + methodology + style + tool constraints); generated SKILLs must reach at least Level 3 (Role + domain expertise + methodology)
- **Domain**: Metadata Domain
- **Example**: Level 3 identity declaration: "You are a Python security audit expert (role), proficient in OWASP Top 10 and CWE (domain expertise), following the progressive review methodology of black-box → gray-box → white-box (methodology)"

### G76 Methodology Fill-in Effect

- **Definition**: When specific domains and methodologies are described in the identity declaration, the LLM automatically "fills in" the expected detailed knowledge for that role — no need to explicitly enumerate all skills. Fabricated years of experience have counterproductive effects
- **Domain**: Metadata Domain
- **Example**: Declaration: "You are a security architect with incident response experience" → LLM automatically fills in threat modeling, attack chain analysis, etc. without needing to add "You master STRIDE, MITRE ATT&CK..."

### G78 Lost in the Middle Effect

- **Definition**: The phenomenon where LLMs capture information in the middle positions of context at significantly lower rates than at the two ends — the foundational assumption for Progressive Loading (G14), Primacy/Recency Zones (G15), Double Prompting (G26), and the 500-line body limit
- **Domain**: Metadata Domain
- **Example**: Placing key constraints in the middle of the body (lines 200-300) → due to the Lost in the Middle effect, LLM adherence to those constraints is significantly lower than the same constraints placed in the primacy or recency zones

---

## 6. Delivery Domain

### G27 Information Density

- **Definition**: The amount of valid information per token of SKILL Markdown content — eliminate formulaic filler, avoid redundant declarations, each sentence conveys independent information. Not quantifiable (no universal formula), but detectable by removing prefixes like "it should be noted that"
- **Domain**: Delivery Domain
- **Example**: Delete "One thing that needs to be noted here is that efficiency should be maintained" → "MUST keep body < 500 lines"

### G28 Delivery Completeness

- **Definition**: Whether the generated SKILL file package covers all deliverables required by the pre-analysis report (G83) — SKILL.md + all references/ + all Scripts/ + all assets/, no omissions, no redundant files. Complementary to G27 (Information Density): information density measures single-file quality, delivery completeness measures file package completeness
- **Domain**: Delivery Domain
- **Example**: Pre-analysis report requires generation of references/glossary.md + references/anti-patterns.md + scripts/validate.py → delivery completeness check confirms all three files generated and non-empty

### G29 research-analyst

- **Definition**: UR-SKILL's mandatory pre-sub-SKILL (research-analyst), automatically performs requirements parsing, domain derivation, file dependency decisions, and outputs a pre-analysis report (G83). Supports four input modes: A (Generate from scratch), B (Optimize existing SKILL), C (Extract from knowledge source), D (Localization adaptation). Capability matrix includes 8 radiating domains
- **Domain**: Delivery Domain
- **Example**: Step 1 Parse → invoke research-analyst to execute four-mode identification, 8-dimension review, output pre-analysis report

### G79 Tool Binding

- **Definition**: A mandatory rule requiring each executable action in the workflow to be syntactically bound to at least one specific tool (format: `[ToolName] Operation → Output`); abstract action descriptions without tool binding are prohibited
- **Domain**: Delivery Domain
- **Example**: `[Write] Write capability matrix analysis to references/capability-analysis.md → Output: capability domain partitioning plan` instead of "save the analysis results"

### G80 Degradation Chain

- **Definition**: A fault-tolerance mechanism for tool calls — provides a chain of Degradation1 → Degradation2 → Last Resort fallback for the preferred tool. Baseline operations that cannot be degraded (e.g., git diff for code review) terminate if they fail
- **Domain**: Delivery Domain
- **Example**: Preferred `WebSearch` online retrieval → Degradation1: `WebFetch` directly fetch known URL → Degradation2: search local knowledge base → Last Resort: fallback to training knowledge (annotated "not externally validated")

### G81 Capability Degradation (Anti-pattern 10)

- **Definition**: Professional boundary statements written as capability reduction (e.g., "only review incremental code, not historical code", "only identify, not analyze") rather than defining true professional scope — causing SKILL delivery quality to be lowered by its own boundary declarations. Consistent with G22 (Capability Degradation concept), but as Anti-pattern 10 specifically refers to "capability degradation appearing in professional boundary statements"
- **Domain**: Quality Domain
- **Example**: Professional boundary statement: "only perform security checks, not code style checks" → triggers Anti-pattern 10 Capability Degradation → security review should inherently cover style-related security issues (e.g., hardcoded keys are often hidden in disorganized code)

### G82 Master Node / Sub-Node

- **Definition**: The two-level structure of the UR-SKILL workflow — master nodes (Analyze/Execute/Reflect/Deliver) are the 4 phase groupings of the workflow, each containing several sub-nodes (specific steps). Sub-nodes are classified by review dimension into decision-type (all 6 dimensions), gate-type (all 6 dimensions), and execution-type (3 dimensions). See G09/G10
- **Domain**: Workflow Domain
- **Example**: Master node "Analyze" contains 5 sub-nodes (Parse → Coordinate → Dispatch → Research → Planning), where Research and Planning are decision-type sub-nodes (6 dimensions), the rest are execution-type sub-nodes (3 dimensions)

### G83 Pre-Analysis Report

- **Definition**: The standard output format of the research-analyst sub-SKILL (G29) — contains Requirements Card (mode/type/domain/constraints), Capability Matrix Draft (core + radiating domains × 4 progressive layers), File Dependency Manifest (filename + type + necessity), Asset File Type Manifest (classification/detection/pattern/fix/glossary, etc.), and Blind-Spot Report (attempted actions + remaining blind spots + feasibility recommendations); all five items are mandatory
- **Domain**: Delivery Domain
- **Example**: Step 3 (Dispatch) receives the pre-analysis report from research-analyst → checks all five items are present → after confirmation, proceeds to Step 4 (Research)

### G84 SKILL Type Trichotomy

- **Definition**: Task feature classification of the target SKILL performed by UR-SKILL in Step 1 (Parse) — Functional Type (tool/automation/detection), Creative Type (generation/design/creation), Social Type (dialogue/companion/role-play). Type judgment influences the sub-node selection strategy in the subsequent workflow
- **Domain**: Workflow Domain
- **Example**: User requirement "Code security review SKILL" → Step 1 classifies as Functional Type → subsequent workflow emphasizes tool binding and executability; user requirement "Creative writing SKILL" → classified as Creative Type → subsequent workflow emphasizes output diversity and style control

### G85 Technical Documentation Generation Engineering

- **Definition**: The core domain of the tech-documentation sub-SKILL — based on the file dependency manifest of the pre-analysis report (G83), generates all references/ files (glossary/anti-patterns/troubleshooting/examples, etc.) for the target SKILL, and performs cross-file consistency validation. Carries 6 capability facets
- **Domain**: Architecture Domain
- **Example**: Pre-analysis report requires generation of references/glossary.md → tech-documentation researches target domain terminology → generates glossary according to glossary-design-guide.md format

### G86 Script Generation & Verification Engineering

- **Definition**: The core domain of the script-engineer sub-SKILL — based on the scripts/ section of the pre-analysis report (G83), generates executable validation/detection scripts (Python), and ensures script correctness through self-testing and positive/negative example validation. Carries 6 capability facets
- **Domain**: Architecture Domain
- **Example**: Pre-analysis report requires scripts/validate_skill.py → script-engineer generates validation script → executes self-test (correct SKILL passes / incorrect SKILL caught) → outputs validation report

### G87 Occupation Mapping

- **Definition**: The process in which research-analyst maps the target occupation/role in the user's requirement to a standard occupation classification system (e.g., Chinese National Occupation Classification, O*NET) during the Parse step — a prerequisite for G41 (Job Competency Analysis), providing occupational anchor points for subsequent KSAO analysis and domain derivation
- **Domain**: Architecture Domain
- **Example**: User says "make a lawyer assistant SKILL" → Occupation Mapping maps "lawyer" to standard occupation code → triggers G41 Job Competency Analysis (lawyer's KSAO model) → derive radiating domains (legal research/evidence analysis/document drafting, etc.)

---

## 7. Model Format Domain

### G30 Model Format Adaptation

- **Definition**: Adjusting the generated SKILL's structural syntax to match the target platform's format preferences (Claude → XML tags, ChatGPT → Markdown + separators, Gemini → PTCF framework). Only affects section headings, separators, and output format specifications; does not change the capability matrix, workflow logic, or rule system
- **Domain**: Model Format Domain
- **Example**: User says "generate for Claude" → adapts generated SKILL from default Markdown to XML tag structure (`<role>`, `<instructions>`, `<output_format>`); capability matrix and workflow steps remain unchanged

### G31 Default Format

- **Definition**: UR-SKILL's baseline output format: standard Markdown (ATX headings with `#`, RFC 2119 keywords as `**MUST**`, Markdown tables, triple backtick code blocks, `- [ ]` checklists). Used when the user doesn't specify a target platform or cross-model portability is needed
- **Domain**: Model Format Domain
- **Example**: User provides requirements but no target platform → generate SKILL in default Markdown format. "Claude eats XML, ChatGPT eats Markdown, Gemini eats PTCF" — when no platform is specified, Markdown is the safest fallback

---

## Reference Index (by File)

> The table below marks the design domain concepts (grouped by G numbers) covered by each file, not direct text references.

| File | Design Domains (Conceptual Coverage) |
|:---|:---|
| SKILL.md | G01-G04 (Capability Matrix), G05-G15 (Structural System), G17 (Anti-patterns), G18 (Troubleshooting), G20-G25 (Rule System), G39-G45 (Identity), G75-G78 (Model Format), G82-G84 (Output Spec) |
| templates/capability-architecture-template.md | G01-G07 (Capability Matrix), G39-G45 (Identity), G87 (Completeness) |
| templates/workflow-template.md | G08-G14 (Workflow), G50-G58 (Tool Invocation), G79-G80 (Configuration), G82 (Output) |
| templates/rules-template.md | G20-G22 (Hard Constraints / Hard Prohibitions), G25 (Strong Preference) |
| design-rationale/design-rationale.md | G05 (Core Domain), G27 (Radiating Domains), G32-G38 (Facets), G39 (Identity), G84 (Validation) |
| References/anti-patterns.md | G17 (Anti-patterns), G18 (Troubleshooting), G22 (Rule Conflicts), G66-G74 (Validation), G81 (Bilingual) |
| References/troubleshooting.md | G01-G03 (Matrix Structure), G17 (Anti-patterns), G64-G65 (Execution Check) |
| design-guides/structure-design-guide.md | G15 (File Structure), G25-G27 (Radiating Domains), G75-G76 (Model), G78 (Format) |
| design-guides/boundary-design-guide.md | G20-G23 (Rules/Boundaries), G71 (Safety), G81 (Bilingual) |
| design-guides/skill-package-design-guide.md | G30-G31 (Package Structure/Platform) |
| agent/research-analyst.md | G39 (Identity), G58 (Tools), G83 (Output), G87 (Completeness) |
| agent/tech-documentation.md | G85 (Documentation) |
| agent/script-engineer.md | G86 (Scripts) |

> Note: G77 has been deprecated (merged into G15). G52 is a newly added number (Tool Action Marker). G28 definition restored (Delivery Completeness). G81-G87 are newly added terms.
