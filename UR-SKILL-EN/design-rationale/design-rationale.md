# Design Rationale

> Purpose: Houses explanatory content from the UR-SKILL body, reducing body information density
> Core Principle: The body retains only "what to do" and "how to do it"; all "why" sinks down to here

---

## 1. Why the Capability Matrix Uses "Capability Domains" Instead of "Workflow Steps"

See ../templates/capability-architecture-template.md section 1.1 for the complete definition of the Ordering Test and the Three-Question Screening. (independence / irreplaceability / complementarity).

In short: The capability matrix answers "what capabilities exist"; the workflow answers "in what order to execute." Stuffing workflow steps into the capability matrix is Anti-Pattern 4 (Architecture Confusion).

---

## 2. Why the Number of Radiating Domains Is Determined by Task Analysis

The number of radiating domains is not fixed; it is determined by task analysis (recommended 4-8, minimum 3, maximum 8).

**Determination Method**:
1. Analyze the core task: What is the core task of this SKILL?
2. Identify the core domain: What is the most essential professional dimension for completing this task?
3. Identify radiating domains: Using the core task as the investigation direction, research what related professional domains are needed to complete the task.
4. Check independence: Is each domain independent and complementary? (Ordering Test + Three-Question Screening)
5. Verify coverage: Are all necessary capabilities covered?
6. Control quantity: Does it exceed 8? If so, merge related domains.

**Why not a fixed number**: Different tasks require different capability domains. Search analysis needs 7 radiating domains (search research, information management, analytical research, deep reasoning, question construction, outcome expression, process monitoring), while Python code inspection needs 5 (static analysis, security audit, performance diagnosis, style standards, refactoring suggestions). The number of domains is determined by task analysis, not by arbitrary regulation.

---

## 3. Why the Capability Matrix Depth Is Fixed at 4 Layers

The 4 layers form a complete chain of capability progression:

| Layer | Cognitive Level |
|:---|:---|
| Foundational | Memorization / Comprehension |
| Advanced | Application |
| Expert | Analysis / Evaluation |
| Extended | Creation |

Even simple tasks require complete capability progression. A SKILL without depth is worse than having none.

---

## 4. Why Critical Checkpoints Use All 6 Dimensions and Non-Critical Checkpoints Use 3

The 6 review dimensions cover the complete elements of decision quality:

| Review Item | Question |
|:---|:---|
| Goal Alignment | Are you doing the right thing? |
| Fact Anchoring | Is there a basis for this? |
| Direction Calibration | Is the direction correct? |
| Adversarial Validation | Does it withstand challenge? |
| Blind Spot Identification | Is anything missed? Action taken after identification? |
| Impact Projection | What is the impact on subsequent steps? |

Critical Checkpoints (research, architecture, verification, validation) are decision nodes requiring thorough review. Non-Critical Checkpoints (parsing, execution, delivery) are operational nodes where the path is already determined; only goal, facts, and blind spots need confirmation.

---

## 5. Why the Body Is Limited to 500 Lines / 5000 Tokens

Based on LLM attention mechanisms: information at the two ends of context has the highest capture rate, with a significant drop in the middle (Lost in the Middle effect). Beyond the threshold, rules, constraints, and examples in the middle are easily diluted.

Thus, progressive loading is adopted:
- L1: name + description (~100 tokens)
- L2: body (< 500 lines / < 5000 tokens)
- L3: references/, scripts/, assets/ (loaded on demand)

---

## 6. Why Rules Use RFC 2119 Keywords

RFC 2119 (and RFC 8174) is an Internet engineering standard that defines precise semantics for MUST / MUST NOT / SHOULD / SHOULD NOT / MAY. In all-caps, they carry special meaning and can be mechanically parsed by tools.

---

## 7. Why Blind Spot Identification Must Be Followed by Concrete Action

Purely declarative blind spots ("deficiencies exist here") do not drive further optimization. The three-tier mechanism enforces action:

