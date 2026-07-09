# 模型格式适配设计指南

> 用途：指导将 SKILL 输出格式适配为不同 LLM 平台（Claude、ChatGPT、Gemini 等）的结构化偏好。用户指定目标平台时按平台调整结构语法；未指定时使用默认 Markdown 格式。

---

## 1. 为什么需要格式适配

不同 LLM 的训练数据使用不同的 token 模式，对结构标记的响应差异显著。同一句 Prompt 在不同模型上性能差异可达 30-50%——仅因格式不匹配，而非内容质量问题。一个在 Claude 上得分 92% 的 prompt，如果使用 XML 标签而非 Markdown 围栏，丢给 GPT-4 可能只有 78%。

**根本原因**：各模型厂商对训练数据结构做出了不同的选择：
- **Anthropic** 明确训练 Claude 将 XML 标签识别为结构锚点
- **OpenAI** 训练数据富含 Markdown 和 JSON Schema
- **Google** 为 Gemini 优化了多模态输入和清晰的上下文分隔

这与"正确"语法无关——所有现代 LLM 都能理解所有格式。关键在于匹配训练数据模式，让模型习得的关联正确触发。

**适用范围**：本指南适用于模式 A（从零生成）和模式 B1（外部 SKILL 优化）。对于模式 B2（内部优化）和模式 C（知识提取），通常不需要格式适配。

---

## 2. UR-SKILL 的默认格式：Markdown

UR-SKILL 使用 **Markdown** 作为默认输出格式。以下情况使用默认格式：
- 用户未指定目标平台
- 目标平台未知
- 生成的 SKILL 目标是跨模型可移植

**选择 Markdown 作为默认格式的原因**：
1. 最安全的跨模型兜底方案——所有主流模型都能胜任 Markdown
2. 生态系统支持最广泛
3. 人类可读、工具可解析
4. UR-SKILL 自身的 SKILL.md 文件就是 Markdown 编写的，保证格式一致

**UR-SKILL 使用的 Markdown 规范**：

| 元素 | 规范 | 理由 |
|:---|:---|:---|
| 章节标题 | `#`、`##`、`###`（ATX 风格） | 所有 Markdown 渲染器通用 |
| 关键约束 | `**MUST**`、`**SHOULD**`、`**MAY**`（RFC 2119） | 机器可解析，语义精确 |
| 二维数据 | Markdown 表格 `\| col \| col \|` | 对比关系一目了然 |
| 顺序步骤 | `1. → 2. → 3.` 编号列表 | 显式顺序保证 |
| 检查清单 | `- [ ]` / `- [x]` | 标准任务列表语法 |
| 代码/结构化数据 | 带语言标签的三反引号 | 所有模型要求的代码块格式 |
| 引用块 | `>` 前缀 | 清晰的语义分离 |
| 模块分隔 | `---` 水平线 | YAML frontmatter + 逻辑分段 |
| 不使用 emoji | 不作为约束标记 | 避免编码风险和解析歧义 |

---

## 3. 各模型格式偏好详解

### 3.1 Claude（Anthropic）

**首要偏好**：XML 标签结构
**次要偏好**：干净文本 + 显式标签
**避免**：能用 XML 时不要只用重 Markdown

**关键特征**：
- XML 标签是"超能力"——Anthropic 官方文档确认 Claude 被专门训练将 XML 标签解释为结构元数据
- 内部测试显示 XML 结构化提示相比散文版本一致性提升 20-40%
- 文档位置很重要：参考资料放**顶部**，指令和问题放**下方**——响应质量最多可提升 30%
- 字面指令遵循："精确做你要求的事，不多不少"
- 反例很强大（"不要包含免责声明。不要模糊你的结论。"）
- 3-5 个 few-shot 示例显著提升一致性

**推荐结构标签**：

| 标签 | 用途 | 优先级 |
|:---|:---|:---|
| `<role>` | Claude 的角色/身份 | 必选 |
| `<context>` | 背景、受众、约束 | 推荐 |
| `<task>` | 要做什么，用可操作的语言 | 必选 |
| `<instructions>` | 分步指导 | 推荐 |
| `<examples>` | few-shot 输出样本 | 推荐 |
| `<documents>` / `<document>` | 参考资料（带 `<source>` 元数据） | 推荐 |
| `<output_format>` | 期望的输出形状 | 推荐 |
| `<thinking>` | 内部推理（仅当 extended thinking 关闭时） | 按需 |

