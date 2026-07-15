"""测试 validator_runtime.py。

覆盖 _check_ref_exists、_validate_references、_validate_tool_binding、
_validate_output_spec、_validate_file_dependency、_validate_ur_skill_leaks、
_validate_tool_reference_table 和入口函数 validate。
"""

from __future__ import annotations

import os
import shutil
import tempfile
from pathlib import Path

import pytest

from common import SkillContext
import validator_runtime


# =========================================================================
# _check_ref_exists
# =========================================================================


class TestCheckRefExists:
    def test_file_exists(self, tmp_path: Path) -> None:
        d = tmp_path / "subdir"
        d.mkdir()
        f = d / "test.py"
        f.write_text("")
        assert validator_runtime._check_ref_exists("subdir/test.py", tmp_path) is True

    def test_file_not_exists(self, tmp_path: Path) -> None:
        assert validator_runtime._check_ref_exists("nonexistent.py", tmp_path) is False

    def test_path_traversal_returns_false(self, tmp_path: Path) -> None:
        """路径穿越（../../outside.txt）应被拒绝。"""
        assert validator_runtime._check_ref_exists("../outside.txt", tmp_path) is False


# =========================================================================
# _validate_references
# =========================================================================


class TestValidateReferences:
    def test_reference_missing(self, zh_config: dict, tmp_path: Path) -> None:
        text = """---
name: test-skill
description: A test skill for unit testing purposes
metadata:
  updated: "2025-01-15"
---

See References/guide.md for more details.
"""
        ctx = SkillContext(text=text, path=tmp_path / "SKILL.md", config=zh_config)
        findings = validator_runtime._validate_references(ctx, zh_config)
        assert any(f.rule == "missing-reference" for f in findings)

    def test_reference_exists(self, zh_config: dict, tmp_path: Path) -> None:
        (tmp_path / "References").mkdir()
        (tmp_path / "References" / "guide.md").write_text("# Guide")
        text = """---
name: test-skill
description: A test skill for unit testing purposes
metadata:
  updated: "2025-01-15"
---

See References/guide.md for more details.
"""
        ctx = SkillContext(text=text, path=tmp_path / "SKILL.md", config=zh_config)
        findings = validator_runtime._validate_references(ctx, zh_config)
        assert not any(f.rule == "missing-reference" for f in findings)

    def test_script_missing(self, zh_config: dict, tmp_path: Path) -> None:
        text = """---
name: test-skill
description: A test skill for unit testing purposes
metadata:
  updated: "2025-01-15"
---

Run Scripts/deploy.sh to deploy.
"""
        ctx = SkillContext(text=text, path=tmp_path / "SKILL.md", config=zh_config)
        findings = validator_runtime._validate_references(ctx, zh_config)
        assert any(f.rule == "missing-script" for f in findings)

    def test_script_exists(self, zh_config: dict, tmp_path: Path) -> None:
        (tmp_path / "Scripts").mkdir()
        (tmp_path / "Scripts" / "deploy.sh").write_text("echo deploy")
        text = """---
name: test-skill
description: A test skill for unit testing purposes
metadata:
  updated: "2025-01-15"
---

Run Scripts/deploy.sh to deploy.
"""
        ctx = SkillContext(text=text, path=tmp_path / "SKILL.md", config=zh_config)
        findings = validator_runtime._validate_references(ctx, zh_config)
        assert not any(f.rule == "missing-script" for f in findings)

    def test_script_no_ext_skipped(self, zh_config: dict, tmp_path: Path) -> None:
        """Scripts 引用没有扩展名且不包含路径分隔符时跳过校验。"""
        text = """---
name: test-skill
description: A test skill for unit testing purposes
metadata:
  updated: "2025-01-15"
---

Run Scripts/some_command.
"""
        ctx = SkillContext(text=text, path=tmp_path / "SKILL.md", config=zh_config)
        findings = validator_runtime._validate_references(ctx, zh_config)
        assert not any(f.rule == "missing-script" for f in findings)

    def test_script_glob_skipped(self, zh_config: dict, tmp_path: Path) -> None:
        """Scripts 引用包含通配符时跳过校验（覆盖 line 61 continue 分支）。"""
        text = """---
name: test-skill
description: A test skill for unit testing purposes
metadata:
  updated: "2025-01-15"
---

Run Scripts/validate_*.py for validation.
"""
        ctx = SkillContext(text=text, path=tmp_path / "SKILL.md", config=zh_config)
        findings = validator_runtime._validate_references(ctx, zh_config)
        assert not any(f.rule == "missing-script" for f in findings)

    def test_asset_missing(self, zh_config: dict, tmp_path: Path) -> None:
        text = """---
name: test-skill
description: A test skill for unit testing purposes
metadata:
  updated: "2025-01-15"
---

See assets/logo.png for the logo.
"""
        ctx = SkillContext(text=text, path=tmp_path / "SKILL.md", config=zh_config)
        findings = validator_runtime._validate_references(ctx, zh_config)
        assert any(f.rule == "missing-asset" for f in findings)

    def test_asset_exists(self, zh_config: dict, tmp_path: Path) -> None:
        (tmp_path / "assets").mkdir()
        (tmp_path / "assets" / "logo.png").write_text("fake-png")
        text = """---
name: test-skill
description: A test skill for unit testing purposes
metadata:
  updated: "2025-01-15"
---

See assets/logo.png for the logo.
"""
        ctx = SkillContext(text=text, path=tmp_path / "SKILL.md", config=zh_config)
        findings = validator_runtime._validate_references(ctx, zh_config)
        assert not any(f.rule == "missing-asset" for f in findings)

    def test_design_guide_missing(self, zh_config: dict, tmp_path: Path) -> None:
        text = """---
name: test-skill
description: A test skill for unit testing purposes
metadata:
  updated: "2025-01-15"
---

See Design-Guides/architecture.md for details.
"""
        ctx = SkillContext(text=text, path=tmp_path / "SKILL.md", config=zh_config)
        findings = validator_runtime._validate_references(ctx, zh_config)
        assert any(f.rule == "missing-design-guide" for f in findings)

    def test_template_missing(self, zh_config: dict, tmp_path: Path) -> None:
        text = """---
name: test-skill
description: A test skill for unit testing purposes
metadata:
  updated: "2025-01-15"
---

Use Templates/report.md as the base.
"""
        ctx = SkillContext(text=text, path=tmp_path / "SKILL.md", config=zh_config)
        findings = validator_runtime._validate_references(ctx, zh_config)
        assert any(f.rule == "missing-template" for f in findings)

    def test_no_references_returns_empty(self, zh_config: dict, tmp_path: Path) -> None:
        text = """---
name: test-skill
description: A test skill for unit testing purposes
metadata:
  updated: "2025-01-15"
---

This is a simple body with no references.
"""
        ctx = SkillContext(text=text, path=tmp_path / "SKILL.md", config=zh_config)
        findings = validator_runtime._validate_references(ctx, zh_config)
        assert len(findings) == 0


