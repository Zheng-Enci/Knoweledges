# 如何给 Agent 加一个 askQuestion 提问工具：从工具 Schema 到中断恢复的完整实现

> **核心结论**：给 Agent 加「向用户提问」的能力，本质是加一个**特殊工具**——当 Agent 调用它时，**执行不是「返回结果」，而是「暂停」（interrupt），把问题抛给用户，等用户回答后把答案当成工具结果（tool result）回填，再继续跑（resume）**。这就是 human-in-the-loop（人在回路）的核心机制。落地要解决四件事：**① 设计工具的 Schema（问题、选项、单选/多选、是否允许自定义输入）；② 实现「工具调用 → 中断 → 序列化状态 → 用户输入 → 恢复」的完整链路；③ 定好「什么时候该问」的规则（别问太泛、别问太频）；④ 处理超时和中断兜底**。做对了，Agent 从「瞎猜」变成「先确认再动手」，成功率会明显提升——因为很多失败不是能力不够，是**信息不足还硬猜**。

## 目录

- 1. 一句话结论
- 2. 为什么 Agent 需要「会提问」：从瞎猜到求证
- 3. 核心机制：工具调用即中断（Tool Call as Interrupt）
- 4. 工具 Schema 怎么设计：问题、选项、多选、自定义
- 5. 中断与恢复：暂停、序列化、resume 回填
- 6. 各框架怎么做：LangGraph、OpenAI Agents SDK、Agno
- 7. 提问设计规范：什么时候问、怎么问
- 8. 三种反模式：问太多、问太泛、问了不接
- 9. 完整可运行代码：一个 ask_question 工具 + 中断恢复循环
- 10. 对照表：症状 → 原因 → 解法
- 11. 判断收尾

## 1. 一句话结论

先建立一个直觉 🎭：**给 Agent 装提问工具，就像给新员工装一部「可以打电话问老板」的电话**——遇到拿不准的，打个电话问一句，比硬着头皮猜错强一万倍；但电话不能打太勤，否则老板会烦。

所以这件事的核心是三层：

- **工具层**：定义 `ask_user_question` 工具的 Schema（问什么、给什么选项）。
- **机制层**：工具调用不是返回数据，而是**中断执行、等用户回答、再恢复**。
- **策略层**：规定「只在关键决策点问」，别把每个细节都抛给用户。

一句话：**askQuestion 不是普通工具，它是「让 Agent 停下来问人」的开关——调用的瞬间，执行流从「自动」切到「等待」，答完再切回来。**

## 2. 为什么 Agent 需要「会提问」：从瞎猜到求证

先讲清楚「为什么要加这个工具」，不然容易做成摆设。

Agent 失败的一大原因是**信息不足还硬猜**：

- 用户说「帮我订张票」，但没说去哪、什么时间——Agent 如果不问，只能瞎猜城市和日期。
- 用户说「把这个函数优化一下」，但没说优化目标（速度？可读性？内存？）——不问就按自己的理解改，改完用户不满意。
- 涉及高危动作（删数据、发消息、下单）——不问就执行，出了事无法挽回。

加提问工具的价值：

- **把「未知」变成「已知」**：缺的信息直接问，而不是猜。
- **把「自作主张」变成「用户确认」**：关键决策让用户拍板。
- **把「一次做错重来」变成「一次问清做对」**：减少返工。

用类比 🎭：**这就像手术前的「知情同意」**——医生不问你「要不要切这里」「要不要保守治疗」就直接开刀，你敢躺上去吗？Agent 也一样，关键节点问一句，用户才敢把事交给它。

> 💡 我在本专栏《Agent 评测体系是什么》里讲过「高危动作必须人工确认」——askQuestion 正是实现这个「人工确认」最直接的工具。

## 3. 核心机制：工具调用即中断（Tool Call as Interrupt）

这是整个实现的关键认知：**askQuestion 和普通工具（读文件、调 API）的执行方式完全不同**。

| 对比项 | 普通工具 | askQuestion 工具 |
|--------|---------|-----------------|
| 调用后 | 执行逻辑，返回结果 | **暂停执行**，等外部输入 |
| 结果来源 | 程序内部产生 | **用户提供** |
| 耗时 | 毫秒级 | **可能几秒到几小时**（人要时间想） |
| 状态 | 无需保存 | **必须序列化保存**（等的时候可能关机） |

所以它不是一个「函数调用」，而是一个**中断（interrupt）**：

