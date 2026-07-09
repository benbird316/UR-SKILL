# Troubleshooting: Technical Documentation Lossless Semantic Optimization

> Common troubleshooting guide for Technical Documentation Lossless Semantic Optimization.

## Problem: Circuit Breaker Triggered Excessively

**Symptom**: During the Layered Compression step, the Circuit Breaker triggers repeatedly, causing optimization to stop at the Formal Layer + Lexical Layer only.

**Possible Causes**:
1. The document contains dense timeline descriptions (e.g., project plans, version histories), where compressing the timeline inevitably leads to chronological disorder
2. The baseline Causal Chain Strength is too high (>0.9), making even minor changes likely to trigger the 0.3 Decay Rate threshold

**Solutions**:
1. Pre-classify timeline-dense documents as "Chronologically Sensitive" and skip Discourse Layer compression entirely
2. Adjust the Circuit Breaker threshold to use relative Decay Rate (30% of the original strength rather than an absolute value of 0.3)
3. Execute stepwise: first optimize non-chronological sections independently, then handle chronological sections with minimal intervention

---

## Problem: Five-Dimensional Classification Tag Dimension Conflicts

**Symptom**: The classification tags assigned to the same entity in different locations exhibit dimension conflicts (e.g., direction tags are incompatible with type tags).

**Possible Causes**:
1. The document itself contains inconsistent concept usage
2. The same entity across chapters was not detected during Baseline extraction
3. The inter-dimension mapping rules for the five-dimensional classification are incomplete

**Solutions**:
1. Perform cross-document entity alignment: merge all tag occurrences for the same entity
2. Apply classification conflict detection rules: Direction [Positive/Negative/Neutral] must not directly contradict Type [Definition/Operation/Evaluation]
3. Flag conflicting tags as items requiring user confirmation

---

## Problem: Cross-References Break After Optimization

**Symptom**: The optimized document contains references pointing to non-existent sections or figures (e.g., "See Section 3.2" but that section no longer exists).

**Possible Causes**:
1. Referenced sections were merged or deleted during logical reorganization
2. Reference ID integrity was not preserved during compression
3. Cross-document references were not synchronized during updates

**Solutions**:
1. Build a complete reference dependency graph before logical reorganization
2. Add protection markers to each referenced anchor point and prohibit their deletion
3. Execute reference integrity verification (see `SKILL.md` Step 4: Verify — Fidelity Consistency Verification)

---

## Problem: Confidence Decay Rate Exceeds Threshold but Optimization Quality Is Intuitively Good

**Symptom**: The calculated Confidence Decay Rate exceeds 0.15, but manual evaluation deems the optimized document to be of higher quality.

**Possible Causes**:
1. Baseline Confidence was assigned too high: sources with lower credibility were given an excessively high initial confidence score
2. The Confidence calculation model is overly sensitive: it is too conservative about subtle semantic changes caused by text streamlining

**Solutions**:
1. Recalibrate Baseline Confidence: differentiate source credibility tiers (official documentation 0.95, community content 0.75, AI-generated 0.60)
2. Introduce manual evaluation weighting: when the Decay Rate exceeds the threshold but manual evaluation passes, mark as "Manual Confirmation Passed"
3. Record the cause of Confidence decay, distinguishing between "Benign Decay" (redundancy removal) and "Malignant Decay" (information loss)

---

## Problem: Code Block Retention Rate Below Standard

**Symptom**: Post-optimization Code Block retention rate is below 90%, or code blocks have been improperly modified internally.

**Possible Causes**:
1. The compression algorithm treated Code Block comments as redundant information and removed them
2. Code formatting operations altered the original coding style
3. Traceability records were not preserved during cross-document migration

**Solutions**:
1. Apply protection locks to all Code Blocks before compression, setting an indivisible attribute
2. Only allow whitespace adjustments external to Code Blocks (indentation normalization); zero internal content modification
3. Generate migration traceability records when moving Code Blocks across documents (migration timestamp, source document ID)

---

## Problem: Fuzzy Semantics Misclassification

**Symptom**: Fuzzy Semantics that should be preserved (e.g., probabilistic judgments) are incorrectly classified as "eliminable" and removed.

**Possible Causes**:
1. Fuzzy Semantics classification rules are not granular enough
2. The context window is insufficient to recognize the qualifying function of fuzzy terms

**Solutions**:
1. Apply the "Three Questions for Fuzzy Semantics": Does this term affect the certainty of conclusions? Does it have conditional dependencies? Would its removal alter the reader's understanding?
2. Expand the context window to the paragraph level for semantic classification judgment
3. Default any uncertain classification result to "Preserve" and take a conservative approach
