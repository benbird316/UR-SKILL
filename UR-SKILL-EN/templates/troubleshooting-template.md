# Troubleshooting File Template

> Purpose: Defines the standard structure for generating a SKILL's troubleshooting.md
> Core Principle: Every fault must be paired with "Symptom -> Root Cause -> Fix Action"; declarative-only prompts are prohibited
> For design methodology details, see [design-guides/troubleshooting-design-guide.md](../design-guides/troubleshooting-design-guide.md)

---

## 1. {Fault Domain 1}

### T01 {Fault Name}

- **Symptom**: {Observable manifestation visible to the user/LLM}
- **Root Cause**: {Underlying reason causing the symptom}
- **Fix Action**:
  1. {Specific step 1}
  2. {Specific step 2}
  3. {Specific step 3}

### T02 {Fault Name}

- **Symptom**: {Specific manifestation}
- **Root Cause**: {Underlying reason}
- **Fix Action**:
  1. {Specific step 1}
  2. {Specific step 2}

---

## 2. {Fault Domain 2}

### T03 {Fault Name}

- **Symptom**: {Specific manifestation}
- **Root Cause**: {Underlying reason}
- **Fix Action**:
  1. {Specific step 1}
  2. {Specific step 2}

---

## Completeness Checklist

- [ ] Each fault contains all three elements: Symptom, Root Cause, Fix Action
- [ ] Symptoms are specific and observable
- [ ] Root cause explains "why"
- [ ] Fix actions are executable
- [ ] Faults are grouped by fault domain (3-5 domains)
- [ ] Faults are numbered with T{SequenceNumber}
- [ ] Number of faults matches complexity (medium: 8-12, complex: 12-15)
- [ ] File < 200 lines
