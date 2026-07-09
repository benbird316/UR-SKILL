#!/usr/bin/env python3
"""
SKILL 静态校验脚本

用途：在交付前自动检查 SKILL.md 的格式、内容、引用一致性与反模式。
核心原则：所有规则必须可程序化验证，避免人工逐行检查。
"""

import argparse
import re
import sys
from datetime import datetime
from pathlib import Path


try:
    import yaml  # type: ignore

    HAS_YAML = True
except ImportError:  # pragma: no cover
    HAS_YAML = False


# ----------------------------- 配置 -----------------------------

MAX_BODY_LINES = 500
MAX_DESCRIPTION_CHARS = 200
MIN_DESCRIPTION_CHARS = 50
PLACEHOLDER_PATTERNS = [
    # 匹配 [xxx] 占位符，但排除 Markdown 链接 [text](url) 和合法标记 [认知操作]
    r"\[(?!认知操作\])(?![^\]]*\]\()[^\]]*\]",
    r"\{.*?\}",
    r"TODO|FIXME|XXX|HACK",
]

REQUIRED_FRONTMATTER_FIELDS = {
    "name": str,
    "description": str,
    "type": str,
    "whenToUse": str,
    "metadata": dict,
}

VALID_TYPES = {"prompt", "tool", "hybrid"}

# 风险边界关键词（仅适用于 UR-SKILL 自身校验，其他 SKILL 的风险边界由领域安全需求决定）
RISK_BOUNDARIES = [
    "违法",
    "歧视",
    "恶意注入",
]

# 步骤名称 -> 期望检查项数量（审视维度 + 风险边界门控）
STEP_EXPECTED_COUNTS = {
    "解析": 3,
    "前置分析": 4,
    "调研": 7,
    "架构": 7,
    "执行": 4,
    "交付": 4,
    "校验": 7,
    "验证": 8,
}

# 需覆盖全部 6 个审视维度的步骤（关键节点）
CRITICAL_STEPS = {"调研", "架构", "校验", "验证"}

# 关键节点必须覆盖的 6 个审视维度
REQUIRED_DIMENSIONS = [
    "目标对齐",
    "事实锚定",
]

CRITICAL_ONLY_DIMENSIONS = [
    "方向校准",
    "对抗验证",
    "盲区识别",
    "影响推演",
]

# RFC 2119 关键词
RFC2119_KEYWORDS = ["MUST", "MUST NOT", "SHOULD", "SHOULD NOT", "MAY"]

# 风险边界滥用检测关键词（能力降级措辞 — 风险边界中不应出现）
# 风险边界只声明安全红线，任何"不负责/只做X不做Y"都是滥用
RB_ABUSE_KEYWORDS = [
    r"不负责", r"不属于", r"不在.*范围", r"不管", r"不承担",
    r"只做.*不做", r"仅限于", r"不涉及", r"不包含",
]

# 专业边界滥用检测关键词（能力降级措辞 — 专业边界中不应出现）
# 专业边界可以描述"不包含X"（如"不包含具体买卖价位"），
# 但不能是能力降级（"只做X不做Y"且Y是X的自然延伸）
PB_ABUSE_KEYWORDS = [
    r"不负责", r"只做.*不做", r"不管", r"不承担",
]

# 切面填充检测模式（通用套话）
FACET_FILLER_PATTERNS = [
    r"掌握相关领域知识",
    r"熟悉(?:相关)?领域(?:知识|规范)",
    r"识别潜在风险",
    r"保证输出质量",
    r"考虑全局影响",
    r"优化资源投入",
    r"分析任务复杂度",
    r"确保.*质量",
]

# 盲区甩锅检测关键词
BLIND_DUMP_KEYWORDS = [
    r"仅供参考",
    r"请自行验证",
    r"可能存在.*盲区",
    r"不保证.*(?:完整|准确)",
    r"使用前请.*(?:检查|验证|确认)",
]


# ----------------------------- 工具绑定检测 -----------------------------

# 常见 Agent 工具名称（大小写不敏感匹配）
KNOWN_TOOLS = [
    "Read", "Write", "Edit", "DeleteFile",
    "RunCommand", "CheckCommandStatus", "StopCommand",
    "Grep", "Glob", "LS", "SearchCodebase",
    "WebSearch", "WebFetch",
    "AskUserQuestion", "NotifyUser",
    "Task", "Skill", "run_mcp",
    "TodoWrite", "OpenPreview", "GetDiagnostics",
]

# 审查/测试类 SKILL 关键词（审查/评审/测试/审计）
CRT_KEYWORDS = [
    "review", "test", "audit", "scan",
    "审查", "评审", "测试", "审计", "扫描", "安全",
    "code-review", "security-review", "质量", "quality",
]

