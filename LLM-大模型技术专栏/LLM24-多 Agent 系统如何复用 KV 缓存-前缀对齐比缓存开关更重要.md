# 多 Agent 系统如何复用 KV 缓存：前缀对齐比缓存开关更重要

## 1. 先给结论：缓存省的是 prefill，不是 decode

先说最容易误解的一点：prefix caching（前缀缓存）优化的是 prefill（预填充）阶段，不是 decode（解码）阶段。

一次推理通常分两段。prefill 把整段输入 prompt 一次性喂进模型，算出每个 token 的 KV cache（键值缓存）；decode 再基于这份缓存逐个吐出新 token。如果新请求的开头和之前某个请求完全一样，那段缓存直接复用，不用重算。vLLM 官方文档写得很明确：Automatic Prefix Caching（自动前缀缓存）只减少 prefilling 阶段的时间，不减少生成新 token 的时间。具体行为以对应版本官方文档为准。

收益因此集中在 TTFT（首 token 延迟），也就是按下回车后等第一个字的时间。后面吐字快不快，取决于 decode。

多 agent 恰好是理想场景：十个 agent 共享同一套 system prompt（系统提示词）和 tool schema（工具定义），前面几千 token 理论上只该算一次。但现实常是「缓存开了，命中率接近零」。问题不在开关，在前缀没对齐。

## 2. KV cache 到底是什么

KV cache 是把注意力算过的中间结果存下来，避免下一轮重复算。

Transformer 每生成一个 token，都要让当前 token 去「看」前面所有 token，并产生 K/V 两组向量。没有缓存，生成第 100 个 token 要把前 99 个重算；有缓存，前 99 份直接读，只算新的一个。代价是显存：序列越长、层数越多、并发越高，占用越大。

在 vLLM 里，缓存不按请求存，而是切成固定大小的 block（块）做哈希去重。哈希输入包括父 block 哈希、本 block 的 token，以及额外标识，例如 LoRA ID、多模态输入的哈希、多租户隔离用的 cache salt（缓存盐）。只有完整 block 会被缓存，实现细节以对应版本官方文档为准。

看一个最小示意：

```
请求 A: [系统提示 2000 token][工具定义 800 token][用户问题 A]
请求 B: [系统提示 2000 token][工具定义 800 token][用户问题 B]
                            └──── 前 2800 token 完全一致 ────┘
```

如果这 2800 个 token 一个不差，B 的 prefill 就只算后面的问题部分。差一个字符，后面全部作废。

## 3. 前缀缓存的命中条件：从第一个 token 开始就必须一致

命中条件只有一句话：从第一个 token 开始，逐 token 完全一致。不是语义相似，是 token id 序列一模一样。

由此有三个约束。

第一，比对是前缀式的。新请求从第 0 个 token 开始比，比到第一个不同就停。差异出现在第 3000 个 token，前 2999 个仍可复用，之后全部重算。

第二，复用有 block 粒度。只有完整命中的 block 才能整体搬走，结尾不满一块的部分仍要 prefill，所以收益是阶梯式的。

第三，哈希是链式的。一个 block 的哈希包含父 block 哈希，父变了子全变。开头放一个时间戳杀伤力大，就是因为它污染了整条链。

SGLang 用 RadixAttention（基数树注意力）维护一棵前缀树，多个生成调用共享树节点，本质仍是从根匹配；vLLM 则按 block 哈希管理。两套实现不同，判定条件相同，具体以对应版本官方文档为准。

还有一个隐形杀手是模板。换行、空格、参数顺序、序列化编码变了，文本看着一样，token 已经不同。

## 4. 多 agent 场景里，前缀通常断在哪

多 agent 的前缀不是随机断的，而是有固定的几个高发位置。

以常见的托管 API 为例，缓存读取顺序是 tools、system、messages，也就是工具定义在系统提示之前。这意味着工具定义改一个字，后面的 system prompt 缓存一起作废。具体顺序以对应版本官方文档为准。

