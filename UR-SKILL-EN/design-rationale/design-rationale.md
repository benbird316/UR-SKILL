# Design Rationale

> **Purpose**: House explanatory content from the UR-SKILL body, reducing body information density
> **Core Principle**: The body retains only "what to do" and "how to do it"; all "why" content is pushed down here

---

## 1. Why the Capability Matrix Uses "Capability Domains" Instead of "Workflow Steps"

See ../templates/capability-architecture-template.md §1.1 for the full definition of the Sort Test and Three-Question Filter (Independence / Irreplaceability / Complementarity).

In short: The capability matrix answers "what capabilities exist," while the workflow answers "in what order to execute." Stuffing workflow steps into the capability matrix is Anti-pattern 4 (Architecture Confusion).

---

## 2. Why Radiating Domain Count Is Determined by Task Analysis

The number of radiating domains is not fixed; it is determined by task analysis (recommended 3-8, minimum 3, maximum 8).

**Determination Method**:
1. Analyze the core task: What is this SKILL's core task?
2. Identify the core domain: What is the most critical professional dimension for completing this task?
3. Identify radiating domains: Using the core task as the investigation direction, research which related professional domains are needed to complete the task.
4. Check independence: Is each domain independent and complementary? (Sort Test + Three-Question Filter)
5. Verify coverage: Are all necessary capabilities covered?
6. Control count: Does it exceed 8? If so, merge related domains.

**Why Not a Fixed Number**: Different tasks require different capability domains. Investigation analysis needs 7 radiating domains (Search Research, Information Management, Analytical Research, Deep Reasoning, Problem Construction, Output Expression, Process Monitoring), while Python code review needs 5 (Static Analysis, Security Audit, Performance Diagnosis, Style Conventions, Refactoring Suggestions). The number of domains is determined by task analysis, not by arbitrary rules.

---

## 3. Why the Capability Matrix Has a Fixed 4-Layer Depth

4 layers form a complete capability progression chain:

| Layer | Cognitive Level |
|:---|:---|
| Foundation | Memory / Understanding |
| Advanced | Application |
| Expert | Analysis / Evaluation |
| Extension | Creation |

Even simple tasks require a complete capability progression. A SKILL without depth is better not used.

---

## 4. Why Critical Nodes Use All 6 Dimensions, Non-Critical Nodes Use 3

The 6 review dimensions cover the complete elements of decision quality:

| Review Dimension | Question |
|:---|:---|
| Goal Alignment | Did we do what we were supposed to do? |
| Fact Anchoring | Is there supporting evidence? |
| Direction Calibration | Is the direction correct? |
| Adversarial Validation | Can it withstand scrutiny? |
| Blind Spot Identification | Are there omissions? Were actions taken after identification? |
| Impact Projection | What is the impact on subsequent steps? |

Critical nodes (Research, Planning, Verify, Validation, Loop Decision) are decision/gate nodes requiring all 6 dimensions for thorough review. Non-critical nodes (Parse, Coordinate, Dispatch, Consolidate, Execute, Assemble) are execution nodes where the path is already determined, requiring only 3 dimensions: Goal Alignment, Fact Anchoring, Blind Spot Identification.

---

## 5. Why Body Is Limited to 500 Lines / 5000 Tokens

Based on the LLM attention mechanism: information capture rates are highest at both ends of the context and drop significantly in the middle (Lost in the Middle effect). Beyond the threshold, intermediate rules, constraints, and examples are easily diluted.

Therefore, progressive loading is adopted:
- L1: name + description (~100 tokens)
- L2: body (< 500 lines / < 5000 tokens)
- L3: references/, scripts/, assets/ (on-demand loading)

---

## 6. Why Rules Use RFC 2119 Keywords

RFC 2119 (and RFC 8174) is an Internet Engineering task standard that defines precise semantics for MUST / MUST NOT / SHOULD / SHOULD NOT / MAY. In uppercase, they carry special meaning and can be mechanically parsed by tools.

---