1. Agent 决定调用 `ask_user_question`。
2. 执行流**暂停**，把当前状态（消息历史、任务进度）存下来。
3. 问题抛到前端（弹窗 / 卡片）。
4. 用户回答。
5. 把答案包装成这次工具调用的**结果（tool result）**，回填给 Agent。
6. Agent **恢复（resume）**执行。

用类比 🎭：**这就像「游戏存档」**——打到关键节点，游戏暂停，你做了个选择（存档），游戏再从你选的分支继续。选完不是「游戏结束」，而是「从分叉点接着跑」。

## 4. 工具 Schema 怎么设计：问题、选项、多选、自定义

工具定义得好不好，直接决定用户体验。一个实用的 `ask_user_question` Schema 至少要包含：

```json
{
  "name": "ask_user_question",
  "description": "当信息不足或需要用户决策时，向用户提问。仅在关键节点使用。",
  "parameters": {
    "type": "object",
    "properties": {
      "question": { "type": "string", "description": "要问用户的问题" },
      "header": { "type": "string", "description": "简短标题（≤12 字）" },
      "options": {
        "type": "array",
        "description": "2-4 个明确选项，每个含 label 和 description",
        "items": {
          "type": "object",
          "properties": {
            "label": { "type": "string" },
            "description": { "type": "string" }
          }
        }
      },
      "multi_select": { "type": "boolean", "description": "是否允许多选" }
    },
    "required": ["question", "options"]
  }
}
```

四个设计要点：

- **question**：问题要具体，别问「你想怎么办」，要问「这两套方案选哪个」。
- **header**：一个短标签，前端可以做成选项卡，一眼看清问什么。
- **options**：**必须有明确选项**（2–4 个），每个选项带一句 description 说明后果——用户才好选。
- **multi_select**：有些问题是「选哪些功能」，允许多选；有些是「二选一」，单选。

> ⚠️ 关键：**别让选项是「是/否」这种模糊项**。好的选项是「A 方案（快但贵）/ B 方案（慢但省）」——用户一看就能判断，而不是要再问你「A 和 B 分别啥意思」。

