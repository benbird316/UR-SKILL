#!/usr/bin/env python3
"""
UR-SKILL 安装脚本

自动检测用户使用的 AI Agent 平台，将 UR-SKILL 安装到正确位置。
只安装所选语言的 SKILL 包内容（不含仓库根目录的 install.py / tests / README 等）。

支持的平台（39 个）:
    Claude Code, Cursor, VS Code Copilot, Trae, Codex, Gemini CLI,
    Windsurf, Cline, Roo, Goose, Augment, Continue, CodeBuddy, Qwen,
    OpenCode, KiloCode, Kiro, Antigravity, Amp, Adal, Crush, Droid,
    Factory, Iflow, Junie, Kode, MCPJam, Mistral Vibe, Mux, Neovate,
    OpenClaw, OpenHands, Pi, Pochi, Qoder, Replit, Zencoder, CommandCode

用法:
    python install.py                    # 交互式：选择语言 + 自动检测平台
    python install.py --lang zh-cn       # 安装中文版
    python install.py --lang en-us       # 安装英文版
    python install.py --list             # 列出检测到的平台
    python install.py --target trae      # 指定目标平台
    python install.py --uninstall        # 卸载
"""

from __future__ import annotations

import argparse
import os
import shutil
import sys
from pathlib import Path

# ── 39 个 Agent 平台的安装路径配置 ──────────────────────────
# 格式: {agent_id: {"display": "显示名", "local": "项目级路径", "global": "全局路径"}}

