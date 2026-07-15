# 输出规格

> 加载阶段：步骤 6（交付）
> 规范类 ref — 回答"怎么输出？"
> 本文档独立定义 cn-en-tech-translator SKILL 翻译输出的完整规格，包括输出结构、置信度标准和术语映射表格式。

---

## 1. 输出结构

每次翻译交付组装为以下结构：

```markdown
# {English Title}

{英文译文正文 — 保留原文档 Markdown 结构，代码块/URL/占位符原样不动}

---

## Terminology Map

| Chinese Term | English Translation | Confidence | Source | Notes |
|:---|:---|:---:|:---|:---|
| {中文术语1} | {English Term 1} | High | {URL or Standard Name} | — |
| {中文术语2} | {English Term 2} | Medium | {URL} | context-dependent |
| {中文术语3} | {English Term 3} | Low | Inferred: {reasoning} | [Inferred: confidence low] |
```

### 输出组成部分

| 部分 | 是否必需 | 说明 |
|:---|:---:|:---|
| 英文译文正文 | 必需 | 保留原文档结构，术语全文统一 |
| Terminology Map（术语映射表） | 必需 | 至少包含高频术语（出现 >=3 次）和低置信度术语 |
| Translation Notes（翻译说明） | 条件必需 | 当存在术语上下文切换、原文歧义、或无标准英译的中国特有概念时必须附上 |

---

## 2. 置信度标准

| 置信度 | 标准 | 最少验证要求 | 标注方式 |
|:---:|:---|:---|:---|
| **High** | 从官方文档/ISO 标准/IEEE 规范中确认的译法 | >=2 个独立权威来源一致 | 无需特殊标注 |
| **Medium** | 从权威技术社区（Stack Overflow >=10 赞同/GitHub 官方 README）或行业惯例中确认 | >=1 个权威来源 | 无需特殊标注 |
| **Low** | 基于构词规律或类比的推断译法，未经外部验证 | 无权威来源 | 标注 `[Inferred: confidence low]` |

### 置信度降级规则

以下情况自动降级为 Low，无论来源数量：
- 译法来源为中文技术博客、论坛或非官方翻译
- 术语为中国特有概念（如"信创""等保"），无法在英文权威源直接定位

---

## 3. 术语映射表格式

术语映射表使用固定 5 列格式：

| 列名 | 说明 | 示例 |
|:---|:---|:---|
| Chinese Term | 原文中的中文术语 | 服务发现 |
| English Translation | 确认的英文译法 | service discovery |
| Confidence | 置信度等级（High/Medium/Low） | High |
| Source | 译法来源（URL 或标准名称） | CNCF Glossary; Microservices.io |
| Notes | 特殊情况标注（如 context-dependent、Inferred、备选译法） | — 或 context-dependent |

**Notes 列的允许值**：
- `—`：无特殊情况
- `context-dependent`：同一术语在不同上下文使用不同译法
- `[Inferred: confidence low]`：低置信度推断译法
- `[Alt: {备选译法}]`：提供主译法之外的备选

---

## 4. 翻译说明触发条件

当出现以下任一情况时，必须在交付物末尾附加 **Translation Notes** 部分：

### 触发条件

| 编号 | 条件 | 说明格式 |
|:---|:---|:---|
| TN-1 | 术语上下文切换 | `[Context: "{术语}" translated as "{译法A}" in section A, as "{译法B}" in section B — different concepts]` |
| TN-2 | 原文歧义 | `[Ambiguity: original text "{原文}" could mean A or B — selected interpretation A based on context]` |
| TN-3 | 中文特有概念 | `[China-specific: "{术语}" has no standard English equivalent — used "{译法}" with explanation on first occurrence]` |
| TN-4 | 技术错误标记 | `[Original text appears to contain a technical inaccuracy: {描述} — not corrected per rule 08]` |

### 示例

```markdown
## Translation Notes

- [Context: "端口" translated as "port" in network sections, as "connector" in hardware sections — different physical concepts]
- [Ambiguity: original text "节点状态异常" could mean node status is abnormal or node is down — selected "node status is abnormal" based on subsequent troubleshooting steps]
```

---

## 5. 文件命名规范

输出文件命名格式：`{原文件名}_EN.md`

| 原文件名 | 输出文件名 |
|:---|:---|
| `deployment-guide.md` | `deployment-guide_EN.md` |
| `api-spec.md` | `api-spec_EN.md` |
| `README.md` | `README_EN.md` |

当原文件名为中文时，使用原文标题的语义对应英文命名，而非拼音：
- `部署手册.md` -> `deployment-guide_EN.md`（非 `bushu-shouce_EN.md`）
