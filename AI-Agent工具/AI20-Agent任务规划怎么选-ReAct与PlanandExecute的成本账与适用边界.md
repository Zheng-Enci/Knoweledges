# Agent 任务规划怎么选：ReAct 与 Plan-and-Execute 的成本账与适用边界

> **核心结论**：规划方式不是一个「风格偏好」，而是一道**成本结构题**。ReAct 每一步都要把历史重读一遍，步骤越多、上下文越贵；Plan-and-Execute 一次规划、批量执行，省 token 但把风险全押在「第一版计划对不对」上。**步骤少、任务形状不定 → 用 ReAct；步骤多、形状稳定 → 用 Plan-and-Execute；步骤多且会中途变化 → 用分层规划 + 批式复核**。三者不是代际关系，选错了不是「落后」，是白烧钱或者白翻车。

## 目录

- 1. 一句话结论
- 2. 为什么规划形状决定成败
- 3. 三种主流形态：ReAct、Plan-and-Execute、分层规划
- 4. ReAct 的成本：每一步都在重读历史
- 5. Plan-and-Execute 的代价：计划质量决定上限
- 6. 决策表：六个信号怎么选
- 7. 混合方案：规划 + 执行 + 批式复核
- 8. 完整可运行代码：一个双模式执行器
- 9. 对照表：症状 → 原因 → 解法
- 10. 判断收尾

## 1. 一句话结论（TL;DR）

先建立一个直觉 🎭：**ReAct 像「边走边问路」，Plan-and-Execute 像「先看导航再出发」**。走两步就到的地方，边问边走最快；要跨城跑十段路，先规划路线再一口气开完，比每个路口都停车问一次省太多。

**但导航也有个前提：地图得准。** 地图错了，你越听话开得越远。这就是 Plan-and-Execute 唯一的死穴——它省下的钱，是用「计划质量」换的。

把这件事量化一下（假设参数下文会复算）：一个 **10 步**任务、系统提示固定 `1,200` token、每步新增 `350` token——

- ReAct 累计输入约 **27,750** token；
- Plan-and-Execute 累计输入约 **7,200** token；
- 差距约 **3.9 倍**。

所以结论很直接：**先数步骤，再看形状，最后看会不会变**。三步之内别上规划器，十步以上别硬用 ReAct。

## 2. 为什么规划形状决定成败（Why Planning Shape Matters）

「规划形状」指任务被拆成什么结构：是每次只决定下一步（step-by-step），还是一次决定整条路径（plan-first）。形状选错，会出现三种典型死法：

- **漂移（drift）**：边想边做，做到第五步已经忘了最初目标，最后交付的是「一条看起来合理的岔路」。
- **僵化（brittle plan）**：一次规划出十步，第三步现实就和计划对不上，但执行器不敢改计划，硬着头皮跑完。
- **过度拆解（over-decomposition）**：把「查个天气」拆成五步，每步一次模型调用，最后发现调了五次模型只为拼一句话。

这三个死法的根因是同一个：**规划结构的复杂度，必须匹配任务本身的复杂度**。多一分是浪费，少一分是失控。

用类比 🎭：**这就像装修**——刷个墙自己动手就行（ReAct），装整套房得先出图再施工（Plan-and-Execute）；但如果你连户型都没量就出十页图，那叫纸上谈兵（僵化计划）。

## 3. 三种主流形态：ReAct、Plan-and-Execute、分层规划

| 维度 | ReAct | Plan-and-Execute | 分层规划 |
|------|-------|------------------|----------|
| 决策粒度 | 每步一次决策 | 开局一次决策 | 先分大阶段，再拆子任务 |
| 上下文增长 | 线性累积（每步重读历史） | 基本平坦（每步只看当前子任务） | 阶段内累积、阶段间重置 |
| 中途改主意 | 天然支持 | 需要重新规划（re-plan） | 支持，且只重规划当前阶段 |
| 并行能力 | 弱（串行依赖） | 强（子任务可并行） | 中（阶段内可并行） |
| 可审计性 | 差（决策散在过程里） | 好（计划本身是意图记录） | 较好 |
| 典型适用 | 探索类、≤5 步、形状不定 | 流程固定、≥6 步、成本敏感 | 长任务、阶段边界清晰 |

