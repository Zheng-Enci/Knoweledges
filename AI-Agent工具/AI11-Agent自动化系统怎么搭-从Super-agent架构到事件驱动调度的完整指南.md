# Agent 自动化系统怎么搭：从 Super-agent 架构到事件驱动调度（全文可跑）

> **核心结论**：Agent 系统设计里最难的不是让模型变强，而是解决「人的注意力瓶颈（attention bottleneck）」——DeepSeek 在《Super-agent 设计探索》里一句话点透：**单任务的上限取决于模型能力，多任务的上限取决于人的注意力**。你同时只能盯 3 到 5 个会话，那再强的模型也只能被你拖慢。解法是把任务起点从人身上拿掉：用事件（event）当触发器、让 Router 分派、Worker 并行干活，人只在必须拍板时介入。这套「AI 当主管、AI 干活、人做决策」的调度架构，正是 1380 年朱元璋废丞相后自己处理 400 多件事、最终崩溃的历史教训的现代版本。

## 目录

- 1. 一句话结论
- 2. 注意力瓶颈（Attention Bottleneck）：为什么你只能同时跟进 3 到 5 个会话
- 3. 历史教训（Historical Lesson）：朱元璋废丞相，一个人处理 400 多件事的崩溃
- 4. Super-agent 双层架构（Two-Layer Architecture）：Router 分派，Worker 干活
- 5. 事件驱动（Event-Driven）：把任务的起点从人身上拿掉
- 6. 两级过滤与订阅直通（Two-Level Filtering）：让 AI 主动找活干
- 7. Watchdog 外部控制回路（External Control Loop）：监控 Worker 不跑偏
- 8. 落地实践（Practice）：事件中台怎么搭，普通用户也能上手
- 9. 领导力思维（Leadership Mindset）：人只做关键决策
- 10. 完整可运行代码（Runnable Code）：事件驱动调度最小实现
- 11. 对照表：症状 → 原因 → 解法
- 12. 判断收尾

## 1. 一句话结论

先建立一个直觉 🎭：**Agent 系统像一支团队**——你不可能对每个员工的每件小事都点头，否则你就是那个被奏折淹没的皇帝。好团队的特征是「能自己处理的不上报，拿不准的才请你拍板」，Agent 调度系统要复刻的正是这个结构。

这套架构的本质是三句话：

- **Router（路由器）**：持续在线的全局协调节点，接消息、分任务、管上下文，像一个「AI 主管」。
- **Worker（工作器）**：一批相互隔离的会话，并行执行具体任务，像「干活的下属」，不直接回复你，只向 Router 汇报。
- **人只做决策**：你不再发起每个任务，只在必须拍板时介入，把注意力留给真正需要判断的事。

一句话：**Agent 自动化的终点，是让系统像一支好团队一样自行推进，而不是像提线木偶等你拉一下才动一下。**

## 2. 注意力瓶颈（Attention Bottleneck）：为什么你只能同时跟进 3 到 5 个会话

DeepSeek 在《Super-agent 设计探索：迈向更自主的 Agent 系统》开篇给了最扎心的一句：

> 一个人通常只能同时跟进 **3 到 5 个活跃的会话**，在这种设计下，**单任务的上限取决于模型能力，多任务的上限取决于人的注意力**。

这句话值得拆开看：

- 现在大多数人用 Agent 还是「聊天模式」：打开 Claude Code 或 Codex，给一个任务，看着它干，干完检查，再给下一个任务。
- 这个模式里，**所有事情的起点都是你**——你不打开窗口，什么都不发生。模型再强，你能同时推进的事 = 你盯得过来的那几个窗口。
- 所以真正限制你的不是模型，是**你只有一对眼睛**。哪怕挂了 10 个 Agent 在跑，你没有精力逐个盯，等于没有并行。

打个比方 🎭：**这就像你雇了 10 个工人，但你必须亲手给每个人递砖、盯着每个人干活**——10 个工人是雇了，你的双手却只有一双，瓶颈从来不在工人数量。

