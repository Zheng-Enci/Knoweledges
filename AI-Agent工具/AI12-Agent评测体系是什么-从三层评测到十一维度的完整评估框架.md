# Agent 评测体系是什么：从三层评测到十一个维度的完整评估框架

> **核心结论**：Agent 评测体系（Agent Evaluation）就是一套「**系统地判断一个 Agent 好不好用**」的方法，核心是回答两个问题：**评什么**（评测对象）和**怎么评**（评测维度与指标）。评什么分三层：**端到端评测**（把 Agent 当黑盒，只看任务有没有完成）、**过程评测**（看中间轨迹——规划、工具调用、反思是否合理）、**能力评测**（拆开测单项能力——工具使用、记忆、多 Agent 协作）。怎么评有一个行业共识的十一维框架：任务成功、输出质量、规划推理、不确定性决策、工具使用、自主性、学习适应、安全对齐、效率、多 Agent 协作、长期记忆一致性。**现实很骨感**：ClawBench 实测 8 款 Agent 处理日常在线任务，最好的 Claude 也才 **33.3%** 任务完成率——Agent 评测体系的存在，正是因为 Agent「看着能干活、实际经常干不完」。

## 目录

- 1. 一句话结论
- 2. 为什么需要评测体系：Agent「看着能干，实际干不完」
- 3. 评什么：三层分类（端到端 / 过程 / 能力）
- 4. 端到端评测（E2E）：只看任务有没有完成
- 5. 过程评测（Process）：看轨迹是否合理
- 6. 能力评测（Capability）：拆开测单项能力
- 7. 怎么评：十一维评测体系
- 8. 核心指标：任务成功率与轨迹质量
- 9. 主流 Agent Benchmark：从 τ-Bench 到 AgentGym2
- 10. 残酷现实：ClawBench 实测数据
- 11. 完整可运行代码：一个最小评测脚本
- 12. 对照表：症状 → 原因 → 解法
- 13. 判断收尾

## 1. 一句话结论

先建立一个直觉 🎭：**Agent 评测像「给新员工做绩效考核」**——你不能只看他「最后交了没交」，还要看他「过程对不对」（是不是瞎折腾）、「能力够不够」（会不会用工具、记不记得事）。三个层次，对应三层考核。

所以记住这套框架：

- **评什么**（三层）：端到端（结果）→ 过程（轨迹）→ 能力（拆开测）。
- **怎么评**（十一维）：任务成功、工具使用、规划、安全、效率、多 Agent 协作…。
- **核心指标**：任务成功率（Task Success Rate）+ 轨迹质量。

一句话：**Agent 评测体系 = 一套「评什么 + 怎么评」的完整方法**，用来回答「这个 Agent 到底靠不靠谱」。

## 2. 为什么需要评测体系：Agent「看着能干，实际干不完」

Agent 评测之所以成为一门「体系」，是因为 LLM Agent 有一个致命特点：**它输出的是「文本」，但干的是「行动」**。

- 普通 LLM 评测只看「回答得对不对」（答案质量）。
- Agent 评测要看「**任务有没有真完成**」——比如「帮我订好机票」这个任务，Agent 可能回复了一大段漂亮的文字，但**系统里根本没下单**。
- 这就是为什么不能只靠「最终文本看起来正确」来评判——**要核对真实系统状态**（下单了吗、数据库改了吗、文件生成了吗）。

用类比 🎭：**评判一个 Agent 不能像批改作文只看文笔，要像验收工程——墙真的刷好了吗？地真的铺了吗？** 文字再漂亮，活没干完就是没完成。

> 💡 这也是评测体系存在的根本原因：**Agent 的「假成功」（看起来完成了、实际没完成）太常见**，必须用一套严格的方法去戳穿。