# =========================================================================
# _validate_tool_binding
# =========================================================================


class TestValidateToolBinding:
    def test_exempt_skill_returns_empty(self, zh_config: dict, tmp_path: Path) -> None:
        text = """---
name: ur-skill
description: A test skill for unit testing purposes
metadata:
  updated: "2025-01-15"
---

Some body content with workflow actions.
"""
        ctx = SkillContext(text=text, path=tmp_path / "SKILL.md", config=zh_config)
        findings = validator_runtime._validate_tool_binding(ctx, zh_config)
        assert len(findings) == 0

    def test_no_workflow_returns_empty(self, zh_config: dict, tmp_path: Path) -> None:
        text = """---
name: test-skill
description: A test skill for unit testing purposes
metadata:
  updated: "2025-01-15"
---

## Instructions

1. [Read] Read input file
2. Execute analysis
"""
        ctx = SkillContext(text=text, path=tmp_path / "SKILL.md", config=zh_config)
        findings = validator_runtime._validate_tool_binding(ctx, zh_config)
        assert len(findings) == 0

    def test_workflow_all_lines_bound(self, zh_config: dict, tmp_path: Path) -> None:
        text = """---
name: test-skill
description: A test skill for unit testing purposes
metadata:
  updated: "2025-01-15"
---

## Workflow

1. [Read] Read input file
2. [Write] Write output file
3. [RunCommand] Execute command
"""
        ctx = SkillContext(text=text, path=tmp_path / "SKILL.md", config=zh_config)
        findings = validator_runtime._validate_tool_binding(ctx, zh_config)
        assert len(findings) == 0

    def test_workflow_unbound_lines(self, zh_config: dict, tmp_path: Path) -> None:
        text = """---
name: test-skill
description: A test skill for unit testing purposes
metadata:
  updated: "2025-01-15"
---

## Workflow

1. [Read] Read input file
2. 执行数据分析
3. [Write] Write output file
"""
        ctx = SkillContext(text=text, path=tmp_path / "SKILL.md", config=zh_config)
        findings = validator_runtime._validate_tool_binding(ctx, zh_config)
        assert any(f.rule == "tool-binding-missing" for f in findings)

    def test_cognitive_operation_skipped(self, zh_config: dict, tmp_path: Path) -> None:
        """认知操作行没有其他工具绑定时应被跳过。"""
        text = """---
name: test-skill
description: A test skill for unit testing purposes
metadata:
  updated: "2025-01-15"
---

## Workflow

1. [认知操作] 分析输入
2. [Read] Read input file
"""
        ctx = SkillContext(text=text, path=tmp_path / "SKILL.md", config=zh_config)
        findings = validator_runtime._validate_tool_binding(ctx, zh_config)
        assert len(findings) == 0

    def test_cognitive_operation_with_unbound(self, zh_config: dict, tmp_path: Path) -> None:
        """认知操作行之外的行未绑定时仍应产生 finding。"""
        text = """---
name: test-skill
description: A test skill for unit testing purposes
metadata:
  updated: "2025-01-15"
---

## Workflow

1. [认知操作] 分析输入
2. 执行数据分析
3. [Read] Read input file
"""
        ctx = SkillContext(text=text, path=tmp_path / "SKILL.md", config=zh_config)
        findings = validator_runtime._validate_tool_binding(ctx, zh_config)
        assert any(f.rule == "tool-binding-missing" for f in findings)

    def test_exempt_action_prefix(self, zh_config: dict, tmp_path: Path) -> None:
        """exempt_action_prefixes 开头的行应被跳过。"""
        text = """---
name: test-skill
description: A test skill for unit testing purposes
metadata:
  updated: "2025-01-15"
---

## Workflow

1. [Read] Read input file
2. 读取配置文件内容
3. [Write] Write output file
"""
        ctx = SkillContext(text=text, path=tmp_path / "SKILL.md", config=zh_config)
        findings = validator_runtime._validate_tool_binding(ctx, zh_config)
        assert len(findings) == 0

    def test_explanatory_line_skipped(self, zh_config: dict, tmp_path: Path) -> None:
        """为什么/note/说明等解释性行应被跳过。"""
        text = """---
name: test-skill
description: A test skill for unit testing purposes
metadata:
  updated: "2025-01-15"
---

## Workflow

1. [Read] Read input file
2. 为什么需要这样做：因为要保证一致性
3. [Write] Write output file
"""
        ctx = SkillContext(text=text, path=tmp_path / "SKILL.md", config=zh_config)
        findings = validator_runtime._validate_tool_binding(ctx, zh_config)
        assert len(findings) == 0

    def test_no_action_verbs_unbound_not_detected(self, zh_config: dict, tmp_path: Path) -> None:
        """unbound 行不包含 action_verbs 时不产生 finding。"""
        text = """---
name: test-skill
description: A test skill for unit testing purposes
metadata:
  updated: "2025-01-15"
---

## Workflow

1. [Read] Read input file
2. 得到结果
3. [Write] Write output file
"""
        ctx = SkillContext(text=text, path=tmp_path / "SKILL.md", config=zh_config)
        findings = validator_runtime._validate_tool_binding(ctx, zh_config)
        assert len(findings) == 0

    def test_only_unbound_no_tool_returns_empty(self, zh_config: dict, tmp_path: Path) -> None:
        """没有任何工具绑定时不应产生 finding。"""
        text = """---
name: test-skill
description: A test skill for unit testing purposes
metadata:
  updated: "2025-01-15"
---

## Workflow

1. 执行数据分析
2. 读取配置文件
"""
        ctx = SkillContext(text=text, path=tmp_path / "SKILL.md", config=zh_config)
        findings = validator_runtime._validate_tool_binding(ctx, zh_config)
        assert len(findings) == 0