**Claude 专用 SKILL 结构模板**：

```xml
<role>
[身份声明：角色 + 核心任务]
</role>

<context>
[背景信息、受众、约束]
</context>

<task>
[核心指令]
</task>

<instructions>
1. [步骤 1]
2. [步骤 2]
3. [步骤 3]
</instructions>

<examples>
<example>
[期望输出的正面示例]
</example>
</examples>

<output_format>
[结构、长度、风格规格]
</output_format>
```

**重要提示**：
- 层次化嵌套标签以建立优先级（如 `<critical_rules>` 嵌套在 `<system>` 内）
- 启用 extended thinking API 时**不要**使用 `<thinking>` 标签——会冲突
- 通过 API 的 `system` 参数放置角色和稳定指令，而非内联 XML
- 能用 tool use 做结构化输出时优先用 tool use，而非 XML 强制
- 如果用户输入被拼接进 XML，必须转义——用户可能注入 `</instructions>` 等闭合标签

### 3.2 ChatGPT / GPT（OpenAI）

**首要偏好**：Markdown + 显式分隔符
**次要偏好**：JSON Schema 结构化输出
**避免**：没有 Markdown 包裹的纯 XML 提示

**关键特征**：
- 指令放在 prompt **开头**，用 `###` 或 `"""` 分隔指令与上下文
- 近因偏差敏感——prompt 末尾的内容权重更高
- GPT-5+ 系列默认：API 响应**不**默认使用 Markdown，必须显式请求 Markdown 格式
- 长对话中每 3-5 条消息追加一次 Markdown 格式指令以保持遵守
- JSON Schema 最适合结构化输出（function calling、structured outputs API）
- 自然语言推理请求（"逐步思考这个问题"）比 XML 思维标签效果更好
- 使用 `reasoning_effort` 参数控制思考深度（low/medium/high）
- 使用 `verbosity` 参数控制响应长度

**推荐结构元素**：

| 元素 | 用途 | 优先级 |
|:---|:---|:---|
| `###` 或 `"""` 分隔符 | 分离指令与上下文 | 必选 |
| `#` / `##` / `###` 标题 | 章节结构 | 推荐 |
| `**粗体**` | 关键约束和强调 | 推荐 |
| 带语言标签的三反引号 | 代码块和结构化数据 | 必选 |
| JSON Schema | 输出格式规范 | 推荐 |
| 编号列表 | 顺序指令 | 推荐 |
| 引导词（`import`、`SELECT`） | 引导代码生成模式 | 按需 |

**GPT 专用 SKILL 结构模板**：

```markdown
### 身份
你是[角色]。你的核心工作是[任务]。

### 上下文
[背景信息、约束]

### 任务
[核心指令]

### 指令
1. [步骤 1]
2. [步骤 2]
3. [步骤 3]

### 输出格式
按以下 JSON Schema 响应：
{
  "field1": "type",
  "field2": "type"
}

### 示例
**示例 1**：
[正面示例]

**示例 2**：
[正面示例]
```

**重要提示**：
- 具体说明要做什么，而不只是不要做什么（OpenAI 官方最佳实践第 7 条）
- 减少"虚词"描述——"3 到 5 句"优于"不要太长，几句话就行"
- GPT-5.2 特别：显式的 `<output_verbosity_spec>` 块有助于控制啰嗦程度
- 复杂任务用 `reasoning_effort` 参数而非 CoT 提示
- 对于 agentic 工作流，定义计划工具并标里程碑（pending/in_progress/done）

### 3.3 Gemini（Google）

**首要偏好**：PTCF 框架（角色 + 任务 + 上下文 + 格式）
**次要偏好**：带清晰标签的编号列表
**避免**：没有显式标签的深度嵌套层次结构

**关键特征**：
- Google 官方指南推荐四要素框架：角色（Persona）、任务（Task）、上下文（Context）、格式（Format）
- 编号列表和显式章节标签最适合结构组织
- 巨大的上下文窗口（Gemini 3 模型支持 1M+ tokens）——但位置仍然重要
- 使用 API 内置的思考层级（非基于 prompt 的 CoT）
- 多模态输入能力强（图片、音频、视频与文本并列）
- 标签式格式标记：`【目的】`、`【信息】`、`【格式】`
- 强烈推荐 few-shot 示例；零样本"可能效果不佳"

