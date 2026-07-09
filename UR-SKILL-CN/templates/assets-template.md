# 资源型文件模板

> 用途：定义生成 SKILL 的 assets/ 下静态资源文件的标准结构
> 核心原则：资源型文件是可复制、可填充、版本一致的静态内容，不可执行
> 设计方法详见 [design-guides/assets-design-guide.md](../design-guides/assets-design-guide.md)

---

## 1. 资源头信息

```markdown
# {资源名称} 模板

> 用途：{一句话说明用途}
> 版本：{版本号 / YYYY-MM-DD}
> 最后更新：{YYYY-MM-DD}
```

---

## 2. 模板结构

```{结构类型}
{
  "name": "{{name}}",
  "description": "{{description}}",
  "type": "{{type}}",
  "metadata": {
    "updated": "{{updated}}"
  }
}
```

> 结构类型：JSON / XML / YAML / Markdown

---

## 3. 占位符定义

| 占位符 | 类型 | 约束 | 必填 |
|:---|:---|:---|:---:|
| `{{name}}` | string | kebab-case, <= 64 字符 | MUST |
| `{{description}}` | string | <= 1024 字符, "Use when..." 开头 | MUST |
| `{{type}}` | string | 固定 "prompt" / "tool" / "hybrid" | MUST |
| `{{updated}}` | string | YYYY-MM-DD 格式 | MUST |

---

## 4. 填充规则

- **MUST** 填充所有 MUST 占位符，未填充则输出无效
- **MUST** 验证填充值符合约束
- **MAY** 填充可选占位符，未填充则保留默认值
- **MUST NOT** 填充非法值

---

## 5. 版本控制

| 版本策略 | 格式 | 适用场景 |
|:---|:---|:---|
| 语义化版本 | MAJOR.MINOR.PATCH | 复杂资源，频繁变更 |
| 日期版本 | YYYY-MM-DD | 简单资源，低频变更 |

---

## 6. 完整性检查清单

- [ ] 模板结构可验证（JSON Schema / XML Schema / YAML Lint）
- [ ] 所有占位符有定义（名称、类型、约束、必填）
- [ ] 占位符命名符合规范（双大括号、kebab-case、语义化、唯一性）
- [ ] 填充规则明确（必填/可选、验证方法、默认值）
- [ ] 模板有版本号
- [ ] 无嵌套占位符
- [ ] 无逻辑表达式
- [ ] 文件 < 200 行
