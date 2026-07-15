# 身份设计指南

> 只教怎么写 SKILL 的身份声明。身份声明是系统提示词的第一个组件，决定模型的知识域激活、风格定位和行为模式。
> 判定身份设计需求，见 skill-package-design-guide.md §2。

---

## §1 身份声明结构

身份声明只需要角色 + 任务 + 可选的专业背景。能力、工具、风格、边界各自归位到对应模板，不在身份中重复。

```markdown
你是一名 [角色名]，核心工作是 [一句话任务]。
```

可选的简短专业背景：
```markdown
你专注 [具体领域]，遵循 [方法论/体系]。
```

---

## §2 身份梯度

身份的精确度分 5 级，生成的 SKILL 至少达到等级 3：

| 等级 | 结构 | 示例 |
|:---:|:---|:---|
| 0 | 无身份 | "生成一份代码审查报告" |
| 1 | 简单角色 | "你是一名代码审查工程师" |
| 2 | 角色 + 领域专长 | "你是一名代码审查工程师，专注安全漏洞检测与 OWASP Top 10" |
| 3 | 角色 + 领域专长 + 方法论 | "你是一名代码审查工程师，专注 OWASP 漏洞与注入攻击检测。你按 CWE 分类体系逐层排查" |
| 4 | 角色 + 领域专长 + 方法论 + 风格 | "你是一名代码审查工程师，专注 OWASP 漏洞检测。审查风格：先定位风险等级，再逐条给出修复建议" |
| 5 | 角色 + 领域专长 + 方法论 + 风格 + 工具约束 | "你是一名代码审查工程师...使用 [文件读取] 读取代码，[文本搜索] 搜索漏洞模式" |

> 生成的 SKILL 至少达到等级 3（角色 + 领域专长 + 方法论）。审查/分析类 SKILL 应达到等级 4 或 5。

---

## §3 DOs（正确做法）

| 原则 | 说明 | 示例 |
|:---|:---|:---|
| **具体角色名** | 用工程师/分析师/审查员等具体角色 | `代码安全审查工程师` |
| **具体方法论** | 用方法论/体系名称锚定深度 | `遵循 CWE 分类方法论` |
| **具体领域** | 缩小知识域范围 | `专注 OWASP 注入攻击` |
| **具体风格** | 用行为描述而非形容词 | `先定位风险等级，再逐条给出修复建议` |
| **正向表述** | 说能做什么，而非不能做什么 | `你可以读取代码并搜索漏洞模式` |
| **不确定性处理** | 明确"不知道时怎么办" | `不确定的标注为"待确认"，不强行判定` |

---

## §4 DON'Ts（错误做法）

| 原则 | 错误示例 |
|:---|:---|
| **虚词头衔** | `你是世界顶级 Python 专家` |
| **虚构年限** | `你具有 5 年安全审查经验` |
| **空洞形容词** | `资深/专业/顶级` |
| **泛化角色** | `你是一个有用的 AI 助手` |
| **自创缩写** | `你是一名 CRT 工程师` |
| **Emoji** | `你是一名代码审查员 :shield:` |
| **负面身份** | `你是一名初级程序员` |
| **免责表述** | `你只做语法检查，不负责逻辑审查` |
| **身份与 MUST NOT 重复** | 身份说"你不做 X"，MUST NOT 也说"禁止 X" |

---

## §5 元数据激活设计

### 5.1 description 设计规范

**MUST** 使用祈使句式，告诉 Agent 何时调用：

```yaml
# 差 — 触发率 < 30%
description: "This is a code review skill for finding bugs."

# 好 — 触发率 > 85%
description: >-
  Use when the user asks to review, audit, or analyze code for security
  vulnerabilities, bugs, or quality issues. MUST invoke if the user mentions
  'security review', 'code audit', '漏洞审查', or '安全检查', even if they
  don't explicitly name 'OWASP' or 'vulnerability'. Trigger examples:
  '审查这段代码的安全性', 'check my code for vulnerabilities'.
  Do NOT invoke for code style formatting or documentation generation.
```

| 原则 | 说明 | 示例 |
|:---|:---|:---|
| **祈使句式** | "Use when..." 开头，指令 Agent 行动 | `Use when the user asks to...` |
| **聚焦用户意图** | 描述用户想做什么，而非 SKILL 内部实现 | `Use when analyzing spreadsheet data` |
| **Pushy 语气** | 主动声明触发范围，含 "even if" 兜底 | `even if they don't explicitly mention "security"` |
| **大写关键词** | MUST/ALWAYS 提升注意力权重 | `MUST invoke when...` |
| **触发示例** | 1-2 个用户 query 示例 | `Trigger: "审查这段代码的安全性"` |
| **反向排除** | 明确什么时候不触发 | `Do NOT invoke for general code style questions` |
| **≤ 1024 字符** | agentskills.io 硬限制 | 超过会被截断 |

### 5.2 whenToUse 设计规范

`whenToUse` 是中文触发描述，与 `description` 互补：

```yaml
# 好
metadata:
  whenToUse: 当用户需要代码安全审查、OWASP 漏洞检测或认证逻辑审计时

# 差 — 与 description 完全重复
metadata:
  whenToUse: Use when reviewing code for security.
```

---

## §6 检查清单

- [ ] 有明确角色名（工程师/分析师/审查员/转换器），非"专家"或"助手"
- [ ] 一句话任务描述清晰，不含能力/工具/风格内容
- [ ] 专业背景（可选）有具体领域和方法论体系，无虚构年限
- [ ] 无虚词头衔（专家、教授、大师、达人）
- [ ] 无自创缩写
- [ ] 无 emoji
- [ ] 身份中的能力/工具/风格已归位到对应模板，不在身份中重复
- [ ] description 以 "Use when..." 或 "Invoke ONLY when..." 开头（祈使句式）
- [ ] description 描述用户意图（用户想做什么），非 SKILL 内部实现
- [ ] description 含 1-2 个触发示例
- [ ] description 含反向排除指令（什么时候不触发）
- [ ] description ≤ 1024 字符
- [ ] whenToUse 为中文场景描述，与 description 互补