**推荐结构元素**：

| 元素 | 用途 | 优先级 |
|:---|:---|:---|
| `Persona` / `role` | 角色定义 | 必选 |
| `Task` / `instruction` | 做什么 | 必选 |
| `Context` | 背景与约束 | 推荐 |
| `Format` / `constraint` | 输出形状与限制 | 必选 |
| Few-shot 示例 | 校准输出质量 | 推荐 |
| Chain-of-Thought | 复杂推理任务 | 按需 |
| Search grounding | 时效性真实信息 | 按需 |

**Gemini 专用 SKILL 结构模板**：

```
role: [身份声明]
context: [背景、受众、约束]
instruction: [核心任务描述，含具体交付物]
constraint: [输出格式、长度、语气、结构要求]

示例：
---
[期望输出的正面示例]
---
```

替代中文标签结构：

```
【角色】
[身份声明]

【任务】
[核心指令]

【上下文】
[背景与约束]

【格式】
[输出规格]
```

**重要提示**：
- 时效性查询：显式指示模型使用当前日期
- 避免过多 few-shot 示例造成过拟合
- 稳定指令放 system instructions，动态内容放 user message
- CoT 提示对推理有效，但 Gemini 内置的思考层级可能使其冗余
- 分隔符（`"""`、`---`）有助于分离上下文与指令

---

## 4. 跨模型对比矩阵

| 特性 | Claude | GPT | Gemini |
|:---|:---|:---|:---|
| **最优格式** | XML 标签 | Markdown + 分隔符 | PTCF 四要素框架 |
| **指令位置** | 文档之后（自底向上注意力） | 开头（末尾有近因偏差） | 清晰分段分离 |
| **结构化输出** | XML 模板或 tool use | JSON Schema（function calling） | 混合（JSON + 灵活格式） |
| **Few-shot 敏感度** | 高（3-5 个示例强烈提升一致性） | 中（示例有帮助但不主导） | 高（官方建议始终使用 few-shot） |
| **反例** | 强力（"不要包含 X"） | 用正面指令替代 | 可用但正面框架更优 |
| **推理方法** | Extended thinking API 或 `<thinking>` 标签 | `reasoning_effort` 参数 | 内置思考层级 |
| **上下文窗口** | 200K-500K tokens | 128K-256K tokens | 1M+ tokens |
| **文档优先级** | Prompt 顶部（开头获得最多注意力） | Prompt 末尾（近因偏差） | 分段顺序重要但不极端 |
| **安全跨模型格式** | Markdown（可用但非最优） | Markdown（最优） | Markdown + 显式标签 |
| **Token 经济** | XML 标签增加约 20-50 tokens 开销 | Markdown = 最省 tokens | 标签结构 = 中等开销 |

---

## 5. UR-SKILL 适配策略

### 5.1 默认原则

> **用户未指定目标平台时，始终使用默认 Markdown 格式。不主动更改格式。**

UR-SKILL 的默认格式是 Markdown。所有 SKILL.md 文件默认以 Markdown 生成。格式适配仅在用户明确要求针对特定平台时才触发。

### 5.2 触发条件

以下场景 SHOULD 触发格式适配：

| 条件 | 动作 |
|:---|:---|
| 用户说"给 Claude 用"/"部署到 Claude"/"Claude 专用" | 适配为 XML 结构 |
| 用户说"给 ChatGPT 用"/"给 GPT 用"/"GPT 专用" | 适配为 Markdown + 分隔符（已是默认，仅验证） |
| 用户说"给 Gemini 用"/"Gemini 专用" | 适配为 PTCF 框架 |
| 用户说"跨平台"/"多个模型"/"通用" | 保持默认 Markdown（最安全兜底） |
| 用户未提平台 | 保持默认 Markdown |

### 5.3 适配范围

格式适配**只**影响生成 SKILL 的**结构语法**。不改变：
- 能力矩阵设计
- 工作流步骤逻辑
- 规则体系（RFC 2119 关键字全局通用）
- 审视维度
- 盲区机制
- 内容完备性

