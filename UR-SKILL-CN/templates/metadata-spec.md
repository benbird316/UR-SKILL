# 元数据规范

> 用途：定义 SKILL.md YAML frontmatter 的字段、类型、约束与示例
> 核心原则：frontmatter 是 SKILL 的触发层与身份层，必须精简、可机械解析、触发友好

---

## 字段定义

| 字段 | 类型 | 必填 | 约束 | 说明 |
|:---|:---|:---:|:---|:---|
| `name` | string | 是 | kebab-case，全小写，无空格，长度 ≤ 40 | SKILL 唯一标识符 |
| `description` | string | 是 | 50–200 字符；强烈推荐以 `Use when...` 开头；覆盖能力 + 触发场景 | 触发条件与能力说明 |
| `type` | string | 是 | 枚举值：`prompt` / `tool` / `hybrid` | SKILL 类型 |
| `whenToUse` | string | 是 | 中文，20–100 字符，具体场景 | 补充触发场景 |
| `metadata.updated` | string (date) | 是 | 格式 `YYYY-MM-DD` | 最后更新时间 |

---

## 约束说明

- `description` 应稍微 **pushy**：在描述能力的同时，主动覆盖用户可能使用的同义表达，降低 undertrigger 概率。
- `type` 决定后续输出结构：
  - `prompt`：纯提示词 SKILL，无脚本/资源。
  - `tool`：包含可执行脚本或 MCP 调用。
  - `hybrid`：提示词 + 脚本/资源混合。
- 不得在 frontmatter 中引入未声明字段，避免解析失败。

---

## 示例

```yaml
---
name: python-code-review
description: "Use when the user wants to review Python code for quality, security, style, or performance. Invoke for code inspection, bug hunting, refactoring suggestions, or CI-ready linting tasks."
type: prompt
whenToUse: 当用户需要审查 Python 代码质量、安全漏洞、风格或性能时
metadata:
  updated: 2026-07-09
---
```

---

## 校验规则

- `name` 必须匹配正则 `^[a-z0-9]+(?:-[a-z0-9]+)*$`
- `description` 长度必须在 50–200 字符之间
- `type` 必须是 `prompt` / `tool` / `hybrid` 之一
- `metadata.updated` 必须是合法日期 `YYYY-MM-DD`
