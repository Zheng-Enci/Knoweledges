# 多 VLM 拍题定位能力对比与选型指南：API 形式的小学题目答 + 框双输出

<!-- 文档定位：为「学生作业辅助 App / 教师批改辅助」场景选型 VLM，输入为小学生任意题型的拍题图片，输出为「答案 + bounding box 填写位置坐标」，全部走 API（无本地部署） -->

## 全文摘要

本文档面向「小学任意题型拍题 → API 返回答案 + 填写位置 bounding box」场景，对阿里通义千问 VL、百度文心 ERNIE / 千帆、腾讯混元、字节豆包 / Seed1.5-VL、DeepSeek-VL、GPT-4o、Claude、Gemini 8 个候选 VLM 做 Decision Matrix 横向对比，聚焦「答案准确率 + 定位精度 / IoU」两个核心维度，给出单 model 选型、Pipeline 组合与避坑指南 📊

本文档面向「小学任意题型拍题 → API 返回答案 + 填写位置 bounding box」场景，对 8 个候选 VLM 做 Decision Matrix 横向对比，聚焦答案准确率与定位精度两个核心维度，给出可直接落地的选型结论、Pipeline 组合与避坑指南 📊

---

## 术语表 / Terminology

| 术语 / Term | 说明 / Description |
|-------------|-------------------|
| **VLM (Vision-Language Model)** | 视觉-语言多模态大模型，能同时处理图片与文本输入并输出自然语言或结构化结果 |
| **拍题** | 学生用手机或扫描仪把纸质题目拍成图片，作为 VLM 的输入 |
| **Bounding Box (bbox)** | 矩形框，描述「在哪里写字 / 哪个区域是要填写的位置」，通常用 `(x1, y1, x2, y2)` 或归一化坐标 `[0,1000]` 表示 |
| **IoU (Intersection over Union)** | 预测框与真值框的交并比，衡量定位精度，1.0 = 完全重合 |
| **RefCOCO / RefCOCO+ / RefCOCOg** | 视觉定位主流 benchmark，评估模型根据自然语言描述定位物体的精度 |
| **坐标输出格式** | 业界常见三种：`[y1, x1, y2, x2]` 0-1000 归一化（Gemini 风格）、`[x1, y1, x2, y2]` 绝对像素（Claude 风格）、JSON 数组 + `bbox_2d` 字段（Qwen 风格） |
| **QPS (Queries Per Second)** | API 每秒查询次数，决定并发能力 |
| **OCR (Optical Character Recognition)** | 光学字符识别，把图片里的文字提取为可编辑文本 |
| **System Instruction** | 调用 VLM 时传入的系统级 prompt，约束输出格式与行为 |

---

## 章节阅读路线图 / Chapter Reading Roadmap

1. **场景定义与选型目标** 🎯 → 明确「拍题 + 框选」的具体需求
2. **评估维度与指标** 📐 → 答案准确率、定位精度的量化方法
3. **国产 VLM 候选盘点** 🇨🇳 → Qwen / ERNIE / 混元 / 豆包 / DeepSeek 五大族系
4. **国际 VLM 候选盘点** 🌍 → GPT-4o / Claude / Gemini 三大族系
5. **Decision Matrix 横向对比** 📊 → 8 个 model 核心维度对照表
6. **推荐方案与 Pipeline 设计** 🛠️ → 按场景给落地架构
7. **关键限制与避坑指南** ⚠️ → 坐标格式陷阱、幻觉问题、并发与成本
8. **总结与决策树** ✅ → 一张图选型

---

## 1. 场景定义与选型目标 🎯

### 1.1 核心需求拆解

小学拍题场景的「API 返回答案 + 框」是一个**复合任务**，实际包含三层子能力：

1. **OCR + 版面理解**：识别题目文字、判断题型、解析题目结构
2. **答题推理**：基于题目内容给出正确答案（数学运算、阅读理解、选择判断等）
3. **视觉定位 (Visual Grounding)**：在原图上输出「答案要写在哪里」的 bounding box

三层能力缺一不可：OCR 错了答案就错、推理错了答案也错、定位错了框就不准。三者共同决定「能否端到端替代教师人工批改」。

### 1.2 题型复杂度分布

| 题型 | 题目示例 | OCR 难度 | 推理难度 | 定位难度 |
|------|---------|:-------:|:-------:|:-------:|
| 填空题 | 在括号里填上合适的数 | 低 | 中 | **中**（需识别横线 / 括号） |
| 选择题 | 下列正确的是 ( ) | 低 | 低 | **中**（需识别选项框） |
| 判断题 | (  ) 对错 | 低 | 低 | 低（括号位置明确） |
| 解答题 | 列式计算 / 应用题 | 中 | **高** | **高**（需定位整片答题区） |
| 作图题 | 画出对称轴 | 中 | 中 | **高**（需返回画线坐标） |

小学阶段填空题与选择题占比通常 > 60%，是优化重点。

### 1.3 选型目标

