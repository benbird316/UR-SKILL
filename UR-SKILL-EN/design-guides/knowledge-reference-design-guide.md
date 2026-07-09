# Knowledge Reference File Design Guide

> Purpose: Defines the standard format, subtype classification, and design methodology for knowledge reference files
> Core Principle: Knowledge files are about "what to know", not "how to do" or "what not to do" -- responsibilities are separated from operational, instructional, and specification file types

---

## 1. Why a Knowledge Reference File Design Guide Is Needed

When UR-SKILL only had 5 design guides, they covered operational (anti-patterns, troubleshooting), instructional (examples), specification (spec definitions), and resource (templates/schema) types, but missed the most fundamental type: **knowledge files**. This guide fills that gap.

Knowledge files store the **domain-specific expertise** that a SKILL needs when performing tasks -- not "how to do" (workflow), not "what not to do" (anti-patterns), but "what the facts and rules are in this domain."

Without defining knowledge files:
- Domain knowledge gets crammed into the SKILL.md body → body bloats, violating progressive loading
- Domain knowledge gets scattered across multiple files → duplication, inconsistency, unmaintainable
- LLM must rely on general knowledge from training data → unable to access SKILL-specific domain depth
- Knowledge updates require modifying multiple files → high change risk

**Typical scenarios**:
- A Python code security audit SKILL needs detailed OWASP Python Top 10 vulnerability explanations → knowledge file
- A REST API design SKILL needs HTTP status code reference and RESTful constraints → knowledge file
- A frontend component development SKILL needs React Hooks rules and performance patterns → knowledge file
- A financial analysis SKILL needs valuation model formulas and market rules → knowledge file

Knowledge files are **knowledge-type reference files** (L3), loaded on demand. When the LLM needs domain-specific expertise to complete a workflow step, it loads the knowledge file.

---

## 2. Subtype Classification of Knowledge Files

### 2.1 Four Major Subtypes

| Subtype | Description | Typical Filename | When to Use |
|:---|:---|:---|:---|
| **K1 Domain Knowledge** | Concepts, rules, methodology in a specialized domain | `domain-knowledge.md`, `owasp-top10.md` | The SKILL's core task depends on domain-specific expertise |
| **K2 API/CLI Reference** | Interface parameters, command syntax, return values | `api-reference.md`, `cli-reference.md` | The SKILL needs to invoke specific external tools or APIs |
| **K3 Configuration/Policy Documents** | Configuration schemas, company policies, business rules | `policy-rules.md`, `config-schema.md` | The SKILL needs to follow organization-specific rules or configurations |
| **K4 Design Patterns** | Reusable code/architecture patterns | `patterns.md`, `architecture-patterns.md` | The SKILL needs to apply the same set of patterns across multiple scenarios |

> Why subtypes: Different types of knowledge files have different element requirements. API references need parameter tables, domain knowledge needs concept explanations, pattern guides need scenario → solution → trade-off. A uniform format would lose the information structure unique to each subtype.

### 2.2 Subtype Selection Decision Tree

```
SKILL needs a knowledge reference file?
├── Needs to invoke external tools/APIs? → K2 API/CLI Reference
├── Needs to follow organizational rules/configurations? → K3 Configuration/Policy Documents
├── Needs to apply reusable patterns? → K4 Design Patterns
├── Other domain-specific expertise? → K1 Domain Knowledge
└── None of the above? → May not need a knowledge file
```

---

## 3. Standard Formats for Each Subtype

### 3.1 K1 Domain Knowledge

**Three elements**:

| Element | Description | Why Required |
|:---|:---|:---|
| **Concept Definition** | Precise definition of core concepts | Entry point for knowledge; without defining concepts, subsequent rules and constraints have no anchor |
| **Rules/Constraints** | Core rules of the domain | Operability of knowledge; definitions without rules = encyclopedia without working knowledge |
| **Priority/Trade-off** | Priority when rules conflict | Rules often conflict in real scenarios; without stating priorities, LLM cannot make decisions |