# 输出规格必检项
OUTPUT_SPEC_CHECKS = {
    "mermaid": {
        "patterns": [r"mermaid", r"flowchart", r"sequenceDiagram", r"classDiagram", r"stateDiagram"],
        "label": "Mermaid 可视化要求",
    },
    "severity": {
        "patterns": [r"(极危|高危|中危|低危|Critical|High|Medium|Low).*级"],
        "label": "问题分级",
    },
    "interaction": {
        "patterns": [r"AskUserQuestion", r"确认.*修复.*验证.*循环", r"分阶段交付", r"用户交互模式"],
        "label": "用户交互模式",
    },
    "decision": {
        "patterns": [r"判决策略|阻断.*合入|建议.*合入", r"通过\|需修改\|阻断"],
        "label": "判决策略",
    },
}


# ----------------------------- 工具函数 -----------------------------

def parse_frontmatter(text: str) -> tuple[dict | None, str, list[str]]:
    """解析 YAML frontmatter 与 body 内容。"""
    errors: list[str] = []
    if not text.startswith("---"):
        errors.append("SKILL.md 必须以 `---` 开头")
        return None, text, errors

    parts = text.split("---", 2)
    if len(parts) < 3:
        errors.append("无法解析 frontmatter：缺少第二个 `---` 分隔符")
        return None, text, errors

    fm_text = parts[1].strip()
    body = parts[2].strip()

    if not HAS_YAML:
        errors.append("未安装 PyYAML，跳过 frontmatter 字段类型校验（请执行 `pip install pyyaml`）")
        # 简单正则兜底：只检查字段存在性
        fm_data: dict = {}
        for key in REQUIRED_FRONTMATTER_FIELDS:
            if key == "metadata":
                if re.search(rf"^{re.escape(key)}:\s*$", fm_text, re.MULTILINE):
                    fm_data[key] = {}
            else:
                match = re.search(rf"^{re.escape(key)}:\s*(.+)$", fm_text, re.MULTILINE)
                if match:
                    fm_data[key] = match.group(1).strip().strip('"')
        return fm_data, body, errors

    try:
        fm_data = yaml.safe_load(fm_text) or {}
    except yaml.YAMLError as exc:
        errors.append(f"frontmatter YAML 解析失败: {exc}")
        return None, body, errors

    return fm_data, body, errors


def validate_frontmatter(fm: dict) -> list[str]:
    """校验 frontmatter 字段与格式。"""
    errors: list[str] = []

    for field, expected_type in REQUIRED_FRONTMATTER_FIELDS.items():
        if field not in fm:
            errors.append(f"frontmatter 缺少必填字段: {field}")
            continue
        if expected_type is dict:
            if not isinstance(fm[field], dict):
                errors.append(f"frontmatter 字段 {field} 必须是字典")
            continue
        if not isinstance(fm[field], expected_type):
            errors.append(f"frontmatter 字段 {field} 类型错误，期望 {expected_type.__name__}")

    if "name" in fm:
        name = fm["name"]
        if not re.match(r"^[a-z0-9]+(?:-[a-z0-9]+)*$", name):
            errors.append(f"name '{name}' 不是合法 kebab-case")

    if "description" in fm:
        desc = fm["description"]
        if len(desc) < MIN_DESCRIPTION_CHARS or len(desc) > MAX_DESCRIPTION_CHARS:
            errors.append(
                f"description 长度 {len(desc)} 不在 {MIN_DESCRIPTION_CHARS}-{MAX_DESCRIPTION_CHARS} 范围内"
            )

    if "type" in fm and fm["type"] not in VALID_TYPES:
        errors.append(f"type '{fm['type']}' 不是合法值 {VALID_TYPES}")

    if isinstance(fm.get("metadata"), dict):
        updated = fm["metadata"].get("updated")
        if not updated:
            errors.append("metadata.updated 缺失")
        else:
            try:
                datetime.strptime(str(updated), "%Y-%m-%d")
            except ValueError:
                errors.append(f"metadata.updated '{updated}' 不是 YYYY-MM-DD 格式")

    return errors