AGENT_TARGETS: dict[str, dict[str, str]] = {
    "amp":            {"display": "Amp",               "local": ".agents/skills", "global": "$XDG_CONFIG_HOME/agents/skills"},
    "codex":          {"display": "OpenAI Codex",       "local": ".codex/skills",  "global": "$CODEX_HOME/skills"},
    "gemini-cli":     {"display": "Gemini CLI",         "local": ".gemini/skills", "global": "$HOME/.gemini/skills"},
    "github-copilot": {"display": "GitHub Copilot",    "local": ".github/skills", "global": "$HOME/.copilot/skills"},
    "kimi-cli":       {"display": "Kimi Code CLI",      "local": ".kimi/skills",   "global": "$HOME/.config/agents/skills"},
    "opencode":       {"display": "OpenCode",           "local": ".opencode/skills", "global": "$XDG_CONFIG_HOME/opencode/skills"},
    "replit":         {"display": "Replit",             "local": ".agents/skills", "global": "$XDG_CONFIG_HOME/agents/skills"},
    "claude-code":    {"display": "Claude Code",        "local": ".claude/skills", "global": "$CLAUDE_CONFIG_DIR/skills"},
    "cursor":         {"display": "Cursor",             "local": ".cursor/skills", "global": "$HOME/.cursor/skills"},
    "trae":           {"display": "Trae",               "local": ".trae/skills",   "global": "$HOME/.trae/skills"},
    "trae-cn":        {"display": "Trae CN",            "local": ".trae/skills",   "global": "$HOME/.trae-cn/skills"},
    "windsurf":       {"display": "Windsurf",           "local": ".windsurf/skills", "global": "$HOME/.codeium/windsurf/skills"},
    "cline":          {"display": "Cline",              "local": ".cline/skills",  "global": "$HOME/.cline/skills"},
    "roo":            {"display": "Roo",                "local": ".roo/skills",    "global": "$HOME/.roo/skills"},
    "goose":          {"display": "Goose",              "local": ".goose/skills",  "global": "$XDG_CONFIG_HOME/goose/skills"},
    "augment":        {"display": "Augment",            "local": ".augment/skills", "global": "$HOME/.augment/skills"},
    "continue":       {"display": "Continue",           "local": ".continue/skills", "global": "$HOME/.continue/skills"},
    "codebuddy":      {"display": "CodeBuddy",          "local": ".codebuddy/skills", "global": "$HOME/.codebuddy/skills"},
    "qwen":           {"display": "Qwen Code",          "local": ".qwen/skills",   "global": "$HOME/.qwen/skills"},
    "kilocode":       {"display": "KiloCode",           "local": ".kilocode/skills", "global": "$HOME/.kilocode/skills"},
    "kiro":           {"display": "Kiro CLI",           "local": ".kiro/skills",   "global": "$HOME/.kiro/skills"},
    "antigravity":    {"display": "Antigravity",        "local": ".agent/skills",  "global": "$HOME/.gemini/antigravity/skills"},
    "adal":           {"display": "Adal",               "local": ".adal/skills",   "global": "$HOME/.adal/skills"},
    "crush":          {"display": "Crush",              "local": ".crush/skills",  "global": "$HOME/.config/crush/skills"},
    "droid":          {"display": "Factory Droid",      "local": ".factory/skills", "global": "$HOME/.factory/skills"},
    "iflow-cli":      {"display": "iFlow CLI",          "local": ".iflow/skills",  "global": "$HOME/.iflow/skills"},
    "junie":          {"display": "Junie",              "local": ".junie/skills",  "global": "$HOME/.junie/skills"},
    "kode":           {"display": "Kode",               "local": ".kode/skills",   "global": "$HOME/.kode/skills"},
    "mcpjam":         {"display": "MCPJam",             "local": ".mcpjam/skills", "global": "$HOME/.mcpjam/skills"},
    "mistral-vibe":   {"display": "Mistral Vibe",       "local": ".vibe/skills",   "global": "$HOME/.vibe/skills"},
    "mux":            {"display": "Mux",                "local": ".mux/skills",    "global": "$HOME/.mux/skills"},
    "neovate":        {"display": "Neovate",            "local": ".neovate/skills", "global": "$HOME/.neovate/skills"},
    "openclaw":       {"display": "OpenClaw",           "local": "skills",         "global": "$HOME/.openclaw/skills"},
    "openhands":      {"display": "OpenHands",          "local": ".openhands/skills", "global": "$HOME/.openhands/skills"},
    "pi":             {"display": "Pi",                 "local": ".pi/skills",     "global": "$HOME/.pi/agent/skills"},
    "pochi":          {"display": "Pochi",              "local": ".pochi/skills",  "global": "$HOME/.pochi/skills"},
    "qoder":          {"display": "Qoder",              "local": ".qoder/skills",  "global": "$HOME/.qoder/skills"},
    "zencoder":       {"display": "Zencoder",           "local": ".zencoder/skills", "global": "$HOME/.zencoder/skills"},
    "command-code":   {"display": "CommandCode",        "local": ".commandcode/skills", "global": "$HOME/.commandcode/skills"},
}

LANG_CHOICES = {
    "zh-cn": {"display": "UR-SKILL-CN (中文版)",     "source_dir": "UR-SKILL-CN"},
    "en-us": {"display": "UR-SKILL-EN (English)",    "source_dir": "UR-SKILL-EN"},
}


def _expand_path(raw: str) -> Path:
    """展开环境变量占位符为实际路径。"""
    result = raw
    for var in ("HOME", "XDG_CONFIG_HOME", "CLAUDE_CONFIG_DIR", "CODEX_HOME"):
        if f"${var}" in result:
            if var == "HOME":
                value = str(Path.home())
            elif var == "XDG_CONFIG_HOME":
                value = os.environ.get("XDG_CONFIG_HOME", str(Path.home() / ".config"))
            elif var == "CLAUDE_CONFIG_DIR":
                value = os.environ.get("CLAUDE_CONFIG_DIR", str(Path.home() / ".claude"))
            elif var == "CODEX_HOME":
                value = os.environ.get("CODEX_HOME", str(Path.home() / ".codex"))
            result = result.replace(f"${var}", value)
    return Path(result)


