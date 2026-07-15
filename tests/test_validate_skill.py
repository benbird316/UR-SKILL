"""测试 validate_skill.py 的 SKILL 校验逻辑。"""

import importlib.util
import sys
from pathlib import Path
from typing import Any

import pytest

import validate_skill as validate_skill_cn


def _load_en_validate_skill(en_scripts_dir: Path) -> Any:
    """通过 importlib 加载 EN 版本的 validate_skill 模块。"""
    en_path = en_scripts_dir / "validate_skill.py"
    spec = importlib.util.spec_from_file_location("validate_skill_en", str(en_path))
    mod = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(mod)  # type: ignore[union-attr]
    return mod


class TestMainCN:
    """测试 CN 版 validate_skill.main()。"""

    def _run_main(self, skill_dir: Path, lang: str = "zh-cn", fmt: str = "text") -> int:
        """在受控 sys.argv 下调用 main()。"""
        saved = sys.argv
        try:
            sys.argv = ["validate_skill.py", "--skill-dir", str(skill_dir), "--lang", lang]
            if fmt != "text":
                sys.argv.extend(["--format", fmt])
            return validate_skill_cn.main()
        finally:
            sys.argv = saved

    def test_real_cn_skill_runs_without_error(
        self, ur_skill_cn_dir: Path, capsys: pytest.CaptureFixture[str],
    ) -> None:
        """对 UR-SKILL-CN 自身执行校验，不抛异常且有输出。"""
        rc = self._run_main(ur_skill_cn_dir, lang="zh-cn")
        captured = capsys.readouterr()
        # 真实项目可能有校验问题，返回 0 或 1 都可接受
        assert rc in (0, 1)
        assert len(captured.out) > 0

    def test_skill_md_not_found_returns_one(self, tmp_path: Path) -> None:
        """SKILL.md 缺失时返回 1。"""
        rc = self._run_main(tmp_path, lang="zh-cn")
        assert rc == 1

    def test_prints_error_to_stderr(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """SKILL.md 不存在时错误信息写入 stderr。"""
        rc = self._run_main(tmp_path, lang="zh-cn")
        assert rc == 1
        captured = capsys.readouterr()
        assert captured.err != ""
        assert "SKILL.md" in captured.err

    def test_json_format_runs_without_error(
        self, ur_skill_cn_dir: Path, capsys: pytest.CaptureFixture[str],
    ) -> None:
        """JSON 格式下不抛异常且输出有效 JSON。"""
        import json

        rc = self._run_main(ur_skill_cn_dir, lang="zh-cn", fmt="json")
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert isinstance(data, list)
        # RC 可能是 0 或 1，取决于真实 SKILL.md 内容
        assert rc in (0, 1)

    def test_json_output_has_expected_fields(
        self, ur_skill_cn_dir: Path, capsys: pytest.CaptureFixture[str],
    ) -> None:
        """JSON 输出包含规则/消息等字段。"""
        import json

        self._run_main(ur_skill_cn_dir, lang="zh-cn", fmt="json")
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        if data:
            item = data[0]
            assert "rule" in item
            assert "message" in item
            assert "severity" in item

    def test_invalid_frontmatter_returns_one(self, tmp_path: Path) -> None:
        """前导元数据无效时返回 1（name 字段为空）。"""
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text(
            "---\nname: ''\n---\n\nbody",
            encoding="utf-8",
        )
        rc = self._run_main(tmp_path, lang="zh-cn")
        assert rc == 1

    def test_valid_minimal_skill_returns_zero(self, tmp_path: Path) -> None:
        """完全合规的 SKILL.md 返回 0。"""
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text(
            "---\n"
            "name: my-awesome-skill\n"
            "description: >-\n"
            "  这是一个用于通用场景的 SKILL，提供自动化代码处理与文档生成能力，\n"
            "  具备完整的工作流与规则体系，可满足各类日常开发协作需求。\n"
            "metadata:\n"
            '  updated: "2025-01-15"\n'
            "  type: prompt\n"
            "  whenToUse: 用于通用场景\n"
            "---\n"
            "\n"
            "## 能力矩阵\n"
            "\n"
            "| A. 代码处理 | 基础 | 进阶 | 高阶 |\n"
            "| B. 内容分析 | 基础 | 进阶 | 高阶 |\n"
            "| C. 自动化流程 | 基础 | 进阶 | 高阶 |\n"
            "| 核心领域: 文档生成 | 基础 | 进阶 | 高阶 |\n"
            "| 基础层 | 文本处理 | 分析能力 | 输出能力 |\n"
            "| 进阶层 | 文本处理 | 分析能力 | 输出能力 |\n"
            "| 高阶层 | 文本处理 | 分析能力 | 输出能力 |\n"
            "| 拓展层 | 文本处理 | 分析能力 | 输出能力 |\n"
            "\n"
            "## 规则\n"
            "\n"
            "- MUST 规则一: 所有输出必须经过格式验证\n"
            "- SHOULD 规则二: 优先使用结构化数据格式\n"
            "- MAY 规则三: 可根据需要添加自定义选项\n"
            "\n"
            "## 工作流\n"
            "\n"
            "文件依赖决策: 确认是否需要读取用户已有文件\n"
            "\n"
            "1. 使用 [Read] 工具读取输入文件\n"
            "2. 分析内容结构与格式\n"
            "3. 使用 [Write] 工具生成输出文档\n"
            "\n"
            "## 工具引用表\n"
            "\n"
            "| 工具 | 用途 |\n"
            "|------|------|\n"
            "| Read | 读取文件内容 |\n"
            "| Write | 写入生成结果 |\n",
            encoding="utf-8",
        )
        rc = self._run_main(tmp_path, lang="zh-cn")
        assert rc == 0

    def test_missing_skill_md_has_summary_in_output(self, tmp_path: Path, capsys: pytest.CaptureFixture[str]) -> None:
        """SKILL.md 不存在时 stderr 包含路径信息。"""
        self._run_main(tmp_path, lang="zh-cn")
        captured = capsys.readouterr()
        assert captured.err != ""
        # 路径信息会出现在错误消息中
        assert str(tmp_path).replace("\\", "/") in captured.err.replace("\\", "/") or "SKILL.md" in captured.err


class TestMainEN:
    """测试 EN 版 validate_skill.main()。"""

    @pytest.fixture(scope="class")
    def en_module(self, en_scripts_dir: Path) -> Any:
        """加载 EN 版 validate_skill 模块（class 级别共享）。"""
        return _load_en_validate_skill(en_scripts_dir)

    def _run_main(self, en_module: Any, skill_dir: Path, lang: str = "en-us", fmt: str = "text") -> int:
        """在受控 sys.argv 下调用 EN 版的 main()。"""
        saved = sys.argv
        try:
            sys.argv = ["validate_skill.py", "--skill-dir", str(skill_dir), "--lang", lang]
            if fmt != "text":
                sys.argv.extend(["--format", fmt])
            return en_module.main()
        finally:
            sys.argv = saved

    def test_real_en_skill_runs_without_error(
        self, en_module: Any, ur_skill_en_dir: Path, capsys: pytest.CaptureFixture[str],
    ) -> None:
        """对 UR-SKILL-EN 自身执行校验，不抛异常且有输出。"""
        rc = self._run_main(en_module, ur_skill_en_dir, lang="en-us")
        captured = capsys.readouterr()
        assert rc in (0, 1)
        assert len(captured.out) > 0

    def test_skill_md_not_found_returns_one(
        self, en_module: Any, tmp_path: Path,
    ) -> None:
        """SKILL.md 缺失时返回 1。"""
        rc = self._run_main(en_module, tmp_path, lang="en-us")
        assert rc == 1

    def test_en_json_format_runs_without_error(
        self, en_module: Any, ur_skill_en_dir: Path, capsys: pytest.CaptureFixture[str],
    ) -> None:
        """EN 版本 JSON 格式正常工作。"""
        import json

        rc = self._run_main(en_module, ur_skill_en_dir, lang="en-us", fmt="json")
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        assert isinstance(data, list)
        assert rc in (0, 1)

    def test_en_json_output_has_expected_fields(
        self, en_module: Any, ur_skill_en_dir: Path, capsys: pytest.CaptureFixture[str],
    ) -> None:
        """EN 版本 JSON 输出包含规则/消息等字段。"""
        import json

        self._run_main(en_module, ur_skill_en_dir, lang="en-us", fmt="json")
        captured = capsys.readouterr()
        data = json.loads(captured.out)
        if data:
            item = data[0]
            assert "rule" in item
            assert "message" in item
            assert "severity" in item

    def test_valid_minimal_en_skill_returns_zero(
        self, en_module: Any, tmp_path: Path,
    ) -> None:
        """完全合规的 EN SKILL.md 返回 0。"""
        skill_md = tmp_path / "SKILL.md"
        skill_md.write_text(
            "---\n"
            "name: my-awesome-skill\n"
            "description: >-\n"
            "  A SKILL for general-purpose document generation and code processing,\n"
            "  with complete workflow and rule system for daily development tasks.\n"
            "metadata:\n"
            '  updated: "2025-01-15"\n'
            "  type: prompt\n"
            "  whenToUse: for general purpose scenarios\n"
            "---\n"
            "\n"
            "## Capability Matrix\n"
            "\n"
            "| A. code processing | basic | advanced | expert |\n"
            "| B. content analysis | basic | advanced | expert |\n"
            "| C. workflow automation | basic | advanced | expert |\n"
            "| Core Domain: document generation | basic | advanced | expert |\n"
            "| Foundation | text | analysis | output |\n"
            "| Advanced | text | analysis | output |\n"
            "| Expert | text | analysis | output |\n"
            "| Extension | text | analysis | output |\n"
            "\n"
            "## Rules\n"
            "\n"
            "- MUST Rule 1: All output MUST pass format validation\n"
            "- SHOULD Rule 2: Structured data format SHOULD be preferred\n"
            "- MAY Rule 3: Custom options MAY be added as needed\n"
            "\n"
            "## Workflow\n"
            "\n"
            "File dependency decision: confirm if user files need to be read\n"
            "\n"
            "1. Use [Read] tool to read input file\n"
            "2. Analyze content structure\n"
            "3. Use [Write] tool to generate output document\n"
            "\n"
            "## Tool Reference Table\n"
            "\n"
            "| Tool | Purpose |\n"
            "|------|---------|\n"
            "| Read | Read file content |\n"
            "| Write | Write generated output |\n",
            encoding="utf-8",
        )
        rc = self._run_main(en_module, tmp_path, lang="en-us")
        assert rc == 0
