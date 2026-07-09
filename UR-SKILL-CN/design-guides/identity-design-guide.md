# Identity Design Guide

> 用途：指导 SKILL 的身份设计，确保生成的 SKILL 具备清晰、有效的身份声明。

---

## 1. Why Identity Matters

SKILL.md 的 body 就是系统提示词本体。身份声明是系统提示词的第一个组件，决定了模型的知识域激活、风格定位和行为模式。

**不区分的后果：**

- 无身份 → 模型退化为通用助手，输出泛化、无针对性
- 空洞身份（"你是专家"）→ 认知漂移，事实准确性下降（南加州大学 2026.3：知识检索从 71.6% 跌至 66.3%）
- 夸大身份（"世界顶级教授"）→ 过度自信，编造信息（宾大沃顿 2025.12）

**正确设计的收益：**

- 精确激活领域知识子集
- 稳定输出风格和推理深度
- 经验填充效应：具体背景描述触发模型自动召回细分知识

---

## 2. Identity Gradient Model

身份的精确度分 5 级，每提升一级，输出质量和领域针对性显著提升：

```
等级0：无身份
 "生成一份代码审查报告。"
 → 输出：通用、模板化、无亮点

等级1：简单角色
 "你是一名代码审查工程师。"
 → 输出：比等级 0 结构化，仍较通用

等级2：角色 + 领域专长
 "你是一名代码审查工程师，专注安全漏洞检测与 OWASP Top 10 分析方法论。"
 → 输出：领域针对性强

等级3：角色 + 领域专长 + 方法论
 "你是一名代码审查工程师，专注 OWASP 漏洞与注入攻击检测。你按 CWE 分类体系逐层排查，先定位风险等级再逐条给出修复建议。"
 → 输出：深度显著提升

等级4：角色 + 领域专长 + 方法论 + 风格
 "你是一名代码审查工程师，专注 OWASP 漏洞检测。审查风格：先定位风险等级，再逐条给出修复建议。你的审查流程遵循 CWE Top 25 方法论。"
 → 输出：接近高质量专业报告

等级5：角色 + 领域专长 + 方法论 + 风格 + 工具约束
 "你是一名代码审查工程师，专注 OWASP 漏洞检测。
  审查流程：按 CWE Top 25 分类体系逐层排查。
  审查风格：先定位风险等级，再逐条给出修复建议。
  使用 [Read] 读取代码，[Grep] 搜索漏洞模式，[Task] 启动子审查。
  不确定时标注为'待确认'，不强行判定。"
 → 输出：专业、可控、有边界
```

**目标**：生成的 SKILL 至少达到等级 3，审查/分析类 SKILL 应达到等级 4 或 5。

---

## 3. Full System Prompt Design (6 Components)

综合 Microsoft、Anthropic、OpenAI 的系统提示词设计规范，完整的系统提示词设计包含 6 个组件。在生成的 SKILL 中，这 6 个组件映射到不同章节，身份本身只保留最核心的 1-2 行：

```
[角色定义]   你是一名 [角色名]，核心工作是 [一句话任务]。       → rules-template §0 角色定义
[专业背景]   {可选：专注 [具体领域]，掌握 [方法论/体系]。}       → rules-template §0 角色定义（可选）

以下组件由其他模板/章节负责，不属于身份声明：
[能力范围]   你可以 [能做1]、[能做2]、[能做3]。                → capability-architecture-template
[工具说明]   你使用 [工具1] 做 X，[工具2] 做 Y。               → workflow-template（工具绑定）
[风格约束]   你的回答风格是：[行为化描述]。                     → output-template
[不确定性处理] 当遇到 [情况] 时，[如何处理]。                   → rules-template §1 规则 / workflow 门控
```

**设计原则**：身份只需回答"身份是什么、做什么"——一行角色名 + 一行任务描述 + 可选的专业背景。能力、工具、风格、边界各自归位到对应模板，不在身份中重复。

### 身份声明示例（正确 — 只写角色）

