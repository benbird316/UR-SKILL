"""Verify scripts can validate generated SKILLs — both zh-cn and en-us variants.

Tests that new rules (capability-workflow confusion, tool reference table)
work correctly against synthetic generated SKILL content in both languages.
"""

from __future__ import annotations

import tempfile
from pathlib import Path

import pytest

from common import SkillContext
from config_loader import load_config
import validator_content
import validator_runtime


def _make_good_skill_zh() -> str:
    """A well-formed generated SKILL in Chinese (should pass most checks)."""
    return """---
name: code-reviewer
description: >
  Reviews code for quality, security, and best practices. Covers multiple
  languages and frameworks with structured feedback and actionable suggestions.
metadata:
  updated: "2026-07-15"
---

## 1. 能力架构

### 1.1 能力矩阵

**核心领域**:代码审查

| 领域 | 基础层 | 进阶层 | 高阶层 | 拓展层 |
|:---|:---|:---|:---|:---|
| 核心:代码审查 | 语法/风格检查 | 逻辑缺陷分析 | 架构评审 | 自动化审查流水线 |

**辐射领域**:

| 领域 | 基础层 | 进阶层 | 高阶层 | 拓展层 |
|:---|:---|:---|:---|:---|
| 安全漏洞检测 | OWASP Top 10 检查 | CWE 模式匹配 | 威胁建模 | 零日漏洞预判 |
| 性能分析 | 热点识别 | 复杂度分析 | 性能建模 | 调优建议 |
| 测试覆盖评估 | 覆盖率检查 | 边界测试设计 | 变异测试 | 测试策略设计 |

## 2. 工作流

### 步骤 1：解析（需求解析）【2维】

1. [Read] 读取目标代码文件
2. [认知操作] 识别代码语言与框架

- [ ] 目标对齐: 确认审查范围
- [ ] 事实锚定: 代码结构已理解

### 步骤 2：执行（安全审查）【2维】

1. [Grep] 搜索已知漏洞模式
2. [Write] 生成审查报告

- [ ] 目标对齐: 安全检查覆盖需求
- [ ] 事实锚定: 漏洞已验证

## 3. 规则

### MUST

- **规则1** MUST 在审查报告中标注风险等级（Critical/High/Medium/Low）
- **规则2** MUST 对每个问题提供修复建议

### SHOULD

- **规则1** MAY 对历史修复记录进行关联分析

### MUST NOT

- **规则1** MUST NOT 修改源代码

## 工具引用表

| 工具 | 用途 |
|:---|:---|
| Read | 读取文件 |
| Grep | 搜索模式 |
| Write | 生成报告 |
"""


def _make_good_skill_en() -> str:
    """A well-formed generated SKILL in English (should pass most checks)."""
    return """---
name: code-reviewer
description: >
  Reviews code for quality, security, and best practices. Covers multiple
  languages and frameworks with structured feedback and actionable suggestions.
metadata:
  updated: "2026-07-15"
---

## 1. Capability Architecture

### 1.1 Capability Matrix

**Core Domain**: Code Review

| Domain | Foundation | Advanced | Expert | Extension |
|:---|:---|:---|:---|:---|
| Core: Code Review | Syntax/Style Check | Logic Defect Analysis | Architecture Review | Automated Review Pipeline |

**Radiating Domains**:

| Domain | Foundation | Advanced | Expert | Extension |
|:---|:---|:---|:---|:---|
| Security Vulnerability Detection | OWASP Top 10 Check | CWE Pattern Matching | Threat Modeling | Zero-Day Prediction |
| Performance Analysis | Hotspot Identification | Complexity Analysis | Performance Modeling | Optimization Suggestions |
| Test Coverage Evaluation | Coverage Check | Boundary Test Design | Mutation Testing | Test Strategy Design |

## 2. Workflow

### Step 1: Parse (Requirement Analysis) [Execution - 3 Dimensions]

1. [Read] Read target code files
2. [Cognitive Operation] Identify code language and framework

- [ ] Goal Alignment: Confirm review scope
- [ ] Fact Anchoring: Code structure understood

### Step 2: Execute (Security Review) [Execution - 3 Dimensions]

1. [Grep] Search for known vulnerability patterns
2. [Write] Generate review report

- [ ] Goal Alignment: Security check covers requirements
- [ ] Fact Anchoring: Vulnerabilities verified

## 3. Rules

### MUST

- **Rule 1** MUST assign risk levels (Critical/High/Medium/Low) in the review report
- **Rule 2** MUST provide fix suggestions for each issue

### SHOULD

- **Rule 1** MAY perform correlation analysis on historical fix records

### MUST NOT

- **Rule 1** MUST NOT modify source code

## Tool Reference Table

| Tool | Usage |
|:---|:---|
| Read | Read files |
| Grep | Search patterns |
| Write | Generate reports |
"""