def detect_installed_agents() -> list[str]:
    """检测当前系统安装了哪些 Agent 平台。"""
    detected: list[str] = []
    home = Path.home()

    markers: dict[str, list[str]] = {
        "claude-code":    [".claude", ".claude.json"],
        "cursor":         [".cursor"],
        "trae":           [".trae"],
        "trae-cn":        [".trae-cn"],
        "windsurf":       [".windsurf", ".codeium"],
        "cline":          [".cline"],
        "roo":            [".roo"],
        "goose":          [".goose", ".config/goose"],
        "augment":        [".augment"],
        "continue":       [".continue"],
        "codebuddy":      [".codebuddy"],
        "qwen":           [".qwen"],
        "github-copilot": [".copilot", ".github"],
        "codex":          [".codex"],
        "gemini-cli":     [".gemini"],
        "kimi-cli":       [".kimi"],
        "opencode":       [".opencode"],
        "kilocode":       [".kilocode"],
        "kiro":           [".kiro"],
        "antigravity":    [".agent"],
        "adal":           [".adal"],
        "crush":          [".config/crush"],
        "droid":          [".factory"],
        "iflow-cli":      [".iflow"],
        "junie":          [".junie"],
        "kode":           [".kode"],
        "mcpjam":         [".mcpjam"],
        "mistral-vibe":   [".vibe"],
        "mux":            [".mux"],
        "neovate":        [".neovate"],
        "openclaw":       [".openclaw"],
        "openhands":      [".openhands"],
        "pi":             [".pi"],
        "pochi":          [".pochi"],
        "qoder":          [".qoder"],
        "zencoder":       [".zencoder"],
        "command-code":   [".commandcode"],
    }

    for agent_id, paths in markers.items():
        for p in paths:
            if (home / p).exists():
                detected.append(agent_id)
                break

    return detected


def install_skill(source_dir: Path, target_base: Path, skill_name: str = "ur-skill") -> bool:
    """将 SKILL 包内容复制到目标位置。

    只复制 SKILL 包内部内容（SKILL.md + 子目录），不复制外层仓库文件。
    """
    target_dir = target_base / skill_name

    if target_dir.exists():
        print(f"  [SKIP] Already exists: {target_dir}")
        return False

    # 验证 source 是有效的 SKILL 包
    if not (source_dir / "SKILL.md").exists():
        print(f"  [ERROR] SKILL.md not found in source: {source_dir}")
        return False

    target_dir.mkdir(parents=True, exist_ok=True)

    # 逐项复制 SKILL 包内容（排除 __pycache__）
    copied = 0
    for item in sorted(source_dir.iterdir()):
        if item.name == "__pycache__":
            continue
        dest = target_dir / item.name
        if item.is_dir():
            shutil.copytree(item, dest, dirs_exist_ok=True,
                            ignore=shutil.ignore_patterns("__pycache__", "*.pyc"))
        else:
            shutil.copy2(item, dest)
        copied += 1

    print(f"  Installed {copied} items -> {target_dir}")
    return True


def uninstall_skill(target_base: Path, skill_name: str = "ur-skill") -> bool:
    """卸载 SKILL。"""
    target_dir = target_base / skill_name
    if not target_dir.exists():
        print(f"  [SKIP] Not found: {target_dir}")
        return False
    shutil.rmtree(target_dir)
    print(f"  Removed: {target_dir}")
    return True


def _choose_language(args_lang: str | None) -> str:
    """确定语言版本：命令行指定 > 交互式选择。"""
    if args_lang:
        if args_lang not in LANG_CHOICES:
            print(f"ERROR: Unknown language '{args_lang}'. Choices: {', '.join(LANG_CHOICES)}")
            sys.exit(1)
        lang = args_lang
        print(f"Language: {LANG_CHOICES[lang]['display']}")
        return lang

    print("Select language version:")
    for i, (key, cfg) in enumerate(LANG_CHOICES.items(), 1):
        print(f"  [{i}] {cfg['display']}")

    while True:
        try:
            choice = input("Enter 1 or 2: ").strip()
            if choice == "1":
                lang = "zh-cn"
                break
            elif choice == "2":
                lang = "en-us"
                break
            print("  Please enter 1 or 2")
        except (EOFError, KeyboardInterrupt):
            print("\nCancelled.")
            sys.exit(0)

    print(f"Selected: {LANG_CHOICES[lang]['display']}")
    return lang


