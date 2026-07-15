"""CI Integration Test: End-to-end SKILL package validation.

Generates temporary SKILL packages and runs validate_skill.py CLI on them
via subprocess — the same path GitHub Actions CI uses. This catches
regressions in the full validation pipeline (format → content → runtime).

Usage:
    python Scripts/ci_validate_examples.py
    python Scripts/ci_validate_examples.py --verbose
"""

from __future__ import annotations

import subprocess
import sys
import tempfile
from pathlib import Path

SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "UR-SKILL-CN" / "Scripts"
EN_SCRIPTS_DIR = Path(__file__).resolve().parent.parent / "UR-SKILL-EN" / "Scripts"


def _write_skill(pkg_dir: Path, skill_text: str) -> None:
    (pkg_dir / "SKILL.md").write_text(skill_text, encoding="utf-8")


def _make_good_skill_zh(name: str = "code-reviewer") -> str:
    """A well-formed generated SKILL that should pass all checks."""
    return f"""---
name: {name}
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

> 文件依赖决策：根据影响范围选择输出详略（参照 design-rationale.md §9）

### 步骤 1：解析（需求解析）【2维】

1. [Read] 读取目标代码文件
2. [认知操作] 识别代码语言与框架

- [ ] 目标对齐: 确认审查范围
- [ ] 事实锚定: 代码结构已理解
- [ ] 风险标识: 已知安全风险已检查
- [ ] 质量门禁: 代码规范已验证

### 步骤 2：执行（安全审查）【2维】

1. [Grep] 搜索已知漏洞模式
2. [Write] 生成审查报告

- [ ] 目标对齐: 安全检查覆盖需求
- [ ] 事实锚定: 漏洞已验证
- [ ] 风险标识: 修补建议已提供
- [ ] 质量门禁: 审查标准已满足

## 3. 规则

### MUST

- **MUST** 在审查报告中标注风险等级（Critical/High/Medium/Low）
- **MUST** 对每个问题提供修复建议

### SHOULD

- **MAY** 对历史修复记录进行关联分析

### MUST NOT

- **MUST NOT** 修改源代码

## 工具引用表

| 工具 | 用途 |
|:---|:---|
| Read | 读取文件 |
| Grep | 搜索模式 |
| Write | 生成报告 |
| AskUserQuestion | 确认修复验证循环 |

## 输出规格

- 输出格式：结构化 Markdown 报告（mermaid 流程图展示审查流程）
- 用户交互：确认 → 修复 → 验证循环
- 判决策略：Decision Strategy / Approved
"""


def _make_good_skill_en(name: str = "code-reviewer") -> str:
    """A well-formed English generated SKILL that should pass all checks."""
    return f"""---
name: {name}
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

> File dependency decision: Choose output detail based on impact scope (see design-rationale.md §9)

### Step 1: Parse (Requirement Analysis) (3 Dimensions)

1. [Read] Read target code files
2. [Cognitive Operation] Identify code language and framework

- [ ] Goal Alignment: Confirm review scope
- [ ] Fact Anchoring: Code structure understood
- [ ] Risk Identification: Known security risks checked
- [ ] File dependency decision: Choose output detail based on impact scope

### Step 2: Execute (Security Review) (3 Dimensions)

1. [Grep] Search for known vulnerability patterns
2. [Write] Generate review report

- [ ] Goal Alignment: Security check covers requirements
- [ ] Fact Anchoring: Vulnerabilities verified
- [ ] Risk Identification: Fix suggestions provided
- [ ] Quality Gate: Review criteria met

## 3. Rules

### MUST

- **MUST** assign risk levels (Critical/High/Medium/Low) in the review report
- **MUST** provide fix suggestions for each issue

### SHOULD

- **MAY** perform correlation analysis on historical fix records

### MUST NOT

- **MUST NOT** modify source code

## Tool Reference Table

| Tool | Usage |
|:---|:---|
| Read | Read files |
| Grep | Search patterns |
| Write | Generate reports |
| AskUserQuestion | Confirm-Fix-Verify loop |

## Output Specification

- Output format: Structured Markdown report (mermaid flowchart for review process)
- User interaction: Confirm → Fix → Verify loop
- Decision Strategy: Approved / Reject
"""


def _make_bad_skill_no_matrix() -> str:
    """SKILL missing capability matrix — should fail format validation."""
    return """---
name: bad-skill
description: A SKILL missing required sections for validation testing.
metadata:
  updated: "2026-07-15"
---

## 1. 能力架构

This section has no capability matrix table.

## 2. 工作流

### 步骤 1：处理【2维】

1. [Read] 读取文件

- [ ] 目标对齐: 确认范围
- [ ] 事实锚定: 信息已提取

## 3. 规则

### MUST

- **规则1** MUST 验证测试结果
"""