def _make_bad_skill_zh() -> str:
    """Synthetic SKILL with capability terms in workflow (Chinese)."""
    return """---
name: bad-skill
description: A test SKILL with capability-workflow confusion for validation testing.
metadata:
  updated: "2026-07-15"
---

## 1. 能力架构

### 1.1 能力矩阵

**核心领域**:测试

| 领域 | 基础层 | 进阶层 | 高阶层 | 拓展层 |
|:---|:---|:---|:---|:---|
| 核心:测试 | 基础测试 | 集成测试 | 性能测试 | 测试策略 |

## 2. 工作流

### 步骤 1：解析【2维】

1. [Read] 读取文件
2. 评估核心领域与辐射领域的交互 —— 这是能力矩阵概念不应出现在工作流中！

- [ ] 目标对齐: 确认范围
- [ ] 事实锚定: 信息已提取

## 3. 规则

### MUST

- **规则1** MUST 验证测试结果
"""


def _make_bad_skill_en() -> str:
    """Synthetic SKILL with capability terms in workflow (English)."""
    return """---
name: bad-skill
description: A test SKILL with capability-workflow confusion for validation testing.
metadata:
  updated: "2026-07-15"
---

## 1. Capability Architecture

### 1.1 Capability Matrix

**Core Domain**: Testing

| Domain | Foundation | Advanced | Expert | Extension |
|:---|:---|:---|:---|:---|
| Core: Testing | Basic Testing | Integration Testing | Performance Testing | Test Strategy |

## 2. Workflow

### Step 1: Parse [Execution - 3 Dimensions]

1. [Read] Read files
2. Evaluate interaction between Core Domain and Radiating Domains -- this is capability matrix concepts should NOT appear in workflow!

- [ ] Goal Alignment: Confirm scope
- [ ] Fact Anchoring: Information extracted

## 3. Rules

### MUST

- **Rule 1** MUST verify test results
"""


def _make_bad_no_tool_table_zh() -> str:
    """Synthetic SKILL using tools but no tool reference table (Chinese)."""
    return """---
name: missing-table-skill
description: A SKILL that uses tools but has no tool reference table for testing.
metadata:
  updated: "2026-07-15"
---

## 1. 能力架构

### 1.1 能力矩阵

**核心领域**:数据处理

| 领域 | 基础层 | 进阶层 | 高阶层 | 拓展层 |
|:---|:---|:---|:---|:---|
| 核心:数据处理 | 数据读取 | 数据清洗 | 数据分析 | 数据建模 |

## 2. 工作流

### 步骤 1：处理【2维】

1. [Read] 读取数据文件
2. [Write] 写入结果

- [ ] 目标对齐: 确认数据格式
- [ ] 事实锚定: 数据已加载

## 3. 规则

### MUST

- **规则1** MUST 验证数据完整性
"""


def _make_bad_no_tool_table_en() -> str:
    """Synthetic SKILL using tools but no tool reference table (English)."""
    return """---
name: missing-table-skill
description: A SKILL that uses tools but has no tool reference table for testing.
metadata:
  updated: "2026-07-15"
---

## 1. Capability Architecture

### 1.1 Capability Matrix

**Core Domain**: Data Processing

| Domain | Foundation | Advanced | Expert | Extension |
|:---|:---|:---|:---|:---|
| Core: Data Processing | Data Reading | Data Cleaning | Data Analysis | Data Modeling |

## 2. Workflow

### Step 1: Process [Execution - 3 Dimensions]

1. [Read] Read data files
2. [Write] Write results

- [ ] Goal Alignment: Confirm data format
- [ ] Fact Anchoring: Data loaded

## 3. Rules

### MUST

- **Rule 1** MUST verify data integrity
"""


