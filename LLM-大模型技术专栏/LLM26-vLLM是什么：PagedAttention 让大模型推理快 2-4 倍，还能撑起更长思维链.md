# vLLM是什么：PagedAttention 让大模型推理快 2-4 倍，还能撑起更长思维链

**vLLM 不会让模型更聪明。** 它不开源新模型、不改权重、不做微调，单次问答的答案质量和原模型一模一样你把它理解成「模型的操作系统」更准确：一个开源的 LLM 推理服务引擎（inference serving engine），由 UC Berkeley Sky Computing Lab 发起，用 PagedAttention（分页注意力）把 KV Cache 按 block 管理，把旧系统 60%–80% 的显存浪费压到 4% 以下，同延迟下吞吐提升 2–4 倍。

那「为什么能让大模型推理性更好」这个问题从哪来？因为成本降下来之后，你终于跑得起更长的思维链、更多路的采样投票（self-consistency，自洽性投票）——真正提升 reasoning（推理性）的是这些 test-time compute（测试期计算）手段，vLLM 只是把它们的账单打了下来。

---

## 目录

- 1. vLLM 到底在做什么
- 2. 两个「推理」要分清：inference 与 reasoning
- 3. KV Cache 为什么把显存吃光
- 4. PagedAttention：把操作系统的虚拟内存搬到 GPU 上
- 5. 连续批处理与 chunked prefill：让 GPU 不再空转
- 6. 前缀缓存：长系统提示词只算一次
- 7. 一段可直接跑的代码：用 vLLM 做 self-consistency 采样
- 8. 症状 → 原因 → 解法对照表
- 9. 「推理性更好」的真实来源：test-time compute
- 10. 三个常见误解

---

## 1. vLLM 到底在做什么（What vLLM Does）

一个 LLM 上线要经过两个完全不同的阶段。训练（training）是一次性的，把权重算出来；推理（inference）是长期的，每来一个用户请求就要跑一次前向。vLLM 只负责第二阶段。

它对外暴露的是 **OpenAI-compatible API server**（兼容 OpenAI 接口的服务端）：你原来调 `POST /v1/chat/completions` 的代码，把 `base_url` 换成本地地址就能跑，不用改调用方。对内它做三件事：把请求排进队列并决定每一步跑哪些（scheduling，调度）；管理 GPU 上放 KV Cache 的那块显存（KV cache manager）；把多条请求拼成一个大 batch 一起送进 GPU（batching）。

官方文档给的「为什么快」清单可以归成四类：显存不再碎片化、批处理不再等最慢的那条、重复前缀不再重复算、算子层用 FlashAttention / FlashInfer / FlashMLA 这类优化 kernel。四件事叠起来，才有一个数量级左右的吞吐差距。

> 🍜 打个比方：vLLM 不是把厨师换成米其林大厨，而是把后厨的动线重排了一遍——灶台不再空着等配菜，同一锅汤底不重复熬，八个锅同时开火但共用一口汤锅。菜谱没变，出餐速度变了。

## 2. 两个「推理」要分清：inference 与 reasoning（Inference vs Reasoning）

中文把这两个词都译成「推理」，于是「vLLM 让大模型推理更好」这句话天然会产生歧义。必须拆开：

| 维度 | inference（推理 / 模型推断） | reasoning（推理性 / 推理能力） |
| --- | --- | --- |
| 指的是什么 | 把输入 token 变成输出 token 的这次前向计算 | 模型解决多步问题的能力 |
| 谁负责 | 推理引擎（vLLM、SGLang、TensorRT-LLM） | 模型权重 + 解码策略 + 上下文 |
| 能不能被 vLLM 改变 | 能，大幅改变速度与成本 | 不能，vLLM 不碰权重 |
| 衡量指标 | throughput、TTFT、TPOT、每秒 token 数 | 准确率、pass@k、数学题正确率 |

所以严格说，vLLM 改善的是 **inference 的效率**，不是 **reasoning 的能力**。但这两件事在工程上并不独立——第 9 章会展开这条因果链：效率决定了你能负担多少 test-time compute，而 test-time compute 才是 reasoning 变好的直接原因。顺便说清一个常见混淆：vLLM 里没有「推理模式」这种开关，它不会因为用了 vLLM，模型就多想几步。

## 3. KV Cache 为什么把显存吃光（KV Cache Fragmentation）

