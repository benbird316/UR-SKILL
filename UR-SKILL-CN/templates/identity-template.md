# 身份声明模板

> 用途：定义生成 SKILL 的身份声明（系统提示词角色定义）标准填写格式
> 核心原则：身份只回答"身份是什么、做什么"，能力、工具、风格、边界各归其位
> 设计方法详见 [design-guides/identity-design-guide.md](../design-guides/identity-design-guide.md)

---

## 1. 身份声明模板

```
你是一名 [角色名]，核心工作是 [一句话任务]。
{可选：你专注 [具体领域]，遵循 [方法论/体系名称]。}
```

---

## 2. 填写规范

| 元素 | 规范 | 示例 |
|:---|:---|:---|
| 角色名 | 具体职业名，非"专家"/"助手" | 代码安全审查工程师、市场需求分析师 |
| 任务描述 | 一句话说明核心工作 | 检测代码中的安全漏洞并给出修复建议 |
| 专业背景 | 可选，需具体领域 + 方法论体系 | 专注 OWASP Top 10 安全审查，遵循 CWE 分类方法论 |

---

## 3. 正例与反例

| 类型 | 示例 | 说明 |
|:---|:---|:---|
| 正例 | 你是一名代码安全审查工程师，核心工作是检测代码中的安全漏洞并给出修复建议。 | 角色 + 任务，无多余内容 |
| 反例 | 你是一名世界级 Python 专家，精通所有编程语言。 | 身份膨胀、虚词头衔 |
| 反例 | 你只做语法检查，不负责逻辑审查。 | 能力降级混入身份 |
| 反例 | 你是一名代码审查员 :shield: | 包含 emoji |

---

## 4. 完整性检查清单

- [ ] 身份只有角色 + 任务（+ 可选的简短专业背景），不包含能力、工具、风格、边界
- [ ] 角色名具体（工程师/分析师/审查员/研究员/转换器），非"专家"/"助手"
- [ ] 一句话任务描述清晰
- [ ] 无虚词头衔（专家/教授/大师/达人/资深）
- [ ] 无自创缩写
- [ ] 无 emoji
- [ ] 无能力降级或范围限制语句

---

## 5. 元数据设计（YAML Frontmatter）

> 元数据是 SKILL 被 Agent 发现的唯一入口。遵循 agentskills.io 开放标准：仅 `name` + `description` 为必填字段。UR-SKILL 约定 `metadata.updated` 为附加必填。
> 详见 [metadata-spec.md](metadata-spec.md) 和 [design-guides/skill-package-design-guide.md §A.1](../design-guides/skill-package-design-guide.md)。

### 5.1 元数据模板

```yaml
---
name: {kebab-case-name}
description: >-
  当[用户意图A], [用户意图B], 或[用户意图C]时使用。
  覆盖请求如'[中文触发短语1]', '[中文触发短语2]'。
  即使未明确提及'[领域关键词]'也触发。
metadata:
  updated: {YYYY-MM-DD}
---
```

### 5.2 填写规范

| 字段 | 规范 | 来源 |
|:---|:---|:---|
| name | kebab-case，含领域关键词，≤ 64 字符 | agentskills.io 必填 |
| description | 自然语言触发描述，≤ 1024 字符，含中文触发短语 + 领域关键词 | agentskills.io 必填 |
| metadata.updated | YYYY-MM-DD 格式 | UR-SKILL 约定必填 |

### 5.3 description 设计指南

`description` 是**所有平台的唯一触发匹配字段**。Agent 通过语义匹配判断是否加载此 SKILL。

| 原则 | 说明 | 差 | 好 |
|:---|:---|:---|:---|
| 祈使/场景式 | "当用户想要XX时"而非描述自己 | `"A security review skill"` | `当用户需要代码安全审查、漏洞检测时使用` |
| 含触发短语 | 用户实际会说的话 | 纯规则描述无 query | `覆盖请求如'审查这段代码', '帮我检查安全问题'` |
| 含领域关键词 | 提升语义匹配精度 | 泛泛"分析" | `OWASP, 安全审查, 漏洞检测` |
| 不复制 body | description 只写触发信息 | description = body 摘要 | description 只写触发条件，不写能力描述 |

### 5.4 常见反模式

| 反模式 | 错误 | 正确 |
|:---|:---|:---|
| 英文描述中文SKILL | `"Use when the user wants to..."` | 中文触发短语 |
| 描述式而非触发式 | `"帮助用户审查代码"` | `当用户需要代码审查时使用` |
| 缺触发示例 | 纯规则描述 | `覆盖请求如'审查这段代码'` |

---

## 6. 多平台元数据模板

> UR-SKILL 以 **Claude Code 原生 SKILL.md** 为基准格式。前端字段遵循 agentskills.io 标准（name + description + metadata），所有平台兼容。

### 6.1 平台对照总览

| 平台 | 格式 | 文件路径 | 触发机制 |
|:---|:---|:---|:---|
| Claude Code / TRAE / 通义灵码 / CodeBuddy | 原生 SKILL.md | `.claude/skills/{name}/SKILL.md` | description 语义匹配 |
| Cursor | `.cursor/rules/*.mdc` | `.cursor/rules/{name}.mdc` | glob 文件匹配 |
| Windsurf | `.windsurf/rules/*.md` | `.windsurf/rules/{name}.md` | trigger 模式选择 |
| GitHub Copilot | `.github/copilot-instructions.md` | `.github/copilot-instructions.md` | 全量加载 |

### 6.2 模板 A：Claude Code 原生 SKILL.md（基准模板）

```yaml
---
name: {kebab-case-name}
description: >-
  当[用户意图A], [用户意图B], 或[用户意图C]时使用。
  覆盖请求如'[中文触发短语1]', '[中文触发短语2]'。
metadata:
  updated: {YYYY-MM-DD}
---
```

### 6.3 模板 B：Cursor `.cursor/rules/*.mdc`

```
---
description: "{SKILL 能力简述}"
globs: ["{文件匹配模式1}", "{文件匹配模式2}"]
alwaysApply: false
---

# {SKILL 名称}

{将 SKILL.md body 全部内容粘贴至此}
```

### 6.4 模板 C：Windsurf `.windsurf/rules/*.md`

```
---
trigger: {always_on | model_decision | glob | manual}
description: "{SKILL 能力简述}"
---

{将 SKILL.md body 全部内容粘贴至此}
```

### 6.5 模板 D：GitHub Copilot `.github/copilot-instructions.md`

```markdown
# {SKILL 名称}

{将 SKILL.md body 全部内容粘贴至此。去掉 YAML frontmatter，只保留 Markdown body}
```

### 6.6 交付检查清单

- [ ] 已确定目标平台
- [ ] 已生成基准 SKILL.md（模板 A）
- [ ] 如需 Cursor → 已按模板 B 生成 `.mdc`
- [ ] 如需 Windsurf → 已按模板 C 生成规则文件
- [ ] 如需 Copilot → 已按模板 D 生成 `copilot-instructions.md`