class TestGeneratedSkillValidation:
    """Verify scripts can validate a generated SKILL (not UR-SKILL itself)."""

    @pytest.mark.parametrize(
        "lang, make_good, scripts_fixture",
        [
            pytest.param("zh-cn", _make_good_skill_zh, "scripts_dir", id="zh-cn"),
            pytest.param("en-us", _make_good_skill_en, "en_scripts_dir", id="en-us"),
        ],
    )
    def test_good_skill_passes_capability_check(self, lang, make_good, scripts_fixture, request):
        """Well-formed generated SKILL should pass capability structure check."""
        scripts = request.getfixturevalue(scripts_fixture)
        config = load_config(lang, scripts)
        text = make_good()
        with tempfile.NamedTemporaryFile(suffix=".md", mode="w", encoding="utf-8", delete=False) as f:
            f.write(text)
            tmp_path = Path(f.name)
        try:
            ctx = SkillContext(text=text, path=tmp_path, config=config)
            findings = ctx.run(validator_content._validate_capability_structure)
            errors = [f for f in findings if f.severity == "error"]
            assert len(errors) == 0, f"[{lang}] Good skill should pass capability check: {errors}"
        finally:
            tmp_path.unlink(missing_ok=True)

    @pytest.mark.parametrize(
        "lang, make_bad, scripts_fixture",
        [
            pytest.param("zh-cn", _make_bad_skill_zh, "scripts_dir", id="zh-cn"),
            pytest.param("en-us", _make_bad_skill_en, "en_scripts_dir", id="en-us"),
        ],
    )
    def test_capability_workflow_confusion_detected(self, lang, make_bad, scripts_fixture, request):
        """SKILL with capability terms in workflow should trigger confusion rule."""
        scripts = request.getfixturevalue(scripts_fixture)
        config = load_config(lang, scripts)
        text = make_bad()
        with tempfile.NamedTemporaryFile(suffix=".md", mode="w", encoding="utf-8", delete=False) as f:
            f.write(text)
            tmp_path = Path(f.name)
        try:
            ctx = SkillContext(text=text, path=tmp_path, config=config)
            findings = ctx.run(validator_content._validate_capability_workflow_confusion)
            assert any(
                f.rule == "capability-workflow-confusion" for f in findings
            ), f"[{lang}] Should detect capability-workflow confusion: {findings}"
        finally:
            tmp_path.unlink(missing_ok=True)

    @pytest.mark.parametrize(
        "lang, make_bad, scripts_fixture",
        [
            pytest.param("zh-cn", _make_bad_no_tool_table_zh, "scripts_dir", id="zh-cn"),
            pytest.param("en-us", _make_bad_no_tool_table_en, "en_scripts_dir", id="en-us"),
        ],
    )
    def test_missing_tool_table_detected(self, lang, make_bad, scripts_fixture, request):
        """SKILL using tools without tool reference table should be flagged."""
        scripts = request.getfixturevalue(scripts_fixture)
        config = load_config(lang, scripts)
        text = make_bad()
        with tempfile.NamedTemporaryFile(suffix=".md", mode="w", encoding="utf-8", delete=False) as f:
            f.write(text)
            tmp_path = Path(f.name)
        try:
            ctx = SkillContext(text=text, path=tmp_path, config=config)
            findings = ctx.run(validator_runtime._validate_tool_reference_table)
            assert any(
                f.rule == "tool-reference-table-missing" for f in findings
            ), f"[{lang}] Should detect missing tool reference table: {findings}"
        finally:
            tmp_path.unlink(missing_ok=True)

    @pytest.mark.parametrize(
        "lang, make_good, scripts_fixture",
        [
            pytest.param("zh-cn", _make_good_skill_zh, "scripts_dir", id="zh-cn"),
            pytest.param("en-us", _make_good_skill_en, "en_scripts_dir", id="en-us"),
        ],
    )
    def test_good_skill_has_tool_table(self, lang, make_good, scripts_fixture, request):
        """Well-formed SKILL with tool reference table should not be flagged."""
        scripts = request.getfixturevalue(scripts_fixture)
        config = load_config(lang, scripts)
        text = make_good()
        with tempfile.NamedTemporaryFile(suffix=".md", mode="w", encoding="utf-8", delete=False) as f:
            f.write(text)
            tmp_path = Path(f.name)
        try:
            ctx = SkillContext(text=text, path=tmp_path, config=config)
            findings = ctx.run(validator_runtime._validate_tool_reference_table)
            assert len(findings) == 0, f"[{lang}] Good skill should not trigger tool table warning: {findings}"
        finally:
            tmp_path.unlink(missing_ok=True)