1. Tier 1: Investigate and analyze → self-optimize to fill the gap
2. Tier 2: Still inadequate → request resources
3. Tier 3: No resources to supplement → output a blind spot handling report (attempted actions + remaining blind spots + actionable suggestions)

Jumping directly from Tier 1 to Tier 3 is forbidden.

---

## 8. Why Complexity Determination Is Based on Resource Requirements, Not Domain Count

Complexity determination is based on **organizational and maintenance requirements**. It is **independent** of the capability matrix domain count and **not directly tied** to the number of reference files.

| Determination Dimension | Simple | Medium | Complex |
|:---|:---|:---|:---|
| **Executable Scripts** | Not needed | Not needed | Needed |
| **Static Resources / Templates** | Not needed | Not needed | Needed |
| **Iterative Optimization Loop** | Single-pass output | Single-pass output | Multi-round verification/optimization |
| **Workflow Complexity** | 4 steps (Parse -> Execute -> Verify -> Deliver) | 5-6 steps | 7 steps (includes research, architecture design) |
| **Reference File Organization** | None (single file) | references/ (at minimum: example, anti-pattern, troubleshooting) | references/ + scripts/ + assets/ |
| **Mandatory Reference Files** | None | example + anti-pattern + troubleshooting (3 minimum) | All 8 design-guide covered file types + iteration scripts (specific file types determined by task characteristics, see section 9 File Dependency Decision) |
| **Output Format** | Single format | Structured format | Mixed multi-format + versioned |

**Complexity Decision Tree** (determine in the following order):

1. **Needs executable scripts?** -> Yes -> **Complex**
2. **Needs static resources / templates?** -> Yes -> **Complex**
3. **Needs multi-round iterative optimization (e.g., A/B testing prompt versions)?** -> Yes -> **Complex**
4. **Needs phased workflow (Research -> Architecture -> Execute -> Verify -> Validate -> Deliver)?** -> Yes -> **Medium**
5. **Other cases** -> **Simple**

### Mode B (Optimize Existing SKILL) Complexity Determination Supplement

| Gap Found | Complexity Impact |
|:---|:---|
| Existing SKILL has no capability matrix | -> At least Medium (requires re-architecture) |
| Existing SKILL has no anti-patterns / blind-spot three-tier / references/ | -> At least Medium |
| Existing SKILL has no tool binding | -> At least Medium |
| Existing SKILL has Anti-Pattern 10 (capability degradation) | -> At least Medium |
| Existing SKILL requires scripts/ + assets/ | -> Complex |

### Mode C (Knowledge Extraction) Complexity Determination Supplement

| Knowledge Source Characteristics | Complexity Impact |
|:---|:---|
| Single source (1 document / 1 database table) | -> Simple or Medium |
| Multi-source (multiple heterogeneous documents / multi-table cross-database) | -> Medium or Complex |
| Requires multi-round recursive extraction of cross-document knowledge | -> Complex |

---

## 9. Why a File Dependency Decision Tree Is Needed

After complexity determination is complete, enter file dependency decision-making -- determining which `references/`, `scripts/`, `assets/` files this SKILL needs to create. This decision is **executed after workflow Step 3 ends and before Step 4 begins**, avoiding "discovering missing files halfway through execution."

### Decision Tree (determine in order; each Yes accumulates the required files)

```
Step 0: Is complexity >= Medium?
  ├── No (Simple) -> 0 references/ files, all content inlined in body. End.
  └── Yes (Medium/Complex) -> Base package: example + anti-pattern + troubleshooting (3 minimum files)
         ↓
  Step 1: Does the core domain depend on external knowledge bases (e.g., OWASP / RFC / industry standards / regulations / API documentation / academic theoretical systems)?
         ├── Yes -> Need knowledge-reference files (K1-K4 subtypes determined by knowledge source)
         └── No -> Skip
         ↓
  Step 2: Are there >= 5 self-coined methodological terms, or does it involve cross-domain intersection (e.g., finance + law, security + compliance)?
         ├── Yes -> Need glossary.md
         └── No -> Skip
         ↓
  Step 3: Is complexity "Complex"?
         ├── No (Medium) -> File manifest finalized. End.
         └── Yes (Complex) -> Additionally need scripts/ + assets/, and:
               ├── Review / audit / testing type tasks -> Need output-content specification (mandatory Mermaid + issue severity classification table)
               ├── Requires external tool invocation (API / CLI) -> Need knowledge-reference K2 (API reference file)
               ├── Requires static template output (e.g., reports, configs) -> Need assets/templates/
               └── Requires executable validation scripts -> Need scripts/validate_*.py
```