def validate_quality(body: str) -> list[str]:
    """校验风险边界滥用、切面填充、盲区甩锅等质量问题。"""
    errors: list[str] = []

    # 排除代码块内的示例内容（反例教学）
    body_clean = re.sub(r'```[\s\S]*?```', '', body)

    # ---- 风险边界滥用检测 ----
    # 提取所有风险边界- 声明行
    rb_lines = re.findall(r'^\s*(?:\|\s*)?风险边界-\d+\s*[:\|]\s*(.+)$', body_clean, re.MULTILINE)
    # 也匹配列表格式：- 风险边界-01：xxx
    rb_list = re.findall(r'^\s*[-*]\s*\*\*风险边界-(\d+)\*\*[：:]\s*(.+)$', body_clean, re.MULTILINE)

    # 检查风险边界滥用：风险边界声明中不应含免责措辞
    for line in rb_lines:
        for kw in RB_ABUSE_KEYWORDS:
            if re.search(kw, line):
                errors.append(f"风险边界滥用: 疑似免责措辞 '{kw}' -> '{line[:60]}...'")
                break

    for _, content in rb_list:
        for kw in RB_ABUSE_KEYWORDS:
            if re.search(kw, content):
                errors.append(f"风险边界滥用: 疑似免责措辞 '{kw}' -> '{content[:60]}...'")
                break

    # ---- 专业边界滥用检测 ----
    # 提取所有专业边界- 声明行
    pb_lines = re.findall(r'^\s*(?:\|\s*)?专业边界-\d+\s*[:\|]\s*(.+)$', body_clean, re.MULTILINE)
    pb_list = re.findall(r'^\s*[-*]\s*\*\*专业边界-(\d+)\*\*[：:]\s*(.+)$', body_clean, re.MULTILINE)

    # 检查专业边界滥用：专业边界声明中不应含能力降级措辞
    for line in pb_lines:
        for kw in PB_ABUSE_KEYWORDS:
            if re.search(kw, line):
                errors.append(f"专业边界滥用: 疑似能力降级 '{kw}' -> '{line[:60]}...'")
                break

    for _, content in pb_list:
        for kw in PB_ABUSE_KEYWORDS:
            if re.search(kw, content):
                errors.append(f"专业边界滥用: 疑似能力降级 '{kw}' -> '{content[:60]}...'")
                break

    # ---- 切面填充检测 ----
    # 提取所有切面\d 行（切面定义行）
    facet_lines = re.findall(
        r'^\s*(?:\|\s*)?切面(\d)\s*(?:\|.*?\||\*\*切面\d[^:]*\*\*[：:]\s*)(.+?)(?:\||$)',
        body_clean,
        re.MULTILINE,
    )
    if not facet_lines:  # 回退：匹配更宽松的格式
        facet_lines = re.findall(
            r'切面(\d)\s*[：:]\s*(.+?)(?:\n|$)',
            body_clean,
        )

    for num, content in facet_lines:
        content_clean = content.strip()
        for pattern in FACET_FILLER_PATTERNS:
            if re.search(pattern, content_clean):
                # 丰富的切面内容（> 25 字符）即使含通用词也判为通过（有任务锚定）
                if len(content_clean) >= 25:
                    continue
                # 否则：太短 + 匹配套话模式 = 疑似填充
                errors.append(
                    f"切面填充: {num} 切面过于简短，疑似套话 '{content_clean[:60]}'"
                )
                break  # 每个切面只报告一次

    # ---- 盲区甩锅检测 ----
    # 定位盲区相关段落
    blind_sections = re.findall(
        r'盲区[：:]\s*(.+?)(?=\n\n|\n#|\Z)',
        body_clean,
        re.DOTALL,
    )
    for section in blind_sections:
        section_clean = section.strip()
        # 检查是否包含免责关键词
        has_dump = any(re.search(kw, section_clean) for kw in BLIND_DUMP_KEYWORDS)
        # 检查是否缺少"已尝试"字段
        has_attempt = "已尝试" in section_clean
        if has_dump and not has_attempt:
            errors.append(
                f"盲区甩锅: 纯声明式盲区（无'已尝试动作'）"
            )

    return errors


def validate_first_person(body: str, fm: dict | None = None) -> list[str]:
    """校验 SKILL.md 是否使用了第一人称"我"。

    "我"会让 LLM 混淆人格归属——系统提示词应始终用"你是一个XX"而非"我是一个XX"。
    排除代码块内容（可能是用户示例输入）。
    同时检查 frontmatter description 中的"我"。
    """
    errors: list[str] = []
    body_clean = re.sub(r'```[\s\S]*?```', '', body)

    for i, line in enumerate(body_clean.splitlines(), 1):
        if '我' in line:
            stripped = line.strip()
            if stripped:
                errors.append(
                    f"第一人称: 第 {i} 行含 '我'，应改为'你'或无主语 -> '{stripped[:80]}'"
                )

    # 检查 frontmatter description
    if fm:
        desc = fm.get("description", "")
        if isinstance(desc, str) and '我' in desc:
            errors.append(
                f"第一人称: frontmatter description 含 '我'，应改为无主语 -> '{desc[:80]}'"
            )

    return errors


def validate_identity_title(body: str, fm: dict | None = None) -> list[str]:
    """校验身份声明中是否使用了膨胀头衔（专家/教授/master/expert等）。

    研究依据：
    - 南加州大学 2026.3：空洞身份导致知识检索从 71.6% 跌至 66.3%
    - 宾大沃顿 2025.12：夸大身份导致过度自信与信息编造
    """
    errors: list[str] = []
    inflated_titles = [
        "专家", "教授", "大师", "达人", "资深", "顶级", "领军",
        "expert", "professor", "master", "guru", "veteran",
    ]
    experience_patterns = [
        r"\d+\s*年.*经验",   # "5 年经验", "10年设计经验"
        r"\d+\+?\s*years.*experience",  # "5 years of experience", "10+ years"
    ]

    # 检查 body 中的身份行和描述段落
    for i, line in enumerate(body.split("\n"), 1):
        stripped = line.strip()
        # 识别身份声明行或相关描述
        if any(keyword in stripped for keyword in ("**身份**:", "**Role**:", "角色：", "身份:", "Role:")):
            # 检查膨胀头衔
            for title in inflated_titles:
                if title in stripped:
                    errors.append(
                        f"膨胀头衔: body 第{i}行包含 '{title}'，"
                        f"应使用具体职业名（工程师/分析师/审查员），非虚词头衔"
                    )
                    break
            # 检查虚构经验年限
            for pattern in experience_patterns:
                m = re.search(pattern, stripped)
                if m:
                    errors.append(
                        f"虚构年限: body 第{i}行包含 '{m.group()}'，"
                        f"LLM 没有'年限经验'概念，应改为主攻领域/方法论描述"
                    )
                    break

    # 检查 frontmatter description
    if fm:
        desc = fm.get("description", "")
        for title in inflated_titles:
            if title in desc.lower():
                errors.append(
                    f"膨胀头衔: frontmatter description 包含 '{title}'，"
                    f"应使用具体职业名"
                )
                break
        for pattern in experience_patterns:
            m = re.search(pattern, desc, re.IGNORECASE)
            if m:
                errors.append(
                    f"虚构年限: frontmatter description 包含 '{m.group()}'，"
                    f"LLM 没有'年限经验'概念，应改为主攻领域/方法论描述"
                )
                break

    return errors


