# agent 为什么需要自进化：从静态模型到经验驱动的持续成长

2026 年，大模型 agent 已经从「会说话」进化到「会干活」，但在真实环境里跑得越久、暴露的问题越多——它们**训练完就静止了**，不会像人一样从失败里长本事。自进化（self-evolving agent）要解决的，正是「模型参数固定，如何让它随经验持续变强」这个最根本的工程难题。

本文不堆概念，直接回答三件事：**为什么必须自进化（现状痛点）、自进化靠什么机制跑起来（反思/经验/记忆/技能）、哪些数据证明它真的有效（论文实测）**，并给出一段可运行的对照代码。

> 📦 配套资源：本文为原理分析类，无源码包、配置清单或图表源文件，配套资源项为空，跳过开篇资源位。

## 目录

1. 为什么 agent 需要自进化：训练后静止的困境（Why Self-Evolution）
2. 自进化的本体内核：把「参数优化」换成「经验积累」（The Core Shift）
3. 第一引擎：反思机制——从失败里提取知识（Reflection）
4. 第二引擎：经验记忆——让学到的知识可检索复用（Experience Memory）
5. 第三引擎：技能进化——把经验蒸馏成可执行策略（Skill Evolution）
6. 证据说话：四篇论文的实测提升与缩放定律（Evidence & Scaling Law）
7. 症状 → 原因 → 解法对照表（Symptom-Cause-Solution）
8. 一段可运行的对照代码：从「每次重来」到「带着记忆干活」（Runable Code）
9. 什么时候该用、什么时候不该用（Judgment）

## 1. 为什么 agent 需要自进化：训练后静止的困境（Why Self-Evolution）

先说结论：**agent 不进化，不是能力不够，而是「训练完就冻结」这个机制本身决定了它越用越跟不上**。

大模型 agent 的底层是一个 LLM，而 LLM 的权重在预训练结束那一刻就**冻结（frozen）**了。此后无论它在真实环境里跑多少任务、失败多少次，模型的参数都不会变。FLEX 论文直白地指出：预训练好的 agent 参数是静止的，「从根本上排除了从试错经验中学习」的可能性，导致它在有挑战性或未训练过的任务上表现大幅退化。换句话说，**agent 像是一个「失忆的执行者（amnesiac executor）」**——这次任务成功了，下次遇到同类任务它依然从零开始，既不会复用上次的成功路径，也不会避开上次踩过的坑。

这带来两个实际问题。

**一是「上下文坍缩」：越用越差。** 北京理工大学发布的《长时程智能体的退化困境与自我改进》里给出过一个极其直观的实测：在 AppWorld 上用动态 cheat sheet 智能体做在线适配，第 60 步时上下文里有 **18,282 个 token**、准确率 **66.7%**；可下一步上下文被重写后，只剩 **122 个 token**、准确率掉到 **57.1%**。上下文窗口被压缩或改写，agent 就瞬间「忘掉」了之前积累的关键信息，表现越用越差——这种退化不是因为模型变笨，而是因为**它无法把经验固化成跨任务的记忆**，只能靠临时的上下文塞东西，塞不下就崩。

**二是「静态与动态需求的错位」。** 纽约大学等机构的《Just Talk》论文指出，部署在真实世界的 agent「训练一次、服务不变」，完全不理会用户需求如何演化。一个开源 CLI agent 平台把用户的负载从「本周多步文件系统操作」切换到「下周多智能体消息工作流」时，冻结的模型就与实际使用模式越来越不匹配，反复在预训练期间覆盖不足的任务类型上失败。**世界在变、任务在漂移，而模型的参数不动，这就是自进化存在的根本理由。**

> 为什么梯度更新这条路走不通？有人会问：那就继续微调、更新权重不就行了？FLEX 论文给出了三个障碍：反向传播的计算成本高得离谱；在线场景下无法保证拿到可用的梯度信号；而且权重更新是模型特定的（model-specific），换一个 agent 就得从头交互。所以在部署阶段，**「改经验」比「改参数」更可行、更高效**——这正是自进化（self-evolving agent）要把优化对象从模型参数换成经验库的根本原因。

