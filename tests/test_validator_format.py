"""测试 validator_format.py。"""

from pathlib import Path

import pytest

from common import SkillContext
import validator_format


class TestValidateFrontmatter:
    def test_all_required_fields(self, zh_config) -> None:
        text = """---
name: my-skill
description: 这是一个用于测试的 SKILL 描述，长度需要满足最低要求，所以这里需要写够五十个字符以上来通过校验。
metadata:
  updated: "2025-01-15"
  type: prompt
  whenToUse: 用于测试
---

body
"""
        ctx = SkillContext(text=text, path=Path("/fake/SKILL.md"), config=zh_config)
        findings = validator_format._validate_frontmatter(ctx, zh_config)
        assert len(findings) == 0

    def test_missing_required_field(self, zh_config) -> None:
        text = """---
name: my-skill
type: prompt
---

body
"""
        ctx = SkillContext(text=text, path=Path("/fake/SKILL.md"), config=zh_config)
        findings = validator_format._validate_frontmatter(ctx, zh_config)
        missing_fields = {f.rule for f in findings}
        assert "missing-frontmatter-field" in missing_fields

    def test_name_not_kebab(self, zh_config) -> None:
        text = """---
name: My_SKILL
description: 这是一个用于测试的 SKILL 描述，长度需要满足最低要求，所以这里需要写够五十个字符以上来通过校验。
type: prompt
whenToUse: 用于测试
metadata:
  updated: "2025-01-15"
---

body
"""
        ctx = SkillContext(text=text, path=Path("/fake/SKILL.md"), config=zh_config)
        findings = validator_format._validate_frontmatter(ctx, zh_config)
        assert any(f.rule == "name-not-kebab" for f in findings)

    def test_description_too_short(self, zh_config) -> None:
        text = """---
name: my-skill
description: short
type: prompt
whenToUse: 测试
metadata:
  updated: "2025-01-15"
---

body
"""
        ctx = SkillContext(text=text, path=Path("/fake/SKILL.md"), config=zh_config)
        findings = validator_format._validate_frontmatter(ctx, zh_config)
        assert any(f.rule == "description-length" for f in findings)

    def test_invalid_type_no_longer_validated(self, zh_config) -> None:
        """type 字段不再由 _validate_frontmatter 校验（新 schema 已移除）。"""
        text = """---
name: my-skill
description: 这是一个用于测试的 SKILL 描述，长度需要满足最低要求，所以这里需要写够五十个字符以上来通过校验。
type: invalid-type
whenToUse: 用于测试
metadata:
  updated: "2025-01-15"
---

body
"""
        ctx = SkillContext(text=text, path=Path("/fake/SKILL.md"), config=zh_config)
        findings = validator_format._validate_frontmatter(ctx, zh_config)
        # type 校验已从 schema 中移除，不再产生 "invalid-type" 规则
        assert not any(f.rule == "invalid-type" for f in findings)

    def test_metadata_updated_missing(self, zh_config) -> None:
        text = """---
name: my-skill
description: 这是一个用于测试的 SKILL 描述，长度需要满足最低要求，所以这里需要写够五十个字符以上来通过校验。
type: prompt
whenToUse: 用于测试
metadata:
  other: value
---

body
"""
        ctx = SkillContext(text=text, path=Path("/fake/SKILL.md"), config=zh_config)
        findings = validator_format._validate_frontmatter(ctx, zh_config)
        assert any(f.rule == "metadata-updated-missing" for f in findings)

    def test_metadata_updated_bad_format(self, zh_config) -> None:
        text = """---
name: my-skill
description: 这是一个用于测试的 SKILL 描述，长度需要满足最低要求，所以这里需要写够五十个字符以上来通过校验。
type: prompt
whenToUse: 用于测试
metadata:
  updated: "2025/01/15"
---

body
"""
        ctx = SkillContext(text=text, path=Path("/fake/SKILL.md"), config=zh_config)
        findings = validator_format._validate_frontmatter(ctx, zh_config)
        assert any(f.rule == "metadata-updated-format" for f in findings)


