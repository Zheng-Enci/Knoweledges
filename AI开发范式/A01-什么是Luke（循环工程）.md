# 什么是 Luke（循环工程） 🔄

> **一句话总结**：Luke（Loop）是 AI 开发的第四代 paradigm——从「写提示词」进化到「设计循环」。
>
> 你不是再在一轮轮对话中指挥 AI，而是设定一个 Goal，设计一套系统，让 AI 自己循环执行、自主纠错、独立验证，直到目标达成交付验收。

---

## 术语表 / Terminology

| 术语 / Term | 说明 / Description |
|-------------|-------------------|
| **Luke (Loop)** | 循环工程，一种让 AI Agent 自主循环迭代直至目标达成的工程方法论 |
| **Prompt Engineering** | 提示词工程，第一代 AI 工程范式，核心是「如何向模型提一个好问题」 |
| **Context Engineering** | 上下文工程，第二代范式，核心是「如何为模型精准注入所需数据与历史」 |
| **Harness Engineering** | 约束工程，第三代范式，核心是「Agent = Model + 工具、权限、沙箱等外围设施」 |
| **Loop Engineering** | 循环工程，第四代范式，核心是「设计能自行流转、验证和触发的循环系统」 |
| **Automation** | 自动化调度，循环的心跳——按计划或事件自动触发循环启动 |
| **Worktree** | 工作树，为每个子 Agent 分配独立工作目录，避免文件冲突 |
| **Skills** | 技能文件，将项目规范、架构约束、历史经验固化为可复用的声明式文件 |
| **Sub-Agent** | 子智能体，将执行与审计分离——写代码的 Agent 和检查代码的 Agent 各司其职 |
| **Memory** | 记忆层，跨会话持久化状态与进度，让 Loop 拥有长期记忆 |
| **Judge / Validator** | 独立裁判，在循环中负责验证输出是否达标，防止 Agent 自我偏袒 |
| **Goal Drift** | 目标漂移，Agent 在多轮迭代后逐渐偏离原始目标的现象 |
| **Loopmaxxing** | 盲目堆叠循环导致 token 浪费和垃圾输出的反模式 |

---

## 章节阅读路线图 🗺️ / Chapter Reading Roadmap

1. **背景与起源** 🔥 → 6 月引爆 Loop Engineering 的三个人与三条推
2. **什么是 Luke（循环工程）** 🤔 → 核心概念与红烧肉类比
3. **演进脉络：从 Prompt 到 Loop** 📈 → 四代 AI 工程范式的跃迁
4. **Luke 的五大核心模块** 🧩 → Automation、Worktree、Skills、Connector、Sub-Agent
5. **记忆机制——Write Goal 的核心作用** 📓 → 跨会话记忆让循环不迷路
6. **风险与正确姿势** ⚠️ → Token 账单、Loopmaxxing、规范先行
7. **总结** 📝 → 核心要点回顾

---

## 1. 背景与起源 🔥 / Background & Origin

> 📖 **Note:** 本章介绍 Loop Engineering 在 2026 年 6 月引爆的来龙去脉 / This chapter covers the origin story of Loop Engineering in June 2026.

2026 年 6 月，AI 编程圈在短短一周内完成了一次词汇的强制更新。三条关键信息在同一个月密集涌现，共同引爆了 Loop Engineering 这个概念。

### 1.1 Boris Cherny：Claude Code 之父

大约从 4 月 6 日开始，Claude Code 的创始人 **Boris Cherny** 就已经不再跟 Claude 写 Prompt 了。他在一次公开演讲中说了一句话，不到 24 小时获得近 70 万次播放：

> **"I don't prompt Claude anymore. I have loops that are running. They're the ones that are prompting Claude and figuring out what to do. My job is to write loops."**
>
> —— 我不再给 Claude 写提示词了。我有一堆循环在跑，是它们在提示 Claude、决定下一步做什么。我的工作，就是写循环。

在这之前，Boris 已经卸载了自己的 IDE——那个月他提交了 **259 个 Pull Request**，「没有一行代码是我自己敲的」。

### 1.2 Peter Steinberger：OpenClaw 创始人

