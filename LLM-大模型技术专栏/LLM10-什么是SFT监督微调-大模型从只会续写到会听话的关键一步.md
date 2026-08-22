# 什么是 SFT 监督微调：大模型从只会续写到会听话的关键一步

> 刚预训练完的大模型只会做一件事——预测下一个字，也就是不停地续写。而可以在产品里用的聊天模型，得听懂你的指令、按格式回答、该拒绝还得拒绝。从「不会续写」到「会听话」，中间这关键一步最常用的技术之一，就叫 **SFT（Supervised Fine-Tuning，监督微调）**。本文带你拆解 SFT 的定义、数据、机制与能力边界。

---

## 全文摘要

SFT（Supervised Fine-Tuning，监督微调）是让大模型从「只会续写」走向「会听话」的关键一步。它不是在预训练时把整个互联网再读一遍，而是拿一批高质量的「指令 + 答案」数据，在已经预训练好的基础模型上继续训练，手把手告诉模型「碰到这种请求，应该这样回答」。SFT 的训练目标仍然是语言模型那套老办法——最小化下一个 Token（词元）的预测损失，变的只是数据从「随便一段文本」换成了「指令加标准回答」。但 SFT 不是万能钥匙：它学不到样本里没覆盖的知识，主要是在模仿参考答案而非真正理解偏好，也保证不了安全。把 SFT 吹成搞定对齐的万能钥匙是错误的，它的价值在于提升指令遵循、输出格式与任务可用性。

---

## 1. 背景介绍：预训练模型只会续写

一个刚预训练完的大模型（Base Model，基础模型），其实只会做一件事：**预测下一个字**。你给它一段文本，它就接着往下写；你问它问题，它大概率不会回答你，而是顺着问题继续编一段「看似合理的下文」。这是因为预训练阶段的任务目标就是 Next Token Prediction（下一词元预测）——在互联网规模的文本上，学习「给定前面的词，下一个最可能的词是什么」。它学到了海量的语言模式与知识分布，却完全没有学会「回答问题」「遵循指令」「拒绝请求」这些人类使用习惯。

一个可以在产品里用的聊天模型，需要具备三类能力：**听懂你的指令**、**按格式回答**、**该拒绝还得拒绝**。这些能力不会在预训练阶段凭空出现，必须通过后续的 Post-Training（后训练）阶段注入。而从「不会续写」到「会听话」，中间最常用、最基础的关键一步，就是 SFT（Supervised Fine-Tuning，监督微调）。

**参考资料：**