### Decision Quick Reference Table

| Condition | Triggered File | Type ID | Mandatory / Optional |
|:---|:---|:---:|:---:|
| Medium+ complexity (threshold condition) | example.md | C1 | **Mandatory** |
| Medium+ complexity (threshold condition) | anti-patterns.md | A1 | **Mandatory** |
| Medium+ complexity (threshold condition) | troubleshooting.md | A2 | **Mandatory** |
| Depends on external knowledge base | knowledge-reference files | B1-B4 | Mandatory if triggered |
| Self-coined terms >= 5 or cross-domain | glossary.md | D3 | Mandatory if triggered |
| Complex + review / audit / testing type | output-content specification | A3 derivative | Mandatory |
| Complex + external tool invocation | K2 API reference file | B2 | Recommended |
| Complex (threshold condition) | scripts/ + assets/ | -- | **Mandatory** |
| Requires custom specification (e.g., non-standard metadata-spec) | Specification-type files | D1 | On demand |

### Decision Examples

**Example 1: Python Security Audit SKILL**
```
0. Complexity >= Medium? -> Yes (Complex, 7-step workflow) -> 3 minimum
1. Depends on external knowledge base? -> Yes (OWASP Top 10 + CWE Top 25) -> + knowledge-reference K1
2. Self-coined terms >= 5 or cross-domain? -> Yes (security domain terminology) -> + glossary
3. Complex + audit type? -> + output-content specification (mandatory Mermaid + issue severity classification), + scripts/validate_*.py
```
-> Manifest: example + anti-patterns + troubleshooting + knowledge-reference(OWASP) + glossary + output-content specification + scripts/

**Example 2: React Component Generation SKILL**
```
0. Complexity >= Medium? -> Yes (Medium, 5-step workflow) -> 3 minimum
1. Depends on external knowledge base? -> Yes (React API reference + component patterns) -> + knowledge-reference K2(API) + K4(patterns)
2. Self-coined terms >= 5 or cross-domain? -> No
3. Medium -> End
```
-> Manifest: example + anti-patterns + troubleshooting + knowledge-reference(React API + patterns)

**Example 3: Blog Writing Guidance SKILL**
```
0. Complexity >= Medium? -> Yes (Medium) -> 3 minimum
1. Depends on external knowledge base? -> No (writing knowledge can be inlined)
2. Self-coined terms >= 5 or cross-domain? -> No
3. Medium -> End
```
-> Manifest: example + anti-patterns + troubleshooting (only 3 minimum files)

---

## 10. Knowledge Domain Design Justification

### 10.1 Problem: Anti-Patternization of Old Radiating Domains

The pre-analysis engineer's old radiating domains were:

```
A Semantic Parsing -> B Task Domain Research -> C Capability Domain Derivation -> D Complexity Determination -> E File Dependency Decision -> F Structured Output
```

The problem is that these 6 domains were in **strict one-to-one correspondence** with workflow steps (A->Step1, B->Step2, C->Step3, D+E->Step4, F->Step7), violating the UR-SKILL core rule: **Capability domains != Workflow steps**.

The Three-Question Screening does not pass:
- **Ordering Test**: A->B->C->D->E->F can only be linearly serial; reordering breaks the logic
- **Independence**: C "Capability Domain Derivation" and D "Complexity Determination" are sequentially dependent in the workflow and cannot function independently
- Conclusion: This is a classic case of **Anti-Pattern 4 (Workflow Aliasing)**, documented in [../References/anti-patterns.md](../References/anti-patterns.md)

