#!/usr/bin/env python3
"""双语同步检查脚本。

检查 UR-SKILL-CN 和 UR-SKILL-EN 的文件结构是否一致，
确保两个目录有相同的文件布局，避免语义漂移。

用法：
    python bilingual_sync.py
    python bilingual_sync.py --base-dir ../
"""

from __future__ import annotations

import argparse
import sys
from pathlib import Path


def collect_relative_files(root: Path, skip_patterns: list[str] | None = None) -> set[str]:
    """收集目录下所有文件（相对于 root 的路径）。"""
    skip_patterns = skip_patterns or []
    files: set[str] = set()
    for f in root.rglob("*"):
        if f.is_file() and not f.name.startswith("."):
            rel = f.relative_to(root).as_posix()
            if any(rel.startswith(p) for p in skip_patterns):
                continue
            if any(part == "__pycache__" for part in Path(rel).parts):
                continue
            files.add(rel)
    return files


def main(base_dir: Path | None = None) -> int:
    if base_dir is None:
        base_dir = Path(__file__).resolve().parent.parent.parent
    else:
        base_dir = base_dir.resolve()
    cn_dir = base_dir / "UR-SKILL-CN"
    en_dir = base_dir / "UR-SKILL-EN"

    if not cn_dir.exists():
        print(f"ERROR: CN directory not found: {cn_dir}")
        return 1
    if not en_dir.exists():
        print(f"ERROR: EN directory not found: {en_dir}")
        return 1

    # 跳过这些目录/文件（它们在不同语言下是可以不同的）
    skip = [
        "Scripts/config.zh-cn.yaml",
        "Scripts/config.en-us.yaml",
        "Scripts/bilingual_sync.py",
    ]

    cn_files = collect_relative_files(cn_dir, skip)
    en_files = collect_relative_files(en_dir, skip)

    only_cn = cn_files - en_files
    only_en = en_files - cn_files

    issues = 0

    if only_cn:
        print(f"[WARN] Files only in CN ({len(only_cn)}) — these may need EN counterparts:")
        for f in sorted(only_cn):
            print(f"  - {f}")
            issues += 1

    if only_en:
        print(f"[WARN] Files only in EN ({len(only_en)}) — these may need CN counterparts:")
        for f in sorted(only_en):
            print(f"  - {f}")
            issues += 1

    # 检查 common 文件是否双向同步
    common_files = {f for f in cn_files & en_files}
    cn_size: dict[str, int] = {}
    en_size: dict[str, int] = {}

    for f in common_files:
        cn_size[f] = (cn_dir / f).stat().st_size
        en_size[f] = (en_dir / f).stat().st_size

    size_diff = {f for f in common_files if abs(cn_size.get(f, 0) - en_size.get(f, 0)) > 0}
    if size_diff:
        print(f"\n[INFO] Files with size difference (may need sync):")
        for f in sorted(size_diff):
            print(f"  - {f}: CN={cn_size[f]}B, EN={en_size[f]}B")

    total_cn = len(cn_files)
    total_en = len(en_files)
    common = len(common_files)
    overlap = common / max(total_cn, total_en) * 100 if max(total_cn, total_en) > 0 else 100

    print(f"\n[SUMMARY] CN={total_cn} files, EN={total_en} files, Common={common} files, Overlap={overlap:.1f}%")

    if issues > 0:
        print(f"[RESULT] {issues} issue(s) found")
        return 1
    else:
        print("[RESULT] CN/EN directories are structurally aligned")
        return 0


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="检查 CN/EN 双语文件结构一致性")
    parser.add_argument("--base-dir", type=Path, default=None, help="仓库根目录（默认自动检测）")
    args = parser.parse_args()
    sys.exit(main(args.base_dir))