## 7. Why Blind Spot Identification Must Be Followed by Concrete Actions

Pure declarative blind spots ("deficiencies exist here") do not drive continued optimization. The three-layer mechanism enforces action:

1. Layer 1: Investigation and analysis -> self-optimization to fill the gap
2. Layer 2: Still insufficient -> request resources
3. Layer 3: No resource supplementation -> output blind spot handling report (actions attempted + remaining blind spots + feasibility recommendations)

Jumping directly from Layer 1 to Layer 3 is prohibited.

---

## 8. File Dependency Decisions Driven by research-analyst Pre-Analysis

UR-SKILL does not rely on predefined complexity tiers. In the current design, file dependencies are dynamically determined by the following mechanism:

1. **SKILL Type Determination (Step 1)**: Functional/Creative/Social classification (see G84) influences subsequent sub-node selection strategy
2. **research-analyst Pre-Analysis (Step 3)**: Investigation Analysis & Domain Research Engineering (G39) automatically analyzes requirements and outputs a file dependency manifest
3. **Decision Quick Reference (skill-package-design-guide §2.5)**: The criteria for each asset type are distilled into testable single questions -- "Can LLM training data reliably cover this? Is programmatic verification needed? Are there 5+ self-coined terms?"
4. **Decision Tree (§9)**: A complete step-by-step decision process executed sequentially by research-analyst during file dependency analysis

Core Principle: **Criteria-driven, not tier-driven**. Each SKILL's deliverable manifest is determined by task feature analysis -- platform-based writing needs knowledge-reference (platform conventions + category terminology), general writing does not -- rather than applying a "simple/medium/complex" template.

---

## 9. Why a File Dependency Decision Tree Is Needed

The file dependency decision determines which `references/`, `scripts/`, `assets/` files need to be created for this SKILL. This decision is **executed in workflow Step 5 (Planning)** to avoid "discovering missing files halfway through execution." Its logic is internalized into the research-analyst sub-SKILL's "Investigation Analysis & Domain Research Engineering" radiating domain (see §8).

### Decision Tree (Determine in order; each Yes accumulates required files)

```
Step 0: Does the SKILL need standalone reference files (not a single-file SKILL)?
  |-- No (all content can be inlined in body) -> 0 references/ files, all content inlined in body. End.
  |-- Yes (needs standalone file organization) -> Base pack: example + anti-pattern + troubleshooting (3 baseline files)
         |
  Step 1: Does the core domain depend on external knowledge bases (e.g., OWASP/RFC/industry standards/regulations/API docs/academic theory systems/platform writing conventions)?
         |-- Yes -> Needs knowledge-reference file (explanatory/method/verification/pattern/specification -- 5 types, determined by usage purpose)
         |-- No -> Skip
         |
  Step 2: Are there >= 5 self-coined methodological terms, or does the task involve cross-domain intersection (e.g., finance+law, security+compliance)?
         |-- Yes -> Needs glossary.md
         |-- No -> Skip
         |
  Step 3: Are executable scripts or static resources/templates needed?
         |-- No -> File manifest determined. End.
         |-- Yes -> Additionally needs scripts/ + assets/, and:
               |-- Review/audit/test type tasks -> Needs output-content specification (mandatory Mermaid + issue severity table)
               |-- Needs external tool invocation (API/CLI) -> Needs method-type ref (API reference)
               |-- Needs static template output (e.g., reports, configs) -> Needs assets/templates/
               |-- Needs executable validation script -> Needs scripts/validate_*.py
```

### Decision Quick Reference Table

| Condition | Triggered File | Type Code | Required/Optional |
|:---|:---|:---:|:---:|
| Needs standalone file organization (threshold) | example.md | C1 | **Required** |
| Needs standalone file organization (threshold) | anti-patterns.md | A1 | **Required** |
| Needs standalone file organization (threshold) | troubleshooting.md | A2 | **Required** |
| Depends on external knowledge base | knowledge-reference file (5 types) | B1-B4 | Required when triggered |
| Self-coined terms >=5 or cross-domain | glossary.md | D3 | Required when triggered |
| Review/audit/test type | output-content specification | A3 derivative | Required |
| External tool invocation | method-type ref (API reference) | B2 | Recommended |
| Needs executable scripts/resources (threshold) | scripts/ + assets/ | -- | **Required** |
| Needs custom specification (e.g., non-standard metadata-spec) | Specification-type file | D1 | On demand |

