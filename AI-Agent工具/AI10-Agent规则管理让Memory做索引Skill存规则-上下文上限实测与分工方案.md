# Agent 规则管理：让 Memory 做索引、让 Skill 存规则——上下文上限实测与分工方案

> **核心结论**：很多人把规则、SOP、工作流全写进 Memory（记忆），但 Claude 和 Codex 的 Memory 都有硬上限——CLAUDE.md 建议控制在 200 行以内，200K 上下文窗口里它每次都会占掉约 40000 字符空间。规则一多，AI 执行任务时会把一堆规则都读一遍，既挤占上下文，又相互干扰。正确的做法只有一句话：**让 Memory 做索引，让 Skill 存规则**。Memory 只负责告诉 AI「这个任务该读哪个 Skill」，具体的规则、SOP、操作手册全部写进 Skill，不写进 Memory。这样规则不容易被挤掉，工作流之间也不会互相干扰。

---

## 目录

- 1. Memory 到底有没有上限：把数字摆出来
- 2. 规则全塞进 Memory 的两种代价
- 3. 核心解法：Memory 做索引，Skill 存规则
- 4. Skill 的加载机制：为什么规则不会挤掉
- 5. 可运行的判断函数：这行规则该进 Memory 还是 Skill
- 6. 对照表：症状 → 原因 → 解法
- 7. 结论：该用 / 不该用的判据

---

## 1. Memory 到底有没有上限：把数字摆出来

先别争论「Memory 有没有上限」这个哲学问题，直接把官方给出的约束数字摆出来。

**CLAUDE.md 的推荐行数**：Anthropic 官方明确建议每个 CLAUDE.md 文件控制在 **200 行以内**。超过这个长度，官方原话是「consume more context and reduce adherence」——占更多上下文、降低遵守度。这不是审美建议，是实测后的工程约束。

**200K 上下文窗口对应多少字符**：在默认的 200K 上下文窗口里，CLAUDE.md 的可用空间约 **40000 个字符**（1M 上下文窗口的模型则是 200000/150000 字符）。这意味着如果规则写得又长又密，单靠一个文件就能吃掉接近整窗的几分之一。

**MEMORY.md 的加载限制**：自动记忆（auto memory）的索引文件 MEMORY.md，每次会话开始时**只加载前 200 行，或前 25KB，哪个先到取哪个**。超过的部分本次会话根本读不到——你写了，但 AI 看不见。

**Skill 的加载成本**：真正按需加载的是 Skill（技能）。Skill 启动时只加载它的 **name + description（约 100 token）**，完整 SKILL.md 正文（<5k token）只有在技能被触发时才进入上下文。

把四个数字放在一起，结论就清楚了：**Memory 是「常驻内存」，Skill 是「按需读取」**。常驻的东西一多，每轮任务都要为无关规则买单。

**参考资料：**

