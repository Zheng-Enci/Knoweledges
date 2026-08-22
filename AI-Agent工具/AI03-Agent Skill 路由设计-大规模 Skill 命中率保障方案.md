# Agent Skill 路由设计：大规模 Skill 命中率保障方案 🎯

> 当 Agent（智能体）的 Skill（工具/功能）数量突破上百个后，如何保证 Agent（智能体）调用命中率是一个经典的系统设计问题。本文从描述区分度、分层路由、负样本约束、召回加重排四个维度，系统性地拆解大规模 Skill（工具/功能）路由的工程化方案，并提供可落地的架构设计参考。

---

**参考资料：**
- [SkillRouter: Retrieve-and-Rerank Skill Selection for LLM Agents at Scale -- arXiv](https://arxiv.org/abs/2603.22455) ⭐值得阅读
- [Agent Skills：把团队里"只会做一遍"的经验，变成 Agent 能反复调用的能力包 -- 阿里云开发者社区](https://developer.aliyun.com/article/1751992)
- [Agent Skills Documentation -- Microsoft](https://learn.microsoft.com/en-ca/agent-framework/agents/skills)
- [我的 Prompt & Skill 工程实践 -- 牛客网](https://www.nowcoder.com/discuss/880964795619426304) ⭐值得阅读
- [工具精选（Tool Refinement）-- 阿里云 AI 网关](https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/tool-selection)

---

## 1. 背景与问题定义（Background & Problem Definition）

> **Note（提示）：** 本章定义大规模 Skill（工具/功能）路由问题的本质，分析为什么"全量塞入"策略不可行

### 1.1 问题现象（The Problem）

当 Agent（智能体）的 Skill（工具/功能）数量从几十个增长到上百个时，一个典型的退化现象开始出现：

- 用户请求"生成 SQL 查询"，模型却跳到了 Code Interpreter（代码解释器）
- 用户请求"创建前端组件"，模型却调用了后端 API 接口
- 明明有专门的 Chart（图表）生成 Skill（工具/功能），模型却偏要用通用的 Data Processing（数据处理）Skill（工具/功能）

很多人第一反应是"模型变笨了"，于是拼命优化每个 Skill（工具/功能）内部的 prompt（提示词），把 system prompt（系统提示词）写成万字长篇小说。结果 Token（词元）消耗暴涨，问题却根本没有解决。

### 1.2 根因分析（Root Cause Analysis）

这个问题的本质不是 Skill（工具/功能）质量不够好，而是 **路由（Routing）层设计出了问题**。当上百个 Skill（工具/功能）摊平在一个层级时，模型面临的是"大海捞针"式的选择困境：

1. **语义空间过密**（Dense Semantic Space）：上百个 Skill（工具/功能）的 description（描述）在向量空间中高度重叠，模型难以区分
2. **注意力稀释**（Attention Dilution）：全量塞入后，每个 Skill（工具/功能）分到的 attention（注意力）权重极低，关键信息被淹没
3. **上下文窗口爆炸**（Context Window Explosion）：所有 Skill（工具/功能）的完整 prompt（提示词）加在一起远超模型的有效上下文长度

**核心矛盾：** 把上百个 Skill（工具/功能）的完整 prompt（提示词）全塞进 system prompt（系统提示词）里，靠模型从长文本中"大海捞针"——这本质上是个不可行的方案。

### 1.3 解决思路（Solution Approach）

真正写过大规模系统的人都清楚，这个问题不能靠死磕 Skill（工具/功能）内部实现，而是要把路由当做一个 **分发组（Dispatch Layer）** 来设计。行业里已经形成共识的四种方案：

| 方案 | 核心思路 | 类比 |
|------|---------|------|
| 提高描述区分度 | 用"触发场景"而非"功能摘要"定义 Skill（工具/功能） | Java Interface 的接口契约 |
| 分层路由 | 构建 Skill Tree（技能树），逐层缩小选择范围 | Java Package 层次结构 |
| 负样本约束 | 明确声明"什么时候不用" | Java `throws` 异常声明 |
| 召回 + 重排 | 两阶段：粗筛 + 精排 | Database Index（数据库索引） + Re-rank（重排） |

---

**参考资料：**
- [SkillRouter: Retrieve-and-Rerank Skill Selection for LLM Agents at Scale -- arXiv](https://arxiv.org/abs/2603.22455) ⭐值得阅读
- [HTAA: Hybrid Toolset Agentization & Adaptation -- arXiv](https://arxiv.org/pdf/2604.10917)

---

## 2. 提高描述区分度（Description Differentiation）

> **Note（提示）：** 本章讲解如何通过优化 Skill（工具/功能）的 name（名称）和 description（描述）来提升路由命中率

### 2.1 常见误区（Common Pitfalls）

新人写 Skill（工具/功能）description（描述）时最常见的错误是写 **功能摘要（Function Summary）** ，而不是 **触发场景（Trigger Scenario）** ：

```text
❌ 错误：数据分析助手
❌ 错误：通用办公工具
❌ 错误：代码处理专家
```

这些 description（描述）太泛了，模型根本不知道"什么时候该用它"。当上百个 Skill（工具/功能）都是这种泛泛的描述时，路由命中率必然崩溃。

### 2.2 正确写法（Correct Approach）

正确的写法应该像写 Java Interface 的 Javadoc 一样——定义清楚 **契约（Contract）** ：

- **触发条件（Trigger Conditions）**：什么场景下使用
- **输入输出（Input/Output）**：参数、返回值、语义
- **排除条件（Exclusion Conditions）**：什么情况下不要用

**正例对比：**

```text
❌ 错误：负责生成PPT
✅ 正确：当用户要求制作汇报材料、融资路演、季度总结或演示文稿时使用
```

```text
❌ 错误：SQL查询工具
✅ 正确：仅用于生成 SQL 查询语句，不适用于数据库对象管理（DDL）和性能调优（EXPLAIN）
```

**核心原则：** 场景描述越具象，在向量空间里越容易精准对齐。Anthropic 官方也强调——description（描述）要包含 **"when to use"（何时使用）** 的触发条件，而不是泛泛的功能介绍。

### 2.3 命名规范（Naming Convention）

Skill（工具/功能）的 name（名称）也需要遵循统一的命名规范：

- **命名空间前缀**（Namespace Prefix）：按业务领域加前缀，如 `sql-query-generator`、`chart-pie-creator`
- **动词开头**（Verb-Initial）：用动词 + 名词结构，如 `generate-sql-query`、`create-bar-chart`
- **避免歧义**（Avoid Ambiguity）：同一个语义只对应一个 Skill（工具/功能），不自相矛盾

### 2.4 实验验证（Experimental Validation）

SkillRouter 论文的系统性实验表明，description（描述）的质量直接影响路由命中率。当使用模糊的 description（描述）时，路由准确率下降 29-44 个百分点（percentage points），说明描述区分度是路由命中率的 **决定性因素** 。

---

**参考资料：**
- [SkillRouter: What Signals Drive Skill Selection -- arXiv](https://arxiv.org/abs/2603.22455) ⭐值得阅读
- [我的 Prompt & Skill 工程实践 -- 牛客网](https://www.nowcoder.com/discuss/880964795619426304) ⭐值得阅读
- [Agent Skills 官方规范 -- agentskills.io](https://agentskills.io/)

---

## 3. 分层路由（Hierarchical Routing）

> **Note（提示）：** 本章讲解如何用 Skill Tree（技能树）替代平铺式路由，大幅缩小每层的选择范围

### 3.1 平铺式的问题（The Flat Problem）

把所有 Skill（工具/功能）摊平在一层，等于让模型每次在 100 多个候选里做 **暴力选举（Brute-force Selection）** 。这就像在 Java 里把所有类都放在一个 package（程序包）里——不现实，也没人这么干。

### 3.2 分层设计思路（Hierarchical Design）

Java 管理几百个类靠的是什么？

- **Package（程序包）分层**：按业务模块划分命名空间
- **双亲委派模型**（Parent Delegation Model）：逐层向上搜索，缩小定位范围
- **Spring MVC 的 HandlerMapping**：先按路径前缀 + 请求方法做粗筛，再进入具体的 Controller

Skill（工具/功能）管理完全可以套用同样的模式。构建一棵 **Skill Tree（技能树）**：

```
第一层：按业务领域切（粗筛）
├── 研发（R&D）
│   ├── SQL 生成
│   ├── 代码审查
│   └── 部署流水线
├── 运营（Operations）
│   ├── 数据分析
│   ├── 报表生成
│   └── 监控告警
├── 市场（Marketing）
│   ├── 内容生成
│   ├── SEO 优化
│   └── 广告投放
└── 财务（Finance）
    ├── 报销审批
    ├── 预算编制
    └── 财务报表

第二层：按能力切（精筛）
├── 研发 > SQL 生成
│   ├── sql-query-generator
│   ├── sql-optimizer
│   └── sql-schema-designer
└── ...
```

### 3.3 渐进式披露（Progressive Disclosure）

Anthropic 提出的 Agent Skills 规范中，核心机制就是 **Progressive Disclosure（渐进式披露）**：

1. **第1级 - 元数据（Metadata）**：启动时只加载所有 Skill（工具/功能）的 name（名称）和 description（描述）（每个 Skill（工具/功能）几十到一百个 token（词元））
2. **第2级 - 完整指令（Full Instruction）**：只有当模型判断当前任务匹配某个 Skill（工具/功能）时，才加载该 Skill（工具/功能）的完整 SKILL.md
3. **第3级 - 按需资源（On-demand Resources）**：执行过程中按需加载 references/ 和 scripts/ 中的内容

**三级加载的好处：** 即使装了 500 个 Skill（工具/功能），模型每次看到的 selectable items（可选项）也只有几十个——路由空间被有效压缩。

### 3.4 行业实践（Industry Practice）

大规模 Agent（智能体）系统背后的路由几乎都是分层设计：

- **HTAA（Hybrid Toolset Agentization，混合工具集代理化）**：将高频共用的工具封装为 specialized agent tools（专用智能体工具），reducing the planner's action space（减少规划器的动作空间）
- **Microsoft Agent Framework**：原生支持 Skill（工具/功能）层级结构，按 skill sources（技能来源）组织
- **阿里云 AI 网关**：通过工具精选策略实现两阶段筛选

---

**参考资料：**
- [Agent Skills Documentation -- Microsoft](https://learn.microsoft.com/en-ca/agent-framework/agents/skills) ⭐值得阅读
- [HTAA: Hybrid Toolset Agentization & Adaptation -- arXiv](https://arxiv.org/pdf/2604.10917)
- [Agent Skills 规范 -- agentskills.io](https://agentskills.io/)
- [Twilio Skills for AI coding agents -- Twilio](https://www.twilio.com/docs/ai/skills)

---

## 4. 负样本约束（Negative Sample Constraints）

> **Note（提示）：** 本章讲解如何通过声明"什么时候不用"来降低误触发率

### 4.1 为什么需要负样本（Why Negative Samples）

只告诉模型"什么时候用"还不够，还得明确告诉它"什么时候绝对不要用"。Java 里怎么防止 API 误用？靠 **契约（Contract）** ：

- 方法签名上声明 `throws SQLException`，告诉你这个方法会跟 database（数据库）打交道，别拿它处理文件
- 接口定义里写 `@deprecated`，告诉你这个方法已经废弃，不要用

Skill（工具/功能）的 description（描述）也需要同样的思路。

### 4.2 负样本写法（Negative Sample Writing）

**示例对比：**

```text
❌ 只有触发条件：
仅用于生成 SQL 查询语句

✅ 触发条件 + 排除条件：
仅用于生成 SQL 查询语句，不适用于数据库对象管理（DDL）、性能调优（EXPLAIN）和权限管理（GRANT）
```

```text
❌ 只有功能描述：
负责前端组件代码生成

✅ 功能描述 + 排除条件：
仅负责前端组件代码生成，不负责后端接口开发、数据库设计和部署配置
```

### 4.3 排除条件设计原则（Exclusion Design Principles）

根据社区最佳实践，排除条件的设计遵循以下原则：

1. **边界清晰**（Clear Boundaries）：划清 Skill（工具/功能）的能力边界，模型就不在模糊地带瞎猜
2. **误触发损害 > 漏触发**（False Positive > False Negative）：宁可漏调，也不要误调。误调可能产生不可逆后果
3. **触发条件（AND）+ 排除条件（OR）显式写出**：触发条件用 AND 连接（必须全部满足），排除条件用 OR 连接（任一满足即排除）

### 4.4 社区实践（Community Practice）

现在越来越多高质量的 Skill（工具/功能）都加入了排除条件（Negative Constraints）部分，因为它能显著降低误触发概率。边界一旦划清，模型就不再在模糊地带瞎猜。

---

**参考资料：**
- [我的 Prompt & Skill 工程实践 -- 牛客网](https://www.nowcoder.com/discuss/880964795619426304) ⭐值得阅读
- [Best practices for LLM prompt engineering -- Palantir](https://www.palantir.com/docs/foundry/aip/best-practices-prompt-engineering)

---

## 5. 召回 + 重排（Recall + Re-rank）

> **Note（提示）：** 本章讲解两阶段路由架构：粗筛召回 + 精排判定

### 5.1 两阶段架构（Two-stage Architecture）

当 Skill（工具/功能）数量达到几百甚至上千时，即使分层路由也无法完全解决问题。这时需要引入 **两阶段（Two-stage）架构** ：

```
User Query（用户查询）
    │
    ▼
第一阶段：Embedding 粗筛（Coarse Recall）
    │  → 基于向量相似度快速召回 Top-K 候选 Skill
    │  → 召回量：50~200 → Top-10~20
    ▼
第二阶段：LLM/Reranker 精排（Fine-grained Ranking）
    │  → 将候选 Skill 的完整 description 交给 LLM 或 Reranker
    │  → 由模型做最终判定，选出最匹配的 1~3 个 Skill
    ▼
最终调用（Final Call）
```

### 5.2 第一阶段：向量召回（Stage 1: Embedding Recall）

**工作原理：**

1. 将每个 Skill（工具/功能）的 name（名称） + description（描述）离线编码为 Embedding Vector（嵌入向量）
2. 用户请求到来时，实时编码 user query（用户查询）为 Embedding Vector
3. 通过向量相似度（Cosine Similarity 或 Dot Product）计算 Top-K（前 K 个）候选

**关键优化点：**

- **Hard Negative Mining（困难负样本挖掘）**：在训练阶段加入与正例语义相似但功能不同的负样本，提升召回区分度
- **False Negative Filtering（假负例过滤）**：排除实际匹配但未被标注的样本，避免训练信号被污染
- **Bi-Encoder（双编码器）**：独立编码 query（查询）和 skill（工具/功能），适合大规模离线索引

### 5.3 第二阶段：Reranker 精排（Stage 2: Reranker Ranking）

**工作原理：**

1. 将 query（查询）和每个候选 Skill（工具/功能）的 description（描述）拼接为 pair（配对输入）
2. 使用 Cross-Encoder（交叉编码器）或 LLM（大语言模型）计算相关性得分
3. 按得分排序，选出最终调用的 Skill（工具/功能）

**为什么需要第二阶段：**

- Embedding（嵌入）召回只能捕捉浅层语义相似度，无法理解深层任务意图
- Cross-Encoder（交叉编码器）可以让 query（查询）和 Skill（工具/功能）直接交互，捕捉更细粒度的语义匹配
- SkillRouter 论文的实验表明，召回 + 重排的完整 pipeline 可以达到 74.0% 的 Top-1（排名第一）路由准确率

**输入格式示例：**

```text
Query: 帮我把上个月的销售数据做成柱状图
Skill: create-bar-chart - 当用户需要将数据可视化为柱状图、条形图时使用。接收数据表格和图表配置参数，返回柱状图文件。
```

### 5.4 性能数据（Performance Data）

| 场景 | 全量塞入 | 工具精选（召回+重排） | 提升 |
|------|---------|-------------------|------|
| 500 个工具 | 基线 | 准确率 +6% | 6% |
| 500 个工具 | 基线 | 延迟降低 7 倍 | 7× |
| 500 个工具 | 基线 | Token（词元）成本降低 4-6 倍 | 4-6× |

数据来源：阿里云 AI 网关在 Salesforce 开源数据集上的评测结果。

### 5.5 与 Progressive Disclosure 的关系（Relationship with Progressive Disclosure）

召回 + 重排和分层路由（Progressive Disclosure）并不矛盾，它们是不同维度的优化：

- **分层路由**：解决的是"怎么组织 Skill（工具/功能）"的问题（结构维度）
- **召回 + 重排**：解决的是"怎么从大量候选里选"的问题（算法维度）

两者可以组合使用：先按 Skill Tree（技能树）粗筛到某层，再对候选子集做向量召回 + 重排。

---

**参考资料：**
- [SkillRouter: Retrieve-and-Rerank Skill Selection -- arXiv](https://arxiv.org/abs/2603.22455) ⭐值得阅读
- [工具精选（Tool Refinement）-- 阿里云 AI 网关](https://help.aliyun.com/zh/api-gateway/ai-gateway/user-guide/tool-selection) ⭐值得阅读
- [LLM工具工程化实战：从提示词设计到生产级调优全指南 -- 思否](https://segmentfault.com/a/1190000047973019)

---

## 6. 总结与架构对比（Summary & Architecture Comparison）

> **Note（提示）：** 本章总结四种方案的定位与适用场景，给出架构选型建议

### 6.1 四种方案对比（Four Methods Comparison）

| 方案 | 解决的问题 | 成本 | 适用阶段 | 复杂度 |
|------|---------|------|---------|--------|
| 描述区分度 | Skill（工具/功能）语义模糊 | 低（只需改描述） | 起步阶段 | ⭐ |
| 分层路由 | 选择空间过大 | 中（需重构 Skill（工具/功能）组织） | 50+ Skill（工具/功能） | ⭐⭐ |
| 负样本约束 | 误触发率高 | 低（只需加排除条件） | 起步阶段 | ⭐ |
| 召回 + 重排 | 候选量级爆炸 | 高（需部署向量库 + Reranker（重排器）） | 200+ Skill（工具/功能） | ⭐⭐⭐⭐⭐ |

### 6.2 核心洞察（Key Insights）

回顾这四种方案，可以发现一个共同点：**它们没有一个是修改 Skill（工具/功能）内部逻辑的，全部都在优化分发层（Dispatch Layer）和约束搜索空间（Search Space）**。

回到根上，Skill（工具/功能）路由做得好不好，根本不在于 prompt（提示词）写得有多花哨，而在于：

1. **接口契约定义清晰**（Clear Interface Contract）——像设计好的 Java Service 一样
2. **输入空间边界收窄**（Narrow Input Space）——把搜索范围控制在可接受规模
3. **工程化约束能力**（Engineering Constraints）——用代码和架构，而非靠模型自觉

### 6.3 架构选型建议（Architecture Recommendations）

根据 Skill（工具/功能）规模选择不同的路由方案：

```
Skill < 20 个：
  → 描述区分度 + 负样本约束（零成本方案）

Skill 20 ~ 100 个：
  → 以上 + 分层路由（Progressive Disclosure）

Skill 100 ~ 500 个：
  → 以上 + 向量召回（Embedding Recall）

Skill > 500 个：
  → 全量方案：分层路由 + 负样本约束 + 召回 + 重排
```

### 6.4 最佳实践总结（Best Practices Summary）

1. **description（描述）聚焦"when to use"（何时使用），而非"what it does"（它做什么）**
2. **明确排除条件，划清边界**
3. **用分层路由替代平铺式暴力选举**
4. **两阶段架构：粗筛 + 精排**
5. **不要靠优化 prompt（提示词）来解决路由问题——设计架构**

---

**参考资料：**
- [SkillRouter: Retrieve-and-Rerank Skill Selection -- arXiv](https://arxiv.org/abs/2603.22455) ⭐值得阅读
- [Agent Skills：把团队经验变成 Agent 能力包 -- 阿里云开发者社区](https://developer.aliyun.com/article/1751992)
- [我的 Prompt & Skill 工程实践 -- 牛客网](https://www.nowcoder.com/discuss/880964795619426304)

---

**最后更新时间**：2026-07-31