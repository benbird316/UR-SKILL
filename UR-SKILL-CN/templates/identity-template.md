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

> 元数据（name / description / whenToUse）是 SKILL 被 Agent 发现的唯一入口。设计方法详见 [design-guides/identity-design-guide.md §10](../design-guides/identity-design-guide.md)。

### 5.1 元数据模板

```yaml
---
name: {kebab-case-name}
description: >-
  Use when [用户想要达成的目标 A], [目标 B], or [目标 C].
  MUST invoke if the user mentions [关键词1], [关键词2], or [关键词3],
  even if they don't explicitly name [领域]. Trigger examples:
  '[用户 query 示例1]', '[用户 query 示例2]'.
  Do NOT invoke for [排除场景1] or [排除场景2].
metadata:
  updated: {YYYY-MM-DD}
  type: prompt
  whenToUse: 当[中文场景描述，与 description 互补]
---
```

### 5.2 填写规范

| 字段 | 规范 | 必填 |
|:---|:---|:---|
| name | kebab-case，含领域关键词，≤ 64 字符 | 是 |
| description | 祈使句式 "Use when..."，≤ 1024 字符，含触发示例 + 反向排除 | 是 |
| metadata.type | 固定值 `prompt` | 是 |
| metadata.whenToUse | 中文场景描述，与 description 互补不重复 | 是 |
| metadata.updated | YYYY-MM-DD 格式 | 是 |

### 5.3 好坏对比

```yaml
# 差 — 触发率低（描述式、无示例、无排除）
description: "This is a skill for code security review."
metadata:
  whenToUse: 代码审查

# 好 — 触发率高（祈使式、有示例、有排除）
description: >-
  Use when the user asks to review, audit, or analyze code for security
  vulnerabilities, bugs, or quality issues. MUST invoke if the user mentions
  'security review', 'code audit', '漏洞审查', or '安全检查', even if they
  don't explicitly name 'OWASP'. Trigger examples:
  '审查这段代码的安全性', 'check my code for vulnerabilities'.
  Do NOT invoke for code style formatting or documentation generation.
metadata:
  whenToUse: 当用户需要代码安全审查、OWASP 漏洞检测或认证逻辑审计时
```

### 5.4 常见元数据反模式

| 反模式 | 错误示例 | 修正 |
|:---|:---|:---|
| 描述式而非祈使式 | `"This skill helps with..."` | `"Use when the user needs to..."` |
| 缺触发示例 | 纯规则描述无 query | 加 `Trigger examples: '...'` |
| 缺反向排除 | 可能被误触发 | 加 `Do NOT invoke for...` |
| 与 body 内容重复 | description = body 第一段 | description 只写触发条件 |
| whenToUse 复制 description | 中英文完全相同 | whenToUse 写中文互补场景 |

---

## 6. 多平台元数据模板

> UR-SKILL 以 **Claude Code 原生 SKILL.md** 为基准格式。以下 4 套模板覆盖国内外主流平台，交付时根据目标平台选用对应模板。

### 6.1 平台对照总览

| 平台 | 格式 | 文件路径 | 触发机制 | 国内热度 |
|:---|:---|:---|:---|:---|
| Claude Code | 原生 SKILL.md | `.claude/skills/{name}/SKILL.md` | description 语义匹配 | 高 |
| Codex CLI | 原生 SKILL.md | `.agents/skills/{name}/SKILL.md` | description 语义匹配 | 中 |
| Gemini CLI | 原生 SKILL.md | `.claude/skills/{name}/SKILL.md` | description 语义匹配 | 低 |
| **TRAE** | 原生 SKILL.md | `.claude/skills/{name}/SKILL.md` | description 语义匹配 | **最高** |
| 通义灵码 | 原生 SKILL.md 兼容 | 同 Claude Code | description 语义匹配 | 高 |
| CodeBuddy | 原生 SKILL.md 兼容 | 同 Claude Code | description 语义匹配 | 高 |
| **Cursor** | `.cursor/rules/*.mdc` | `.cursor/rules/{name}.mdc` | glob 文件匹配 | **最高** |
| **Windsurf** | `.windsurf/rules/*.md` | `.windsurf/rules/{name}.md` | trigger 模式选择 | 高 |
| **GitHub Copilot** | `.github/copilot-instructions.md` | `.github/copilot-instructions.md` | 全量加载（无渐进式） | 高 |

### 6.2 模板 A：Claude Code 原生 SKILL.md（基准模板）

> 适用：Claude Code / Codex CLI / Gemini CLI / TRAE / 通义灵码 / CodeBuddy

