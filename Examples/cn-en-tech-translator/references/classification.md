# 说明类 ref：翻译标准与领域知识

> 加载阶段：步骤 2（调研）
> 回答"这是什么？"——翻译领域的标准体系、LLM 翻译特性、技术写作规范等概念性知识

---

## 1. ISO 翻译标准体系

### 1.1 ISO 17100:2015 — 翻译服务流程标准

ISO 17100:2015 是翻译服务的国际标准，规定了专业翻译服务的核心要求：

- **译者资格**：需具备翻译学位或同等能力证明 + 源语言和目标语言的专业能力
- **双语审校（Revision）**：译文必须由第二位合格语言学家审校，检查语义准确性、术语一致性和风格
- **领域专长**：译者需具备所翻译内容所属技术领域的基础知识
- **质量管理**：需建立文档化的质量管理流程


### 1.2 ISO 18587:2017 — 机译后编辑标准

ISO 18587:2017 规定了机器翻译输出后编辑（MTPE）的流程要求和后编辑者能力标准：

- **全量后编辑 vs 轻量后编辑**：全量后编辑质量对标人工翻译，轻量后编辑仅保证可理解性
- **后编辑者六项能力**：翻译能力、源语言与目标语言能力、MT 素养、研究能力、文化能力、技术能力

**修订进展**：第二版预计 2026 年底发布（来源：EUATC April 2026 研讨会）。关键变化：
- 范围从"machine translation output"扩展为"AI-generated translation output"，明确覆盖 LLM（GPT、Claude、Gemini 等）
- 新增 AI 特异性错误分类：Hallucination（幻觉）、Source Divergence（源偏离）、False Fluency（伪流畅）、Context Leakage（上下文泄漏）、Register Inconsistency（语域不一致）
- 新增"非人类翻译""人工智能翻译""自动后编辑"等术语
- 与 ISO 17100 结构对齐，引入与 ISO 42001（AI 管理系统）的关联
- 新增可行性评估条款和附录，帮助项目经理判断 MTPE 是否适用于给定文本

### 1.3 ISO 5060:2024 — 翻译输出质量评估

ISO 5060:2024 是翻译输出评估的最新国际标准，提供了系统化的分析性评估框架：

**7 大错误类别**（Error Types）：
1. **Terminology**：术语不一致或使用不当术语
2. **Accuracy**：误译、漏译、增译
3. **Linguistic conventions**：语法、标点、拼写错误
4. **Style**：风格或语域不一致
5. **Locale conventions**：日期、数字、货币等本地化格式错误
6. **Audience appropriateness**：文化特定引用不当
7. **Design and markup**：格式、布局、超链接问题

**3 级严重度**（Severity Levels）：
- **Critical**：致命错误，使译文不可用，可能导致严重后果（如经济损失、声誉损害）
- **Major**：严重错误，影响译文可用性或可信度
- **Minor**：轻微错误，不影响核心信息传递

**3 阶段评估流程**：
1. **Pre-evaluation**：定义项目规格、评估目的、采样策略
2. **Evaluation**：使用评分卡记录错误类型、严重度和罚分，计算质量评级（Pass/Fail）
3. **Post-evaluation**：提供反馈、处理争议

**与 MQM 框架的关系**：ISO 5060 基于 MQM（Multidimensional Quality Metrics）框架构建，两者共享错误分类体系。

---

## 2. LLM 翻译特异性研究

### 2.1 HalloMTBench: LLM 翻译幻觉基准（Alibaba/Tianjin University, 2025）

Wu et al. (2025) 在论文 "Challenging Multilingual LLMs: A New Taxonomy and Benchmark for Unraveling Hallucination in Translation" 中，对 17 个主流 LLM 进行了翻译幻觉系统性评估：

**核心发现**：
- 17 个模型的幻觉率分布在 33%-60%（GPT-4o-mini 最低，Seed-X-PPO-7B 最高）
- 现有评估基准无法暴露真实漏洞 —— 传统测试中模型表现近零幻觉，但 HalloMTBench 暴露了系统性脆弱性

**两大幻觉类型**：
1. **Instruction Detachment（指令脱离）**：模型翻译成错误的语言，或完全不执行翻译
2. **Source Detachment（源脱离）**：译文中添加了不存在的内容（Addition），或遗漏了原文关键信息（Omission）

**幻觉触发因素**：
- 文本长度：极短文本（0-29 字符）和超长文本（>499 字符）触发率最高
- 模型架构：RL（强化学习）微调的模型更倾向产出"语言混用"错误
- 语言对差异：英葡、英日、英越幻觉率最高；英中受影响较小

> 对本 SKILL 的启示：步骤 4 校验时必须执行均匀采样（前 1/3、中 1/3、后 1/3 各至少 1 段），以检测长文档中的"一致性衰减"和"风格漂移"。

### 2.2 Alibaba SASFT: LLM 语言混用研究（2026）

Deng et al. (2026) 在 "SASFT: Sparse Autoencoder-guided Supervised Finetuning to Mitigate Unexpected Code-Switching in LLMs" 中指出：
- LLM 在多语言场景下存在意外的 code-switching（语言混用），即响应中混入非目标语言内容
- 通过稀疏自编码器分析发现，code-switching 发生时，非目标语言的 SAE 特征出现过度预激活
- SASFT 方法可将 code-switching 降低 50% 以上

> 对本 SKILL 的启示：中译英任务中，需在步骤 4 对全文执行中文字符扫描，以检测"语言混用/指令脱离"问题。

### 2.3 NAACL 2025: 翻译幻觉偏好优化缓解

Tang et al. (2025) 提出了基于偏好优化的幻觉缓解方法，通过构造幻觉聚焦的偏好数据集微调 LLM，将 5 个语言对的幻觉率平均降低 96%，零样本场景下降低 89%。

---

## 3. 技术写作风格指南

### 3.1 Microsoft Writing Style Guide（持续更新至 2026 年 7 月）

微软写作风格指南是技术文档写作的权威参考，最新更新至 2026 年 7 月。核心原则：
- **Warm and relaxed, crisp and clear**：温暖轻松、干脆清晰
- **主动语态优先**：`You can enable this feature` 优于 `This feature can be enabled`
- **句首精简**：删除冗余引导词，直接进入要点
- **句子大小写**：标题和标题使用 sentence-case（仅首字母大写），不使用 title-case
- **一致性**：同一 UI 元素用同一动词，术语全文统一

与本 SKILL 相关的规则对应：规则 18（主动语态）、规则 19（短句优先）、规则 17（精简冗余）。

### 3.2 Google Developer Documentation Style Guide

Google 开发者文档风格指南强调：
- **Task-oriented**：面向任务而非功能描述
- **Second person**：使用第二人称（you）和祈使句
- **Present tense**：默认现在时
- **Inclusive language**：包容性语言
