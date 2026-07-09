# 工具调用设计指南

> 用途：指导 UR-SKILL 在生成 SKILL 时，将抽象"动作"映射为具体工具调用。定义工具选型、调用模式、降级策略的完整规范。
> 核心原则：动作是"做什么"，工具是"用什么做"——每一条可执行的动作必须绑定至少一个工具或降级路径。

---

## 1. 为什么需要工具调用设计

**问题**：当前 UR-SKILL 生成的 FL 技能在工作流中只有抽象动作描述：

```
动作：读取代码 diff，分析变更范围
```

Agent 看到这个不知道用哪个工具去"读取代码 diff"——是用 `git diff` 还是读文件？是 `Read` 还是 `SearchCodebase`？

**结果**：生成的 SKILL 变成纯粹的方法论文档，Agent 执行时依赖自身判断，而非 SKILL 指引，导致执行不稳定。

**解决方案**：在生成 SKILL 时，为每个可执行动作绑定具体工具和调用参数。

---

## 2. 工具分类与选型矩阵

### 2.1 工具全景

将 Agent 可用工具按操作类型分为 7 大类：

| 类别 | 工具 | 适用场景 | 输入要求 |
|:---|:---|:---|:---|
| **文件读取** | `Read` | 读取已知路径的文件内容 | 绝对路径 |
| **文件搜索** | `Glob` | 按文件名模式查找文件 | glob 模式 |
| **文本搜索** | `Grep` | 按正则搜索文件内容 | 正则 + 路径 |
| **语义搜索** | `SearchCodebase` | 按意图/概念查找代码 | 自然语言问题 |
| **目录浏览** | `LS` | 列出目录结构 | 绝对路径 |
| **联网搜索** | `WebSearch` | 获取网络实时信息 | 搜索关键词 |
| **联网抓取** | `WebFetch` | 获取指定 URL 内容 | URL |
| **命令执行** | `RunCommand` | 运行 Shell 命令（git/build/test） | 命令字符串 |
| **文件写入** | `Write` | 创建新文件 | 路径 + 内容 |
| **文件编辑** | `SearchReplace` | 精确替换文件内容 | 路径 + old_str + new_str |
| **文件删除** | `DeleteFile` | 删除文件 | 路径列表 |

### 2.2 选型决策矩阵

| 用户需求 | 推荐工具 | 次选 | 不推荐 |
|:---|:---|:---|:---|
| 搜索某个类的实现 | `SearchCodebase` | `Grep` | `Glob` |
| 查找所有 `.ts` 文件 | `Glob` | `LS` | `Grep` |
| 阅读已知文件 | `Read` | — | `Grep` / `RunCommand cat` |
| 搜索字符串 "todo" | `Grep` | — | `SearchCodebase` |
| 了解代码库架构 | `SearchCodebase` | `Glob` + `Read` | `Grep` |
| 获取外部最新信息 | `WebSearch` | `WebFetch` | — |
| 运行测试 | `RunCommand` | — | — |
| 获取 git diff | `RunCommand` (`git diff`) | — | — |
| 修改代码 | `SearchReplace` | `Write` | — |
| 列出项目结构 | `LS` | `Glob` | `RunCommand ls` |

### 2.3 禁止行为

- **MUST NOT** 在动作中用 `cat`/`head`/`tail`/`find`/`grep`/`sed`/`awk` 替代专用工具
- **MUST NOT** 在动作中写"读取文件"而不指定工具名
- **MUST NOT** 跨类别混用工具（如用 `WebSearch` 搜索本地代码）

---

## 3. 动作-工具映射规范

### 3.1 标准映射格式

在 SKILL 工作流的"动作"中，使用以下格式：

```
动作：
1. [工具名] 读取用户输入 → 提取 {输出物}
2. [工具名] 获取 {输入材料} → {输出物}
3. [工具名] 检查 {内容} → {结论}
```

**正确示例**（工具显式绑定）：