### Decision Examples

**Example 1: Python Security Audit SKILL**
```
0. Needs standalone file organization? -> Yes -> 3 baseline
1. Depends on external knowledge base? -> Yes (OWASP Top 10 + CWE Top 25) -> + explanatory-type ref (security standards)
2. Self-coined terms >=5 or cross-domain? -> Yes (security domain terminology) -> + glossary
3. Needs executable scripts/resources? -> Yes (audit type + needs scripts/) -> + output-content spec (mandatory Mermaid + issue severity), + scripts/validate_*.py
```
-> Manifest: example + anti-patterns + troubleshooting + explanatory-type ref(OWASP) + glossary + output-content spec + scripts/

**Example 2: React Component Generation SKILL**
```
0. Needs standalone file organization? -> Yes -> 3 baseline
1. Depends on external knowledge base? -> Yes (React API reference + component patterns) -> + method-type ref(API) + pattern-type ref(component patterns)
2. Self-coined terms >=5 or cross-domain? -> No
3. Needs executable scripts/resources? -> No -> End
```
-> Manifest: example + anti-patterns + troubleshooting + method-type ref(React API) + pattern-type ref(component patterns)

**Example 3: General Creative Writing SKILL (no platform binding)**
```
0. Needs standalone file organization? -> Yes -> 3 baseline
1. Depends on external knowledge base? -> No (rhetoric and narrative techniques are general knowledge, can be inlined)
2. Self-coined terms >=5 or cross-domain? -> No
3. Needs executable scripts/resources? -> No -> End
```
-> Manifest: example + anti-patterns + troubleshooting (only 3 baseline files)

**Example 4: Xiaohongshu Content Creation SKILL (platform-bound)**
```
0. Needs standalone file organization? -> Yes -> 3 baseline
1. Depends on external knowledge base? -> Yes (platform layout conventions + category terminology + hashtag strategy) -> + explanatory-type ref(platform conventions) + pattern-type ref(category terminology)
2. Self-coined terms >=5 or cross-domain? -> Yes (platform-specific concepts like "grass-planting," "viral hit," "Captain Potato") -> + glossary
3. Needs executable scripts/resources? -> No -> End
```
-> Manifest: example + anti-patterns + troubleshooting + explanatory-type ref(Xiaohongshu conventions) + pattern-type ref(category terminology) + glossary

> **Key Distinction**: Platform-bound writing (Xiaohongshu/WeChat Official Account/Zhihu) depends on platform-specific format conventions, category terminology, and trend knowledge -- these are external knowledge that cannot be inlined. General writing (rhetoric/narrative) can be inlined.

---

## 10. Knowledge Domain Design Rationale

### 10.1 Problem: The Workflow Alias Anti-Pattern for Radiating Domains

If radiating domains are designed as strict one-to-one mappings with workflow steps, this constitutes the classic workflow alias anti-pattern:

```
A Semantic Parsing -> B Task Domain Research -> C Capability Domain Derivation -> D Complexity Determination -> E File Dependency Decision -> F Output Structuring
```

The core problem with this design is that 6 domains **strictly correspond one-to-one** with workflow steps (A->Step1, B->Step2, C->Step3, D+E->Step4, F->Step7), violating the UR-SKILL core rule: **capability domains != workflow steps**.

Three-Question Filter fails:
- **Sort Test**: A->B->C->D->E->F can only be linear sequential; reordering breaks the logic
- **Independence**: C "Capability Domain Derivation" and D "Complexity Determination" are sequentially dependent in the workflow, unable to function independently
- Conclusion: This is a classic case of **Anti-pattern 4 (Workflow Alias)**, documented in [../References/anti-patterns.md](../References/anti-patterns.md)