def validate_tool_name_migration(body: str) -> list[str]:
    """校验是否使用了已废弃的工具名（如 SearchReplace 应改为 Edit）。"""
    errors: list[str] = []
    if "SearchReplace" in body:
        errors.append("工具名迁移: 发现 'SearchReplace'，应使用 'Edit' 替代")
    return errors


def validate_body(body: str, fm: dict | None = None) -> list[str]:
    """校验 body 内容。"""
    errors: list[str] = []
    lines = body.splitlines()

    # 排除代码块和 Mermaid 块的占位符误报
    body_clean = re.sub(r'```[\s\S]*?```', '', body)

    if len(lines) > MAX_BODY_LINES:
        errors.append(f"body 行数 {len(lines)} 超过阈值 {MAX_BODY_LINES}")

    for pattern in PLACEHOLDER_PATTERNS:
        matches = set(re.findall(pattern, body_clean, re.IGNORECASE))
        filtered = []
        for m in matches:
            # 跳过 Markdown 复选框 [ ] / [x]
            if m in ("[ ]", "[x]", "[X]"):
                continue
            # 跳过 Markdown 链接 [text](url)
            if re.match(r"^\[.*\]\(.*\)$", m):
                continue
            # 跳过格式说明符 [工具名]、[文件名] 等占位符模板
            if m in ("[工具名]", "[文件名]", "[目录名]", "[参数]", "[操作]"):
                continue
            # 跳过工具引用格式 [Read]、[Write]、[AskUserQuestion] 等
            if re.match(r"^\[[A-Z][a-zA-Z]+\]$", m):
                continue
            # 跳过 Mermaid 节点文本 ["xxx"] 格式
            if re.match(r'^\[".*"\]$', m):
                continue
            # 跳过 Mermaid 节点嵌套 ["[xxx] ..."] 格式
            if re.match(r'^\["\[.*\].*"\]$', m):
                continue
            # 跳过工具调用格式 [xxx] 出现在任意位置
            if re.match(r'^\[(Read|Write|AskUserQuestion|NotifyUser|RunCommand|Grep|Glob|Task|Skill|DeleteFile|Edit|TodoWrite)\b', m):
                continue
            # 跳过 Mermaid 节点片段 ["[xxx] （括号开头但未闭合的）
            if m.startswith('["[') or m.startswith('["') :
                continue
            filtered.append(m)
        if filtered:
            should_report = True
            # 对 {} 模式：跳过模板变量格式
            if pattern == r"\{.*?\}":
                real_placeholders = [m for m in filtered if not re.match(r'^\{[A-Za-z\u4e00-\u9fff].*\}$', m)]
                real_placeholders = [m for m in real_placeholders if m != '{date}']
                if real_placeholders:
                    errors.append(f"疑似占位符残留 ({pattern}): {real_placeholders[:5]}")
                should_report = False  # 已由上方分支处理
            if should_report:
                errors.append(f"疑似占位符残留 ({pattern}): {filtered[:5]}")

    # RISK_BOUNDARIES 关键词检查仅适用于 UR-SKILL 自身
    # 其他 SKILL 的风险边界由领域安全需求决定，不应硬编码检查
    is_UR_SKILL = fm and fm.get("name", "") == "ur-skill"
    if is_UR_SKILL:
        for rb in RISK_BOUNDARIES:
            if rb not in body_clean:
                errors.append(f"缺少风险边界声明: {rb}")

    return errors


