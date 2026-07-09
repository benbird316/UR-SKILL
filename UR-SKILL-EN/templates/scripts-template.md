# Scripts File Template

> Purpose: Defines the standard structure for script files under a generated SKILL's scripts/ directory
> Core Principle: Scripts are read-only first; must annotate safety level and side effects; high-risk operations are prohibited
> For design methodology details, see [design-guides/scripts-design-guide.md](../design-guides/scripts-design-guide.md)

---

## 1. Script Header

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
| Read-Only First | Prioritize reading; do not modify the filesystem |
| Idempotency | Multiple executions produce the same result |
| Self-Contained | No dependency on external environment |
| Least Privilege | Request only necessary permissions |
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
SAFE_MODE = True  # True = read-only, False = allow write (requires manual confirmation)


def main():
    """Main function"""
    input_path = validate_input()
    result = process(input_path)
    print(result)


def validate_input():
    """Validate input"""
    # Check if input exists
    # Check if input format is valid
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
| Scan Script | Static checking, identify issues | Safe |
| Validation Script | Validate format, constraints, compliance | Safe |
| Generation Script | Generate content, populate templates | Medium Risk |
| Conversion Script | Format conversion, data migration | Medium Risk |
| Deployment Script | Deploy to production environment | High Risk |

---

## 5. Completeness Checklist

- [ ] Script has safety level annotation
- [ ] Script has side effect description
- [ ] Script has input validation
- [ ] Script does not perform high-risk operations (delete, write, network, system commands)
- [ ] Script outputs to stdout, does not write files directly
- [ ] Script has error handling
- [ ] Script has logging
- [ ] Medium-risk and above scripts undergo manual review
- [ ] Script is self-contained, no dependency on external environment
- [ ] Script is idempotent; multiple executions produce the same result
- [ ] File < 200 lines
