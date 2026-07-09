# Glossary File Design Guide

> Purpose: Define the standard format, content requirements, and design methodology for glossary reference files (glossary.md)
> Core principle: The glossary is the consistency anchor for concepts within the system, eliminating ambiguity and preventing concept drift

---

## 1. Why a Glossary File Is Needed

The glossary is the "semantic protocol" of the SKILL system. When a SKILL involves domain-specific concepts, custom methodologies, or abstract terminology, the same term across different files (SKILL.md body, references/ files, templates/ templates) must point to the same concept.

If the glossary is not maintained:
- The same term is understood differently across files (concept drift)
- Newly introduced LLMs cannot infer the precise definition of a term from context
- Cross-file references create cognitive gaps where "the term is mentioned but not defined"
- Semantic changes to terms during system evolution cannot be tracked

**ur-skill's own particularity**: ur-skill is a "SKILL for designing SKILLs" -- it defines a set of methodological terms (Capability Matrix, Radiating Domain, Ordering Test, Three-Question Screening, Blind Spot Three-Tier Mechanism...). These terms are scattered across multiple files (SKILL.md body, templates/, design-guides/, References/) without a unified definition source. The glossary is the only means of eliminating this dispersion.

The glossary file is a **knowledge-type reference file** (L3), loaded on demand. When an LLM encounters an uncertain term in the SKILL.md body or references/, it loads the glossary to obtain the precise definition.

---

## 2. Standard Format of the Glossary

### 2.1 Four Required Elements

| Element | Description | Why It's Required |
|:---|:---|:---|
| **Term** | Precisely defined name | Unique identifier for retrieval and reference |
| **Definition** | Single-sentence precise definition, unambiguous | Core; the glossary's sole value lies in "what exactly does this term mean" |
| **Domain** | Which concept domain the term is used in | The same term may have different meanings in different domains (e.g., "Gate" in the workflow domain vs. the delivery domain) |
| **Usage Example** | Actual usage within the SKILL system | Definitions are abstract → examples are concrete; "I understood it but don't know how to use it" is a common glossary failure mode |

> Why four elements: The term identifies the retrieval target, the definition eliminates ambiguity, the domain prevents cross-domain confusion, and the usage example bridges abstraction and concreteness. Fewer than four turns the glossary into a "keyword list" rather than a "semantic anchor"; more than four reduces information density.

### 2.2 Format Template

```markdown
## {Term}

- **Definition**: {One-sentence precise definition, using other already-defined terms within the domain}
- **Domain**: {The concept domain in which this term is used, e.g., "Workflow Domain," "Architecture Domain," "Quality Domain"}
- **Example**: {Actual usage in SKILL body / references, 1-2 sentences}
```

### 2.3 Organization Method

Terms are grouped by **Concept Domain**, and within each domain sorted by **logical dependency** (define foundational terms first, then define compound terms that depend on them).

| Sorting Strategy | Applicable Scenario | Why Not Applicable |
|:---|:---|:---|
| Alphabetical order | Large general-purpose dictionaries (100+ terms) | SKILL glossaries typically have 20-50 terms; alphabetical order severs conceptual associations |
| **Concept Domain Grouping + Logical Dependency** | SKILL system glossaries | Terms have dependency relationships -- you must understand "Capability Matrix" before "Radiating Domain" |

> Why group by concept domain: The use case for a glossary is "looking up unfamiliar terms," but the SKILL glossary use case is closer to "understanding the conceptual map of the entire system." Domain grouping helps LLMs build associations between concepts rather than memorizing them in isolation.

### 2.4 Numbering System

Each term is assigned a **G{sequential-number}** identifier (G = Glossary) for cross-file referencing.

```markdown
## G01 Capability Matrix
...
## G02 Core Domain
...
```

> Why numbering: Consistent with anti-pattern numbering (Anti-pattern1) and rule numbering (Rule01), following the UR-SKILL numbering system specification (see structure-guideline.md Section 1.2).

---

## 3. Glossary Content Requirements

### 3.1 Content That Must Be Addressed

- **Each term MUST have a "Definition"**: Without a definition, the glossary is a term list, not a glossary.
- **Definitions MUST use already-defined terms within the domain**: Using undefined terms to explain a definition = circular dependency. Prefer referencing numbered terms already in the glossary.
- **Each term MUST have an "Example"**: Without an example, "I understood it but don't know how to use it."

### 3.2 Prohibited Content

- **Prohibited: Circular definitions**: Term A's definition depends on Term B, and Term B's definition depends on Term A.
- **Prohibited: Over-definition**: Such as "a checklist is a list used for checking" -- explains nothing.
- **Prohibited: External references substituting for definitions**: Such as "see external link for details" -- the glossary is a self-contained semantic anchor; you cannot expect the LLM to look up definitions externally.
- **Prohibited: Vague qualifiers**: Such as "usually," "generally," "in most cases" -- term definitions must be definitive.