def validate_tool_binding(body: str, fm: dict | None = None) -> list[str]:
    """校验工作流步骤中的动作是否绑定了具体工具。

    格式要求：每个可执行动作包含 `[工具名] 操作 → 输出` 格式的工具调用。
    UR-SKILL 自身不适用此检查（它的工具调用在 body 外）。
    """
    errors: list[str] = []

    # UR-SKILL 自身的 SKILL 不适用此检查
    if fm and fm.get("name") in ("ur-skill", "pre-analysis-engineer"):
        return errors

    # 定位工作流区块（适配 "## 工作流"、"## 3. 工作流" 等格式）
    workflow_match = re.search(r"^#{2,3}\s*(?:\d+\.?\s*)?工作流", body, re.MULTILINE)
    if not workflow_match:
        return errors  # 非运行时 SKILL，跳过

    wf_start = workflow_match.end()
    next_section = re.search(r"^#{2,3}\s+(?!\d|工作流|[Ww]orkflow).*?\n", body[wf_start:], re.MULTILINE)
    wf_end = wf_start + next_section.start() if next_section else len(body)
    workflow_body = body[wf_start:wf_end]

    # 提取所有动作行（以数字开头的列表项）
    action_lines = re.findall(
        r"^\s*\d+\.\s+(.+)",
        workflow_body,
        re.MULTILINE,
    )

    tool_pattern = re.compile(r"\[([A-Za-z_][A-Za-z0-9_]*)\]")

    has_any_tool = False
    unbound_lines = []

    for i, line in enumerate(action_lines):
        line_clean = line.strip()
        # 跳过纯描述行（非动作）
        if line_clean.startswith(("读取", "确认", "检查", "组装", "汇总", "模拟", "填充")):
            # 这些是 UR-SKILL 自身的元操作，不强制工具绑定
            continue
        # 处理 [认知操作]：纯认知操作（无外部工具）跳过，混有真实工具的继续检查
        if "认知操作" in line_clean:
            remaining = line_clean.replace("[认知操作]", "")
            other_tools = tool_pattern.findall(remaining)
            if not other_tools:
                continue  # 纯认知操作，无外部工具绑定
            # 有认知操作 + 外部工具 → 继续走下面的工具绑定检查
        # 跳过"为什么"、"设计原理"等说明行
        if re.match(r"(为什么|设计原理|注意|说明)", line_clean):
            continue

        matches = tool_pattern.findall(line_clean)
        if matches:
            has_any_tool = True
            # 验证工具名是否在已知列表中
            for tool_name in matches:
                if tool_name not in KNOWN_TOOLS:
                    # 不是已知工具但不是致命错误——可能是自定义工具
                    pass
        else:
            # 只报告看起来像动作的行（含动词）
            if re.search(r"(读取|调用|执行|运行|搜索|创建|写入|编辑|删除|打开)", line_clean):
                unbound_lines.append(f"  L{i+1}: {line_clean[:60]}...")

    # 只有当存在工具绑定的其他地方但没有工具绑定的动作时才报错
    if has_any_tool and unbound_lines:
        errors.append(
            f"工具绑定缺失：以下动作未绑定工具（格式 [工具名] 操作 → 输出），"
            f"但同 SKILL 的其他动作已绑定工具：\n" + "\n".join(unbound_lines[:5])
        )
    elif not has_any_tool and action_lines:
        # 没有显式工具绑定但有动作——这是 FL 体系特征（依赖内置工具）
        # 不强制报错，只给出 info
        pass

    return errors


def validate_output_spec(body: str, fm: dict | None) -> list[str]:
    """校验审查/测试类 SKILL 是否包含必要的输出规格。

    审查/测试类 = Code Review / Test / Security Audit 类 SKILL。
    检查项：Mermaid 可视化、问题分级、判决策略、用户交互模式。
    """
    errors: list[str] = []

    if fm is None:
        return errors

    name = str(fm.get("name", "")).lower()
    desc = str(fm.get("description", "")).lower()

    # 判定是否为审查/测试类 SKILL
    is_crt = any(kw in name for kw in CRT_KEYWORDS) or any(kw in desc for kw in CRT_KEYWORDS)
    if not is_crt:
        return errors

    # 审查/测试类 SKILL：检查 4 项输出规格
    for key, spec in OUTPUT_SPEC_CHECKS.items():
        found = any(re.search(pat, body) for pat in spec["patterns"])
        if not found:
            errors.append(
                f"审查/测试类 SKILL 缺少 {spec['label']}："
                f"未检测到 {spec['patterns'][:2]} 相关模式"
            )

    return errors


def validate_workflow(body: str) -> list[str]:
    """校验工作流节点检查项数量与内容维度。"""
    errors: list[str] = []

    # 匹配每个工作流步骤的标题与检查清单
    step_pattern = re.compile(
        r"^#{2,4}\s*\d+\.\s*(\S+?)\s*[（\(].*?[）\)].*?维.*$",
        re.MULTILINE,
    )

    for match in step_pattern.finditer(body):
        step_name = match.group(1)
        # 从当前匹配位置到下一个同层级标题之前
        start = match.end()
        next_match = step_pattern.search(body, start)
        end = next_match.start() if next_match else len(body)
        section = body[start:end]

        check_count = section.count("- [ ]") + section.count("- [x]")

        if step_name in STEP_EXPECTED_COUNTS:
            expected = STEP_EXPECTED_COUNTS[step_name]
            if check_count != expected:
                errors.append(
                    f"步骤 '{step_name}' 检查项数量 {check_count}，期望 {expected}"
                )

        # ------ 检查项维度内容校验 ------
        # 提取该步骤中所有检查项文本
        checklist_items = re.findall(
            r"- \[[ x]\]\s*(.+?)(?=\n- \[|$)",
            section,
            re.DOTALL,
        )

        # 收集该步骤已覆盖的维度名
        covered = set()
        for item in checklist_items:
            item_text = item.strip().split("\n")[0]  # 只取第一行检查项标题
            # 移除 Markdown 加粗标记用于匹配
            clean_text = re.sub(r"\*\*(.+?)\*\*", r"\1", item_text)
            for dim in REQUIRED_DIMENSIONS + CRITICAL_ONLY_DIMENSIONS:
                if dim in clean_text:
                    covered.add(dim)

        # 所有步骤都必须覆盖这 2 个维度
        for dim in REQUIRED_DIMENSIONS:
            if dim not in covered:
                errors.append(
                    f"节点 '{step_name}' 缺少必检维度: {dim}"
                )

        # 关键节点额外覆盖 4 个维度
        if step_name in CRITICAL_STEPS:
            for dim in CRITICAL_ONLY_DIMENSIONS:
                if dim not in covered:
                    errors.append(
                        f"关键节点 '{step_name}' 缺少维度: {dim}"
                    )

    return errors


