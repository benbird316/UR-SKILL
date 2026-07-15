# Script File Template

> **Purpose**: Define the standard structure for script files under the generated SKILL's scripts/ directory
> **Core Principle**: Scripts are read-first by default; must annotate safety level and side effects; high-risk operations are prohibited
> **Design Methodology**: See [design-guides/scripts-design-guide.md](../design-guides/scripts-design-guide.md)

---

## 1. Script Header Information

```python
#!/usr/bin/env python3
"""
{Script Name}

Purpose: {One-sentence description of purpose}
Safety Level: {Safe / Medium Risk / High Risk}
Input: {Input file / data}
Output: {Output format}
Side Effects: {None / Read / Write / Network}

Author: {Generator}
Date: {YYYY-MM-DD}
"""
```

---

## 2. Safety Principles

| Principle | Requirement |
|:---|:---|
| Read-First | Prefer reading; do not modify the filesystem |
| Idempotency | Consistent results on multiple executions |
| Self-Contained | No external environment dependencies |
| Least Privilege | Only request necessary permissions |
| Input Validation | Validate all input; reject invalid input |

---

## 3. Script Structure Template

```python
#!/usr/bin/env python3
"""
{Script Name}

Purpose: {One-sentence description of purpose}
Safety Level: {Safe / Medium Risk / High Risk}
Input: {Input file / data}
Output: {Output format}
Side Effects: {None / Read / Write / Network}
"""

import os
import re

# Configuration
SAFE_MODE = True  # True=read-only, False=allows writes (requires human confirmation)


def main():
    """Main function"""
    input_path = validate_input()
    result = process(input_path)
    print(result)


def validate_input():
    """Validate input"""
    # Check that input exists
    # Check that input format is valid
    # Reject invalid input
    pass


def process(input_path):
    """Processing logic"""
    # Read-only operations / pure computation / no side effects
    pass


if __name__ == "__main__":
    main()
```

---

## 4. Script Type Selection

| Type | Purpose | Safety Level |
|:---|:---|:---:|
| Scan script | Static check, identify issues | Safe |
| Validation script | Validate format, constraints, compliance | Safe |
| Generation script | Generate content, fill templates | Medium Risk |
| Conversion script | Format conversion, data migration | Medium Risk |
| Deployment script | Deploy to production environment | High Risk |

---

## 5. Completeness Checklist

- [ ] Script has safety level annotation
- [ ] Script has side effect description
- [ ] Script has input validation
- [ ] Script does not perform high-risk operations (delete, write, network, system commands)
- [ ] Script outputs to stdout, does not directly write files
- [ ] Script has error handling
- [ ] Script has logging
- [ ] Scripts at Medium Risk and above have undergone manual review
- [ ] Script is self-contained, no external environment dependencies
- [ ] Script is idempotent, consistent results on multiple executions
- [ ] File < 200 lines