### 10.2 Design Principles

What the pre-analysis engineer needs are **genuine knowledge bodies**, not aliases for workflow steps. It must be able to understand the professional substance, unique risks, and ethical norms of any target profession -- like an HR professional analyzing a job role.

Design principles:
1. **Universal professional perspective**: The first 4 domains should be capable of analyzing any profession
2. **Methodology internalization**: The 5th domain honestly acknowledges the need to internalize UR-SKILL's own methodology
3. **Independent and cross-referenceable**: The 5 domains can be cross-referenced with no temporal dependency

### 10.3 6-Domain Industry Benchmarking

| Knowledge Domain | Industry Benchmark | Benchmark Source |
|:---|:---|:---|
| Requirements Engineering | Requirements Engineering | IEEE SWEBOK v4.0 KA 2 (Elicitation / Analysis / Specification / Validation) |
| Job Competency Analysis | Job Analysis / Competency Modeling | O\*NET KSAO Model, I-O Psychology (Knowledge / Skills / Abilities / Other characteristics) |
| Capability Domain Information Assessment | Information Quality Assessment / Media Literacy | CRAAP Test, SIFT Method, Lateral Reading (source evaluation and cross-verification) |
| Professional Risk Identification | Professional Risk Assessment | HSE 5-step, ISO 31000 (universal red lines + profession-specific risk taxonomy) |
| Professional Ethics | Professional Ethics | APA Ethics Code, IEEE Code of Ethics, CFA Code of Ethics |
| Institutional Knowledge | Institutional Knowledge | UR-SKILL internal methodology (complexity decision tree / anti-patterns / RFC 2119 / checklists) |

### 10.4 Domain Selection Rationale: First 5 Domains vs. 6th Domain

**First 5 Domains = External understanding of the target profession**:

- **Requirements Engineering**: What the user wants to do (goal / domain / deliverable form / implicit assumptions)
- **Job Competency Analysis**: What capabilities this profession requires (KSAO analysis, capability domain mapping)
- **Capability Domain Information Assessment**: Whether the information supporting capability judgments is reliable (official standards vs. AI-generated, timeliness verification, source lineage establishment)
- **Professional Risk Identification**: What unique risks this profession has (beyond just "illegal / discriminatory" -- psychological counseling has psychological intervention risks, finance has conflict-of-interest risks, medicine has misdiagnosis risks)
- **Professional Ethics**: The ethical constraints of this profession (positive obligations + negative constraints, e.g., psychological counseling MUST maintain confidentiality, MUST NOT exploit psychological vulnerability for coercion)

**6th Domain = Internal understanding of UR-SKILL**:

- **Institutional Knowledge**: Internalize the entire methodology. This is the only unavoidable internal knowledge, but it is honestly named without masquerading as a "general skill."

### 10.5 Comparison with Old 6 Domains

| Dimension | Old 6 Domains (Anti-Pattern) | New 6 Domains (Correct) |
|:---|:---|:---|
| Domain Nature | Workflow step aliases, linearly serial | Independent knowledge bodies, cross-referenceable |
| Three-Question Filter | Does not pass | Passes |
| Professional Generality | None (all internal manual content) | First 5 domains can analyze any profession |
| Information Quality | No filtering (use whatever is found) | Has capability domain information assessment, filtering low-quality / AI-generated / outdated info |
| Risk Analysis | Anti-pattern-oriented only | Can analyze profession-specific risk taxonomy |
| Ethical Constraints | Only "touching safety red line -> terminate" | Can understand professional ethics frameworks |

### 10.6 Professional Risk: Unique Risk Taxonomy (Examples)

Different professions have completely different risk taxonomies. The following are examples; actual analysis must be expanded based on the target profession:

