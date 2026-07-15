# 方案类 ref：中译英转换模式

> 加载阶段：步骤 3（执行）
> 回答"怎么做？"——中文技术文档英译中的常见转换模式和解决方案

---

## 1. 中式英语系统化消除

### 1.1 四类冗余词

| 类型 | 错误示例 | 修正 | 原理 |
|:---|:---|:---|:---|
| 冗余名词 | `preparation works` | `preparations` | "works" 是类别名词，隐含在 `preparations` 中 |
| 冗余动词 | `realize data exchange` | `exchange data` | `realize` + 名词 = 动词，直接用动词即可 |
| 冗余修饰 | `2017 and 2018 consecutively` | `2017 and 2018` | 连续两年是常识，无需额外修饰 |
| 镜像陈述 | `If A, then valid. Otherwise invalid.` | `Only valid if A.` | 正反两面说同一件事，英文只需正面陈述 |

来源：Espressif Manual of Style

---

## 2. 中文冗余套话转换矩阵

中文技术文档中大量使用的套话，英译时 90% 可直接精简：

| 中文冗余表达 | 错误英译 | 正确英译 | 转换策略 |
|:---|:---|:---|:---|
| 进行配置 | carry out the configuration | configure | 冗余动词 + 名词 → 直接用动词 |
| 实现功能 | implement the functionality | supports / provides | 根据语境选择精准动词 |
| 需要注意的是 | it is necessary to note that | Note:（或直接省略） | 引导词直接省略，英文直接陈述 |
| 在这个过程当中 | in this process | （省略） | 上下文已包含的信息省略 |
| 针对该问题 | with regard to this issue | （省略） | 同上，话题引导词直接省略 |
| 相关/相应/有关 | relevant / corresponding / related | （省略 90% 场景） | 中文修饰词 90% 无独立语义 |
| 本文档中 | in this document | （省略） | 不言自明的语境省略 |
| 如下所示 | as shown below | （冒号或直接列表） | 引导性表述简化 |

---

## 3. 中文"话题—评论"结构 → 英文"主语—谓语"结构

### 3.1 问题描述

中文技术文档常采用"话题—评论"结构（Topic-Comment）：先提话题作为引子，再陈述核心内容。英文技术写作要求"主语—谓语"结构（Subject-Predicate），直接进入动作主体。

### 3.2 转换模式

**模式：话题状语前置 → 主语前置**

| 中文（话题—评论） | 英文错误（直译） | 英文正确（主谓结构） |
|:---|:---|:---|
| 对于这个请求，服务器会返回一个 JSON 响应。 | For this request, the server will return a JSON response. | The server returns a JSON response for this request. |
| 在分布式系统中，一致性是核心问题。 | In distributed systems, consistency is a core problem. | Consistency is a core problem in distributed systems. |
| 关于配置项，详见下表。 | Regarding configuration items, see the table below. | See the table below for configuration items. |

### 3.3 识别特征

中文句子以以下介词开头时，大概率是话题—评论结构，需要转换：
- 对于 / 关于 / 针对 / 至于
- 在...中 / 在...方面 / 在...领域
- 从...角度 / 从...来看

---

## 4. 中文无主语句 → 英文祈使句

### 4.1 问题描述

中文技术文档中大量使用无主语句（省略主语的祈使或陈述），英文必须补全主语或转为祈使句。API 文档、操作指南等场景尤其常见。

### 4.2 转换模式

**模式 A：直接转为祈使句（操作指南场景）**

| 中文无主语句 | 英文祈使句 |
|:---|:---|
| 需要确保配置文件已保存。 | Ensure that the configuration file has been saved. |
| 点击"确认"按钮提交表单。 | Click "Confirm" to submit the form. |
| 运行以下命令启动服务。 | Run the following command to start the service. |

**模式 B：补充主语（说明性场景）**

| 中文无主语句 | 英文补充主语 |
|:---|:---|
| 默认端口为 8080。 | The default port is 8080. |
| 支持多种认证方式。 | It supports multiple authentication methods. |
| 需要管理员权限才能执行。 | Administrator privileges are required to execute. |

### 4.3 判断依据

- 文档类型为 API 文档、操作手册、CLI 工具说明 → 优先祈使句
- 文档类型为技术规范、架构说明、产品介绍 → 补充陈述性主语
- Google/Microsoft 风格指南均推荐第二人称祈使句作为技术文档默认风格

---

## 5. 中文流水长句拆分

### 5.1 问题描述

中文习惯用逗号连接多个分句形成长句，英文要求每句一个核心意思，长句需要拆分。

### 5.2 拆分策略

1. **按逻辑节点拆分**：找到逗号连接的独立语义单元，每单元一句
2. **添加逻辑连接词**：用 however / therefore / additionally 等建立句间关系
3. **平衡原则**：目标不是"每句都短"，而是"每句都可被清晰理解"
4. **目标句长**：技术文档推荐每句 15-25 词

### 5.3 示例

**中文长句**：
> 系统启动后会自动加载配置文件，如果配置文件不存在则使用默认配置，同时记录一条警告日志，管理员可以通过日志查看配置加载情况。

**拆分后英文**：
> After startup, the system automatically loads the configuration file. If the file does not exist, it falls back to default settings and logs a warning. Administrators can review configuration loading status through the log.

---

## 6. 中国特有技术概念处理

### 6.1 处理模式

对于"信创""等保""国密"等中国特有技术概念，英文中无直接对应术语：

**模式：音译 + 括号解释**

```
{拼音} ({英文解释})
```

示例：
- `Xinchuang (China's IT Application Innovation initiative)`
- `Dengbao (China's Multi-Level Protection Scheme for cybersecurity)`
- `Guomi (Chinese national cryptographic algorithms, also known as SM series)`

### 6.2 使用规则

1. 首次出现时使用完整格式：拼音 + 英文解释
2. 后续出现可直接用拼音（读者已建立关联）
3. 在术语映射表中单独标注：`China-specific concept`
4. 置信度统一标记为 Low（无国际标准对应）