# =========================================================================
# _validate_output_spec
# =========================================================================


class TestValidateOutputSpec:
    def test_not_crt_skill_returns_empty(self, zh_config: dict, tmp_path: Path) -> None:
        text = """---
name: my-helper-skill
description: A simple helper skill
metadata:
  updated: "2025-01-15"
---

Some body content.
"""
        ctx = SkillContext(text=text, path=tmp_path / "SKILL.md", config=zh_config)
        findings = validator_runtime._validate_output_spec(ctx, zh_config)
        assert len(findings) == 0

    def test_crt_skill_all_specs_present(self, zh_config: dict, tmp_path: Path) -> None:
        text = """---
name: code-review-skill
description: A review skill for testing purposes
metadata:
  updated: "2025-01-15"
---

## Workflow

1. Review the code

```mermaid
flowchart LR
    A-->B
```

Critical issues found.

AskUserQuestion to confirm fixes.

判决策略: 阻断合入
"""
        ctx = SkillContext(text=text, path=tmp_path / "SKILL.md", config=zh_config)
        findings = validator_runtime._validate_output_spec(ctx, zh_config)
        assert len(findings) == 0

    def test_crt_skill_missing_mermaid(self, zh_config: dict, tmp_path: Path) -> None:
        text = """---
name: code-review-skill
description: A review skill for testing purposes
metadata:
  updated: "2025-01-15"
---

## Workflow

1. Review the code

Critical issues found.

AskUserQuestion to confirm fixes.

判决策略: 阻断合入
"""
        ctx = SkillContext(text=text, path=tmp_path / "SKILL.md", config=zh_config)
        findings = validator_runtime._validate_output_spec(ctx, zh_config)
        assert any(f.rule == "output-spec-missing" for f in findings)

    def test_crt_skill_missing_severity(self, zh_config: dict, tmp_path: Path) -> None:
        text = """---
name: code-review-skill
description: A review skill for testing purposes
metadata:
  updated: "2025-01-15"
---

## Workflow

1. Review the code

```mermaid
flowchart LR
    A-->B
```

AskUserQuestion to confirm fixes.

判决策略: 阻断合入
"""
        ctx = SkillContext(text=text, path=tmp_path / "SKILL.md", config=zh_config)
        findings = validator_runtime._validate_output_spec(ctx, zh_config)
        assert any(f.rule == "output-spec-missing" for f in findings)

    def test_crt_skill_missing_decision(self, zh_config: dict, tmp_path: Path) -> None:
        text = """---
name: code-review-skill
description: A review skill for testing purposes
metadata:
  updated: "2025-01-15"
---

## Workflow

1. Review the code

```mermaid
flowchart LR
    A-->B
```

Critical issues found.

AskUserQuestion to confirm fixes.
"""
        ctx = SkillContext(text=text, path=tmp_path / "SKILL.md", config=zh_config)
        findings = validator_runtime._validate_output_spec(ctx, zh_config)
        assert any(f.rule == "output-spec-missing" for f in findings)


