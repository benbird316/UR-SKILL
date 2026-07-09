# 输出模板

> 用途：根据生成的 SKILL 复杂度，选择对应输出结构
> 核心原则：输出规格必须包含格式类型、输出结构、问题分级、判决策略、用户交互模式
> 设计方法详见 [design-guides/output-content-design-guide.md](../design-guides/output-content-design-guide.md)

---

## 1. 简单复杂度（单文件，4 步）

```yaml
---
name: {kebab-case-name}
description: "Use when [触发条件]. [能力说明]"
type: prompt
whenToUse: 当[具体场景]时
metadata:
  updated: {YYYY-MM-DD}
---

# {SKILL名称}

## 能力矩阵

（核心领域 1 个 + 辐射领域由任务分析确定，推荐 4-8 个，每个 4 层：基础 → 进阶 → 高阶 → 拓展）

### 核心领域

| 领域 | 基础层 | 进阶层 | 高阶层 | 拓展层 |
|:---|:---|:---|:---|:---|
| 核心：{核心领域名} | ... | ... | ... | ... |

### 辐射领域

| 领域 | 基础层 | 进阶层 | 高阶层 | 拓展层 |
|:---|:---|:---|:---|:---|
| A {领域1} | ... | ... | ... | ... |
| B {领域2} | ... | ... | ... | ... |
| C {领域3} | ... | ... | ... | ... |
| ... | ... | ... | ... | ... |

## 能力切面

（只针对核心领域，6 个切面）

- **切面1 效率成本**：...
- **切面2 知识深耕**：...
- **切面3 风险识别**：...
- **切面4 质量检验**：...
- **切面5 领域融合**：...
- **切面6 系统全局**：...

## 工作流

1. 解析（3 维）
   - 动作：...
   - 检查清单：...
   - 任一未确认 → 补齐 → 返回确认 → 全部确认 → 进入 2

2. 执行（3 维）
   - 动作：...
   - 检查清单：...
   - 任一未确认 → 补齐 → 返回确认 → 全部确认 → 进入 3

3. 校验（6 维，关键节点）
   - 动作：...
   - 检查清单：...
   - 任一未确认 → 补齐 → 返回确认 → 全部确认 → 进入 4

4. 交付（3 维）
   - 动作：...
   - 检查清单：...
   - 任一未确认 → 补齐 → 返回确认 → 全部确认 → 完成交付

## 输出规范

{自然语言/结构化/混合，简短描述}

## 规则

### 硬约束

- **MUST** ...
- **MUST** ...

### 硬禁止

- **MUST NOT** ...
- **MUST NOT** ...

### 强偏好

- **SHOULD** ...
- **SHOULD NOT** ...

### 可选

- **MAY** ...

## 风险边界声明

> 格式详见 [templates/boundary-template.md](../templates/boundary-template.md)

| 编号 | 声明 |
|:---|:---|
| 风险边界-01 | {该 SKILL 不可逾越的安全红线} |
| 风险边界-02 | {该 SKILL 不可逾越的安全红线} |
| 风险边界-03 | {该 SKILL 不可逾越的安全红线} |

## 专业边界声明

> 格式详见 [templates/boundary-template.md](../templates/boundary-template.md)

| 编号 | 声明 |
|:---|:---|
| 专业边界-01 | {该 SKILL 不得越界的专业领域限制} |

## 示例

### 示例1：{场景}
**Input**：...
**Output**：...
```

---

## 2. 中等复杂度（+ references/，6 步）

