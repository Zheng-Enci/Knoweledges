# LangChain 与 LangGraph 区别及 Agent（智能体）开发学习路径讲解

> 本文从一道高频面试题切入，拆解 LangChain 与 LangGraph 的真实分工——一个提供 LLM（大语言模型）应用的能力组件，一个负责有状态 Agent（智能体）的执行编排——并给出一条从「会调 API（应用程序接口）」到「会设计 Agent（智能体）架构」的四层学习路径

---

## 全文摘要

本文以一道高频面试题「LangChain 与 LangGraph 有什么区别和关联」为切入点，展开一条从概念辨析到学习路径的完整讲解。文章先从场景差异切入：固定 pipeline（流水线）用 LangChain 足矣，而真正的 agent（智能体）需要分支、循环、状态与中断，LCEL（LangChain Expression Language，链式表达式语言）组合出的 DAG（Directed Acyclic Graph，有向无环图）无法胜任，这正是 LangGraph 作为 agent runtime（智能体运行时）的诞生理由；随后分章拆解 LangChain 的四大组件 Model（模型）、Prompt（提示词）、Tool（工具）、Retriever（检索器）与 LCEL（链式表达式语言）/Runnable（可运行对象）组合协议，以及 LangGraph 的 State（状态）、Node（节点）、Edge（边）、Compile（编译）四原语、Pregel super-step（超级步）执行模型、checkpointer（检查点器）持久化与 interrupt（中断）恢复机制；再用五个维度（定位、状态、控制流、人工介入、学习曲线）对比两者区别，给出「先问流程需不需要拐弯」的选型口诀与 AWS 跨境电商客服 agent（智能体）的实战迁移案例；最后整理 agent（智能体）开发四层学习路径——LangChain 基础、tool calling（工具调用）与 ReAct（推理与行动）基础 agent（智能体）、LangGraph 核心、生产级工程化，每层附明确通关标准。核心结论：两者不是替代关系，LangChain 提供能力组件，LangGraph 负责有状态 agent（智能体）的可控编排，2026 年 LangChain 的 `create_agent` 已反向构建在 LangGraph 之上。

---

## 1. 🤔 从一道面试题说起：为什么有了 LangChain，还要再造一个 LangGraph？

这是字节跳动 AI（人工智能）Agent（智能体）研发岗的一道典型面试题： **LangChain 和 LangGraph 有什么区别和关联** 🎯 。很多人第一反应是「LangChain 是链式调用，LangGraph 是图」——这句话不能说错，但如果你面试只答到这里，基本还停留在「会用框架」的水平 🥲 。因为面试官真正想听的，是那个更本质的问题： **为什么已经有 LangChain 了，还要再造一个 LangGraph** 🔪 。

要回答这个问题，得先从一个最简单的场景说起。

### 1.1 固定流程：LangChain 完全够用

假设你要做的只是一个「用户提问 → 调用模型 → 查知识库 → 生成答案」的固定 pipeline（流水线），这种流程用 LangChain 完全够了 ✅ 。它擅长的就是把 Model（模型）、Prompt（提示词）、Tool（工具）这些能力组件组合起来，快速搭一个 LLM（大语言模型） 应用。LangChain 在 2022 年 10 月发布时的定位就是「最快让 LLM（大语言模型）应用跑起来的方式」，而它的 LCEL（LangChain Expression Language，链式表达式语言）让你能像搭积木一样把组件串成一条 chain（链）。

但这里有一个容易被忽略的技术细节： **LCEL（链式表达式语言）组合出来的 chain 本质上是 DAG（Directed Acyclic Graph，有向无环图）** ——数据单向流动，没有回路。官方在 2024 年发布 LangGraph 的博文中明确点名了这个局限：LangChain 一直缺少一种「往链里引入 cycles（循环）」的简单方法 🤔 。

### 1.2 真正的 Agent：分支、循环、状态与中断