### 3.3 Definition Quality Standards

| Standard | Description | Counterexample → Correct Example |
|:---|:---|:---|
| **Single-sentence definition** | Definition completed in one sentence, no more than 50 words | "A Capability Matrix is a matrix containing core domains and radiating domains..." → "Capability Matrix: A structured expression of capabilities consisting of 1 core domain + 3-8 radiating domains x 4 depth levels" |
| **No tautology** | Definition does not repeat the term itself | "A Radiating Domain is the radiating domain of the core domain" → "Radiating Domain: An independent professional capability dimension surrounding the core domain" |
| **Distinguishes similar concepts** | Definition can differentiate easily confused terms | The definitions of "Risk Boundary" and "Professional Boundary" must allow differentiation |

---

## 4. Generation Method (ur-skill Special Notes)

> This SKILL is a "SKILL for designing SKILLs" (ur-skill) and needs its own glossary; it also provides glossary design capability for generated SKILLs.

### 4.1 Creating a Glossary for ur-skill Itself

Follow these steps:

1. **Extract candidate terms**: Scan SKILL.md body, templates/, design-guides/, References/ for proprietary concepts and methodological terms
2. **Deduplicate and categorize**: Merge synonyms, group by concept domain
3. **Sort by logical dependency**: Foundational concepts → Compound concepts → Methodological concepts
4. **Validate completeness**:
   - [ ] Each term appears in at least 2 files (ensuring it's not a one-off use)
   - [ ] Each term has a definition, domain, and example
   - [ ] No circular dependencies between definitions
   - [ ] Similar terms' definitions can distinguish each other

### 4.2 Creating a Glossary for Generated SKILLs

When a generated SKILL contains domain-specific terms (e.g., "PEP 8," "CWE," "OWASP Top 10" in a Python Code Audit SKILL), create a glossary at `references/glossary.md`:

1. **Extract from the core domain**: What is the core domain? What are the radiating domains? What key terms does each domain have?
2. **Extract from examples**: What specialized terms appear in the Input/Output of examples.md?
3. **Extract from anti-patterns**: Do the concepts involved in anti-patterns.md require definition?
4. **Control the count**: 10-30 terms in the glossary, grouped into 2-4 concept domains. Exceeding 30 reduces information density.

### 4.3 Glossary Trigger Conditions

Whether a glossary is needed is not determined by complexity alone, but by Step 2 of the File Dependency Decision Tree in design-rationale.md Section 9:

> **"Does the SKILL create >= 5 proprietary methodological terms, or involve cross-domain intersections (e.g., finance + law, security + compliance)?"**
> -- Yes → Glossary required (trigger = mandatory)

Reference relationship between complexity and glossary (for reference only; final decision by the decision tree):

| Complexity | Glossary | Rationale |
|:---|:---|:---|
| Simple | Not needed | Simple SKILLs have few concepts; proprietary terms are typically < 5; terms are explained inline in the body |
| Medium | Possibly (depends on term count) | Medium SKILLs with >= 5 methodological terms → needed; < 5 → optional |
| Complex | Usually needed | Complex SKILLs almost inevitably have >= 5 proprietary terms or require one due to cross-domain intersection |

---

## 5. Relationship Between Glossary and Other System Files

| File | Relationship | Description |
|:---|:---|:---|
| **SKILL.md body** | Body references term numbers | The first occurrence of a term in the body is annotated with its number reference: `Capability Matrix (G01)` |
| **references/anti-patterns.md** | Anti-pattern descriptions reference term numbers | Anti-pattern "Manifestation" and "Harm" reference term numbers to ensure conceptual consistency |
| **references/troubleshooting.md** | Troubleshooting references term numbers | Fault symptom descriptions use term numbers |
| **templates/** | Templates reference term numbers | Concepts in capability-architecture-template.md reference glossary numbers |

> Why cross-file term number references: Ensures consistent understanding of the same concept across all system files. Number references are more efficient than inline definitions -- LLMs seeing a number know to look up the precise definition in the glossary, avoiding redundant definitions in the body.

---

## 6. Completeness Checklist

When designing a glossary file, check each item:

- [ ] Each term has four elements (Term, Definition, Domain, Example)
- [ ] Definitions are completed in one sentence, no tautology
- [ ] No circular dependencies between definitions
- [ ] Similar terms' definitions can distinguish each other
- [ ] Grouped by concept domain, sorted by logical dependency within domain
- [ ] Terms have G{sequential-number} identifiers
- [ ] Term count matches complexity (medium 10-20, complex 20-30)
- [ ] Each term appears at least 2 times in the system (not a one-off use)
- [ ] No external references substituting for definitions (self-contained)
- [ ] File < 200 lines; split if exceeded