- **ReAct（Reason + Act，推理-行动交替）**：思考 → 调工具 → 看结果 → 再思考。它把「想」和「做」交织在同一个循环里。
- **Plan-and-Execute（先规划后执行）**：规划器（planner）先产出一份多步子任务清单，执行器（executor）逐条执行，必要时再由 re-planner 决定「继续 / 完成 / 改计划」。
- **分层规划（hierarchical planning）**：在两者中间加一层——先分出「阶段」，每个阶段内部再按子任务执行，阶段之间可以重置上下文。

> 💡 这三者不是版本迭代关系。ReAct 是 2023 年就被系统化的范式（Yao 等，arXiv:2210.03629），Plan-and-Execute 的思路在提示工程里也有对应方案（Plan-and-Solve，arXiv:2305.04091）。**老不代表差，只代表适用面窄。**

## 4. ReAct 的成本：每一步都在重读历史（The Cost of ReAct）

ReAct 最大的隐性成本是：**它没有「记忆压缩」，只有「历史回放」**。第 n 步的输入 = 系统提示 + 前 n−1 步的全部轨迹。

设系统提示与工具说明共 `B` token，每步新增轨迹 `c` token，则第 n 步的输入约为：

$$ T_n = B + c \cdot (n-1) $$

n 步的累计输入（近似，忽略每步输出差异）为等差数列求和：

$$ T_{\text{React}}(n) = nB + c \cdot \frac{n(n-1)}{2} $$

代入 `B = 1,200`、`c = 350`、`n = 10`：

- 第一步：`1,200`
- 第十步：`1,200 + 350 × 9 = 4,350`
- 累计：`10 × 1,200 + 350 × 45 = 12,000 + 15,750 = 27,750`

可以看到**平方项才是杀手**：`n(n−1)/2` 随步骤数二次增长，而 `nB` 只是线性。步骤从 10 加到 20，累计输入约从 `2.78 万` 变成 `7.85 万`，接近 3 倍。

用类比 🎭：**这就像开会不带会议纪要**——每开一次会，都要把之前所有会重讲一遍。5 个人开 10 次会，你讲的不是 10 次内容，是 55 次。

> ⚠️ 常见误区：以为 ReAct 贵在「模型调用次数」。真正贵的是**单次调用的输入长度**——调用次数相同的情况下，ReAct 的最后一步可能是第一步的 3 倍多输入。

## 5. Plan-and-Execute 的代价：计划质量决定上限（The Cost of Planning）

Plan-and-Execute 的成本结构完全不同：一次规划（贵），N 次执行（便宜）。

- 规划调用：输入 `B = 1,200`，输出计划约 `300` token；
- 每次执行：只需「当前子任务 + 相关上下文」约 `500` token；
- 10 步任务，若中途不含 re-plan：`1,200 + 300 + 10 × 500 = 7,200`。

**同一任务，`7,200` vs `27,750`，差 3.9 倍。** 这也是这类架构被反复强调的原因——LLMCompiler（arXiv:2312.04511）在论文自报的基准里给出过最高 `3.7×` 延迟加速与 `6.7×` 成本节省（该数字出自论文自己的实验设置，不是普适常数，引用时要说清出处）。

但省下来的钱是有对价的，代价有三条：

- **计划错了就全错**：执行器越听话，错误越被放大。第三步发现走偏，前两步的产出基本作废。
- **re-plan 是隐性成本**：真实任务很少一次规划到底，每加一次 re-plan，就多一次「规划级」调用。
- **需要合格的 planner**：规划器要能理解工具边界。规划出「调用不存在的接口」，执行器只能报错重来。

用类比 🎭：**这就像请人装修先出效果图**——图出得好，施工队闭眼干；图出错了，施工越专业、返工越彻底。

## 6. 决策表：六个信号怎么选（Choosing by Signal）

不要问「哪个更先进」，要问「我的任务在这六个信号上落在哪边」：

| 信号 | 偏 ReAct | 偏 Plan-and-Execute |
|------|----------|---------------------|
| 步骤数 | ≤ 5 步 | ≥ 6 步 |
| 形状可预测性 | 每步依赖上一步结果 | 开局就能列出子任务 |
| 并行性需求 | 基本串行 | 子任务可并行 |
| 可审计性 | 不要求 | 要求「计划可回溯」 |
| 成本敏感度 | 调用量小、不敏感 | 高频、量大、按量计费 |
| 错误代价 | 错了重跑很便宜 | 错了代价高，需先审计划 |