```yaml
---
name: {kebab-case-name}
description: "Use when [触发条件]. [能力说明]"
type: prompt
whenToUse: 当[具体场景]时
metadata:
  updated: {YYYY-MM-DD}
---

# {SKILL名称}

## 能力矩阵

（核心领域 1 个 + 辐射领域由任务分析确定，推荐 4-8 个，每个 4 层）

## 能力切面

（只针对核心领域，6 个切面）

## 工作流

1. 解析（3 维）
2. 调研（6 维，关键节点）
3. 架构（6 维，关键节点）
4. 执行（3 维）
5. 校验（6 维，关键节点）
6. 交付（3 维）

## 输出规范

> 参照 ../design-guides/output-content-design-guide.md 设计输出内容

### 输出格式
- **格式类型**：{问题表格 + 执行摘要 / Mermaid 流程图 + 表格 / 检查清单 / ...}
- **强制可视化**：{是/否}

### 输出结构
1. 执行摘要（判决 + 风险等级 + 关键发现）
2. {主体输出区块}
3. {正面观察 / 推荐行动}

### 问题分级
| 等级 | 标识 | 定义 | 动作 |
|:---|:---|:---|:---:|
| 极危 | [Critical] | 安全漏洞/数据损失/破坏性 Bug | 阻断合入 |
| 高危 | [High] | 重大功能缺陷 | 合入前必须修复 |
| 中危 | [Medium] | 明显代码坏味/架构问题 | 合入前建议修复 |
| 低危 | [Low] | 轻微改进建议 | 可后续优化 |

### 判决策略
参照 ../design-guides/output-content-design-guide.md §4.3

### 用户交互
- **模式**：{一次性报告 / 确认-修复-验证循环 / ...}
- **循环轮数**：{N}

### 输出文件
- **路径**：{`docs/{type}/{scope}-{date}.md`}

## 规则

硬约束 + 硬禁止 + 强偏好 + 可选 + 风险边界声明

## 风险边界声明

> 格式详见 [templates/boundary-template.md](../templates/boundary-template.md)

| 编号 | 声明 |
|:---|:---|
| 风险边界-01 | {该 SKILL 不可逾越的安全红线} |
| 风险边界-02 | {该 SKILL 不可逾越的安全红线} |
| 风险边界-03 | {该 SKILL 不可逾越的安全红线} |

## 专业边界声明

> 格式详见 [templates/boundary-template.md](../templates/boundary-template.md)

| 编号 | 声明 |
|:---|:---|
| 专业边界-01 | {该 SKILL 不得越界的专业领域限制} |
| 专业边界-02 | {该 SKILL 不得越界的专业领域限制} |

## 参考引用

- 输出模板：../templates/output-template.md
- 输出内容设计指南：../design-guides/output-content-design-guide.md
- 示例：../examples/examples.md
- 反模式：../References/anti-patterns.md
- 故障诊断：../References/troubleshooting.md

## 工具参考

> 本 SKILL 使用的工具及调用示例（中等复杂度须包含此表）：

| 步骤 | 工具 | 调用示例 | 用途 |
|:---|:---|:---|:---|
| N. {步骤名} | `{工具名}` | `{示例参数}` | {用途说明} |
```

---

## 3. 复杂复杂度（+ references/ + scripts/ + assets/，7 步+）

```yaml
---
name: {kebab-case-name}
description: "Use when [触发条件]. [能力说明]"
type: prompt
whenToUse: 当[具体场景]时
metadata:
  updated: {YYYY-MM-DD}
---

# {SKILL名称}

## 能力矩阵

（核心领域 1 个 + 辐射领域由任务分析确定，推荐 4-8 个，每个 4 层）

## 能力切面

（只针对核心领域，6 个切面）

## 工作流

1. 解析（3 维）
2. 调研（6 维，关键节点）
3. 架构（6 维，关键节点）
4. 执行（3 维）
5. 校验（6 维，关键节点）
6. 验证（6 维，关键节点）
7. 交付（3 维）

## 输出规范

> 参照 ../design-guides/output-content-design-guide.md 设计输出内容

### 输出格式
- **格式类型**：{问题表格 + 执行摘要 + Mermaid 图表 + 代码块 / ...}
- **强制可视化**：{是/否} → 满足条件时要求 Mermaid 图表

### 可视化要求（若强制）
- **Mermaid {类型}**：展示 {内容}（{flowchart / sequenceDiagram / stateDiagram}）
- **最少 {N} 张图**：复杂场景追加 {额外图类型}
- **配色**：`fill:#{填充色},color:#{文字色}` 每个节点显式指定

### 输出结构
1. 执行摘要（判决 + 风险等级 + 关键发现）
2. {主体输出区块}（表格 / 图表 / 分级清单）
3. 正面观察（至少 1 条）
4. 推荐行动（合入前必须 / 合入后建议 / 后续优化）