会改变的部分：
- 章节标题风格（Markdown `##` vs XML `<section>` vs PTCF 标签）
- 分隔符选择（三反引号 vs XML 标签 vs `role:` 标签）
- 输出格式规范（Markdown 表格 vs JSON Schema vs 标签格式）
- 指令位置（根据模型注意力模式决定放顶部还是底部）

### 5.4 何时不进行适配

以下情况 SHOULD NOT 进行格式适配：
- 生成的 SKILL 是 UR-SKILL 内部子 SKILL（始终使用 Markdown）
- SKILL 是设计参考或模板（模板保持 Markdown 以保证可移植性）
- 适配需要重写超过 30% 的内容（收益递减，警告用户）

---

## 6. 与 UR-SKILL 工作流的集成

### 6.1 在前置分析阶段（Step 1：子 SKILL）

`pre-analysis-engineer` SHOULD 从用户输入中检测目标平台并在前置分析报告中标注。未指定平台时标注为"默认（Markdown）"。

### 6.2 在执行阶段（Step 4：模块组装）

若前置分析报告标注了非默认平台，Step 4（执行）MUST 额外：
1. 读取 `./design-guides/model-format-adaptation-design-guide.md`
2. 按第 3 节选择对应平台的格式结构
3. 按第 5.3 节的适配范围限制执行调整
4. 不改变能力矩阵、工作流逻辑或规则体系

### 6.3 在校验阶段（Step 5：质量检查）

若已应用格式适配，校验阶段 SHOULD 额外检查：
- 适配后的格式与目标平台剖面匹配（按第 3 节）
- 适配未改变内容语义
- 所有 RFC 2119 关键字保持完整
- 检查清单和审视维度结构保留

### 6.4 在交付阶段（Step 7：输出组装）

若已应用格式适配，交付报告 MUST 包含：
- 目标平台声明
- 格式适配摘要（改变了什么）
- 提示：此 SKILL 在非目标平台上可能表现欠佳

---

## 7. 格式迁移检查清单

将 Markdown 默认 SKILL 适配到特定平台时，验证：

- [ ] **身份**保持：角色定义和核心任务不变
- [ ] **能力矩阵**保持：所有领域和层级完整
- [ ] **工作流步骤**保持：编号和逻辑不变
- [ ] **RFC 2119 关键字**保持：MUST/SHOULD/MAY 声明完整
- [ ] **检查清单**保持：`- [ ]` 项全部保留，审视维度结构完整
- [ ] **盲区机制**保持：三层处理流程完整
- [ ] **仅调整结构语法**：章节标题、分隔符、输出格式规范
- [ ] **无内容丢失**：重新格式化过程中未遗漏任何规则、检查项或声明

---

## 8. 参考文献