**Format template**:

```markdown
## {Concept Name}

**Definition**: {One-sentence precise definition}

**Rules**:
- {Rule 1}
- {Rule 2}
- {Rule 3}

**Priority**: When {Rule A} conflicts with {Rule B} → {Decision rule}
```

**Example (OWASP Python Top 10 excerpt)**:

```markdown
## SQL Injection

**Definition**: An attacker concatenates user input into SQL statements to execute unintended database operations.

**Rules**:
- MUST use parameterized queries instead of string concatenation
- MUST NOT embed user input directly into SQL statements
- SHOULD use ORM instead of raw SQL (unless performance requirements dictate otherwise)

**Priority**: ORM convenience vs. parameterized queries → Parameterized queries take priority. ORM-generated SQL still requires review.
```

### 3.2 K2 API/CLI Reference

**Three elements**:

| Element | Description | Why Required |
|:---|:---|:---|
| **Call Signature** | Basic signature of the command/method | Entry point for knowledge; unable to invoke without knowing the signature |
| **Parameter Table** | Parameter name, type, required, default value, description | Core of knowledge; parameters are key to invocation correctness |
| **Return Value/Output** | Normal output, error output format | Boundary of knowledge; unable to process results without knowing the return format |

**Format template**:

```markdown
## {Tool/API Name}

### Call Signature
`{command_signature}` or `{method_signature}`

### Parameters

| Parameter | Type | Required | Default | Description |
|:---|:---|:---:|:---|:---|
| {param1} | {type} | MUST | {default} | {Description} |

### Return Value
- Success: {Format and example}
- Failure: {Error format and common error codes}
```

### 3.3 K3 Configuration/Policy Documents

**Three elements**:

| Element | Description | Why Required |
|:---|:---|:---|
| **Policy Statement** | Content of the rule | Body of knowledge |
| **Scope of Application** | When the rule applies and when it doesn't | Unclear boundaries = rule misuse or omission |
| **Violation Handling** | Consequences when violated | Gives the rule enforcement power |

**Format template**:

```markdown
## {Policy Name}

**Rule**: {Policy content}

**Scope of Application**:
- Applicable: {Scenario A, Scenario B}
- Not Applicable: {Scenario C}

**Violation Handling**: {Specific action when violated}
```

### 3.4 K4 Design Patterns

**Four elements**:

| Element | Description | Why Required |
|:---|:---|:---|
| **Scenario** | Under what conditions to use | Pattern matching entry point |
| **Solution** | How specifically to do it | Pattern content |
| **Trade-off** | Pros and cons of the solution | Basis for pattern selection |
| **Non-Applicable Scenarios** | Under what conditions not to use | Anti-pattern prevention |

**Format template**:

```markdown
## {Pattern Name}

**Scenario**: {Under what requirements/constraints to use}

**Solution**: {Specific approach, with code/configuration examples}

**Trade-off**:
- Advantages: {Benefits}
- Costs: {Costs}

**Non-Applicable Scenarios**: {When not to use, and why}
```

---

## 4. General Design Principles for Knowledge Files

### 4.1 Atomicity

One file, one topic. K1 domain knowledge split by domain, K2 API references split by module, K3 policies split by rule group, K4 patterns split by pattern domain.

> Why atomicity: The core of progressive loading -- only load the knowledge needed. One file containing SQL injection + XSS + CSRF → the LLM is forced to load all when it only needs SQL injection knowledge.

### 4.2 Referencability

Every rule/constraint in knowledge files should have a number, making it easy for the SKILL.md body to reference.

```markdown
## K1.1 Parameterized Queries

**Rules**:
- {KN-01} MUST use parameterized queries ...
```

### 4.3 Timeliness Annotation

Every piece of knowledge in knowledge files should have source and timeliness annotations.

```markdown
> **Source**: OWASP Top 10 2021 | **Validity**: Long-term | **Review Cycle**: 12 months
```