```
你是一名代码安全审查工程师，核心工作是检测代码中的安全漏洞并给出修复建议。
```
可选的简短专业背景：
```
你专注 OWASP Top 10 安全审查，遵循 CWE 分类方法论。
```
错误 — 把能力/风格/工具塞进身份：
```
你是一名代码安全审查工程师，核心工作是检测代码漏洞。
你可以读取代码、搜索漏洞模式、调用子审查任务。    ← 能力 → capability-architecture
你的审查风格：先定位风险等级，再逐条给出修复建议。  ← 风格 → output-template
你使用 [Read] 读取代码，[Grep] 搜索危险模式。       ← 工具 → workflow
```

---

## 4. DOs and DON'Ts

### DO（正确做法）

| 原则 | 说明 | 示例 |
|:---|:---|:---|
| **具体角色名** | 用工程师/分析师/审查员等具体角色 | `代码安全审查工程师` |
| **具体方法论** | 用方法论/体系名称锚定深度 | `遵循 CWE 分类方法论` |
| **具体领域** | 缩小知识域范围 | `专注 OWASP 注入攻击` |
| **具体风格** | 用行为描述而非形容词 | `先定位风险等级，再逐条给出修复建议` |
| **正向表述** | 说能做什么，而非不能做什么 | `你可以读取代码并搜索漏洞模式` |
| **不确定性处理** | 明确"不知道时怎么办" | `不确定的标注为"待确认"，不强行判定` |

### DON'T（错误做法）

| 原则 | 说明 | 错误示例 |
|:---|:---|:---|
| **虚词头衔** | 专家/教授/大师/达人 — 造成认知漂移（南加州大学 2026.3：准确率 -5.3%） | `你是世界顶级 Python 专家` |
| **虚构年限** | "X 年经验" — LLM 无此概念，虚构数字破坏身份真实感 | `你具有 5 年安全审查经验` |
| **空洞形容词** | 资深/专业/顶级 — 无锚定效果 | `你是一名资深工程师` |
| **泛化角色** | 角色太宽 → 知识域不聚焦 | `你是一个有用的 AI 助手` |
| **自创缩写** | 任何非通用缩写 → 增加认知负担 | `你是一名 CRT 工程师` |
| **Emoji** | 任何 emoji → 噪声，干扰指令解析 | `你是一名代码审查员 :shield:` |
| **负面身份** | 低级角色 → 降低性能 | `你是一名初级程序员` |
| **免责表述** | 在身份中声明"不负责X" | `你只做语法检查，不负责逻辑审查` |

---

## 5. The "Methodology Filling" Effect

**原理**：大模型通过海量文本训练，内化了不同角色的知识结构。当你描述具体领域和方法论时，模型会"脑补"填充该角色应有的细分知识——无需显式列举。虚构年限无效且有害（南加州大学 2026.3：空洞身份使准确性下降 5.3%）。

**示例**：

```
身份 A（无领域专长）：
"你是一名产品经理。"
→ 激活：需求分析、原型设计、用户研究（通用基础）

身份 B（有领域专长 + 方法论）：
"你是一名产品经理，专注电商推荐系统，遵循协同过滤与冷启动问题的方法论。"
→ 激活：上述通用知识 + 用户行为分析、协同过滤算法、A/B 测试框架、
  冷启动策略、实时推荐架构（自动填充的细分知识）
```

**应用**：领域描述越具体（专长 + 方法论 + 体系名），知识填充越精准。不需要在身份中编造年限数字或显式列出所有细分技能。

---

## 6. Identity Strategies by SKILL Type

身份声明只需要角色 + 任务 + 可选的领域专长背景。不同 SKILL 类型在**角色名和领域用词**上有差异：

### 审查/测试类 SKILL

```
角色名：审查工程师 / 测试工程师
专业背景：必填（领域专长 + 方法论体系）
示例：你是一名代码安全审查工程师，核心工作是检测安全漏洞并给出修复建议。
      你专注 OWASP Top 10 安全审查，遵循 CWE 分类方法论。
```

### 生成类 SKILL