参考资料：
- [User Feedback：ask_user 工具 -- Agno](https://docs.agno.com/tools/toolkits/others/user-feedback) ⭐值得阅读

## 5. 中断与恢复：暂停、序列化、resume 回填

Schema 定义好，接下来是机制实现。核心难点在于「暂停期间状态怎么保存」——用户可能要过很久才回答，中间进程可能重启。

完整链路分五步：

1. **触发中断**：Agent 产生一个 `ask_user_question` 的 tool call，识别到这是「需要人工」的工具，立即暂停。
2. **序列化状态**：把当前对话历史、任务进度、待回复的 tool_call_id 全部序列化（存内存 / 数据库 / 文件）。
3. **对外暴露问题**：把 question + options 推给前端。
4. **接收用户回答**：用户点选 / 输入。
5. **恢复执行**：把用户答案包装成对应 `tool_call_id` 的 tool result，重新调起 Agent，从暂停点继续。

关键细节：

- **tool_call_id 必须对上**：恢复时要把答案关联到「当初那个提问的调用」，否则 Agent 不知道这个结果属于哪次提问。
- **状态要可序列化**：LangGraph 用 `Command` 携带 resume 值恢复，OpenAI Agents SDK 用 `RunState` 序列化暂停的运行，都是为了「暂停后可恢复」。
- **幂等**：如果恢复失败重试，要保证不会重复执行前面的动作。

用类比 🎭：**这就像「在线问卷」**——你填到一半可以关掉，下次打开从上次的进度继续，因为你填的每一笔都存了档。中断恢复机制就是给 Agent 的「运行」装上这种存档能力。

参考资料：
- [Interrupts：Resuming interrupts -- LangChain](https://docs.langchain.com/oss/javascript/langgraph/interrupts) ⭐值得阅读
- [Human-in-the-loop -- OpenAI Agents SDK](https://openai.github.io/openai-agents-python/human_in_the_loop/) ⭐值得阅读

## 6. 各框架怎么做：LangGraph、OpenAI Agents SDK、Agno

不同框架的实现思路高度一致，看几个代表：

| 框架 | 机制 | 关键 API |
|------|------|---------|
| LangGraph | 图节点内 `interrupt()` 暂停，用 `Command` 携带 resume 值恢复 | `interrupt()` / `Command(resume=...)` |
| OpenAI Agents SDK | 工具声明需要审批，暂停运行，`RunState` 序列化后可恢复 | pending approvals / `RunState` |
| Agno | `UserFeedbackTools` 提供 `ask_user`，结构化问题 + 预定义选项，暂停后恢复 | `ask_user` |
| AgentScope | 抛出 `UserInterruptEvent` 暂停，传事件恢复 | `UserInterruptEvent` |

共同点：

- **都是「工具触发 + 中断 + 恢复」三段式**，没有花哨差异。
- **都强调状态可序列化**——因为等待时间不确定。
- **都支持结构化选项**——不是让用户自由输入，而是点选（降低回答成本）。

> 💡 你不需要从头造轮子：选一个支持 interrupts 的框架（LangGraph 最典型），定义好 ask 工具的 Schema，接上「暂停 + 恢复」就能用。

## 7. 提问设计规范：什么时候问、怎么问

工具实现完，最容易翻车的是「提问策略」——用不好，Agent 会变成「十万个为什么」。

**该问的场景**：

- **信息缺失**：完成任务的必要参数缺失（去哪、什么时间、什么目标）。
- **关键决策点**：两种方案都合理、需要用户拍板。
- **高危动作前**：删除、发送、支付、下单——执行前必须确认。

**不该问的场景**：

- **能自己推断的**：用户说「订最近的咖啡店」，就别问「最近的可以吗」。
- **无关紧要的细节**：格式化的颜色、无关变量命名——自己定，别烦用户。
- **同一件事的重复确认**：问过一次就别再问。

**怎么问**：

- **一次一问**：把多个问题拆成多次，别一次抛 5 个问题糊脸。
- **给推荐项**：把最可能的选择放第一个，标「推荐」。
- **选项要具体**：带后果说明，让用户「一看就能选」。

> ⚠️ 提问的本质是**成本转移**：你少猜一次 = 用户多点一次。所以只在「猜错的代价 > 打扰的成本」时才问。

## 8. 三种反模式：问太多、问太泛、问了不接

**反模式一：问太多（Over-asking）**

- 症状：每个小决定都问，「要用什么字体」「要保存到哪个目录」。
- 后果：用户被问烦，干脆不用了。
- 解药：定「必须问」的白名单（高危、信息缺失、关键决策），其余自己定。

**反模式二：问太泛（Vague Question）**

- 症状：问「你想怎么办」这种开放问题，用户不知道怎么答。
- 后果：用户回一句「你看着办」，等于没问。
- 解药：给具体选项 + 后果说明，让用户做选择题而不是问答题。

**反模式三：问了不接（Ask Without Resume）**

- 症状：工具实现只「弹窗」，用户答完答案没回填给 Agent，执行流断了。
- 后果：Agent 永远卡在等待，或重新从头开始。
- 解药：恢复链路必须接上——答案要包装成 tool result，绑定 tool_call_id 回填。

| 反模式 | 症状 | 后果 | 解药 |
|--------|------|------|------|
| 问太多 | 每个小决定都问 | 用户被烦跑 | 只问高危/缺失/关键决策 |
| 问太泛 | 「你想怎么办」开放问题 | 用户答「你看着办」 | 给具体选项 + 后果 |
| 问了不接 | 弹窗后答案没回填 | Agent 卡死/重跑 | 接上 tool result 回填 |

## 9. 完整可运行代码：一个 ask_question 工具 + 中断恢复循环

下面是一段**复制粘贴就能跑**的 Python 代码，实现完整的「提问 → 中断 → 恢复」闭环：Agent 遇到信息缺失时调用 `ask_user_question`，程序暂停并向用户提问，拿到答案后包装成 tool result 回填，Agent 继续执行。用预置输入模拟用户，无需第三方库。

```python
# ask_user_question 工具 + 中断恢复循环（最小实现）
class AskInterrupt(Exception):
    """自定义中断信号：Agent 调用提问工具时抛出，暂停执行"""
    def __init__(self, tool_call_id, question, options):
        self.tool_call_id = tool_call_id      # 本次提问的调用 ID
        self.question = question              # 要问的问题
        self.options = options                # 选项列表

# 工具定义：ask_user_question
ASK_TOOL = {
    "name": "ask_user_question",
    "description": "信息不足或需用户决策时提问，仅关键节点使用",
}

def ask_user_question(tool_call_id, question, options):
    """调用即中断：抛出信号，暂停 Agent 执行"""
    raise AskInterrupt(tool_call_id, question, options)

def run_agent(user_task, answers):
    """
    模拟 Agent 主循环：遇到信息缺失就提问，收到答案后继续。
    参数:
        user_task: 用户任务
        answers: 预置的用户回答（模拟交互）
    返回: 最终执行结果
    """
    history = []                              # 消息历史
    # 第一步：Agent 发现信息缺失，决定提问
    try:
        ask_user_question(                       # 触发中断
            tool_call_id="call_001",
            question="订票需要确认目的地和日期，请选择：",
            options=["北京→上海，明天", "北京→深圳，明天", "其他（自定义）"],
        )
    except AskInterrupt as it:                   # 捕获中断：暂停
        print(f"[中断] 向用户提问：{it.question}")
        for i, opt in enumerate(it.options, 1):
            print(f"  {i}. {opt}")
        answer = answers.get(it.tool_call_id)    # 获取用户回答
        # 关键：把答案包装成 tool result，绑定 tool_call_id 回填
        history.append({
            "role": "tool",
            "tool_call_id": it.tool_call_id,
            "content": answer,
        })
        print(f"[恢复] 收到用户回答：{answer}，继续执行")

    # 第二步：Agent 拿到答案，继续完成任务
    answer = history[0]["content"]
    return f"已根据你的选择「{answer}」完成订票"

if __name__ == "__main__":
    # 预置用户回答（真实场景来自前端交互）
    user_answers = {"call_001": "北京→上海，明天"}
    result = run_agent("帮我订张票", user_answers)
    print("[最终结果]", result)
```

**怎么读这段代码**：`AskInterrupt` 就是第 3 节的「中断信号」——调用 `ask_user_question` 不返回数据，而是抛异常暂停；`except AskInterrupt` 捕获后打印问题、拿用户答案，这正是第 5 节「对外暴露问题 → 接收回答」；最关键的一步是 `history.append({..., "tool_call_id": it.tool_call_id, "content": answer})`——把答案**绑定到原始 tool_call_id** 包装成 tool result，这是第 5 节强调的「必须对上 ID」；最后 Agent 从答案继续完成任务，对应「resume 恢复」。真实场景把 `raise/except` 换成框架的 `interrupt()` + `Command(resume=...)`，把 `print` 换成前端弹窗即可。

## 10. 对照表：症状 → 原因 → 解法

| 症状 | 原因 | 解法 |
|------|------|------|
| Agent 老是自己瞎猜、做完不对 | 缺 askQuestion 能力，信息不足硬猜 | 加提问工具，关键节点先问再做 |
| 加了提问工具，用户被烦跑 | 问太多、每个细节都问 | 只在高危/信息缺失/关键决策时问 |
| 用户回答「你看着办」 | 问题太泛、没给具体选项 | 给 2–4 个带后果的明确选项 |
| 用户答完，Agent 卡住不动 | 答案没回填、恢复链路断了 | 答案绑定 tool_call_id 包装成 tool result |
| 暂停后进程重启，任务丢了 | 状态没序列化 | 暂停时序列化对话与任务状态 |
| 危险操作没确认就执行了 | 高危动作没强制人工确认 | 高危工具强制走 ask 中断 |

## 11. 判断收尾

**什么时候该加 askQuestion 工具**：你的 Agent 会处理**信息经常缺失**（用户描述不全）、或涉及**高危动作**（删除/支付/发送）、或遇到**多种合理方案需用户拍板**的任务——这时加提问工具能显著提升成功率与信任感。**什么时候不必加**：任务边界清晰、信息每次都给全、且无高危操作（比如固定的数据格式转换）——这时加提问反而拖慢流程。判断标准只有一条：**「猜错的代价」是否大于「打扰用户一次的成本」**——大于，就值得问；不大于，就让 Agent 自己决定。

本专栏《AI-Agent 工具》从 Agent 记忆、上下文、工具调用一路讲到架构、评测与人机交互，每篇配可直接运行的代码，持续更新。想在做 Agent 产品时少踩坑，可在专栏页订阅。

参考资料（综合）：
- [Interrupts：Resuming interrupts -- LangChain](https://docs.langchain.com/oss/javascript/langgraph/interrupts) ⭐值得阅读
- [Human-in-the-loop -- OpenAI Agents SDK](https://openai.github.io/openai-agents-python/human_in_the_loop/) ⭐值得阅读
- [User Feedback：ask_user 工具 -- Agno](https://docs.agno.com/tools/toolkits/others/user-feedback) ⭐值得阅读
- [Human-in-the-loop -- LangChain](https://docs.langchain.com/oss/python/langchain/human-in-the-loop)
- [Interrupt the Agent -- AgentScope](https://docs.agentscope.io/versions/2.0.4/en/building-blocks/agent)