- [Anthropic 提示最佳实践](https://platform.claude.com/docs/en/build-with-claude/prompt-engineering)（2026年5月）
- [OpenAI GPT-5.2 提示指南](https://cookbook.openai.com/examples/gpt-5/gpt-5-2_prompting_guide)（2025年12月）
- [Google Gemini 提示设计策略](https://ai.google.dev/gemini-api/docs/prompting-strategies)（2026年）
- [Elnashar et al. "结构化数据生成的提示工程"（2025）](https://doi.org/10.55092/aias2025009) —— 6种提示风格的跨模型系统比较
- [Claude XML FAQ (claudexml.com)](https://claudexml.com/faq/) —— XML 标签实用指南
- [跨模型结构规范差异 (scalingthoughts.com)](https://scalingthoughts.com/blog/structural-conventions-across-models/) —— Claude 爱 XML、GPT 爱 JSON 的原因

---

## 8. 各平台 Subagent 支持情况

### 8.1 Subagent 是行业标准，不是平台特性

Subagent（也称子代理、子智能体、Task Agent）**不是某个平台的独有功能**——截至 2026 年，它已是行业标准。Subagent 是一个拥有独立上下文窗口、工具限制和系统提示词的隔离 AI 工作单元，由父代理启动以处理特定任务，仅返回结果。

**Subagent 对 SKILL 委派的意义**：
- **上下文隔离**：子代理的工作不污染父代理的上下文窗口
- **角色分离**：每个子代理有独立的身份声明，避免"两个'我是谁'在一个上下文里竞争"
- **并行执行**：多个子代理可同时运行
- **独立校验**：子代理以全新视角审视，不受父代理上下文的影响（无确认偏差）

### 8.2 各平台 Subagent 能力矩阵

#### 国际平台

| 平台 | Subagent 支持 | 机制 | 上下文隔离 |
|:---|:---:|:---|:---:|
| **Claude Code** | ✅ 原生 | 内置（Explore/Plan/general-purpose）+ YAML frontmatter 自定义 | ✅ 独立上下文窗口 |
| **Cursor** | ✅ 原生 | 内置（Explore/Bash/Browser）+ 前景/后台模式 | ✅ 独立上下文窗口 |
| **GitHub Copilot** | ✅ Copilot Agents | Copilot Workspace + Agent 模式（2025） | ✅ 任务隔离 |
| **Windsurf** | ✅ Cascade | Agent 模式 + SWE-grep 子代理 | ✅ 独立上下文 |
| **OpenAI Codex** | ✅ 原生 | 云端沙箱子代理，异步执行 | ✅ 沙箱隔离 |

#### 国内平台

| 平台 | Subagent 支持 | 机制 | 上下文隔离 |
|:---|:---:|:---|:---:|
| **Trae（字节）** | ✅ SOLO agent | Builder 模式 + subagent Task 工具 | ✅ 独立上下文窗口 |
| **Qoder CN（阿里）** | ✅ 原生 | Quest 2.0 子代理协同 + 专家团多代理 | ✅ 独立上下文 |
| **CodeBuddy（腾讯）** | ✅ Craft 模式 | 任务拆解 + 多代理协作 | ✅ 任务隔离 |
| **文心快码（百度）** | ✅ 多智能体 | 多智能体协同编程 | ✅ 代理隔离 |
| **CodeGeeX（智谱）** | ⚠️ 有限 | 代码翻译 + 指令模式，无显式子代理 API | 部分 |

### 8.3 UR-SKILL 的 Subagent 策略

#### 默认方案（跨平台安全）：`[Skill]` + 显式角色切换

UR-SKILL 的 Step 1 通过 `[Skill]` 调起前置分析 SKILL，并紧接着执行**角色切换声明**：

```
> 角色切换：前置分析阶段结束。以下所有步骤仅使用 UR-SKILL 主 SKILL 的身份和规则。
> 前置分析 SKILL 的角色定义、规则和约束不再适用。
```

**为什么 `[Skill]` 是安全默认**：
- `[Skill]` 是平台无关的概念——所有 agent 都能理解"将 SKILL 文件加载进上下文"
- 显式角色切换声明防止身份冲突和上下文污染
- 无论平台是否支持原生 subagent，都能正常工作

#### 升级方案：`[Task]` Subagent（平台依赖）

若用户指定了确认支持 subagent 的目标平台（Trae、Claude Code、Cursor、Qoder CN 等），可将前置分析 SKILL 的调用方式升级为 subagent（`[Task]`）而非 `[Skill]`：

| 方式 | 优点 | 缺点 | 适用场景 |
|:---|:---|:---|:---|
| `[Skill]` + 角色切换 | 跨平台安全，无语法差异 | 角色短暂共享上下文 | 默认（用户未指定平台） |
| `[Task]` Subagent | 真正上下文隔离，独立校验 | 平台特有语法，不可移植 | 用户明确指定支持 subagent 的平台 |

**建议**：默认使用 `[Skill]` + 角色切换以保证可移植性。适配指南的升级方案记录 subagent 选项，供确定目标平台的用户优化。

### 8.4 对 SKILL 设计的影响

在执行阶段（Step 4）为目标平台应用格式适配时：

- 若平台支持 subagent → 在生成的 SKILL 工作流中注明："本平台支持原生 subagent。在上下文隔离有益的场景中，可考虑将顺序的 [Skill] 调用替换为并行的 [Task] subagent 调用。"
- 若平台不支持 subagent → 生成的 SKILL 工作流 MUST 在任何嵌入 SKILL 调用后使用角色切换声明

这确保生成的 SKILL 在充分利用目标平台能力的同时，不产生可移植性问题。
