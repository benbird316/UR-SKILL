# Changelog

All notable changes to UR-SKILL will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.1.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [2.0.0] - 2026-07-15

### Added

- **English version (UR-SKILL-EN)**: Full bilingual parity — all SKILL.md, design guides, templates, references, scripts, and agents synced and independently validated. Bilingual sync at 100% (44/44 files).
- **CI integration tests** (`ci_validate_examples.py`): End-to-end SKILL package validation in CI — smoke test, good/bad matrix, empty package, CN/EN cross-check. CI pipeline now 5 steps.
- **CI coverage gate**: `--cov-fail-under=60` enforced on all PRs. Coverage at 87%.
- **CI path expansion**: Push and PR triggers now cover `.github/workflows/**` and `**/templates/**`.
- **Dependabot** (`.github/dependabot.yml`): Weekly auto-updates for GitHub Actions pinned SHAs.
- **System prompt output mode**: SKILL.md now explicitly supports generating system prompts as a variant — same workflow, strip metadata at step 13, skip steps 6-7 (ref file generation + script generation).
- **README deployment guide**: Replaced `install.py` with clear manual deployment instructions covering directory copy and UI-based deployment for 5+ platforms.

### Changed

- **Actions pinned to SHA**: `checkout@v4` -> `11bd71901bbe5b1630ceea73d27597364c9af683` (v4.2.2), `setup-python@v5` -> `42375524e23c412d93fb67b49958b491fce71c38` (v5.4.0).
- **Agent files**: Removed YAML frontmatter from all 3 agents (CN+EN). Agents are not SKILL files — no metadata needed.
- **examples.md Example 4**: Replaced dead-linked translation SKILL reference with UR-SKILL's own complete directory structure (self-demonstration).
- **SKILL.md Core Principle (EN)**: Fixed triple redundancy — "executes its full 13 steps completely — no step skipping (each step must be reached and evaluated against its prerequisites)" -> "executes all 13 steps — no step skipping (each step must be reached and its prerequisites evaluated; sub-Agent invocation may be skipped by decision)".
- **SKILL.md identity statement**: Clarified default output is SKILL package, not system prompt.
- **SKILL.md Steps 4/5/10/11 (CN)**: Added missing blind-spot handling details, now matching EN.
- **SKILL.md gate rule**: "跳过步骤评估" -> "不进行反思★门控（校验→验证→循环判定）则交付无效" (corrected inaccurate phrasing).
- **bilingual_sync.py size_diff threshold**: `> 0` -> `> 50` bytes, filtering punctuation/encoding noise (~30-40 bytes) from genuine content differences (200+ bytes).
- **EN SKILL.md name**: Fixed `name: ur-skill-cn` -> `name: ur-skill-en` (copy-paste error).

### Fixed

- **RFC2119 detection (EN)**: 28 false negatives in `validator_content.py` — regex prefix group consumed `MUST`/`SHOULD` keywords, causing all 28 rules to be skipped. Fixed by removing `|MUST NOT|MUST|SHOULD NOT|SHOULD|MAY` from prefix capture group.
- **EN description first-person**: Chinese character `我` in `帮我写一个skill` triggered first-person detection with misleading English error message. Rewrote description without `我`.
- **EN description-length**: 300 chars (exceeded 250-char limit for English). Compressed to 188 chars.
- **jsonschema silent fallback**: `_HAS_JSONSCHEMA=False` silently returned `[]`. Now outputs `[WARNING]` to stderr.
- **EN config rules_heading_pattern**: Fixed `MUST NOT|MUST|SHOULD NOT|SHOULD|MAY` -> `MUST NOT|MUST|SHOULD NOT|SHOULD|MAY|SHALL|SHALL NOT` in CN config.

### Removed

- **install.py**: Removed from root. Cross-platform path detection (Windows `%APPDATA%` vs Unix `$HOME`, 39 platforms) was unreliable. Replaced with README deployment instructions.

### Quality

- **Tests**: 48 -> 135 (87 new: 26 validator_runtime + 26 bilingual_sync/validate_skill + 17 validator_format + 10 validator_content + 5 ci_validate_examples + 3 self_validate)
- **Coverage**: 87.34% overall (up from ~60%). validator_runtime.py: 53% -> 97%, bilingual_sync.py: 0% -> 93%, validate_skill.py: 0% -> 96%.
- **Bilingual sync**: 100.0% overlap (44/44 files each).
- **Known errors whitelist**: All `test_self_validate.py` exemptions documented with rationale comments.

---

## [1.1.0] - 2026-07-10

### Added

- agentskills.io frontmatter compliance: metadata block, JSON Schema validation
- `install.py` with `--lang` flag
- `bilingual_sync.py` synced to EN directory
- Sub-agent detection in workflow Step 1

### Changed

- README, CONTRIBUTING, CHANGELOG rewritten in English
- Config per language (CN: zh-cn only, EN: en-us only)
- Templates and design guides updated to new frontmatter format
- Validator adapted for backward-compatible field reading

### Fixed

- `validator_runtime.py` path traversal fix
- `common.py` report `info`-level findings no longer fail validation
- YAML date serialization for JSON Schema
- EN placeholder regex: case-insensitive + abbreviation support
- Exempt skill lists updated for both language versions

---

## [1.0.0] - 2026-07-09

### Added

- Initial release: 6-domain Capability Matrix, 7-step Verified Workflow, 3 Generation Routes
- Pre-Analysis Agent with Three-Tier Source Anchoring
- 15+ design guides, 14 templates, 80-term glossary, 11 anti-patterns
- Multi-model format adaptation (Claude, ChatGPT, Gemini)
- `validate_skill.py` static quality checker
- Bilingual README, Apache 2.0 License, CONTRIBUTING.md