# =========================================================================
# _validate_file_dependency
# =========================================================================


class TestValidateFileDependency:
    def test_no_workflow_returns_empty(self, zh_config: dict, tmp_path: Path) -> None:
        text = """---
name: test-skill
description: A test skill for unit testing purposes
metadata:
  updated: "2025-01-15"
---

## Instructions

1. Do something
"""
        ctx = SkillContext(text=text, path=tmp_path / "SKILL.md", config=zh_config)
        findings = validator_runtime._validate_file_dependency(ctx, zh_config)
        assert len(findings) == 0

    def test_workflow_with_decision_indicator(self, zh_config: dict, tmp_path: Path) -> None:
        text = """---
name: test-skill
description: A test skill for unit testing purposes
metadata:
  updated: "2025-01-15"
---

## 工作流

1. 检查文件依赖决策
2. Execute action
"""
        ctx = SkillContext(text=text, path=tmp_path / "SKILL.md", config=zh_config)
        findings = validator_runtime._validate_file_dependency(ctx, zh_config)
        assert len(findings) == 0

    def test_workflow_without_decision_indicator(self, zh_config: dict, tmp_path: Path) -> None:
        text = """---
name: test-skill
description: A test skill for unit testing purposes
metadata:
  updated: "2025-01-15"
---

## 工作流

1. 执行数据分析
2. 写入结果
"""
        ctx = SkillContext(text=text, path=tmp_path / "SKILL.md", config=zh_config)
        findings = validator_runtime._validate_file_dependency(ctx, zh_config)
        assert any(f.rule == "file-dependency-missing" for f in findings)

    def test_workflow_with_design_rationale_ref(self, zh_config: dict, tmp_path: Path) -> None:
        """引用 design-rationale.md#9 也应视为决策指示器。"""
        text = """---
name: test-skill
description: A test skill for unit testing purposes
metadata:
  updated: "2025-01-15"
---

## 工作流

1. 参考 design-rationale.md#9 进行决策
2. Execute action
"""
        ctx = SkillContext(text=text, path=tmp_path / "SKILL.md", config=zh_config)
        findings = validator_runtime._validate_file_dependency(ctx, zh_config)
        assert len(findings) == 0