Super-agent 设计探索参考资料：
- [DeepSeek 提出 Super-agent 架构设计：Router 与 Worker 双层架构 -- IT之家](https://m.ithome.com/html/1020615.htm)
- [DeepSeek发布全新Agent架构“Super-agent”，让AI调度AI -- 环球网](http://m.toutiao.com/group/7703023092108362283/)

## 3. 历史教训（Historical Lesson）：朱元璋废丞相，一个人处理 400 多件事的崩溃

注意力瓶颈不是 AI 时代的新问题，历史上早就上演过无数次。

- **1380 年**，朱元璋借着胡惟庸案，把中书省和丞相一起废了，六部直接对皇帝负责，天下大事全部直通他本人。
- 报应来得很快：**洪武十七年九月**，给事中张文辅给他算了一笔账——从十四号到二十一号，**8 天**，内外衙门送来的奏札 **1660 件**，要处理的事 **3000 多件**。
- 平均下来，一天 200 多份奏札、**400 多件事**。朱元璋是出了名的勤快，也绷不住了，当场对大臣们说：「**朕一人处此多务，岂能一一周遍**」——我一个人管这么多事，怎么可能每件都顾得过来？

这跟 AI 时代的你有什么区别？

- 六百多年前，皇帝接的是六部九卿的奏折；今天，**递奏折的是一群 Agent**——告警、日报、待办、PR 评论、CI 失败，全部堆到你面前。
- 皇帝删掉了「丞相」这个中间层，代价是**自己成了瓶颈**；你要是删掉了所有中间层，让每个 Agent 都直接找你，你也会成为瓶颈。
- 区别只在于：朱元璋没有选择，只能硬扛；而你可以设计一个「调度系统」，让 Agent 互相分派、自行推进，只把需要决策的事推到你面前。

这个特质，其实就叫 **领导力（leadership）**：不是事事亲力亲为，而是让系统在大部分时间里自行运转，你只做最关键的判断。

## 4. Super-agent 双层架构（Two-Layer Architecture）：Router 分派，Worker 干活

DeepSeek 给出的答案是一套经典的 **Router / Worker 双层架构**，本质是把「团队」结构数字化：

- **Router 层（Router layer）**：一个持续运行的全局协调节点。它承接所有人类交互、维护全局上下文、统一接收群聊 / GitHub / 邮件等各渠道消息，然后把任务分派给 Worker。它是唯一的「AI 主管」。
- **Worker 层（Worker layer）**：一批在相互隔离的会话中并发执行具体任务的 Agent，比如问题复现、代码审查、功能开发。**Worker 不直接回复用户**，而是把状态和结果汇报给 Router，由 Router 统一对外。
- **Subagent**：Worker 在执行中还能再派生 Subagent（子代理）处理子任务，形成多级分工。

这样设计解决了什么问题？

- **上下文隔离（context isolation）**：每个 Worker 只维护自己任务相关的上下文，不会被别的任务污染，也不互相挤占 context window（上下文窗口）。
- **全局不失焦**：Router 持有全局上下文，能判断「这个任务该交给谁」，但不必自己下场干活。
- **并行成为可能**：多个 Worker 各自推进，速度不再受限于你的眼睛。

用团队类比 🎭：**Router 是项目经理，Worker 是执行工程师**——项目经理不写代码，但他知道每个工程师在干什么、该接哪个活；工程师埋头干活，做完向项目经理汇报，而不是每个都冲过来找你签字。如果你还在纠结「该用单 Agent 还是多 Agent 编排」，在[Agent 架构怎么选：从单 Agent 到多 Agent 编排的选型决策指南](https://juejin.cn/post/7702483654677364774)中我们讲过选型判据，本文的 Router/Worker 双层架构就是多 Agent 编排的一种具体落地形态。

架构参考资料：
- [DeepSeek 开源 Super-agent 架构：AI 主动发现 Bug 并提交 PR -- 腾讯云开发者社区](https://cloud.tencent.com/developer/article/2773523)
- [DeepSeek开源Super-agent，AI开始自己给AI派活 -- 36氪](https://36kr.com/p/4052484771681158)

## 5. 事件驱动（Event-Driven）：把任务的起点从人身上拿掉

双层架构解决的是「怎么分工」，**事件驱动（event-driven）** 解决的是「谁来发起任务」——答案：**不要人来发起**。

- 聊天式用法的最大弊端：任务的起点永远是你。你只要不开口，一切都停摆。
- 事件驱动的做法：**把「信号」当成触发器**。定时任务（cron）、Webhook、CI 结果、邮件、GitHub 评论，任何信号都可以触发一个 Agent 去干活。
- 比如告警触发 → Agent 自动查日志 → 定位到 bug → 直接修 → 提交 PR → 把结果汇报给你。整个过程你不需要出现在起点。

这正是 DeepSeek 强调的「主动性（proactivity）」来源：系统不是「等命令」，而是「订阅信号」。

- 定时任务就是一个「事件搜寻器」：固定每分钟或每小时去查一次，有新东西就触发对应 Worker。
- Webhook 是「事件通知器」：外部系统主动把事件推过来，比如「这个 PR 有新的 review 评论」。

用朱元璋的比喻 🎭：**好的团队从不等你下命令**——大臣们遇见事，能自己处理就处理掉，只有拿不准的才上报给你。事件驱动就是把「大臣们」变成「自动运转的 Agent」，把「只有拿不准的才上报」变成调度规则。

参考资料：
- [折腾了整整1年，毫无保留地分享一下我这套Agent自动化系统 -- 人人都是产品经理](https://www.woshipm.com/ai/6487627.html) ⭐值得阅读

## 6. 两级过滤与订阅直通（Two-Level Filtering）：让 AI 主动找活干

「所有信号都触发 Agent」是灾难——一天几百条消息，全处理等于没处理。DeepSeek 的关键设计是**两级过滤（two-level filtering）**，借鉴了操作系统的 fast path / slow path 思想：

- **第一级（Fast Path，快速路径）**：程序层规则先筛掉大部分噪音——来源白名单、关键词规则、事件类型判断，**快且免费**，不消耗模型。
- **第二级（Slow Path，慢速路径）**：剩下需要语义判断的事件，才交给大模型结合上下文判断「值不值得介入」，**灵活但贵**。

这样做的收益很直接：**90% 以上的噪音在程序层就被过滤掉了，大模型只处理真正值得关注的事件**，token 成本大幅下降，还避免了「每来一条消息就唤醒一个 Agent」的资源浪费。

另一个关键机制是**订阅与直通（subscription & pass-through）**：

- DeepSeek 把同一个话题（IM 群聊）或同一个 PR 下的连续事件定义为 **Thread（线程）**。
- Router 只负责新任务的**冷启动（cold start）**：任务刚创建时由它分派给某个 Worker。
- 之后这个 Thread 的后续事件，**由程序直接推送给订阅它的 Worker**，不再绕回 Router。比如 Worker 接手一个 GitHub PR 后直接订阅后续评论，新的修改意见无需 Router 转发。

这解决了什么问题？**Router 不会被高频后续事件压垮**，它只处理「新任务来了该交给谁」这种低频决策；已归属的后续事件走直通，又快又省。

参考资料：
- [拆解DeepSeek Super-agent：经典系统思想的Agent新用 -- CSDN博客](https://blog.csdn.net/ChesterXue/article/details/169720042) ⭐值得阅读
- [DeepSeek Harness Team Open-Sources a Super-agent Prototype -- Pandaily](https://pandaily.com/deepseek-harness-super-agent-prototype-router-worker-event-driven-watchdog-open-source-mit)

## 7. Watchdog 外部控制回路（External Control Loop）：监控 Worker 不跑偏

让 Agent 自主干活，最大的风险是**它跑偏了没人知道**。DeepSeek 在主干架构之外加了一个独立的 **Watchdog Session（看门狗会话）**，形成外部控制回路（external control loop）：

- 它不是 Worker 之一，而是一个**独立的监控者**，不参与具体任务。
- 它监控两类问题：**基础设施问题**（接口报错、状态恢复失败等）和**方向问题**（Worker 是否取得实质进展、执行方向是否偏离目标）。
- 发现异常时，Watchdog 会主动介入修复，比如终止一个原地打转的 Worker、或纠正方向。

这对应的是团队管理里的「**巡检（inspection）**」：项目经理不可能事无巨细盯着每个人，但必须有一个人定期检查「大家是不是在往对的方向走」。

对个人用户来说，这个思想可以简化成一条规则：**定期 review 每个 Worker 的产出与进展，发现没有实质进展的就停掉或重新指派**——不需要你全程盯着，但需要你设一个「检查点」。

## 8. 落地实践（Practice）：事件中台怎么搭，普通用户也能上手

DeepSeek 的架构是给大团队的开源原型，普通人怎么落地？我在近一年的 Agent 自动化实践中，沉淀出一套简化版——**事件中台（event middleware）**，核心就三件事：

**第一，定义事件（Define Events）**。把「所有可能触发 Agent 工作的信号」统一归纳成事件。世间万物的信号触发，都可以归纳为一个事件：

| 事件类型 | 触发来源 | 典型 Agent 动作 |
|---------|---------|----------------|
| 定时事件 | cron 定时任务 | 每天早上的系统日报、每周到期复查 |
| 告警事件 | 监控系统 / Webhook | 出问题就查日志、定位 bug、直接修复 |
| 消息事件 | 群聊 / 邮件 / IM | 识别潜在缺陷，主动复现并尝试修复 |
| 代码事件 | GitHub PR / CI 结果 | 代码审查、CI 失败自动排查 |

**第二，统一路由（Unified Routing）**。所有事件进中台，统一格式、统一路由、统一去重——新增一类事件只需加一条规则，不需要重写流程。中台按规则叫醒对应的 Agent（可以指定不同的模型：运维用便宜大碗的，浏览器操控用擅长工具的）。

**第三，人工决策点（Human Decision Points）**。中台把 Agent 的产出整理成「待决策卡片」推给你（比如在飞书里点卡片），**你只在卡片上做少数关键决策**：同意 / 驳回 / 修改，其余全部让系统自己跑。

我的实践结论：这套「事件中台 + 分层 Agent + 卡片决策」的组合，让**一个人同时运转了十几个自动化 Agent**（告警处理、日报、浏览器操控、复查等），而不需要逐个窗口盯着——这就是把注意力瓶颈从「3 到 5 个会话」拓宽到「十几个 Agent」的实战路径。

参考资料：
- [折腾了整整1年，毫无保留地分享一下我这套Agent自动化系统 -- 人人都是产品经理](https://www.woshipm.com/ai/6487627.html) ⭐值得阅读

## 9. 领导力思维（Leadership Mindset）：人只做关键决策

架构聊完，最后落到认知层面——这套系统的核心不是技术，而是**领导力思维**。

- **好的团队不会事事跟你汇报**：它自行推进，只把需要你拍板的事拿给你，剩下的自己干掉。你要给的，是充分的信任。
- **任务的起点要从人身上拿掉**：如果你还是「不打开窗口什么都不会发生」，那不管模型多强，你能同时推进的事永远等于你盯得过来的窗口。
- **你的角色是皇帝，但不是朱元璋**：朱元璋废了丞相自己扛 400 多件事，是失败的管理；你的目标应该是「**只做最关键的决策，其余全部自动化**」。

这个特质的最终形态是：**你是系统的目标设定者与最终决策者，Agent 是执行层，事件是驱动力**。系统 90% 的时间在自行运转，你只需要在关键节点出现——就像真正的领导，平时不出现，出现时必拍板。

## 10. 完整可运行代码（Runnable Code）：事件驱动调度最小实现

下面是一段**复制粘贴就能跑**的最小事件驱动调度器，用标准库实现：事件队列 → 两级过滤（规则过滤 + 语义判断）→ Router 分派 → Worker 执行 → 结果汇报。跑一遍，你就理解整个架构的核心循环。

运行：`python agent_dispatcher.py`（无需任何第三方库）。

```python
"""
事件驱动 Agent 调度器最小实现
演示：事件 → 两级过滤 → Router 分派 → Worker 执行 → 汇报结果
"""
import queue          # 事件队列（线程安全）
import time            # 模拟 Worker 执行耗时
import random          # 模拟慢路径语义判断的随机放行

# ---------- 事件定义 ----------
class Event:
    """事件对象：携带来源与负载"""
    def __init__(self, source, payload):
        self.source = source      # 来源：cron / webhook / alert / ci
        self.payload = payload    # 负载：事件内容

# ---------- 第一级过滤：Fast Path（规则过滤，不消耗模型） ----------
FAST_PATH_RULES = {
    "cron":     True,          # 定时任务直接放行
    "alert":    True,          # 告警直接放行
    "webhook":  lambda p: "review" in p,  # webhook 只放行含 review 的消息
    "ci":       lambda p: "failed" in p,  # CI 只放行失败事件
}

def fast_path_filter(event):
    """程序层规则过滤：快且免费，挡掉大部分噪音"""
    rule = FAST_PATH_RULES.get(event.source, False)
    if callable(rule):                       # 规则是函数就调用判断
        return rule(event.payload)
    return rule

# ---------- 第二级过滤：Slow Path（语义判断，消耗模型） ----------
def slow_path_filter(event):
    """模拟大模型语义判断：是否值得介入"""
    if event.source == "cron":               # 定时任务语义明确，直接放行
        return True
    if "critical" in event.payload or "error" in event.payload:
        return True                          # 关键/错误类事件值得介入
    return random.random() < 0.3             # 其余 30% 概率放行（模拟语义判断）

# ---------- Router 分派 ----------
def router(event):
    """Router：根据事件来源决定交给哪个 Worker"""
    routing_table = {
        "cron":    "worker_daily_report",    # 定时任务 → 日报 Worker
        "alert":   "worker_debug_fix",       # 告警 → 排查修复 Worker
        "webhook": "worker_code_review",     # 消息 → 代码审查 Worker
        "ci":      "worker_ci_fix",          # CI 失败 → CI 修复 Worker
    }
    return routing_table.get(event.source, "worker_default")

# ---------- Worker 执行 ----------
def worker_execute(worker_id, event):
    """Worker：模拟执行任务，完成后汇报结果"""
    print(f"[{worker_id}] 处理事件：{event.source} -> {event.payload}")
    time.sleep(0.3)                          # 模拟耗时
    return f"完成 {event.source} 任务：{event.payload[:12]}..."

# ---------- 主循环：事件驱动调度 ----------
def main():
    """事件中台主循环：收事件 → 过滤 → 分派 → 执行 → 汇报"""
    event_queue = queue.Queue()              # 事件队列（先进先出）

    # 预置一批事件（模拟：定时任务 + 告警 + webhook + CI 混在一起）
    test_events = [
        Event("cron",    "daily report due"),
        Event("alert",   "service down critical"),
        Event("webhook", "PR #42 has review comment"),
        Event("webhook", "PR #42 spam message"),   # 该被一级过滤挡掉
        Event("ci",      "build failed on main"),
        Event("ci",      "build passed on main"),  # 该被一级过滤挡掉
    ]
    for ev in test_events:
        event_queue.put(ev)

    while not event_queue.empty():
        event = event_queue.get()            # 取一个事件

        if not fast_path_filter(event):      # 第一级过滤：程序层挡噪音
            print(f"[过滤] 一级规则直接丢弃：{event.source} -> {event.payload}")
            continue
        if not slow_path_filter(event):      # 第二级过滤：语义判断
            print(f"[过滤] 二级语义判断丢弃：{event.source} -> {event.payload}")
            continue

        worker_id = router(event)            # Router 分派
        result = worker_execute(worker_id, event)  # Worker 执行
        print(f"[汇报] {result}")

if __name__ == "__main__":
    main()
```

**怎么读这段代码**：`fast_path_filter` 就是 Fast Path——cron 和 alert 直接放行、webhook 只放行含 `review` 的消息、CI 只放行失败事件，噪音在这层被规则挡掉，零模型成本；`slow_path_filter` 模拟 Slow Path 的语义判断（含 `critical` 或 `error` 的必放行）；`router` 用一张路由表把事件分派给对应 Worker——这就是「事件中台统一路由」的最小形态。把 `worker_execute` 换成真实调用 Claude / Codex / 本地脚本，就是一套可用的自动化骨架。

## 11. 对照表：症状 → 原因 → 解法

| 症状 | 原因 | 解法 |
|------|------|------|
| 同时开多个 Agent 窗口，哪个都盯不过来 | 注意力瓶颈：你同时只能跟进 3 到 5 个会话 | 用事件驱动，让任务起点从人身上拿掉 |
| 你不打开窗口，什么都不会发生 | 聊天式用法：任务起点永远是你 | 改成信号触发：cron / Webhook / 告警自动唤醒 Agent |
| 每个 Agent 都直接找你汇报，信息爆炸 | 没有中间层，你成了朱元璋 | 加 Router 层：统一接消息、分派、维护上下文 |
| 一个任务卡死，其他全部停摆 | 没有上下文隔离，任务互相污染 | 用 Worker 隔离会话，各任务独立推进 |
| 消息太多，Agent 疲于奔命，token 烧钱 | 所有事件都触发 Agent | 两级过滤：程序规则挡噪音，语义判断留精华 |
| Router 被高频后续事件压垮 | 后续事件全绕 Router 转发 | 订阅直通：已归属事件直接推给对应 Worker |
| Agent 跑偏了没人知道，白干半天 | 缺少监控回路 | 加 Watchdog：定期检查实质进展，异常即介入 |

## 12. 判断收尾

**什么时候该上这套架构**：你手头有多个重复性任务（告警、日报、复查、CI 修复）需要同时推进，且愿意花时间搭一次事件中台——这套架构的收益是「注意力从 3 到 5 个会话拓宽到十几个 Agent」，边际成本极低。**什么时候不该上**：你只是偶尔用 Agent 处理单个任务，没有稳定的重复性工作流——此时搭中台属于过度设计，一个聊天式 Agent 反而更快。判断标准只有一条：**有没有「持续发生、值得自动处理」的事件流**。

本专栏《AI-Agent 工具》从 Agent 记忆、工具调用、架构选型一路讲到自动化调度系统设计，每篇都配可直接运行的代码与实战案例，持续更新。想在 Agent 实战里少踩坑，可在专栏页订阅。

参考资料（综合）：
- [Super-agent 设计探索：迈向更自主的 Agent 系统（原文）-- IT之家](https://m.ithome.com/html/1020615.htm)
- [折腾了整整1年，毫无保留地分享一下我这套Agent自动化系统 -- 人人都是产品经理](https://www.woshipm.com/ai/6487627.html) ⭐值得阅读
- [拆解DeepSeek Super-agent：经典系统思想的Agent新用 -- CSDN](https://blog.csdn.net/ChesterXue/article/details/169720042) ⭐值得阅读
- [DeepSeek 开源 Super-agent 架构：AI 主动发现 Bug 并提交 PR -- 腾讯云](https://cloud.tencent.com/developer/article/2773523)
- [DeepSeek开源Super-agent，AI开始自己给AI派活 -- 36氪](https://36kr.com/p/4052484771681158)
