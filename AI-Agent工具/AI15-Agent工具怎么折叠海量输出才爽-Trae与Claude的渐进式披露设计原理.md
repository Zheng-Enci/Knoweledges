# Agent 工具怎么折叠海量输出才「爽」：Trae、Claude Code 的渐进式披露设计原理

> **核心结论**：Trae、Claude Code、Cursor 这些 Agent 工具处理海量输出（工具调用、命令执行、思考过程）的核心不是「藏起来」，而是 **渐进式披露（Progressive Disclosure，渐进式披露）**——**默认只给你一层「干净可操作」的界面（最终答案 + 一句状态），把细节折叠进可展开的容器，你想看再点开**。它遵循一套三层信息架构：**第一层结论面**（答案 + 「思考了 8 秒」「正在读文件」这类状态）、**第二层证据面**（工具结果、引用、关键数据）、**第三层原始轨迹**（完整思考链、完整命令输出、每一步日志）。折叠的四种形态——时间折叠、工具折叠、思考折叠、结果折叠——分别对应四类噪音。做对这三件事（默认干净 + 按需深挖 + 实时反馈），用户才有「爽感」；做错任何一件，不是被淹没就是被憋死。

## 目录

- 1. 一句话结论
- 2. 为什么 Agent 输出会「淹死」用户
- 3. 核心原则：渐进式披露（Progressive Disclosure）
- 4. 分层信息架构：三层信息怎么分
- 5. 折叠的四种形态：时间 / 工具 / 思考 / 结果
- 6. 产品实践：Claude Code、Trae、Cursor 怎么做的
- 7. 「爽感」的三个来源：干净、深挖、反馈
- 8. 两种反模式：藏过头 vs 全暴露
- 9. 完整可运行代码：一个渐进式披露折叠组件
- 10. 对照表：症状 → 原因 → 解法
- 11. 判断收尾

## 1. 一句话结论

先建立一个直觉 🎭：**Agent 的输出来自「后厨」，用户只想看「摆盘好的菜」**——后厨切菜、颠勺、洗碗（工具调用、命令执行、思考过程）全塞给客人，客人只会没胃口；但客人想知道菜是怎么做的时，你也不能把后厨门焊死。

所以，Agent 输出的「爽感」来自三句话：

- **默认干净**：第一眼只给「答案 + 一句状态」，别让 3000 行日志糊脸。
- **按需深挖**：想看的细节折叠在可展开的容器里，点开就有。
- **实时反馈**：哪怕在折叠状态下，也要让用户看到「它在干活」（思考了 8 秒、正在读文件）。

一句话：**不是「隐藏输出」，而是「分层呈现」——把 90% 的噪音折叠，把 10% 的信号留下，剩下的按需展开。**

## 2. 为什么 Agent 输出会「淹死」用户

先理解问题有多严重。一个 Agent 跑一次任务，产生的输出大致有：

- **思考过程（reasoning / chain-of-thought）**：模型在回答前的推理 token，可能几千字。
- **工具调用（tool calls）**：每一步调了什么工具、传了什么参数、返回什么结果，几十甚至上百步。
- **命令执行（shell output）**：编译日志、测试输出、文件列表，动辄几百上千行。
- **中间结果**：读到的文件内容、搜索结果、API 返回的 JSON。

把这些全平铺到界面上，结果就是：**用户刷 10 屏都看不到最终答案**，而且真正重要的信息（「任务成功了没」「答案是什么」）被淹没在噪音里。

用类比 🎭：**这就像用「把整本菜谱 + 采购清单 + 洗碗记录」当餐厅菜单**——客人只想点菜，你却给了他一整个后厨的流水账。信息不是越多越好，**未加工的信息量 = 认知负担**。

> 💡 关键认知：Agent 的**过程信息**对调试者有用，对普通用户是噪音。折叠的本质是**区分「谁在什么场景下需要哪一层」**。

