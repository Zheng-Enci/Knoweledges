# 大模型的分类到底怎么分：从基础模型到推理模型、从通用到专用的完整图谱

> **核心结论**：大模型「分类」没有唯一答案，不同维度切出来的类别完全不同，但有三条主线索最实用：**① 按能力定位**——基础模型（Base）、指令微调模型（Instruct）、推理模型（Reasoning），对应「会续写 → 会听话 → 会思考」三个层次；**② 按应用领域**——通用大模型（L0）、行业大模型（L1）、垂域大模型（L2），对应「通识教育 → 行业熟手 → 场景专家」；**③ 按模态与架构**——纯语言 / 多模态、稠密（Dense）/ 混合专家（MoE）。理解这套分类，你才能知道该选哪个模型、为什么同一个模型家族要分 base 和 chat 两个版本、以及「推理模型」凭什么更贵。

## 目录

- 1. 一句话结论
- 2. 为什么大模型「分类」说不清：维度不同、答案就不同
- 3. 按能力定位分（Base / Instruct / Reasoning）：会续写、会听话、会思考
- 4. Base 基础模型：只会续写的「百科全书式新员工」
- 5. Instruct 指令微调模型：学会「听话」的对话助手
- 6. Reasoning 推理模型：会「停下来想」的思考者
- 7. 按应用领域分（L0 / L1 / L2）：通用、行业、垂域
- 8. 按架构分：稠密 Dense vs 混合专家 MoE
- 9. 按模态分：纯语言 vs 多模态
- 10. 一张总表：三种分类维度的对照
- 11. 完整可运行代码：用 HuggingFace 区分三种模型
- 12. 对照表：症状 → 原因 → 解法
- 13. 判断收尾

## 1. 一句话结论

先建立一个直觉 🎭：**大模型分类像「给员工分职级」**——同一个人的学历（能力定位）是一回事，他在哪个部门（应用领域）是另一回事，他是什么部门类型（架构）又是第三回事。你不能用「他是研究生」来回答「他是哪个部门的」，这两件事本就独立。

所以记三个最实用的分类框架：

- **能力定位**（最重要）：Base（会续写）→ Instruct（会听话）→ Reasoning（会思考）。
- **应用领域**：L0 通用（通识）→ L1 行业（熟手）→ L2 垂域（专家）。
- **架构 / 模态**：Dense vs MoE、纯语言 vs 多模态。

一句话：**先搞懂「能力定位」这一维，你就已经解决了 80% 的选型问题**——其他维度是锦上添花。

## 2. 为什么大模型「分类」说不清：维度不同、答案就不同

很多人问「大模型分哪几类」，得到的答案五花八门，是因为**大家都从不同维度回答**：

- 有人说分「通用 / 行业 / 垂域」——这是按**应用领域**切。
- 有人说分「基础 / 对话 / 推理」——这是按**能力定位**切。
- 有人说分「稠密 / 稀疏」——这是按**架构**切。
- 有人说分「语言 / 视觉 / 多模态」——这是按**输入类型**切。

这些答案都对，但它们**属于不同的坐标系**。一个模型可以同时是「通用 + Instruct + MoE + 多模态」，就像一个人可以同时是「研究生 + 技术部 + 程序员」——四个标签来自四个维度，彼此不冲突。

> ⚠️ 理解这一点是读懂本文的前提：**「大模型分几类」没有一个标准答案，只有「按这个维度分几类」。** 接下来分别讲三条最常用坐标轴。

## 3. 按能力定位分（Base / Instruct / Reasoning）：会续写、会听话、会思考

这是**最实用的分类维度**，因为它直接对应「你下载模型时会看到的三个版本名」——几乎所有主流模型家族（Qwen、Llama、DeepSeek 等）都会发布这三个版本：

- **Base 基础模型**：预训练（pretraining）后的原始 checkpoint，只会「续写下一个 token」。
- **Instruct 指令微调模型**：Base 再经过指令微调（instruction tuning）+ 偏好对齐，学会「照着指令回答」。
- **Reasoning 推理模型**：Instruct 之上再做推理专用训练（如 RL 强化学习），学会「先思考再作答」。

| 模型类型 | 训练阶段 | 核心能力 | 典型例子 |
|---------|---------|---------|---------|
| Base | 预训练后 | 续写、补全、few-shot | Qwen3-8B（未对齐版） |
| Instruct | + 指令微调 + 对齐 | 回答问题、跟格式 | Qwen3-8B-Instruct |
| Reasoning | + 推理强化训练 | 长思维链、解难题 | Qwen3-8B-Thinking |

