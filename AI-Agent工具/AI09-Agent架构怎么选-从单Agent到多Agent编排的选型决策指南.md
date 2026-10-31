# Agent 架构怎么选：从单 Agent 到多 Agent 编排的选型决策指南

> **核心结论**：Agent 架构选型的唯一原则是 **workflow 优先，agent 兜底**——95% 的场景先别想「要不要多 Agent」，先问「这个流程能不能固定下来」。能固定就用 workflow（fixed shape），不能固定且需要中间决策才用 agent（runtime shape）。多 Agent 不是进阶，是昂贵的兜底：Anthropic 实测 orchestrator-worker 比单 Agent 好约 90%，但烧掉约 15 倍 token；而在同等算力预算下，多 Agent 只换来约 4% 的提升、付出 4 倍成本。

## 目录

- 1. 一句话说透：workflow 优先，agent 兜底
- 2. 先分清两个根本概念：固定形状 vs 运行时形状
- 3. 单 Agent 什么时候够用：3 条判据
- 4. 多 Agent 什么时候真值：只有两种场景
- 5. 编排模式图谱：ReAct / Planner-Executor / Orchestrator-Worker
- 6. 成本与可靠性的账：为什么多 Agent 是烧钱的
- 7. 框架怎么选：LangGraph / CrewAI / AutoGen / Swarm
- 8. 可运行的选型决策代码：一个 Python 函数
- 9. 选型对照表：症状 → 原因 → 解法
- 10. 结论：该用 / 不该用的判据

## 1. 一句话说透：workflow 优先，agent 兜底

很多人一上来就问「单 Agent 还是多 Agent」，**问反了**。真正该先问的是：这个任务能不能用 workflow 解决？

Anthropic 在《Building Effective Agents》里给出的建议非常明确：**始终优先实现 workflow，只有在真正需要时才 resort 到 agent**。理由是 workflow 能给生产应用提供大多数场景所需要的 reliability（可靠性）和 predictability（可预测性），而 agent 则是为「需求无法预判」的场景提供 flexibility（灵活性）。

打个比方 🎭：workflow 像**流水线**，工位顺序提前定死，每次跑都稳定；agent 像**自由职业者**，你只给目标和工具箱，他现场决定先干哪步。流水线不需要聪明，只需要稳定；自由职业者聪明，但每次都可能给你 surprise。

**判断口诀**：流程清晰且可重复 → workflow；流程随输入变化、需要中间决策 → 考虑 agent；刚开始 → 先 workflow，量出结果弱了再换 agent。

## 2. 先分清两个根本概念：固定形状 vs 运行时形状

选型前必须先建立这对概念，否则后面全是糊涂账。

**Workflow（固定形状）**：你在设计阶段就定义好步骤、顺序、分支和 fallback。系统每次运行都走同一套结构。模型（如果有）只是在流水线的特定槽位填文本，它**不决定**流水线长什么样。

**Agent（运行时形状）**：你给它一个 goal 和一批 tools，**模型自己决定**执行哪些步骤、按什么顺序、要不要调用工具、是否继续。没有一条预先写死的路径。

为什么这个区分是选型的基石？因为**决策的难度不同**。workflow 的复杂度在你脑子里一次性想清楚，agent 的复杂度被推迟到每次运行都重新想一遍——后者意味着更高的 token 成本、更不可控的输出，以及更难排查的失败。

引用 Anthropic 的定义：agent 是「LLM 动态地指挥自己的流程和工具使用的系统」；workflow 是「预定义的代码路径」。二者是**从 workflow 到 agent 的连续光谱**，不是非黑即白。

## 3. 单 Agent 什么时候够用：3 条判据

单 Agent（一个 LLM 带若干工具，自主完成多步）是大多数场景的默认选择。判断它够不够用，看这 3 条：

1. **步骤数可预估** —— 任务大致在 3~5 步内能闭环。例如「查天气 → 推荐穿搭」，ReAct（Rea soning + Action，推理与行动交替）这种单 Agent 模式天然适合。
2. **工具少而相关** —— 只有 3~5 个工具，模型不会在选择上犯迷糊。工具一多，单 Agent 的命中率就断崖式下降。
3. **无需并行** —— 每一步都依赖前一步结果，串行推进即可，没有可以拆开同时跑的子块。

满足这 3 条，单 Agent 是最优解：**成本低、可控、好调试**。你只需要给模型一个明确的 tool 清单和一份好的 system prompt。

**反例启发**：如果任务需要 8 个以上工具、步骤超过 10 步、且中间步骤会纠错，单 Agent 会变得又慢又贵又不稳——这时候才轮到多 Agent 出场。