现在换个场景。你要做的不是普通问答，而是一个真正的 Agent（智能体）：模型先判断任务 → 调用工具 → 失败了重新规划 → 结果不满意再反思一次 → 某些情况回到前面的步骤重新执行 → 中途还需要人工确认。

你会发现，这已经不是一条简单的链了——它开始出现 **Branching（分支）、Cycles（循环）、State（状态）与 Interruption（中断）** ，本质上是个循环图，DAG（有向无环图）那套拓扑排序算法直接出局 ⚠️ 。

官方在 LangGraph 发布博文里把这个转变讲得很透：早期的 AgentExecutor 把「计划 → 调工具 → 看结果 → 再决策」这个循环里几乎所有的决策权都交给了 LLM（大语言模型），简单场景没问题；但真正把 agent（智能体）推向 production（生产环境）的团队会发现， **你需要更多控制权** ——你可能想强制 agent（智能体）第一步必须调用某个工具，可能想根据当前 state（状态）用不同的 prompt（提示词），可能想让循环在特定条件下停下来。官方内部把这类流程称为 **state machine（状态机）** ：它有循环处理模糊输入的灵活性，又保留了开发者「预先设计」的控制力 💡 。

### 1.3 一句话总结两者的关系

所以我给这两者的定位是：不是「二选一」的竞争关系，而是分工明确的上下层 🤝 。

- **LangChain 提供「能力组件」** ：model 怎么接、prompt（提示词）怎么写、tool 怎么调用、Runnable（可运行对象）怎么组合——解决「LLM（大语言模型）应用需要哪些积木」的问题；
- **LangGraph 负责「执行编排」** ：这些组件在一个复杂 agent（智能体）里，按照什么 state（状态）和 path（路径）执行——解决「流程怎么被可控地组织起来」的问题。

一个有意思的佐证是两者关系的演进：2024 年 LangGraph 刚发布时，官方说它是「构建在 LangChain 之上的模块」；而到了 2026 年，官方的表述已经反转——LangChain 的核心 agent（智能体）抽象 `create_agent` 反过来 **构建在 LangGraph 之上** ，因为生产级 agent（智能体）需要 human-in-the-loop（人在回路）、observability（可观测性）、fault tolerance（容错）这些 LangGraph 的原语能力。用官方的分层说法： **LangGraph 是 agent runtime（智能体运行时），LangChain 是构建在其上的组件层与便捷抽象层** 📌 。

所以，面试时只答「一个是链、一个是图」，暴露的其实是一个更大的问题：你的 agent（智能体）学习路线可能还停留在「会调框架 API（应用程序接口）」这一层。别慌，这正是我后面第 5 章四层学习路径要解决的问题 😄 。

**参考资料：**

