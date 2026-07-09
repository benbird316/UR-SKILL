# Changelog

All notable changes to UR-SKILL will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [1.1.0] - 2026-07-10

### Added

- **agentskills.io frontmatter compliance**: SKILL.md frontmatter now follows the [agentskills.io specification](https://agentskills.io/specification)
  - Custom fields (`type`, `whenToUse`) moved under `metadata` block
  - Added `license`, `compatibility`, `allowed-tools` fields
  - CN name: `ur-skill-cn`, EN name: `ur-skill-en` (matching parent directory)
- **JSON Schema** (`templates/skill-schema.json`): Structured frontmatter validation schema (compliant with agentskills.io + UR-SKILL extensions). Synced to both CN and EN directories.
- **Schema validation in CI**: Optional `jsonschema`-based validation integrated into `validator_format.py`. Gracefully falls back if `jsonschema` is not installed.
- **install.py**: Supports `--lang zh-cn|en-us` for language-specific installation. Only installs the SKILL package content (SKILL.md + subdirectories), not the entire repository. Excludes `__pycache__`. Language-aware default install directory name.
- **bilingual_sync.py**: Synced to EN directory (was CN-only). Now both language versions can independently check structural consistency.
- **Sub-agent detection in Step 1 (Pre-Analysis)**: Workflow now detects sub-agent capability. Path A uses `[Skill]` tool when available; Path B falls back to `[Read]` + inline execution on unsupported platforms. Replaced declarative role-switch with explicit context-awareness note.
- **agent/SKILL.md output constraint**: Added MUST NOT prohibiting self-referential language ("as a pre-analysis engineer") in output, preventing identity pollution when sub-agent output carries into main context.

### Changed

- **README.md**: Fully rewritten in English (was bilingual Chinese/English). Added TL;DR, feature comparison table, "Who Is This For" audience matrix, Quick Start guide, CLI Tools Reference table, and Design Philosophy section.
- **CONTRIBUTING.md**: Rewritten from Chinese to full English
- **CHANGELOG.md**: Rewritten from Chinese to full English
- **Config per language**: CN now contains only `config.zh-cn.yaml` (removed `config.en-us.yaml`); EN now contains only `config.en-us.yaml` (removed `config.zh-cn.yaml`)
- **metadata-spec.md** rewritten: Now organized by agentskills.io standard fields (required/optional) + UR-SKILL custom extensions
- **output-template.md**: All 3 complexity-level frontmatter templates updated to new format
- **identity-template.md**: Frontmatter examples and field reference table updated
- **examples/examples.md**: Example SKILL frontmatter updated to new format
- **design-guides**: Examples and code snippets in `examples-design-guide.md` and `identity-design-guide.md` updated
- **Validator module structure**: `type` and `whenToUse` removed from `required_fields` in config; validator now reads from both top-level and `metadata`
- **README badges**: Fixed branch name `master` → `main`. Test count updated `43` → `48`.

### Fixed

- `validator_format.py`: `type` field validation now checks both `fm["type"]` and `fm.get("metadata", {}).get("type")` for backward compatibility
- `validator_runtime.py`: `_discover_ur_skill_files` path traversal fix — no longer goes one level too far up from SKILL.md
- `common.py`: `to_text()` report no longer treats `info`-level findings as validation failure
- YAML date serialization: `_normalize_for_schema()` converts `datetime.date` objects to strings before JSON Schema validation
- Exempt skill lists in config updated to include `ur-skill-cn` and `ur-skill-en`
- `config.en-us.yaml`: Placeholder regex fixed to match both `cognitive operation` and `Cognitive Op` (case-insensitive + abbreviation support). Previously flagged `[Cognitive Op]` as a false-positive placeholder residue.

### Infrastructure

- Tests increased from 43 to 48 (5 new JSON Schema tests added)
- `validate.yml` CI updated: Python 3.12, `pytest==8.3.5`, locked Actions to commit SHA
- All changes cross-verified: 48 pytest, CN validate, EN validate, bilingual sync (CN=44 files, EN=44 files, 100% aligned)

---

## [1.0.0] - 2026-07-09

### Added

#### Core Methodology
- **6-Domain Capability Matrix**: 1 Core Domain (SKILL Design Engineering) + 6 Radiating Domains (Domain Knowledge Modeling, Identity & Behavior Architecture, Boundary & Safety Engineering, Workflow Orchestration, Quality Assurance Engineering, Iterative Improvement), each with 4 depth layers
- **7-Step Verified Workflow**: Structured pipeline from pre-analysis through quality verification
- **3 Generation Routes**: Full-auto, interactive, and manual generation paths
- **"Eat Your Own Dog Food"**: UR-SKILL itself is generated using its own methodology

#### Pre-Analysis Agent (agent/SKILL.md)
- Mandatory pre-analysis sub-SKILL that runs before main SKILL generation
- Three-Tier Source Anchoring: L1 MUST web-search → L2 knowledge base retrieval → L3 LLM fallback with annotation
- Explicit role switch after sub-SKILL invocation to prevent context pollution

#### Model Format Adaptation
- Multi-model format adaptation design guide (CN + EN)
- Claude (XML tags), ChatGPT (Markdown + ###), Gemini (PTCF framework) formats
- Subagent support matrix covering 10 platforms (Claude Code, Cursor, Windsurf, GitHub Copilot, Codex CLI, Trae IDE, Tongyi Lingma, Baidu Comate, iFlytek iFlyCode, DeepSeek Coder)
- Default format: Standard Markdown

#### Templates (14 templates, CN + EN)
- Identity template, workflow template, boundary template, anti-pattern template, metadata spec, and more

#### Design Guides (15+ guides, CN + EN)
- Examples design guide, model format adaptation design guide, and domain-specific guides
- Anti-patterns library with cross-references to design guides

#### References (CN + EN)
- **Glossary**: 80 terms (G01-G80) across architecture, workflow, quality, metadata, and delivery domains
- **Anti-Patterns Library**: AP01-AP11 with remediation guidance
- **Troubleshooting Guide**: T01-T17 covering common issues

#### Scripts
- `validate_skill.py`: Static quality checker for generated SKILL packages
- YAML metadata validation, capability matrix completeness check, boundary rule coverage

#### Example SKILL
- `tech-doc-optimizer`: A production-grade SKILL manufactured by UR-SKILL for technical documentation optimization (included in `Examples/`)

#### Project Infrastructure
- Bilingual README.md (CN + EN)
- Apache 2.0 License
- `.gitignore` for Python, IDE, and OS files
- `CHANGELOG.md` (this file)
- `CONTRIBUTING.md`
- `install.py` supporting 39 agent platforms

### Changed
- N/A (initial release)

### Deprecated
- N/A (initial release)

### Removed
- N/A (initial release)

### Fixed
- N/A (initial release)

### Security
- Professional boundary rules (03): Sensitive licensed profession detection
- Data isolation and context safety mechanisms
- Cross-model format safety (avoiding format-specific syntax leaks)