```
动作：
1. Read 读取用户需求描述 → 提取任务类型与目标系统
2. RunCommand `git diff origin/HEAD...` → 获取代码变更清单
3. Glob `**/*.py` 枚举变更文件 → 确定审查范围
4. SearchCodebase "where is input validation located?" → 定位现有校验器
```

**错误示例**（仅有抽象描述）：

```
动作：
1. 读取用户需求，提取任务类型
2. 获取代码变更清单
3. 确定审查范围
4. 定位现有校验器
```

### 3.2 参数化规范

当工具需要参数时，在动作中给出**示例参数**，让 Agent 知道应该传什么：

| 动作描述 | 工具 | 示例参数 |
|:---|:---|:---|
| 获取当前分支变更 | `RunCommand` | `git diff --name-only origin/HEAD...` |
| 搜索注入漏洞模式 | `Grep` | `pattern:"execute\(|eval\(|exec\(" glob:"*.py"` |
| 联网调查行业标准 | `WebSearch` | `query:"OWASP Top 10 2026"` |
| 理解模块职责 | `SearchCodebase` | `"What is the responsibility of AuthService?"` |

### 3.3 组合调用模式

多个工具组合完成一个逻辑步骤时，使用缩进表示组合关系：

```
动作：
1. 确定审查范围：
   a. RunCommand `git diff --merge-base origin/HEAD` → 获取 diff
   b. RunCommand `git diff --name-only origin/HEAD...` → 枚举变更文件
   c. 若 a 失败 → RunCommand `git diff HEAD~1`（降级方案）
2. 审查每个变更文件：
   a. Read 读取文件完整内容 → 识别变更上下文
   b. SearchCodebase "what validators exist in this project?" → 获取项目校验模式
```

---

## 4. 降级与容错设计

### 4.1 降级链定义

| 工具 | 首选 | 降级1 | 降级2 | 最后手段 |
|:---|:---|:---|:---|:---|
| 获取 diff | `git diff --merge-base origin/HEAD` | `git diff origin/HEAD...` | `git diff HEAD~1` | `AskUserQuestion` 请求指定范围 |
| 代码搜索 | `SearchCodebase` | `Grep` | `Glob` + `Read` | 声明信息边界 |
| 联网调研 | `WebSearch` | `WebFetch` | 声明知识截止日期 | 请求用户补充 |
| 文件读取 | `Read` | — | — | 声明无法访问 |

### 4.2 降级语法

在动作中标记降级路径：

```
动作：执行联网调查（首选 WebSearch，若不可用则用 WebFetch，若两者不可用则声明知识截止日期）
```

简洁写法：

```
动作：WebSearch（↘ WebFetch）→ 获取行业标准信息
```

### 4.3 不可降级的底线操作

以下操作不存在降级路径，失败必须终止当前步骤：

- `RunCommand` 执行 git 操作获取 diff — diff 是代码审查的输入，无 diff 则无法审查
- `Read` 读取代码文件 — 代码是审查对象，无法读取则无法审查

---

## 5. 按工作流节点类型的工具绑定

### 5.1 解析节点

核心工具：`Read`、`AskUserQuestion`

```
动作：
1. Read 读取用户需求输入 → 提取任务类型/目标系统/交付形式
2. 若信息不足 → AskUserQuestion 询问 [选项A/选项B/选项C/选项D]
```

### 5.2 调研节点

核心工具：`WebSearch`、`WebFetch`、`SearchCodebase`、`Grep`、`Glob`

```
动作：
1. WebSearch query="{关键词}" → 获取行业标准/最佳实践
2. SearchCodebase "what {概念} exists in this project?" → 理解项目现有模式
3. Glob "{pattern}" 枚举相关文件 → 确定调研范围
```

### 5.3 执行节点（代码审查/安全扫描/质量检查类）

核心工具：`RunCommand`、`Read`、`SearchCodebase`、`Grep`

```
动作：
1. RunCommand `git diff --merge-base origin/HEAD` → 获取变更内容
2. Read 读取变更文件完整内容 → 理解上下文
3. SearchCodebase "{问题}" → 查找项目现有校验器/orm/安全模式
4. Grep pattern:"{危险模式}" → 扫描已知漏洞特征
```

### 5.4 校验节点

核心工具：`Grep`（占位符扫描）、`Read`（交叉验证）

```
动作：
1. Grep pattern:"\{.*\}" 扫描输出 → 检查占位符残留
2. Read 对照 References/anti-patterns.md → 逐条比对
```

### 5.5 交付节点

核心工具：`Write`、`SearchReplace`

```
动作：
1. Write 生成最终 SKILL.md → 路径 {output_path}
2. 若修改已有文件 → SearchReplace 精确替换
```

---

## 6. 生成的 SKILL 中工具调用的声明位置

### 6.1 在 actions 中声明（内联）

推荐用于简单任务，工具调用直接写在工作流动作中：

```
### 步骤2：上下文收集【关键节点，6维全开】

动作：
1. RunCommand `git diff --name-only origin/HEAD...` → 列出变更文件
2. Read 逐个读取变更文件 → 获取完整上下文
3. SearchCodebase "what are the existing validation helpers?" → 理解项目校验模式
```

### 6.2 在"工具参考"章节声明（集中式）

推荐用于复杂任务，在 SKILL 末尾添加独立的工具参考区块：

```
## X. 工具参考

本 SKILL 使用的工具及调用示例：

| 步骤 | 工具 | 调用示例 | 用途 |
|:---|:---|:---|:---|
| 2. 收集 diff | `RunCommand` | `git diff --merge-base origin/HEAD` | 获取代码变更 |
| 2. 收集 diff（降级） | `RunCommand` | `git diff origin/HEAD...` | 降级方案 |
| 3. 上下文获取 | `Read` | `Read file_path="{path}"` | 读取文件内容 |
| 4. 项目基线分析 | `SearchCodebase` | `"what security validators exist?"` | 理解现有安全模式 |
```

### 6.3 选择策略

| SKILL 复杂度 | 推荐策略 |
|:---|:---|
| 简单（单文件） | 6.1 内联声明 |
| 中等（+ references/） | 6.1 内联 + 6.2 集中式 |
| 复杂（+ scripts/ + assets/） | 6.2 集中式为主，内联为辅 |

---

## 7. 反模式

| 编号 | 反模式 | 表现 | 修正 |
|:---:|:---|:---|:---|
| 工具反模式1 | 无工具绑定 | 动作只写"读取代码"，不指定用 `Read` 还是 `RunCommand cat` | 每个动作必须以 `[工具名]` 开头 |
| 工具反模式2 | 工具错配 | 用 `WebSearch` 搜索本地代码，用 `Grep` 做语义理解 | 参照 §2.2 选型矩阵，为每个需求匹配正确工具 |
| 工具反模式3 | 无降级路径 | 工具调用无 fallback，单点故障导致整个步骤失败 | 为关键工具调用提供至少 1 个降级路径 |
| 工具反模式4 | 混用专用工具与 Shell | 动作中同时出现 `Read` 和 `cat`、`grep` | 一律使用专用工具，禁止用 Shell 命令替代 |
| 工具反模式5 | 参数空洞 | 写 `WebSearch query:"搜索相关内容"` 无具体关键词 | 参数必须具体，如 `WebSearch query:"OWASP Top 10 2026"` |

---

## 8. 设计流程（UR-SKILL 使用本指南的步骤）

当 UR-SKILL 在执行步骤中生成 SKILL 时，按以下流程为每个工作流步骤绑定工具：

1. **识别步骤类型**：该步骤是解析/调研/执行/校验/交付中的哪一种？
2. **查核心工具表**：参照 §5 找到该节点类型的核心工具
3. **匹配具体参数**：根据 SKILL 的任务领域，填充具体参数（如 `git diff origin/HEAD...`、`"OWASP Top 10"`）
4. **设计降级链**：为关键工具调用添加降级路径（参照 §4.1）
5. **选择声明策略**：根据 SKILL 复杂度选择 §6 中的内联或集中式声明
6. **写入动作**：将工具绑定后的动作写入工作流模板

---

## 9. 能力嵌入规范（动作与能力矩阵对齐）

生成 SKILL 时，动作描述不仅要绑定工具，还要与能力矩阵语义对齐，避免动作与能力域脱节。

### 9.1 基本要求

1. 每个动作必须绑定至少一个具体工具（`[工具名]` 格式），或明确标注为 `[认知操作]`
2. 动作描述应自然地嵌入能力矩阵中的术语，使动作语义与能力域对齐；禁止动作语义与能力矩阵脱节
3. **所有动作都应在描述中声明对应的能力域和层级**，内联格式为：`→ 声明 **{辐射领域}·{层级}**：{输出}`
   - 工具动作（如 `[Read]`/`[Write]`）用**声明**：该动作产出的结果归属于哪个能力域·层级
   - 认知操作（`[认知操作]`）用**激活**：纯推理过程触发了哪个能力域·层级的思维模式
4. **禁止**在步骤头部增加独立的能力调用声明区块（避免混淆能力域与工作流步骤）
5. 动作语义与能力矩阵的映射关系通过术语自然嵌入，而非外部标签
6. 高阶层/拓展层动作（如 LLM 推理、自适应策略、推断缺失领域）必须在步骤5被检验是否有依据支撑

### 9.2 正确示例

```markdown
动作：
1. [Read] 读取 capability-architecture-template.md → 声明 **SKILL 架构设计·基础层**：获取能力矩阵通用骨架
2. [认知操作] 推断隐含需求并判定复杂度 → 激活 **需求工程与业务翻译·高阶层**：复杂度判定结果
3. [Write] 对每个辐射领域执行排序测试（随机重排）→ 声明 **SKILL 架构设计·高阶层**：标记重排后逻辑崩坏的领域
```

### 9.3 错误示例

```markdown
动作：
1. 读取模板
2. 分析需求
```

问题：未绑定工具，且未嵌入能力矩阵术语，无法判断对应哪个能力域与层级。

---

## 10. 完整性检查清单

- [ ] 每个工作流步骤的动作都包含至少 1 个工具调用
- [ ] 工具调用符合选型矩阵（§2.2），无跨类别混用
- [ ] 关键工具调用有降级路径
- [ ] 无 Shell 命令替代专用工具（如用 `cat` 替代 `Read`）
- [ ] 参数具体而非空洞占位符
- [ ] 中等及以上复杂度 SKILL 包含集中式工具参考表
- [ ] 不可降级的底线操作已标记（失败即终止）
- [ ] `AskUserQuestion` 作为最后手段时，提供了具体选项（非"请输入范围"这类空洞提问）
- [ ] 动作语义与能力矩阵对齐，高阶层/拓展层动作有依据支撑