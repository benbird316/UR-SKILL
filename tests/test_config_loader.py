"""测试配置加载器。"""

import re

import pytest
import yaml

from config_loader import load_config


class TestLoadConfig:
    def test_load_zh_cn(self, scripts_dir) -> None:
        config = load_config("zh-cn", scripts_dir)
        assert config["lang"] == "zh-cn"
        assert "thresholds" in config
        assert "frontmatter" in config
        assert "workflow" in config
        assert "rules" in config
        assert "placeholders" in config
        assert "tools" in config
        assert "identity" in config
        assert "messages" in config

    def test_load_en_us(self, en_scripts_dir) -> None:
        config = load_config("en-us", en_scripts_dir)
        assert config["lang"] == "en-us"
        assert "thresholds" in config
        assert "frontmatter" in config
        assert "messages" in config

    def test_all_regex_compile(self, scripts_dir, en_scripts_dir) -> None:
        """确保所有 YAML 中的正则都能编译。"""
        paths = [
            (scripts_dir / "config.zh-cn.yaml", "zh-cn"),
            (en_scripts_dir / "config.en-us.yaml", "en-us"),
        ]
        for path, lang in paths:
            config = yaml.safe_load(path.read_text(encoding="utf-8")) or {}

            for pat in config.get("placeholders", {}).get("general_patterns", []):
                re.compile(pat)

            for item in config.get("placeholders", {}).get("unresolved_patterns", []):
                re.compile(item["pattern"])

            for pat in config.get("placeholders", {}).get("allowed_patterns", []):
                re.compile(pat)

            wf_pat = config.get("workflow", {}).get("step_heading_pattern")
            if wf_pat:
                re.compile(wf_pat)

            rules_pat = config.get("rules", {}).get("rules_heading_pattern")
            if rules_pat:
                re.compile(rules_pat)

    def test_config_fallback_exists(self, scripts_dir) -> None:
        """若 config.yaml 回退文件存在，测试回退逻辑。"""
        fallback = scripts_dir / "config.yaml"
        if fallback.exists():
            config = load_config("nonexistent", scripts_dir)
            assert isinstance(config, dict)
        else:
            with pytest.raises(FileNotFoundError):
                load_config("nonexistent", scripts_dir)

    def test_invalid_yaml_raises(self, scripts_dir, tmp_path) -> None:
        """非法 YAML 配置文件应抛出错误。"""
        bad = tmp_path / "config.bad.yaml"
        bad.write_text(": : : invalid yaml [[[", encoding="utf-8")
        with pytest.raises(yaml.YAMLError):
            load_config("bad", tmp_path)
