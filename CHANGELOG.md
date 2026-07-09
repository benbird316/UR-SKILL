# Changelog

All notable changes to UR-SKILL will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

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
- Bilingual README.md (CN + EN side-by-side)
- Apache 2.0 License
- `.gitignore` for Python, IDE, and OS files
- `CHANGELOG.md` (this file)

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