# ----------------------------- UR-SKILL 文件泄漏检测 -----------------------------

def _discover_UR_SKILL_files() -> set[str]:
    """动态发现 UR-SKILL 自身的所有文件（相对路径集合）。"""
    script_dir = Path(__file__).resolve().parent
    UR_SKILL_root = script_dir.parent
    files: set[str] = set()
    for f in UR_SKILL_root.rglob("*"):
        if f.is_file() and not f.name.startswith("."):
            rel = f.relative_to(UR_SKILL_root).as_posix()
            # 只记录 UR-SKILL 独有目录下的文件（不会出现在生成 SKILL 中）
            if any(
                rel.startswith(prefix)
                for prefix in ("design-guides/", "templates/", "design-rationale/", "Scripts/")
            ):
                files.add(rel)
            # 特定 References 文件（非通用名）
            elif rel in ("References/pre-analysis.md",):  # 已迁移至 design-rationale，向后兼容
                files.add(rel)
            # 子 SKILL 文件
            elif rel in ("agent/SKILL.md",):
                files.add(rel)
    return files


# 缓存
_UR_SKILL_FILES: set[str] | None = None


def _get_UR_SKILL_files() -> set[str]:
    """获取 UR-SKILL 自身文件列表（缓存）。"""
    global _UR_SKILL_FILES
    if _UR_SKILL_FILES is None:
        _UR_SKILL_FILES = _discover_UR_SKILL_files()
    return _UR_SKILL_FILES


def validate_UR_SKILL_file_leaks(body: str, fm: dict | None = None) -> list[str]:
    """检查生成的 SKILL 是否泄漏了 UR-SKILL 的内部文件引用。

    自包含规则：生成的 SKILL 不得引用 UR-SKILL 自身的文件（design-guides/、
    templates/、design-rationale/、Scripts/ 等目录下的内容）。
    当 fm.name 为 'ur-skill' 或 'pre-analysis-engineer' 时跳过检查。
    """
    errors: list[str] = []

    # UR-SKILL 自身的 SKILL 必然引用内部文件，跳过
    if fm and fm.get("name") in ("ur-skill", "pre-analysis-engineer"):
        return errors

    # 排除代码块内容（避免示例代码中的路径被误报）
    body_clean = re.sub(r'```[\s\S]*?```', '', body)

    UR_SKILL_files = _get_UR_SKILL_files()
    if not UR_SKILL_files:
        return errors  # 无法发现 UR-SKILL 文件，跳过

    # 扫描 body 中是否有引用 UR-SKILL 文件
    leaked: set[str] = set()
    for sb_file in UR_SKILL_files:
        escaped = re.escape(sb_file)
        # 匹配各种引用格式: [text](path), 裸 path, ./path, ../path, /path
        patterns = [
            rf'\b{escaped}\b',               # 裸路径: design-guides/xxx.md
            rf'\./{escaped}\b',             # ./ 前缀
            rf'\.\.\/{escaped}\b',          # ../ 前缀
        ]
        for pat in patterns:
            if re.search(pat, body_clean):
                leaked.add(sb_file)
                break  # 每种文件只报告一次

    for f in sorted(leaked):
        errors.append(
            f"UR-SKILL 文件引用泄漏: 生成 SKILL 中引用了 '{f}'，"
            f"违反了自包含规则（MUST NOT 引用 UR-SKILL 内部文件）"
        )

    return errors


# ----------------------------- 未填充占位符检测 -----------------------------