# =========================================================================
# _validate_ur_skill_leaks
# =========================================================================


class TestValidateUrSkillLeaks:
    def _make_context(self, body: str, path: Path, config: dict) -> SkillContext:
        text = f"""---
name: test-leak-skill
description: A test skill for leak detection
metadata:
  updated: "2025-01-15"
---

{body}
"""
        return SkillContext(text=text, path=path, config=config)

    def test_exempt_skill_returns_empty(self, zh_config: dict, tmp_path: Path) -> None:
        text = """---
name: ur-skill-cn
description: A test skill for leak detection
metadata:
  updated: "2025-01-15"
---

Scripts/common.py
"""
        ctx = SkillContext(text=text, path=tmp_path / "SKILL.md", config=zh_config)
        validator_runtime._UR_SKILL_FILES = None
        findings = validator_runtime._validate_ur_skill_leaks(ctx, zh_config)
        assert len(findings) == 0

    def test_skill_outside_project_returns_empty(self, zh_config: dict, tmp_path: Path) -> None:
        """skill_dir 在 project_root 之外时 _discover_ur_skill_files 返回空 set。"""
        validator_runtime._UR_SKILL_FILES = None
        ctx = self._make_context("Any content here.", tmp_path / "SKILL.md", zh_config)
        findings = validator_runtime._validate_ur_skill_leaks(ctx, zh_config)
        assert len(findings) == 0

    def test_leak_detected(self, zh_config: dict, scripts_dir: Path) -> None:
        """设置 _UR_SKILL_FILES 已知集合，验证泄漏检测逻辑。"""
        validator_runtime._UR_SKILL_FILES = {"Scripts/common.py", "Scripts/validator_format.py"}
        ctx = self._make_context(
            "This file references Scripts/common.py which should be a leak.",
            scripts_dir.parent / "SKILL.md",
            zh_config,
        )
        findings = validator_runtime._validate_ur_skill_leaks(ctx, zh_config)
        assert any(f.rule == "ur-skill-leak" for f in findings)

    def test_leak_with_dot_slash(self, zh_config: dict, scripts_dir: Path) -> None:
        """./Scripts/some.py 也应被检测为泄漏。"""
        validator_runtime._UR_SKILL_FILES = {"Scripts/some.py"}
        ctx = self._make_context(
            "Reference ./Scripts/some.py here.",
            scripts_dir.parent / "SKILL.md",
            zh_config,
        )
        findings = validator_runtime._validate_ur_skill_leaks(ctx, zh_config)
        assert any(f.rule == "ur-skill-leak" for f in findings)

    def test_no_leak(self, zh_config: dict, scripts_dir: Path) -> None:
        """body 中不包含任何泄漏文件引用。"""
        validator_runtime._UR_SKILL_FILES = {"Scripts/common.py", "Scripts/validator_format.py"}
        ctx = self._make_context(
            "This file references no internal files at all.",
            scripts_dir.parent / "SKILL.md",
            zh_config,
        )
        findings = validator_runtime._validate_ur_skill_leaks(ctx, zh_config)
        assert len(findings) == 0

    def test_leak_in_code_block_filtered(self, zh_config: dict, scripts_dir: Path) -> None:
        """代码块中的泄漏引用应被 strip_code_blocks 过滤。"""
        validator_runtime._UR_SKILL_FILES = {"Scripts/common.py"}
        ctx = self._make_context(
            "Here is an example:\n```python\nimport Scripts/common.py\n```",
            scripts_dir.parent / "SKILL.md",
            zh_config,
        )
        findings = validator_runtime._validate_ur_skill_leaks(ctx, zh_config)
        assert len(findings) == 0

    def test_discover_files_inside_project(self, zh_config: dict, scripts_dir: Path) -> None:
        """测试 _discover_ur_skill_files 在 project_root 内发现文件。

        在 UR-SKILL-CN 下创建临时目录结构，触发文件发现逻辑。
        """
        test_dir_path = tempfile.mkdtemp(dir=str(scripts_dir.parent))
        try:
            # 创建匹配 forbidden_prefixes 的文件结构
            scripts_sub = os.path.join(test_dir_path, "Scripts")
            os.makedirs(scripts_sub)
            Path(scripts_sub, "test_script.py").write_text("# test")
            design_sub = os.path.join(test_dir_path, "design-guides")
            os.makedirs(design_sub)
            Path(design_sub, "guide.md").write_text("# guide")

            text = """---
name: test-discovery-skill
description: A test skill for discovery testing
metadata:
  updated: "2025-01-15"
---

Clean body.
"""
            ctx = SkillContext(
                text=text,
                path=Path(test_dir_path) / "SKILL.md",
                config=zh_config,
            )
            validator_runtime._UR_SKILL_FILES = None
            findings = validator_runtime._validate_ur_skill_leaks(ctx, zh_config)
            assert len(findings) == 0  # 干净的 body，无泄漏

            # 验证缓存已填充
            cached = validator_runtime._UR_SKILL_FILES
            assert "Scripts/test_script.py" in cached
            assert "design-guides/guide.md" in cached
        finally:
            shutil.rmtree(test_dir_path, ignore_errors=True)