| 前缀场景 | 是否命中 | 原因 |
| --- | --- | --- |
| 所有 agent 共用同一段 system prompt，工具列表顺序固定 | 会命中 | 从第 0 个 token 起完全一致 |
| system prompt 开头拼接「当前时间：2026-10-22 09:03」 | 不会命中 | 第一个 block 就不同，哈希链整条失效 |
| system prompt 开头拼接 user_id 或 session_id | 不会命中 | 每个用户、每个会话都是新前缀 |
| 工具定义用字典动态序列化，键顺序不稳定 | 不会命中 | JSON 文本不同，token 序列随之不同 |
| 共享段在前，角色描述追加在末尾 | 会部分命中 | 共享段仍可复用，只重算尾部 |
| 角色描述放在最前面，每个 agent 各不相同 | 不会命中 | 差异出现在最靠前的位置，后续全部重算 |
| 多轮对话只追加新消息，不改历史 | 会命中 | 历史前缀不变，只新增尾部 |
| 每轮把工具列表按相关度重新排序 | 不会命中 | 工具段顺序变化，system 与 messages 缓存全部失效 |

四类断点按杀伤力排序：动态字段置顶最致命，工具顺序漂移其次，角色描述位置第三，模板差异最隐蔽。

角色描述最容易被忽视。很多实现把角色设定放在最前面，后面才拼共享的工具说明，结果每个 agent 从第 1 个 token 就分道扬镳。正确做法相反：先共享，后差异。

工具顺序更隐蔽。同一批工具用不同的字典构造方式序列化，键顺序可能不同；人看着一样，tokenizer 看到的是两段文本。

## 5. 四条前缀对齐规则

**规则一：稳定内容前置，差异内容后置。** 把共用内容按「最稳定 → 最易变」排序：基础 system prompt、工具定义、领域知识、角色描述、用户输入。角色描述哪怕每个 agent 不同，也放共享段之后。这一条能把「完全没命中」变成「至少命中前几千 token」。

**规则二：工具定义固定顺序、固定序列化。** 工具按稳定键排序，比如工具名；schema 统一走同一个序列化函数，固定键顺序与编码。不依赖运行时字典顺序，也不在不同服务里各写一套 `json.dumps`。

**规则三：模板化拼接，禁止散落的字符串加法。** 所有 prompt 由同一个模板函数产出，预留固定插槽；动态字段统一注入末尾的 user message。模板改动走版本号，避免灰度期新旧前缀混跑。

**规则四：共享块版本化与显式缓存边界。** 共享 prompt 一变就当作不兼容升级：新版本用新前缀，旧版本短期保留，不要让两版交替出现。框架支持显式缓存断点时，把断点打在共享段末尾。

四条规则的共同点是：都在改「字符串怎么拼」，而不是「缓存怎么开」。

## 6. 命中率怎么观测与验证

「我感觉开了」不算观测。至少要回答三个问题：缓存有没有被查询、命中了多少、省了多少。

以 vLLM 的 V1 引擎为例，`/metrics` 端点暴露两组关键计数器：`vllm:prefix_cache_queries` 记录查询次数，`vllm:prefix_cache_hits` 记录命中次数，两者相除就是命中率。再看 `vllm:kv_cache_usage_perc` 判断占用是否长期逼近上限，`vllm:num_preemptions_total` 判断是否因显存不足发生抢占。指标名称与语义以对应版本官方文档为准。

有了指标，排查顺序可以固定下来：

1. 先确认计数器在增长。`prefix_cache_queries` 一直为 0，说明请求没走缓存路径，先查配置。
2. 再看命中率是否稳定。忽高忽低通常意味着前缀在变，比如灰度期两套模板并存。
3. 抽样比对真实前缀。把拼装后的 prompt 前 N 个 token 打日志或算哈希，直接看到第几个 token 分叉。
4. 对照第 5 节的四条规则逐项检查。
5. 最后才怀疑容量。命中率随流量上升而下降，且 `kv_cache_usage_perc` 长期接近上限，问题在淘汰。

只看平均 TTFT 是常见误区。TTFT 受排队、batch 组成、输入长度共同影响，缓存只是变量之一。验证缓存是否生效，命中率比延迟更直接。

## 7. 显存与容量的真实代价

前缀缓存不是白拿的，它吃的就是 KV cache 那块显存，而这块显存同时在养着正在跑的请求。

框架初始化时把可用显存切成一池 block，用 free queue（空闲队列）管理。请求来了就分配，引用计数归零后归还；队列头部是最久未使用的 block，也就是 LRU（Least Recently Used，最近最少使用）淘汰的对象。被淘汰的 block 会从缓存索引里摘掉，下次只能重新 prefill。流程细节以对应版本官方文档为准。