## 4. 多 Agent 什么时候真值：只有两种场景

多 Agent 不是「更高级」，是**为了特定收益付出高昂代价**。真正值得上多 Agent 的场景只有两类：

**场景一：真并行（True Parallelism）**。任务能拆成互不依赖的独立子块，并行跑比串行拼起来更快。比如「同时调研 10 个公司」「同时分析 20 份文档」。研究证实，在可并行任务上多 Agent 有明显提升，而在**顺序推理任务上普遍退化**——因为多 Agent 的交接会丢失上下文。

**场景二：生成 + 校验的双角色（Generator-Critic）**。一个 Agent 负责写，另一个 Agent 以全新视角审。这种「写—审」结构提升最大、代价相对最小。因为 LLM 自我纠错能力弱，换个视角的批评者能抓到很多它自己看不见的问题。

在这两类之外，多 Agent 基本是负收益。尤其要警惕**顺序链路**：每加一个 agent，成功率就按乘法累积。假设单步可靠率 95%，链 5 步成功率降到 77.4%，链 10 步掉到 59.9%；如果单步可靠率只有 90%（复杂模糊任务很常见），10 步只剩 34.9%。这就是那句「单 Agent 能干的活，别上多 Agent」的数学依据。

## 5. 编排模式图谱：ReAct / Planner-Executor / Orchestrator-Worker

如果你确认需要 agent，接下来要选**编排模式（orchestration pattern）**。三张主流牌打出来对比：

**ReAct（推理-行动交替）**：单模型内循环——模型每轮「想一下 → 调工具 → 看结果 → 再想」。适合简单问答、研究助手、3~5 个工具的单目的 agent。不适合复杂多步、需要规划、需要中途恢复的错误场景。

**Planner-Executor（规划-执行分离）**：一个 planner LLM 提前制定完整计划，executor（更小的模型或确定性 runner）按依赖顺序执行，可选 replanning。优点：多步 workflow 更快更便宜（大模型不用每步都被问一遍）；缺点：计划在第 0 步就冻结，真实任务常在中途暴露新信息，需要改计划。适合**结构清晰、可预测**的文档解析管线、数据转换任务；挣扎于开放式的、路径依赖发现的研究任务。

**Orchestrator-Worker（编排者-工人）**：一个 orchestrator 负责把任务拆解、分发给多个 worker，再聚合结果。适合**广度优先、可并行**的工作。Anthropic 的研究助手就是这种结构，在内部评测中比单 Agent 好约 90%，但烧了约 15 倍 token。

**怎么选**：需要并行 → Orchestrator-Worker；需要场景规划且任务可预测 → Planner-Executor；任务简单自主 → ReAct。三者不是替代，是分层递进的复杂度。

## 6. 成本与可靠性的账：为什么多 Agent 是烧钱的

多 Agent 的「贵」不是玄学，是可以算的账。

- **token 消耗**：多 Agent 运行成本大约是单 Agent 的 **2~10 倍**。来源包括 supervisor 开销、每个子 Agent 各自加载 system prompt、交接时的 context 序列化重排。轻量的并行 fan-out 在低端，层级式辩论在高端。
- **Anthropic 的对照**：同等算力预算下，多 Agent 设计只换来约 4% 的提升，却付出 4 倍成本。而 orchestrator-worker 虽然评测好 90%，但 15 倍 token 的代价让它在很多场景不划算。
- **成功率衰减**：多 Agent 顺序链路中，每个交接点都可能丢上下文、出错。第 4 节提过的乘法累积效应，就是 reliability 的最大杀手。

**结论先行**：多 Agent 的性价比是「用钱买并行度或买新视角」。如果任务不并行、也不需要生成-校验双角色，那多 Agent 就是纯亏损。

## 7. 框架怎么选：LangGraph / CrewAI / AutoGen / Swarm

定下架构后，选框架只是工具。四家主流横向权衡（参考 2026 年对比）：

| 框架 | 最强优势 | 短板 | 适合 |
|---|---|---|---|
| LangGraph | 生产选择，完全掌控，state 管理稳，graph 显式可控 | 学习曲线陡 | 生产系统，需要精确知道什么顺序、什么条件下跑什么 |
| CrewAI | 上手最简单，角色+任务范式直觉 | 复杂分支/循环控制弱，底层状态自定义难 | 市场调研、内容写作、快速验证原型 |
| AutoGen | 多 agent 对话冠军 | 2026 年 4 月进入维护模式，并入 Microsoft Agent Framework | 研究/复杂 agent 对话；新项目官方建议换 Microsoft Agent Framework |
| OpenAI Swarm | 延迟最低、吞吐最高，适合实时 | 轻量实验性 | 实时应用、快速原型 |