三条落地判据，记住就够用：

- **能列出清单的，就别用 ReAct**：你能在开工前把子任务写出来，说明形状已经稳定。
- **需要「根据上一步结果决定下一步」的，就别硬规划**：规划器猜不准分支，写了也是废纸。
- **两者都占的任务，用分层**：阶段内 ReAct，阶段间规划。

## 7. 混合方案：规划 + 执行 + 批式复核（Hybrid）

实际生产里最常见的不是纯 ReAct，也不是纯 Plan-and-Execute，而是「**规划一次 → 执行 k 步 → 复核一次**」。

- `k` 太小（=1）退化成 ReAct，成本优势消失；
- `k` 太大（=N）退化成纯计划，纠错太晚；
- 实践中常把 `k` 放在 **3 左右**：既让执行器连跑一段、摊销规划成本，又能在偏差扩散前拉回来。

三段式职责划分：

1. **planner**：只负责「拆」，不调用业务工具，产出结构化子任务（含依赖关系）。
2. **executor**：只负责「做」，输入是单个子任务 + 精简上下文，不感知全局计划。
3. **re-planner（批式）**：每 k 步读一次「计划 vs 实际」，输出三种决策之一——继续、完成、改计划。

这套结构的额外好处是**可审计**：计划是一份可存档的意图记录，出问题能回放「当初怎么想的」。