- [LangGraph -- LangChain Blog](https://www.langchain.com/blog/langgraph) ⭐值得阅读
- [Building LangGraph: Designing an Agent Runtime from Scratch -- LangChain Blog](https://www.langchain.com/blog/building-langgraph) ⭐值得阅读
- [3 Years of Graph Engineering with LangGraph -- LangChain Blog](https://www.langchain.com/blog/3-years-of-graph-engineering-with-langgraph) ⭐值得阅读
- [Deep Agents vs LangChain vs LangGraph -- LangChain Blog](https://www.langchain.com/blog/deep-agents-vs-langchain-vs-langgraph) ⭐值得阅读
- [LangGraph: Multi-Agent Workflows -- LangChain Blog](https://www.langchain.com/blog/langgraph-multi-agent-workflows)
- [LangChain vs LangGraph: A Developer's Guide to Choosing Your AI Frameworks -- Milvus](https://milvus.io/zh/blog/langchain-vs-langgraph.md)
- [LangChain vs LangGraph: Compare Features & Use Cases -- TrueFoundry](https://www.truefoundry.com/blog/langchain-vs-langgraph)
- [LangChain vs. LangGraph？需要资源和指导！ -- Reddit](https://www.reddit.com/r/LangChain/comments/1ojwl1y/new_to_langchain_agents_langchain_vs_langgraph/?tl=zh-hans)
- [LangChain vs LangGraph: Which One Should You Use? -- YouTube](https://www.youtube.com/watch?v=gyBxdNpFM-8)

---

## 2. 🔗 LangChain：LLM（大语言模型）应用的能力组件库

要理解 LangGraph 解决了什么，得先看清 LangChain 到底提供了什么。我把它概括为一句话： **LangChain 是 LLM（大语言模型）应用的「能力组件库 + 组合协议」** 🧰 。

### 2.1 四大基础组件：Model、Prompt、Tool、Retriever

LangChain 的核心抽象都在 `langchain_core` 这个 package（包） 里，拆开看就是四类积木 🧱 ：

- **Model（模型）** ：用 `init_chat_model` 一行代码初始化任意 provider（提供商） 的 chat model（对话模型），接口统一，随时换厂商不 lock-in（锁定）。模型侧还内置了 tool calling（工具调用）、structured output（结构化输出）、multimodality（多模态）这些标准能力；
- **Prompt（提示词）** ：`ChatPromptTemplate` 把 system（系统）、human（用户）、placeholder（占位符） 消息模板化，变量一填就发射；
- **Tool（工具）** ：一个 `@tool` 装饰器，函数签名加 docstring（文档字符串） 就能自动生成工具 schema（结构契约） ，让模型「看懂」这个工具是干嘛的；
- **Retriever（检索器）** ：对接 vector store（向量库） 和知识库，是 RAG（Retrieval-Augmented Generation，检索增强生成） 应用的原料进口 📦 。

### 2.2 LCEL 与 Runnable：组件之间的「组合协议」

有了积木，还得有乐高式的拼接标准。这就是 LCEL（LangChain Expression Language，链式表达式语言） 的价值——它的核心接口叫 **Runnable（可运行对象）** ，统一了 `invoke` / `stream` / `batch` 三种调用方式，并用一根管道符 `|` 把组件串起来：

```python
# 最经典的 LCEL 组合：提示词 → 模型 → 输出解析器
chain = prompt | model | output_parser
```

`RunnableSequence`（顺序）、`RunnableParallel`（并行）、`RunnablePassthrough`（透传）这一族 Runnables（可运行对象） 覆盖了绝大多数组合需求。但记住第 1 章说过的那句话： **LCEL（链式表达式语言）拼出来的是 DAG（有向无环图），数据单向流动** ——这就是它的能力边界 🚧 。

### 2.3 从组件到 Agent：tool calling 与 create_agent

LangChain 生态里第一个「agent（智能体）味」的东西是 tool calling（工具调用） 标准接口： `ChatModel.bind_tools()` 把工具定义挂到模型上，模型返回的 `AIMessage.tool_calls` 用统一格式告诉你要调哪个工具、传什么参数——不再需要为每家 provider（提供商） 写定制解析逻辑 🎉 。

而如今 LangChain 文档的招牌 API（应用程序接口） 是 `create_agent`，官方给它的定义非常精辟： **Agent（智能体） = Model（模型） + Harness（执行骨架）** 。harness（执行骨架） 就是环绕模型循环的一切——prompt（提示词）、tools、middleware（中间件） 。三行代码就能得到一个能调工具的 agent（智能体）：

```python
from langchain.agents import create_agent

agent = create_agent(
    model="openai:gpt-5.4",
    tools=[get_weather],
    system_prompt="You are a helpful assistant",
)
```

那 LangChain 的能力边界在哪？官方文档也写得很清楚： `create_agent` 是一个 **「最小化、高度可配置」的标准循环** ——模型每步决定下一步做什么，你通过 middleware（中间件） 注入定制逻辑；但一旦你的流程需要「非标准循环」——强制的执行顺序、确定性步骤与 agent（智能体）步骤混搭、任意位置的中断与恢复——middleware（中间件） 就不够用了，该下潜到 LangGraph 了 🤿 。

**参考资料：**

- [LangChain overview -- LangChain Docs](https://docs.langchain.com/oss/python/langchain/overview) ⭐值得阅读
- [Tool Calling with LangChain -- LangChain Blog](https://www.langchain.com/blog/tool-calling-with-langchain) ⭐值得阅读
- [langchain_core -- LangChain Reference](https://reference.langchain.com/python/langchain-core)
- [Models -- LangChain Docs](https://docs.langchain.com/oss/python/langchain/models)
- [LangChain表达式语言（LCEL） -- 知乎](https://zhuanlan.zhihu.com/p/658836911)
- [【LangChain】理论及应用实战（7）：LCEL -- CSDN博客](https://blog.csdn.net/u012856866/article/details/146297058)
- [大模型学习9-LangChain核心概念详解 -- 博客园](https://www.cnblogs.com/luohenyueji/p/20983358)
- [LangChain Explained in 10 Minutes -- YouTube](https://www.youtube.com/watch?v=xTmU8ZImUO8)

---

## 3. 🕸️ LangGraph：有状态 Agent（智能体）的执行引擎

如果说 LangChain 是「积木」，LangGraph 就是「流水线车间」。官方对它的定位是 **low-level orchestration framework（低层编排框架）** ——不帮你预设抽象，而是给你 control and durability（控制权与持久性）🏭 。这一章我按「四原语 → 执行模型 → 记忆与中断」三层拆解。

### 3.1 四原语：State、Node、Edge、Compile

LangGraph 的 Graph API 一共就四个核心概念，先把定义刻进脑子 🧠 ：

- **State（状态）** ：一个共享数据结构，代表应用的当前 snapshot（快照） 。它由 schema（结构契约） 加 **reducer（归约函数）** 组成——schema 一般用 `TypedDict` 或 Pydantic 模型定义，reducer 则规定「多个节点同时更新同一个 key 时怎么合并」：默认是覆盖，消息列表用内置的 `add_messages`（按 message ID 追加或更新）；
- **Node（节点）** ：一个函数，签名为 `State -> Partial`——读入当前 state（状态），干活（调 LLM（大语言模型）、执行工具），返回一份 **partial update（局部更新）** 字典，由框架套上 reducer 合并回总状态；
- **Edge（边）** ：决定「下一步去哪」。Normal Edge（固定边） 一条道走到黑；Conditional Edge（条件边） 通过 routing function（路由函数） 动态选路；还有 `Command(update=..., goto=...)` 可以在节点返回时同时更新状态、跳转节点；
- **Compile（编译）** ：`StateGraph` 只是 builder（构建器） ，必须 `.compile()` 之后才能 `invoke` / `stream`——编译时会做结构检查（比如有没有 orphan node（孤儿节点） ），也是你挂 checkpointer 的地方 ✅ 。

### 3.2 执行模型：Pregel super-step 与循环控制

LangGraph 的底层算法致敬了 Google 的 **Pregel** 图计算系统：执行以 **super-step（超级步）** 为单位推进——同一 super-step（超级步） 里的节点并行跑，各自把 state（状态） 更新沿 channel（通道） 发出去；没有新消息进账的节点自动 halt（停机） ，全部节点 inactive（未激活） 且无消息在途时，整个图结束 🔁 。这个设计还带来一个隐藏福利：并行节点的更新顺序不影响最终结果，LLM（大语言模型）的非确定性不会被框架放大 🎲 。

**循环怎么停下来**是面试高频追问 🚨 。答案有两层：

1. conditional edge（条件边） 的路由函数返回 `END`，或者返回「重试节点」继续循环——重试、反思、回炉全是这么写的；
2. 官方特别警告：同一个节点 **不要混用 normal edge（固定边） 和动态路由** ，否则两条路都可能执行，图的行为会变得难以推理 ⚠️ 。

另外还有个 `Send` API：节点可以在 runtime（运行时） 动态把任务分发给任意数量的下游节点——「检索 N 个来源再并行处理」这种 fan-out（扇出） 场景全靠它。

### 3.3 Checkpointer 与中断恢复：LangGraph 的杀手锏

这是 LangGraph 最值钱的部分，也是「复杂 agent（智能体）可控」的底气 💎 ：

- **Checkpointer（检查点器）** ：每到一个 super-step（超级步） 边界，把整个 state（状态） 持久化为 checkpoint（检查点） ，用 `thread_id` 作为指针区分不同会话。开发用 `InMemorySaver`，production（生产环境） 换 `PostgresSaver`——state（状态） 落盘，进程挂了也能接着跑 🛟 ；
- **Interrupt（中断）** ：在任意节点的任意位置调用 `interrupt()`，图立刻暂停、state（状态） 落盘、无限期等待；人工审核完后用 `Command(resume=...)` 重新唤起，resume（恢复） 的值会成为 `interrupt()` 的返回值——这就是 human-in-the-loop（人在回路） 的标准实现，比「挂着进程等人」优雅太多；
- **一个必须知道的坑** ⚠️ ：checkpoint（检查点） 保存在 super-step（超级步） 边界，不是函数内部——所以 resume（恢复） 时 **整个节点函数会从头重跑** ，`interrupt()` 之前的副作用（比如已经发出的 API（应用程序接口） call）必须设计成 idempotent（幂等） ，否则会重复执行。

多轮对话记忆、崩溃恢复、人工审批、甚至 time travel（时间旅行，回滚到任意 checkpoint 重跑） ——全是这套机制的衍生物。学到这一层，你才算真正从「会调用 agent（智能体）」跨进「会设计 agent（智能体）执行流程」的门槛 🚪 。

**参考资料：**

- [Graph API overview -- LangChain Docs](https://docs.langchain.com/oss/python/langgraph/graph-api) ⭐值得阅读
- [Interrupts -- LangChain Docs](https://docs.langchain.com/oss/python/langgraph/interrupts) ⭐值得阅读
- [checkpoints -- LangChain Reference](https://reference.langchain.com/python/langgraph/checkpoints) ⭐值得阅读
- [StateGraph -- LangChain Reference](https://reference.langchain.com/python/langgraph/graph/state/StateGraph)
- [add_conditional_edges -- LangChain Reference](https://reference.langchain.com/python/langgraph/graph/state/StateGraph/add_conditional_edges)
- [LangGraph 架构全解：图编排运行时的状态检查点与持久化设计 -- 腾讯云](https://developer.cloud.tencent.com/article/2748338?policyId=1003)
- [LangGraph - 03：持久化机制，让AI 智能体拥有"记忆" -- 知乎](https://zhuanlan.zhihu.com/p/1972437682400519404)
- [LangGraph 快速入门 -- CSDN（ModelEngine 社区）](https://modelengine.csdn.net/690c4fde5511483559e2a937.html)
- [LangGraph基本概念介绍 -- zhengw-tech](https://zhengw-tech.com/2025/05/25/langgraph-basic/)

---

## 4. ⚖️ 核心区别：不是替代，而是分工

前两章把两边的能力拆完了，这一章正面回答那道面试题。我先把区别压缩成一张五维对比表，再看表展开 📊 。

### 4.1 五个维度看区别

| 维度 | LangChain | LangGraph |
|------|-----------|-----------|
| **定位** | 能力组件库 + 组合协议（LCEL，链式表达式语言） | 低层编排框架 + agent runtime（智能体运行时） |
| **状态** | 默认 stateless（无状态） ，chain 跑完即弃 | 显式 state（状态） schema，全程共享、可持久化 |
| **控制流** | LCEL（链式表达式语言） 组成 DAG（有向无环图），数据单向流动 | 图结构支持循环、分支、动态路由 |
| **人工介入** | 无原生支持，得自己造轮子 | `interrupt()` + resume（恢复） 是一等公民 |
| **学习曲线** | 平缓，官方示例丰富，一天上手 | 更陡峭，得理解 state（状态）、reducer（归约函数）、checkpoint（检查点） |

逐个维度说人话 🔍 ：

- **状态是分水岭** 。LangChain 的 chain 是「一次性管道」：输入进、输出出，中间状态不保留；LangGraph 的 graph 是「有状态的会话」：state（状态） 全程存在，每个 checkpoint（检查点） 都能落盘，所以多轮记忆、崩溃恢复才成为可能；
- **控制流决定上限** 。LCEL（链式表达式语言） 的 `|` 管道再花哨也拼不出「回到三步之前重来」；LangGraph 的 conditional edge（条件边） + 循环结构天然支持 reflection（反思）、retry（重试）、multi-agent（多智能体）协作这些「流程会拐弯」的场景；
- **human-in-the-loop（人在回路）的差距最直观** 。在 LangChain 里做人工审批，你得自己设计暂停机制、state（状态） 存取、恢复逻辑；在 LangGraph 里，一个 `interrupt()` 加一个 `Command(resume=...)` 就完事了——这也是为什么生产级 agent（智能体）几乎都长在 LangGraph 上 🏗️ 。

### 4.2 选型决策：什么时候用哪个

我的选型口诀很简单： **先问你的流程需不需要「拐弯」** 🧭 。

- **固定 pipeline（流水线）** ——RAG（检索增强生成） 问答、批处理、ETL（Extract-Transform-Load，抽取-转换-加载） 式的数据流，用 LangChain 的 LCEL（链式表达式语言） 就好，别为了图而图；
- **流程需要自主决策** ——工具调用失败要重试、结果要反思、步骤要回滚，上 LangGraph；
- **中间地带** ——如果只是想要一个「能调工具的标准 agent（智能体）」，LangChain 的 `create_agent` 就够了，它底层就是 LangGraph 帮你把图画好了，你不必亲手碰 state（状态） 。

有个来自 AWS 中国区博客的实战案例很典型：一家快时尚跨境电商的客服 agent（智能体），第一版用 LangChain 快速搭了个 RAG（检索增强生成） 问答就上线了；随着业务复杂化——多轮澄清、退款要人工审核、调用外部系统失败要降级重试——团队把执行层迁移到了 LangGraph，LangChain 的组件原封不动地继续当「积木」用 🛠️ 。这个案例完美演绎了两者的分工： **组件层不用换，换的是执行编排层** 。

另外提醒一个 2026 年的新变化：LangGraph 自己也分出了 Graph API 和 Functional API 两种写法——前者显式画图，后者用装饰器写函数式流程。官方的 choosing-apis 文档给了决策标准：需要显式控制流、标准化 checkpoint（检查点） 就用 Graph API；想写简单的线性 agent（智能体）流就试 Functional API。选型这件事，从「框架之间」细化到了「框架内部」😄 。

**参考资料：**

- [Choosing a graph API or functional API -- LangChain Docs](https://docs.langchain.com/oss/python/langgraph/choosing-apis) ⭐值得阅读
- [LangChain vs LangGraph: Which Should You Use? -- Vercel](https://vercel.com/i/langchain-vs-langgraph) ⭐值得阅读
- [LangGraph vs LangChain: A Comprehensive Comparison -- stacksandflows](https://stacksandflows.com/compare/langgraph-vs-langchain/) ⭐值得阅读
- [快时尚跨境电商 Agent 设计思路与应用实践（下）-- AWS 中国区博客](https://aws.amazon.com/cn/blogs/china/fast-fashion-e-commerce-agent-design-ideas-and-application-practice-part-two/) ⭐值得阅读
- [LangChain 与 LangGraph 核心区别解析 -- 知乎](https://zhuanlan.zhihu.com/p/2046967027114555170)
- [LangChain vs LangGraph: The Ultimate 2026 Comparison -- Zoetic AI](https://www.zoeticai.com/guides/langchain-vs-langgraph/)
- [LangChain vs LangGraph 架构差异对比 -- GitHub](https://github.com/Joseph19820124/langchain-20250523)

---

## 5. 🗺️ Agent（智能体）开发四层学习路径

面试答不出「为什么」，根子在学习路线。我结合官方文档、DeepLearning.AI 课程和几份高星 GitHub roadmap（路线图），把 agent（智能体）开发整理成四层路径——顺序不能乱，每一层都有明确的「通关标准」✅ 。

### 5.1 第一层：LangChain 基础能力

**目标：能独立搭一个简单的 LLM（大语言模型）应用。**

- `init_chat_model` 接模型、`ChatPromptTemplate` 写 prompt（提示词）、`@tool` 定义工具、Retriever（检索器） 接知识库；
- LCEL（链式表达式语言） 的 `|` 管道组合：能写出 `chain = prompt | model | output_parser` 并解释每一段在干嘛；
- 通关标准：不看文档，从零搭一个「提问 → 检索 → 生成」的 RAG（检索增强生成） 问答 demo（示例） 🧱 。

### 5.2 第二层：tool calling 与基础 Agent

**目标：理解 agent（智能体）的「思考-行动」循环。**

- `bind_tools()` + `AIMessage.tool_calls`：模型怎么「选」工具、工具结果怎么回传给模型；
- ReAct（Reasoning + Acting，推理与行动）模式为什么能循环调工具——模型每轮输出「下一步调什么」，代码负责执行并喂回结果；
- 工具调用失败怎么办：错误信息回传、重试策略、降级方案；
- 通关标准：手写（不用框架的 agent（智能体）封装）一个能循环调用工具的 agent（智能体），并说清「模型决策」和「代码执行」的分工边界 🔁 。

### 5.3 第三层：LangGraph 核心

**目标：从「会调用 agent（智能体）」到「会设计 agent（智能体）执行流程」。**

这一层重点不是背 API（应用程序接口），而是搞懂第 3 章那套原语怎么用：

- state（状态） 到底存什么、reducer（归约函数） 怎么合并冲突；
- node 怎么设计、conditional edge（条件边） 什么时候用；
- 循环怎么停下来、`Send` 怎么做 fan-out（扇出） ；
- checkpoint（检查点） 为什么重要：任务中断以后怎么恢复、human-in-the-loop（人在回路） 怎么实现、为什么副作用必须 idempotent（幂等） ；
- 通关标准：能画出一个「失败重试 + 人工审核 + 断点恢复」agent（智能体）的完整 state（状态）图，并用 LangGraph 实现 🕸️ 。

### 5.4 第四层：生产级 Agent 工程化

**目标：能回答「为什么这么设计」——这是真正拉开差距的一层。**

- 状态持久化：PostgresSaver 落盘、多租户 `thread_id` 隔离；
- 失败恢复：进程挂了怎么从最近的 checkpoint（检查点） 续跑；
- multi-agent（多智能体）协作：supervisor（监督者） 模式 vs 去中心化模式、agent（智能体）间怎么 handoff（交接） ；
- 人工介入：哪些节点必须 pause（暂停） 等审批、审批结果怎么回流；
- 可观测性：执行链怎么用 LangSmith 做 tracing（链路追踪） ——一个 agent（智能体）跑 10 轮之后出错，怎么定位是哪一步的 prompt（提示词） 还是哪个工具的锅 🔬 ；
- 通关标准：面试官问「为什么这里要设计成循环 state（状态）」「为什么这么存 state（状态）」「任务挂了为什么还能接着跑」，你能对着自己的项目讲出 tradeoff（权衡取舍） 。

一个参考节奏：DeepLearning.AI 的 *AI Agents in LangGraph* 课程（LangChain 创始人 Harrison Chase 亲授）适合第三层入门；GitHub 上的 `agent_learning`、`Agentic-AI-Roadmap`、`build-ai-agents-from-scratch` 三份开源 roadmap（路线图） 分别提供了中文化的系统教程、九 module（模块） 生产课程和 14 章渐进式实战，可以按需当陪练 📚 。

**参考资料：**

- [AI Agents in LangGraph -- DeepLearning.AI](https://www.deeplearning.ai/courses/ai-agents-in-langgraph) ⭐值得阅读
- [agent_learning: 从零开始学 AI Agent 开发 -- GitHub](https://github.com/haozhe-xing/agent_learning) ⭐值得阅读
- [Agentic-AI-Roadmap-with-Notes-and-Projects -- GitHub](https://github.com/AdilShamim8/Agentic-AI-Roadmap-with-Notes-and-Projects) ⭐值得阅读
- [build-ai-agents-from-scratch -- GitHub](https://github.com/ps06756/build-ai-agents-from-scratch) ⭐值得阅读
- [langchain-fde-curriculum -- GitHub](https://github.com/Tatendaz/langchain-fde-curriculum)
- [第一章 LangChain 与 LangGraph 框架认知（easy-langent）-- GitHub](https://github.com/datawhalechina/easy-langent/blob/main/docs/guide/chapter1.md)
- [LangGraph 与 LangChain 的关系以及系统性学习路线选择 -- CSDN](https://agent.csdn.net/6a4e6555662f9a54cb8bf32e.html)
- [2026 年 AI Agent 框架横评：LangChain、Dify、LangGraph -- 知乎](https://zhuanlan.zhihu.com/p/2072286952045466320)
- [【完整版 Agent 合集】2026 最新版 LangChain+LangGraph 开发实战 -- bilibili](https://www.bilibili.com/video/BV1zoux6aEh3/)

---

## 6. 📌 总结：一句话回答面试题

回到开头那道字节跳动的面试题，现在可以给出一个有层次的回答了 🎯 。

**一句话版本**：LangChain 解决的是「LLM（大语言模型）应用需要哪些能力组件」，LangGraph 更关注「复杂 agent（智能体）的 state（状态）和执行流程怎么被可控地组织起来」——一个偏能力组件和应用开发，一个偏有状态、多步骤、可循环的 agent（智能体）编排。

**展开版本**（面试加分项）💪 ：

1. 它们不是竞争关系，更不是谁替代谁——LangGraph 是 agent runtime（智能体运行时），LangChain 是构建在其上的组件层与便捷抽象层；
2. 当应用从简单 pipeline（流水线）走向复杂 agent（智能体），对执行控制的要求变了：分支、循环、状态、中断、持久化，每一个都是 LangGraph 存在的理由；
3. 2026 年的现实是 LangChain 的 `create_agent` 已经构建在 LangGraph 之上——框架自己早就用行动投了票 🗳️ 。

**最后一个思考题**：如果让你做一个「失败后能重新规划、人工审核后还能继续执行」的 agent（智能体），用 LangChain 直接写还是 LangGraph？答案是 LangGraph——这三个需求分别对应 conditional edge（条件边） 重试循环、`interrupt()` 人工介入、checkpoint（检查点） 断点恢复，全是 LangGraph 的原生原语；用 LangChain 硬写，等于自己从零造一遍这三样轮子 🔧 。如果你还说不清为什么，说明第 3 章和 5.3 节得再翻一遍 📖 。

别只学框架怎么调用，要学一个 agent（智能体）为什么要这样设计——这才是这套学习路径的真正终点 🏁 。

**参考资料：**

- [LangChain overview -- LangChain Docs](https://docs.langchain.com/oss/python/langchain/overview) ⭐值得阅读
- [LangGraph overview -- LangChain Docs](https://docs.langchain.com/oss/python/langgraph/overview) ⭐值得阅读
