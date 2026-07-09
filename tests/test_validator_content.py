"""测试 validator_content.py。"""

import copy
from pathlib import Path

import pytest

from common import SkillContext
import validator_content


class TestFirstPerson:
    def test_detects_wo(self, zh_config) -> None:
        text = """---
name: my-skill
description: 用于测试的 SKILL
type: prompt
whenToUse: 测试时
metadata:
  updated: "2025-01-15"
---

我觉得这个应该这样做
"""
        ctx = SkillContext(text=text, path=Path("/fake/SKILL.md"), config=zh_config)
        findings = validator_content._validate_first_person(ctx, zh_config)
        assert any(f.rule == "first-person" for f in findings)

    def test_no_first_person(self, zh_config) -> None:
        text = """---
name: my-skill
description: 用于测试的 SKILL
type: prompt
whenToUse: 测试时
metadata:
  updated: "2025-01-15"
---

你应该这样做
"""
        ctx = SkillContext(text=text, path=Path("/fake/SKILL.md"), config=zh_config)
        findings = validator_content._validate_first_person(ctx, zh_config)
        assert not any(f.rule == "first-person" for f in findings)

    def test_first_person_in_description(self, zh_config) -> None:
        text = """---
name: my-skill
description: 我觉得这是一个很好的 SKILL
type: prompt
whenToUse: 测试
metadata:
  updated: "2025-01-15"
---

body
"""
        ctx = SkillContext(text=text, path=Path("/fake/SKILL.md"), config=zh_config)
        findings = validator_content._validate_first_person(ctx, zh_config)
        assert any(f.rule == "first-person-description" for f in findings)

    def test_wo_in_code_block_filtered(self, zh_config) -> None:
        """'我' 在代码块中应被过滤，不触发。"""
        text = """---
name: my-skill
description: 用于测试 代码块过滤的 SKILL
type: prompt
whenToUse: 测试时
metadata:
  updated: "2025-01-15"
---

看一下这段代码：
```python
# 我觉得这里可以优化
x = 1
```
"""
        ctx = SkillContext(text=text, path=Path("/fake/SKILL.md"), config=zh_config)
        findings = validator_content._validate_first_person(ctx, zh_config)
        assert not any(f.rule == "first-person" for f in findings)


class TestRFC2119:
    def test_rules_block_with_rfc2119(self, zh_config) -> None:
        config = copy.deepcopy(zh_config)
        config["rules"]["rules_heading_pattern"] = r"^#{2,3}\s*(?:\d+\.?\s*)?\S*[Rr]ules\S*"
        text = """---
name: my-skill
description: 用于测试 RFC2119 规则检查的 SKILL
type: prompt
whenToUse: 测试
metadata:
  updated: "2025-01-15"
---

## Rules

- MUST 使用前检查
- SHOULD 保持简洁
"""
        ctx = SkillContext(text=text, path=Path("/fake/SKILL.md"), config=config)
        findings = validator_content._validate_rfc2119(ctx, config)
        assert not any(f.rule == "rule-no-rfc2119" for f in findings)
        assert not any(f.rule == "rules-block-not-found" for f in findings)

    def test_rule_without_rfc2119(self, zh_config) -> None:
        config = copy.deepcopy(zh_config)
        config["rules"]["rules_heading_pattern"] = r"^#{2,3}\s*(?:\d+\.?\s*)?\S*[Rr]ules\S*"
        text = """---
name: my-skill
description: 用于测试 RFC2119 规则检查的 SKILL
type: prompt
whenToUse: 测试
metadata:
  updated: "2025-01-15"
---

## Rules

- 使用前要检查
- 保持简洁
"""
        ctx = SkillContext(text=text, path=Path("/fake/SKILL.md"), config=config)
        findings = validator_content._validate_rfc2119(ctx, config)
        assert any(f.rule == "rule-no-rfc2119" for f in findings)

    def test_no_rules_block(self, zh_config) -> None:
        config = copy.deepcopy(zh_config)
        config["rules"]["rules_heading_pattern"] = r"^#{2,3}\s*(?:\d+\.?\s*)?\S*[Rr]ules\S*"
        text = """---
name: my-skill
description: 一个没有 Rules 块的 SKILL 用于测试规则区块缺失检测逻辑是否正确
type: prompt
whenToUse: 测试
metadata:
  updated: "2025-01-15"
---

## Workflow

body
"""
        ctx = SkillContext(text=text, path=Path("/fake/SKILL.md"), config=config)
        findings = validator_content._validate_rfc2119(ctx, config)
        assert any(f.rule == "rules-block-not-found" for f in findings)