def main() -> int:
    parser = argparse.ArgumentParser(
        description="UR-SKILL 安装脚本 — 选择语言版本，自动检测平台并安装",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
示例:
  python install.py                    # 交互式：选语言 + 自动安装
  python install.py --lang zh-cn       # 安装中文版到所有检测到的平台
  python install.py --lang en-us       # 安装英文版
  python install.py --target trae      # 只安装到指定平台
  python install.py --list             # 列出检测到的平台
  python install.py --uninstall        # 卸载
  python install.py --global           # 安装到全局路径
        """,
    )
    parser.add_argument("--lang", type=str, choices=["zh-cn", "en-us"], help="语言版本（zh-cn / en-us），不指定则交互选择")
    parser.add_argument("--target", type=str, help="指定目标 Agent 平台（如 trae, cursor, claude-code）")
    parser.add_argument("--list", action="store_true", help="仅列出检测到的 Agent 平台")
    parser.add_argument("--global", dest="use_global", action="store_true", help="安装到全局路径（~/.xxx/）而非项目级")
    parser.add_argument("--uninstall", action="store_true", help="卸载 UR-SKILL")
    parser.add_argument("--name", type=str, default=None, help="SKILL 安装后的目录名（默认 ur-skill-cn 或 ur-skill-en）")
    parser.add_argument("--source", type=Path, default=None, help="源目录路径（默认自动检测仓库根目录）")
    args = parser.parse_args()

    # ── 仓库根目录 ──
    if args.source:
        repo_root = args.source.resolve()
    else:
        repo_root = Path(__file__).resolve().parent

    # ── 确定目标平台 ──
    if args.target:
        if args.target not in AGENT_TARGETS:
            print(f"ERROR: Unknown agent '{args.target}'")
            print(f"       Supported: {', '.join(sorted(AGENT_TARGETS.keys()))}")
            return 1
        targets = {args.target: AGENT_TARGETS[args.target]}
    else:
        detected = detect_installed_agents()
        if not detected:
            if args.list:
                targets = {}
            else:
                print("No AI agent platform detected.")
                print("Use --target to specify one manually.")
                print(f"Supported: {', '.join(sorted(AGENT_TARGETS.keys()))}")
                return 1
        else:
            print(f"Detected agents: {', '.join(detected)}")
            targets = {aid: AGENT_TARGETS[aid] for aid in detected if aid in AGENT_TARGETS}

    if args.list:
        if targets:
            print("\nDetected agent platforms:")
            for aid, cfg in targets.items():
                local = _expand_path(cfg["local"])
                global_ = _expand_path(cfg["global"])
                print(f"  {cfg['display']:20s}  local={local}  global={global_}")
        else:
            print("No AI agent platforms detected on this system.")
        return 0

    # ── 选择语言 ──
    lang = _choose_language(args.lang)
    source_dir = repo_root / LANG_CHOICES[lang]["source_dir"]

    if not source_dir.exists():
        print(f"ERROR: Source directory not found: {source_dir}")
        return 1
    if not (source_dir / "SKILL.md").exists():
        print(f"ERROR: SKILL.md not found in {source_dir}")
        return 1

    print(f"Source: {source_dir}")

    # ── 安装或卸载 ──
    skill_name = args.name or f"ur-skill-{lang}"
    count = 0

    for aid, cfg in sorted(targets.items()):
        display = cfg["display"]
        path_raw = cfg["global"] if args.use_global else cfg["local"]
        target_base = _expand_path(path_raw)

        print(f"\n[{display}]  target={target_base / skill_name}")

        if args.uninstall:
            if uninstall_skill(target_base, skill_name):
                count += 1
        else:
            if install_skill(source_dir, target_base, skill_name):
                count += 1

    print(f"\nDone. {count} operation(s) completed.")
    return 0


if __name__ == "__main__":
    sys.exit(main())