- [How Claude remembers your project -- Claude Code Docs](https://code.claude.com/docs/en/memory) ⭐值得阅读
- [Extend Claude Code -- Claude Code Docs](https://code.claude.com/docs/en/features-overview) ⭐值得阅读
- [Give Claude context: CLAUDE.md and better prompts -- Claude Help Center](https://support.claude.com/en/articles/14553240-give-claude-context-claude-md-and-better-prompts)
- [Agent Skills -- Claude API Docs](https://console.anthropic.com/docs/en/agents-and-tools/agent-skills/overview)

---

## 2. 规则全塞进 Memory 的两种代价

规则一多、全塞进 Memory，会付出两种实实在在的代价。这两种代价不是「性能差一点」，而是会直接让 AI 干不好活。

**代价一：规则被挤掉（被截断）**。Memory 有 200 行 / 25KB 的加载门槛，规则写多了，靠后的规则在会话里根本加载不进去。你以为写了「必须先审代码再提交」，但因为太长排在后面，AI 这轮可能根本没看到。规则没有消失，只是「在窗外的角落里躺着」，而 AI 不会去翻。

**代价二：工作流互相干扰**。当几十条不同主题的规则（数据库迁移、发布清单、代码审查规范）全部塞进同一份 Memory，AI 每次执行任务都要把它们**从头到尾读一遍**。这会产生两类干扰：一是无关规则抢占 attention（注意力），让该执行的规则被稀释；二是规则之间可能相互矛盾，AI 在矛盾中来回摇摆。

打个比方 🎭：Memory 像**电脑的常驻内存**，开机就占着；Skill 像**按需加载的软件**，你点开才载入。把所有软件都做成开机自启，内存很快爆掉，还互相抢资源——这跟规则全塞 Memory 是一个道理。

**参考资料：**

- [Claude Code usage limits and token optimization -- TechRounder](https://www.techrounder.com/pdf/blog/claude-code-usage-limits-token-optimization.pdf)
- [Your CLAUDE.md Is Too Long: What to Cut So Claude Code Follows It -- DEV Community](https://dev.to/promptmaster/your-claudemd-is-too-long-what-to-cut-so-claude-code-follows-it-5713)

---

## 3. 核心解法：Memory 做索引，Skill 存规则

既然 Memory 是稀缺的常驻资源，解决思路就一句话：**Memory 只做索引，具体的规则和 SOP 全部交给 Skill**。

**Memory 负责什么**：只记录「这个项目有哪些 Skill、每个 Skill 是干嘛的、什么时候该调用某个 Skill」。它是一张**索引卡片**，告诉 AI「这个任务该读哪个 Skill」。核心是 signal-dense（信号密集）——每一行都要值回它占用的上下文。

**Skill 负责什么**：具体的规则、SOP、操作手册、检查清单。比如数据库迁移流程、发布 checklist、代码审查规范、某种框架的 API 用法。这些内容只在触发时才加载，不挤占常驻上下文。

**为什么这么分是成立的**：因为 Skill 天然支持 progressive disclosure（渐进式披露）。Skill 的 name 和 description 常驻（约 100 token），正文按需加载。规则放进 Skill，等于让「该读的规则」在需要时才进上下文，平时不占空间。

**判断口诀**：如果一条内容「AI 每轮都必须知道」→ 放 Memory；如果「只有某种任务才需要」→ 放 Skill；如果是「多步流程 / 操作手册」→ 一定放 Skill。

**参考资料：**

- [Steering Claude Code: skills, hooks, rules, subagents and more -- Claude](https://claude.com/de/blog/steering-claude-code-skills-hooks-rules-subagents-and-more) ⭐值得阅读
- [Equipping agents for the real world with Agent Skills -- Anthropic](https://www.anthropic.com/research/equipping-agents-for-the-real-world-with-agent-skills) ⭐值得阅读
- [How to remember: CLAUDE.md vs skills -- Claude Docs](https://code.claude.com/docs/en/features-overview)

---

## 4. Skill 的加载机制：为什么规则不会挤掉

有人会问：「把规则挪进 Skill，万一 AI 想不起来读呢？」答案是：Skill 有自动触发与按需加载机制，它不怕「被挤掉」，因为它在会话里占的坑极小。

**Skill 的三级加载**（progressive disclosure）：

| 层级 | 何时加载 | token 成本 | 内容 |
|---|---|---|---|
| Level 1：元数据 | 启动时 | 约 100 token / 个 | name + description |
| Level 2：指令 | Skill 被触发时 | <5k token | SKILL.md 正文 |
| Level 3：资源 | 执行需要时 | 不设限 | references / scripts 等 |

**为什么这能解决「规则被挤掉」**：Skill 的正文平时根本不加载，所以不存在「写太多被截断」的问题。真正占上下文的是 Level 1 的 name + description（每个约 100 token），而这部分恰恰是**最精简的索引**——它只告诉你「有这个技能、什么时候用它」。

**怎么触发**：Skill 可以被路径命令显式调用（如 `/code-review`），也可以由任务自动匹配。一旦触发，AI 会把完整 SKILL.md 读进上下文，临时获得全部规则。

**参考资料：**

- [Agent Skills -- Claude API Docs](https://console.anthropic.com/docs/en/agents-and-tools/agent-skills/overview) ⭐值得阅读
- [Skill authoring best practices -- Claude Platform Docs](https://platform.claude.com/docs/en/agents-and-tools/agent-skills/best-practices)
- [How Claude Code works -- Claude Code Docs](https://code.claude.com/docs/en/how-claude-code-works)

---

## 5. 可运行的判断函数：这行规则该进 Memory 还是 Skill

下面这段代码把「该进 Memory 还是 Skill」的判断规范化成 4 个问题。运行不需要任何外部依赖，复制即跑：

```python
def classify_rule_entry(
    always_needed: bool,   # 这条内容 AI 是否每轮都必须知道
    is_workflow: bool,     # 是否属于多步流程 / 操作手册
    task_specific: bool,   # 是否只有某个特定任务才需要
) -> str:
    """判断一条规则应该放在 Memory（索引）还是 Skill（正文）.

    参数:
        always_needed: 内容是否每次会话都必须常驻（如项目约定、命名规范）
        is_workflow: 是否属于多步流程、SOP、操作手册
        task_specific: 是否只在某个特定任务场景下才需要
    返回:
        推荐存放位置: memory / skill
    """
    # 1) 多步流程 / 操作手册 -> 一定放 Skill，避免挤占常驻上下文
    if is_workflow:
        return "skill（Skill）: 流程/手册按需加载，不挤占常驻上下文"

    # 2) 每轮必须知道 -> 放 Memory，作为常驻索引
    if always_needed:
        return "memory（Memory）: 常驻索引，确保每次会话都加载"

    # 3) 只在特定任务需要 -> 放 Skill，用 description 做自动触发
    if task_specific:
        return "skill（Skill）: 任务触发时加载，用 description 匹配"

    # 4) 都不满足 -> 默认放 Skill，最保守
    return "skill（Skill）: 默认按需加载，避免冗余"


# 示例：判断「数据库迁移流程」该放哪
if __name__ == "__main__":
    print(classify_rule_entry(
        always_needed=False,  # 迁移流程不是每轮都要
        is_workflow=True,     # 它是多步操作手册
        task_specific=False,
    ))
    # 输出: skill（Skill）: 流程/手册按需加载，不挤占常驻上下文
```

这段代码把判断逻辑浓缩成一条可执行的决策路径。核心原则：**能进 Skill 的尽量进 Skill，Memory 只留必须常驻的索引**。

---

## 6. 对照表：症状 → 原因 → 解法

| 症状 | 原因 | 解法 |
|---|---|---|
| 规则写了很多，AI 执行任务时却总漏掉某条 | 规则排在 Memory 200 行 / 25KB 之外，会话里根本没加载 | 把非核心规则挪进 Skill，Memory 只留索引 |
| AI 每次执行任务都慢、token 消耗高 | 大量无关规则每次都读进来，占满常驻上下文 | 精简 Memory 到 200 行内，规则改由 Skill 按需加载 |
| 几条工作流规则互相矛盾，AI 摇摆不定 | 不同主题规则全塞进同一份 Memory，相互干扰 | 按主题拆成不同 Skill，各自触发、互不干扰 |
| 想加一条新规则，却不知道放哪 | 缺乏「索引 vs 正文」的划分标准 | 用上面的判断函数：多步流程进 Skill，常驻约定进 Memory |
| 项目里 Skill 一大堆，AI 却想不起来用 | Skill 的 description 写得太泛，无法自动触发 | 强化 Skill 的 description 为「when to use」触发场景 |

---

## 7. 结论：该用 / 不该用的判据

**什么时候该用**：规则是「每轮都必须知道的约定」（命名规范、构建命令、基础项目结构）→ 放 Memory（CLAUDE.md）；规则是「多步流程、SOP、操作手册」→ 放 Skill（按需加载）。判断标准就一条——**这条规则 AI 是不是每轮都要看**，是就进 Memory，否就进 Skill。

**什么时候不该用**：不要把所有规则都塞进 Memory，尤其不要塞多步流程和长手册；不要让 Memory 超过 200 行 / 25KB；不要用大量内容撑满上下文窗口，那只会降低规则的遵守度。规则一多，该做的是拆分到 Skill，而不是继续堆进 Memory。

---

本专栏《AI Agent 工具专栏》从工具调用、记忆管理、Skill 路由一路讲到规则治理与上下文上限，每篇都配可运行的代码与一张对照表，聚焦生产落地的真实取舍，每周更新一篇。想在 Agent 工程里少踩坑，可在专栏页订阅。