### 10.2 Design Principles

What research-analyst needs are **true knowledge bodies**, not workflow step aliases. It must understand the professional substance, unique risks, and ethical norms of any target occupation, much like an HR analyst evaluating a role.

Design principles:
1. **General occupational perspective**: The first 4 domains should be capable of analyzing any occupation
2. **System internalization**: The 5th domain honestly acknowledges the need to internalize UR-SKILL's own methodology
3. **Independent and cross-referenceable**: 5 domains can be cross-invoked with no temporal dependencies

### 10.3 6-Domain Industry Benchmark

| Knowledge Domain | Industry Benchmark | Source |
|:---|:---|:---|
| Requirements Engineering | Requirements Engineering | IEEE SWEBOK v4.0 KA 2 (Elicitation/Analysis/Specification/Validation) |
| Job Competency Analysis | Job Analysis / Competency Modeling | O\*NET KSAO Model, I-O Psychology (Knowledge/Skills/Abilities/Other Characteristics) |
| Information Source Assessment | Information Quality Assessment / Media Literacy | CRAAP Test, SIFT Method, Lateral Reading (source evaluation & cross-validation) |
| Occupational Risk Identification | Professional Risk Assessment | HSE 5-step, ISO 31000 (general red lines + occupation-specific risk spectrum) |
| Professional Ethics | Professional Ethics | APA Ethics Code, IEEE Code of Ethics, CFA Code of Ethics |
| System Cognition | Institutional Knowledge | UR-SKILL internal methodology (complexity decision tree/anti-patterns/RFC 2119/checklist) |

### 10.4 Domain Selection Logic: First 5 Domains vs. 6th Domain

**First 5 domains = External cognition of the target occupation**:

- **Requirements Engineering**: What the user wants to do (goals/domain/delivery form/implicit assumptions)
- **Job Competency Analysis**: What capabilities this occupation requires (KSAO analysis, capability domain mapping)
- **Information Source Assessment**: Is the information supporting capability judgments reliable? (official standards vs AI-generated, timeliness verification, source pedigree establishment)
- **Occupational Risk Identification**: What unique risks does this occupation have? (not just "illegal/discriminatory" -- psychological counseling has intervention risks, finance has conflict of interest risks, medicine has misdiagnosis risks)
- **Professional Ethics**: This occupation's ethical constraints (positive duties + negative constraints, e.g., psychological counseling MUST maintain confidentiality, MUST NOT exploit psychological vulnerability to coerce)

**6th Domain = Internal cognition of UR-SKILL**:

- **System Cognition**: Internalization of the complete methodology. This is the only unavoidable internal knowledge domain, but it is honestly named, not disguised as "general skills."

### 10.5 Anti-Pattern Comparison

| Dimension | Workflow Alias Pattern (Anti-pattern 4) | Correct Knowledge Body Design |
|:---|:---|:---|
| Domain essence | Workflow step alias, linear sequential | Independent knowledge body, cross-referenceable |
| Three-Question Filter | Fails | Passes |
| Occupational generality | None (all internal instructions) | First 5 domains can analyze any occupation |
| Information quality | No filtering (uses whatever is found) | Has Information Source Assessment, filters low-quality/AI-generated/outdated information |
| Risk analysis | Anti-pattern-oriented only | Can analyze occupation-specific risk spectrum |
| Ethical constraints | Only "touch safety red line -> terminate" | Can understand professional ethics systems |

### 10.6 Occupational Risk: Unique Risk Spectrum (Example)

Different occupations have completely different risk spectra. The following are examples; actual analysis must be expanded based on the target occupation:

