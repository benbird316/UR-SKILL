#!/usr/bin/env python3
"""SKILL static validation script.

Purpose: Automatically check SKILL.md format, content, reference consistency,
and anti-patterns before delivery.
Core principle: All rules must be programmatically verifiable, avoiding manual
line-by-line review.

Usage:
    python validate_skill.py --skill-dir ../ --lang en-us
    python validate_skill.py --skill-dir ../ --lang zh-cn --format json
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
    parser = argparse.ArgumentParser(description="Validate SKILL.md quality")
    parser.add_argument(
        "--skill-dir",
        type=Path,
        default=Path("."),
        help="SKILL directory (containing SKILL.md and references/)",
    )
    parser.add_argument(
        "--lang",
        choices=["zh-cn", "en-us"],
        default="en-us",
        help="Validation rule language",
    )
    parser.add_argument(
        "--format",
        choices=["text", "json"],
        default="text",
        help="Output format",
    )
    args = parser.parse_args()

    scripts_dir = Path(__file__).resolve().parent
    config = load_config(args.lang, scripts_dir)

    skill_file = args.skill_dir / "SKILL.md"
    if not skill_file.exists():
        msg = config.get("messages", {}).get("skill_file_not_found", "Error: {path} not found")
        print(msg.format(path=skill_file), file=sys.stderr)
        return 1

    text = skill_file.read_text(encoding="utf-8")
    ctx = SkillContext(text=text, path=skill_file, config=config)

    findings: list[Finding] = []
    for validator in VALIDATORS:
        findings.extend(ctx.run(validator))

    # frontmatter parse errors also added to findings
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
    summary_items = msgs.get("summary_items", [])
    rendered = [item.format(body_lines=body_lines, max_lines=max_lines) for item in summary_items]
    print("\n".join(msgs["summary_line"].format(item=item) for item in rendered))


if __name__ == "__main__":
    sys.exit(main())
