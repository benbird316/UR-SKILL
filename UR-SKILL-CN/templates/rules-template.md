# 规则模板

> 用途：为生成的 SKILL 定义领域行为约束的结构模板。
> 使用说明：根据任务分析结果，将本模板中的占位符替换为目标领域的具体规则。规则只声明约束，执行校验由工作流门控负责。
> 核心原则：规则、门控、反模式、风险边界、专业边界职责分离；本模板只包含规则、门控与领域特有反模式
> 设计方法详见 [design-guides/rules-design-guide.md](../design-guides/rules-design-guide.md)
>
> 相关模板：
> - 身份声明：[templates/identity-template.md](../templates/identity-template.md)
> - 边界声明：[templates/boundary-template.md](../templates/boundary-template.md)

---

## 1. 规则

### 1.1 硬约束（MUST）

本节的每条规则描述 SKILL 必须执行的行为。规则数量 3-8 条，每条规则 MUST 包含明确的动作和触发条件。

- **规则01 MUST** {动作要求}。{触发条件或范围限定}
- **规则02 MUST** {动作要求}。{触发条件或范围限定}

### 1.2 硬禁止（MUST NOT，宜少不宜多）

MUST NOT 是绝对禁止，只用于会产生实际危害的行为。其他场景优先用正向 MUST 或 SHOULD NOT。

以下两条是**每个 SKILL 必须包含**的边界引用规则，不重复边界声明的具体内容：

- **规则N MUST NOT** 违反风险边界声明中的任一条安全红线（详见 [templates/boundary-template.md](../templates/boundary-template.md)）
- **规则N+1 MUST NOT** 超越专业边界声明中的任一条专业边界（详见 [templates/boundary-template.md](../templates/boundary-template.md)）

可补充该领域特有的其他 MUST NOT（控制在 1-3 条）：

- **规则N+2 MUST NOT** {该领域特有的禁止行为}。{触发条件}

### 1.3 强偏好（SHOULD / SHOULD NOT）

本节的每条规则描述 SKILL 强烈推荐或强烈不推荐的行为。规则数量 2-4 条。

- **规则N SHOULD** {推荐动作}
- **规则N SHOULD NOT** {不推荐动作}

### 1.4 可选（MAY）

本节的每条规则描述 SKILL 可选择执行的行为。规则数量 1-3 条。

- **规则N MAY** {可选动作}

---

## 2. 门控检查点

门控在工作流执行过程中动态校验规则遵守情况。检查项引用规则编号，未通过时执行指定动作。

| 检查点 | 检查项（规则引用） | 未通过动作 |
|:---|:---|:---|
| {门控名称} | {引用的规则编号} | {回退到哪个阶段，执行什么修补动作} |

> 门控设计原则详见 [design-guides/rules-design-guide.md §3](../design-guides/rules-design-guide.md)。

---

## 3. 反模式扫描（静态检查）

反模式在交付前执行一次，识别"看似正确实则有害"的做法。仅列出该 SKILL 领域特有的反模式。

| 编号 | 反模式 | 检测方法 | 修复策略 |
|:---|:---|:---|:---|
| 反模式1 | {反模式名称} | {具体的检测手段} | {修复策略} |
| 反模式2 | {反模式名称} | {具体的检测手段} | {修复策略} |

> 反模式扫描设计原则详见 [design-guides/anti-patterns-design-guide.md](../design-guides/anti-patterns-design-guide.md)。

---

## 4. 完整性检查清单

- [ ] 规则使用 RFC 2119 关键词（MUST / MUST NOT / SHOULD / SHOULD NOT / MAY）
- [ ] 硬约束数量 3-8 条（MUST）
- [ ] 硬禁止（MUST NOT）包含两条边界引用规则，不重复边界声明的具体内容
- [ ] 强偏好数量 2-4 条（SHOULD / SHOULD NOT）
- [ ] 可选数量 1-3 条（MAY）
- [ ] 无抽象规则（如"做好工作"）
- [ ] 无矛盾规则（如规则01 说 MUST A，规则02 说 MUST NOT A）
- [ ] 门控检查点引用规则编号，不重复规则内容
- [ ] 反模式仅列出该领域特有的，不包含通用反模式
- [ ] 规则、门控、反模式、风险边界、专业边界五者职责分离，不重叠
- [ ] 风险边界与专业边界的具体内容不在本模板中重复，由 [templates/boundary-template.md](../templates/boundary-template.md) 负责