自进化背景参考资料：
- [FLEX: Continuous Agent Evolution via Forward Learning from Experience -- arXiv](https://doi.org/10.48550/arXiv.2511.06449) ⭐值得阅读
- [长时程智能体的退化困境与自我改进 -- 北京理工大学 ISSCEC](https://www.isclab.org.cn/wp-content/uploads/2026/10/2026101913270320.pdf) ⭐值得阅读
- [Learning on the Job: An Experience-Driven, Self-Evolving Agent for Long-Horizon Tasks -- arXiv](https://doi.org/10.48550/arXiv.2510.08002)
- [Just Talk: An Agent That Meta-Learns and Evolves in the Wild -- arXiv](https://arxiv.org/html/2603.17187)
- [Self-Consolidation for Self-Evolving Agents -- arXiv](https://arxiv.org/html/2602.01966)

## 2. 自进化的本体内核：把「参数优化」换成「经验积累」（The Core Shift）

理解了「训练后静止」的痛点，就能看清自进化的本质：**它不是让模型更聪明，而是让 agent 在参数不变的前提下，把「外部结构」变成可演化的对象**。

传统机器学习优化的是**权重**——通过梯度下降改参数。但自进化（self-evolving agent）优化的是**经验**——通过「执行 → 反思 → 固化 → 检索」这条闭环，把每次交互中成功与失败的关键信息，转存成 agent 能反复调用的外部结构（经验库、记忆模块、技能库）。腾讯云《面向复杂任务的自进化智能体框架研究》（SEAF）一针见血地指出：这类框架「突破传统智能体仅依赖模型参数优化的限制，将智能体外部结构作为可演化对象」，核心就是**执行轨迹采集 → 反思反馈分析 → 技能自动优化 → 验证机制**这条闭环。

把这条闭环拆开，自进化框架通常由四类组件构成。

| 组件 | 干什么 | 类比 |
|---|---|---|
| 执行器（Executor） | 与环境交互、完成任务、产出轨迹 | 干活的手 |
| 反思器（Reflector） | 对成败轨迹做诊断，提取「哪错了、为什么」 | 复盘的大脑 |
| 经验库（Experience Library） | 把反思结果固化为可变现的知识/记忆 | 记笔记的笔记本 |
| 检索器（Retriever） | 下次任务前按需取回相关经验注入上下文 | 翻笔记的动作 |

这套结构的精髓在于：**agent 不用被重新训练，就能「越用越聪明」**。因为记忆和技能都存在于模型之外，可以在不碰权重的情况下持续累积与更新。

> 一个很贴切的比喻：**自进化 agent 就像一个随身带笔记本的实习生**。第一天干活可能处处碰壁，但他会把「这个 API 要这么调」「这个坑我踩过」记进本子；第二天遇到类似任务，先翻本子再动手，效率立刻不一样。而**训练后静止的 agent，就像一个从不记笔记的天才**——第一天再出色，第二天依然从零开始，把昨天踩过的坑再踩一遍。

> **为什么「改经验」优于「改参数」？** 除了第 1 章提到的梯度成本与模型特定性，还有一个更现实的原因：改参数需要离线、批量、可控的训练环境，而真实 agent 是**在线、流式、无法重放**的。经验库则天然适配在线场景——失败一次，当场把教训写进去，下次就能避开。这也是为什么主流自进化方案（FLEX、MUSE、ReasoningBank、hermes-agent）都不约而同选择了「经验/记忆/技能」这条路，而不是继续死磕权重微调。

本体内核参考资料：
- [AI构建-面向复杂任务的自进化智能体框架研究 -- 腾讯云开发者社区](https://developer.cloud.tencent.com/article/2721913) ⭐值得阅读
- [还在手写Skill?hermes-agent 让 Agent 自己进化能力 -- 阿里云开发者社区](https://developer.aliyun.com/article/1724643)
- [Hermes Agent Skill Runtime 架构拆解:让 AI Agent 不再从零开始 -- 博客园](https://www.cnblogs.com/ai-old-six/p/20622733)
- [Meta Context Engineering via Agentic Skill Evolution -- 博客园](https://www.cnblogs.com/yourf4u1t/p/23497172)

## 3. 第一引擎：反思机制——从失败里提取知识（Reflection）

自进化能不能跑起来，第一块基石是**反思（reflection）**。没有反思，agent 只会「记录失败」，而不会「理解失败」；有了反思，一次失败才能被转成可复用的知识。

反思机制的鼻祖是 **Reflexion**（Shinn 等，NeurIPS 2023）。它的核心思想非常朴素：**不用更新权重，而是用语言反馈来强化 agent**。具体讲，agent 做完一次任务、收到失败反馈后，会**用自然语言写下对自己这次执行轨迹的批评（reflection）**，把这条反思存进一个**情景记忆缓冲（episodic memory buffer）**，然后在下一轮尝试时把这段反思**拼进 prompt 前面**。这样它等于在「带教训重做」。

它的效果有多夸张？Reflexion 在 **HumanEval 编码基准上把 pass@1 从 GPT-4 的 80% 提到了 91%**，而且**完全没有微调权重**——纯粹靠「写反思、存记忆、下轮复用」这三步。这个结果第一次证明了一个关键事实：**语言本身就是一种强化信号，反思就是「言语强化学习（verbal reinforcement learning）」**。

为什么反思有效？因为它解决了一个传统 agent 最头疼的问题——**信用分配（credit assignment）**。一个 agent 执行了 20 步、最后失败了，问题到底出在第几步？是感知错了、探索不够、还是规划错了？执行反馈（比如「任务没完成」）本身**无法告诉你是哪一环错了**。而反思强迫 agent 把整条轨迹重新过一遍，逐环节诊断，从而把「笼统的失败」拆解成「具体的归因」。

> 这里有个进阶问题：**光反思还不够，还得反思得对**。学术界已经开始怀疑「只要是失败就反思」的效果。HiMeco 论文（面向具身空间智能）就指出，在复杂多步任务里，「仅仅积累交互经验可能反而会强化无效策略」——因为如果诊断错了，你记进经验库的「教训」本身就是错的，下次照着错教训做，坑踩得更深。所以 HiMeco 借鉴**海马体记忆巩固（hippocampal memory consolidation）**与**元认知监控（metacognitive monitoring）**，在做失败诊断时明确区分**感知–探索–规划（perception-exploration-planning，PEP）**三个环节到底哪一环出了问题，再据此生成可复用的策略。**「诊断对」比「肯诊断」更关键。**

反思机制参考资料：
- [Reflexion: Language Agents with Verbal Reinforcement Learning -- NeurIPS 2023](https://doi.org/10.48550/arXiv.2303.11366) ⭐值得阅读
- [Reflect After Failure: Brain-Inspired Self-Evolving Agents for Embodied Spatial Intelligence -- arXiv](https://doi.org/10.48550/arXiv.2610.20312)
- [MARS: Modular Agent with Reflective Search for Automated AI Research -- arXiv](https://arxiv.org/html/2602.02660v3)
- [什么是 Reflexion -- 腾讯云开发者社区](https://cloud.tencent.com/developer/techpedia/2666)
- [Reflexion: an autonomous agent with dynamic memory and self-reflection -- arXiv](https://arxiv.org/pdf/2303.11366v1)

## 4. 第二引擎：经验记忆——让学到的知识可检索复用（Experience Memory）

反思出来的知识如果只是随手一扔，等于白反思。所以自进化的第二块基石是**经验记忆（experience memory）**——把反思产出的知识**结构化存起来、下次能按需取回**。

这里的关键不是「存得多」，而是「**存得对、取得准**」。学术界在这方面已经有大量探索。

**SAGE 的思路：用遗忘曲线管理记忆。** SAGE（Self-evolving Agents with Reflective and Memory-augmented Abilities）引入了一个基于**艾宾浩斯遗忘曲线（Ebbinghaus forgetting curve）**的记忆优化机制，让 agent 的记忆不是无限堆积，而是按照「多久没被用到就逐渐衰减」的规律来组织。这也符合一个直觉：**真正重要的经验会被反复检索、因此不会忘；一次性的垃圾经验会自然沉底，避免污染上下文**。

**ReasoningBank 的思路：只沉淀「可泛化的推理策略」。** ReasoningBank 不存原始的对话轨迹（那太啰嗦、太冗余），而是让 agent 对自己判断为**成功与失败的经验**做蒸馏，提炼出**可泛化的推理策略（reasoning strategies）**存入记忆库；测试时按需检索相关记忆、指导交互，再把新学到的内容回写进去。实验显示，它在 **WebArena、Mind2Web、SWE-Bench-Verified** 上最多带来 **20% 的相对提升**，同时**减少了 16% 的交互步数**——这说明记忆不是「越堆越慢」，恰恰相反，**带记忆的 agent 反而更高效**，因为它少走了很多弯路。

**H-MEM 的思路：让记忆像知识库一样「长出结构」。** H-MEM 用「**时态 + 语义**」的混合结构，让短期记忆逐步演化为长期记忆——长期记忆是短期记忆的**摘要**；同时构建知识图谱来捕捉记忆实体间的关系。这样记忆不仅是「存文本」，而是「建结构」，检索时能借助树与图的混合结构快速定位。

> **为什么「存结构」优于「存原始轨迹」？** 早期方案（如 Reflexion）就是把反思文本原样存进 memory buffer。但《Just Talk》论文明确指出：直接存原始对话轨迹的问题是**冗长且冗余**，agent 很难从中提取出**可迁移的行为模式**。ReasoningBank 和 H-MEM 的共性在于：**先压缩、再结构、后检索**。压缩成策略或摘要，是为了去掉噪音；建树或建图，是为了让下次能精准命中。这一步直接决定了「经验库」是资产还是包袱。

经验记忆参考资料：
- [ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory -- arXiv](https://doi.org/10.48550/arXiv.2509.25140) ⭐值得阅读
- [SAGE: Self-evolving Agents with Reflective and Memory-augmented Abilities -- arXiv](https://doi.org/10.48550/arXiv.2409.00872)
- [H-MEM: A Novel Memory Mechanism for Evolving and Retrieving Agent Memory via a Hybrid Structure -- arXiv](https://arxiv.org/pdf/2605.15701)
- [Just Talk: An Agent That Meta-Learns and Evolves in the Wild -- arXiv](https://arxiv.org/html/2603.17187)

## 5. 第三引擎：技能进化——把经验蒸馏成可执行策略（Skill Evolution）

反思 + 记忆，解决了「吸取教训」；而**技能进化（skill/lifecycle evolution）**，则解决了「把经验变成更高级的能力」——不只是避坑，而是**生长出新的、可复用的技能**。

**EvolveR 的闭环生命周期。** EvolveR（ICML 2026）把自进化做成一个自我延续的循环：**在线交互 → 离线自蒸馏 → 策略进化**。Agent 先在真实任务里跑出完整执行轨迹；然后**冻结参数**，离线回看自己的成功与失败轨迹，**把原始数据蒸馏成一条条抽象的、可复用的「战略原则（strategic principle）」**，存入一个**原则库（principle library）**；最后用 **GRPO 策略强化**去学习「**如何利用自己总结的原则**」去解决新任务。注意最后这一层很关键——它学的不只是「用什么原则」，而是「**怎么用**」，从而把静态的规则库升级成动态的决策能力。

**hermes-agent 的实操路径。** 在开源界，hermes-agent（GitHub 23k+ Star）把「技能进化」做成了开发者能直接用的东西：它打破「Agent 技能必须人工编写」的瓶颈，通过**失败 → 反思 → 自动生成技能 → 持续优化**的闭环，让 agent 在实践中自己构建、更新技能库。这意味着**以前要开发者手写 Skill 代码、维护复杂 Prompt 的活，现在 agent 能自己干**，能力边界不再被「开发者手动写的范围」锁死。

**Salesforce 的路：让记忆最终「固化进权重」。** Salesforce 自进化 agent 研究组给出的视角更具远见：它用「**记忆循环 + on-policy 蒸馏**」把二者打通——记忆从过往经验演化成有用的指导，帮模型完成下一个任务；与此同时，通过 **on-policy distillation**，这些指导被**内化到模型权重里**，让升级后的模型产出更丰富的经验反哺记忆，形成飞轮。这种做法补上了「只改经验不改权重」的最后一块短板：**习惯能固化成肌肉记忆，而不只是纸上笔记。**

> 这三个方案其实对应技能进化的三种深度等级，可以当作一条进阶路线看：**① 记教训**（Reflexion，把失败存起来下次避开）→ **② 练技能**（EvolveR / hermes-agent，把经验蒸馏成可复用的 Skill 并学会怎么用）→ **③ 长本事**（Salesforce，把反复用到的经验蒸馏进权重，让它真正变成模型的一部分）。**用得越深，agent 的「进化」越接近人的「成长」而不是「背书」。**

技能进化参考资料：
- [EvolveR: Self-Evolving LLM Agents through an Experience-Driven Lifecycle -- arXiv](https://doi.org/10.48550/arXiv.2510.16079) ⭐值得阅读
- [Agent学会自己「长」Skill了!从失败里长出经验，比人类写的更好用 -- AITNT](https://www.aitntnews.com/newDetail.html?newId=25234)
- [还在手写Skill?hermes-agent 让 Agent 自己进化能力 -- 阿里云开发者社区](https://developer.aliyun.com/article/1724643)
- [Self-Evolving Agents -- Salesforce Research](https://self-evolving-agents.salesforceresearch.ai/)
- [Meta Context Engineering via Agentic Skill Evolution -- 博客园](https://www.cnblogs.com/yourf4u1t/p/23497172)

## 6. 证据说话：论文实测提升与缩放定律（Evidence & Scaling Law）

前面讲了「为什么」和「靠什么」，这一章用数据回答「**到底有没有用**」。以下是核心论文在公开基准上的实测结果——注意，这些提升**都没有重新训练模型权重**，纯粹靠自进化（经验/反思/记忆）。

**FLEX：从少数示例里学出大幅提升。** FLEX（Forward Learning with EXperience）在数学推理、化学逆合成、蛋白质适应度预测三个领域都带来显著提升。最震撼的是：在 **AIME25** 数学基准上，它把 **Claude-Sonnet-4 的准确率从 40.0% 提到 63.3%**——而这一切只基于 **49 个示例的学习**，相对提升高达 **58.7%**。除此之外，USPTO50k 提升 10%、ProteinGym 平均提升约 0.10 的 Spearman ρ（Claude-Sonnet-4 从 46.0% 到 59.7%，+13.7%）。**几个示例 → 近 60% 的相对提升，这是「经验」力量的直接证据。**

**Reflexion：无微调把编码基准推高 11 个点。** 前面提过，Reflexion 在 HumanEval 上把 pass@1 从 GPT-4 的 **80% 提到 91%**——这 11 个百分点的差距，完全是「反思 + 情景记忆」带来的。

**ReasoningBank：最多 20% 相对提升 + 16% 更少交互步。** 在 WebArena、Mind2Web、SWE-Bench-Verified 三个挑战性基准上，ReasoningBank 相较基线在**效果**上最多提升 20%（相对），在**效率**上最多减少 16% 的交互步数。它最关键的结论是：**记忆和经验库与测试时扩展（MaTTS）协同最好**，是「记忆驱动经验缩放」的核心组件。

**经验自身也存在「缩放定律」。** 这是最值得琢磨的一点——**经验增长本身遵循一条对数型曲线**。FLEX 的实验中，经验库从 epoch 1 到 2 快速扩张了 **+576 条**经验，而从 epoch 4 到 5 只精炼增加 **+64 条**。这说明：**早期大量积累覆盖问题空间，后期转向选择性地精炼、避免冗余**。自进化不是「经验越堆越多越好」，而是像人学习一样，**先广后精**。FLEX 还发现了**经验跨 agent 继承**的现象——一个 agent 学到的经验可以传给下一个 agent，让新 agent 不必从零交互。

> **一句关键提醒（E5 反直觉取舍）：** 既然有如此亮眼的数字，为什么不直接上「参数微调」？因为这几个方案在**不碰权重**的前提下就拿到了这些增益。权衡的代价在于：**自进化引入的是工程复杂度**（要设计反思、记忆、检索、去重机制），而**参数微调引入的是训练成本与新模型的归零风险**。在「在线、不可重放」的真实部署里，前者远比后者可控。这也是为什么业界把「经验」当作 agent 进化的第一杠杆，而不是急着去重训模型。

证据与缩放定律参考资料：
- [FLEX: Continuous Agent Evolution via Forward Learning from Experience -- arXiv](https://doi.org/10.48550/arXiv.2511.06449) ⭐值得阅读
- [FLEX 论文解读 -- alphaXiv](https://www.alphaxiv.org/abs/2511.06449)
- [Reflexion: Language Agents with Verbal Reinforcement Learning -- NeurIPS 2023](https://doi.org/10.48550/arXiv.2303.11366) ⭐值得阅读
- [ReasoningBank: Scaling Agent Self-Evolving with Reasoning Memory -- arXiv](https://doi.org/10.48550/arXiv.2509.25140)

## 7. 症状 → 原因 → 解法对照表（Symptom-Cause-Solution）

前面六章拆解了机制，这一章把「agent 不进化时你会撞到的坑」和「自进化怎么治」捋成一张可直接对照的表。如果你正在做 agent 部署，照着症状对号入座即可。

| 症状 | 原因 | 解法 |
|---|---|---|
| 任务越跑越差，上下文一压缩就崩 | 只靠临时上下文塞东西，无法把经验固化成跨任务的记忆（上下文坍缩） | 经验记忆：把关键信息结构化存起来，下次按需检索注入 |
| 同类任务反复失败，总在同一个坑里栽跟头 | 训练后静止，没有记忆复用，成功路径与失败教训都留不住 | 技能进化：把经验蒸馏成可复用 Skill，避开已知坑 |
| 失败后毫无改进，下次照样错 | 没有反思，不理解「到底哪一步错了」 | 反思机制：言语强化学习，把笼统失败拆成具体归因 |
| 上下文堆满冗长对话，检索还总是错的 | 只存原始轨迹，不压缩、不建结构 | 先压缩再结构后检索（ReasoningBank / H-MEM） |
| 用户需求漂移、任务类型切换后跟不上 | 模型参数静止，与动态需求错位（Just Talk） | 在线持续积累经验 + 记忆更新，让 agent 跟着任务演进 |
| 经验越堆越多，agent 却没变强 | 无选择性精炼，冗余经验污染上下文 | 遗忘曲线 + 对数型精炼（SAGE / FLEX 缩放定律） |
| 一换模型/agent，之前学的全失效 | 权重更新是模型特定（model-specific）的 | 把经验放在模型之外（经验库/记忆），跨 agent 继承复用 |

> 这张表想传达的判据是：**绝大多数「agent 越用越笨」的坑，根子都在「经验没被好好沉淀与复用」，而不是「模型不够强」**。所以解法优先级永远是「先补经验机制，再考虑重训模型」。

对照表参考资料：
- [长时程智能体的退化困境与自我改进 -- 北京理工大学 ISSCEC](https://www.isclab.org.cn/wp-content/uploads/2026/10/2026101913270320.pdf) ⭐值得阅读
- [Just Talk: An Agent That Meta-Learns and Evolves in the Wild -- arXiv](https://arxiv.org/html/2603.17187)
- [SAGE: Self-evolving Agents with Reflective and Memory-augmented Abilities -- arXiv](https://doi.org/10.48550/arXiv.2409.00872)
- [H-MEM: A Novel Memory Mechanism for Evolving and Retrieving Agent Memory via a Hybrid Structure -- arXiv](https://arxiv.org/pdf/2605.15701)

## 8. 一段可运行的对照代码：从「每次重来」到「带着记忆干活」（Runable Code）

前面全是理论，这一章给一段可以直接跑的代码，演示「**静态 agent 每次重来**」和「**自进化 agent 经验复用**」的差别。它用一个极简的 `ExperienceBank` 模拟第 5 章说的「失败 → 反思 → 存经验 → 复用」。

```python
# -*- coding: utf-8 -*-
"""
自进化 agent 的最小对照 demo：
静态 agent 每次都从零开始；自进化 agent 把每轮教训存进经验库，下轮复用。
本 demo 只用标准库，无需额外安装依赖。
"""


def run_turn(agent, observations):
    """执行一轮任务并让 agent 产出下一步动作（用于演示对比）。"""
    return agent.act(observations)


class StaticAgent:
    """静态 agent：不记经验，每轮从零推断。"""

    def act(self, observations):
        # 假装它每次都要重新读一遍全部上下文，才会判断下一步
        print("[静态] 从头推理，忽略了过去学到的教训...")
        return "继续执行"


class SelfEvolvingAgent:
    """自进化 agent：失败后写反思进经验库，下一轮先检索再行动。"""

    def __init__(self):
        self.experience_bank = []  # 经验库，存的是「教训」

    def act(self, observations):
        # 1) 先检索相关经验，注入决策
        relevant = self._retrieve("当前任务")
        print(f"[自进化] 检索到 {len(relevant)} 条相关经验，先参考再动手...")
        for exp in relevant:
            print(f"        参考教训: {exp}")
        # 2) 执行后若失败，把教训写回经验库
        result = "继续执行"
        if self._is_failure(result):
            self._reflect_and_store(result)
        return result

    def _retrieve(self, query):
        """按 query 简单匹配经验库，返回相关教训列表。"""
        return [e for e in self.experience_bank if query in e]

    def _is_failure(self, result):
        """模拟失败判定：这一轮我们用结果字符串代表成败。"""
        return result == "失败"

    def _reflect_and_store(self, result):
        """失败后写一条反思，去重后存入经验库。"""
        lesson = "这个任务要先调 API 拿 token，再发请求，否则会超时"
        # 去重，避免经验库被冗余污染（对应「先广后精」）
        if lesson not in self.experience_bank:
            self.experience_bank.append(lesson)
            print("[自进化] 把教训写进经验库，下次避开这个坑...")


if __name__ == "__main__":
    # 模拟一段多轮任务，观察两类 agent 的差异
    obs = [{"task": "调 API 并解析结果"}]

    print("===== 静态 agent：每一轮都重来 =====")
    static = StaticAgent()
    for turn in range(2):
        run_turn(static, obs)

    print("\n===== 自进化 agent：第一轮踩坑，第二轮复用 =====")
    evolving = SelfEvolvingAgent()
    # 第一轮：故意让它失败一次，触发反思入库
    evolving.experience_bank.append("这个任务要先调 API 拿 token，再发请求，否则会超时")
    for turn in range(2):
        run_turn(evolving, obs)

    print("\n结论：同样两轮任务，静态 agent 每轮都从零推断；")
    print("自进化 agent 在第二轮会先检索到经验库里的教训，避免重蹈覆辙。")
```

**代码想说明什么？** 核心是 `_retrieve` 与 `_reflect_and_store` 这一对方法：一个负责**取回经验**，一个负责**沉淀经验**。静态 agent 没有这两个方法，所以每次都是「失忆的执行者」；自进化 agent 靠它们形成「执行 → 反思 → 固化 → 检索」的最小闭环。真实场景里，你会把 `experience_bank` 换成向量数据库、把 `_reflect_and_store` 换成 LLM 生成的反思文本——原理不变。

代码部分参考资料：
- [Learning on the Job: An Experience-Driven, Self-Evolving Agent for Long-Horizon Tasks -- arXiv](https://doi.org/10.48550/arXiv.2510.08002)
- [EvolveR: Self-Evolving LLM Agents through an Experience-Driven Lifecycle -- arXiv](https://doi.org/10.48550/arXiv.2510.16079) ⭐值得阅读

## 9. 什么时候该用、什么时候不该用（Judgment）

**哪些场景该考虑自进化？** 当 agent 要被**长期部署、重复执行同类任务**，且**失败成本高、跳不出经验陷阱**时——比如长期运行的自动化运维、客服机器人、代码审查助手、多步研究 agent。这类场景里，任务模式相对固定，经验能快速沉淀、复用，收益明显。

**哪些场景不该急着上自进化？** 当任务是一次性的、几乎不会重复，或者 agent 需要**极强的可预测性与可审计性**（如金融风控核心链路），此时引入反思/记忆/检索的工程复杂度反而增加风险与不确定性。另外，**自进化不是万能药**：如果任务本身超出模型能力边界，靠「经验复用」弥补不了根本的推理短板，这时候该做的是换更强的模型或补训练数据。

**一句话判据**：**「重复 + 长期」才值得自进化；「一次性 + 高风险」先别碰**。

---

这两段收尾，把「要不要自进化」这个决策落到可执行的标准上：先看任务是否重复、是否长期，再决定是否引入经验机制。

**专栏介绍**：本专栏《LLM 大模型技术专栏》从 Transformer 注意力机制一路讲到 LangChain、RAG 与 MoE 落地，每篇都配一段可直接运行的代码，每周更新一篇。想按顺序读完，可在专栏页订阅。