class TestValidateBody:
    def test_body_too_long(self, zh_config) -> None:
        config = zh_config.copy()
        config["thresholds"] = {"max_body_lines": 3, "max_description_chars": 200, "min_description_chars": 50}
        lines = ["line" + str(i) for i in range(10)]
        text = """---
name: my-skill
description: 这是一个用于测试的 SKILL 描述，长度需要满足最低要求，所以这里需要写够五十个字符以上来通过校验。
type: prompt
whenToUse: 测试
metadata:
  updated: "2025-01-15"
---

""" + "\n".join(lines)
        ctx = SkillContext(text=text, path=Path("/fake/SKILL.md"), config=config)
        findings = validator_format._validate_body(ctx, config)
        assert any(f.rule == "body-too-long" for f in findings)

    def test_known_tool_not_placeholder(self, zh_config) -> None:
        """确保已知工具名如 [WebSearch] 不触发 placeholder 误报。"""
        inner_config = zh_config.copy()
        inner_config["rules"]["risk_boundaries"] = []  # 跳过 UR-SKILL 特殊检查
        text = """---
name: other-skill
description: 一个用于测试的 SKILL 描述，长度需要满足最低要求，所以这里需要写够五十个字符以上来通过校验。
type: prompt
whenToUse: 测试
metadata:
  updated: "2025-01-15"
---

[WebSearch] 搜索 → 返回结果
[Read] 读取文件
"""
        ctx = SkillContext(text=text, path=Path("/fake/SKILL.md"), config=inner_config)
        findings = validator_format._validate_body(ctx, inner_config)
        assert not any("WebSearch" in f.message for f in findings)
        assert not any("Read" in f.message for f in findings)

    def test_allowed_literal_date_not_placeholder(self, zh_config) -> None:
        """{date} 字面量不触发 placeholder 告警。"""
        inner_config = zh_config.copy()
        inner_config["rules"]["risk_boundaries"] = []
        text = """---
name: other-skill
description: 一个用于测试的 SKILL 描述，长度需要满足最低要求，所以这里需要写够五十个字符以上来通过校验。
type: prompt
whenToUse: 测试
metadata:
  updated: "2025-01-15"
---

更新时间: {date}
"""
        ctx = SkillContext(text=text, path=Path("/fake/SKILL.md"), config=inner_config)
        findings = validator_format._validate_body(ctx, inner_config)
        assert not any("placeholder" in f.rule for f in findings)


class TestValidateUnresolvedPlaceholders:
    def test_unfilled_placeholder(self, zh_config) -> None:
        inner_config = zh_config.copy()
        inner_config["rules"]["risk_boundaries"] = []
        text = """---
name: other-skill
description: 一个用于测试的 SKILL 描述，长度需要满足最低要求，所以这里需要写够五十个字符以上来通过校验。
type: prompt
whenToUse: 测试
metadata:
  updated: "2025-01-15"
---

{kebab-case-name}
"""
        ctx = SkillContext(text=text, path=Path("/fake/SKILL.md"), config=inner_config)
        findings = validator_format._validate_unresolved_placeholders(ctx, inner_config)
        assert any(f.rule == "unresolved-placeholder" for f in findings)


class TestDeprecatedTools:
    def test_detects_searchreplace(self, zh_config) -> None:
        text = """---
name: my-skill
description: 这是一个用于测试的 SKILL 描述，长度需要满足最低要求，所以这里需要写够五十个字符以上来通过校验。
type: prompt
whenToUse: 测试
metadata:
  updated: "2025-01-15"
---

使用 SearchReplace 来替换文本
"""
        ctx = SkillContext(text=text, path=Path("/fake/SKILL.md"), config=zh_config)
        findings = validator_format._validate_deprecated_tools(ctx, zh_config)
        assert any(f.rule == "deprecated-tool" for f in findings)

    def test_no_deprecated_tool(self, zh_config) -> None:
        text = """---
name: my-skill
description: 这是一个用于测试的 SKILL 描述，长度需要满足最低要求，所以这里需要写够五十个字符以上来通过校验。
type: prompt
whenToUse: 测试
metadata:
  updated: "2025-01-15"
---

使用 Edit 来替换文本
"""
        ctx = SkillContext(text=text, path=Path("/fake/SKILL.md"), config=zh_config)
        findings = validator_format._validate_deprecated_tools(ctx, zh_config)
        assert not any(f.rule == "deprecated-tool" for f in findings)