def _make_bad_skill_leak() -> str:
    """SKILL that leaks UR-SKILL internal files."""
    return """---
name: bad-skill
description: A SKILL that leaks internal paths for validation testing.
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

### 步骤 1：执行【2维】

1. [Read] 读取文件
2. [Write] 输出结果

- [ ] 目标对齐: 确认范围
- [ ] 事实锚定: 信息已提取

## 3. 规则

### MUST

- **规则1** MUST 验证测试结果

## 工具引用表

| 工具 | 用途 |
|:---|:---|
| Read | 读取 |
| Write | 输出 |
"""


def _validate_example(pkg_dir: Path, script_path: Path, lang: str,
                      expected_exit: int = 0, verbose: bool = False) -> bool:
    """Run validate_skill.py on a package directory.

    Returns True if actual exit code matches expected_exit.
    """
    cmd = [sys.executable, str(script_path),
           "--skill-dir", str(pkg_dir),
           "--lang", lang]
    result = subprocess.run(cmd, capture_output=True, text=True)
    passed = result.returncode == expected_exit

    if verbose or not passed:
        status = "PASS" if passed else "FAIL"
        print(f"  [{status}] exit={result.returncode} (expected={expected_exit})")
        if result.stdout.strip():
            print(f"    stdout: {result.stdout.strip()[:200]}")
        if result.stderr.strip():
            print(f"    stderr: {result.stderr.strip()[:200]}")

    return passed


def _check_ci_integration() -> bool:
    """Check that all existing CI scripts accept --help (smoke test)."""
    all_ok = True
    scripts = [
        ("UR-SKILL-CN", "bilingual_sync.py"),
        ("UR-SKILL-EN", "bilingual_sync.py"),
        ("UR-SKILL-CN", "validate_skill.py"),
        ("UR-SKILL-EN", "validate_skill.py"),
    ]
    for pkg, script in scripts:
        path = Path(__file__).resolve().parent.parent / pkg / "Scripts" / script
        if not path.exists():
            print(f"  [FAIL] Script not found: {path}")
            all_ok = False
            continue
        result = subprocess.run(
            [sys.executable, str(path), "--help"],
            capture_output=True, text=True
        )
        if result.returncode != 0:
            print(f"  [FAIL] {script} --help returned {result.returncode}")
            all_ok = False
        else:
            print(f"  [PASS] {script} --help")
    return all_ok


def run_tests(verbose: bool = False) -> int:
    """Run all integration tests. Returns 0 on success, 1 on failure."""
    failed = 0
    total = 0

    # Smoke: CI scripts respond to --help
    print("=== Smoke: CI script availability ===")
    if not _check_ci_integration():
        failed += 1
    total += 1

    # Test good CN skill
    print("\n=== Test: Good SKILL (zh-cn) — should pass ===")
    with tempfile.TemporaryDirectory() as td:
        pkg = Path(td)
        _write_skill(pkg, _make_good_skill_zh())
        if not _validate_example(pkg, SCRIPTS_DIR / "validate_skill.py",
                                 "zh-cn", expected_exit=0, verbose=verbose):
            failed += 1
        total += 1

    # Test good EN skill
    print("\n=== Test: Good SKILL (en-us) — should pass ===")
    with tempfile.TemporaryDirectory() as td:
        pkg = Path(td)
        _write_skill(pkg, _make_good_skill_en())
        if not _validate_example(pkg, EN_SCRIPTS_DIR / "validate_skill.py",
                                 "en-us", expected_exit=0, verbose=verbose):
            failed += 1
        total += 1

    # Test bad SKILL — missing capability matrix
    print("\n=== Test: Bad SKILL (no capability matrix) — should fail ===")
    with tempfile.TemporaryDirectory() as td:
        pkg = Path(td)
        _write_skill(pkg, _make_bad_skill_no_matrix())
        if not _validate_example(pkg, SCRIPTS_DIR / "validate_skill.py",
                                 "zh-cn", expected_exit=1, verbose=verbose):
            failed += 1
        total += 1

    # Test bad SKILL — missing SKILL.md
    print("\n=== Test: Empty package (no SKILL.md) — should fail ===")
    with tempfile.TemporaryDirectory() as td:
        pkg = Path(td)
        if not _validate_example(pkg, SCRIPTS_DIR / "validate_skill.py",
                                 "zh-cn", expected_exit=1, verbose=verbose):
            failed += 1
        total += 1

    # Summary
    passed = total - failed
    print(f"\n{'=' * 40}")
    print(f"Results: {passed}/{total} passed, {failed} failed")
    print(f"{'=' * 40}")

    return 1 if failed > 0 else 0


def main() -> int:
    import argparse
    parser = argparse.ArgumentParser(
        description="CI integration tests for SKILL validation pipeline"
    )
    parser.add_argument("--verbose", "-v", action="store_true",
                        help="Show full output for each test")
    args = parser.parse_args()
    return run_tests(verbose=args.verbose)


if __name__ == "__main__":
    sys.exit(main())