打个比方 🎭：**Base 像「读遍公司所有书但没上过班的新员工」**——知识全有但不会办事；Instruct 像「培训过如何接指令的正式员工」——会照着规矩干活；Reasoning 像「会先想清楚再动手的老手」——遇难题会停下来琢磨。

参考资料：
- [Base, Instruct, and Reasoning Models Compared -- Sebastian Raschka](https://sebastianraschka.com/faq/docs/base-vs-instruct-vs-reasoning-model.html) ⭐值得阅读
- [Base vs Instruct vs Chat vs Reasoning Models -- LMVersity](https://lmversity.com/learn/llm-foundations/base-instruct-chat-reasoning-families)

## 4. Base 基础模型：只会续写的「百科全书式新员工」

Base 模型是**预训练的直接产物**——在海量文本上用「预测下一个 token」练出来的原始 checkpoint。

- **会什么**：补全文本、续写故事、few-shot（给几个例子它能照着来）、计算「下一句最可能是什么」。
- **不会什么**：它不会「正常回答问题」。你问「15% of 60」，它可能继续编一个问题、列一堆不相干的问题，或写成一段小作文——因为对它来说，这些都只是「合理续写」。
- **为什么存在**：Base 是 Instruct / Reasoning 的**起点原料**，也是研究者做「继续预训练」「领域预训练」的基底。

用新员工类比 🎭：**Base 是那个「把公司所有书都读了一遍、但一天班没上过」的新人**——你问他怎么处理报销，他给你背一段 HR 手册的原文，而不是告诉你「填这张单子」。他知识渊博，但不会办事。

> 💡 对普通用户：**别直接用 Base 模型**。它不适合对话，你用起来会觉得「这 AI 怎么答非所问」——那是你选错了版本，不是模型差。

## 5. Instruct 指令微调模型：学会「听话」的对话助手

Instruct 模型在 Base 之上，用「指令-回答」的配对数据做了**指令微调（instruction tuning）**，再用偏好数据（如 RLHF，人类反馈强化学习）对齐，让模型「学会听话」。

- **会什么**：直接回答问题、遵循你指定的格式（JSON、列表、摘要）、按对话模板（chat template）跟你对话。
- **关键点**：它要求**特定的对话格式**——特殊的 token、角色标记、turn 结束标记。格式给错了，质量会断崖式下降，看起来就像「这个模型很烂」。
- **为什么重要**：Instruct 是**绝大多数人日常用的模型**——你打开 ChatGPT、Kimi、文心一言，背后基本都是 Instruct / Chat 类模型。

> ⚠️ 常见误区：很多人下载了 Base 模型当对话用，效果差就骂模型不行——**其实是该用 Instruct 版本**。这也是我在[同样的模型为什么本地和云API差别那么大：量化精度、聊天模板与采样参数的三大元凶](https://juejin.cn/spost/7702592474153975858)里强调的「聊天模板」问题的根源。

参考资料：
- [Base, Instruct, Chat, Reasoning -- LMVersity](https://lmversity.com/learn/llm-foundations/model-families-and-variants)
- [Foundation Models: Base vs Instruct vs Chat -- AI/TLDR](https://ai-tldr.dev/learn/llm-fundamentals/llm-basics/base-vs-instruct-models/)

## 6. Reasoning 推理模型：会「停下来想」的思考者

推理模型（Reasoning Model）是近两年最热的一类，代表如 OpenAI 的 o 系列、DeepSeek-R1、Qwen 的 Thinking 版。它在 Instruct 基础上，用强化学习专门训练「先思考再回答」。

- **核心差异**：普通模型「看到问题立刻答」，推理模型会先生成一段**长思维链（chain-of-thought）**，把中间推理过程写出来，再给最终答案。
- **擅长什么**：数学题、逻辑题、编程、复杂推理——需要「多步推导」的任务。
- **代价是什么**：**慢、贵、token 消耗大**。它每个问题都「想半天」，推理成本比 Instruct 高好几倍。

用类比 🎭：**Instruct 像「反应快的实习生」**，问啥秒答，但复杂问题容易答错；**Reasoning 像「会打草稿的老手」**，先在草稿纸上算一遍再报答案，慢但准。

> 💡 **选型判断**：日常聊天、摘要、普通问答 → Instruct 够用且快；数学、推理、疑难编程 → 上 Reasoning。别为所有问题都用推理模型，那是拿大炮打蚊子。

参考资料：
- [Choosing the right model -- BentoML](https://www.bentoml.com/llm/getting-started/choosing-the-right-model)

## 7. 按应用领域分（L0 / L1 / L2）：通用、行业、垂域

第二条主坐标轴，按「服务于谁」切分，国内常用 **L0 / L1 / L2** 三层的说法（由行业专家提出，如中科院王金桥）：

- **L0 通用大模型（基础通用）**：泛化能力强、能「举一反三」，相当于完成「通识教育」。如 GPT、DeepSeek、Qwen 的通用旗舰。
- **L1 行业大模型（行业）**：在 L0 基础上，用特定行业数据（医疗、金融、法律语料）微调，掌握行业术语与知识体系，相当于「进入行业的熟手」。如金融领域的专用对话模型。
- **L2 垂域大模型（垂直场景）**：面向更具体的业务场景深度优化，相当于「解决特定问题的专家」。如针对某种单据识别的 OCR 大模型。

用类比 🎭：**L0 是「上过通识课的大学毕业生」，L1 是「入职某行业干了三年的熟手」，L2 是「专门修某一类设备的老师傅」**——越往下越专、越窄，但解决具体问题的效率越高。

参考资料：
- [大模型有大应用，武汉遴选出首批26个垂直大模型 -- 武汉市政府](https://www.wuhan.gov.cn/sy/whyw/202512/t20251223_2699087.shtml)
- [大模型L0-L2分级与分类详解 -- 51CTO学堂](https://edu.51cto.com/article/note/61641.html)

## 8. 按架构分：稠密 Dense vs 混合专家 MoE

第三条坐标轴是「模型内部怎么组织」，主要分两类：

- **稠密模型（Dense）**：所有参数在每个输入上都被激活。结构简单、行为可预期，但**参数多、推理成本高**。
- **混合专家模型（MoE，Mixture of Experts）**：由多个「专家子网络」组成，**每个输入只激活其中一部分专家**。同样的总参数量下，单次推理只走一小部分专家，**又快又省**，还能把参数堆到万亿级。

用类比 🎭：**Dense 像「一支全队都要上场的球队」**，每个球员都参与；**MoE 像「一个分工明确的大团队」**，接到任务只派最对口的几个小组上场，其他人待命。

> 💡 在本专栏的《MoE 混合专家模型深度解析》中我们详细讲过 MoE 的机制，这里只记住结论：**MoE 用「总参数大、单次计算小」换来了「大模型 + 低推理成本」**，是当前万亿级模型的默认选择。

## 9. 按模态分：纯语言 vs 多模态

第四条坐标轴看「模型能处理什么输入」：

- **纯语言大模型（LLM，Large Language Model）**：只处理文本，输入是 token，输出也是 token。
- **多模态大模型（LMM，Large Multimodal Model）**：能处理文本、图像、音频、视频，比如「看图说话」「语音理解」。常见形式是**视觉语言模型（VLM）**，如 GPT-4V、Qwen-VL。

用类比 🎭：**纯语言模型像「只认字的编辑」**，多模态模型像「能看图说话的记者」——都能产出文字，但后者多了「看图」这个输入通道。

> 💡 这是**最独立的维度**：多模态和「通用 / 专用」不冲突，也和「Base / Instruct」不冲突——一个模型可以同时是「多模态 + Instruct + 通用」。

## 10. 一张总表：三种分类维度的对照

把四条坐标轴放在一起看，才不会乱：

| 分类维度 | 类别 | 核心区别 | 一句话记忆 |
|---------|------|---------|-----------|
| 能力定位 | Base / Instruct / Reasoning | 续写 → 听话 → 思考 | 三档职级 |
| 应用领域 | L0 通用 / L1 行业 / L2 垂域 | 通识 → 熟手 → 专家 | 三个部门 |
| 架构 | Dense / MoE | 全激活 / 部分激活 | 全队上场 vs 分工 |
| 模态 | 纯语言 / 多模态 | 只看字 / 能看图 | 认字 vs 看图 |

**关键认知**：这四个维度是**正交**的（互相独立），一个模型在这四个维度上各有一个标签。理解它们，你就看懂了模型命名里的后缀含义——`-Instruct` 是能力定位，`-VL` 是多模态，`-MoE` 是架构，`-L2`（如果标注）是应用层级。

## 11. 完整可运行代码（Runnable Code）：用 HuggingFace 区分三种模型

下面是一段**复制粘贴就能跑**的代码，用 HuggingFace 加载同一个模型的三个版本，直观对比 Base / Instruct / Reasoning 对同一句 prompt 的响应差异。运行前 `pip install transformers`。

```python
from transformers import AutoModelForCausalLM, AutoTokenizer
import torch

# 用 Qwen 家族演示：同一个模型系列的三个版本（能力定位三档）
MODELS = {
    "Base":      "Qwen/Qwen2.5-0.5B",        # 基础模型：只会续写
    "Instruct":  "Qwen/Qwen2.5-0.5B-Instruct",  # 指令微调：会听话
    # Reasoning 版用 DeepSeek-R1-Distill 演示（小参数推理模型）
    "Reasoning": "deepseek-ai/DeepSeek-R1-Distill-Qwen-1.5B",
}

prompt = "15% of 60 is"  # 一个需要"先想再答"的数学问题

for kind, name in MODELS.items():
    print(f"\n===== {kind} 模型：{name} =====")
    tokenizer = AutoTokenizer.from_pretrained(name)   # 加载对应分词器
    model = AutoModelForCausalLM.from_pretrained(name)  # 加载对应模型
    inputs = tokenizer(prompt, return_tensors="pt")    # 编码 prompt
    out = model.generate(**inputs, max_new_tokens=40,  # 生成 40 个 token 的续写
                         do_sample=False)              # 贪心解码，结果确定
    print("输出：", tokenizer.decode(out[0], skip_special_tokens=True))
```

**怎么读这段代码**：同一个 prompt `15% of 60 is`，**Base 版**大概率会继续「编一句合理的续写」（答非所问）；**Instruct 版**会规规矩矩给出「15% of 60 is 9」；**Reasoning 版**会先输出一段「思考」再给答案。三行代码就能看出「能力定位」三档模型的本质差异——这也是第 3～6 节讲的概念的可运行落地。

## 12. 对照表：症状 → 原因 → 解法

| 症状 | 原因 | 解法 |
|------|------|------|
| 下载模型聊不起来，答非所问 | 下了 Base 版本，它只会续写 | 换用 Instruct / Chat 版本 |
| 让模型出 JSON / 列表，格式总乱 | 用的模型没做指令对齐 | 用 Instruct 版，且聊天模板要正确 |
| 数学 / 逻辑题总答错 | 普通 Instruct 不会「先思考」 | 换 Reasoning / Thinking 版模型 |
| 复杂推理用普通模型，又慢又贵 | 该用推理模型却用了对话模型 | 上 Reasoning，但别所有问题都用 |
| 想要行业专用能力（金融/医疗） | 通用模型缺领域深度 | 用 L1 行业大模型或微调 |
| 纠结「模型分几类」答案不一致 | 各人按不同维度切 | 先定维度，再谈分类 |

## 13. 判断收尾

**什么时候该用这套分类**：你需要在「选模型 / 理解模型版本后缀 / 判断为什么某个模型不听话」时——先看**能力定位**（Base/Instruct/Reasoning）定版本，再看**应用领域**（L0/L1/L2）定专业度，最后用**架构与模态**补充约束。**什么时候不必纠结**：你只是用现成的 API 聊天、不自己部署模型时，这些分类对你只是「知道即可」的背景知识，不用逐个深究。判断标准只有一条——**你是在「选模型」还是在「用模型」**，前者需要这套分类，后者直接挑口碑好的通用 Instruct 版即可。

本专栏《LLM 大模型技术专栏》从 Transformer 注意力机制一路讲到模型选型、微调、推理优化与 Agent 落地，每篇都配一段可直接运行的代码，每周更新一篇。想按顺序读完，可在专栏页订阅。

参考资料（综合）：
- [Base, Instruct, and Reasoning Models Compared -- Sebastian Raschka](https://sebastianraschka.com/faq/docs/base-vs-instruct-vs-reasoning-model.html) ⭐值得阅读
- [Base vs Instruct vs Chat vs Reasoning Models -- LMVersity](https://lmversity.com/learn/llm-foundations/base-instruct-chat-reasoning-families) ⭐值得阅读
- [Choosing the right model -- BentoML](https://www.bentoml.com/llm/getting-started/choosing-the-right-model)
- [大模型L0-L2分级与分类详解 -- 51CTO学堂](https://edu.51cto.com/article/note/61641.html)
- [大模型有大应用，武汉遴选出首批26个垂直大模型 -- 武汉市人民政府门户网站](https://www.wuhan.gov.cn/sy/whyw/202512/t20251223_2699087.shtml)