class TestJsonSchema:
    """JSON Schema 校验测试。"""

    def test_valid_frontmatter_passes_schema(self, zh_config, scripts_dir) -> None:
        """新格式 frontmatter 通过 JSON Schema 校验。"""
        text = """---
name: my-skill
description: 这是一个用于测试的 SKILL 描述，长度需要满足最低要求，所以这里需要写够五十个字符以上来通过校验。
metadata:
  updated: "2025-01-15"
  type: prompt
  whenToUse: 用于测试
---

body
"""
        ctx = SkillContext(text=text, path=scripts_dir / "SKILL.md", config=zh_config)
        findings = validator_format._validate_json_schema(ctx)
        assert any(f.rule == "schema-valid" for f in findings), f"Expected schema-valid, got {findings}"

    def test_old_format_fails_schema(self, zh_config, scripts_dir) -> None:
        """旧格式 frontmatter (type/whenToUse 在顶层) 被 JSON Schema 拒绝。"""
        text = """---
name: my-skill
description: 这是一个用于测试的 SKILL 描述，长度需要满足最低要求，所以这里需要写够五十个字符以上来通过校验。
type: prompt
whenToUse: 用于测试
metadata:
  updated: "2025-01-15"
---

body
"""
        ctx = SkillContext(text=text, path=scripts_dir / "SKILL.md", config=zh_config)
        findings = validator_format._validate_json_schema(ctx)
        violations = [f for f in findings if f.rule == "schema-violation"]
        assert len(violations) > 0, f"Expected schema violations for old format, got {findings}"

    def test_missing_metadata_type_passes_schema(self, zh_config, scripts_dir) -> None:
        """metadata.type 不再被 schema 要求（新 schema 简化后仅要求 metadata.updated）。"""
        text = """---
name: my-skill
description: 这是一个用于测试的 SKILL 描述，长度需要满足最低要求，所以这里需要写够五十个字符以上来通过校验。
metadata:
  updated: "2025-01-15"
  whenToUse: 用于测试
---

body
"""
        ctx = SkillContext(text=text, path=scripts_dir / "SKILL.md", config=zh_config)
        findings = validator_format._validate_json_schema(ctx)
        violations = [f for f in findings if f.rule == "schema-violation"]
        assert len(violations) == 0, f"Expected no schema violations for missing metadata.type, got {findings}"

    def test_our_cn_skill_passes(self, zh_config, scripts_dir) -> None:
        """UR-SKILL-CN 自身的 SKILL.md 通过 JSON Schema 校验。"""
        skill_path = scripts_dir.parent / "SKILL.md"
        if not skill_path.exists():
            pytest.skip("UR-SKILL-CN SKILL.md not found")
        text = skill_path.read_text(encoding="utf-8")
        ctx = SkillContext(text=text, path=skill_path, config=zh_config)
        findings = validator_format._validate_json_schema(ctx)
        assert any(f.rule == "schema-valid" for f in findings), f"Expected schema-valid, got {findings}"

    def test_our_en_skill_passes(self, en_config, en_scripts_dir) -> None:
        """UR-SKILL-EN 自身的 SKILL.md 通过 JSON Schema 校验。"""
        skill_path = en_scripts_dir.parent / "SKILL.md"
        if not skill_path.exists():
            pytest.skip("UR-SKILL-EN SKILL.md not found")
        text = skill_path.read_text(encoding="utf-8")
        ctx = SkillContext(text=text, path=skill_path, config=en_config)
        findings = validator_format._validate_json_schema(ctx)
        assert any(f.rule == "schema-valid" for f in findings), f"Expected schema-valid, got {findings}"