参考资料：
- [Agent 评估简介 -- 腾讯云开发者社区](https://cloud.tencent.com/developer/techpedia/2737) ⭐值得阅读

## 3. 评什么：三层分类（端到端 / 过程 / 能力）

评测对象分三层，对应「从整体到零件」的递进：

| 层级 | 评测对象 | 类比 | 核心指标 |
|------|---------|------|---------|
| 端到端评测 | 把 Agent 当黑盒，只看最终结果 | 验收工程 | 任务完成率 |
| 过程评测 | 看中间轨迹（工具调用、规划、反思） | 看施工过程 | 轨迹质量 |
| 能力评测 | 拆开测单项能力（工具、记忆、协作） | 单测零件 | 能力分 |

- **端到端（End-to-End）**：最直觉，给任务、跑完、看结果对不对。评「任务有没有完成」。
- **过程（Process）**：看轨迹是否合理——是不是绕了远路、工具调用顺序对不对、有没有无效反思。
- **能力（Capability）**：拆开测单项能力——单独测工具调用、单独测记忆、单独测多 Agent 协作。

> 💡 三层不是互斥，而是**组合使用**：端到端给你「总分」，过程给你「哪里掉链子」，能力给你「哪块短板」。生产环境的评测通常三层都上。

参考资料：
- [Agent 评测体系：三层分类与一条流程 -- CSDN](https://blog.csdn.net/2401_87562521/article/details/169168074) ⭐值得阅读

## 4. 端到端评测（E2E）：只看任务有没有完成

这是最常用、也是成本最低的一层评测。

- **做法**：给 Agent 一个任务，让它跑完，比对「最终结果」和「正确答案」。
- **核心指标**：任务完成率（Task Completion Rate / Task Success Rate）——完成的任务占总任务的占比。
- **优点**：全自动、成本低——部署 Agent、跑任务、比对结果就能出分。
- **缺点**：只看结果，**不知道过程对不对**，也容易被「假成功」欺骗。

用类比 🎭：**端到端评测像「期末只考最后成绩」**——方便快捷，但一个靠死记硬背高分的学生和一个真正懂的学生，可能拿到一样的分数。

> ⚠️ 关键坑：**端到端评测必须核对真实系统状态**。比如「订票」任务，要看票务系统里到底有没有订单，而不是信 Agent 的「已成功订票」这句话——否则「假成功」会混进分数。

参考资料：
- [How to Evaluate AI Agents From Tool Calls to Task Completion -- NVIDIA](https://developer.nvidia.com/blog/how-to-evaluate-ai-agents-from-tool-calls-to-task-completion/) ⭐值得阅读

## 5. 过程评测（Process）：看轨迹是否合理

端到端解决「完成了没」，过程评测解决「**完成得怎么样**」。

- **做法**：检查 Agent 的**执行轨迹（trajectory）**——它调用了哪些工具、顺序对不对、有没有无效的反复尝试、规划是否合理。
- **核心指标**：轨迹质量（Trajectory Quality）——路径的合理性、效率、是否偏离目标。
- **为什么重要**：两个 Agent 可能都完成了任务，但一个「直来直去」，一个「绕了十圈 + 反复改错」——过程评测能区分它们。
- **落地**：在工具调用层面打分，比如「工具调用正确率」「无效调用次数」「是否需要人工干预」。

> 💡 过程评测适合**上线前调试**：当端到端分数不高时，看轨迹能定位「卡在哪一步」——是规划错、工具调用错、还是反思无效。

参考资料：
- [How to Evaluate AI Agents -- NVIDIA](https://developer.nvidia.com/blog/how-to-evaluate-ai-agents-from-tool-calls-to-task-completion/) ⭐值得阅读

## 6. 能力评测（Capability）：拆开测单项能力

第三层把 Agent 拆成「零件」，逐个测单项能力：

| 单项能力 | 评测什么 | 典型问题 |
|---------|---------|---------|
| 工具使用 | 能否正确调用工具并处理结果 | 「给它 API，它调用对吗？」 |
| 规划推理 | 能否拆解任务、按序执行 | 「复杂任务会拆步骤吗？」 |
| 记忆一致性 | 能否记住上下文、跨轮次保持 | 「隔几轮还记得初始目标吗？」 |
| 自主性 | 需要多少人工干预 | 「能自己推进，还是总要人拉？」 |
| 多 Agent 协作 | 多个 Agent 能否协调 | 「分工时会不会互相干扰？」 |

- 能力评测的价值：**定位「短板」**——如果端到端总分低，能力评测告诉你「是工具用不好，还是记不住事」。
- 我在[Agent架构怎么选：从单Agent到多Agent编排的选型决策指南](https://juejin.cn/post/7702483654677364774)里讲过 Agent 架构选型，能力评测正是「选型之后验证」的那一步——架构定了，要用能力评测确认每个角色真能胜任。

> 💡 三层评测的组合逻辑：**端到端给总分 → 过程给「哪步坏」→ 能力给「哪块弱」**，三层加起来才是完整的评测体系。

## 7. 怎么评：十一维评测体系

「评什么」定了对象，「怎么评」给出一套全面的维度框架。一份 Agentic AI 评测综述提出了**十一维评测体系（11-dimensional taxonomy）**，覆盖 Agent 的方方面面：

| 维度 | 测什么 |
|------|--------|
| 1 任务成功 | 最终目标是否达成 |
| 2 输出质量 | 产出内容是否优质 |
| 3 规划与推理 | 拆解与推导是否正确 |
| 4 不确定性决策 | 信息不全时能否做对判断 |
| 5 工具使用 | 调用工具的准确性 |
| 6 自主性与人工干预 | 需要多少人工兜底 |
| 7 学习与适应 | 能否从反馈中改进 |
| 8 安全与对齐 | 是否做危险/越权的事 |
| 9 效率与资源 | 是否又快又省 |
| 10 多 Agent 协作 | 多体协调是否顺畅 |
| 11 长期记忆一致性 | 跨长会话是否保持状态 |

- 这十一维是「完整评测」的理想框架，**实际项目不必全测**——按场景选几个关键维度即可。
- 比如一个「订票 Agent」重点测：任务成功、工具使用、安全（别误订）；一个「客服 Agent」重点测：输出质量、记忆一致性、不确定性决策。

用类比 🎭：**十一维评测像「体检全项」**——理论上能测的都给你测一遍；但日常你只需要按风险挑几项做专项检查，不必每次都做全套。

参考资料：
- [Evaluating Agentic AI: A Survey of Metrics, Benchmarks, and Methodologies -- TechRxiv](https://www.techrxiv.org/doi/pdf/10.36227/techrxiv.177162480.04513202/v2) ⭐值得阅读

## 8. 核心指标：任务成功率与轨迹质量

评测维度很多，但落到「分」上，核心就是两个指标：

**任务成功率（Task Success Rate）**——最核心的「总分」：

$$\text{Success Rate} = \frac{\text{成功完成任务数}}{\text{总任务数}}$$

- 判断「成功」的标准：**核对真实系统状态**，而不是信 Agent 的自述。
- 进阶：τ-Bench 提出的 **pass^k** 指标——同一个任务跑 k 次，要求**至少一次成功**才算过，用来衡量「可靠性」（不是碰运气成功一次）。

**轨迹质量（Trajectory Quality）**——过程的「过程分」：

- 工具调用正确率、无效调用次数、是否需要人工干预、是否偏离目标。
- NVIDIA 的实践：分**两步打分**——step-level（单步对不对，定位链子断在哪）+ end-to-end（最终环境状态对不对）。

> 💡 一句话：**任务成功率看「干成没干成」，轨迹质量看「干得正不正常」**——两者要一起看，只看成功率可能被「碰巧成功」骗。

参考资料：
- [τ-BENCH: A Benchmark for Tool-Agent-User Interaction -- ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/file/1b126cc38b8638e07bef37e7b2bb72bf-Paper-Conference.pdf) ⭐值得阅读

## 9. 主流 Agent Benchmark：从 τ-Bench 到 AgentGym2

理论框架之外，评测最终要落到具体的 benchmark（基准测试）上。近年涌现了一批「真实场景」Agent 基准：

| Benchmark | 测什么 | 特点 |
|-----------|--------|------|
| τ-Bench | 工具 Agent 与用户动态对话 | 模拟用户，比对数据库终态，引入 pass^k 指标 |
| AgentGym2 | 去理想化的真实环境 | 暴露真实部署的不确定性、需要主动探索 |
| ClawBench | 日常在线任务 | 实测真实可复现的在线任务 |
| SlackBench | 协作研发项目 | 多对话 + 演进代码库，140 条查询 |
| EnterpriseClawBench | 企业真实会话 | 从真实工作会话构建，852 个可复现任务 |

- **共同趋势**：从「理想化玩具环境」走向「真实世界」——旧 benchmark 输入干净、工具齐全，新 benchmark 强调**不确定性、噪声、主动探索**。
- AgentGym2 明确批评旧基准「预设干净输入、忽略关键步骤、假设工具就绪」，与真实部署差很远。

> 💡 选 benchmark 的原则：**越贴近你真实场景的越好**。做订票就用 τ-Bench 类，做企业流程就用 EnterpriseClawBench 类——别用一个通用的「玩具基准」给生产 Agent 打分。

参考资料：
- [AgentGym2: Benchmarking LLM Agents in De-Idealized Real-World Environments -- arXiv](https://arxiv.org/html/2607.05174) ⭐值得阅读
- [SlackBench: Benchmarking Agents on Collaborative Projects -- arXiv](https://arxiv.org/html/2611.05512v1) ⭐值得阅读

## 10. 残酷现实：ClawBench 实测数据

评测体系之所以重要，是因为**现实数据很残酷**。ClawBench 在 EMNLP 2026 实测了 8 款 Agent 处理「日常在线任务」的真实完成率：

| Agent | 任务完成率 |
|-------|:---:|
| Claude Sonnet 4.6 | **33.3%** |
| Qwen 3.5 | 26.1% |
| GLM-5 | 24.2% |
| GPT-5.4 | 6.5% |

- 最好的 Claude 也才 **33.3%**，意味着**大部分日常在线任务，连最强 Agent 都完不成**。
- 值得注意的是 **GPT-5.4 只有 6.5%**——这说明「模型强」不等于「Agent 强」，评测体系能帮你识别这种「名不副实」的坑。
- 低完成率不是单点问题，而是**任务层面普遍存在**——评测体系的价值就在这里：**用数据告诉你，别盲目相信 Agent 的「演示效果」**。

> ⚠️ 数字启示：**Agent 的 demo 和真实评测是两回事**。厂商演示视频里的「惊艳表现」，放到严格评测里往往大幅缩水——这也是「为什么要有评测体系」最有力的注脚。

参考资料：
- [ClawBench实测8款Agent：真能完成日常在线任务吗？ -- Link Researcher](https://linkresearcher.com/theses/7b4147d0-60fc-4fab-9aa9-1d9cfba49870) ⭐值得阅读
- [EnterpriseClawBench: Building Enterprise Agent Benchmarks -- EMNLP 2026](https://aclanthology.org/2026.emnlp-industry.219.pdf)

## 11. 完整可运行代码：一个最小评测脚本

下面是一段**复制粘贴就能跑**的 Python 脚本，实现一个最小的「端到端 + 过程」评测：给定一个 Agent 的任务轨迹，计算任务成功率、工具调用正确率、无效调用次数三个核心指标。运行无需第三方库。

```python
import json

# 一条 Agent 执行轨迹（真实评测中来自日志；这里用模拟数据演示）
trajectory = {
    "task_id": "order_ticket_01",
    "goal": "为张三订一张明天上午10点的北京到上海的机票",
    "steps": [
        {"step": 1, "action": "search_flights",  "params": {"from": "北京", "to": "上海"}, "ok": True},
        {"step": 2, "action": "search_flights",  "params": {"from": "北京", "to": "上海"}, "ok": True},  # 与上步重复 → 无效
        {"step": 3, "action": "select_flight",   "params": {"id": "CA1837"},              "ok": True},
        {"step": 4, "action": "book_ticket",     "params": {"id": "CA1837", "name": "张三"}, "ok": True},
        {"step": 5, "action": "confirm_payment", "params": {"id": "CA1837"},              "ok": True},
    ],
    "task_success": True,   # 端到端：真实系统里订单已生成（需人工/系统核验，非 Agent 自述）
}

def evaluate_agent(traj):
    """
    最小评测：算任务成功率、工具调用正确率、无效调用次数。
    参数:
        traj: 一条 Agent 执行轨迹（含 steps、task_success）
    返回: 三个核心指标的字典
    """
    steps = traj["steps"]
    total = len(steps)                            # 总步骤数
    ok = sum(1 for s in steps if s["ok"])         # 正确步骤数
    tool_acc = ok / total if total else 0.0       # 工具调用正确率

    # 模拟「无效调用」：相邻两步是相同动作即算一次无效重复
    invalid = 0
    for i in range(1, total):
        if steps[i]["action"] == steps[i-1]["action"]:
            invalid += 1                          # 重复调用同一工具 = 无效
    # 轨迹质量：正确率越高、无效越少越好
    quality = max(0.0, tool_acc - 0.1 * invalid)  # 每个无效调用扣 0.1

    return {
        "任务成功率": 1.0 if traj["task_success"] else 0.0,  # 端到端指标
        "工具调用正确率": round(tool_acc, 3),                # 过程指标
        "无效调用次数": invalid,                             # 过程指标
        "轨迹质量分": round(quality, 3),                     # 综合过程分
    }

# 跑评测：输出四个核心指标
result = evaluate_agent(trajectory)
print("任务成功率:", result["任务成功率"])        # 应输出 1.0
print("工具调用正确率:", result["工具调用正确率"])  # 5 步全对 → 1.0
print("无效调用次数:", result["无效调用次数"])      # 第 4 步重复 → 1
print("轨迹质量分:", result["轨迹质量分"])          # 1.0 - 0.1 = 0.9
```

**怎么读这段代码**：`evaluate_agent` 把评测拆成三个指标——`task_success` 是**端到端**的「任务成功率」（必须是系统核验过的真实状态，不是 Agent 自述）；`tool_acc`（工具调用正确率）和 `invalid`（无效调用次数）是**过程**的「轨迹质量」；`quality` 把两者合并成综合过程分。真实评测里，`trajectory` 来自 Agent 运行日志，`task_success` 来自人工/系统对最终状态的核验——这套骨架能直接扩展成生产评测脚本。

## 12. 对照表：症状 → 原因 → 解法

| 症状 | 原因 | 解法 |
|------|------|------|
| 演示很惊艳，上线就翻车 | 评测只看 demo 没看真实任务 | 用端到端评测核对真实系统状态 |
| 分不清 Agent 靠不靠谱 | 没有评测体系 | 建「端到端 + 过程 + 能力」三层评测 |
| 只看到「假成功」 | 信了 Agent 的自述 | 任务成功率必须核验真实系统状态 |
| 不知道 Agent 卡在哪 | 只看最终分 | 看轨迹：过程评测定位掉链子的一步 |
| 模型很强但 Agent 很弱 | 模型能力 ≠ Agent 能力 | 用 ClawBench 类真实基准单独测 Agent |
| 评测分数虚高 | 用了理想化玩具基准 | 选贴近真实场景的 benchmark（τ-Bench/AgentGym2） |

## 13. 判断收尾

**什么时候该建评测体系**：你正在开发 / 采购 / 运维 Agent——只要 Agent 会被真实使用，就值得至少搭一层「端到端 + 过程」评测，否则你永远在「演示效果」和「实际效果」之间猜。**什么时候可以简化**：只是快速验证一个想法、或临时跑个 demo，不必建完整十一维体系——先测任务成功率一个指标，够用就够。判断标准只有一条：**这个 Agent 会不会被真实地用起来**——会，就值得一套评测体系；不会，别过度设计。

本专栏《AI-Agent 工具》从 Agent 记忆、工具调用、架构选型一路讲到自动化调度系统设计与评测，每篇配可直接运行的代码，持续更新。想在 Agent 实战里少踩坑，可在专栏页订阅。

参考资料（综合）：
- [Evaluating Agentic AI: A Survey of Metrics, Benchmarks, and Methodologies -- TechRxiv](https://www.techrxiv.org/doi/pdf/10.36227/techrxiv.177162480.04513202/v2) ⭐值得阅读
- [AgentGym2: Benchmarking LLM Agents in De-Idealized Real-World Environments -- arXiv](https://arxiv.org/html/2607.05174) ⭐值得阅读
- [τ-BENCH: A Benchmark for Tool-Agent-User Interaction -- ICLR 2025](https://proceedings.iclr.cc/paper_files/paper/2025/file/1b126cc38b8638e07bef37e7b2bb72bf-Paper-Conference.pdf) ⭐值得阅读
- [How to Evaluate AI Agents From Tool Calls to Task Completion -- NVIDIA](https://developer.nvidia.com/blog/how-to-evaluate-ai-agents-from-tool-calls-to-task-completion/) ⭐值得阅读
- [ClawBench实测8款Agent：真能完成日常在线任务吗？ -- Link Researcher](https://linkresearcher.com/theses/7b4147d0-60fc-4fab-9aa9-1d9cfba49870) ⭐值得阅读
- [Agent 评测体系：三层分类与一条流程 -- CSDN](https://blog.csdn.net/2401_87562521/article/details/169168074)