```
角色名：生成工程师 / 设计师
专业背景：必填（领域专长 + 方法论体系）
示例：你是一名 API 文档生成工程师，核心工作是将代码注释转为 OpenAPI 规范文档。
      你专注 REST API 设计，遵循 OpenAPI 3.1 规范。
```

### 分析类 SKILL

```
角色名：分析师 / 研究员
专业背景：必填（领域专长 + 方法论体系）
示例：你是一名市场需求分析师，核心工作是分析用户反馈并提炼产品改进建议。
      你专注 B2B SaaS 产品分析，遵循 JTBD 需求分析框架。
```

### 工具类 SKILL

```
角色名：转换器 / 工具
专业背景：可选
示例：你是一名 Python 命名工具，核心工作是将自然语言描述转为 PEP 8 函数/变量名。
```

---

## 7. Common Pitfalls

| 陷阱 | 表现 | 修正 |
|:---|:---|:---|
| **身份膨胀** | "你是世界顶级代码专家，精通所有编程语言" | 收窄到具体专长："专注 Python 安全审查" |
| **身份弱化** | "你是一个助手" | 提升到等级 3："代码审查工程师，专注 OWASP 漏洞检测" |
| **能力降级混入身份** | "你只做语法检查" | 能力降级是反模式，不是身份 |
| **范围限制当身份** | "你只能给投资建议，不做医疗诊断" | 范围限制应放在专业边界声明 |
| **身份与 MUST NOT 重复** | 身份说"你不做 X"，MUST NOT 也说"禁止 X" | 身份只写正向能力，禁止行为去 MUST NOT |
| **Emoji 噪声** | ":rocket: 你是一个快速工程师" | 去掉所有 emoji |

---

## 8. Checklist

在完成 SKILL 的 identity 设计后，逐条检查：

- [ ] 有明确角色名（工程师/分析师/审查员/转换器），非"专家"或"助手"
- [ ] 一句话任务描述清晰，不含能力/工具/风格内容
- [ ] 专业背景（可选）有具体领域和方法论体系，无虚构年限
- [ ] 无虚词头衔（专家、教授、大师、达人）
- [ ] 无自创缩写
- [ ] 无 emoji
- [ ] 身份中的能力/工具/风格已归位到对应模板，不在身份中重复

---

## 9. File Relationships

```
identity-design-guide.md
  ↑ 引用
  ├── rules-template.md §3.1 角色定义 — "设计方法详见 identity-design-guide.md"
  ├── capability-architecture-template.md — 身份设计影响能力描述的粒度
  ├── design-rationale.md — 前置分析中识别身份膨胀/弱化
  └── anti-patterns.md 反模式 — 身份膨胀、身份弱化、能力降级混入身份
```

---

## 10. 元数据激活设计（YAML Frontmatter 的 name / description / whenToUse）

> 元数据是 SKILL 被激活的唯一入口。Agent 启动时只加载 name + description（~100 token），匹配后才加载 SKILL.md 全文。description 写不好 = SKILL 永远不会被触发。

### 10.1 渐进式加载机制

Agent Skills 使用三段式加载（Progressive Disclosure）：

| 阶段 | 加载内容 | token 量 | 时机 |
|:---|:---|:---|:---|
| Discovery | `name` + `description` | ~100 token | Agent 启动时 |
| Activation | `SKILL.md` 全文 | ~5,000 token 上限 | 用户意图匹配时 |
| Execution | `scripts/`、`references/`、`assets/` | 按需 | 执行过程中 |

**关键含义**：description 是触发合同的全部。如果 description 写不好，SKILL 正文再优秀也不会被加载。

### 10.2 description 设计规范

#### 句式要求

description **MUST** 使用祈使句式，告诉 Agent 何时调用：

```
正例: "Use when the user needs to perform code security review, detect OWASP Top 10 vulnerabilities, or audit authentication logic."
反例: "This skill helps with code review and security."（第三人称描述式 → 触发率低）
反例: "Code security review skill."（名词短语 → 几乎不触发）
```

#### 核心原则