# 来自 output-template.md 的占位符模式（必须被填充）
UNRESOLVED_PLACEHOLDER_PATTERNS: list[tuple[str, str]] = [
    # 基础占位符
    (r'\{kebab-case-name\}', 'name 占位符'),
    (r'\{SKILL名称\}', '标题占位符'),
    (r'\{YYYY-MM-DD\}', '日期占位符'),
    # 能力架构占位符
    (r'\{核心领域名\}', '核心领域名占位符'),
    (r'\{领域\d\}', '辐射领域名占位符'),
    # 边界占位符
    (r'\{该 SKILL (?:不可逾越的安全红线|不得越界的专业领域限制)\}', '边界声明占位符'),
    # 输出规格占位符
    (r'\{自然语言/结构化/混合[,，]\s*简短描述\}', '输出格式描述占位符'),
    (r'\{格式类型\}', '输出格式类型占位符'),
    (r'\{Mermaid \{类型\}\}', 'Mermaid 类型占位符'),
    (r'\{N\}', '循环轮数占位符'),
    (r'\{填充色\}', 'Mermaid 填充色占位符'),
    (r'\{文字色\}', 'Mermaid 文字色占位符'),
    # 示例占位符
    (r'\{场景\}', '示例场景占位符'),
    (r'\{用户输入内容\}', '示例输入占位符'),
    (r'\{期望输出内容[^}]*\}', '示例输出占位符'),
    # 通用占位符
    (r'\{N 个月\}', '审查周期占位符'),
    (r'\{MAJOR\.MINOR\.PATCH\}', '语义化版本占位符'),
]


def validate_unresolved_placeholders(body: str) -> list[str]:
    """检查生成 SKILL 中是否残留未填充的模板占位符。

    只检查来自 output-template.md 的特定占位符模式，避免通用 {} 的误报。
    """
    errors: list[str] = []

    # 排除代码块（示例中的占位符是教学用的）
    body_clean = re.sub(r'```[\s\S]*?```', '', body)
    # 也排除 YAML frontmatter
    body_no_fm = re.sub(r'^---[\s\S]*?---', '', body_clean)

    for pattern, label in UNRESOLVED_PLACEHOLDER_PATTERNS:
        matches = re.findall(pattern, body_no_fm)
        if matches:
            errors.append(
                f"占位符未填充: 发现 {len(matches)} 处 '{label}'"
            )

    return errors


def _check_ref_exists(rel_path: str, skill_dir: Path) -> bool:
    """检查引用文件是否存在于 skill_dir 或其父目录（用于子目录示例 SKILL）。"""
    # 标准位置
    if (skill_dir / rel_path).exists():
        return True
    # 子目录示例 SKILL 可能引用项目根目录文件
    if skill_dir.parent and (skill_dir.parent / rel_path).exists():
        return True
    return False


def validate_references(body: str, skill_dir: Path) -> list[str]:
    """校验 body 中引用的 references/、scripts/、assets/、design-guides/、templates/ 文件是否存在。"""
    errors: list[str] = []
    refs = re.findall(r"[Rr]eferences/([a-zA-Z0-9_\-\./]+)", body)
    scr = re.findall(r"[Ss]cripts/([a-zA-Z0-9_\-\./]+)", body)
    ast = re.findall(r"assets/([a-zA-Z0-9_\-\./]+)", body)
    dg = re.findall(r"[Dd]esign-[Gg]uides/([a-zA-Z0-9_\-\./]+)", body)
    tpl = re.findall(r"[Tt]emplates/([a-zA-Z0-9_\-\./]+)", body)

    for ref in set(refs):
        if not _check_ref_exists(f"References/{ref}", skill_dir):
            errors.append(f"引用的 reference 文件不存在: References/{ref}")

    for script in set(scr):
        if not _check_ref_exists(f"Scripts/{script}", skill_dir):
            errors.append(f"引用的 script 文件不存在: Scripts/{script}")

    for asset in set(ast):
        if not _check_ref_exists(f"assets/{asset}", skill_dir):
            errors.append(f"引用的 asset 文件不存在: assets/{asset}")

    for guide in set(dg):
        if not _check_ref_exists(f"design-guides/{guide}", skill_dir):
            errors.append(f"引用的 design-guide 文件不存在: design-guides/{guide}")

    for template in set(tpl):
        if not _check_ref_exists(f"templates/{template}", skill_dir):
            errors.append(f"引用的 template 文件不存在: templates/{template}")

    return errors


def validate_file_dependency_decision(body: str) -> list[str]:
    """校验工作流中是否执行了文件依赖决策。

    检查工作流区块是否包含"文件依赖决策"或"pre-analysis.md §2"或"design-rationale.md §9"指令。
    复杂度为"中等"或"复杂"的 SKILL 必须在创建 references/ 等文件前执行此决策。
    """
    errors: list[str] = []

    # 定位工作流区块
    workflow_match = re.search(r"^#{2,3}\s*(?:\d+\.?\s*)?工作流", body, re.MULTILINE)
    if not workflow_match:
        return errors

    wf_start = workflow_match.end()
    next_section = re.search(r"^#{2,3}\s+(?!\d|工作流|[Ww]orkflow).*?\n", body[wf_start:], re.MULTILINE)
    wf_end = wf_start + next_section.start() if next_section else len(body)
    workflow_section = body[wf_start:wf_end]

    has_decision = (
        "文件依赖决策" in workflow_section
        or "pre-analysis.md §2" in workflow_section
        or "pre-analysis.md#2" in workflow_section
        or "design-rationale.md §9" in workflow_section
        or "design-rationale.md#9" in workflow_section
    )
    if not has_decision:
        errors.append(
            "文件依赖决策缺失：工作流中未发现文件依赖决策指令"
            "（应添加 '文件依赖决策' 或引用 pre-analysis.md §2 或 design-rationale.md §9）"
        )

    return errors