自回归生成有个特点：生成第 $t$ 个 token 时，前面 $t-1$ 个 token 的 Key 和 Value 向量不会变。所以标准做法是把它们缓存起来，避免每步重算——这就是 KV Cache（KV 缓存）。

问题在于这块缓存的大小是**动态且不可预知**的。它随序列长度线性增长，而序列长度取决于用户会问多长、模型会答多长，事先谁也不知道。vLLM 团队 2023 年的测量结论是：现有系统因为内存碎片（fragmentation）和过度预留（over-reservation），浪费了 60%–80% 的 KV Cache 显存。

浪费来自两处：

- **内部碎片（internal fragmentation）**：按最大可能长度预分配，实际只用了 20%，剩下 80% 空着
- **外部碎片（external fragmentation）**：每条请求要求一段**连续**显存，不同长度请求交错释放后，碎片之间的空洞谁也填不进去

在 8×A100-80GB 上跑 LLaMA-13B，这相当于约 300 GB 显存被空槽位占着。显存空着 batch 就开不大，batch 开不大算力就闲置——吞吐上不去，单 token 成本下不来。

## 4. PagedAttention：把操作系统的虚拟内存搬到 GPU 上（PagedAttention）

PagedAttention 的思路几乎是把操作系统的分页虚拟内存（paged virtual memory）原样照搬：

- 把 KV Cache 切成固定大小的 **block**（默认 16 个 token 一块），物理上不需要连续
- 每条请求维护一张 **block table**（块表），记录它的逻辑块号映射到哪几个物理块
- 注意力 kernel 按 block table 去散落的物理块里取 K/V，算子内部处理不连续性

这样内部碎片最多剩最后一个 block 的零头，外部碎片直接消失——因为根本不需要连续空间。vLLM 官方给的数据是浪费率从 60%–80% 降到 **4% 以下**。

单块的显存占用可以精确算出来：

$$
\text{bytes per block} = 2 \times \text{block\_size} \times \text{num\_kv\_heads} \times \text{head\_size} \times \text{dtype\_bytes}
$$

前面的 2 是 Key 和 Value 各一份。以 block_size = 16、num_kv_heads = 8、head_size = 128、bf16（2 字节）为例，一块约 64 KB；显存能放多少块，由启动时一次 dummy 前向 + 显存快照测出，这个数字直接决定能开多大的 batch。

**附带收益比省显存更重要：block 可以共享。** 同一个 prompt 的多个采样分支、同一个系统提示词的多个请求，可以指向同一批物理块，只在写的时候复制（copy-on-write）。这正是第 6 章前缀缓存和第 9 章多路采样的地基。

论文给出的实测结果是：在同等延迟下，vLLM 的吞吐比 FasterTransformer 和 Orca 高 **2–4 倍**；序列越长、模型越大、解码策略越复杂（beam search、并行采样），差距越明显。原因很直接——这些场景正是 KV Cache 最吃显存、碎片最严重的场景。

## 5. 连续批处理与 chunked prefill：让 GPU 不再空转（Continuous Batching）

旧式批处理（static batching，静态批处理）的问题很朴素：一个 batch 里最长的序列不结束，整批就得等着。GPU 的显存和算力一直被那几条已经生成完的请求占着，新请求排在门外。

**Continuous batching**（连续批处理，也叫 iteration-level scheduling，迭代级调度）把调度粒度从「一整次生成」缩小到「一次前向」：每跑完一步就回到调度器，把已结束的请求踢出去、把排队的新请求塞进来。这个概念出自 Orca 论文（OSDI '22），vLLM 是它最广泛部署的实现。Anyscale 在 Llama-13B 上实测最高 **23 倍**吞吐提升，而且 p50 延迟同时下降——理由很朴素：空转的 GPU 对谁都没好处。

**Chunked prefill**（分块预填充）解决的是另一个打架问题。prefill 要一次算完整个 prompt，是**计算密集**（compute-bound）的；decode 每步只算一个 token，是**显存带宽密集**（memory-bandwidth-bound）的。一条 32K 的长 prompt 整块跑，会把所有正在 decode 的请求全部卡住，用户的字就一个个往外挤。

chunked prefill 把长 prompt 切成若干块，每块和当前 decode 请求合到同一个 batch 里跑。代价是长请求的 TTFT（time to first token，首 token 延迟）变长一点，换来已经开始的流式输出不停顿——**尾延迟（tail latency）比平均延迟更值钱**，用户感知到的卡顿就来自那几次停顿。V1 引擎默认开启，且调度时优先服务 decode 请求。