**判断逻辑**：需要严格执行控制 → LangGraph；想要快速搭建 + 自然直觉 → CrewAI；要实时低延迟 → Swarm（但它是实验性的）；遇 AutoGen → 新项目别用了，维护模式已标注。

## 8. 可运行的选型决策代码：一个 Python 函数

下面是可直接复制跑的选型决策函数。它把你脑中的判断规范化成 4 个问题，输出建议架构。运行不需要任何外部依赖：

```python
def recommend_agent_architecture(
    steps_estimable: bool,    # 步骤数能否预估
    tool_count: int,          # 需要多少个工具
    needs_parallel: bool,     # 任务能否拆成互不依赖的并行子块
    needs_critic: bool,       # 是否需要「生成 + 校验」双角色
    flow_fixed: bool,         # 流程能否在设计期固定下来
) -> str:
    """根据任务特征推荐 Agent 架构.

    参数:
        steps_estimable: 任务步骤是否能提前预判
        tool_count: 单 Agent 需要的工具数量
        needs_parallel: 是否可并行
        needs_critic: 是否需要生成/校验双角色
        flow_fixed: 流程能否在设计期固定（固定形状）
    返回:
        推荐架构: workflow / single_agent / orchestrator_worker / generator_critic
    """
    # 1) 流程能固定，优先 workflow——Anthropic 的「workflow 优先」原则
    if flow_fixed:
        return "workflow（固定形状）：最稳最省，先量出结果"

    # 2) 步骤可预估 + 工具少，单 Agent 的 ReAct 即可
    if steps_estimable and tool_count <= 5:
        return "single_agent（ReAct）：单模型循环，成本低好调试"

    # 3) 需要并行，用 Orchestrator-Worker 换速度
    if needs_parallel:
        return "orchestrator_worker（编排者-工人）：真并行才值，注意 token 成本"

    # 4) 需要生成+校验，用双角色
    if needs_critic:
        return "generator_critic（生成-校验双角色）：代价小提升大"

    # 5) 都不满足，退回保守的单 Agent 多工具编排
    return "single_agent（多工具）+ LangGraph：工具多了需要显式 graph 控制"


# 示例：一个「汇总 20 份财报并给出结论」的任务
if __name__ == "__main__":
    print(recommend_agent_architecture(
        steps_estimable=False,  # 财报内容不可预判
        tool_count=6,           # 需要读取、解析、对比等多类工具
        needs_parallel=True,    # 20 份可并行处理
        needs_critic=False,
        flow_fixed=False,
    ))
    # 输出: orchestrator_worker（编排者-工人）：真并行才值，注意 token 成本
```

这段代码把前面 1~7 章的判断浓缩成一条可执行的决策路径，复制即跑。

## 9. 选型对照表：症状 → 原因 → 解法

| 症状 | 原因 | 解法 |
|---|---|---|
| Agent 一次调用经常选错工具 | 工具太多，单 Agent 决策压力大 | 缩工具到 <=5 个，或上 LangGraph 显式路由 |
| 多 Agent 串行跑，结果却更差 | 顺序推理丢上下文（乘法累积效应） | 退回单 Agent，或只在真并行时用多 Agent |
| 任务步骤可预估但很慢、很贵 | 每步都让大模型重想一遍 | 换 Planner-Executor，规划一次，执行用小模型 |
| 想要多 Agent 但成本爆炸 | 缺少并行度，纯为「高级」而上 | 确认是否真并行，否则用单 Agent 省 2~10 倍 token |
| 想用 AutoGen 新项目 | 已进维护模式，无新功能 | 新项目换 Microsoft Agent Framework 或 LangGraph |
| workflow 写好了，但结果总不达标 | 步骤间需要模型做判断 | 把中间判断点抽出，转成 agent 自治或 replanning |

## 10. 结论：该用 / 不该用的判据

**什么时候该用**：流程能固定成 workflow 就别碰 agent；必须自治但工具少、步骤可预估时用单 Agent ReAct；任务能真并行、或需要生成-校验双角色时，才值得上多 Agent。

**什么时候不该用**：不能并行、也不需要新视角时，多 Agent 就是纯烧钱（2~10 倍 token 只换来 ±4% 提升）；顺序链路超过 5~10 步时要警惕成功率暴跌，优先考虑拆分支或回退单 Agent。

---

本专栏《AI Agent 工具专栏》从工具调用、内存、Skill 路由一路讲到架构选型与工程防线，每篇都配可运行的代码与一张对照表，聚焦生产落地的真实取舍，每周更新一篇。想在 Agent 工程里少踩坑，可在专栏页订阅。
