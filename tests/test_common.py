"""测试 common.py 的基础设施。"""

import json
from pathlib import Path

import pytest

from common import Finding, Report, SkillContext, strip_code_blocks


class TestFinding:
    def test_create(self) -> None:
        f = Finding("test-rule", "test message")
        assert f.rule == "test-rule"
        assert f.message == "test message"
        assert f.severity == "error"
        assert f.line is None

    def test_with_line(self) -> None:
        f = Finding("rule", "msg", "warning", 42)
        assert f.line == 42
        assert f.severity == "warning"

    def test_to_dict(self) -> None:
        f = Finding("r1", "m1", "info", 5)
        d = f.to_dict()
        assert d == {"rule": "r1", "message": "m1", "severity": "info", "line": 5}


class TestSkillContext:
    def test_parse_simple_skill(self) -> None:
        text = """---
name: test-skill
description: A test SKILL.
type: prompt
whenToUse: For testing
metadata:
  updated: "2025-01-15"
---

# Body content here
"""
        ctx = SkillContext(text=text, path=Path("/fake/SKILL.md"), config={})
        assert ctx.frontmatter["name"] == "test-skill"
        assert ctx.frontmatter["description"] == "A test SKILL."
        assert "Body content here" in ctx.body

    def test_missing_frontmatter_delimiter(self) -> None:
        ctx = SkillContext(text="# No frontmatter", path=Path("/fake/SKILL.md"), config={})
        assert len(ctx.fm_parse_errors) >= 1

    def test_missing_second_delimiter(self) -> None:
        ctx = SkillContext(text="---\nname: test\n", path=Path("/fake/SKILL.md"), config={})
        assert len(ctx.fm_parse_errors) >= 1

    def test_invalid_yaml_frontmatter(self) -> None:
        text = """---
name: test
invalid: [unclosed
---
body
"""
        ctx = SkillContext(text=text, path=Path("/fake/SKILL.md"), config={})
        assert len(ctx.fm_parse_errors) >= 1

    def test_run_method(self) -> None:
        """测试 ctx.run(validator) 调用路径。"""
        text = """---
name: test-skill
description: A simple test SKILL for verifying the run method invocation path works correctly.
type: prompt
whenToUse: testing
metadata:
  updated: "2025-01-15"
---

body
"""
        ctx = SkillContext(text=text, path=Path("/fake/SKILL.md"), config={})

        def dummy_validator(c: SkillContext, cfg: dict) -> list[Finding]:
            return [Finding("dummy", "test")]

        findings = ctx.run(dummy_validator)
        assert len(findings) == 1
        assert findings[0].rule == "dummy"

    def test_skill_dir_property(self) -> None:
        ctx = SkillContext(text="", path=Path("/some/dir/SKILL.md"), config={})
        assert ctx.skill_dir == Path("/some/dir")


class TestReport:
    def test_json_format(self) -> None:
        findings = [Finding("r1", "msg1", "error"), Finding("r2", "msg2", "warning")]
        report = Report(findings, {})
        json_out = report.to_json()
        data = json.loads(json_out)
        assert len(data) == 2
        assert data[0]["rule"] == "r1"

    def test_text_format(self) -> None:
        findings = [Finding("r1", "msg1", "error")]
        report = Report(findings, {"messages": {"validation_failed": "失败: {count}"}})
        output = report.to_text()
        assert "失败" in output
        assert "msg1" in output

    def test_no_findings(self) -> None:
        report = Report([], {"messages": {"validation_passed": "OK"}})
        assert report.to_text() == "OK"
        assert not report.has_error

    def test_has_error_only_warning(self) -> None:
        report = Report([Finding("r1", "msg", "warning")], {})
        assert not report.has_error


class TestStripCodeBlocks:
    def test_single_block(self) -> None:
        text = "before\n```python\nprint('hello')\n```\nafter"
        result = strip_code_blocks(text)
        assert "before" in result
        assert "after" in result
        assert "print" not in result

    def test_multiple_blocks(self) -> None:
        text = "a\n```\ncode1\n```\nb\n```\ncode2\n```\nc"
        result = strip_code_blocks(text)
        assert "code1" not in result
        assert "code2" not in result
        assert "a" in result
        assert "b" in result
        assert "c" in result

    def test_no_blocks(self) -> None:
        text = "plain text without any code blocks"
        result = strip_code_blocks(text)
        assert result == text

    def test_unclosed_block(self) -> None:
        text = "before\n```python\nprint('hello')\n"
        result = strip_code_blocks(text)
        assert "before" in result

    def test_empty_input(self) -> None:
        result = strip_code_blocks("")
        assert result == ""