> 🚌 打个比方：静态批处理像包车，人齐了才走，中途不能上下；连续批处理像公交，每站都停，有人下车马上有人上车。chunked prefill 则是给超长行李单独开了个托运窗口，不堵在车门那儿。

## 6. 前缀缓存：长系统提示词只算一次（Prefix Caching）

线上流量的一个特征是**前缀高度重复**：同一个应用的 system prompt（系统提示词）、同一份 few-shot 示例、同一个 Agent 的工具定义，每条请求开头都一模一样。

**Automatic Prefix Caching**（自动前缀缓存，APC）按 block 做哈希：每个 block 的哈希由「前缀所有 token 的哈希 + 本 block 的 token」算出。新请求进来时逐块比对，命中的块直接从显存复用，不重算。

三个必须记住的边界条件：

- 只缓存**完整**的 block（默认 16 token），零头不缓存
- 只减少 **prefill 时间**，不减少生成阶段的时间——输出 token 还是得一个个算
- 命中率取决于前缀是否逐 token 完全一致，差一个字符就整块失效

所以前缀缓存最典型的收益场景是「长系统提示词 + 短用户输入」，比如客服机器人、代码补全、多 Agent 协作。我在[多 Agent 系统如何复用 KV 缓存](https://juejin.cn/post/7699072089819070474)里拆过这个问题：多 Agent 场景下真正决定命中率的是**前缀对齐**，而不是缓存开关本身——把变化的字段（时间戳、用户 ID）从前缀里挪出去，比调任何参数都有效。vLLM 在 `/metrics` 暴露的 `vllm:prefix_cache_queries` 和 `vllm:prefix_cache_hits` 两个计数器，就是用来算实际命中率的。

## 7. 一段可直接跑的代码：用 vLLM 做 self-consistency 采样（Runnable Code）

下面这段代码把第 4 章和第 9 章串起来：用 vLLM 一次性对同一道题采样 8 条独立思维链，再对最终答案做多数投票。复制粘贴即可运行（需要一张显存 ≥ 8 GB 的 NVIDIA GPU）。

```python
# 环境：pip install "vllm>=0.6.0"；GPU 显存建议 >= 8GB，模型会自动下载
import re                                                        # 用正则从生成文本里抠出最终答案
from collections import Counter                                  # 用计数器做多数投票
from vllm import LLM, SamplingParams                             # vLLM 离线推理入口

MODEL_NAME = "Qwen/Qwen2.5-1.5B-Instruct"                        # 换成任意 HF 模型名或本地权重路径
PROBLEM = (                                                      # 一道需要多步推理的算术题
    "一个班有 38 名学生，其中 14 名是女生。"                       # 条件一：总人数与女生数
    "男生每人交 3 元班费，女生每人交 5 元。"                       # 条件二：两类人的单价
    "全班一共交多少钱？请一步一步算，最后单独一行写「答案：X」。"   # 要求模型显式给出最终答案
)

def extract_answer(text: str) -> str:                            # 从一段生成文本中抽取最终答案
    nums = re.findall(r"-?\d+(?:\.\d+)?", text)                   # 抓出所有数字（含负数与小数）
    return nums[-1] if nums else text.strip()[-20:]               # 取最后一个数字，兜底取末尾 20 字

def main() -> None:                                              # 主流程：采样 → 抽答案 → 投票
    llm = LLM(                                                   # 构造推理引擎，相当于起一个本地服务
        model=MODEL_NAME,                                        # 指定模型权重
        gpu_memory_utilization=0.85,                             # 允许占用 85% 显存做 KV Cache 池
        max_model_len=4096,                                      # 单条请求最长 4096 token
    )                                                            # 引擎构造时会跑一次 dummy 前向测算显存
    params = SamplingParams(                                     # 采样参数，关键在 n > 1
        n=8,                                                     # 同一道题采 8 条独立思维链
        temperature=0.8,                                         # 调高温度让 8 条路径尽量不重复
        top_p=0.95,                                              # nucleus 采样，截掉长尾低概率 token
        max_tokens=512,                                          # 每条思维链最多生成 512 token
    )                                                            # 8 条请求共享同一段 prompt 前缀
    outputs = llm.generate([PROBLEM], params)[0].outputs         # 一次喂 8 条，vLLM 内部合批跑
    answers = [extract_answer(o.text) for o in outputs]          # 逐条抽取最终答案
    print("8 条思维链的答案：", answers)                          # 打印投票分布，便于观察分歧大小
    winner, votes = Counter(answers).most_common(1)[0]           # 取出现次数最多的答案
    print(f"多数投票结果：{winner}（{votes}/8 票）")              # 输出最终答案与得票数

if __name__ == "__main__":                                       # 脚本入口
    main()                                                       # 执行主流程
```

这段代码里有三处值得注意：`n=8` 是关键，不设 `n` 就只有一条思维链，投票无从谈起；8 条请求共享同一段 prompt 前缀，prefix caching 命中后 prefill 只算一次；8 条请求被合成一个 batch 一起跑，显存占用远小于起 8 个独立进程，这正是 block 共享的收益。

把 `n` 从 1 调到 8，自己串行调用 8 次，耗时大约翻 8 倍；在 vLLM 里通常远小于 8 倍。这个差值就是「reasoning 变好的成本」被压下来的部分。

## 8. 症状 → 原因 → 解法对照表（Symptom / Cause / Fix）

| 症状（Symptom） | 原因（Cause） | 解法（Fix） |
| --- | --- | --- |
| 并发一上来，GPU 显存就 OOM，但 `nvidia-smi` 显示利用率不高 | 静态批处理按最长序列预分配显存，内部/外部碎片吃掉 60%–80% | 换 vLLM 的 PagedAttention，block 化后浪费降到 4% 以下 |
| 长 prompt 进来后，已经在输出的用户突然卡住 | 整块 prefill 独占一步，把 decode 全挤出去了 | 开 chunked prefill，切块与 decode 合批 |
| 吞吐上不去，`nvidia-smi` 利用率长期跑不满 | 一个 batch 里最慢的请求拖着整批，GPU 空转 | 连续批处理（V1 默认），结束即换人 |
| 系统提示词 8K，每条请求都重算一遍 | 前缀没被复用 | 开 automatic prefix caching，并把时间戳等易变字段移出前缀 |
| 命中率看着有，但省的时间不明显 | 只缓存完整 block，且只省 prefill 不省 decode | 对齐到 16 token 的整数倍；输出侧优化另算 |
| 想跑 self-consistency 提准确率，一算成本就放弃 | 多路采样的 prefill 与显存开销叠加 | 用 `n>1` 共享前缀块，同一 batch 内并行采样 |
| 换了量化模型，显存够了但单请求首 token 更慢 | 小 batch 下反量化 kernel 开销占主导 | 只在吞吐瓶颈处用量化，别为了显存盲目上 |

## 9. 「推理性更好」的真实来源：test-time compute（测试期计算）

回到最初的提问。如果你观察到「上了 vLLM 之后模型答题变准了」，那多半不是错觉，但归因错了。真正发生的事有四层：

**第一层：上下文变长了。** PagedAttention 让 KV Cache 的显存效率提升一个量级，你能承受的 `max_model_len` 随之变大。上下文变长意味着可以塞进更多示例、更完整的文档、更长的历史对话——而 in-context learning（上下文学习）的效果对示例数量和质量高度敏感。这一步确实会让准确率提升，但提升来自「喂了更多信息」，不来自引擎。

**第二层：多路采样变便宜了。** 这是最关键的一层。Self-Consistency（自洽性）的做法是：同一道题采样多条思维链，对最终答案做多数投票。论文在 LaMDA-137B 上的实测是 MultiArith **+23.9** 个百分点、SVAMP **+14.4** 个百分点，AddSub / ASDiv / AQuA / GSM8K 大约都在 **+10** 个百分点量级；在 PaLM-540B 上，GSM8K 从 **56.5%** 提到 **74.4%**。

这条曲线的成本是线性的：采 8 条就要付 8 条的钱。而 vLLM 把单条成本压到原来的 1/2 到 1/4，等于同样预算能采 2 到 4 倍的路数。**reasoning 的提升来自采样路数，vLLM 只负责让这个路数付得起。**

**第三层：显存省下来就能开更大的 batch。** batch 越大，GPU 的矩阵乘越接近理论算力，单位 token 成本继续下降。这一层是纯粹的规模效应。

**第四层：更长的输出不再被系统卡死。** 思维链的本质是「用更多 token 换更准的答案」。引擎扛不住长输出，产品侧就只能把 `max_tokens` 压到 512，模型被强制在没想清楚时给答案。chunked prefill 加上连续批处理让长输出不再是系统风险，产品才敢放开上限。

四层叠起来，就是「vLLM 让大模型推理性更好」这个说法的真实来源。它是**间接因果**，中间隔着「成本」这一环。

> 💡 一句话记法：vLLM 不提高模型的智商，它降低「让模型多想几遍」的价格。

## 10. 三个常见误解（Three Misconceptions）

**误解一：vLLM 能提升模型能力。** 不能。同一份权重、同一个 prompt、`temperature=0`，vLLM 的输出和 HuggingFace `transformers` 逐 token 一致（数值上可能有极小浮点差异）。能力由权重决定，vLLM 不参与。

**误解二：vLLM 只是「快一点的 transformers」。** 差距不是常数倍，而是随负载形态变化。低并发、短序列、单请求场景下，vLLM 甚至可能比裸 `transformers` 慢一点——调度和 block 管理有固定开销。它的优势在高并发、变长序列、前缀重复这三类负载上。

**误解三：开量化能白拿性能。** 量化（FP8、INT8、AWQ、GPTQ 等）用精度换显存和带宽，在**大 batch 的吞吐瓶颈**处收益最明显；小 batch 下反量化 kernel 的固定开销可能让首 token 延迟变差。保留这条而不是删掉，理由见第 8 章表格最后一行——它是真实存在的负收益场景，不该被「量化=加速」的简化叙事盖掉。

顺带说清几个容易和主线混淆的能力：投机解码（speculative decoding）用小模型草稿 + 大模型校验，减少 decode 步数；分离式 prefill/decode（disaggregated P/D）把两个阶段放到不同机器上各自按最优配比扩容；张量并行 / 流水线并行（TP / PP）解决单卡装不下的问题。它们的共同点是**都不改变模型输出分布**（投机解码在数学上等价），只改变跑得多快、多便宜。

---

**参考资料：**

- [vLLM 官方文档首页 -- vLLM Docs](https://docs.vllm.ai/en/stable/index.html)
- [Efficient Memory Management for Large Language Model Serving with PagedAttention -- SOSP 2023，DOI: 10.1145/3600006.3613165](https://doi.org/10.1145/3600006.3613165) ⭐值得阅读
- [vLLM: Easy, Fast, and Cheap LLM Serving with PagedAttention -- vLLM Blog](https://blog.vllm.ai/2023/06/20/vllm.html)
- [Inside vLLM: Anatomy of a High-Throughput LLM Inference System -- vLLM Blog](https://vllm-project.github.io/2025/09/05/anatomy-of-vllm.html) ⭐值得阅读
- [Achieve 23x LLM Inference Throughput & Reduce p50 Latency -- Anyscale Blog](https://www.anyscale.com/blog/continuous-batching-llm-inference)
- [Orca: A Distributed Serving System for Transformer-Based Generative Models -- USENIX OSDI '22](https://www.usenix.org/conference/osdi22/presentation/yu)
- [Self-Consistency Improves Chain of Thought Reasoning in Language Models -- arXiv，DOI: 10.48550/arXiv.2203.11171](https://doi.org/10.48550/arXiv.2203.11171) ⭐值得阅读
- [Jenga: Effective Memory Management for Serving LLM with Heterogeneity -- arXiv，DOI: 10.48550/arXiv.2503.18292](https://doi.org/10.48550/arXiv.2503.18292)
- [vLLM V1 User Guide -- vLLM Docs](https://docs.vllm.ai/en/latest/usage/v1_guide.html)
- [Automatic Prefix Caching 设计文档 -- vLLM GitHub](https://docs.vllm.ai/en/latest/design/prefix_caching.html)
- [PagedAttention and vLLM -- Neel Mishra](https://neelmishra.github.io/blog/mlops/llm-inference/paged-attention.html)
- [vllm-project/vllm -- GitHub](https://github.com/vllm-project/vllm)

**最后更新时间**：2026-10-28

瓶颈在 GPU 利用率和单位 token 成本时，vLLM 值得上；瓶颈在模型本身答不对时，换模型、补示例、加自洽性采样才是解法，vLLM 只负责让最后一项变得便宜。

本专栏《LLM 大模型技术专栏》从 Transformer 注意力机制一路讲到推理引擎、RAG 与 Agent 落地，每篇都配一段可直接运行的代码，每周更新一篇。想按顺序读完，可在专栏页订阅。