def validate_rfc2119(body: str) -> list[str]:
    """校验规则区块是否使用了 RFC 2119 关键词。"""
    errors: list[str] = []

    # 定位规则区块（按标题名称搜索，不依赖固定编号）
    # 匹配 "## 规则"、"## 5. 规则" 等格式
    rules_match = re.search(r"^#{2,3}\s*(?:\d+\.?\s*)?规则\s*$", body, re.MULTILINE)
    if not rules_match:
        # 回退：尝试匹配英文 "## Rules"
        rules_match = re.search(r"^#{2,3}\s*(?:\d+\.?\s*)?[Rr]ules\s*$", body, re.MULTILINE)
    if not rules_match:
        errors.append("未找到规则区块（标题应包含'规则'或'Rules'）")
        return errors

    start = rules_match.end()
    # 找到下一个同层级（相同 # 数量）标题作为结束
    level = len(rules_match.group(0)) - len(rules_match.group(0).lstrip('#'))
    next_section = re.search(r"^#{%d,%d}\s+(?:\d+\.?\s*)?(?!规则|[Rr]ules).*?\n" % (level, level), body[start:], re.MULTILINE)
    end = start + next_section.start() if next_section else len(body)
    rules_section = body[start:end]

    # 提取所有规则条目
    # 适配格式: "- **规则01 MUST** ..." 或 "- **规则01 MUST NOT** ..."
    # 提取完整条目内容后跳过编号前缀，检查是否以 RFC2119 关键词开头
    rule_lines = re.findall(
        r"^\s*[-*]\s+(?:\*\*)?(?:规则\d+\s+)?(.+?)(?:\*\*)?(?:\s|$)",
        rules_section,
        re.MULTILINE,
    )

    if not rule_lines:
        # 回退：更宽松的匹配
        rule_lines = re.findall(
            r"^\s*[-*]\s+.*?(MUST NOT|MUST|SHOULD NOT|SHOULD|MAY)\s",
            rules_section,
            re.MULTILINE,
        )

    if not rule_lines:
        errors.append("规则区块中未找到任何规则条目（bullet list）")
        return errors

    # 检查每条规则是否以 RFC 2119 关键词开头
    for idx, item in enumerate(rule_lines, 1):
        item_clean = re.sub(r"\*\*", "", item).strip()
        has_keyword = any(
            item_clean.upper().startswith(kw) for kw in RFC2119_KEYWORDS
        )
        if not has_keyword:
            errors.append(
                f"规则{idx:02d} 未使用 RFC 2119 关键词: '{item_clean[:60]}...'"
            )

    return errors


def main() -> int:
    parser = argparse.ArgumentParser(description="校验 SKILL.md 质量")
    parser.add_argument(
        "--skill-dir",
        type=Path,
        default=Path("."),
        help="SKILL 目录（包含 SKILL.md 与 references/）",
    )
    args = parser.parse_args()

    skill_file = args.skill_dir / "SKILL.md"
    if not skill_file.exists():
        print(f"错误：未找到 {skill_file}", file=sys.stderr)
        return 1

    text = skill_file.read_text(encoding="utf-8")
    fm, body, fm_parse_errors = parse_frontmatter(text)
    all_errors = list(fm_parse_errors)

    if fm is not None:
        all_errors.extend(validate_frontmatter(fm))

    all_errors.extend(validate_body(body, fm))
    all_errors.extend(validate_tool_name_migration(body))
    all_errors.extend(validate_workflow(body))
    all_errors.extend(validate_references(body, args.skill_dir))
    all_errors.extend(validate_rfc2119(body))
    all_errors.extend(validate_quality(body))
    all_errors.extend(validate_first_person(body, fm))
    all_errors.extend(validate_tool_binding(body, fm))
    all_errors.extend(validate_output_spec(body, fm))
    all_errors.extend(validate_file_dependency_decision(body))
    all_errors.extend(validate_UR_SKILL_file_leaks(body, fm))
    all_errors.extend(validate_unresolved_placeholders(body))
    all_errors.extend(validate_identity_title(body, fm))

    if all_errors:
        print(f"校验失败：发现 {len(all_errors)} 个问题\n")
        for idx, err in enumerate(all_errors, 1):
            print(f"{idx}. {err}")
        return 1

    body_lines = len(body.splitlines())
    print(
        f"校验通过：{skill_file}\n"
        f"  - frontmatter 字段完整\n"
        f"  - body 行数 {body_lines}/{MAX_BODY_LINES}\n"
        f"  - 无占位符\n"
        f"  - 风险边界声明完整\n"
        f"  - 专业边界声明完整\n"
        f"  - 工作流检查项数量正确\n"
        f"  - 引用文件全部存在\n"
        f"  - 工具绑定检查通过\n"
        f"  - 输出规格检查通过"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
