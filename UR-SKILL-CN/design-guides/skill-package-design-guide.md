# SKILL 包设计指南

> 核心原则：SKILL.md 是"大脑"（<500行），所有细节卸载到子目录。
> 本指南判定：目标 SKILL 需要哪些非主体文件。

---

## §1 目录结构标准

```
skill-name/
├── SKILL.md              ← 必须。主体文件，<500行
├── references/           ← 可选。参考文档，按需加载
├── scripts/              ← 可选。可执行脚本，按需执行
└── assets/               ← 可选。静态资源，按需加载
```

**MUST** SKILL.md < 500 行。超过则必须拆分内容到 references/。
**MUST** references/ 下文件保持一级深度，禁止嵌套子目录。
**MUST** 文件引用使用相对路径（`references/xxx.md`），禁止绝对路径。
**MUST NOT** 创建给人看的文件（README.md、CHANGELOG.md、INSTALLATION_GUIDE.md）。

---

## §2 文件触发判定（三原则）

判定顺序：原则1 → 原则2 → 原则3

### 2.1 原则1：用户意图驱动（第一优先级）

用户是否明确要求了特定标准/风格/方法论？

| 用户意图信号 | 需要文件 | 存放位置 | 示例 |
|:---|:---|:---|:---|
| "按XX标准/规范" | 说明类 ref | references/classification.md | "按PEP 8" → Python编码规范分类 |
| "避免XX问题" | 方案类 ref / 反模式文件 | references/fix-patterns.md / references/anti-patterns.md | "避免口语化" → 反模式：口水话 |
| "输出要包含XX分级" | 规范类 ref | references/output-spec.md | "问题分级" → 分级标准 |
| "需要可执行脚本" | 脚本 | scripts/*.py | "自动校验" → validate.py |
| "需要输出模板" | 资源文件 | assets/* | "按品牌模板输出" → template.md |
| "涉及多领域术语" | 术语表 | references/glossary.md | "金融+法律" → 术语表 |
| "给我示例参考" | 示例文件 | references/examples.md | "参考优秀案例" → 示例 |

**MUST** 用户意图信号是强制触发条件。一旦命中，无论 SKILL 规模如何，都必须创建对应文件。

### 2.2 原则2：主体容量测试（第二优先级）

| 容量状态 | 动作 |
|:---|:---|
| 主体 < 500 行，且内容完整 | 无需拆分，保持单文件 |
| 主体 ≥ 500 行，或内容装不下 | 必须拆分：将规范表格、示例、详细规则下沉到 references/ |
| 主体 < 500 行，但信息密度过低 | 检查是否冗余，删除模式化填充 |

**MUST** 主体容量测试是硬性约束，不是可选规则。

### 2.3 原则3：领域深度修正（第三优先级）

在原则1和原则2之后，用领域深度修正文件类型和数量。

| 级别 | 判断 | 修正动作 |
|:---|:---|:---|
| 通用域 | LLM训练数据中广泛存在 | 无需额外 ref |
| 通用域 + 深度 | 用户要求特定标准/风格 | 原则1已覆盖 |
| 专业域 | LLM可能知道但不精确 | 增加说明类 ref（术语定义、分类体系） |
| 专业域 + 细化 | 需要可操作方法 | 增加方法类 + 验证类 ref |
| 深度专业域 | 知识快速迭代/内部规范 | 增加全部类型 |

> **知识文件拆分粒度**：一个辐射领域 → 至多一个知识文件。若辐射领域的知识内容较少（< 50 行），允许合并到相邻领域；若超出 200 行（ref-types-design-guide.md §4 硬约束），在领域内按子主题拆分并加编号（如 `classification-domain1.md`）。

---

### 2.4 ref 文件类型参考（启发式起点，非强制）

以下为按 SKILL 类型的默认推荐。**最终判定以 research-analyst 的领域调查结果和用户明确需求为准**——如果领域调查发现该领域不需要反模式，或用户明确说"不要术语表"，则覆盖本表。

| ref 文件类型 | 功能型 | 创意型 | 社交型 | 覆盖条件 |
|:---|:---:|:---:|:---:|:---|
| 说明类 ref | 推荐 | 可选 | — | 领域有专业分类体系时才做 |
| 方法类 ref | 推荐 | — | — | 领域有对错标准/检测方法时才做 |
| 验证类 ref | 推荐 | — | — | 领域有已知故障模式时才做 |
| 方案类 ref | 推荐 | 可选 | — | 领域有"好心办坏事"的反模式时才做 |
| 规范类 ref | 推荐 | 推荐 | 可选 | 几乎所有 SKILL 都需要，只是详略不同 |
| 术语表 | 推荐 | 可选 | — | 领域有 10+ 个需精确定义的术语时才做 |
| 示例 | 推荐 | 推荐 | 推荐 | 三种类型都需要，仅数量和性质不同 |
| 脚本 | 可选 | — | — | 需自动化检测/验证时才做 |
| 资源文件 | 可选 | 可选 | — | 需输出模板/品牌素材时才做 |

> 覆盖规则：research-analyst 步骤 2 的领域调查（最佳实践 + 常见错误实践）可推翻本表任何默认推荐。本表仅提供"通常需要什么"的起点判断，不做最终裁定。

### 2.5 判定速查：从判据到文件

以下按资产类型逐一分析**为什么需要**，并给出可测试的单一判据。research-analyst 在文件依赖分析阶段直接使用此表。

#### 三底线（门槛文件）

任何非单文件 SKILL（内容无法完全内联到 body）都必须创建：

| 文件 | 为什么需要 | 判据 |
|:---|:---|:---|
| **references/example.md** | 用户需要看到具体输入→输出映射，否则无法理解 SKILL 的行为边界 | 一律需要（仅纯工具型单文件 SKILL 可无示例文件） |
| **references/anti-patterns.md** | 缺乏反模式，模型将系统性重复同一类错误——"怎么写"必须有"别怎么写"对照 | 一律需要（领域调查中收集 ≥3 个常见错误模式） |
| **references/troubleshooting.md** | 运行时必然出现边缘情况，没有故障恢复指南意味着每次出错都从零开始 | 一律需要（领域调查中收集 ≥3 个典型故障场景） |

> 三底线例外：
> 1. 单文件 SKILL（所有逻辑 < 500 行，无外部知识依赖，无自创术语）可将三底线精简为 body 内的 `## 注意事项` 小节，无需独立文件。
> 2. 用户明确表示不需要参考文件时，可不生成。
> 3. 用户仅要求生成**系统提示词**（非完整 SKILL 包）时，可不生成三底线文件。

#### 按需文件

| 文件 | 为什么需要 | 判据（单问） | 典型触发场景 |
|:---|:---|:---|:---|
| **领域知识 ref（5类）** | LLM 训练数据的知识有截止日期且可能不精确——外部标准、平台规范、API 接口、学术理论需要可靠引用源 | **LLM 训练数据能否稳定覆盖该领域知识？**<br>否 → 需要<br>按用途分为：说明类/方法类/验证类/方案类/规范类 | OWASP/CWE（安全，说明类）、PEP 8（Python，说明类）、小红书排版规范（平台，说明类）、React API 签名（接口，方法类） |
| **glossary** | 同一术语在不同领域含义不同（如"模型"在 AI/建筑/金融中），无精确定义会导致下游步骤歧义累积 | **是否引入 ≥5 个自创术语，或跨 ≥2 个专业领域？**<br>是 → 需要 | 方法论术语（KSAO、三问筛选）、平台特有概念（种草/爆款）、跨域场景（金融+法律） |
| **scripts/** | 人工校验无法规模化——代码格式、输出结构、合规检查需要可重复的程序化验证 | **是否需要程序化验证/检测/生成？**<br>是 → 需要 | 安全审计（validate_findings.py）、代码生成（check_syntax.py）、输出格式校验 |
| **assets/** | 用户需要可复用的产出物模板或品牌素材，不是每次从零手写 | **是否需要静态模板/配置/素材？**<br>是 → 需要 | 报告模板（report_template.md）、品牌素材、配置文件模板 |
| **output-spec** | 输出无结构规范会导致格式漂移——"问题分级表""严重度"等概念每次不同，下游工具无法解析 | **输出是否需要分级/量化/结构化？**<br>是 → 需要 | 安全审查（问题分级 P0-P3 + Mermaid 图）、代码审查（严重度/类型/修复建议）、测试报告 |

#### 边界场景判别指南

| 场景 | 判据 | 结论 |
|:---|:---|:---|
| 小红书内容创作 | 平台排版规范、品类术语、话题策略 → LLM 不稳定覆盖 | **需要说明类 ref（平台规范）+ 方案类 ref（品类模式）** |
| 通用创意写作 | 修辞/叙事/结构为通用知识，LLM 训练数据充分 | **不需要** 领域知识 ref |
| 公众号排版 | 平台有特定排版规范（字号/间距/配图规则） | **需要** 说明类 ref |
| Python 基础编码 | PEP 8 是公开标准且在训练数据中 | 边界——推荐 lightweight 说明类 ref，非强制 |
| REST API 设计 | API 签名/端点随版本变化，不可靠 | **需要** 方法类 ref（API 参考） |
| 个人日记写作 | 无平台绑定，无标准约束 | 单文件 SKILL，三底线可内联为 body 小节 |

> 覆盖规则：research-analyst 步骤 2 的领域调查（最佳实践 + 常见错误实践）可推翻本表任何默认推荐。本表仅提供"通常需要什么"的起点判断，不做最终裁定。

---

## §3 文件类型速查表

| 文件类型 | 存放位置 | 触发条件（满足任一） | 设计指南 |
|:---|:---|:---|:---|
| 说明类 ref | references/classification.md | 用户要求特定标准/分类体系 | classification-ref-design-guide.md |
| 方法类 ref | references/detection-methods.md | 需要可操作的检测/追溯方法 | detection-ref-design-guide.md |
| 验证类 ref | references/verification-patterns.md | 需要验证/校准真假问题 | fault-ref-design-guide.md |
| 方案类 ref | references/fix-patterns.md | 需要正反模式对照 | pattern-ref-design-guide.md |
| 规范类 ref | references/output-spec.md | 输出需要分级/量化标准 | output-design-guide.md |
| 反模式文件 | references/anti-patterns.md | 需要识别常见错误模式 | pattern-ref-design-guide.md §反模式 |
| 故障诊断文件 | references/troubleshooting.md | 需要运行时故障修复 | fault-ref-design-guide.md §故障诊断 |
| 术语表 | references/glossary.md | 自创术语 ≥ 5 个，或多领域交叉 | glossary-design-guide.md |
| 示例文件 | references/examples.md | 用户要求示例，或任务模式复杂 | examples-design-guide.md |
| 脚本 | scripts/*.py | 需要自动化检测/验证/生成 | scripts-design-guide.md |
| 资源文件 | assets/* | 需要输出模板/配置文件/品牌素材 | assets-design-guide.md |

---

## §4 决策清单

```markdown
## 文件依赖决策清单

### 原则1：用户意图信号
- [ ] 用户是否要求特定标准/规范？ → 需要说明类 ref
- [ ] 用户是否要求避免特定问题？ → 需要方案类 ref / 反模式文件
- [ ] 用户是否要求输出分级/量化？ → 需要规范类 ref
- [ ] 用户是否要求可执行脚本？ → 需要 scripts/
- [ ] 用户是否要求输出模板？ → 需要 assets/
- [ ] 用户是否涉及多领域术语？ → 需要术语表
- [ ] 用户是否要求示例参考？ → 需要示例文件

### 原则2：主体容量测试
- [ ] SKILL.md body 预估行数 < 500？
- [ ] 若 ≥ 500，哪些内容需要下沉到 references/？

### 原则3：领域深度修正
- [ ] 领域深度：通用域 / 通用域+深度 / 专业域 / 专业域+细化 / 深度专业域
- [ ] 修正：增加/减少哪些文件类型？

### 最终决策
| 文件类型 | 需要 | 数量 | 设计指南 |
|:---|:---:|:---:|:---|
| ... | ... | ... | ... |
```

---

## §5 检查清单

- [ ] 目录结构符合标准（SKILL.md + references/ + scripts/ + assets/）
- [ ] 文件引用使用相对路径，一级深度
- [ ] 判定遵循三原则顺序（意图 → 容量 → 深度）
- [ ] 用户意图信号作为强制触发条件，不依赖三档复杂度标签
- [ ] SKILL.md < 500 行（硬性约束）


---

## §A 平台适配附录（仅在用户指定目标平台时加载）

> 本附录提供平台特定的 frontmatter 字段差异、格式偏好、工具映射和约束数据。
> 仅在用户明确要求"给XX平台用"/"XX专用"/"部署到XX"时加载。
> 未指定平台时，使用 agentskills.io 标准格式（§A.1）。

---

### A.1 Frontmatter 字段兼容性矩阵

不同平台/工具对 frontmatter 字段的支持程度不同。以下为实测结论：

| 字段 | agentskills.io | Trae IDE | Claude Code | Codex CLI | Cursor | 说明 |
|:---|:---:|:---:|:---:|:---:|:---:|:---|
| `name` | **必填** | **必填** | **必填** | **必填** | **必填** | 所有平台通用 |
| `description` | **必填** | **必填** | **必填** | **必填** | **必填** | 触发匹配的核心字段 |
| `metadata` | 可选 | 可选 | 可选 | 可选 | 可选 | 任意键值对，平台扩展入口 |
| `updated` | 可选 | 可选 | 可选 | 可选 | 可选 | ① 版本变迁追踪；② 让 LLM 感知数据新鲜度，判断领域知识是否可能过时。UR-SKILL 约定必填，放于 `metadata` 内 |


> **关键结论**：
> - **触发匹配靠 `description`**——所有平台都用它来判断是否加载 SKILL
> - `updated`  不是任何平台的标准字段，是 **UR-SKILL 自身的质量元数据约定**
> **默认策略**：按 agentskills.io 标准，将所有非标准字段放入 `metadata`。这是最安全、最具跨平台兼容性的做法。



---

### A.2 模型格式速查表

| 平台 | 最优格式 | 指令位置 | 结构化输出 | Few-shot敏感度 | 上下文窗口 | 安全跨模型格式 |
|:---|:---|:---|:---|:---|:---|:---|
| **Claude** | XML标签 | 文档之后（自底向上） | XML模板或tool use | 高（3-5个示例） | 200K-500K | Markdown（可用但非最优） |
| **GPT** | Markdown+分隔符 | 开头（末尾有近因偏差） | JSON Schema | 中 | 128K-256K | Markdown（最优） |
| **Gemini** | PTCF框架 | 清晰分段分离 | 混合（JSON+灵活格式） | 高（官方建议始终使用） | 1M+ | Markdown+显式标签 |
| **默认** | Markdown | — | Markdown表格+代码块 | 中 | — | Markdown（最安全兜底） |

**推荐结构标签/元素**：
- **Claude**：`<role>`、`<context>`、`<task>`、`<instructions>`、`<examples>`、`<output_format>`
- **GPT**：`###` 或 `"""` 分隔符、`#`/`##`/`###` 标题、`**粗体**`、带语言标签的三反引号、JSON Schema
- **Gemini**：`role:`/`context:`/`instruction:`/`constraint:`、Few-shot示例

**格式适配范围**：只调整结构语法（章节标题、分隔符、输出格式规范），不改变能力矩阵、工作流逻辑或规则体系。

---

### A.3 IDE工具映射表

SKILL.md 中使用**通用类别**，Agent 执行时自动映射为当前 IDE 的具体工具名。

| 通用类别 | Trae | Cursor | Claude Code | Windsurf | CodeBuddy | Qoder | Codex CLI |
|:---|:---|:---|:---|:---|:---|:---|:---|
| `[文件读取]` | `view_files` | `read_file` | `Read` | `view_file` | `read_file` | `read_file` | `—`（通过 `shell`） |
| `[文件写入]` | `write_to_file` | `edit_file` | `Write` | `write_to_file` | `write_to_file` | `create_file` | `apply_patch` |
| `[文件编辑]` | `update_file` | `edit_file` | `Edit` | `replace_file_content` | `replace_in_file` | `search_replace` | `apply_patch` |
| `[文件名搜索]` | `—`（用 regex+glob） | `glob_file_search` | `Glob` | `find_by_name` | `list_files` | `search_file` | `—`（通过 `shell`） |
| `[文本搜索]` | `search_by_regex` | `grep` | `Grep` | `grep_search` | `search_files` | `grep_code` | `—`（通过 `shell`） |
| `[语义搜索]` | `search_codebase` | `codebase_search` | `—`（可通过 MCP） | `codebase_search` | `—`（可通过 MCP） | `search_codebase` | `—` |
| `[目录浏览]` | `list_dir` | `list_dir` | `LS` | `list_dir` | `list_files` | `list_dir` | `—`（通过 `shell`） |
| `[联网搜索]` | `web_search` | `web_search` | `WebSearch` | `search_web` | `—`（可通过 MCP） | `search_web` | `—` |
| `[联网抓取]` | `—` | `—` | `WebFetch` | `read_url_content` | `—`（可通过 MCP） | `fetch_content` | `—` |
| `[命令执行]` | `run_command` | `run_terminal_cmd` | `Bash` | `run_command` | `execute_command` | `run_in_terminal` | `shell` |
| `[诊断信息]` | `—` | `read_lints` | `—` | `—` | `—` | `get_problems` | `—` |

> 通用类别定义详见 [tool-invocation-design-guide.md §1](tool-invocation-design-guide.md)。语义自明的工作流原语（`[Task]`/`[AskUserQuestion]`/`[Skill]`）定义和调用规则详见 [tool-invocation-design-guide.md §1](tool-invocation-design-guide.md)。
>
> 生成的 SKILL 默认使用通用类别；若可确定目标平台，按本表替换为平台特定工具名。UR-SKILL 自身文件必须始终保持通用类别。

---

### A.4 平台特定约束

| 平台 | 模型驱动 | 子代理支持 | 关键约束 |
|:---|:---|:---|:---|
| **Trae** | 多模型 | ✅ 多代理体系（Coordinator→Sub→Specialist）；`.trae/agents/` 自定义 | 中文原生优化；SOLO/Builder 双模式；snake_case 工具命名 |
| **Cursor** | GPT-4.1 + 多模型 | ✅ Explore / Bash / Browser + `.cursor/agents/*.md`（最多4并发） | VS Code fork；chatml 格式；TypeScript namespace 定义 |
| **Claude Code** | Claude Sonnet/Haiku | ✅ Agent 工具（5 种内置）+ `.claude/agents/*.md` 自定义 | CLI 优先；git 安全协议严格；PascalCase 工具命名 |
| **Windsurf** | SWE-1.5（Devin Local） | ⚠️ Cascade 已 EOL（2026-07-01），Devin Local 内生并行 | 产品更名 Devin Desktop；ACP 协议支持第三方代理 |
| **CodeBuddy** | 腾讯云驱动 | ✅ Subagents（agentic/manual）+ `.codebuddy/agents/` | 三模式（Ask/Craft/Plan）；Plan 五步生命周期 |
| **Qoder** | 通义大模型 | ✅ Experts Mode（Lead + 7 专家）+ Quest 2.0 | 前身通义灵码；2026-05-20 更名 Qoder CN |
| **Codex CLI** | OpenAI | ✅ MultiAgentV2 + Sandbox 审批体系 | 核心仅 3 工具；大部分操作通过 `shell` 间接完成 |

---

### A.5 子Agent 部署路径

UR-SKILL 的 3 个子Agent（[research-analyst](../../agent/research-analyst.md)、[tech-documentation](../../agent/tech-documentation.md)、[script-engineer](../../agent/script-engineer.md)）为通用 Markdown 格式，使用通用工具类别。部署到各平台时，将对应 `agent/*.md` 文件复制到平台的 Agent 目录下即可：

| 平台 | Agent 目录 | 部署说明 |
|:---|:---|:---|
| **Trae** | `.trae/agents/` | 将 3 个 `.md` 文件放入项目根目录的 `.trae/agents/`；Agent 间可通过多代理体系互相调用 |
| **Cursor** | `.cursor/agents/` | 放入 `.cursor/agents/`；主Agent 自动发现并调用，最多 4 并发 |
| **Claude Code** | `.claude/agents/` | 放入 `.claude/agents/`；通过 `Agent` 工具显式启动，支持并发 |
| **CodeBuddy** | `.codebuddy/agents/` | 放入 `.codebuddy/agents/`；支持 agentic 自动委派或 manual 手动切换 |
| **Windsurf** | Devin Local 内生 | 无用户级 agents 目录；子代理由引擎内部分配，用户无需手动部署 |
| **Qoder** | Experts Mode 内置 | 专家角色内置，不需外部 agent 文件；若需自定义子代理，通过 Quest 配置 |
| **Codex CLI** | Hook 定义 | 通过 `SubagentStart` Hook 事件触发，无静态 agents 目录 |

> **原则**：`agent/` 下为通用源码（保持通用工具类别），部署到平台时直接复制，无需修改工具名——平台自动映射通用类别到具体工具。不支持 agents 目录的平台（Windsurf/Qoder/Codex CLI）通过各自的内置机制覆盖子代理需求。

---

### A.6 格式迁移检查清单

将 Markdown 默认 SKILL 适配到特定平台时，验证：

- [ ] 身份保持：角色定义和核心任务不变
- [ ] 能力矩阵保持：所有领域和层级完整
- [ ] 工作流步骤保持：编号和逻辑不变
- [ ] RFC 2119 关键字保持：MUST/SHOULD/MAY 完整
- [ ] 检查清单保持：`- [ ]` 项全部保留
- [ ] 盲区机制保持：三层处理流程完整
- [ ] 仅调整结构语法：章节标题、分隔符、输出格式规范
- [ ] 无内容丢失：重新格式化过程中未遗漏任何规则
