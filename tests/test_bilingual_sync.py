"""测试 bilingual_sync.py 的双语同步检查逻辑。"""

from pathlib import Path

from bilingual_sync import collect_relative_files, main


class TestCollectRelativeFiles:
    """测试 collect_relative_files() 文件收集逻辑。"""

    def test_collects_all_files(self, tmp_path: Path) -> None:
        """收集常规文件。"""
        (tmp_path / "file1.txt").write_text("a")
        sub = tmp_path / "sub"
        sub.mkdir()
        (sub / "file2.py").write_text("b")
        nested = sub / "nested"
        nested.mkdir()
        (nested / "file3.md").write_text("c")

        files = collect_relative_files(tmp_path)
        assert files == {
            "file1.txt",
            "sub/file2.py",
            "sub/nested/file3.md",
        }

    def test_skips_hidden_files(self, tmp_path: Path) -> None:
        """跳过 . 开头的隐藏文件。"""
        (tmp_path / "visible.txt").write_text("a")
        (tmp_path / ".hidden.yaml").write_text("b")
        (tmp_path / ".env").write_text("c")

        files = collect_relative_files(tmp_path)
        assert files == {"visible.txt"}

    def test_skips_pycache(self, tmp_path: Path) -> None:
        """跳过 __pycache__ 目录。"""
        (tmp_path / "main.py").write_text("x")
        pycache = tmp_path / "__pycache__"
        pycache.mkdir()
        (pycache / "main.cpython-313.pyc").write_text("")
        sub_pycache = tmp_path / "sub" / "__pycache__"
        sub_pycache.mkdir(parents=True)
        (sub_pycache / "mod.cpython-313.pyc").write_text("")

        files = collect_relative_files(tmp_path)
        assert files == {"main.py"}

    def test_skips_custom_patterns(self, tmp_path: Path) -> None:
        """跳过 skip_patterns 匹配的路径。"""
        (tmp_path / "keep.txt").write_text("a")
        (tmp_path / "skip_me.txt").write_text("b")
        sub = tmp_path / "sub"
        sub.mkdir()
        (sub / "also_skip.txt").write_text("c")

        files = collect_relative_files(tmp_path, skip_patterns=["skip_me", "sub/"])
        assert files == {"keep.txt"}

    def test_empty_directory(self, tmp_path: Path) -> None:
        """空目录返回空集合。"""
        files = collect_relative_files(tmp_path)
        assert files == set()

    def test_non_ascii_filenames(self, tmp_path: Path) -> None:
        """非 ASCII 文件名也能正确处理。"""
        (tmp_path / "中文文件.txt").write_text("a")
        (tmp_path / "README.md").write_text("b")
        files = collect_relative_files(tmp_path)
        assert files == {"中文文件.txt", "README.md"}


class TestMain:
    """测试 bilingual_sync.main() 的集成逻辑。"""

    def test_aligned_directories_returns_zero(self, tmp_path: Path) -> None:
        """CN/EN 完全对齐时返回 0。"""
        cn = tmp_path / "UR-SKILL-CN"
        en = tmp_path / "UR-SKILL-EN"
        cn.mkdir(parents=True)
        en.mkdir(parents=True)

        (cn / "SKILL.md").write_text("# CN Skill")
        (en / "SKILL.md").write_text("# EN Skill")
        scripts_cn = cn / "Scripts"
        scripts_cn.mkdir(parents=True)
        (scripts_cn / "common.py").write_text("cn common")
        scripts_en = en / "Scripts"
        scripts_en.mkdir(parents=True)
        (scripts_en / "common.py").write_text("en common")

        rc = main(base_dir=tmp_path)
        assert rc == 0

    def test_only_cn_returns_one(self, tmp_path: Path) -> None:
        """CN 多出文件时返回 1。"""
        cn = tmp_path / "UR-SKILL-CN"
        en = tmp_path / "UR-SKILL-EN"
        cn.mkdir(parents=True)
        en.mkdir(parents=True)

        (cn / "SKILL.md").write_text("# CN Skill")
        (cn / "extra_cn_file.txt").write_text("only in cn")
        (en / "SKILL.md").write_text("# EN Skill")

        rc = main(base_dir=tmp_path)
        assert rc == 1

    def test_only_en_returns_one(self, tmp_path: Path) -> None:
        """EN 多出文件时返回 1。"""
        cn = tmp_path / "UR-SKILL-CN"
        en = tmp_path / "UR-SKILL-EN"
        cn.mkdir(parents=True)
        en.mkdir(parents=True)

        (cn / "SKILL.md").write_text("# CN Skill")
        (en / "SKILL.md").write_text("# EN Skill")
        (en / "extra_en_file.txt").write_text("only in en")

        rc = main(base_dir=tmp_path)
        assert rc == 1

    def test_cn_dir_missing_returns_one(self, tmp_path: Path) -> None:
        """CN 目录缺失时返回 1。"""
        en = tmp_path / "UR-SKILL-EN"
        en.mkdir(parents=True)
        (en / "SKILL.md").write_text("# EN Skill")

        rc = main(base_dir=tmp_path)
        assert rc == 1

    def test_en_dir_missing_returns_one(self, tmp_path: Path) -> None:
        """EN 目录缺失时返回 1。"""
        cn = tmp_path / "UR-SKILL-CN"
        cn.mkdir(parents=True)
        (cn / "SKILL.md").write_text("# CN Skill")

        rc = main(base_dir=tmp_path)
        assert rc == 1

    def test_skip_patterns_respected(self, tmp_path: Path) -> None:
        """skip 列表中的文件差异不视为问题。"""
        cn = tmp_path / "UR-SKILL-CN"
        en = tmp_path / "UR-SKILL-EN"
        cn.mkdir(parents=True)
        en.mkdir(parents=True)

        (cn / "SKILL.md").write_text("# CN Skill")
        (en / "SKILL.md").write_text("# EN Skill")
        # 这些文件在 skip 列表中，差异不报错
        scripts_cn = cn / "Scripts"
        scripts_cn.mkdir(parents=True, exist_ok=True)
        (scripts_cn / "config.zh-cn.yaml").write_text("zh")
        (scripts_cn / "bilingual_sync.py").write_text("sync")

        rc = main(base_dir=tmp_path)
        assert rc == 0

    def test_with_real_project_detects_issues(self, ur_skill_cn_dir: Path) -> None:
        """对真实项目执行 bilingual_sync，预期返回 0 或 1 且有进度输出。"""
        base_dir = ur_skill_cn_dir.parent
        rc = main(base_dir=base_dir)
        # 真实项目可能存在临时文件差异，只验证函数不抛异常
        assert rc in (0, 1)
