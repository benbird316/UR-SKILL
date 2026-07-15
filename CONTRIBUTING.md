# Contributing Guide

Thank you for your interest in UR-SKILL! This guide covers everything you need to contribute effectively.

## Table of Contents

- [Quick Links](#quick-links)
- [How to Report a Bug](#how-to-report-a-bug)
- [How to Submit a Pull Request](#how-to-submit-a-pull-request)
- [Development Setup](#development-setup)
- [Validation Pipeline (Must Pass Before Merge)](#validation-pipeline-must-pass-before-merge)
- [Directory Structure & Conventions](#directory-structure--conventions)
- [Code Style](#code-style)
- [Contributors](#contributors)

---

## Quick Links

| Resource | Link |
|:---|:---|
| Issue Tracker | [GitHub Issues](https://github.com/benbird316/UR-SKILL/issues) |
| Discussions | [GitHub Discussions](https://github.com/benbird316/UR-SKILL/discussions) |
| CI Status | [Actions](https://github.com/benbird316/UR-SKILL/actions) |

---

## How to Report a Bug

### Before Submitting

1. Search [Issues](https://github.com/benbird316/UR-SKILL/issues) to check if the bug has already been reported.
2. Confirm you are using the latest version.

### Bug Report Template

Please include the following in your issue:

```
**Title**: [Bug] Brief description of the issue

**Environment**:
- OS: [e.g. Windows 11 / macOS 14 / Ubuntu 22.04]
- Python version: [e.g. 3.12.3]
- UR-SKILL version/commit: [e.g. c2a2462]

**Steps to Reproduce**:
1. Run command '...'
2. ...
3. See error

**Expected Behavior**:
What should have happened.

**Actual Behavior**:
What actually happened.

**Additional Info**:
Error logs or screenshots.
```

---

## How to Submit a Pull Request

### 1. Fork the Repository

Fork the repo on GitHub, then clone:

```bash
git clone https://github.com/YOUR_USERNAME/UR-SKILL.git
cd UR-SKILL
git remote add upstream https://github.com/benbird316/UR-SKILL.git
```

### 2. Create a Branch

```bash
git checkout -b feature/your-feature-name
```

### 3. Develop & Test

```bash
pip install pyyaml pytest
python -m pytest tests/ -v
```

### 4. Run Validation

**Chinese version**:
```bash
python UR-SKILL-CN/Scripts/validate_skill.py --skill-dir UR-SKILL-CN --lang zh-cn
```

**English version**:
```bash
python UR-SKILL-EN/Scripts/validate_skill.py --skill-dir UR-SKILL-EN --lang en-us
```

**Bilingual sync check**:
```bash
python UR-SKILL-CN/Scripts/bilingual_sync.py
```

### 5. Commit

```bash
git add .
git commit -m "feat: brief description of your change"
# or fix: / docs: / refactor: / test:
```

Commit message conventions:
- `feat:` — New feature
- `fix:` — Bug fix
- `docs:` — Documentation changes
- `refactor:` — Code refactoring (no functional change)
- `test:` — Test changes
- `chore:` — Maintenance work

### 6. Push & Create PR

```bash
git push origin feature/your-feature-name
```

Then create a Pull Request on GitHub. The PR description should explain:
- **What** was changed
- **Why** it was changed
- Related Issue number (if any, use `Closes #123`)

### PR Merge Requirements

All PRs must pass before merging:
- [ ] **validate_skill.py CN passes**
- [ ] **validate_skill.py EN passes**
- [ ] **pytest all pass**
- [ ] **bilingual_sync.py shows no structural differences**
- [ ] At least one maintainer review approval

---

## Development Setup

```bash
# Clone and install dependencies
git clone https://github.com/benbird316/UR-SKILL.git
cd UR-SKILL
pip install pyyaml pytest

# Run tests to confirm environment is working
python -m pytest tests/ -v
```

## Validation Pipeline (Must Pass Before Merge)

All PRs automatically trigger GitHub Actions running the following checks:

| Step | Command | Description |
|:---|:---|:---|
| Unit Tests | `python -m pytest tests/ -v` | 48 tests |
| CN Validation | `python UR-SKILL-CN/Scripts/validate_skill.py ...` | SKILL.md quality check |
| EN Validation | `python UR-SKILL-EN/Scripts/validate_skill.py ...` | English version quality check |
| Bilingual Sync | `python UR-SKILL-CN/Scripts/bilingual_sync.py` | File structure alignment check |

**All checks must pass before merging**. If validation fails:
1. Check the CI logs to identify the issue
2. Fix and push again
3. If it's a false positive, modify the relevant rules under `placeholders.allowed_patterns` or `placeholders.allowed_literals` in `config.zh-cn.yaml` or `config.en-us.yaml`

---

## Directory Structure & Conventions

### Bilingual Maintenance Rules

The CN and EN directories are mirror structures. **Any change to the CN directory must be synced to the corresponding file in the EN directory**.

Exceptions:
- `config.zh-cn.yaml` exists only in CN; `config.en-us.yaml` exists only in EN
- SKILL.md body content is independently translated (Chinese examples in CN, English examples in EN)

Run `bilingual_sync.py` after syncing to confirm nothing was missed.

### File Naming

- SKILL.md — PascalCase (Agent Skills specification)
- Python scripts — snake_case: `validate_skill.py`
- YAML config — kebab-case: `config.zh-cn.yaml`
- Markdown docs — kebab-case: `boundary-design-guide.md`
- Test files — `test_` prefix: `test_config_loader.py`

### Path Conventions

- References inside SKILL.md use `./` relative paths (relative to the SKILL.md directory)
- Do not use bare paths starting with `templates/`, `design-guides/`, etc. (self-containment check)

---

## Code Style

### Python

- Python 3.12+
- Type annotations using standard library (`Path | None`, not `Optional[Path]`)
- Indentation: 4 spaces
- Line width: 100 characters
- Docstrings: Chinese (CN code) or English (EN code)

### Markdown

- Aligned tables
- Code blocks with language tags
- No emoji (except in SKILL body examples)
- Single `#` heading only once per file

### YAML Config

- Regular expressions should be written in double-quoted strings to avoid single-quote backslash escaping issues
- List items use `- ` prefix, no trailing commas
- After loading, patterns should be pre-validated with `re.compile()` in `config_loader.py`

---

## Contributors

Maintainer:
- **benbird316** — Project creator

Want to become a contributor? Start with an issue labeled `good first issue`.

---

## Code of Conduct

By participating in this project, you agree to abide by the [Contributor Covenant 2.1](https://www.contributor-covenant.org/version/2/1/code_of_conduct/) Code of Conduct. Be respectful, communicate constructively. Violations should be reported to the project maintainer.