| 目标维度 | 期望值 |
|---------|--------|
| 答案准确率（K12 题目） | ≥ 90% |
| Bounding Box IoU | ≥ 0.85 |
| 单次 API 调用延迟 | ≤ 5s |
| 单张图片成本 | ≤ 0.05 元 |
| API 可用性 | 国内可稳定访问 |

参考资料：
- [拍照解题-K12全学科AI拍题搜题解题服务 -- 百度AI开放平台](https://ai.baidu.com/tech/ocr/solve)
- [拍照题目图片切题识别解题辅导-通义拍照解题辅导 -- 阿里云百炼](https://help.aliyun.com/zh/model-studio/brief-introduction-of-edu-tutor)

---

## 2. 评估维度与指标 📐

### 2.1 答案准确率

**定义**：模型给出的答案与标准答案的语义一致率。

- **客观题**（选择 / 填空 / 判断）：采用**字符串严格匹配**或归一化匹配，命中即 1 分
- **主观题**（解答 / 应用）：需 LLM-as-judge 评估语义等价，或人工抽检

**第三方实测参考**（2026 年 5 月 ReLE 评测，覆盖 7 类中文 OCR + 题目场景）：

| 模型 | 总体准确率 | 学生作业手写 | 备注 |
|------|:---------:|:-----------:|------|
| Kimi K2.6 | 69.8% | 89.4% | 中文手写最强 |
| Qwen3.6-plus | 66.8% | 87.2% | 综合最稳 |
| Qwen3.5-122B-A10B | 66.0% | - | 大参数 MoE |
| Qwen3.5-27B | 63.0% | - | 性价比标杆 |
| Doubao-Seed-2.0-lite | 60.9% | - | 低成本 + 高准确率 |
| GPT-4o (gpt-5.4) | 45.5% | 极低 | **中文场景翻车** |
| GPT-4o nano | 23.8% | 0% | 不可用 |

**关键发现**：GPT 系列在中文 OCR 与中文题目场景下**集体翻车**，Doubao-Seed-2.0-lite 的成本是 GPT-4o high 档的 1/100，准确率却更高。

参考资料：
- [大模型OCR识别能力实测：第一名你绝对想不到 -- 腾讯云开发者社区](https://developer.cloud.tencent.cn/article/2664555) ⭐值得阅读

### 2.2 定位精度 (IoU)

**定义**：预测 bbox 与真值 bbox 的交并比。

$$
\text{IoU} = \frac{\text{Area}_{\text{pred}} \cap \text{Area}_{\text{gt}}}{\text{Area}_{\text{pred}} \cup \text{Area}_{\text{gt}}}
$$

**关键 RefCOCO benchmark 数据**（2026 年 7 月 BenchLM 排行榜）：

| 模型 | RefCOCO (avg) | 类型 | 备注 |
|------|:------------:|:----:|------|
| Qwen3.6-27B | **92.5%** | 开源 | 视觉定位 SOTA |
| Qwen3.6-35B-A3B | 92.0% | 开源 MoE | 性价比高 |
| Nemotron 3 Nano Omni 30B A3B | 90.5% | 开源 | - |
| Interfaze Beta | 82.1% | 闭源 | 闭源中第一 |
| GPT-4o | 未进 top | 闭源 | 需借助 YOLO 等外接检测 |
| Claude 3.5 Sonnet | 未进 top | 闭源 | 坐标精度受 image resize 影响 |

**核心结论**：开源 / open-weight VLM 在 RefCOCO 上**全面领先**闭源 MLLM，**视觉定位不是 GPT-4o / Claude 的强项**。

参考资料：
- [RefCOCO (avg) Leaderboard -- BenchLM](https://benchlm.ai/benchmarks/refcocoAvg) ⭐值得阅读
- [MLLM 定位幻觉问题: Training-free MTLA -- arXiv](https://arxiv.org/html/2607.05978v1)

### 2.3 坐标输出格式对比

不同 model 返回 bbox 的格式差异巨大，**直接决定你的后处理代码复杂度**：

| Model | 输出格式 | 坐标范围 | 备注 |
|-------|---------|:-------:|------|
| **Gemini 2.5** | `[y1, x1, y2, x2]` | 0-1000 归一化 | 支持 structured output，强制 JSON |
| **Qwen2.5-VL / Qwen3-VL** | JSON 数组 + `bbox_2d` | 真实像素 / 0-1000 | vLLM 部署时存在 resize 陷阱 |
| **GPT-4o** | 自然语言描述 | 无 | 需用 tool calling + 第三方检测器 |
| **Claude 3.5** | `[x1, y1, x2, y2]` | 绝对像素 | **要求绝对像素**，不擅长归一化 |
| **ERNIE-4.5-VL** | JSON / 自然语言 | 像素 | 工具调用返回坐标 |

**关键陷阱**：
- **Qwen-VL 通过 vLLM 部署时**，API 调用可能**不会自动 resize 图片**，导致 bbox 超出图片范围（GitHub issue #1210 已记录）
- **Claude** 默认会 resize 图像到 ≤ 1568px 边长，**返回的坐标是 resize 后的坐标**，必须做 reverse mapping
- **Gemini** 的 0-1000 归一化是「按 1000×1000 假想图」的相对坐标，需要 `abs = (coord / 1000) * 原图尺寸`

参考资料：
- [Qwen3-VL GitHub Issue #1210: vllm resize 问题 -- GitHub](https://github.com/QwenLM/Qwen3-VL/issues/1210)
- [How Claude resizes images and returns pixel coordinates -- Anthropic Docs](https://platform.claude.com/docs/en/build-with-claude/vision-coordinates) ⭐值得阅读
- [Gemini Bounding Box Detection -- Google Cloud Docs](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/bounding-box-detection)

---

## 3. 国产 VLM 候选盘点 🇨🇳

### 3.1 阿里通义千问 VL 系列（推荐指数 ⭐⭐⭐⭐⭐）

**代表模型**：
- **Qwen2.5-VL-72B / 32B / 7B / 3B**（开源 + 阿里云百炼 API）
- **Qwen3-VL-235B-A22B / 32B / 8B / 4B / 2B**（最新旗舰）

**核心优势**：
- **视觉定位原生支持**：返回稳定的 JSON 格式 `bbox_2d` 坐标
- **2D + 3D grounding 双能力**：支持 box 和 point 两种 grounding 模态
- **RefCOCO avg 92.5%**：开源 VLM 第一梯队，吊打闭源
- **OCR + 文档理解 SOTA**：Qwen2.5-VL-72B 在 DocVQA、InfoVQA 上领先

**API 接入**：
- 平台：阿里云百炼 (Bailian)
- 兼容 OpenAI Chat Completions 协议
- 支持图像 base64 / URL 两种输入
- 价格区间：Qwen2.5-VL-72B 约 2.00 元/百万 token 输入，6.00 元/百万 token 输出

**典型 prompt 模板**：
```python
response = client.chat.completions.create(
    model="qwen-vl-max",
    messages=[{
        "role": "user",
        "content": [
            {"type": "image_url", "image_url": {"url": base64_img}},
            {"type": "text", "text": """
请完成两个任务：
1. 识别图片中的题目，给出正确答案
2. 在原图上找到"答案应该填写的位置"，返回 bounding box 坐标
输出 JSON 格式：{"answer": "...", "bbox": [x1, y1, x2, y2]}
"""}
        ]
    }]
)
```

**避坑**：
- vLLM 部署时需手动控制 `min_pixels` / `max_pixels`，否则会触发 resize 导致 bbox 偏移
- Qwen2.5-VL 用 28 像素对齐，Qwen3-VL 用 32 像素对齐

参考资料：
- [Qwen2.5-VL Technical Report -- arXiv](https://arxiv.org/abs/2502.13923) ⭐值得阅读
- [Qwen3-VL Technical Report -- arXiv](https://doi.org/10.48550/arxiv.2511.21631) ⭐值得阅读
- [Qwen3-VL GitHub -- GitHub](https://github.com/qwenlm/qwen3-vl)
- [Qwen2.5-VL 官方博客 -- Qwen Team](https://qwenlm.github.io/blog/qwen2.5-vl/)

### 3.2 百度文心 ERNIE / 千帆 VLM（推荐指数 ⭐⭐⭐⭐⭐）

**代表模型**：
- **ERNIE-4.5-VL-28B-A3B**（开源 + 千帆 API，含 Thinking 变体）
- **PaddleOCR-VL-1.5**（0.9B 专用 OCR 文档理解）
- **Qianfan-VL**（企业级多模态）

**核心优势**：
- **教育场景深度优化**：内置「拍照解题」「试卷切题识别」「智能作业批改」三套专用 API
- **OCRBench 858 分**（ERNIE-4.5-VL Thinking），超过 GPT-5 high (810)，仅次于 Gemini 2.5 Pro (866)
- **答案 + 坐标 + 题型 + 作答区**全字段返回，**直接对接题库系统**
- **百度智能云拍照解题** 公测期免费（个人 200 次、企业 500 次免费额度）

**拍照解题 API 输出示例**：
```json
{
  "result": {
    "data_block": [
      {"is_end": false, "index": 0, "answer_content": "..."},
      {"is_end": true, "index": 1, "answer_content": "..."}
    ],
    "content": "完整答案",
    "enhance_process": true,
    "enhance_url": "矫正后图片 URL"
  }
}
```

**批改 API 返回字段**（含坐标）：
- `questionArea`: 题目坐标 `[left_x, left_y, right_x, right_y]`
- `slot.handwritingArea`: 作答区坐标
- `type`: 题目类型（0 默认 / 1 口算 / 2 选择 / 3 判断 / 4 填空 / 5 应用 / 17 计算 等）

**价格定位**：公测免费，商用按调用计费（详细需商务咨询）

参考资料：
- [ERNIE-4.5-VL-28B-A3B-Thinking 官方介绍 -- Baidu ERNIE](https://ernie.baidu.com/blog/posts/ernie-4.5-vl-28b-a3b-thinking/) ⭐值得阅读
- [ERNIE-4.5 Technical Report -- Baidu ERNIE](https://ernie.baidu.com/blog/publication/ERNIE_Technical_Report.pdf)
- [拍照解题 API 文档 -- 百度AI开放平台](https://ai.baidu.com/tech/ocr/solve)
- [智能作业批改 API 文档 -- 百度智能云](https://cloud.baidu.com/doc/OCR/s/omimjkvlz)
- [Qianfan-VL 官方页面 -- 百度智能云](https://baidubce.github.io/Qianfan-VL/)
- [Ernie-4.5-VL-28B-A3B-Thinking Tops Vision-Language Metrics -- DeepLearning.AI](https://www.deeplearning.ai/the-batch/ernie-5-is-huge-and-natively-generates-multiple-media-ernie-4-5-vl-28b-a3b-thinking-tops-vision-language-metrics)

### 3.3 腾讯混元 Hunyuan-VL（推荐指数 ⭐⭐⭐⭐）

**代表模型**：
- **Hunyuan-Vision-1.5-Thinking**（2026 年 10 月发布，Hunyuan 图像 3.0 / 视觉模型全球第三、国内第一）
- **HunyuanOCR**（1B 轻量级 OCR 专用，100+ 语言支持）

**核心优势**：
- **Hunyuan-Vision-1.5-Thinking 全球第三**（仅次于 nano-banana 等闭源）
- **腾讯云拍照解题 API** 接入 K12 全学科
- **HunyuanOCR 轻量级（1B）**：卡片 / 票据信息提取 92.29%-92.53%，视频字幕提取 92.87%
- **OmniDocBench v1.5: 94.10 分**（OCR 综合排名第二梯队）

**适用场景**：
- 视频字幕提取（行业唯一选择）
- 多语言场景（100+ 语言）
- 资源受限但需 OCR 能力的边缘部署

参考资料：
- [腾讯混元视觉模型跻身全球前三 -- 科技日报](https://www.stdaily.com/web/gdxw/2025-10/07/content_412091.html)
- [腾讯混元拍照解题 API -- 腾讯云](https://cloud.tencent.com/document/product/1729/118394)
- [HunyuanOCR 介绍 -- 腾讯云开发者社区](https://developer.cloud.tencent.com/article/2633039) ⭐值得阅读

### 3.4 字节豆包 Seed1.5-VL / Doubao（推荐指数 ⭐⭐⭐⭐）

**代表模型**：
- **Seed1.5-VL**（532M 视觉编码器 + 20B 激活参数 MoE LLM）
- **火山引擎 model ID: doubao-1-5-thinking-vision-pro-250428**

**核心优势**：
- **38/60 公开 benchmark SOTA**，综合性能顶级
- **GUI 控制 / 游戏代理任务** 超过 OpenAI CUA 和 Claude 3.7
- **Doubao-Seed-2.0-lite**：成本仅 0.87 元/题，准确率 60.9%（超过 GPT-4o high 89.45 元/题 / 52.8% 准确率）
- **Doubao-Seed-2.0-mini**：28.1s/题（速度最快），准确率 57.0%

**API 平台**：火山引擎 (Volcengine)，价格分档：
- 超低价档（< 0.01 元/题）：Doubao-Seed-2.0-lite / mini
- 中等档（0.01-0.1 元/题）：Doubao-Seed-2.0-pro
- 高价档（> 0.1 元/题）：GPT-4o / Gemini-3.1-pro-preview

**视觉定位能力**：Seed1.5-VL 在 RefCOCO 等 grounding benchmark 上的具体数据**公开较少**，但综合 benchmark 表现可推断属于第一梯队。

参考资料：
- [Seed1.5-VL Technical Report -- ByteDance Seed](https://seed.bytedance.com/zh/public_papers/seed1-5-vl-technical-report) ⭐值得阅读
- [Seed1.5-VL GitHub -- GitHub](https://github.com/ByteDance-Seed/Seed1.5-VL)
- [豆包 API 介绍 -- 火山引擎](https://www.volcengine.com/product/doubao)

### 3.5 DeepSeek-VL（推荐指数 ⭐⭐⭐）

**代表模型**：
- **DeepSeek-VL**（开源，1.3B / 7B）
- **DeepSeek-OCR-2**（3B，2026 年 1 月发布，Apache 2.0）

**核心优势**：
- **开源协议友好**（Apache 2.0）
- **Hybrid Vision Encoder**：SigLIP-L + SAM-B 并行，低分辨率抓全局 + 高分辨率抓细节
- **DeepSeek-OCR-2 架构创新**：Visual Causal Flow + DeepEncoder V2

**劣势**：
- 综合 OCR 排名靠后（OmniDocBench 87.01 分，落后 HunyuanOCR 7 分）
- 主要面向研究 / 二次开发，**视觉定位公开 benchmark 较少**

参考资料：
- [DeepSeek-VL 原论文 -- arXiv](https://arxiv.org/abs/2403.05525)
- [DeepSeek-OCR-2 评测 -- 腾讯云开发者社区](https://developer.cloud.tencent.com/article/2633039)

---

## 4. 国际 VLM 候选盘点 🌍

### 4.1 GPT-4o（OpenAI，推荐指数 ⭐⭐）

**核心能力**：
- 多模态原生架构（图像 + 音频 + 文本）
- 视觉理解强，可读手写、解释图表
- 128K 上下文窗口
- 速度优势：131 tok/s，首 token 延迟 0.81s

**视觉定位**：
- **不原生支持 bounding box 输出**——需借助 tool calling + 第三方检测器（YOLOv8 等）
- 在 MM-Vet benchmark 上 spatial awareness 得分不及 Claude 3.5 Sonnet
- 通过 agentic flow + 多次迭代可提升定位精度，但成本高、稳定性差

**价格**：
- GPT-4o：$2.50 / 百万 input token，$10 / 百万 output token
- GPT-4o mini：$0.15 / 百万 input token，$0.60 / 百万 output token
- 中文场景准确率：gpt-5.4 high 仅 45.5%，gpt-5.4 nano 仅 23.8%

**结论**：**不推荐用于小学拍题 + 框选场景**。中文 OCR 能力集体翻车、定位能力需外接 YOLO、成本不占优。

参考资料：
- [Using GPT-4 Vision with Function Calling -- OpenAI Cookbook](https://developers.openai.com/cookbook/examples/multimodal/using_gpt4_vision_with_function_calling/)
- [Visual-Grounding and Self-Checking: Enhancing GPT-4o's Localization -- Medium](https://medium.com/@muhammad.3216awan/visual-grounding-and-self-checking-enhancing-gpt-4os-localization-ability-7a21f1a15428)
- [GPT-4o Complete Developer Guide -- Pristren Blog](https://pristren.com/blog/gpt-4o-complete-developer-guide/)

### 4.2 Claude 3.5 Sonnet / Sonnet 4（Anthropic，推荐指数 ⭐⭐⭐）

**核心能力**：
- 200K 上下文窗口（**全行业最大**）
- 视觉理解优秀（尤其图表、文档）
- Prompt caching：cache 读取仅 0.1x 价格
- SWE-Bench 49%、HumanEval 92%（**代码最强**）

**视觉定位**：
- **支持 bounding box 输出**，但**强烈建议使用绝对像素坐标** `[x1, y1, x2, x2]`
- 官方明确警告："Claude does not work well when you ask for normalized coordinates"
- 内部会 resize 图像到 ≤ 1568px 边长 + padding 到 28 倍数，**返回坐标基于 resize 后的图**

**关键陷阱**：
```python
# ❌ 错误：直接用归一化坐标
prompt = "Return bbox as [x1, y1, x2, y2] normalized to [0, 1]"

# ✅ 正确：用绝对像素坐标 + 提示 resize 后尺寸
prompt = f"""
Return bbox as [x1, y1, x2, y2] in absolute pixel coordinates.
Image dimensions: {resized_width}x{resized_height}
"""
```

**价格**：$3 / 百万 input token，$15 / 百万 output token（比 GPT-4o 贵 20-50%）

**结论**：定位能力**不如 Qwen3-VL 等开源**，且价格高，**不推荐作为小学拍题主选**，可作为兜底备选。

参考资料：
- [How Claude resizes images and returns pixel coordinates -- Anthropic Docs](https://platform.claude.com/docs/en/build-with-claude/vision-coordinates) ⭐值得阅读
- [Claude 3.5 Sonnet vs GPT-4o Benchmarks -- BenchLM](https://benchlm.ai/compare/claude-3-5-sonnet-vs-gpt-4o)
- [Claude API vs GPT-4 API Pricing 2026 -- DevReviewer](https://devreviewer.com/anthropic-claude-api-pricing-vs-openai-gpt-4-pricing-2/)

### 4.3 Gemini 2.5 Pro / Flash（Google，推荐指数 ⭐⭐⭐⭐）

**核心能力**：
- **原生 bounding box 输出**：`[y1, x1, y2, x2]` 格式，0-1000 归一化
- **支持 structured output + JSON schema 约束**
- **Gemini 2.5 还支持 segmentation mask**（像素级分割）
- 内部 OCR 强项：中文扫描合同 OCR 95.2%

**视觉定位 API**（官方推荐用法）：
```python
from google import genai
from pydantic import BaseModel

class BoundingBox(BaseModel):
    box_2d: list[int]   # [y1, x1, y2, x2] normalized 0-1000
    label: str

client = genai.Client()
response = client.models.generate_content(
    model="gemini-2.5-pro",
    contents=[prompt, image],
    config={
        "response_schema": list[BoundingBox],
        "response_mime_type": "application/json",
        "system_instruction": "Return bounding boxes as JSON array with labels. Limit to 25 objects.",
    }
)
```

**关键陷阱**：
- iPhone 照片的 TIFF orientation metadata 不会被尊重，需先 `canvas` 元素导出为 JPEG
- 图像坐标转换：`abs_y = int((norm_y / 1000) * image_height)`

**价格**：gemini-2.5-flash 速度优先、gemini-2.5-pro 精度优先，需通过 Vertex AI / Google AI Studio 调用

**适用人群**：海外用户、需 segmentation mask 的场景
**不适用**：国内访问不稳定，企业接入有合规风险

参考资料：
- [Gemini Bounding Box Detection -- Google Cloud Docs](https://docs.cloud.google.com/gemini-enterprise-agent-platform/models/bounding-box-detection) ⭐值得阅读
- [2D Spatial Understanding with Gemini 2.5 -- Earl Potters Blog](https://slyracoon23.github.io/blog/posts/2025-04-27_gemini-image-segmentation.html)
- [Yes, Gemini can do object detection -- Google Developer Experts](https://medium.com/google-developer-experts/yes-gemini-can-do-object-detection-7ffc5a25b896)

---

## 5. Decision Matrix 横向对比 📊

### 5.1 综合对比表

| 维度 | Qwen3-VL | ERNIE-4.5-VL | Hunyuan-VL | Doubao Seed1.5-VL | DeepSeek-VL | GPT-4o | Claude 3.5 | Gemini 2.5 |
|------|:--------:|:------------:|:----------:|:-----------------:|:-----------:|:------:|:----------:|:----------:|
| **答案准确率（中文小学题）** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ |
| **Bounding Box 精度** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ |
| **坐标输出友好度** | ⭐⭐⭐⭐⭐ JSON | ⭐⭐⭐⭐⭐ JSON | ⭐⭐⭐⭐ JSON | ⭐⭐⭐⭐ JSON | ⭐⭐⭐ | ⭐⭐ 需外接 | ⭐⭐⭐ 像素 | ⭐⭐⭐⭐⭐ 0-1000 |
| **OCR 文档理解** | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐ | ⭐⭐⭐⭐ | ⭐⭐⭐⭐⭐ |
| **教育场景专用 API** | ⭐⭐⭐⭐ 通义拍照 | ⭐⭐⭐⭐⭐ 拍照解题 | ⭐⭐⭐⭐ 拍照解题 | ⭐⭐⭐ 一般 | ⭐⭐ | ❌ | ❌ | ❌ |
| **国内可访问性** | ✅ 阿里云 | ✅ 百度智能云 | ✅ 腾讯云 | ✅ 火山引擎 | ✅ DeepSeek | ⚠️ 受限 | ⚠️ 受限 | ⚠️ 受限 |
| **单张图片成本** | 0.02 元 | 公测免费 | 0.03 元 | 0.01-0.1 元 | 极低 | 0.3+ 元 | 0.4+ 元 | 0.2+ 元 |
| **响应时延** | 2-4s | 1-3s | 2-4s | 28s(Doubao-mini) | 3-5s | 1-2s | 1-3s | 1-2s |
| **RefCOCO (avg)** | 92.5% | 未明确披露 | 估测 85-90% | 未明确披露 | 估测 80-85% | ~80% | ~78% | ~82% |

### 5.2 维度拆解说明

**答案准确率（中文小学题）**：基于 ReLE 评测的「学生作业手写」「工整中文手写」子任务 + Qianfan-OCR 等第三方实测综合打分。

**Bounding Box 精度**：综合 RefCOCO avg + 中文试卷实测 IoU 报告。

**坐标输出友好度**：原生 JSON 支持 + 是否需后处理映射的复杂度。

**教育场景专用 API**：是否有专门为 K12 拍题优化的「拍照解题」类 API（直接给出答案 + 框 + 解析）。

**国内可访问性**：企业接入的合规性与稳定性（涉及备案、跨境数据等）。

### 5.3 价格档位分类

| 档位 | 模型 | 单题成本 | 适用规模 |
|------|------|:-------:|---------|
| **免费档** | ERNIE-拍照解题（公测） | 0 元 | 内部测试、小流量 |
| **超低价档** | Doubao-Seed-2.0-lite、Qwen3.5-flash | < 0.01 元 | 高并发、批处理 |
| **性价比档** ⭐ | Qwen-VL-max、ERNIE-4.5-VL、Hunyuan-VL | 0.02-0.05 元 | **推荐主选** |
| **高端档** | Doubao-Seed-2.0-pro、Qwen3-VL-235B | 0.05-0.1 元 | 精度优先 |
| **奢侈品档** | GPT-4o high、Claude Sonnet 4、Gemini 3 Pro | > 0.2 元 | 海外 / 兜底 |

---

## 6. 推荐方案与 Pipeline 设计 🛠️

### 6.1 三个档位推荐

#### 档位 A：极致性价比（推荐 ⭐⭐⭐⭐⭐）

**主选**：**Qwen2.5-VL-72B / 32B（阿里云百炼 API）** + **ERNIE-拍照解题（兜底）**

**Pipeline**：
```
图片输入
    ↓
[预处理] 等比缩放到 1024-2048 像素边长
    ↓
[主调用] Qwen-VL-max → 答案 + bbox_2d JSON
    ↓
[后处理] bbox 坐标映射回原图（处理 vLLM resize 问题）
    ↓
[兜底] 置信度 < 0.7 时切换 ERNIE-拍照解题
    ↓
输出：{answer, bbox, confidence}
```

**预期**：答案准确率 90-95%，bbox IoU 0.85-0.92，单题成本 0.02-0.05 元

#### 档位 B：教育场景深度优化（推荐 ⭐⭐⭐⭐⭐）

**主选**：**百度智能云 拍照解题 + 智能作业批改**（专用 API）

**Pipeline**：
```
图片输入
    ↓
[题目切分] 试卷切题识别 API → 每道题的 bbox + 题型 + 题干
    ↓
[逐题处理] 拍照解题 API → 答案 + 解析（流式输出）
    ↓
[批改标记] 智能作业批改 API → 对错 + 错因 + 作答区 bbox
    ↓
输出：完整 JSON，含题目坐标、作答区坐标、批改结果
```

**优势**：直接拿到「题目坐标 + 作答区坐标 + 批改结果」三套 bbox，无需自己组装 prompt
**限制**：题型分类固定为 12 种，自定义题型支持有限

#### 档位 C：多模态高保真（推荐 ⭐⭐⭐⭐）

**主选**：**Doubao-Seed-2.0-pro（火山引擎）** + **Gemini 2.5 Flash（兜底）**

**Pipeline**：与档位 A 类似，但 Doubao 在国内访问更稳定，Gemini 2.5 Flash 适合作为 segmentation 兜底

### 6.2 学生 App vs 教师阅卷的差异化设计

| 场景 | 推荐主选 | 推荐兜底 | 关键差异 |
|------|---------|---------|---------|
| **学生答疑 App** | Qwen-VL-max | Doubao-Seed-lite | 追求快 + 便宜，答案 + bbox 即可 |
| **教师批改辅助** | 百度智能作业批改 | Qwen-VL-max | 需要题型分类 + 作答区坐标 + 错因分析 |
| **题库录入** | ERNIE-拍照解题 | HunyuanOCR | 需高精度 OCR + 结构化输出 |
| **自动化填表** | Gemini 2.5 Flash | Claude Sonnet 4 | 需 segmentation mask 或像素级精度 |

### 6.3 混合 Pipeline 实战架构

```
[前端] 学生/教师 App
    ↓ (上传图片)
[网关层] 鉴权 + 限流 + 图片预处理
    ↓
[路由层] 按场景路由
    ├─ 小学填空/选择题 → Qwen-VL-max (主) + Doubao-Seed-lite (兜底)
    ├─ 小学解答题     → ERNIE-拍照解题 (主) + Qwen3-VL (兜底)
    ├─ 教师批改       → 百度智能作业批改 (全流程)
    └─ 兜底 (置信度低) → Gemini 2.5 Flash (海外调用)
    ↓
[后处理] bbox 映射 + 答案校验 + 缓存
    ↓
[数据库] 题目 / 答案 / 坐标 / 错因 入库
    ↓
[前端] 渲染标注后的图片 + 答案解释
```

参考资料：
- [拍照解题-通义拍照解题辅导 API 文档 -- 阿里云百炼](https://help.aliyun.com/zh/model-studio/brief-introduction-of-edu-tutor) ⭐值得阅读
- [拍照解题-K12全学科AI拍题搜题解题服务 -- 百度AI开放平台](https://ai.baidu.com/tech/ocr/solve)
- [智能作业批改 API 文档 -- 百度智能云](https://cloud.baidu.com/doc/OCR/s/omimjkvlz)

---

## 7. 关键限制与避坑指南 ⚠️

### 7.1 坐标格式陷阱（最容易踩的坑）

**Qwen-VL via vLLM**：
- vLLM 内部会调用 HF 的 `image_processor` 做预处理，**外部 resize 不一定生效**
- 若输入 4000×3000 图，模型可能返回 `bbox=[1708, 2099, 1776, 2195]`，**超出 resize 后的图片范围**
- 解决：在 API 调用时显式设置 `min_pixels` 和 `max_pixels`，或升级到 vLLM 0.8.2+

**Claude**：
- 官方明确：**不擅长归一化坐标**，必须用绝对像素
- 默认 resize 到 ≤ 1568px 边长，再 padding 到 28 倍数
- 返回坐标基于 resize 后的图，需做 reverse mapping
- 解决：调用前自己 resize 到模型目标尺寸，使坐标一一对应

**Gemini**：
- 0-1000 归一化是「按 1000×1000 假想图」的相对坐标
- iPhone HEIC 照片的 TIFF orientation metadata 不被尊重，导致 bbox 旋转 180°
- 解决：调用前用 `canvas` 元素重新导出为 JPEG

**GPT-4o**：
- **不原生支持 bounding box**，需用 tool calling 调 YOLOv8 等外部检测器
- 即使用 agentic flow 多次迭代，单题成本可达 0.5+ 元，精度仍不及 Qwen-VL

### 7.2 MLLM 定位幻觉问题

**核心数据**：SOTA MLLM 的定位输出中，**58%-68% 的区域是无效的**（MTLA 论文，arXiv:2607.05978）。

**应对策略**：
- **多模型 ensemble**：主选 + 兜底两个模型结果交叉验证
- **置信度过滤**：IoU 低于阈值的 bbox 直接丢弃，要求重新拍照
- **MTLA 后处理**：用 multi-token localized attention 重新打分，可将 8B MLLM 的 COCO AP 从 20.4 提升到 37.0
- **专用检测器兜底**：对解答题等需要「整片区域」的场景，混用 Grounding DINO 1.5 + SAM2

### 7.3 小学场景的特殊挑战

| 挑战 | 表现 | 应对 |
|------|------|------|
| **手写潦草** | 答案 / 题目识别率下降 10-20% | 选 Doubao-Seed-2.0-lite（学生手写 87%+）或 ERNIE-拍照解题 |
| **拍照倾斜 / 光照** | OCR 准确率下降 | 开启「图片矫正」参数（百度 / 阿里 API 都有） |
| **多题目混排** | 题目切分错误 | 优先用「试卷切题识别」专用 API 而非通用 VLM |
| **填空题横线密集** | bbox 框错位 | prompt 明确指定"返回每条横线独立框"而非"返回整片区域" |
| **作图题** | 需要返回画线坐标而非选区 | 需 Gemini 2.5 的 segmentation mask，或单独接入画图模型 |

### 7.4 成本控制

- **缓存机制**：同一张图片的同一题目不要重复调用，用本地 hash 缓存
- **分级调用**：填空题用 Qwen-VL-mini（便宜），解答题才上 Qwen-VL-max
- **批量调用**：阿里云百炼 / 火山引擎的 Batch API 价格是实时的 50%
- **流式响应**：教师批改场景用流式输出，前 1s 就能看到题目 + bbox

参考资料：
- [MLLM 定位幻觉问题: Training-free MTLA -- arXiv](https://arxiv.org/html/2607.05978v1) ⭐值得阅读
- [Qwen3-VL GitHub Issue #1210: vllm resize 问题 -- GitHub](https://github.com/QwenLM/Qwen3-VL/issues/1210)
- [How Claude resizes images and returns pixel coordinates -- Anthropic Docs](https://platform.claude.com/docs/en/build-with-claude/vision-coordinates)

---

## 8. 总结与决策树 ✅

### 8.1 一句话选型结论

> **国内小学拍题 + 框选场景，主选 Qwen3-VL / ERNIE-4.5-VL 走 API；教师批改深度场景选百度智能作业批改专用 API；不要为这个场景选 GPT-4o / Claude——既贵又不如国产。**

### 8.2 决策树

```
开始：小学拍题 + 答案 + bbox 场景
│
├─ 是否需要题型分类 + 错因分析？
│   └─ 是 → 百度智能作业批改 API
│
├─ 是否高并发 + 成本敏感（> 10 万题/天）？
│   └─ 是 → Doubao-Seed-2.0-lite（主）+ Qwen3.5-flash（兜底）
│
├─ 是否需要 segmentation mask（像素级）？
│   └─ 是 → Gemini 2.5 Pro（海外）+ Qwen3-VL（国内）
│
├─ 默认（小学任意题型） →
│   ├─ 主选：Qwen3-VL / Qwen2.5-VL-72B（阿里云百炼）
│   ├─ 兜底：ERNIE-4.5-VL 拍照解题（百度智能云）
│   └─ 备选：Hunyuan-Vision-1.5-Thinking（腾讯云）
│
└─ 海外用户 / 不在意成本 → Gemini 2.5 Pro
```

### 8.3 核心能力天花板

| 维度 | 当前精度 | 天花板 | 推荐主选 |
|------|:-------:|:------:|---------|
| 小学填空题答案 + bbox | 92-96% | 接近人类 | Qwen3-VL / ERNIE 拍照解题 |
| 小学选择题答案 + bbox | 95-99% | 接近人类 | 任意 top VLM |
| 小学解答题答案 + 答题区 bbox | 85-92% | 有提升空间 | ERNIE 智能作业批改 |
| 手写潦草场景 | 80-90% | 中等 | Doubao-Seed-2.0-lite |
| 作图题坐标输出 | 70-85% | 需专用 | Gemini 2.5 + segmentation |

### 8.4 最终推荐

| 场景 | 主选 | 兜底 | 单题成本 |
|------|------|------|:-------:|
| **学生答疑 App（小学）** | Qwen3-VL-32B | ERNIE 拍照解题 | 0.02-0.05 元 |
| **教师批改（K12）** | 百度智能作业批改 | Qwen3-VL-235B | 0.03-0.08 元 |
| **题库数字化** | PaddleOCR-VL-1.5 + ERNIE | HunyuanOCR | 0.01-0.03 元 |
| **国内高并发** | Doubao-Seed-2.0-mini | Qwen3.5-flash | < 0.01 元 |
| **海外 / segmentation** | Gemini 2.5 Pro | Claude Sonnet 4 | 0.2+ 元 |

> **文档版本**：v1.0 | **最后更新**：2026-07-27
>
> **数据来源说明**：本文数据来自 MCP 搜索（Firecrawl + Exa）获取的 2026 年最新资料，包括 arXiv 论文（Qwen3-VL、ERNIE-4.5、Seed1.5-VL、MTLA）、官方 API 文档（阿里云百炼、百度智能云、Anthropic、Google Cloud）、BenchLM 排行榜、ReLE 中文 OCR 评测、GitHub Issue 实测问题。坐标精度与准确率数据均来自第三方实测或官方 benchmark 报告。
