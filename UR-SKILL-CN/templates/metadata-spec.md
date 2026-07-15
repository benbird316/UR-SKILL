# 元数据规范

> 符合标准：[agentskills.io Specification](https://agentskills.io/specification)
> 核心原则：极简。能与所有平台互操作，不引入任何平台特化字段。

---

## 字段定义

| 字段 | 位置 | 必填 | 约束 | 说明 |
|:---|:---|:---:|:---|:---|
| `name` | 顶层 | 是 | 1–64 字符，kebab-case，全小写，必须匹配父目录名 | SKILL 唯一标识符。agentskills.io 标准必填。 |
| `description` | 顶层 | 是 | 1–1024 字符；推荐以 `Use when...` 开头 | **触发匹配的唯一字段**。所有平台用此字段决定是否加载 SKILL。应同时覆盖能力描述和触发场景。 |
| `metadata.updated` | metadata 内 | 是 | 格式 `YYYY-MM-DD` | 最后更新时间。两个用途：① 版本变迁追踪；② 让 LLM 感知数据新鲜度，判断领域知识是否可能过时。UR-SKILL 约定必填。 |

> **以上三字段，仅此而已。**



---

## 示例

### UR-SKILL 自身

```yaml
---
name: ur-skill-cn
description: "Use whenever the user wants to create, design, standardize, or package a SKILL.md file, AI agent skill, or structured system prompt. Invoke even if they don't explicitly say 'SKILL'. Chinese version."
metadata:
  updated: 2026-07-09
---
```

### 通用技能示例

```yaml
---
name: python-code-review
description: "Use when the user wants to review Python code for quality, security, style, or performance. Invoke for code inspection, bug hunting, refactoring suggestions."
metadata:
  updated: 2026-07-14
---
```

### 子技能示例（内联调用）

```yaml
---
name: research-analyst
description: >-
  当需要分析用户需求、优化已有SKILL、从知识库提取知识、或本地化外部SKILL时使用。
  支持四种模式（A/B/C/D），输出统一格式的前置分析报告。
  模式 A 通常由 UR-SKILL 内联调用；模式 B/C/D 可独立触发或内联调用。
metadata:
  updated: 2026-07-09
---
```

---

## 校验规则

- `name` 必须匹配正则 `^[a-z0-9]+(?:-[a-z0-9]+)*$`
- `description` 长度必须在 1–1024 字符之间
- `metadata.updated` 必须是合法日期 `YYYY-MM-DD`
- 不得出现未声明的顶层字段
