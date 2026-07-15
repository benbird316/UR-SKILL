"""Self-validation: both CN and EN SKILL.md must pass format, content and runtime checks.

白名单说明（known_errors）：
- 这些规则是我们自身 SKILL.md 的"设计使然"豁免项，不是因为代码有 bug。
- 任何新增的 error 都必须先判断：是真正的 regression，还是又一个设计豁免。
- 如果确实是设计使然，加到这里并写清楚原因。
"""

from __future__ import annotations

import pytest

from common import SkillContext
from config_loader import load_config
import validator_format
import validator_content
import validator_runtime


@pytest.mark.parametrize(
    "lang, ur_skill_dir, ur_skill_text, scripts_dir_fixture",
    [
        pytest.param("zh-cn", "ur_skill_cn_dir", "ur_skill_cn_text", "scripts_dir", id="zh-cn"),
        pytest.param("en-us", "ur_skill_en_dir", "ur_skill_en_text", "en_scripts_dir", id="en-us"),
    ],
)
def test_format_self_validation(lang, ur_skill_dir, ur_skill_text, scripts_dir_fixture, request):
    """SKILL.md passes format validation (except known pre-existing issues)."""
    skill_dir = request.getfixturevalue(ur_skill_dir)
    text = request.getfixturevalue(ur_skill_text)
    scripts = request.getfixturevalue(scripts_dir_fixture)
    config = load_config(lang, scripts)
    ctx = SkillContext(text=text, path=skill_dir / "SKILL.md", config=config)
    findings = ctx.run(validator_format.validate)

    # known_errors 说明：
    #   description-length : 元技能自身的描述需要列举使用场景，必然超过 300 字阈值
    #   placeholder-residue: 元技能的工具标记（如 [SKILL]）被正则误判为未替换占位符
    #   body-too-long      : 元技能 13 步工作流 + 完整规则体系必然超过 500 行阈值
    known_errors = {"description-length", "placeholder-residue", "body-too-long"}
    errors = [f for f in findings if f.rule not in known_errors and f.severity == "error"]
    assert len(errors) == 0, f"[{lang}] New format errors: {[(e.rule, e.message[:80]) for e in errors]}"


@pytest.mark.parametrize(
    "lang, ur_skill_dir, ur_skill_text, scripts_dir_fixture",
    [
        pytest.param("zh-cn", "ur_skill_cn_dir", "ur_skill_cn_text", "scripts_dir", id="zh-cn"),
        pytest.param("en-us", "ur_skill_en_dir", "ur_skill_en_text", "en_scripts_dir", id="en-us"),
    ],
)
def test_content_self_validation(lang, ur_skill_dir, ur_skill_text, scripts_dir_fixture, request):
    """SKILL.md passes content validation (except known pre-existing issues)."""
    skill_dir = request.getfixturevalue(ur_skill_dir)
    text = request.getfixturevalue(ur_skill_text)
    scripts = request.getfixturevalue(scripts_dir_fixture)
    config = load_config(lang, scripts)
    ctx = SkillContext(text=text, path=skill_dir / "SKILL.md", config=config)
    findings = ctx.run(validator_content.validate)

    # known_errors 说明：
    #   first-person-description          : description 引用了用户请求中的"我"（如"帮我写一个skill"）,
    #                                       这是元技能描述的自然语言示例，非真实第一人称
    #   workflow-missing-dimension        : 工作流中的非关键节点（如"Why"解释步骤）不需要 6 维标注，
    #                                       正则扫描会误判这些节点缺少维度
    #   workflow-critical-missing-dimension: 同上，非关键节点不需要完整维度
    #   capability-workflow-confusion     : 元技能自身引用了能力架构概念（如 Capability Facets），
    #                                       正则无法区分"解释能力"和"定义能力"
    known_errors = {
        "first-person-description",
        "workflow-missing-dimension",
        "workflow-critical-missing-dimension",
        "capability-workflow-confusion",
    }
    errors = [f for f in findings if f.rule not in known_errors and f.severity == "error"]
    assert len(errors) == 0, f"[{lang}] New content errors: {[(e.rule, e.message[:80]) for e in errors]}"


@pytest.mark.parametrize(
    "lang, ur_skill_dir, ur_skill_text, scripts_dir_fixture",
    [
        pytest.param("zh-cn", "ur_skill_cn_dir", "ur_skill_cn_text", "scripts_dir", id="zh-cn"),
        pytest.param("en-us", "ur_skill_en_dir", "ur_skill_en_text", "en_scripts_dir", id="en-us"),
    ],
)
def test_runtime_self_validation(lang, ur_skill_dir, ur_skill_text, scripts_dir_fixture, request):
    """SKILL.md passes runtime validation (no known_errors needed — all rules enforced)."""
    skill_dir = request.getfixturevalue(ur_skill_dir)
    text = request.getfixturevalue(ur_skill_text)
    scripts = request.getfixturevalue(scripts_dir_fixture)
    config = load_config(lang, scripts)
    ctx = SkillContext(text=text, path=skill_dir / "SKILL.md", config=config)
    findings = ctx.run(validator_runtime.validate)

    errors = [f for f in findings if f.severity == "error"]
    assert len(errors) == 0, f"[{lang}] Runtime errors: {[(e.rule, e.message[:80]) for e in errors]}"
