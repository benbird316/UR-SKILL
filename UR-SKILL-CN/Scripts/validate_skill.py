#!/usr/bin/env python3
"""SKILL 静态校验脚本。

用途：在交付前自动检查 SKILL.md 的格式、内容、引用一致性与反模式。
核心原则：所有规则必须可程序化验证，避免人工逐行检查。

用法：
    python validate_skill.py --skill-dir ../ --lang zh-cn
    python validate_skill.py --skill-dir ../ --lang en-us --format json
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path

from common import Finding, Report, SkillContext
from config_loader import load_config
import validator_format
import validator_content
import validator_runtime

VALIDATORS = [
    validator_format.validate,
    validator_content.validate,
    validator_runtime.validate,
]


def main() -> int:
    parser = argparse.ArgumentParser(description="校验 SKILL.md 质量")
    parser.add_argument(
        "--skill-dir",
        type=Path,
        default=Path("."),
        help="SKILL 目录（包含 SKILL.md 与 references/）",
    )
    parser.add_argument(
        "--lang",
        choices=["zh-cn", "en-us"],
        default="zh-cn",
        help="校验规则语言",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="输出格式",
    )
    args = parser.parse_args()

    scripts_dir = Path(__file__).resolve().parent
    config = load_config(args.lang, scripts_dir)

    skill_file = args.skill_dir / "SKILL.md"
    if not skill_file.exists():
        msg = config.get("messages", {}).get("skill_file_not_found", "错误：未找到 {path}")
        print(msg.format(path=skill_file), file=sys.stderr)
        return 1

    text = skill_file.read_text(encoding="utf-8")
    ctx = SkillContext(text=text, path=skill_file, config=config)

    findings: list[Finding] = []
    for validator in VALIDATORS:
        findings.extend(ctx.run(validator))

    # frontmatter 解析错误也加入 findings
    for err in ctx.fm_parse_errors:
        findings.insert(0, Finding("frontmatter-parse", err, "error"))

    report = Report(findings, config)

    if args.format == "json":
        print(report.to_json())
    else:
        print(report.to_text())
        if not report.has_error:
            _print_summary(ctx, config)

    return 1 if report.has_error else 0


def _print_summary(ctx: SkillContext, config: dict) -> None:
    msgs = config.get("messages", {})
    body_lines = len(ctx.body.splitlines())
    max_lines = config.get("thresholds", {}).get("max_body_lines", 500)
    summary_items = [
        "frontmatter 字段完整",
        f"body 行数 {body_lines}/{max_lines}",
        "无占位符",
        "风险边界声明完整",
        "专业边界声明完整",
        "工作流检查项数量正确",
        "引用文件全部存在",
        "工具绑定检查通过",
        "输出规格检查通过",
    ]
    print("\n".join(msgs["summary_line"].format(item=item) for item in summary_items))


if __name__ == "__main__":
    sys.exit(main())