## 3. 核心原则：渐进式披露（Progressive Disclosure）

这是所有 Agent 工具输出设计的底层原则：

- **定义**：默认展示一个**干净、可操作的表面**，让用户按需钻取细节。
- **为什么叫「渐进」**：信息不是一次性全给，而是**从概要 → 证据 → 原始轨迹逐层展开**。
- **对 Agent 的适配**：Agent 会生成大量信息（推理轨迹、工具调用、中间结果、置信度、引用），**直接倒进 UI 就是认知过载**。

渐进式披露的收益：

- **第一眼清爽**：用户先看到「结果」，快速判断「这答案我满不满意」。
- **需要时可控**：想核对细节、想调试、想看证据，展开就行。
- **认知分级**：不同用户要不同深度——普通用户看结论，开发者看轨迹。

> ⚠️ 要注意它的代价：**用户可能永远不展开、错过关键信息**（比如某个工具失败了藏在折叠里），也可能因为**要反复点击才能找到细节而烦躁**。所以「折叠」必须配合「关键状态浮出」——这是第 7、8 节要解决的。

参考资料：
- [Progressive Disclosure UI Patterns -- Agentic Design](https://agentic-design.ai/patterns/ui-ux-patterns/progressive-disclosure-patterns) ⭐值得阅读
- [Agent UX & Transparency：Progressive Disclosure -- Max Gherman](https://www.max-gherman.dev/design/anatomy-of-ai-agent/agent-ux-and-transparency/) ⭐值得阅读

## 4. 分层信息架构：三层信息怎么分

渐进式披露落到结构上，就是**分层信息架构（Layered Information Architecture）**。Agent 输出按价值分三层：

| 层级 | 内容 | 默认状态 | 给谁看 |
|------|------|---------|--------|
| 第一层 · 结论面 | 最终答案 + 一句状态 | **始终可见** | 所有用户 |
| 第二层 · 证据面 | 工具结果、引用、关键数据点 | 折叠（一行摘要） | 想核对的人 |
| 第三层 · 原始轨迹 | 完整思考链、完整命令输出、每步日志 | 深度折叠 | 开发者 / 调试 |

- **第一层永远可见**：用户最关心的「做完了没、答案是什么」，不能被折叠。
- **第二层给「想确认的人」**：引用来源、工具返回的关键结果——一句话摘要 + 展开看全。
- **第三层给「想调试的人」**：完整 trace、原始日志——默认最深，需要才翻。

用类比 🎭：**这三层像「报纸的标题 → 导语 → 全文」**——标题扫一眼就知道讲什么（第一层），导语补充关键事实（第二层），想深究再翻全文（第三层）。没人会要求「报纸只印全文」。

## 5. 折叠的四种形态：时间 / 工具 / 思考 / 结果

具体到「怎么折叠」，行业里沉淀出四种装配形态，分别对付四类噪音：

**① 时间折叠（Thinking Duration）**

- 做法：把整段思考过程压成一句「**思考了 8 秒**」，点开才看完整推理。
- 这是 Claude Code 的经典做法——「Thought for 12s」只显示时长，不显示内容。
- 适用：推理模型的思考链太长，但对结果判断没那么重要时。

**② 工具折叠（Tool Call Accordion）**

- 做法：每次工具调用收成一行「**已读取 config.py**」「**运行 pytest（3 个失败）**」，点开看参数和完整结果。
- 运行中显示「**Using Read...**」这类状态指示，完成后折叠成一行摘要。
- 适用：工具调用步数多、每步输出冗长时。
- 工具调用本身的完整链路我在[Agent 如何进行工具调用：从一次 Function Calling 到生产级工具编排的完整链路](https://juejin.cn/post/7702408998457409562)里讲过，本文关注的是它「在界面上怎么被折叠成一行」。

**③ 思考折叠（Chain-of-Thought Collapse）**

- 做法：把推理步骤收进一个可折叠的「思考」手风琴（accordion），默认收起。
- assistant-ui 的 `ChainOfThought` 组件就是干这个的——分组展示推理步骤与工具调用。
- 适用：需要「可见但不打扰」地呈现推理过程。

**④ 结果折叠（Output Truncation）**

- 做法：长输出（命令日志、文件内容）默认只显示前 N 行 + 「展开全部（共 1200 行）」。
- 适用：单次输出几千行、用户 99% 只看前几行时。

| 折叠形态 | 折叠对象 | 折叠后可见 | 展开触发 |
|---------|---------|-----------|---------|
| 时间折叠 | 整段思考 | 「思考了 8 秒」 | 点击展开 |
| 工具折叠 | 单次工具调用 | 一行动作摘要 | 点击展开 |
| 思考折叠 | 推理步骤链 | 「思考」标题 | 点击展开 |
| 结果折叠 | 超长输出 | 前 N 行 + 行数 | 点击展开全部 |

参考资料：
- [ChainOfThought 组件 -- assistant-ui](https://www.assistant-ui.com/docs/primitives/chain-of-thought) ⭐值得阅读

## 6. 产品实践：Claude Code、Trae、Cursor 怎么做的

看几个真实产品的做法，能更直观理解「分层 + 折叠」。

**Claude Code / VS Code 插件**：

- 思考块默认只显示一个标签，如「**Thought for 12s**」，点开才看内容——典型的「时间折叠」。
- 支持 **streaming thinking**：思考以 `thinking_delta` 流式推过来，界面实时滚动但不刷屏。
- 工具调用也流式，且用 `in_tool` 状态标记，运行中显示「Using Read...」。

**Cursor / Trae 类 IDE Agent**：

- 每个工具调用是一张**可折叠卡片**：默认一行「已编辑 xxx.ts」，展开看 diff。
- 「思考中 / 正在生成」用动效 + 进度提示，让用户知道「它在干活」而不是卡死。
- 命令执行结果默认截断，点「查看全部输出」才展开完整日志。

**通用模式（几乎所有产品都在用）**：

- 「摘要先行」：先给结论，再给过程。
- 「失败优先」：工具报错、验证失败这类关键信息**不折叠、直接浮出**。
- 「状态常驻」：即使全折叠，也保留一个「正在做什么」的状态条。

> 💡 观察它们的共同点：**折叠的是「过程细节」，不折叠的是「结果」和「异常」**。这是所有设计的分界线。

参考资料：
- [Stream responses in real-time -- Claude Code Docs](https://code.claude.com/docs/en/agent-sdk/streaming-output) ⭐值得阅读
- [Thinking：Streaming thinking -- Claude Platform Docs](https://platform.claude.com/docs/en/build-with-claude/thinking)

## 7. 「爽感」的三个来源：干净、深挖、反馈

用户说的「查看爽感」，拆开其实就三件事，缺一件就翻车：

**① 干净：默认别糊脸**

- 第一屏必须是「结果 + 一句状态」，不要一上来就是几千行日志。
- 判断标准：用户**不滚动屏幕**就能知道「任务成没成、答案是什么」。

**② 深挖：想看的都点得到**

- 折叠不是「删掉」，是「收起来」——点开必须能看到完整内容。
- 判断标准：用户想核对时，**一次点击就能拿到**，不用翻聊天记录找。

**③ 反馈：折叠状态也要「活着」**

- 哪怕思考过程全折叠，也要有「思考了 8 秒」「正在运行测试」这类**实时状态**。
- 判断标准：用户**不会因为界面「没动静」而怀疑卡死**。

用类比 🎭：**这就像「外卖 App」**——第一眼看「已送达 + 预计时间」（干净），点开能看「骑手轨迹」（深挖），配送中地图上的小车一直在动（反馈）。三者齐了才叫「爽」。

> ⚠️ 很多工具翻车在第三点：折叠做得漂亮，但没有任何「正在干活」的反馈，用户盯着一个静止界面猜「是不是卡了」——体验反而更差。

## 8. 两种反模式：藏过头 vs 全暴露

折叠设计最常见的两种翻车方式，正好是两个极端：

**反模式一：藏过头（Over-collapse）**

- 症状：把「失败」「异常」「关键证据」都折叠了，用户永远不知道工具报错了。
- 后果：用户以为任务成功，实际 Agent 早就失败了——比不折叠还糟。
- 解药：**「失败优先浮出」**——错误、验证不通过、置信度低，这些**不折叠，直接顶到最上层**。

**反模式二：全暴露（Over-expose）**

- 症状：不加任何折叠，把所有思考、工具调用、命令输出平铺。
- 后果：用户刷 10 屏看不到答案，认知过载，直接放弃。
- 解药：**默认收敛到第一层**，其余折叠。

| 反模式 | 症状 | 后果 | 解药 |
|--------|------|------|------|
| 藏过头 | 失败/证据也被折叠 | 用户误以为成功 | 失败优先浮出，关键异常不折叠 |
| 全暴露 | 所有过程平铺 | 认知过载看不到答案 | 默认收敛到第一层结论 |

> 💡 一句话划界：**折叠「过程」，暴露「结果」和「异常」**——这条线画对了，两个反模式都能避开。

## 9. 完整可运行代码：一个渐进式披露折叠组件

下面是一段**复制粘贴就能跑**的完整 HTML，实现一个「渐进式披露」的 Agent 输出组件：工具调用卡片默认折叠成一行摘要、点击展开看详情、失败项默认高亮浮出、并带一个「思考中」的实时状态。保存为 `agent-output.html` 浏览器打开即可。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>渐进式披露：Agent 输出折叠组件</title>
<style>
  body { font-family: sans-serif; max-width: 640px; margin: 40px auto; padding: 0 16px; }
  /* 第一层：结论面（始终可见） */
  .answer { background: #f0fdf4; border-left: 4px solid #22c55e; padding: 12px 16px; border-radius: 8px; }
  /* 状态条：折叠状态下也显示"正在干活"的反馈 */
  .status { color: #666; font-size: 14px; margin: 12px 0; }
  .dot { display: inline-block; width: 8px; height: 8px; border-radius: 50%;
         background: #22c55e; margin-right: 6px; animation: blink 1s infinite; }
  @keyframes blink { 50% { opacity: 0.2; } }
  /* 第二/三层：可折叠的工具调用卡片 */
  .tool { border: 1px solid #e5e7eb; border-radius: 8px; margin: 8px 0; overflow: hidden; }
  .tool summary { cursor: pointer; padding: 10px 14px; background: #fafafa;
                  font-size: 14px; list-style: none; }
  .tool summary::-webkit-details-marker { display: none; }   /* 隐藏默认三角 */
  .tool summary::before { content: "▸ "; color: #999; }
  .tool[open] summary::before { content: "▾ "; }
  .tool .detail { padding: 12px 14px; font-size: 13px; color: #444;
                  background: #fff; border-top: 1px solid #f0f0f0; white-space: pre-wrap; }
  /* 失败优先：错误卡片默认高亮、且默认展开 */
  .tool.error { border-color: #ef4444; }
  .tool.error summary { background: #fef2f2; color: #b91c1c; font-weight: bold; }
</style>
</head>
<body>
  <!-- 第一层：结论面，用户第一眼就看到 -->
  <div class="answer">✅ 任务完成：已修复 config.py 中的端口配置，测试全部通过。</div>

  <!-- 实时反馈：折叠状态下也显示"在干活" -->
  <div class="status"><span class="dot"></span>Agent 已结束，共执行 3 个工具调用</div>

  <!-- 第二层：工具调用折叠卡片（默认收起，点开看详情） -->
  <details class="tool">
    <summary>已读取 config.py（128 行）</summary>
    <div class="detail">port = 8080
host = "0.0.0.0"
# ...（这里放完整文件内容）</div>
  </details>

  <details class="tool">
    <summary>已编辑 config.py：8080 → 9090</summary>
    <div class="detail">- port = 8080
+ port = 9090</div>
  </details>

  <!-- 失败优先：错误项默认展开并高亮，绝不藏在折叠里 -->
  <details class="tool error" open>
    <summary>⚠ 测试曾有 1 个失败（已修复）</summary>
    <div class="detail">FAILED test_server.py::test_port
AssertionError: expected 9090, got 8080
（修复后重新运行：3 passed）</div>
  </details>
</body>
</html>
```

**怎么读这段代码**：`.answer` 是第一层「结论面」，永远可见；`.status` 状态条是「实时反馈」，即使工具详情全折叠，用户也知道「执行了 3 个工具」；每个 `<details class="tool">` 是第二层「证据面」，用原生 `<details>/<summary>` 实现折叠，`summary::before` 用 ▸/▾ 做展开指示（替代默认三角）；最关键的 `.tool.error` 加了 `open` 属性——**失败项默认展开 + 红色高亮**，正是第 8 节「失败优先浮出」的落地。这段代码把「分层 + 折叠 + 反馈 + 失败优先」四个要点全占了。

## 10. 对照表：症状 → 原因 → 解法

| 症状 | 原因 | 解法 |
|------|------|------|
| 用户刷很多屏看不到答案 | 所有过程平铺，无折叠 | 默认收敛到第一层结论面 |
| 折叠后用户以为任务成功，其实失败了 | 失败信息也被折叠 | 失败优先浮出，异常默认展开 |
| 用户抱怨「要反复点击才找到细节」 | 折叠层级太深、入口不明显 | 关键细节放第二层，一次点击可达 |
| 界面静止，用户以为卡死 | 折叠后没有实时状态反馈 | 保留「思考中 / 运行中」状态条 |
| 思考链太长、刷屏 | 推理 token 全量展示 | 时间折叠：「思考了 8 秒」 |
| 命令输出几千行 | 长输出未截断 | 结果折叠：前 N 行 + 展开全部 |

## 11. 判断收尾

**什么时候该做一套完整的渐进式披露**：你做的 Agent 工具会产出**多步工具调用 + 长思考链 + 大量命令输出**，且用户既要看结果、偶尔又要核对过程——这时三层架构 + 四种折叠是刚需，否则体验必然翻车。**什么时候可以简化**：Agent 只做单步、输出很短，或用户就是开发者、全程想看完整 trace——这时直接平铺反而更合适，强行折叠是过度设计。判断标准只有一条：**用户是不是「只看结果、偶尔看过程」**——是，就该分层折叠；如果是「全程都要看过程」，那折叠反而是负担。

本专栏《AI-Agent 工具》从 Agent 记忆、工具调用、架构选型讲到自动化调度、评测与交互设计，每篇配可直接运行的前端/后端代码，持续更新。想在做 Agent 产品时少踩坑，可在专栏页订阅。

参考资料（综合）：
- [Progressive Disclosure UI Patterns -- Agentic Design](https://agentic-design.ai/patterns/ui-ux-patterns/progressive-disclosure-patterns) ⭐值得阅读
- [Agent UX & Transparency：Progressive Disclosure -- Max Gherman](https://www.max-gherman.dev/design/anatomy-of-ai-agent/agent-ux-and-transparency/) ⭐值得阅读
- [ChainOfThought 组件 -- assistant-ui](https://www.assistant-ui.com/docs/primitives/chain-of-thought) ⭐值得阅读
- [Stream responses in real-time -- Claude Code Docs](https://code.claude.com/docs/en/agent-sdk/streaming-output) ⭐值得阅读
- [Reasoning Glimpse（Chain-of-Thought Visualization） -- Agentic UX Patterns](https://agenticuxpatterns.com/patterns/reasoning-glimpse)