### 问题分级
| 等级 | 标识 | 定义 | 动作 |
|:---|:---|:---|:---|
| 极危 | [Critical] | 安全漏洞/数据损失/破坏性 Bug | 阻断合入 |
| 高危 | [High] | 重大功能缺陷 | 合入前必须修复 |
| 中危 | [Medium] | 明显代码坏味/架构问题 | 合入前建议修复 |
| 低危 | [Low] | 轻微改进建议 | 可后续优化 |

### 判决策略
| 极危 | 高危 | 判决 |
|:---|:---|:---|
| > 0 | 任意 | 驳回 |
| 0 | > 3 | 需修改 |
| 0 | 1-3 | 有条件通过 |
| 0 | 0 | 通过 |

### 用户交互
- **模式**：{确认-修复-验证循环 / 分阶段交付 / ...}
- **交互工具**：{AskUserQuestion} → 提供 [{选项A}/{选项B}/{选项C}] 选项
- **循环轮数**：最多 {N} 轮

### 输出文件
- **路径**：{`docs/{type}/{scope}-{date}.md`}
- **格式**：Markdown，UTF-8

## 规则

硬约束 + 硬禁止 + 强偏好 + 可选 + 风险边界声明 + 专业边界声明 + 领域特殊规则

## 风险边界声明

> 格式详见 [templates/boundary-template.md](../templates/boundary-template.md)

| 编号 | 声明 |
|:---|:---|
| 风险边界-01 | {该 SKILL 不可逾越的安全红线} |
| 风险边界-02 | {该 SKILL 不可逾越的安全红线} |
| 风险边界-03 | {该 SKILL 不可逾越的安全红线} |

## 专业边界声明

> 格式详见 [templates/boundary-template.md](../templates/boundary-template.md)

| 编号 | 声明 |
|:---|:---|
| 专业边界-01 | {该 SKILL 不得越界的专业领域限制} |
| 专业边界-02 | {该 SKILL 不得越界的专业领域限制} |

## 参考引用

- 输出模板：../templates/output-template.md
- 输出内容设计指南：../design-guides/output-content-design-guide.md
- 示例：../examples/examples.md
- 反模式：../References/anti-patterns.md
- 故障诊断：../References/troubleshooting.md
- 可执行脚本：scripts/
- 静态资源：assets/

## 工具参考

> 本 SKILL 使用的工具及调用示例（复杂复杂度须包含此表，含降级路径）：

| 步骤 | 工具 | 调用示例 | 用途 | 降级 |
|:---|:---|:---|:---|:---|
| N. {步骤名} | `{工具名}` | `{示例参数}` | {用途说明} | `↘ {降级工具}` |
```

---

## 4. 输出约束（通用）

- body 必须 < 500 行
- YAML frontmatter 必须完整（name, description, type, whenToUse, metadata.updated）
- description 强烈推荐以 "Use when..." 开头
- 不得将 references/ 内容直接填充到 body 中
- 目录名使用复数形式：references/、scripts/、assets/
- 校验节点无论复杂度必须 6 维全开
- 关键节点（调研、架构、校验、验证）6 维全开
- 非关键节点（解析、执行、交付）3 维
- 能力矩阵：核心领域 1 个，辐射领域数量由任务分析确定（推荐 4-8 个，最少 3 个，最多 8 个），与复杂度独立
- 能力矩阵：每个领域 4 层深度（基础 → 进阶 → 高阶 → 拓展），所有复杂度
- 能力切面：只针对核心领域，6 个切面
- 风险边界声明：安全红线（数量由领域安全需求决定，通常 3-5 条）
- 专业边界声明：越界防护（数量由领域范围决定，通常 1-3 条）
- 中等及以上复杂度 `type` 为 `hybrid` 或 `tool` 的 SKILL：必须包含集中式工具参考表
- 可执行动作格式：`[工具名] 操作 → 输出`（`prompt` 类型 SKILL 豁免）
- 审查/测试类 SKILL（审查/评审/测试/审计类）输出规范：必须包含输出格式类型、强制可视化检查、问题分级（极危/高危/中危/低危）、判决策略、用户交互模式（参照 ../design-guides/output-content-design-guide.md）
- 触发强制可视化的 SKILL：Mermaid 图表颜色必须显式指定（`fill:#xxx,color:#xxx`），禁止依赖主题默认色
- 审查类 SKILL：输出结构必须包含执行摘要 + 正面观察 + 推荐行动