| Occupation | General Safety Red Lines | + Unique Risks of This Occupation |
|:---|:---|:---|
| Psychological Counseling | No illegality/discrimination | Must not exploit psychological vulnerability for reverse psychological intervention; must not establish dual relationships |
| Medical Diagnosis | No illegality/discrimination | Must not provide diagnostic conclusions without confirmed diagnosis; drug recommendations must be based on clinical evidence |
| Financial Investment | No illegality/discrimination | Must not guarantee principal protection; must disclose related party relationships |
| Legal Consultation | No illegality/discrimination | Must not provide formal legal opinions (without license); must inform about statutes of limitation |
| Educational Tutoring | No illegality/discrimination | Must not replace professional special education assessments; must not recommend unverified "treatment" programs |

### 10.7 Professional Ethics: Bidirectional Structure

Professional ethics are not a simple "cannot do X" list, but a **bidirectional structure**:

- **Positive duties**: Professional responsibilities to be actively fulfilled (MUST do what)
- **Negative constraints**: Bottom lines that must not be crossed (MUST NOT do what)
- **Practice boundaries**: Distinguish between what this occupation can do and what must be referred out

Using APA Ethics Code (Psychological Counseling) as illustration:
```
Positive duties:
  - MUST protect client privacy and informed consent rights
  - MUST maintain professional competence and receive continuing education regularly
  - MUST take reasonable protective measures in crisis situations

Negative constraints:
  - MUST NOT exploit psychological vulnerability for coercion or control
  - MUST NOT establish dual relationships outside the therapeutic relationship
  - MUST NOT disclose client information on social media

Practice boundaries:
  - Can do: Psychological assessment, counseling, and therapy
  - Cannot do: Psychiatric medication prescription (must refer to psychiatrist)
  - Cannot do: Forensic psychological evaluation (requires specialized qualifications)
```

## 11. Why Step 1 (Parse) Only Does Fact Extraction, Step 2 (Research) Does Deep Analysis

### 11.1 Problem: Contradiction in the Old Design

If research-analyst's Step 1 was designed to bear the following cognitive load, it would cause logical inversion:

- Mode A Step 1.3: Output "goal + domain + delivery form"
- Mode B1 Step 1.2: Preliminary gap analysis (missing items/defective items/retainable items)
- Mode C Step 1.3: Map to requirement parsing card (goal/domain/delivery form/implicit assumptions)

These actions are nominally "parsing" but substantively require **deep research and system cognition** to complete. Outputting "domain" and "gap judgment" before conducting web research and understanding the target occupation's professional substance is a logical inversion.

### 11.2 Contradiction Breakdown

| Contradiction | Symptom | Root Cause |
|:---|:---|:---|
| Output "domain" without research | Step 1 claims to produce domain attribution but knows nothing about the occupation's professional composition | Parse should only extract "what the user says they want to do"; domain attribution requires web research to determine |
| B1 "Gap analysis" is research | Judging missing/defective/retainable items requires deep system cognition | Gap analysis = discovering "what is missing," which is itself the essence of research |
| Domain declaration confusion | `[WebSearch] Declare Job Competency Analysis·Expert Layer` -- action and domain don't match | Domains should declare the knowledge domain the action is situated in, not the action type |

### 11.3 Correct Boundary

```
Step 1 (Parse) = Fact Extraction
  Input: User natural language
  Output: Mode type + User core requirements summary + Tentative occupation mapping + Implicit assumption list
         (B1: Raw structure card / B2: Optimization direction + fact summary / C: Knowledge source fact card)
  Prohibited: Domain derivation, gap analysis, 6-facet audit, web research

Step 2 (Research) = Deep Cognition
  Input: Step 1's fact card
  Output: Candidate capability domains (passed Sort Test + Three-Question Filter) + Occupational risk spectrum + Professional ethics + Optimization/completion plan
  Actions: Job analysis -> Gap assessment -> Capability derivation -> Web research -> Audit -> Activate optimization
```

### 11.4 Analogy: HR Recruitment Process

