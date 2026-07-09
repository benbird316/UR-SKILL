# 示例

> 用途：展示 UR-SKILL 在不同复杂度下的输出形态
> 核心原则：示例只展示结构与关键设计决策，不替代 references/ 中的模板

---

## 示例 1：简单 SKILL（无 references/）

**用户输入**：
> 写一个把自然语言描述转成 Python 函数名的 SKILL。

**核心任务**：标识符生成工程

**输出结构**：

```yaml
---
name: pythonize-name
description: "Use when converting a natural language description into a valid Python function or variable name. Invoke for naming helpers, refactoring suggestions, or API method naming."
metadata:
  updated: 2026-07-09
  type: prompt
  whenToUse: 当用户想把自然语言描述转成合法的 Python 函数名或变量名时
---
```

```markdown
# pythonize-name

> 角色：你是 Python 命名工程师。将自然语言描述转换为符合 PEP 8 的函数/变量名。

## 能力矩阵

**核心领域**：标识符生成工程

| 领域 | 基础层 | 进阶层 | 高阶层 | 拓展层 |
|:---|:---|:---|:---|:---|
| 核心：标识符生成工程 | 识别关键词 | 去停用词与缩写 | 处理多义词与歧义 | 推断项目命名风格 |

**辐射领域**：

| 领域 | 基础层 | 进阶层 | 高阶层 | 拓展层 |
|:---|:---|:---|:---|:---|
| 需求解析 | 提取动作与对象 | 识别隐含参数 | 处理否定与条件 | 推断用户真实意图 |
| B 命名规范 | 掌握 PEP 8 | 区分 public/private | 处理缩写与首字母 | 适配团队约定 |
| C 格式约束 | 转小写/下划线 | 处理特殊字符 | 截断超长名称 | 保证可读性 |

## 工作流

1. 解析（3 维）：提取原始描述与约束
2. 执行（3 维）：生成候选名称
3. 校验（6 维）：检查 PEP 8、可读性、唯一性
4. 交付（3 维）：输出排序后的候选列表

## 规则

- **MUST** 输出小写下划线格式
- **MUST NOT** 使用 Python 保留字
- **SHOULD** 优先使用动词开头

## 风险边界声明

| 编号 | 声明 |
|:---|:---|
| 风险边界-01 | 不生成侮辱性、歧视性或违法名称 |
| 风险边界-02 | 不生成可能造成安全误导的名称 |
| 风险边界-03 | 不执行任何外部代码 |
```

**Rationale**：简单 SKILL 的核心任务单一（命名转换），辐射领域 3 个即可覆盖，无需外部知识库或独立 references/。工作流简化为 4 步，规则仅 3 条，全部内联在 body 中。

**边界说明**：本示例假设用户输入是中文/英文自然语言，输出为 Python 标识符；不处理其他编程语言命名规范。

---

## 示例 2：中等 SKILL（+ references/）

**用户输入**：
> 写一个 Kubernetes 容器安全基线调研的 SKILL，要引用官方文档和 NSA/CISA 指南。

**核心任务**：联网调查分析报告工程

**输出结构要点**：

- `references/source-evaluation-guide.md`：来源分级标准
- `references/output-template.md`：报告结构模板
- `references/examples.md`：更多示例
- body 中保留：能力矩阵、工作流、规则、风险边界

**能力矩阵设计要点**：

| 类型 | 示例 |
|:---|:---|
| 核心领域 | 联网调查分析工程 |
| 辐射领域 | 研究方法论、信息检索工程、来源评估、证据综合、报告设计、质量治理 |

注意：辐射领域是独立专业能力，而不是“解析→检索→评估→写作”这种流水线。

**Rationale**：中等复杂度 SKILL 依赖外部知识库（NSA/CISA 指南、Kubernetes 官方文档），需要将来源分级、报告结构、更多示例下沉到 references/，避免 body 超过 500 行。辐射领域 6 个覆盖调研分析的完整链路。

**边界说明**：本示例聚焦容器安全基线调研，不覆盖运行时入侵检测、漏洞利用验证或具体环境的配置下发。

---

## 示例 3：复杂 SKILL（+ references/ + scripts/ + assets/）

**用户输入**：
> 做一个 Python 代码审查 SKILL，能调用 pylint/mypy 做静态检查，还能输出带行号的 Markdown 报告。

**核心任务**：Python 代码质量保障工程

**输出结构要点**：

- `scripts/run_linters.py`：调用 pylint/mypy 并解析输出
- `assets/report-template.md`：报告模板
- `references/domain-knowledge/`：Python 安全漏洞模式、PEP 8 规范
- body 中保留：能力矩阵、工作流、规则、风险边界、脚本调用说明

**Rationale**：复杂 SKILL 需要调用外部可执行脚本（pylint/mypy）、使用静态报告模板，并依赖大量领域知识（PEP 8、OWASP Python Top 10）。这些资源必须拆分到 scripts/、assets/、references/，实现渐进式加载。

**边界说明**：本示例聚焦静态代码审查，不执行被审查代码，也不替代安全渗透测试或人工代码评审。

---

## 常见错误示例

### 错误：能力矩阵写成工作流

```markdown
**辐射领域**：
| A 解析需求 | ... |
| B 检索资料 | ... |
| C 评估来源 | ... |
| D 生成报告 | ... |
```

**问题**：这些是按时间顺序的工作流步骤，不是独立能力域。排序后会破坏逻辑。

**修正**：改为独立专业能力，例如“研究方法论”“信息检索工程”“来源评估学”“知识综合”“报告设计”。
