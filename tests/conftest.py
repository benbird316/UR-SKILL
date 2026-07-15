"""pytest 共享 fixtures，消除测试文件间的重复。"""

import sys
from pathlib import Path

import pytest
import yaml

# 将 UR-SKILL-CN/Scripts 加入搜索路径，使所有测试可以直接导入 common、config_loader 等
ROOT = Path(__file__).resolve().parent.parent
SCRIPTS_DIR = ROOT / "UR-SKILL-CN" / "Scripts"
EN_SCRIPTS_DIR = ROOT / "UR-SKILL-EN" / "Scripts"
sys.path.insert(0, str(SCRIPTS_DIR))

from config_loader import load_config


@pytest.fixture(scope="session")
def scripts_dir() -> Path:
    """返回 CN Scripts 目录路径。"""
    return SCRIPTS_DIR


@pytest.fixture(scope="session")
def en_scripts_dir() -> Path:
    """返回 EN Scripts 目录路径。"""
    return EN_SCRIPTS_DIR


@pytest.fixture(scope="session")
def zh_config(scripts_dir: Path) -> dict:
    """中文校验配置（zh-cn）。"""
    return load_config("zh-cn", scripts_dir)


@pytest.fixture(scope="session")
def en_config(en_scripts_dir: Path) -> dict:
    """英文校验配置（en-us），从 EN 目录加载。"""
    return load_config("en-us", en_scripts_dir)


@pytest.fixture(scope="session")
def ur_skill_cn_dir() -> Path:
    """UR-SKILL-CN 项目根目录。"""
    return ROOT / "UR-SKILL-CN"


@pytest.fixture(scope="session")
def ur_skill_en_dir() -> Path:
    """UR-SKILL-EN 项目根目录。"""
    return ROOT / "UR-SKILL-EN"


@pytest.fixture(scope="session")
def ur_skill_cn_text(ur_skill_cn_dir: Path) -> str:
    """读取 UR-SKILL-CN 自身的 SKILL.md。"""
    return (ur_skill_cn_dir / "SKILL.md").read_text(encoding="utf-8")


@pytest.fixture(scope="session")
def ur_skill_en_text(ur_skill_en_dir: Path) -> str:
    """读取 UR-SKILL-EN 自身的 SKILL.md。"""
    return (ur_skill_en_dir / "SKILL.md").read_text(encoding="utf-8")
