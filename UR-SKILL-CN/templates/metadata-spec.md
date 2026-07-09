# 元数据规范

> 用途：定义 SKILL.md YAML frontmatter 的字段、类型、约束与示例
> 核心原则：frontmatter 是 SKILL 的触发层与身份层，必须精简、可机械解析、触发友好
> 符合标准：[agentskills.io Specification](https://agentskills.io/specification)

---

## 字段定义

### 必填字段（agentskills.io 标准）

| 字段 | 类型 | 必填 | 约束 | 说明 |
|:---|:---|:---:|:---|:---|
| `name` | string | 是 | 1–64 字符，kebab-case，全小写，无空格；必须匹配父目录名 | SKILL 唯一标识符 |
| `description` | string | 是 | 1–1024 字符；强烈推荐以 `Use when...` 开头；覆盖能力 + 触发场景 | 触发条件与能力说明 |

### 可选字段（agentskills.io 标准）

| 字段 | 类型 | 必填 | 约束 | 说明 |
|:---|:---|:---:|:---|:---|
| `license` | string | 否 | SPDX 标识符或许可证文件名，建议 ≤50 字符 | 许可证声明 |
| `compatibility` | string | 否 | 1–500 字符，声明所需环境 | 兼容性说明（平台、Python 版本等） |
| `metadata` | dict | **是** | 至少含 `updated` 字段 | 任意键值对，扩展信息 |
| `allowed-tools` | string | 否 | 空格分隔的工具名列表（试验性字段） | 预批准的工具白名单 |

### UR-SKILL 自定义字段（存放在 `metadata` 下）

| 字段 | 类型 | 必填 | 约束 | 说明 |
|:---|:---|:---:|:---|:---|
| `metadata.type` | string | 是 | 枚举值：`prompt` / `tool` / `hybrid` | SKILL 类型（UR-SKILL 自定义） |
| `metadata.whenToUse` | string | 是 | 中文，20–100 字符，具体场景 | 补充触发场景（UR-SKILL 自定义） |
| `metadata.updated` | string (date) | 是 | 格式 `YYYY-MM-DD` | 最后更新时间 |

> **设计原则**：agentskills.io 标准只定义 `name`、`description` 为必填。`metadata` 用于承载 UR-SKILL 自身的扩展字段（`type`、`whenToUse` 等），不影响标准合规性。

---

## 约束说明

- `description` 应稍微 **pushy**：在描述能力的同时，主动覆盖用户可能使用的同义表达，降低 undertrigger 概率。
- `metadata.type` 决定后续输出结构：
  - `prompt`：纯提示词 SKILL，无脚本/资源。
  - `tool`：包含可执行脚本或 MCP 调用。
  - `hybrid`：提示词 + 脚本/资源混合。
- `license` 建议使用标准 SPDX 标识符（如 `Apache-2.0`、`MIT`）。
- `compatibility` 仅当 SKILL 有特殊环境需求时才需要填写，大多数 SKILL 不需要。
- 不得在 frontmatter 中引入未声明字段，避免解析失败。

---

## 示例

### 最简示例（agentskills.io 标准合规）

```yaml
---
name: python-code-review
description: "Use when the user wants to review Python code for quality, security, style, or performance. Invoke for code inspection, bug hunting, refactoring suggestions."
---
```

### 完整示例（UR-SKILL 推荐）

```yaml
---
name: python-code-review
description: "Use when the user wants to review Python code for quality, security, style, or performance. Invoke for code inspection, bug hunting, refactoring suggestions, or CI-ready linting tasks."
license: Apache-2.0
compatibility: Requires Python 3.12+
allowed-tools: Read Write Grep Glob RunCommand
metadata:
  updated: 2026-07-09
  type: prompt
  whenToUse: 当用户需要审查 Python 代码质量、安全漏洞、风格或性能时
---
```

---

## 校验规则

- `name` 必须匹配正则 `^[a-z0-9]+(?:-[a-z0-9]+)*$`
- `description` 长度必须在 1–1024 字符之间
- `metadata.type` 必须是 `prompt` / `tool` / `hybrid` 之一
- `metadata.updated` 必须是合法日期 `YYYY-MM-DD`
