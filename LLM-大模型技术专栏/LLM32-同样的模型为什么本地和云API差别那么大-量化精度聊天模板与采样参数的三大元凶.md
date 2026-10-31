# 同样的模型，为什么本地和云 API 差别那么大：量化精度、聊天模板与采样参数的三大元凶

> **核心结论**：同一个模型，本地跑和云 API 调用效果天差地别，多半不是模型不行，而是三件最容易被忽略的事没对齐——本地为了省显存做了**量化**（int4 精度损失是头号元凶）、**聊天模板**用错导致模型把对话当成一坨文本、**采样参数**不同让输出气质完全不同。把这三层对齐，差别立刻缩小大半。

## 目录

- 1. 一句话结论：差别不在模型，在「精度 + 模板 + 参数」
- 2. 第一层：量化精度——本地最大的坑，也是最大元凶
- 3. 第二层：聊天模板（chat template）——模型当它是对话，你却喂它一坨文本
- 4. 第三层：采样参数（sampling parameters）——temperature / top_p 不同，输出气质就不同
- 5. 第四层：上下文被截断——显存吃紧时，KV Cache 先被挤掉
- 6. 可运行的完整示例：同一模型，跑本地和云端各一份
- 7. 对照表：症状 → 原因 → 解法
- 8. 什么时候本地能追上云、什么时候永远追不上
- 9. 判断收尾

## 1. 一句话结论：差别不在模型，在「精度 + 模板 + 参数」

很多人拿到同一个开源模型，本地一跑发现「怎么这么笨」，转头去调云 API 又觉得「哇好聪明」，于是怀疑是不是被厂商阉割了。**其实模型权重是同一套**，差别在你「怎么喂它」和「怎么跑它」。

可以打个比喻 🎭：同一个厨子（模型权重），你给他**真铁锅**（bf16 高精度）还是**塑料锅**（int4 量化），炒的菜火候完全不同；你给他**标准菜单**（正确的聊天模板）还是**乱写的小纸条**（模板错位），他理解的意思也完全不同；你再调一下**火候**（temperature / top_p），菜的「气质」又能变。

所以排查顺序应当是：**先看精度，再看模板，最后调参数**。下面逐层拆开。

## 2. 第一层：量化精度（quantization）——本地最大的坑，也是最大元凶

**这是本地和云端差别最大、最容易被忽略的一层。**

云 API 通常用 **BF16 / FP16**（16 位浮点）甚至 **FP8** 高精度权重在跑，精度损失几乎为零。而你本地部署为了塞进显存，几乎一定会做**量化**——把权重从 16 位压到 8 位、4 位，甚至 3 位。每压一档，精度就掉一截。

代价有多大？可复算的数据摆在这里：

- **INT8 基本无损**：Llama 3 8B 量化到 FP8 后，MMLU 仍保留 **99.2%** 的基线准确率；70B 保留 **99.6%**。8 位几乎感知不到退化。
- **INT4 明显掉**：GSM8K（数学推理）在 INT4 下准确率**掉 9%–18%**，而 MMLU（事实知识）只掉 **1%–3%**。数学推理是最敏感的任务。
- **3 位更狠**：最激进的 3-bit 配置省空间最多，但退化也最大。
- **长上下文更糟**：4-bit 量化在输入 context 变长时会**逐渐恶化**，英文以外语言掉得更明显；8-bit 则基本保持。

这些数字合起来说明一个关键规律：**量化对「会算的数」伤害大，对「纯背诵」伤害小。** 所以你本地跑数学题、写代码、做推理，往往会觉得「变笨了」；而问常识、翻译，又觉得「还行」。

> **量化精度**（quantization）：把模型权重从高精度浮点压缩到低位宽（8/4/3 bit）以省显存、提速度的技术。

补充一个「精度」维度的次要点：即便同是 16 位，**推理引擎**（vLLM、llama.cpp、TensorRT）在算子实现、KV Cache 管理上也有差异，但比起量化这一层，引擎差异通常是次要的。