# =========================================================================
# _validate_tool_reference_table
# =========================================================================


class TestValidateToolReferenceTable:
    def test_exempt_skill_returns_empty(self, zh_config: dict, tmp_path: Path) -> None:
        text = """---
name: ur-skill
description: A test skill
metadata:
  updated: "2025-01-15"
---

[Read] Read file
"""
        ctx = SkillContext(text=text, path=tmp_path / "SKILL.md", config=zh_config)
        findings = validator_runtime._validate_tool_reference_table(ctx, zh_config)
        assert len(findings) == 0

    def test_no_tool_binding_returns_empty(self, zh_config: dict, tmp_path: Path) -> None:
        text = """---
name: test-skill
description: A test skill
metadata:
  updated: "2025-01-15"
---

No tools used here.
"""
        ctx = SkillContext(text=text, path=tmp_path / "SKILL.md", config=zh_config)
        findings = validator_runtime._validate_tool_reference_table(ctx, zh_config)
        assert len(findings) == 0

    def test_has_tool_binding_and_table(self, zh_config: dict, tmp_path: Path) -> None:
        text = """---
name: test-skill
description: A test skill
metadata:
  updated: "2025-01-15"
---

[Read] Read input file

## 工具引用表

| 工具 | 用途 |
|------|------|
| Read | 读取文件 |
"""
        ctx = SkillContext(text=text, path=tmp_path / "SKILL.md", config=zh_config)
        findings = validator_runtime._validate_tool_reference_table(ctx, zh_config)
        assert len(findings) == 0

    def test_has_tool_binding_no_table(self, zh_config: dict, tmp_path: Path) -> None:
        text = """---
name: test-skill
description: A test skill
metadata:
  updated: "2025-01-15"
---

[Read] Read input file
[Write] Write output file
"""
        ctx = SkillContext(text=text, path=tmp_path / "SKILL.md", config=zh_config)
        findings = validator_runtime._validate_tool_reference_table(ctx, zh_config)
        assert any(f.rule == "tool-reference-table-missing" for f in findings)

    def test_tool_reference_map_pattern(self, zh_config: dict, tmp_path: Path) -> None:
        """Tool Reference Map 模式也应被识别。"""
        text = """---
name: test-skill
description: A test skill
metadata:
  updated: "2025-01-15"
---

[Read] Read input file

## Tool Reference Map

| Tool | Purpose |
|------|---------|
| Read | Read files |
"""
        ctx = SkillContext(text=text, path=tmp_path / "SKILL.md", config=zh_config)
        findings = validator_runtime._validate_tool_reference_table(ctx, zh_config)
        assert len(findings) == 0