```
Step 1 (Parse) = Receive resume + Read JD
  -> Sees: candidate wrote "proficient in Python" (fact)
  -> Does not judge: Is Python truly proficient or just wrote a few scripts? (leave for interview)

Step 2 (Research) = Interview + Technical assessment
  -> Verifies: Python understanding depth (Sort Test = can they teach others?)
  -> Discovers: Lacks Django experience (Gap analysis = compare against role standard)
  -> Decision: Hire or not (Three-Question Filter = Independence/Irreplaceability/Complementarity)
```

### 11.5 Design Principles Summary

- **Facts before judgment**: First know "what exists," then ask "what does it mean"
- **Parse does not include research**: Parse = read, Research = think + investigate
- **Domain declaration matches action**: `[WebSearch]` declares that this search serves a particular knowledge domain, not the action type


## 12. UR-SKILL Master SKILL Capability Matrix Redesign

### 12.1 Problem: The Workflow Alias Anti-Pattern for Radiating Domains

If radiating domains are designed as aliases for workflow steps, this constitutes Anti-pattern 4 -- using the UR-SKILL master SKILL's 6-domain design as an example:

```
A Semantic Parsing -> B Knowledge Retrieval -> C Architecture Design -> D Content Engineering -> E Quality Assurance -> F Delivery Management
```

This design strictly corresponds to workflow steps:

| Anti-Pattern Domain | Corresponding Workflow Step |
|:---|:---|
| A Semantic Parsing | Step 1 Parse |
| B Knowledge Retrieval | Step 2 Research |
| C Architecture Design | Step 3 Architecture (old naming) |
| D Content Engineering | Step 4 Execute |
| E Quality Assurance | Step 5 Verify |
| F Delivery Management | Step 7 Deliver (old naming) |

Not only is it one-to-one, but the domain names are themselves verbs (Semantic Parsing/Knowledge Retrieval/Content Engineering) -- directly workflow step names. The 4-layer progression (Foundation -> Advanced -> Expert -> Extension) reinforces the "step nesting" feel.

### 12.2 Design Principles

Same as research-analyst (§10), UR-SKILL's radiating domains must be independent knowledge bodies:

1. **Based on Prompt Engineering industry standards**: Academia (Vu & Oppenlaender 2025) + Japan PE-BoK (5 domains) + industry skill matrix
2. **Nouns, not verbs**: Each domain answers "what you know" not "what you do"
3. **No temporal dependencies**: Any workflow step can invoke any domain

### 12.3 Current 6-Domain Design

| Knowledge Domain | Industry Benchmark | Connotation |
|:---|:---|:---|
| Requirements Engineering & Business Translation | SWEBOK Requirements Engineering / PE Communication Skills | Vague intent -> structured requirements, map business goals to SKILL capabilities |
| SKILL Architecture Design | PE System Design / UR-SKILL specific | Capability matrix/progressive loading/complexity decision tree/file dependency/workflow gating |
| Prompt System Engineering | Japan PE-BoK Design Patterns/Structured Output | Information architecture (Primacy/Recency)/RFC 2119/attention management/tool binding syntax |
| Quality Engineering | PE-BoK Iterative Improvement/Evaluation | Anti-pattern detection/boundary verification/completeness checking/cross-reference consistency |
| Ethics & Safety | PE-BoK Ethics & Safety / APA Ethics Code | Risk boundaries (illegal/discriminatory/injection)/occupation-specific risk spectrum/professional boundaries |
| Iterative Improvement | PE Version Management/Platform Adaptation / HSE 5-step | Platform adaptation/blind-spot feedback self-healing/metadata optimization/version evolution |

### 12.4 Design Comparison

```
Workflow Alias Pattern (Verbs + Sequential)     Current 6 Domains (Nouns + No Temporal Dep.)
A Semantic Parsing → B Knowledge Retrieval      Requirements Engineering & Business Translation   SKILL Architecture Design
↓                                                 Prompt System Engineering   Quality Engineering
C Architecture Design → D Content Engineering    Ethics & Safety   Iterative Improvement
↓
E Quality Assurance → F Delivery Management     ← Any step can cross-invoke any domain
```
