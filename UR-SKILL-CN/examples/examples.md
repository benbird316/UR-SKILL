# 示例

> 用途：UR-SKILL 自带的真实生产级示例，全部由 UR-SKILL 方法论设计并通过验证，可直接参考或复用
> 核心原则：示例是完整可运行的 SKILL / Agent，不是结构示意图

---

## 示例总览

| 示例 | 位置 | 类型 | 特点 | 适合参考 |
|:---|:---|:---|:---|:---|
| 调查分析师 Agent | `agent/research-analyst.md` | 子 Agent（单文件） | 聚焦联网调研与信息综合，标准 4 主节点工作流 | 子 Agent 设计、调研类技能、门控节点写法 |
| 技术文档工程师 Agent | `agent/tech-documentation.md` | 子 Agent（单文件） | 聚焦结构化文档生成，能力矩阵 + 输出规范完整 | 文档类技能、输出规格设计 |
| 脚本工程师 Agent | `agent/script-engineer.md` | 子 Agent（单文件） | 聚焦代码生成与验证，风险边界严格 | 代码类技能、安全边界设计、校验节点 |
| UR-SKILL 自身 | 当前安装的语言目录 | 完整 SKILL 包（SKILL.md + design-guides/ + templates/ + References/ + agent/ + Scripts/） | 13 步工作流 + 3 Agent + 15+ 设计指南 + 9 模板 + 运行时参考，由自身方法论生成并通过自校验 | 完整 SKILL 包结构、能力矩阵四层设计、工作流门控、自包含引用

---

## 示例 1：调查分析师 Agent（子 Agent）

**位置**：`agent/research-analyst.md`

**核心领域**：联网调查分析工程

**参考价值**：
- 子 Agent 的标准单文件结构
- 调研类技能的能力矩阵设计
- 门控节点（调研、校验、验证）的 6 维检查清单写法
- 来源分级与交叉验证方法论

**结构特点**：单文件 SKILL，无独立 references/，全部知识内联。适合任务单一、领域知识量不大的场景。

---

## 示例 2：技术文档工程师 Agent（子 Agent）

**位置**：`agent/tech-documentation.md`

**核心领域**：技术文档生成工程

**参考价值**：
- 文档类技能的输出规范设计
- 结构化输出的格式约束
- 从需求分析到文档交付的完整链路

**结构特点**：单文件 SKILL，聚焦输出质量与格式一致性。

---

## 示例 3：脚本工程师 Agent（子 Agent）

**位置**：`agent/script-engineer.md`

**核心领域**：自动化脚本工程

**参考价值**：
- 代码生成类技能的风险边界设计
- 验证节点的对抗测试思路
- 执行-校验-验证的反思闭环

**结构特点**：单文件 SKILL，风险边界严格，强调安全执行。

---

## 示例 4：UR-SKILL 自身（完整的生产级 SKILL 包）

**位置**：当前安装的语言目录（即 `SKILL.md` 所在目录）

**核心领域**：SKILL 生成工程

**参考价值**：
- 完整 SKILL 包的标准化目录结构
- 能力矩阵四层设计的具体实现（核心领域 + 6 辐射领域 × 4 层）
- 4 主节点 + 13 子步骤的完整工作流（分析→执行→反思→交付）
- 门控节点（步骤 10-12）的 6 维检查清单写法
- 15+ 设计指南的组织方式与交叉引用
- 9 个模板文件的示例填充
- 3 个子 Agent 的能力矩阵与工作流设计
- 盲区三层处理机制、Loop 循环原则、风险边界声明
- 自包含引用（所有 `./` 引用均指向 SKILL 包内部文件）

**目录结构**：
```
UR-SKILL-CN/
├── SKILL.md                      # 主文件（能力架构 + 工作流 + 规则）
├── design-guides/                # 设计指南（生成方法论的具体规则）
│   ├── skill-package-design-guide.md
│   ├── capability-design-guide.md
│   ├── workflow-design-guide.md
│   ├── structure-design-guide.md
│   ├── output-design-guide.md
│   ├── tool-invocation-design-guide.md
│   ├── identity-design-guide.md
│   ├── boundary-design-guide.md
│   ├── rules-design-guide.md
│   ├── ref-types-design-guide.md
│   ├── glossary-design-guide.md
│   ├── examples-design-guide.md
│   ├── scripts-design-guide.md
│   ├── assets-design-guide.md
│   └── spec-design-guide.md
├── templates/                    # 模板文件
│   ├── skill-template.md
│   ├── capability-architecture-template.md
│   ├── workflow-template.md
│   ├── metadata-spec.md
│   ├── identity-template.md
│   ├── boundary-template.md
│   ├── rules-template.md
│   ├── scripts-template.md
│   └── assets-template.md
├── References/                   # 运行时参考（反模式 + 故障诊断 + 术语表）
│   ├── anti-patterns.md
│   ├── troubleshooting.md
│   └── glossary.md
├── agent/                        # 子 Agent（调查分析 + 技术文档 + 脚本自动化）
│   ├── research-analyst.md
│   ├── tech-documentation.md
│   └── script-engineer.md
├── Scripts/                      # 校验脚本
│   ├── validate_skill.py
│   ├── validator_format.py
│   ├── validator_content.py
│   ├── validator_runtime.py
│   └── bilingual_sync.py
└── examples/                     # 本文件
    └── examples.md
```

**自吃狗粮说明**：UR-SKILL 本身由其自身方法论设计生成，并通过自校验（test_self_validate.py）确保格式、内容、运行时三层验证全部通过。查看 UR-SKILL 自身的 SKILL.md 就是从方法论到产物的最佳端到端示例。

---

## 如何选择参考对象

| 你的场景 | 优先参考 |
|:---|:---|
| 做一个简单的单文件技能 | 3 个子 Agent 中的任意一个 |
| 做调研 / 信息收集类技能 | 调查分析师 Agent |
| 做文档 / 内容生成类技能 | 技术文档工程师 Agent |
| 做代码 / 脚本类技能 | 脚本工程师 Agent |
| 做完整的生产级 SKILL 包 | UR-SKILL 自身的 SKILL.md + 目录结构 |
| 学习设计指南如何组织 | UR-SKILL 的 design-guides/ 目录 |
| 学习工作流门控的写法 | UR-SKILL 的步骤 10-12（校验→验证→循环判定） |