| Profession | Universal Safety Red Lines | + Unique Risks of This Profession |
|:---|:---|:---|
| Psychological Counseling | No illegal / discriminatory acts | Must not exploit psychological vulnerability for reverse psychological intervention; must not establish dual relationships |
| Medical Diagnosis | No illegal / discriminatory acts | Must not provide unconfirmed diagnostic conclusions; medication recommendations must be based on clinical evidence |
| Financial Investment | No illegal / discriminatory acts | Must not promise principal-guaranteed returns; must disclose affiliated relationships |
| Legal Consultation | No illegal / discriminatory acts | Must not provide formal legal opinions (when unlicensed); must inform about statute of limitations |
| Educational Tutoring | No illegal / discriminatory acts | Must not substitute for professional special education assessment; must not recommend uncertified "treatment" programs |

### 10.7 Professional Ethics: Bidirectional Structure

Professional ethics is not a simple "don't do X" checklist, but a **bidirectional structure**:

- **Positive Obligations**: Professional duties to actively perform (what you MUST do)
- **Negative Constraints**: Bottom lines that must not be crossed (what you MUST NOT do)
- **Practice Boundaries**: Distinguishing what this profession can do vs. what must be referred out

Using APA Ethics Code (psychological counseling) as illustration:
```
Positive Obligations:
  - MUST protect client privacy and informed consent rights
  - MUST maintain professional competence with regular continuing education
  - MUST take reasonable protective measures in crises

Negative Constraints:
  - MUST NOT exploit psychological vulnerability for coercion or control
  - MUST NOT establish dual relationships outside the therapeutic relationship
  - MUST NOT disclose client information on social media

Practice Boundaries:
  - Can do: Psychological assessment, counseling, and therapy
  - Cannot do: Psychiatric medication prescription (refer to psychiatrist)
  - Cannot do: Forensic psychological evaluation (requires specialized qualification)
```

## 11. Why Step 1 (Parse) Only Does Fact Extraction and Step 2 (Research) Does Deep Analysis

### 11.1 Problem: Contradictions in the Old Design

The old pre-analysis-engineer Step 1 carried excessive cognitive load:

- Mode A Step 1.3: Output "goal + domain + deliverable form"
- Mode B1 Step 1.2: Preliminary gap analysis (missing items / defective items / retainable items)
- Mode C Step 1.3: Map to requirements analysis cards (goal / domain / deliverable form / implicit assumptions)

These actions were nominally "parsing" but substantively required **deep research and institutional knowledge** to complete. Outputting "domain" and "gap judgment" before conducting web research or understanding the target profession's professional substance is logically inverted.

### 11.2 Contradiction Decomposition

| Contradiction | Symptom | Root Cause |
|:---|:---|:---|
| Outputting "domain" without research | Step 1 claims to produce domain attribution but has zero knowledge of the profession's composition | Parsing should only state "what the user says they want to do"; domain attribution requires web research |
| B1 "gap analysis" is essentially research | Determining missing / defective / retainable items requires deep institutional knowledge | Gap analysis = discovering "what's missing," which is the essential work of research |
| Domain declaration confusion | `[WebSearch] declare Job Competency Analysis - Expert` -- action and domain don't match | Domains should declare the knowledge domain the action serves, not the action type |

### 11.3 Correct Boundaries

```
Step 1 (Parse) = Fact Extraction
  Input: User natural language
  Output: Pattern type + user core need summary + tentative profession mapping + implicit assumption list
         (B1: raw structure card / B2: optimization direction + fact summary / C: knowledge source fact card)
  Forbidden: Domain derivation, gap analysis, 6-facet audit, web research

Step 2 (Research) = Deep Cognition
  Input: Step 1 fact cards
  Output: Candidate capability domains (having passed Ordering Test + Three-Question Screening) + professional risk taxonomy + professional ethics + optimization / completion plan
  Actions: Job analysis -> Gap assessment -> Capability derivation -> Web research -> Audit -> Activate optimization
```

### 11.4 Analogy: HR Recruitment Process