| 原则 | 说明 | 示例 |
|:---|:---|:---|
| **祈使句式** | "Use when..." 开头，指令 Agent 行动 | `Use when the user asks to...` |
| **聚焦用户意图** | 描述用户想做什么，而非 SKILL 内部实现 | `Use when analyzing spreadsheet data`，非 `This skill parses CSV files` |
| **Pushy 语气** | 主动声明触发范围，含 "even if" 兜底 | `even if they don't explicitly mention "security"` |
| **大写关键词** | MUST/ALWAYS 提升注意力权重 | `MUST invoke when the user requests code review` |
| **触发示例** | 1-2 个用户 query 示例 | `Trigger: "审查这段代码的安全性"` |
| **反向排除** | 明确什么时候不触发 | `Do NOT invoke for general code style questions` |
| **≤ 1024 字符** | agentskills.io 硬限制 | 超过会被截断 |

#### description 模板

```
"Use when [用户想要达成的目标 A], [目标 B], or [目标 C]. MUST invoke if the user mentions [关键词1], [关键词2], or [关键词3], even if they don't explicitly name [领域]. Trigger examples: '[用户 query 示例1]', '[用户 query 示例2]'. Do NOT invoke for [排除场景1] or [排除场景2]."
```

#### 好坏对比

```yaml
# 差 — 触发率 < 30%
description: "This is a code review skill for finding bugs."

# 中 — 触发率 ~60%
description: "Use when reviewing code for bugs and vulnerabilities."

# 好 — 触发率 > 85%
description: >-
  Use when the user asks to review, audit, or analyze code for security
  vulnerabilities, bugs, or quality issues. MUST invoke if the user mentions
  'security review', 'code audit', '漏洞审查', or '安全检查', even if they
  don't explicitly name 'OWASP' or 'vulnerability'. Trigger examples:
  '审查这段代码的安全性', 'check my code for vulnerabilities'.
  Do NOT invoke for code style formatting or documentation generation.
```

### 10.3 whenToUse 设计规范

`whenToUse` 是中文触发描述，与 `description` 互补：

| 原则 | 说明 |
|:---|:---|
| **场景化** | 描述具体使用场景，非能力声明 |
| **中文优先** | 面向中文用户的中文场景描述 |
| **动作词开头** | "当用户..." 或 "需要在...时" |
| **互补而非重复** | 补充 description 未覆盖的中文使用场景 |

```yaml
# 好
metadata:
  whenToUse: 当用户需要代码安全审查、OWASP 漏洞检测或认证逻辑审计时

# 差 — 与 description 完全重复
metadata:
  whenToUse: Use when reviewing code for security.
```

### 10.4 平台适配因素

不同平台对元数据的处理方式不同。生成 SKILL 时应以 **Claude Code 原生 SKILL.md 为基准**，交付时按 [identity-template.md §6 多平台元数据模板](../templates/identity-template.md) 转换：

| 平台 | 格式 | 模板 | 触发机制 | 国内热度 |
|:---|:---|:---|:---|:---|
| Claude Code / Codex / Gemini CLI / **TRAE** / 通义灵码 / CodeBuddy | 原生 SKILL.md | 模板 A | description 语义匹配 | TRAE 最高 |
| Cursor | `.cursor/rules/*.mdc` | 模板 B | glob 文件匹配 | 最高 |
| Windsurf | `.windsurf/rules/*.md` | 模板 C | trigger 模式（always_on/model_decision/glob/manual） | 高 |
| GitHub Copilot | `.github/copilot-instructions.md` | 模板 D | 全量加载 | 高 |

### 10.5 检查清单

- [ ] description 以 "Use when..." 或 "Invoke ONLY when..." 开头（祈使句式）
- [ ] description 描述用户意图（用户想做什么），非 SKILL 内部实现
- [ ] description 含 1-2 个触发示例
- [ ] description 含反向排除指令（什么时候不触发）
- [ ] description ≤ 1024 字符
- [ ] description 使用大写 MUST/ALWAYS 提升注意力权重
- [ ] whenToUse 为中文场景描述，与 description 互补
- [ ] name 使用 kebab-case，简洁且包含领域关键词