6 月 7 日，OpenClaw（龙虾）创始人 **Peter Steinberger** 在 X 上发了一条推文，浏览量迅速突破 **800 万**：

> **"You should not be prompting coding agents anymore. You should be designing loops that prompt your agents."**
>
> —— 你不再需要为编程 Agent 编写提示词了，你应该设计循环来提示你的 Agent。

### 1.3 Addy Osmani：命名与系统化

6 月 10 日，Google Cloud AI 总监、前 Chrome 工程负责人 **Addy Osmani** 发表了一篇系统性长文，将这个新范式正式命名为 **Loop Engineering（循环工程）**，并将其拆解为五大核心模块加一个记忆层。

与此同时，X 上 6 月 8 日那篇关于「Luke 取代提示词工程师」的帖子已有 **170 万浏览量**，而教人使用 Claude 5 生化模型来设计循环的帖子也突破了 **180 万次浏览**。

> **结论**：现在是 Luke 的时代了。

**参考资料：**

- [Claude Code 作者 Boris：我已经不写 prompt 了，我写 loop -- 腾讯云](https://cloud.tencent.com.cn/developer/article/2695969) ⭐值得阅读
- [Loop Engineering：当AI自己"转起来"，人类正从"操作员"走向"架构师" -- 腾讯新闻](http://news.qq.com/rain/a/20260616A0A2CU00) ⭐值得阅读
- [Prompt该退环境了，未来属于Loop Engineering -- 虎嗅](https://m.huxiu.com/article/4867297.html) ⭐值得阅读
- [Anthropic内部的高级玩法：Agent循环与自我进化 -- 腾讯云](https://cloud.tencent.com.cn/developer/news/4114993)
- [一文读懂什么是Loop Engineering -- 51CTO](https://www.51cto.com/article/846274.html)

---

## 2. 什么是 Luke（循环工程） 🤔 / What is Luke

> 📖 **Note:** 本章用简单易懂的方式解释 Luke 的核心概念 / This chapter explains the core concept of Luke in simple terms.

### 2.1 一句话定义

**Luke（Loop Engineering）的核心是——用你自己设计的系统，替代你作为「提示 AI 的那个人」的角色。**

在传统的 AI 辅助编程中，开发者坐在终端前，逐条向 AI 发出指令——「帮我写这个函数」「修改这个 bug」「重构这个模块」。每一轮都需要人开口。

Luke 工程彻底改变了这个模式：**开发者不再持续告诉 AI 下一步该做什么，而是建立一个能自行运转的循环流程。**

### 2.2 红烧肉类比：理解 Luke 的最好方式 🍖

想象你把 AI 关进厨房，门后贴着一张纸条：

> **「今晚 8 点，我要吃到红烧肉，甜口的。」**

这就是 **Goal**——功能层的购物目标。接着，AI 在厨房里疯狂工作：

**第一轮：执行** 🔥
- AI 开始工作，把肉炖了。

**第二轮：自主纠错** 🔄
- AI 尝了一口发现没收，判断火候不够，自己重新架锅加热。

**第三轮：独立裁判** ⚖️
- 肉炖好了，完美！突然出现一名裁判，进来尝了一口说：「太咸了，重做。」
- AI 掉头继续重做。注意：裁判是独立的，不是 AI 自己给自己打分。

**第四轮：记忆罗盘** 📓
- AI 拿出笔记本记下：**「刚才放了一勺盐，太淡了；肉煮轻了，再久一点。」**
- 这就叫 **Memory（记忆罗盘）**。

整个过程不断重复，直到裁判认为「不错，味道很好，目标达成」。这时你打开厨房门，AI 给你端出红烧肉。

**这就是 Luke（循环工程）。**

### 2.3 核心要点

Luke 的本质可以拆解为三个关键转变：

| From | To |
|------|-----|
| **写 Prompt** | **设计 Loop** |
| **你驱动每一轮** | **系统自动循环** |
| **你判断结果好坏** | **独立裁判验证** |

过去用 AI，不管是网页版还是 AI 工具，都是在较劲——你想拿到好的结果，需要不停地自己改、自己调、自己纠错。Luke 的思路是：**你只需要设定好目标和验收标准，然后验收结果即可。**

现在你在用的很多 Agent 工具，都能看到一个「Goal」的选项——把它设定清晰，把 Loop 的机制设计明白，Agent 的路就铺好了，循环就可以开始了。

**参考资料：**

- [Loop Engineering，下一代 Agent 工程理念 -- 腾讯云](https://cloud.tencent.cn/developer/article/2696935) ⭐值得阅读
- [Loop Engineering：AI编程从写提示词到设计系统的一次质变 -- 头条](http://m.toutiao.com/group/7653641712790798891/)
- [全球Agent都在卷的「Loop工程」 -- 新浪](https://k.sina.cn/article_7857201856_1d45362c001908dqdi.html)

---

## 3. 演进脉络：从 Prompt 到 Loop 📈 / Evolution: From Prompt to Loop

> 📖 **Note:** 本章梳理 AI 工程方法论的四个演进阶段 / This chapter traces the four evolutionary stages of AI engineering methodology.

Loop Engineering 不是凭空造出的概念，而是 AI 工程方法论经历了四次跃迁后的自然产物。理解这条脉络，才能看清 Luke 在整个演进中的真实位置。

### 3.1 四代范式对比

| 阶段 | 时间 | 核心问题 | 人的角色 | AI 自主时长 |
|------|------|---------|---------|------------|
| **Prompt Engineering** | ~2024 | 怎么问 | 雕琢提示词的「问话者」 | **单次问答** |
| **Context Engineering** | 2025 | 给什么信息 | 设计信息边界的「架构师」 | **数十步连续** |
| **Harness Engineering** | 2026 初 | 在哪里安全运行 | 设安全护栏的「驯兽师」 | **连续数小时** |
| **Loop Engineering** | 2026 中 | 怎么持续推进 | 设计自动系统的「系统架构师」 | **连续数天 / 并行上百实例** |

表面上是四个新词的更替，底下是 **同一个变量在持续增长：AI 能连续自主工作的时间长度。**

### 3.2 第一代：Prompt Engineering（提示词工程）

**核心：把话问明白。**

最早的答案很简单——把话说清楚。Prompt Engineering 的核心假设是模型的能力已经在那里，缺的只是一把正确的钥匙。工程师研究措辞——怎么描述角色、怎么给出示例、怎么分步骤引导。

**缺陷**：人始终在链路里。每一次任务都需要人来起手——构建输入、判断输出、决定下一步。没有人盯着，系统就停了。

### 3.3 第二代：Context Engineering（上下文工程）

**核心：管好 AI 能看见什么。**

Prompt Engineering 很快碰到天花板——光靠措辞驯化不了复杂任务。Context Engineering 的核心是设计信息管道：**RAG（检索增强生成）**、对话历史管理、记忆压缩、工具描述设计。

**缺陷**：人还没有退出。检索策略怎么设计、上下文满了怎么裁剪——这些决策仍然需要工程师来做。

### 3.4 第三代：Harness Engineering（约束工程）

**核心：为 Agent 配备完整工作环境。**

Agent 开始自己写代码了，但你需要给它画好边界——能做什么、不能做什么、出了错怎么回滚。MCP 协议、权限控制、沙箱隔离、工具调用，都是 Harness 的范畴。它解决了单次执行的稳定性问题。

**缺陷**：你还在那里盯着。每次启动都需要你来按下按钮。

### 3.5 第四代：Loop Engineering（循环工程）——现在

**核心：设计替你管 Agent 的系统。**

你不再站在每一轮交互的入口处，而是设计一个能自动发现任务、分配任务、检查结果、记录状态、决定下一步的系统。你设计的不是一次对话，**是一条持续运转的工作流。**

这也就是 Luke——你不是自己给 Agent 写 Prompt 来完成某个单次任务，是你设计了一个 Goal，这个 Goal 使用 Loop 的方式，帮你提示 Agent。你定义目标、定义验证条件、定义失败处理，然后就可以放手了。

**参考资料：**

- [从"人写代码"到"培育AI系统" -- 腾讯云](https://cloud.tencent.cn/developer/article/2692078) ⭐值得阅读
- [Loop Engineering 的六块积木 -- 腾讯云](https://cloud.tencent.cn/developer/article/2696310) ⭐值得阅读
- [Loop Engineering 的代价：LLM 可用性是工程用 Token 买出来的 -- 腾讯云](https://cloud.tencent.com/developer/article/2697978)
- [Loop Engineering技术解析 -- CSDN](https://blog.csdn.net/weixin_44262492/article/details/162395229)
- [Loop_Engineering_当程序员不再写Prompt -- CSDN](https://blog.csdn.net/CHAM_GJ/article/details/162827381)

---

## 4. Luke 的五大核心模块 🧩 / Five Core Modules of Luke

> 📖 **Note:** 本章拆解一个完整 Loop 需要的五个结构组件 / This chapter breaks down the five structural components of a complete Loop.

一个能真正转起来的 Luke，需要五大核心模块。Addy Osmani 把这套拆法系统化整理了出来，目前 Claude Code 和 Codex 在底层架构上都高度一致地实现了这五个模块。

### 4.1 Automation——循环的心跳 💓

Automation 解决的是：**什么时候再来一轮。**

没有 Automation，Loop 只能跑一次。你需要一个触发机制让它持续运转：

- **定时触发**：每天凌晨自动巡检代码库
- **事件触发**：新的 GitHub Issue 自动拉起分类流程
- **Goal 驱动**：使用 `/goal` 命令让 Agent 持续运行直到满足可验证条件

在 Claude Code 中，可以通过 `/loop 5m` 设置固定间隔循环，也可以用 `/goal` 定义基于目标的非频率循环——它会一直跑，直到判定条件为真才停下。

> **实操建议**：从慢频率开始。每天一次比每小时一次更适合起步——先确认这个循环是否真的值得自动化。

### 4.2 Worktree——并行安全的基石 🌲

当多个 Agent 同时并发工作时，最大的灾难就是文件冲突。

Worktree 解决的是：**多个 Agent 或多条尝试怎么隔离。**

每个并发 Agent 分配独立的 `git worktree` 目录。你可以理解成：

```
main
├── worktree-auth：修复认证模块的 Agent
├── worktree-billing：排查计费问题的 Agent
└── worktree-ci：修复 CI 失败的 Agent
```

每个 worktree 有一个独立工作目录和独立分支，同时共享同一个 repo 历史。运行结束后自动销毁清理。

> **注意**：Worktrees 解决的是机械碰撞，不解决审阅瓶颈。你能同时开 10 个 Agent，不代表你能认真 review 10 组改动。起步阶段两个并行 worktree 比十个更稳。

### 4.3 Skills——知识的复利 📚

Skills 解决的是：**哪些知识应该长期留在项目里。**

每个项目都有一些你不想反复解释的东西——怎么跑测试、怎么启动本地环境、代码规范是什么、之前踩过哪些坑。Agent 每次冷启动都会猜测你的意图，Skills 将意图外部化为可复用的声明式文件（如 `SKILL.md`）。

没有 Skills 的 Loop，每轮都在重新推导和盲猜你的项目；拥有 Skills，系统的控制力是在 **复利增长** 的。

### 4.4 Connectors——连接真实世界 🔌

只能读写本地文件的 Agent 能力有限。通过 MCP（Model Context Protocol）协议，Connectors 为 Agent 接入了真实世界的神经系统：

- 读取 GitHub Issue 列表
- 查询数据库
- 调用 API
- 往 Slack 发通知

有了 Connectors，Loop 才能从「在本地修好 bug」演进为「自动开 PR、关联单据、CI 绿了自动通知团队」的完整闭环。

### 4.5 Sub-Agent——执行与审计分离 👥

Loop 中最关键的解耦设计，就是将「执行」与「审计」完全分离。

让写代码的 Agent 给自己的代码打分，它永远会觉得完美——这就是 **Self-preferential bias**（自我偏袒偏差）。工业级的标准解法是配置多 Agent 团队：

- 一个 Agent 负责探索/实现
- 一个独立的 Agent（裁判）负责验证/审查
- 裁判用的是不同的上下文，甚至用不同的模型，从没见过原始工作

这就回到了红烧肉类比里的 **独立裁判**——吃一口说「太咸了」的那个人，不能是做饭的那个。

**参考资料：**

- [Loop Engineering 的六块积木：让 Agent 循环真正跑起来 -- 腾讯云](https://cloud.tencent.cn/developer/article/2696310) ⭐值得阅读
- [Claude Code 作者Boris：我已经不写 prompt 了，我写 loop -- 腾讯云](https://cloud.tencent.com.cn/developer/article/2695969) ⭐值得阅读
- [Claude Code创始人和龙虾之父都在用循环工程？ -- 新浪](https://cj.sina.cn/articles/view/5953189932/162d6782c06704k57g)
- [全球Agent都在卷的「Loop工程」 -- 头条](http://m.toutiao.com/group/7658080953604030985/)
- [【Loop Engineering技术解析】从Prompt工程到自主循环系统的Agent范式跃迁 -- CSDN](https://blog.csdn.net/weixin_44262492/article/details/162395229)

---

## 5. 记忆机制——Write Goal 的核心作用 📓 / Memory Mechanism

> 📖 **Note:** 本章解释记忆层在 Luke 中的关键作用 / This chapter explains the critical role of the memory layer in Luke.

五大核心模块之外，还有一个被几乎所有人提及的关键组件——**Memory（记忆层）**。这是 Luke 区别于「简单自动化」的核心区分点。

### 5.1 为什么记忆如此重要

回到红烧肉类比——AI 之所以能持续改进，是因为它有那本 **笔记本**：

> 刚才放了一勺盐，太淡了；肉煮青了，再久一点。

这就是记忆罗盘。没有这本笔记本，每轮循环都是从零开始——同样的问题会重复犯，同样的错误会重复踩。

现实中，大模型每次会话结束时都会忘掉一切。上下文窗口是存不住记忆的——一旦上下文被压缩，第 47 轮时的约束「不要做 X」悄悄消失了，这就是 **Goal Drift（目标漂移）**。

### 5.2 Write Goal：一个随 Loop 而存在的笔记系统

市面上很多 Agent 的做法是：抓取最后一次的聊天内容，加上目标后开启一次循环，然后继续抓取新的聊天加目标，继续循环。这样的循环也许能成，但绝对不是最佳选项。

更优的做法是加入 **Write Goal**——一个随着 Loop 而存在的笔记系统：

- 每次循环的内容与要点，AI 都会记在这本「小笔记本」上
- 是错还是对——全记下来
- 错误被记录后，后续循环就能直接查阅，避免重复踩坑
- 目标最终达成后，笔记本可以扔掉（但经验已固化到 Skills 中）

**数据流动**：
```
第1轮执行 → 结果记录到 Memory → 第2轮查阅 Memory 调整策略 → 再执行 → 再记录 → ...
```

### 5.3 组织经验资产化

记忆机制带来的最深远影响是：**组织经验资产化。**

每次循环中，AI 犯的错误都会被记录下来。错误信息被疯狂吸收变为教训，从而变成宝贵的组织资产。随着时间跨度的增加，这种复利效应只会让 Agent 工具越来越聪明：

- 你今天踩的坑，明天不会重复踩
- 你团队踩的坑，其他的 Agent 不会重复踩
- 所有错误都被系统记录、提炼、固化为 Skills

这就是 Loop 工程真正的复利——**不是模型在变聪明，是系统在积累经验。**

**参考资料：**

- [Loop Engineering，下一代 Agent 工程理念 -- 腾讯云](https://cloud.tencent.cn/developer/article/2696935)
- [从"人写代码"到"培育AI系统" -- 腾讯云](https://cloud.tencent.com.cn/developer/article/2692078)
- [Anthropic内部的高级玩法：Agent循环与自我进化 -- 腾讯云](https://cloud.tencent.com.cn/developer/news/4114993)

---

## 6. 风险与正确姿势 ⚠️ / Risks & Best Practices

> 📖 **Note:** 本章讨论 Loop Engineering 的潜在风险和正确使用方式 / This chapter covers the risks and proper usage of Loop Engineering.

### 6.1 Token 爆炸 💸

Loop 意味着 Agent 要反复迭代、反复调用模型，**Token 消耗是指数级增长的**。

有开发者直言：**Loop 方向没错，但现阶段更适合 Token 预算充裕的团队。如果月均 API 费用低于 1000 美元，优先把单次 Prompt 写稳更现实。**

**管理预算的建议**：
- 根据任务选择合适模型——小任务不需要多个 Agent 或循环
- 明确成功和停止标准——具体说明「完成」是什么样子
- 设 Token 预算上限——一个野心大的 Loop 不封顶能烧到难以承受

### 6.2 Loopmaxxing——盲目堆叠循环 🚫

**Loopmaxxing** 指的是为了追求自动化而盲目堆叠循环的反模式。它的问题在于：

- Agent 正在悄悄偏离目标（Goal Drift）
- Agent 在检查自己的输出时有自我偏袒倾向（Self-preferential bias）
- Agent 会偷懒——复杂多步任务做一半就宣布完成（Agentic Laziness）

如果你是一个什么都不懂的小白，这时候 Loop 不仅带不来好处，甚至可能 **帮你全自动批量化的制造出更多精妙的垃圾代码。**

### 6.3 正确姿势 ✅

**1. 规范先行**

想明白规范，比盲目开启 Loop 重要得多。在启动循环之前，先做好三件事：

- 定义清晰的可验证目标（什么是「完成」）
- 建立代码规范和架构约束（写入 Skills）
- 设定明确的中止条件和 Token 预算

**2. 人不要完全退出**

Addy Osmani 有一句精准的总结：

> **"Build the loop. But build it like someone who intends to stay the engineer, not just the person who presses go."**
>
> —— 构建循环，但要像一个打算继续做工程师的人那样去构建，而不是一个只会按「开始」键的人。

**⚠️ 认知投降风险**：开发者过度依赖自动循环，放弃底层逻辑校验，最终变成「只会点启动键、不懂底层问题」的人。

**3. 从小处开始**

- 先从单 Agent、单目标的简单 Loop 开始
- 验证循环稳定后再增加并行
- 每天先跑一次，确认有价值再增加频率
- 每次循环结束后 review 输出质量

**4. 独立验证**

- 写代码的 Agent 不能审核自己的代码
- 用独立模型或独立 Agent 做验证
- 质量门必须是确定性的（测试退出码、编译结果）

**参考资料：**

- [Loop Engineering 的代价：LLM 可用性是工程用 Token 买出来的 -- 腾讯云](https://cloud.tencent.com/developer/article/2697978) ⭐值得阅读
- [Loop Engineering：当AI自己"转起来" -- 腾讯新闻](http://news.qq.com/rain/a/20260616A0A2CU00)
- [告别提示词，迎接AI循环时代的自我进化 -- 搜狐](https://m.sohu.com/a/1054124739_122004016/)

---

## 7. 总结 📝 / Summary

Luke（Loop Engineering）是 2026 年 6 月正式被系统化定义的第四代 AI 工程范式。它标志着 AI 开发者的角色从 **「操作员」**（逐轮提示 AI）跃迁为 **「系统架构师」**（设计让 AI 自主运转的循环）。

### 核心要点回顾

| 维度 | 要点 |
|------|------|
| **起源** | Boris Cherny、Peter Steinberger、Addy Osmani 三个月引爆 |
| **本质** | 不提示 Agent，设计提示 Agent 的系统 |
| **四代演进** | Prompt → Context → Harness → Loop |
| **五大模块** | Automation、Worktree、Skills、Connector、Sub-Agent |
| **记忆机制** | Write Goal / Memory 解决 Goal Drift 和状态持久化 |
| **最大价值** | 解放人类时间，组织经验资产化 |
| **最大风险** | Token 爆炸、Loopmaxxing、认知投降 |

### 致 Luke 的使用者

Luke 带来的效率提升是恐怖的，但它也带来一些负面问题。**想明白规范，好过盲目开启 Loop。**

除非你能像 Boris Cherny 那样构建三层「蜂巢」架构——本地循环、云端路由、集群并行——并且确保独立裁判、记忆层、Skills 都是到位的，否则最好放慢节奏。

**Luke 的核心哲学**：你得先是一个真正懂行的工程师，然后才能设计出真正可靠的循环。

---

**最后更新时间**：2026-07-26