### 4.4 Relationship with Body

The body does not duplicate the content of knowledge files. The body triggers loading through references:

```markdown
**K1 Domain Knowledge**: When auditing Python code, load references/owasp-python-top10.md on demand
```

---

## 5. Generation Method (UR-SKILL Special Notes)

> This SKILL is a "SKILL that designs SKILLs" (UR-SKILL). It does not directly use knowledge files itself (UR-SKILL's own domain knowledge is already distributed across design-guides/ and templates/); but it provides knowledge file design capability for generated SKILLs.

### 5.1 Creating Knowledge Files for Generated SKILLs

1. **Derive from capability domains**: Each radiating domain may require corresponding knowledge files
   - E.g., "Security Audit" radiating domain → K1 Domain Knowledge (vulnerability types), K4 Design Patterns (security patterns)
2. **Judge from workflow steps**: Domain expertise retrieved in research steps → K1 Domain Knowledge; external tools invoked in execution steps → K2 API/CLI Reference
3. **Determine from complexity**: Simple SKILLs don't need independent knowledge files (inline in body); medium and above require them
4. **Control knowledge scope**: Only include the knowledge needed for SKILL task execution; don't pursue "a complete knowledge base for the domain"

### 5.2 Trigger Conditions for Knowledge Files

Whether a knowledge file is needed is not determined by complexity alone, but by Step 1 of the design-rationale.md §9 file dependency decision tree:

> **"Does the core domain depend on an external knowledge base (e.g., OWASP/RFC/industry standards/regulations/API docs/academic theory systems)?"**
> -- Yes → knowledge-reference file needed (mandatory if triggered), subtype selected per §2.2 subtype decision tree

Reference relationship between complexity and knowledge files (for reference only; final decision by decision tree):

| Complexity | Knowledge File | Rationale |
|:---|:---|:---|
| Simple | Not needed (domain knowledge inline in body) | Simple SKILLs have limited knowledge; inlining is more efficient |
| Medium | Possible (depends on whether reliant on external knowledge base) | Reliant on external knowledge base → 1-2 K1 domain knowledge files; not reliant → not needed |
| Complex | Typically needed (depends on whether reliant on external knowledge base) | Reliant on external knowledge base → 2-4 files (may mix K1-K4 subtypes); not reliant → not needed |

---

## 6. Relationship Between Knowledge Files and Other Reference File Types

| Comparison Dimension | Knowledge (K) | Operational (Anti-patterns/Troubleshooting) | Instructional (Examples) | Specification (Spec) |
|:---|:---|:---|:---|:---|
| Core Question | "What to know" | "How to do / What not to do" | "Learn by looking at this" | "What the standard is" |
| Content Nature | Facts, rules, concepts | Processes, steps, detection | Input/Output pairs | Field constraints, validation rules |
| Update Frequency | By domain changes | By practice accumulation | By scenario expansion | By standard evolution |
| Typical Files | owasp-top10.md, react-patterns.md | anti-patterns.md, troubleshooting.md | examples.md | metadata-spec.md |

---

## 7. Completeness Checklist

When designing knowledge files, check item by item:

- [ ] Subtype selected (at least one of K1/K2/K3/K4)
- [ ] Conforms to subtype element requirements (K1: concept definition + rules + priority; K2: signature + parameter table + return value; K3: policy + scope + violation handling; K4: scenario + solution + trade-off + non-applicable scenarios)
- [ ] One file, one topic (atomicity)
- [ ] Every rule/constraint has a number (referencability)
- [ ] Knowledge has source and timeliness annotations
- [ ] Body does not duplicate knowledge file content (only references)
- [ ] Knowledge scope only covers what is needed for SKILL execution (not pursuing a complete encyclopedia)
- [ ] File < 200 lines; if exceeded, split into multiple atomic files
- [ ] Files do not cross-reference each other (progressive loading constraint)