```yaml
---
name: {kebab-case-name}
description: >-
  Use when [用户想要达成的目标 A], [目标 B], or [目标 C].
  MUST invoke if the user mentions [关键词1], [关键词2], or [关键词3],
  even if they don't explicitly name [领域]. Trigger examples:
  '[用户 query 示例1]', '[用户 query 示例2]'.
  Do NOT invoke for [排除场景1] or [排除场景2].
metadata:
  updated: {YYYY-MM-DD}
  type: prompt
  whenToUse: 当[中文场景描述，与 description 互补]
---
```

**关键差异**：这是基准格式，无需转换。TRAE 和通义灵码均原生支持此格式。description 是唯一触发入口，必须遵循 §5.1-§5.2 的祈使句式规范。

---

### 6.3 模板 B：Cursor `.cursor/rules/*.mdc`

> 适用：Cursor IDE

```
---
description: "{SKILL 能力简述，AI 用于判断是否加载此规则}"
globs: ["{文件匹配模式1}", "{文件匹配模式2}"]
alwaysApply: false
---

# {SKILL 名称}

{将 SKILL.md body 全部内容粘贴至此}
```

**关键差异**：
- Cursor 使用 **glob 文件匹配**而非语义匹配——规则在匹配文件被编辑时才加载
- `description` 仅 1 句话（AI 判断相关性用），不是完整的触发合同
- `globs` 决定什么时候加载（如 `"**/*.tsx"`, `"src/api/**/*.ts"`）
- `alwaysApply: true` 则每条消息都加载（token 消耗大，仅核心规范使用）
- 需将 SKILL.md 正文完整粘贴到 .mdc 文件 body 中

**示例**：
```
---
description: "代码安全审查：检测 OWASP Top 10 漏洞、注入攻击、硬编码凭据"
globs: ["**/*.ts", "**/*.js", "**/*.py", "**/*.java", "**/*.go"]
alwaysApply: false
---

# 代码安全审查

当审查代码时，始终检查：
1. SQL 注入（字符串拼接构造数据库查询）
2. 硬编码密钥（API keys、密码、token）
...
```

---

### 6.4 模板 C：Windsurf `.windsurf/rules/*.md`

> 适用：Windsurf IDE

```
---
trigger: {always_on | model_decision | glob | manual}
description: "{SKILL 能力简述}"
---

{将 SKILL.md body 全部内容粘贴至此}
```

**关键差异**：
- 4 种 trigger 模式：
  - `always_on` = 每条消息全量注入（6,000 字符/文件上限，12,000 总量上限）
  - `model_decision` = 仅 description 在上下文中，AI 自行决定是否加载全文
  - `glob` = 匹配文件路径时激活
  - `manual` = 仅 `@mention` 时加载
- 无渐进式加载，全量注入，需精选内容控制 token
- 所有规则文件总计 ≤ 12,000 字符

**示例**：
```
---
trigger: model_decision
description: "代码安全审查规则：OWASP Top 10 漏洞检测与修复建议"
---

当审查代码时，始终检查：
1. SQL 注入...
...
```

---

### 6.5 模板 D：GitHub Copilot `.github/copilot-instructions.md`

> 适用：GitHub Copilot（VS Code / JetBrains / GitHub.com）

```markdown
# {SKILL 名称}

{将 SKILL.md body 全部内容粘贴至此。去掉 YAML frontmatter，只保留 Markdown body}
```

**关键差异**：
- 纯 Markdown，**无 YAML frontmatter**
- 全量加载，无渐进式——所有指令始终在上下文中
- 仅一个文件 `.github/copilot-instructions.md`
- 多个 SKILL 需用 `##` 二级标题分隔
- Copilot Chat 适用，内联补全不适用

**示例**：
```markdown
# 代码安全审查

当审查代码时，始终检查：
1. SQL 注入（字符串拼接构造数据库查询）
2. 硬编码密钥（API keys、密码、token）
...

## 项目构建规则

- 使用 `pnpm build` 构建
- 测试用 `pnpm test`
```

### 6.6 交付检查清单

- [ ] 已确定目标平台（单选或多选）
- [ ] 已生成基准 SKILL.md（模板 A）
- [ ] 如需 Cursor → 已按模板 B 生成 `.mdc`，globs 已正确配置
- [ ] 如需 Windsurf → 已按模板 C 生成规则文件，trigger 模式已选择
- [ ] 如需 Copilot → 已按模板 D 生成 `copilot-instructions.md`
- [ ] 模板 B/C/D 的 body 内容与基准 SKILL.md 保持一致
