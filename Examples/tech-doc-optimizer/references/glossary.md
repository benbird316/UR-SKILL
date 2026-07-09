# Glossary: Technical Document Lossless Semantic Optimization Terminology

> Methodology terminology definitions used by this SKILL, complementing references/knowledge-reference.md.

| Term | English | Definition |
|:---|:---|:---|
| Semantic Fidelity | Semantic Fidelity | Retain 100% of original semantic units during optimization, without adding, deleting, or tampering with information |
| Semantic Compression | Semantic Compression | Identify and protect incompressible elements during compression (core instructions, code blocks, and execution trigger conditions must be fully preserved; qualifying statements, risk warnings, and quantitative thresholds must not be removed), and select compression strategy based on optimization objectives as a boundary control principle |
| Modality Adaptation | Modality Adaptation | The principle that optimization strategies must adapt to the modality of the target document (text, code, structured data); non-text modalities require pre-defined semantic units and annotation labels before optimization can proceed |
| Closed-Loop Reproducibility | Closed-Loop Reproducibility | The principle that every optimization result must be verifiable through baseline comparison and reverse restoration, ensuring that no information is lost in any round of the optimization loop |
| Sequential Logic Protection | Sequential Logic Protection | A sub-mechanism of the Circuit Breaker triggered when timeline compression causes temporal disorder, limiting compression to form + vocabulary layer only to preserve sequential integrity |
| Classification Dimension Retention Rate | Classification Dimension Retention Rate | The percentage of five-dimensional classification tags (direction/type/scope/status/lifecycle) preserved after optimization; target >= 95%, a key quality metric in fidelity verification |
| Net Compression Rate | Net Compression Rate | (1 − optimized tokens / original tokens) × 100%, measuring the overall token reduction achieved after all compression layers are applied; target >= 30% |
| Five-Dimensional Classification Tags | Five-Dimensional Classification Tags | Label semantic units across five dimensions: direction (positive/negative/neutral), type (definition/operation/evaluation/reference), scope (global/local/example), status (stable/draft/deprecated), and lifecycle (creation/maintenance/archival) |
| Dual-Channel Deduplication | Dual-Channel Deduplication | Simultaneously use SimHash fingerprints (structural similarity) and semantic vectors (semantic similarity) for redundancy detection, covering both structural and semantic layers |
| Four-Layer Scope Detection | Four-Layer Scope Detection | Detect redundancy at four levels—same sentence, adjacent sentences, cross-sentence, and method-detail—progressing layer by layer to prevent false deletions |
| Circuit Breaker | Circuit Breaker | A protection mechanism triggered when timeline compression causes temporal disorder or causal chain strength decay exceeds 0.3, automatically degrading to perform only format-layer and lexical-layer compression |
| Seven-Step Restoration | Seven-Step Restoration | Locate → Trace → Complete → Verify → Annotate → Evaluate → Record, used to restore necessary semantic elements lost during optimization |
| Five-Fold Verification | Five-Fold Verification | Baseline comparison + reverse restoration + logic strength verification + ambiguity screening + targeted fuzzy semantics audit, covering all quality dimensions |
| Retainable Fuzzy Semantics | Retainable Fuzzy Semantics | Ineliminable fuzzy expressions such as probability judgments, conditional dependencies, and risk warnings; must be preserved and must not be strengthened during optimization |
| Eliminable Fuzzy Semantics | Eliminable Fuzzy Semantics | Fuzzy expressions with no actual information content, such as those with no choice space, falsifiability, or semantic idling; can be removed |
| Redundancy Classification Mapping | Redundancy Classification Mapping | Establish mapping relationships between redundancy types (decorative, explanatory, repetitive, structural) and classification dimensions to avoid cross-dimensional false deletions |
| Semantic Density | Semantic Density | The number of effective semantic units per token, used to measure optimization efficiency |
| Logic Strength Decay | Logic Strength Decay | 1 − (post-optimization confidence / baseline confidence), measuring whether optimization weakened the logical chain, target value ≤0.15 |
| Executability Index | Executability Index | (Navigation clarity + Boundary completeness) / 2, measuring the clarity of operational instructions, target value ≥0.90 |
| Index Coverage | Index Coverage | The proportion of entities/relationships/conclusions correctly covered in the index, target value ≥95% |
| Format Normalization | Format Normalization | Unify formatting elements such as date formats, number formats, unit formats, and numbering styles within documents |
| Style Governance | Style Governance | Establish and maintain a global style guide to ensure consistency in terminology usage, tone, and heading naming across documents |