# =========================================================================
# validate (入口函数)
# =========================================================================


class TestValidate:
    def test_validate_calls_all_validators(self, zh_config: dict, tmp_path: Path) -> None:
        """验证入口函数串联所有校验器并返回 findings。"""
        text = """---
name: test-skill
description: A test skill for unit testing purposes
metadata:
  updated: "2025-01-15"
---

## 工作流

1. [Read] Read input file
2. 执行数据分析
"""
        ctx = SkillContext(text=text, path=tmp_path / "SKILL.md", config=zh_config)
        validator_runtime._UR_SKILL_FILES = set()
        findings = validator_runtime.validate(ctx, zh_config)
        assert isinstance(findings, list)
        # 至少应该包含 tool-binding-missing 和 file-dependency-missing
        rules = {f.rule for f in findings}
        assert "file-dependency-missing" in rules

    def test_validate_clean_skill(self, zh_config: dict, scripts_dir: Path) -> None:
        """干净的 SKILL 应产生最少的 findings。"""
        text = """---
name: test-skill
description: A test skill for unit testing purposes only
metadata:
  updated: "2025-01-15"
---

## 工作流

1. 文件依赖决策：根据 context 决定是否创建文件
2. [Read] Read input file
3. [Write] Write output file
"""
        ctx = SkillContext(text=text, path=scripts_dir / "SKILL.md", config=zh_config)
        validator_runtime._UR_SKILL_FILES = set()
        findings = validator_runtime.validate(ctx, zh_config)
        # 不应有 file-dependency-missing（包含"文件依赖决策"）
        assert not any(f.rule == "file-dependency-missing" for f in findings)