由此产生一个反直觉现象：容量不足时，缓存开得越久，命中率反而可能下降。

原因是竞争。一条长前缀刚算完进缓存，一批新请求涌进来要 block，free queue 不够就把它淘汰；下一批同前缀请求到达时缓存已没，只能再算一遍。流量越大、前缀越长，抖动越明显。

另一个权衡在并发。缓存占用越多，能同时容纳的请求越少，batch 变小，decode 吞吐下降。缓存优化 prefill，牺牲的是 decode 的空间。长输入短输出划算，短输入长输出收益有限。

多租户和 LoRA 还有两个约束：LoRA ID 会进入 block 哈希，同一段 prompt 挂不同 adapter（适配器）不能共享；多租户常用 cache salt 做隔离，salt 不同也视为不同前缀。这是正确性要求，不是 bug。

## 8. 一份可照抄的 prompt 拼装模板

下面这段是伪代码，重点是拼装顺序，不绑定具体框架的 SDK。换成任何推理框架，结构都成立。

```python
# 共享前缀版本号：共享内容一变就加一，避免新旧模板混跑
SHARED_PREFIX_VERSION = "v3"

# 共享系统提示：来自只读模板文件，禁止运行时拼时间、用户 ID
SHARED_SYSTEM = render_template("system_base.md")

def build_agent_request(agent, user_input, now, request_id):
    # 1) 工具按 name 排序，再固定序列化，保证跨进程 token 一致
    tools = sorted(agent.tools, key=lambda t: t.name)
    tools_payload = stable_json(tools)

    # 2) 共享段在前，角色差异接尾部，分叉点尽量靠后
    system_content = SHARED_SYSTEM + tools_payload + agent.role_prompt
    messages = [{"role": "system", "content": system_content}]

    # 3) 动态字段全部塞进最后一条 user 消息，绝不进入 system 前缀
    messages.append({
        "role": "user",
        "content": f"[request_id={request_id}][ts={now}]\n{user_input}",
    })

    # 4) 带版本号，便于日志里按前缀版本统计命中率
    return {"prefix_version": SHARED_PREFIX_VERSION, "messages": messages}

def stable_json(obj):
    # 固定键顺序、分隔符与编码，避免序列化差异导致 token 漂移
    return json.dumps(obj, ensure_ascii=False, sort_keys=True, separators=(",", ":"))
```

这段代码有三个校验点值得单独测：把 `agent.role_prompt` 换成空字符串，命中率应该上升；把 `sorted` 去掉，命中率应该下降；把 `now` 挪进 `system_content`，命中率应该归零。三个实验做完，前缀对齐就不再是概念，而是可复现的现象。

## 9. 小结：把缓存当成结构设计问题，而不是开关问题

回到开头：prefix caching 省的是 prefill，不是 decode。它不会让模型变聪明，也不会让吐字变快，只会让重复的开头不再重复计算。

多 agent 天然适合它，但天然不等于自动。共享 system prompt 只是「有机会命中」；能不能命中，取决于拼装顺序、工具序列化、动态字段位置这些看起来和推理无关的工程细节。

落地顺序建议：先看 `prefix_cache_queries` 与 `prefix_cache_hits` 确认真实命中率，再做一次前缀审计找出第一个分叉点，最后才去调容量。反过来做，通常是在用显存掩盖结构问题。

把前缀对齐当成一条代码规范，而不是一次性能调优，命中率才会稳定。

---

**参考资料：**

- [Automatic Prefix Caching -- vLLM Docs](https://docs.vllm.ai/en/latest/features/automatic_prefix_caching.html)
- [Automatic Prefix Caching Design -- vLLM Docs](https://docs.vllm.ai/en/latest/design/prefix_caching.html)
- [Metrics -- vLLM Docs](https://docs.vllm.ai/en/latest/design/metrics.html)
- [SGLang: Efficient Execution of Structured Language Model Programs -- LMSYS Org](https://lmsys.org/blog/2024-01-17-sglang/)
- [Prompt caching -- Anthropic Docs](https://docs.anthropic.com/en/docs/build-with-claude/prompt-caching)

**最后更新时间**：2026-10-22