```
Step 1 (Parse) = Receiving resumes + reading JD
  -> See: Candidate wrote "proficient in Python" (fact)
  -> Don't judge: Whether Python proficiency is genuine or just scripting (leave for interview)

Step 2 (Research) = Interview + Technical assessment
  -> Verify: Depth of Python understanding (Ordering Test = ask if they can teach others)
  -> Discover: Missing Django experience (gap analysis = compare with role standards)
  -> Decide: Hire or not (Three-Question Screening = independence / irreplaceability / complementarity)
```

### 11.5 Design Principle Summary

- **Facts before judgment**: First know "what exists," then ask "what does it mean"
- **Parsing excludes research**: Parsing = reading, Research = thinking + investigating
- **Domain declarations match actions**: `[WebSearch]` declares which knowledge domain the search serves, not the action type

## 12. UR-SKILL Main SKILL Capability Matrix Redesign

### 12.1 Problem: Workflow Aliasing of Old A-F Radiating Domains

The 6 radiating domains previously used by the UR-SKILL main SKILL:

```
A Semantic Parsing -> B Knowledge Retrieval -> C Architecture Design -> D Content Engineering -> E Quality Assurance -> F Delivery Management
```

Strictly corresponded to workflow steps:

| Old Domain | Workflow |
|:---|:---|
| A Semantic Parsing | Step 1 Parse |
| B Knowledge Retrieval | Step 2 Research |
| C Architecture Design | Step 3 Architect |
| D Content Engineering | Step 4 Execute |
| E Quality Assurance | Step 5 Verify |
| F Delivery Management | Step 7 Deliver |

Not only one-to-one, the names themselves are verbs (Semantic Parsing / Knowledge Retrieval / Content Engineering) -- directly workflow step names. The 4-layer progression (Foundational -> Advanced -> Expert -> Extended) reinforced the "step nesting" feel.

### 12.2 Design Principles

Same as pre-analysis-engineer (section 10), UR-SKILL's radiating domains must be independent knowledge bodies:

1. **Based on Prompt Engineer industry standards**: Academia (Vu & Oppenlaender 2025) + Japan PE-BoK (5 domains) + industry skill matrix
2. **Nouns not verbs**: Each domain is "what you know" not "what you do"
3. **No temporal dependency**: Any workflow step can invoke any domain

### 12.3 New 6-Domain Design

| Knowledge Domain | Industry Benchmark | Substance |
|:---|:---|:---|
| Requirements Engineering & Business Translation | SWEBOK Requirements Engineering / PE Communication Skills | Vague intent -> structured requirements, mapping business goals to SKILL capabilities |
| SKILL Architecture Design | PE System Design / UR-SKILL specific | Capability matrix / progressive loading / complexity decision tree / file dependencies / workflow gating |
| Prompt Systems Engineering | Japan PE-BoK Design Patterns / Structured Output | Information architecture (primacy / recency) / RFC 2119 / attention management / tool binding syntax |
| Quality Engineering | PE-BoK Iterative Improvement / Evaluation | Anti-pattern detection / boundary validation / completeness checking / cross-reference consistency |
| Ethics & Safety | PE-BoK Ethics & Safety / APA Ethics Code | Risk boundaries (illegal / discriminatory / injection) / profession-specific risk taxonomy / professional boundaries |
| Iterative Improvement | PE Version Management / Platform Adaptation / HSE 5-step | Platform adaptation / self-repair after blind spot discovery / metadata optimization / version evolution |

### 12.4 Old vs. New Comparison

```
Old A-F (verbs + serial)                 New 6 Domains (nouns + no temporal order)
A Semantic Parsing -> B Knowledge        Requirements Engineering &         SKILL Architecture Design
Retrieval                                Business Translation
↓                                        Prompt Systems Engineering        Quality Engineering
C Architecture Design -> D Content       Ethics & Safety                   Iterative Improvement
Engineering
↓
E Quality Assurance -> F Delivery        <- Any step can cross-reference any domain
Management
```
