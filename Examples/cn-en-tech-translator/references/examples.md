# 翻译示例

> 加载阶段：步骤 3（执行）
> 本文档提供 cn-en-tech-translator SKILL 的完整端到端翻译示例，包括正反对照和术语查证过程。

---

## 1. 完整翻译示例

### 1.1 输入：中文原文

以下是一段典型的中文技术文档段落（Docker 容器编排主题）：

```markdown
## 服务发现机制

在微服务架构中，服务发现是保障系统高可用的关键组件。当新实例上线时，
注册中心会自动更新服务列表，并通过健康检查机制确保只有正常运行的实例
对外提供服务。需要注意的是，注册中心本身也需要采用集群化部署方案，
以避免单点故障。

该框架支持两种常见的服务发现模式：客户端发现模式和服务端发现模式。
在客户端发现模式中，服务消费者通过查询注册中心获取可用服务实例列表，
并基于负载均衡策略（如轮询、加权轮询、最少连接数）选择目标实例。
```

### 1.2 输出：英文译文 + 术语映射表

```markdown
## Service Discovery Mechanism

In a microservices architecture, service discovery is a critical component for
ensuring system high availability. When a new instance comes online, the registry
automatically updates the service list and uses health checks to ensure that only
healthy instances serve traffic. The registry itself must also be deployed in a
clustered configuration to avoid single points of failure.

The framework supports two common service discovery patterns: client-side
discovery and server-side discovery. In client-side discovery, the service
consumer queries the registry to obtain a list of available service instances
and selects a target instance based on a load-balancing strategy (such as
round-robin, weighted round-robin, or least connections).

---

## Terminology Map

| Chinese Term | English Translation | Confidence | Source |
|:---|:---|:---:|:---|
| 服务发现 | service discovery | High | CNCF Glossary; Microservices.io |
| 微服务架构 | microservices architecture | High | Martin Fowler's microservices guide |
| 注册中心 | registry | High | Netflix Eureka docs; Spring Cloud docs |
| 健康检查 | health check | High | Kubernetes docs |
| 单点故障 | single point of failure (SPOF) | High | AWS Well-Architected Framework |
| 客户端发现模式 | client-side discovery | High | Microservices.io patterns |
| 服务端发现模式 | server-side discovery | High | Microservices.io patterns |
| 负载均衡 | load balancing | High | NGINX docs |
| 轮询 | round-robin | High | NGINX upstream module docs |
| 加权轮询 | weighted round-robin | High | HAProxy docs |
| 最少连接数 | least connections | High | NGINX upstream module docs |
```

### 1.3 翻译要点说明

| 原文特征 | 翻译要点 |
|:---|:---|
| "需要注意的是" | 精简为省略（英文中直接陈述），而非 `It is necessary to note that` |
| "保障系统高可用" | 英文习惯用 `ensuring system high availability`，`system` 作前置定语 |
| "采用集群化部署方案" | 介词短语 `in a clustered configuration`，不使用 `adopt a clustered deployment solution` |
| "对外提供服务" | 技术惯用语 `serve traffic` |
| "基于...策略" | `based on a ... strategy`，自然转换 |

---

## 2. 术语查证过程示例

### 2.1 术语："注册中心"

**步骤 1**：WebSearch `"注册中心" English technical term`

**步骤 2**：搜索结果指向两个主要译法：
- `registry`（Netflix Eureka、Spring Cloud 官方文档）
- `service registry`（部分社区文章）

**步骤 3**：WebFetch 查阅 Spring Cloud 官方文档，确认使用 `service registry` 在首次提及，后续简称为 `registry`

**步骤 4**：在术语映射表中记录：
- 中文术语：注册中心
- English Translation：registry
- Confidence：High
- Source：Spring Cloud DiscoveryClient docs (https://docs.spring.io/spring-cloud/docs)

### 2.2 术语："服务发现"

**步骤 1**：WebSearch `"服务发现" English technical term`

**步骤 2**：CNCF Glossary 和 Microservices.io 一致使用 `service discovery`

**步骤 3**：确认无误，无需进一步验证

**步骤 4**：在术语映射表中记录：
- Confidence：High（2+ 独立权威来源确认）

---

## 3. 正反对照

### 3.1 同一段落的错误译法 vs 正确译法

**原文**：
> 为了避免因网络波动导致的消息丢失，系统采用消息持久化机制和重试策略，确保关键业务数据最终一致性。

**错误译法** (Bad)：
```
In order to avoid message loss caused by network fluctuation, the system
adopts a message persistence mechanism and retry strategy, to guarantee the
final consistency of key business data.
```

问题标注：
- `In order to` 冗余，`To` 即可
- `adopts a ... mechanism` 中式英语，"采用...机制" 应精简为动词
- `network fluctuation` 技术惯用语为 `network instability`
- `the final consistency` 应为 `eventual consistency`（分布式系统标准术语）
- `guarantee` 在分布式系统中通常用 `ensure`

**正确译法** (Good)：
```
To prevent message loss caused by network instability, the system persists
messages and uses retries to ensure eventual consistency of critical business
data.
```

### 3.2 对照总结

| 特征 | 错误译法 (Bad) | 正确译法 (Good) |
|:---|:---|:---|
| 动词选择 | `adopt a ... mechanism` | `persists` |
| 术语准确性 | `final consistency` | `eventual consistency` |
| 冗余词 | `In order to` | `To` |
| 技术用语 | `network fluctuation` | `network instability` |
| 动词选择 | `guarantee` | `ensure` |

---

## 4. 复杂文档处理示例

### 4.1 含代码块和表格的混合文档

**原文**：

```markdown
## 配置方法

在 `application.yml` 中添加以下配置：

```yaml
server:
  port: 8080
  servlet:
    context-path: /api
```

配置文件各参数说明如下：

| 参数名 | 类型 | 默认值 | 说明 |
|:---|:---|:---|:---|
| port | int | 8080 | 服务端口号 |
| context-path | string | / | 上下文路径 |
```

**译文**：

```markdown
## Configuration

Add the following configuration to `application.yml`:

```yaml
server:
  port: 8080
  servlet:
    context-path: /api
```

The configuration parameters are described below:

| Parameter | Type | Default | Description |
|:---|:---|:---|:---|
| port | int | 8080 | Server port number |
| context-path | string | / | Context path |
```

**关键处理要点**：
- 代码块内容完全不动（`application.yml`、`port`、`context-path` 保持原样）
- 表格表头翻译为英文（`参数名` -> `Parameter`，`说明` -> `Description`）
- 表格内容中技术值（`int`、`8080`、`/`）不翻译
- 行内代码 `` `application.yml` `` 原样保留