- [Post-training: Instruction Tuning, Alignment, and Test-Time Compute -- Stanford Speech and Language Processing 3rd Edition](https://web.stanford.edu/~jurafsky/slp3/9.pdf) ⭐值得阅读
- [SFT Fine-Tuning: Transform Base LLM to Chat Model -- LangCopilot](https://langcopilot.com/posts/2025-07-16-supervised-fine-tuning-sft-llms-practical-guide)
- [第十六章：使用大语言模型 -- transformers.run](https://transformers.run/c4/c16_finetune_llms/)

---

## 2. SFT 的定义：在基础模型上继续训练

SFT 的定义其实很直白：**在一个已经预训练好的基础模型上，再用人工标注、专家编写或者精挑细选出来的「指令 + 回答」数据，继续训练一段时间**。

它不是把整个互联网再给模型读一遍，而是拿一批高质量的指令与标准答案，手把手告诉模型：「碰到这种请求，你应该这样回答」。因此 SFT 又被称为**指令微调（Instruction Tuning）**，也是 InstructGPT 确立的标准对齐第一步。相比预训练动辄数万亿美元级别的算力消耗，SFT 通常在数千到数十万条指令数据上训练几个 Epoch（轮次），成本只是预训练的一个零头。

**参考资料：**

- [Post-training: Instruction Tuning, Alignment, and Test-Time Compute -- Stanford Speech and Language Processing 3rd Edition](https://web.stanford.edu/~jurafsky/slp3/9.pdf) ⭐值得阅读
- [什么是指令调整？ -- IBM](https://www.ibm.com/cn-zh/think/topics/instruction-tuning)
- [第十六章：使用大语言模型 -- transformers.run](https://transformers.run/c4/c16_finetune_llms/)
- [SFT 大模型监督微调 -- CSDN](https://blog.csdn.net/zc621_/article/details/142393070)

---

## 3. SFT 的训练数据：每条样本的三层结构

在 SFT 阶段，我们喂进去的每份样本通常都分成三层：

1. **一条指令（Instruction）**：告诉模型要做什么，例如「请把这句话翻译成英文」
2. **一段可选的输入材料（Input）**：指令所需要的上下文，例如待翻译的中文句子
3. **一个标准回答（Response）**：期望模型输出的目标答案

模型看着指令和输入材料，去学着生成那个标准回答。这种三层结构在开源数据集里随处可见——以经典的 Alpaca 格式为例，每条样本就是一个 JSON 对象：

```json
{
  "instruction": "计算这些物品的总费用",
  "input": "汽车 - $3000，衣服 - $100，书 - $20",
  "output": "汽车、衣服和书的总费用为 $3000 + $100 + $20 = $3120"
}
```

其中 `instruction` 是指令、`input` 是可选输入材料、`output` 是标准回答，正好对应上面的三层结构。

训练时通常还会做 **Loss Masking（损失掩码）**——只对回答部分的 Token 计算损失，指令和输入部分的损失被屏蔽，让模型把全部学习容量花在「学会生成正确回答」上，也避免了它去学习模仿用户的问法。推理阶段则必须使用与训练一致的 Chat Template（聊天模板，如 `<|user|>`、`<|assistant|>` 角色标记），否则模型会偏离它被微调时所处的数据分布。

「监督」两个字的意思就在这里：**每道题都配好了参考答案**。模型不用自己瞎摸索，它做的是模仿这些高质量答案。数据的质量远比数量重要——LIMA 论文发现，仅用 1000 条人工精选的高质量指令数据微调 65B 模型，就能取得与大规模对齐模型相当的效果，这被称为「表面对齐假说（Superficial Alignment Hypothesis）」：模型的知识和能力几乎全部来自预训练，SFT 主要教它「在什么场合用什么样的格式与风格说话」。

**参考资料：**

- [Post-training: Instruction Tuning, Alignment, and Test-Time Compute -- Stanford Speech and Language Processing 3rd Edition](https://web.stanford.edu/~jurafsky/slp3/9.pdf) ⭐值得阅读
- [Supervised Fine-Tuning and PEFT -- AI as an Infrastructure](https://aaai.latere.ai/en/adaptation/sft-peft) ⭐值得阅读
- [SFT Fine-Tuning: Transform Base LLM to Chat Model -- LangCopilot](https://langcopilot.com/posts/2025-07-16-supervised-fine-tuning-sft-llms-practical-guide)
- [数据处理（Alpaca 格式）-- LlamaFactory](https://llamafactory.readthedocs.io/zh-cn/latest/getting_started/data_preparation.html)
- [Alpaca 数据集 -- Stanford CRFM](https://github.com/tatsu-lab/stanford_alpaca)
- [第十六章：使用大语言模型 -- transformers.run](https://transformers.run/c4/c16_finetune_llms/)
- [LIMA: Less Is More for Alignment -- NeurIPS 2023](https://proceedings.neurips.cc/paper_files/paper/2023/hash/ac662d74829e4407ce1d126477f4a03a-Abstract-Conference.html)

---

## 4. SFT 的训练机制：还是预测下一个 Token

SFT 一点都不神秘。多数时候，它用的还是语言模型那套老办法——**最小化下一个 Token 的预测损失，也就是语言模型损失（Language Modeling Loss）**。模型被要求在看完指令和上下文之后，一步步预测出标准回答的每个 Token。

变的只是数据：从「随便一段文本」换成了「指令加标准回答」。数据换了，训练目标不变，模型用交叉熵损失计算预测概率与标准答案之间的差距，通过梯度下降更新权重。这意味着 SFT 并不会为模型「重造大脑」，而是在原有参数的基础上做一个相对小幅、低维度的调整，让模型学会用预训练阶段积累的知识去「按指令办事」。

由于调整幅度小、维度低，SFT 也催生了 LoRA（Low-Rank Adaptation，低秩适配）、QLoRA 等参数高效微调（Parameter-Efficient Fine-Tuning，PEFT）方法：冻结原始权重，只训练极少量新增的低秩参数，就能以接近全参数微调的效果完成指令适配，同时把训练成本降低上百倍。

**参考资料：**

- [Post-training: Instruction Tuning, Alignment, and Test-Time Compute -- Stanford Speech and Language Processing 3rd Edition](https://web.stanford.edu/~jurafsky/slp3/9.pdf) ⭐值得阅读
- [Supervised Fine-Tuning and PEFT -- AI as an Infrastructure](https://aaai.latere.ai/en/adaptation/sft-peft) ⭐值得阅读
- [SFT Fine-Tuning: Transform Base LLM to Chat Model -- LangCopilot](https://langcopilot.com/posts/2025-07-16-supervised-fine-tuning-sft-llms-practical-guide)
- [第十六章：使用大语言模型 -- transformers.run](https://transformers.run/c4/c16_finetune_llms/)

---

## 5. SFT 的能力边界：它不是万能钥匙

SFT 可以让模型学会特定领域的说话方式和任务格式，但**它不是万能钥匙**。有三条边界必须认清：

**第一，SFT 不是事实数据库。** 样本里没有覆盖的知识，模型学不到。SFT 不负责注入新知识，它只是调动预训练阶段已有的知识——如果基础模型本身不知道某件事，再多的指令微调也无法让它凭空「知道」。更隐蔽的风险是：研究（Why Fine-Tuning Encourages Hallucinations）发现，当 SFT 数据引入新的知识时，模型还可能产生「事实遗忘」——原本在预训练中能答对的问题，微调后反而答错了，这被归因于新旧知识在模型内部的表征干扰。

**第二，SFT 主要是在模仿参考答案，不见得真学会了「哪个答案更合人的口味」。** 对每个提示，SFT 只给一个「标准示范」，模型学会的是模仿这个特定输出，而不是学到「简洁、准确、类比得当」这类抽象偏好特质。偏好优化需要相对比较信号（同一个问题下多个回答「A 好还是 B 好」），这正是 RLHF（Reinforcement Learning from Human Feedback，基于人类反馈的强化学习）、DPO（Direct Preference Optimization，直接偏好优化）要解决的问题。

**第三，光靠 SFT 保证不了安全。** 无害性不仅仅是「不输出明显有害内容」，还包括优雅地拒绝危险指令、避免有害刻板印象等抽象原则，这些无法靠输入输出对一一展示。SFT 之后通常还得接上 RLHF/DPO、规则过滤、红队评测（Red Teaming）这一整套对齐链路。

**参考资料：**

- [Why Fine-Tuning Encourages Hallucinations and How to Fix It -- arXiv](https://arxiv.org/abs/2604.15574) ⭐值得阅读
- [监督微调（SFT）的局限性 -- APXML RLHF 课程](https://apxml.com/zh/courses/rlhf-reinforcement-learning-human-feedback/chapter-1-rlhf-foundations-alignment/sft-limitations) ⭐值得阅读
- [Post-training: Instruction Tuning, Alignment, and Test-Time Compute -- Stanford Speech and Language Processing 3rd Edition](https://web.stanford.edu/~jurafsky/slp3/9.pdf) ⭐值得阅读
- [Supervised Fine-Tuning and PEFT -- AI as an Infrastructure](https://aaai.latere.ai/en/adaptation/sft-peft) ⭐值得阅读

---

## 6. 对齐链路：SFT 只是第一棒

把 SFT 吹成「搞定对齐的万能钥匙」是好笑的。真实的大模型对齐（Alignment）是一条接力赛道，SFT 只是第一棒：

1. **SFT（监督微调）**：让模型具备基础的指令遵循与格式能力
2. **RLHF / DPO（偏好对齐）**：用人类偏好数据让模型学会「哪个回答更符合人的口味」，优化 Helpfulness（有用性）、Honesty（诚实性）、Harmlessness（无害性）
3. **规则过滤（Rule-based Filtering）**：用硬规则在训练与推理阶段过滤敏感、违规内容
4. **红队评测（Red Teaming）**：用对抗性攻击与边界测试找出模型的安全漏洞，再针对性地迭代训练

每项技术各司其职：SFT 负责「会听话」，偏好对齐负责「说得更好」，规则过滤与红队负责「不越界」。其中 RLHF 和 DPO 各有取舍：RLHF 需要额外训练一个奖励模型（Reward Model）再用强化学习优化策略，训练更复杂但通常效果更稳；DPO 用偏好数据直接微调模型，绕开奖励建模，实现简单、训练更稳定，但理论上只有在奖励函数可准确表示时才与 RLHF 等价。只有把这些技术组合起来，才能得到真正可用的产品级模型。

**参考资料：**

- [Post-training: Instruction Tuning, Alignment, and Test-Time Compute -- Stanford Speech and Language Processing 3rd Edition](https://web.stanford.edu/~jurafsky/slp3/9.pdf) ⭐值得阅读
- [Understanding the Performance Gap in Preference Learning: A Dichotomy of RLHF and DPO -- arXiv](https://arxiv.org/html/2505.19770)
- [监督微调（SFT）的局限性 -- APXML RLHF 课程](https://apxml.com/zh/courses/rlhf-reinforcement-learning-human-feedback/chapter-1-rlhf-foundations-alignment/sft-limitations) ⭐值得阅读
- [聊聊大模型微调训练全流程的思考 -- 博客园](https://www.cnblogs.com/zhiyong-ITNote/p/18080667)

---

## 7. 总结

最后一定要划清边界：SFT 的价值是**提升指令遵循、输出格式和任务可用性**，但它**保证不了事实正确、偏好最优和安全充分**。SFT 不是重造大脑，而是教模型按指令把事做好——它把预训练阶段积累的知识和语言能力「引导」到符合人类使用习惯的方向上。

记住一句话就足够了：一个刚预训练完的大模型，只会预测下一个字；而 SFT，就是让它从「不停续写」变成「会听话」的那关键一步。

---

## 参考资料汇总

- [Post-training: Instruction Tuning, Alignment, and Test-Time Compute -- Stanford Speech and Language Processing 3rd Edition](https://web.stanford.edu/~jurafsky/slp3/9.pdf) ⭐值得阅读
- [Supervised Fine-Tuning and PEFT -- AI as an Infrastructure](https://aaai.latere.ai/en/adaptation/sft-peft) ⭐值得阅读
- [SFT Fine-Tuning: Transform Base LLM to Chat Model -- LangCopilot](https://langcopilot.com/posts/2025-07-16-supervised-fine-tuning-sft-llms-practical-guide)
- [监督微调（SFT）的局限性 -- APXML RLHF 课程](https://apxml.com/zh/courses/rlhf-reinforcement-learning-human-feedback/chapter-1-rlhf-foundations-alignment/sft-limitations) ⭐值得阅读
- [Why Fine-Tuning Encourages Hallucinations and How to Fix It -- arXiv](https://arxiv.org/abs/2604.15574) ⭐值得阅读
- [Understanding the Performance Gap in Preference Learning: A Dichotomy of RLHF and DPO -- arXiv](https://arxiv.org/html/2505.19770)
- [什么是指令调整？ -- IBM](https://www.ibm.com/cn-zh/think/topics/instruction-tuning)
- [第十六章：使用大语言模型 -- transformers.run](https://transformers.run/c4/c16_finetune_llms/)
- [LIMA: Less Is More for Alignment -- NeurIPS 2023](https://proceedings.neurips.cc/paper_files/paper/2023/hash/ac662d74829e4407ce1d126477f4a03a-Abstract-Conference.html)
- [数据处理（Alpaca 格式）-- LlamaFactory](https://llamafactory.readthedocs.io/zh-cn/latest/getting_started/data_preparation.html)
- [Alpaca 数据集 -- Stanford CRFM](https://github.com/tatsu-lab/stanford_alpaca)
- [SFT 大模型监督微调 -- CSDN](https://blog.csdn.net/zc621_/article/details/142393070)
- [聊聊大模型微调训练全流程的思考 -- 博客园](https://www.cnblogs.com/zhiyong-ITNote/p/18080667)