> 💡 分层的一个隐性收益是**上下文可重置**：阶段之间清掉临时细节，只带「阶段结论」进下一段。我在[Agent 如何动态存储运行时经验](https://blog.csdn.net/2301_79239314/article/details/170554302)里讲过「经验要蒸馏成一句话再入库」——阶段间传递也是同一个道理：传结论，不传过程。

## 8. 完整可运行代码：一个双模式执行器（Runnable Code）

下面这段 Python **复制粘贴就能跑**，不需要任何第三方库。用脚本化的「假模型」演示同一任务在两种模式下的**行为差异**与**token 差异**，你可以直接把自己接的模型换进 `_think` 里。

```python
"""双模式 Agent 执行器：ReAct 与 Plan-and-Execute 的成本对比（无第三方依赖）"""

BASE_TOKENS = 1200      # 系统提示 + 工具说明的固定开销
STEP_TOKENS = 350       # ReAct 每步新增的轨迹 token
EXEC_TOKENS = 500       # Plan-and-Execute 每步执行的上下文 token
PLAN_OUT = 300          # 规划器输出的计划 token


class ToolBox:
    """模拟业务工具：只做字符串拼接，保证可复现"""

    def __init__(self):
        self.data = {"sales.csv": "华东 1200 / 华南 800 / 华北 500"}   # 模拟数据源

    def call(self, name, arg):
        """按工具名分发，返回 (observation, 是否成功)"""
        if name == "read":
            return self.data.get(arg, ""), arg in self.data       # 读文件
        if name == "filter":
            rows = [r for r in self.data["sales.csv"].split(" / ") if arg in r]  # 过滤
            return " / ".join(rows), bool(rows)
        if name == "sum":
            nums = [int(t.split()[-1]) for t in self.data["sales.csv"].split(" / ")]  # 取数字
            return str(sum(nums)), True                            # 求和
        return "", False                                           # 未知工具


def react_loop(task, box, max_steps=10):
    """ReAct：每步都基于完整历史决定下一步，返回 (步骤数, 累计输入 token)"""
    history = []                                               # 完整轨迹（每步都要重放）
    script = [("read", "sales.csv"), ("filter", "华东"), ("sum", ""), ("finish", "")]  # 假模型策略
    used = 0                                                   # 累计输入 token
    for i, (act, arg) in enumerate(script[:max_steps], start=1):
        used += BASE_TOKENS + STEP_TOKENS * (i - 1)            # 第 i 步要重读 i-1 步历史
        if act == "finish":
            history.append("done")                             # 收尾
            break
        obs, ok = box.call(act, arg)                           # 真正调工具
        history.append(f"{act}({arg}) -> {obs} ok={ok}")       # 结果进轨迹
    return len(history), used


def plan_execute(task, box):
    """Plan-and-Execute：先规划，再逐步执行，每步只看当前子任务"""
    plan = [("read", "sales.csv"), ("filter", "华东"), ("sum", "")]   # 规划器一次产出
    used = BASE_TOKENS + PLAN_OUT                              # 一次规划的成本
    for name, arg in plan:
        used += EXEC_TOKENS                                    # 每步只带精简上下文
        box.call(name, arg)                                    # 执行
    return len(plan), used                                     # 步骤数、累计输入


if __name__ == "__main__":
    box = ToolBox()                                            # 共用同一套工具
    n1, t1 = react_loop("统计华东销售额", box)                  # ReAct 跑一遍
    n2, t2 = plan_execute("统计华东销售额", box)                # Plan-and-Execute 跑一遍
    print(f"ReAct           步骤 {n1} | 累计输入 {t1} token")   # 打印 ReAct 成本
    print(f"Plan-and-Exec   步骤 {n2} | 累计输入 {t2} token")   # 打印规划成本
    print(f"倍差 {t1 / t2:.2f}x")                               # 输出倍差
```

**怎么读这段代码**：`react_loop` 里的 `used += BASE_TOKENS + STEP_TOKENS * (i - 1)` 就是第 4 节那个公式的代码化——第 i 步必须重放前 i−1 步的轨迹；`plan_execute` 只累加 `EXEC_TOKENS`，因为每个子任务自成闭环、不需要看到别的子任务。跑一遍你会看到：ReAct `4` 步、累计输入 `6,900` token；Plan-and-Execute `3` 步、累计输入 `3,000` token，**差 2.3 倍**——这正是「贵不在次数，在长度」的直观证明。

## 9. 对照表：症状 → 原因 → 解法（Symptom → Cause → Fix）

| 症状 | 原因 | 解法 |
|------|------|------|
| 任务跑到第五步就跑偏，忘了最初目标 | 边想边做没有全局锚点 | 换成 Plan-and-Execute，先落一份计划 |
| 十步任务每次都要等很久，token 账单吓人 | ReAct 每步重放全部历史 | 改用常驻计划 + 精简执行上下文 |
| 计划做得漂亮，第三步就被现实打脸 | 一次性规划没有纠错点 | 加批式 re-plan，每 k 步复核一次 |
| 拆成十个子任务，跑完发现只要一句话 | 过度拆解，规划成本高于任务本身 | 三步内的小任务回到 ReAct |
| 想并行跑子任务，但总被上一步卡住 | ReAct 的串行依赖结构 | 用计划图拆出可并行的叶子节点 |
| 出了事故无法回溯「当时怎么想的」 | 决策散落在过程里，没有计划存档 | 计划落盘为结构化记录，作为审计依据 |

## 10. 判断收尾（Verdict）

**什么时候该上规划器**：任务步骤 ≥ 6、开局就能列出子任务清单、成本按量计费且调用量大、或者需要「计划可审计」——这时 Plan-and-Execute 几乎是默认选项。**什么时候不该上**：任务 ≤ 5 步、每步必须依赖上一步的观察结果（比如排查一个未知报错）、或者任务形状每次都不一样——这时上规划器只是多一次调用、多一份会过期的文档。判断标准只有一条：**你能不能在上手之前，把子任务写出来**——能，就规划；不能，就边做边说。

本专栏《AI-Agent 工具》从 Agent 记忆、上下文、工具调用一路讲到知识挂载、经验沉淀与规划选型，每篇都配一段可直接运行的代码，持续更新。想在做 Agent 产品时少踩坑，可在专栏页订阅。

参考资料（综合）：
- ReAct: Synergizing Reasoning and Acting in Language Models, ICLR 2023. arXiv:2210.03629. DOI: 10.48550/arXiv.2210.03629
- Plan-and-Solve Prompting: Improving Zero-Shot Chain-of-Thought Reasoning by Large Language Models, ACL 2023. arXiv:2305.04091. DOI: 10.48550/arXiv.2305.04091
- An LLM Compiler for Parallel Function Calling, 2023. arXiv:2312.04511. DOI: 10.48550/arXiv.2312.04511 ⭐值得阅读
- [ReAct vs Plan-and-Execute for Agent Loops（2026）-- Agent Native](https://www.agentnative.dev/compare/react-vs-plan-and-execute-for-agent-loops) ⭐值得阅读
- [Plan-and-Execute Agents -- LangChain Blog](https://www.langchain.com/blog/planning-agents)
- [Plan-and-Execute -- Encyclopedia of Agentic Coding Patterns](https://aipatternbook.com/plan-and-execute/)