参考资料：
- [Post-Training Quantization of LLMs with NVIDIA NeMo -- NVIDIA Technical Blog](https://developer.nvidia.com/blog/post-training-quantization-of-llms-with-nvidia-nemo-and-nvidia-tensorrt-model-optimizer/) 
- [“Give Me BF16 or Give Me Death”? -- arXiv](https://doi.org/10.48550/arXiv.2411.02355)
- [Does quantization affect models’ performance on long-context tasks? -- arXiv](https://doi.org/10.48550/arXiv.2505.20276)
- [Which Quantization Should I Use? LLaMA.cpp Quantization -- arXiv](https://doi.org/10.48550/arXiv.2601.14277)

## 3. 第二层：聊天模板（chat template）——模型当它是对话，你却喂它一坨文本

很多人本地部署时直接用 API 厂商给的原始格式，结果模型输出前言不搭后语。这往往不是模型笨，而是**聊天模板错了**。

每个模型家族都有自己的 `chat template`——它规定了 `system`、`user`、`assistant` 消息之间的分隔符和特殊 token（如 `<|im_start|>`、`[INST]`、`<|start_header_id|>` 等）。模板就是模型的「语法书」，告诉它「哪段是系统指令、哪段是用户问题、哪段是我自己的回答」。

**如果模板错了**，模型会把整段对话当成一堆纯文本，分不清角色边界，自然就「装傻」。这就像你给一个懂中文的人递上去一段没有标点的文字，让他复述，他也能复述，但要他「理解并回答」就很费劲。

所以本地部署时，**一定要加载模型官方推荐的 chat template**——HuggingFace Transformers 的 `apply_chat_template`、llama.cpp 的 `--chat-template`、Ollama 的 Modelfile 里 `TEMPLATE`，都是用对了才能对齐云端效果的关键一步。

参考资料：
- [Model Outputs Garbage: Debugging Bad Generations -- insiderllm](https://insiderllm.com/pdfs/model-outputs-garbage-debug.pdf)

## 4. 第三层：采样参数（sampling parameters）——temperature / top_p 不同，输出气质就不同

即便精度和模板都对，云端和本地**输出会飘**，往往是采样参数没对齐。

- **temperature（温度）**：控制随机性。越高越放飞（0.8–1.0 更创意），越低越保守（0.2–0.3 更稳定）。云 API 常默认 0.7 左右，你本地若是默认 1.0，就会觉得「之前挺稳的，怎么本地开始胡说了」。
- **top_p（核采样）**：只在累计概率达到 p 的最小 token 集合里采样。配合 temperature 一起用。
- **seed（随机种子）**：固定种子能让输出可复现。云 API 往往不保证 seed 生效，本地可以设，这也是「本地每次都不一样、云端像套娃」的一大来源。

一句话：**精度决定「模型有多聪明」，采样参数决定「这聪明劲儿往哪个方向飘」。** 想要对齐，就把本地和云端的 temperature / top_p / max_tokens 设成一致，再对比。

参考资料：
- [My Local LLM Setup: One Model, Many Personalities -- d3v0ps.cloud](https://d3v0ps.cloud/posts/2026/05/my-local-llm-setup/)
- [LLM 重复回答？设置 seed / temperature / top_p -- AiManual](https://ai-manual.ru/article/vasha-lokalnaya-llm-zastryala-na-povtorenii-vskryvaem-seed-temperature-i-topp/)

## 5. 第四层：上下文被截断——显存吃紧时，KV Cache 先被挤掉

这一层很多人踩了却意识不到。云端 API 的 context 通常能撑到 128k、200k，而你本地显存有限，**KV Cache（键值缓存）**是吃显存的大户。

当显存不够时，推理框架可能自动**截断超长上下文**，或者 KV Cache 存不下导致前面讲过的内容「忘掉」。于是你需要「长上下文连贯推理」的任务（多轮对话、长文档总结）在本地就垮了，而云端毫发无损。

判断方法：本地跑长文本时，看看**实际生效的 context 长度**，以及是否触发了 `max_model_len` 之类的限制。这也是「同一个模型，对话短还行、一问长就露馅」的主要原因。

参考资料：
- [Private LLM Inference on Consumer Blackwell GPUs -- arXiv](https://doi.org/10.48550/arXiv.2601.09527)

## 6. 可运行的完整示例：同一模型，跑本地和云端各一份

下面这段代码**复制粘贴就能跑**。它把本地 Ollama 和云端 API 都当作 OpenAI 兼容接口，用**完全相同的 prompt、完全相同的采样参数**去测，让你一眼看出差别在哪儿。

运行前：`pip install openai`；本地装好 Ollama 并 `ollama pull qwen2.5:7b`；云端填你的 API key。

```python
# 同一个模型身份，两个“跑法”：本地量化版 vs 云端高精度版
from openai import OpenAI

# ① 本地（Ollama 默认，qwen2.5:7b 常被量化到 int4/int8；base_url 指向本地服务）
local = OpenAI(base_url="http://localhost:11434/v1", api_key="ollama")

# ② 云端（拿同系列或同源的 API，通常是 bf16 高精度跑）
cloud = OpenAI(api_key="你的云端KEY", base_url="https://api.xxx.com/v1")

# ③ 统一 prompt：故意挑一道数学推理题，量化伤害最大的场景
messages = [
    {"role": "system", "content": "你是一个严谨的数学助手，只给结论并简述步骤。"},
    {"role": "user", "content": "一个篮子里有 3 个苹果，又放进去 5 个，再拿走 2 个，还剩几个？只答数字。"},
]

# ④ 统一采样参数（重点：本地和云端必须一致，否则对比无意义）
common = {"model": "qwen2.5:7b", "messages": messages,
          "temperature": 0.2, "top_p": 0.9, "max_tokens": 64}

print("=== 本地（量化版）===")
print(local.chat.completions.create(**common).choices[0].message.content)

print("=== 云端（高精度版）===")
print(cloud.chat.completions.create(**common).choices[0].message.content)
```

**怎么读这段代码**：它刻意把 `messages`（含 system + user）和 `temperature/top_p/max_tokens` 完全一致，只让 `base_url` 不同。如果两者差别大，你就知道问题出在**「同一个模型在下游被怎么跑」**——大概率是本地那侧做了激进的量化。你可以把 `temperature` 调高到 0.8 再跑，会看到输出的「飘」又不一样。

## 7. 对照表：症状 → 原因 → 解法

| 症状 | 原因 | 解法 |
|---|---|---|
| 本地数学/代码明显变笨，常识还行 | 量化到 INT4，数学推理最敏感 | 改用 Q8_0 / FP8，或至少 Q4_K_M；对推理任务别用太狠的量化 |
| 本地模型前言不搭后语、答非所问 | 聊天模板（chat template）用错了 | 加载模型官方 chat template（`apply_chat_template` / Modelfile `TEMPLATE`） |
| 同样 prompt，本地每次飘、云端很稳 | temperature / top_p / seed 不一致 | 把两端采样参数设成一致；本地固定 seed |
| 对话一长就「失忆」、漏前面内容 | 显存吃紧，KV Cache / context 被截断 | 调大 `max_model_len`，或减小量化位宽腾显存 |
| 本地慢、云端快，但本地是同一模型 | 引擎 + 位宽 + 批处理差异 | 用 vLLM 或 TensorRT 优化引擎，对比前先统一位宽 |
| 明明同源却连「语气」都不同 | 系统提示词在两端的默认值不同 | 每次都显式传 system prompt，不依赖平台默认 |

## 8. 什么时候本地能追上云、什么时候永远追不上

**能基本对齐的场景**：事实问答、翻译、改写、格式规整，这些 task 对 INT8 甚至 INT4 都不太敏感。你只要把聊天模板和采样参数对齐，本地就接近云端。

**永远有差距的场景**：**数学推理、多步逻辑、长上下文连贯、代码生成**——这些正是量化最敏感的「会算的数」和「要连贯」类型。本地再猛，INT4 下这类任务就是追不上云端 bf16；要么上足够贵的显卡（单卡 80GB+ 跑 bf16/FP8），要么接受量化带来的损失。

所以选型口诀：**本地图的是便宜、离线、数据不出门；云端图的是精度、稳定、长上下文。** 你到底要哪头，决定你该不该为「追上云端」去堆硬件。

## 9. 判断收尾

**判断收尾**：当你发现同一模型本地变笨，先别怪模型，按「量化精度 → 聊天模板 → 采样参数 → 上下文截断」四层排查；若你要的是数学、代码、长文这类高精度 task，别指望 INT4 本地版追上云端 bf16，该堆硬件就堆，该上云就上云。

**专栏介绍**：本专栏《LLM 大模型技术专栏》从 Transformer 注意力机制一路讲到量化部署、vLLM 推理与 Agent 落地，每篇都配一段可直接运行的代码，每周更新一篇。想按顺序读完，可在专栏页订阅。
