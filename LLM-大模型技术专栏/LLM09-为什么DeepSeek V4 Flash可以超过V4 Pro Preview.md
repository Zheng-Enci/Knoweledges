# 为什么 DeepSeek V4 Flash 可以超过 V4 Pro Preview

> 2026 年 7 月 31 日，DeepSeek 发布了 V4-Flash-0731 正式版。令人震惊的是，这个仅 284B 总参数（13B 激活）的轻量模型，在 Agentic（智能体）基准测试上全面超越了自家 1.6T 总参数（49B 激活）的 V4-Pro-Preview。本文深入分析这一「以下克上」现象背后的技术原因。

---

## 全文摘要

DeepSeek V4-Flash-0731 在 Terminal Bench 2.1、DeepSWE、Cybergym 等 9 项 Agentic（智能体）Benchmark（基准测试）上全面超越 V4-Pro-Preview，且价格仅为 Pro 的 1/3。核心原因在于：Flash-0731 使用了**完全相同的架构和参数规模**，但通过 **Re-Post-Training（重新后训练）** 大幅提升了 Agentic（智能体）Capability。而 V4-Pro-Preview 仍停留在初始预览版本，未经同样的后训练优化。这一现象揭示了 Post-Training（后训练）在 Agentic（智能体）能力塑造中的关键作用，也说明模型能力的提升并非只有 Scaling 一条路。

---

## 1. 背景介绍

2026 年 4 月 24 日，DeepSeek 正式发布了 **V4 系列**，包含两个 MoE（Mixture of Experts，混合专家模型）模型：

- **DeepSeek-V4-Pro**：1.6T 总参数，49B 激活参数，定位旗舰级推理与 Agentic Coding（智能体编程）
- **DeepSeek-V4-Flash**：284B 总参数，13B 激活参数，定位高性价比、高吞吐量的轻量部署

两者均基于 MIT 开源协议发布，支持 1M Token 的 Context Window（上下文窗口）和 384K 的最大输出长度。在发布之初，Pro 和 Flash 的定位非常清晰：Pro 是能力上限，Flash 是性价比选择。

然而，2026 年 7 月 31 日，DeepSeek 发布了 **V4-Flash-0731** 正式版 API，这一格局被彻底打破。DeepSeek 官方公布的 Benchmark（基准测试）数据显示，V4-Flash-0731 在 9 项 Agentic（智能体）Benchmark（基准测试）上全面超越了 V4-Pro-Preview。更令人意外的是，Flash-0731 与 Flash-Preview 采用了**完全相同的架构和参数规模**，唯一的区别是进行了 **Re-Post-Training（重新后训练）**。

**参考资料：**

- [DeepSeek V4 Flash vs V4 Pro: which tier should you use? -- eesel AI](https://www.eesel.ai/blog/deepseek-v4-flash-vs-v4-pro) ⭐值得阅读
- [DeepSeek V4 Flash vs Pro: The Definitive Benchmark Comparison (22 Tests, Pricing, and a Decision Framework) -- The Agent Report](https://the-agent-report.com/2026/07/deepseek-v4-flash-vs-pro-benchmarks-comparison/)
- [DeepSeek V4-Flash-DSpark -- Hugging Face](https://huggingface.co/deepseek-ai/DeepSeek-V4-Flash-DSpark)
- [DeepSeek V4 Preview: The Complete 2026 Guide -- O-Mega](https://o-mega.ai/articles/deepseek-v4-preview-the-complete-2026-guide)

---

## 2. 架构差异

### 2.1 参数规模对比

| 规格 | V4-Pro | V4-Flash |
|------|--------|----------|
| 总参数 | 1.6T | 284B |
| 激活参数 | 49B（3.1%） | 13B（4.6%） |
| 专家数 | 256 Experts，8 个激活 | 64 Experts，8 个激活 |
| 上下文窗口 | 1M Tokens | 1M Tokens |
| 最大输出 | 384K Tokens | 384K Tokens |
| 精度 | FP4 + FP8 混合 | FP4 + FP8 混合 |
| 开源协议 | MIT | MIT |

### 2.2 架构共同点

两者均采用 DeepSeek 自研的 **Hybrid Attention（混合注意力）架构**，结合了 CSA（Compressed Sparse Attention，压缩稀疏注意力）和 HCA（Heavily Compressed Attention，重度压缩注意力），大幅降低了推理时的计算量和 KV Cache 占用。相比 V3.2，V4-Pro 的推理 FLOPs 降低了 73%，KV Cache 降低了 90%。

### 2.3 关键差异

Pro 的专家数是 Flash 的 4 倍（256 vs 64），激活参数是 Flash 的 3.8 倍（49B vs 13B）。从 Scaling Law（缩放定律）的直觉来看，Pro 应该在所有维度上都优于 Flash。然而，在 Agentic（智能体）任务上，Flash-0731 不仅没有落后，反而实现了反超——这正是本篇文档要解答的核心问题。

**参考资料：**

- [DeepSeek V4 Pro vs Flash: Specs, Pricing & Speed -- Coder's Era](https://codersera.com/blog/deepseek-v4-pro-vs-flash/)
- [DeepSeek V4 Pro vs V4 Flash (2026): Which to Actually Run, Tested -- DataLLM Lab](https://www.datallmlab.com/blog/deepseek-v4-pro-vs-flash.html)
- [DeepSeek V4 Alters Everything We Knew About Price-Performance Math -- Lightning AI](https://lightning.ai/blog/deepseekv4comparison)

---

## 3. 0731 更新：Post-Training 的力量

### 3.1 核心事实：相同架构，不同结果

这是整个事件中最关键的事实：**V4-Flash-0731 与 V4-Flash-Preview 采用了完全相同的架构和参数规模，唯一的区别是进行了 Re-Post-Training（重新后训练）**。

DeepSeek 官方在发布说明中明确写道：「same architecture and size, new post-training」。这意味着，Flash-0731 在 Agentic（智能体）能力上的巨大飞跃，**完全来自于后训练阶段的数据选择和训练策略优化**，而非模型规模的扩大或架构的创新。

### 3.2 Post-Training 的效果有多显著？

从 Preview 到 0731 的改进幅度惊人：

| 基准测试 | Flash-Preview | Flash-0731 | 提升幅度 |
|---------|--------------|------------|---------|
| DeepSWE | 7.3 | 54.4 | **+645%** |
| AutomationBench | 10.8 | 25.1 | **+132%** |
| Cybergym | 38.7 | 76.7 | **+98%** |
| Toolathlon | 49.7 | 70.3 | **+41%** |
| NL2Repo | 39.4 | 54.2 | **+38%** |
| Terminal Bench 2.1 | 61.8 | 82.7 | **+34%** |
| DSBench-FullStack | 37.0 | 68.7 | **+86%** |
| DSBench-Hard | 25.8 | 59.6 | **+131%** |
| Agents' Last Exam | 15.8 | 25.2 | **+59%** |

这些数据清晰地表明：**Post-Training（后训练）对 Agentic（智能体）能力的影响远大于模型规模本身**。尤其是 DeepSWE 从 7.3 提升到 54.4（+645%），说明 DeepSeek 在后训练阶段找到了大幅提升 Agentic（智能体）Capability 的关键训练方法。

### 3.3 为什么 Post-Training 对 Agentic（智能体）任务如此重要？

Agentic（智能体）任务（如 Tool Use（工具调用）、Code Generation（代码生成）、Multi-Step Reasoning（多步推理））与传统的 Language Modeling（语言建模）有本质区别：

1. **复杂的行为序列**：Agentic（智能体）任务需要模型理解多步操作的因果关系，而非简单的 Next Token Prediction（下一个词元预测）
2. **工具调用格式**：需要精确遵循 API 格式和参数规范，这对训练数据中的格式一致性要求极高
3. **错误恢复**：Agent 需要具备从错误中恢复的能力，这种能力在 Pre-Training（预训练）阶段的语料中很少出现
4. **反馈循环**：高质量的后训练数据可以包含执行结果反馈，让模型学会根据环境反馈调整行为

DeepSeek 很可能在 Flash-0731 的后训练中引入了大量高质量的 Agentic Trajectory Data（智能体轨迹数据），包括实际的代码执行反馈、工具调用结果验证等，从而在相同的参数规模下实现了 Agentic（智能体）能力的质变。

**参考资料：**

- [DeepSeek V4-Flash Beats Its Own Pro Model: Agent Benchmarks That Just Changed the Game -- Flowtivity](https://flowtivity.ai/blog/deepseek-v4-flash-agent-benchmarks/) ⭐值得阅读
- [DeepSeek ships production V4-Flash-0731, claims wins over its own Pro model -- AI Insiders](https://aiinsiders.net/article/deepseek-ships-production-v4-flash-0731-claims-wins-over)
- [DeepSeek Performance Review: V4 Pro & Flash Tested -- DeepSeek Guide](https://deepseekai.guide/reviews/deepseek-performance-review/)

---

## 4. Agentic（智能体）Benchmark 对比

### 4.1 Flash-0731 vs Pro-Preview：全面超越

这是 DeepSeek 官方公布的 Agentic（智能体）Benchmark（基准测试）对比数据：

| 基准测试 | Flash-0731 | Flash-Preview | Pro-Preview | GLM-5.2 | Opus-4.8 |
|---------|-----------|--------------|------------|---------|---------|
| **Terminal Bench 2.1** | **82.7** | 61.8 | 72.1 | 81.0 | 85.0 |
| **NL2Repo** | **54.2** | 39.4 | 38.5 | 48.9 | 69.7 |
| **Cybergym** | **76.7** | 38.7 | 52.7 | - | 83.1 |
| **DeepSWE** | **54.4** | 7.3 | 12.8 | 46.2 | 58.0 |
| **Toolathlon Verified** | **70.3** | 49.7 | 55.9 | 59.9 | 76.2 |
| **Agents' Last Exam** | **25.2** | 15.8 | 16.5 | 23.8 | 25.7 |
| **AutomationBench Public** | **25.1** | 10.8 | 12.8 | 12.9 | 27.2 |
| **DSBench-FullStack** | **68.7** | 37.0 | 41.8 | 61.8 | 71.6 |
| **DSBench-Hard** | **59.6** | 25.8 | 31.1 | 54.5 | 71.7 |

Flash-0731 在全部 9 项 Agentic（智能体）Benchmark（基准测试）上均超越了 Pro-Preview（预览版）。尤其是 DeepSWE（54.4 vs 12.8，高出 4.3 倍）和 Cybergym（76.7 vs 52.7，高出 45%）的差距最为显著。

### 4.2 独立评测机构的验证

Artificial Analysis（人工智能分析平台）的独立评测也印证了这一趋势：Flash-0731 在 Intelligence Index（智能指数）上得分 **50**，而 V4-Pro 得分仅为 **44**。在 Cost Per Task（单任务成本）上，Flash 仅为 $0.03，Pro 为 $0.05。

### 4.3 与业界顶尖模型的对比

Flash-0731 在多数 Agentic（智能体）Benchmark（基准测试）上已经接近甚至超越 GLM-5.2（智谱的高端模型）。虽然仍落后于 Claude Opus 4.8，但考虑到 Flash 的价格仅为 Opus 4.8 的 1/50 左右，这一性价比在 Agentic（智能体）领域是前所未有的。

**参考资料：**

- [DeepSeek V4 Flash 0731 (max) -- Artificial Analysis](https://artificialanalysis.ai/models/deepseek-v4-flash)
- [DeepSeek V4 Flash Benchmarks & Pricing (August 2026) -- BenchLM](https://benchlm.ai/models/deepseek-v4-flash)
- [DeepSeek V4 Benchmark：Pro 与 Flash 分数 -- DeepSeek Space](https://deepseekv4.space/zh/blog/deepseek-v4-benchmark)

---

## 5. Pro 仍然占优的领域

虽然 Flash-0731 在 Agentic（智能体）任务上全面超越了 Pro-Preview（预览版），但在以下领域，Pro 仍然保持着明显的优势：

### 5.1 知识召回

SimpleQA-Verified（简易问答-验证集）测试中，Pro-Preview（预览版）得分 57.9，而 Flash 仅为 34.1，差距高达 23.8 个百分点。这表明 Pro 的更大参数规模在 Factual Knowledge（事实知识）的存储和召回上具有天然优势。

### 5.2 长上下文检索

在 MRCR 1M（百万级别上下文检索）测试中，Pro 得分 83.5，Flash 为 78.7，差距 4.8 个百分点。在大规模文档分析和精确信息定位场景中，Pro 的表现更可靠。

### 5.3 复杂推理

在 HLE（Humanity's Last Exam，人类最后的考试）上，Pro 得分 37.7，Flash 约 34.6，差距约 3 个百分点。在需要多步推理和深度分析的场景中，Pro 的更大参数规模仍然提供了更高的上限。

### 5.4 为什么 Pro 在这些领域有优势？

这背后的原因在于 Scaling Law（缩放定律）的本质：知识存储和长上下文处理需要的是模型的「容量」，而 Agentic（智能体）能力更多依赖的是「训练质量」。Pro 的 49B 激活参数提供了更大的知识存储空间，但如果没有经过同样高质量的后训练，这种容量优势在 Agentic（智能体）任务上无法转化为实际能力。

**参考资料：**

- [DeepSeek V4 Pro vs Flash: Which One for Production? -- WaveSpeed](https://wavespeed.ai/blog/posts/deepseek-v4-pro-vs-flash/)
- [DeepSeek V4 Flash vs V4 Pro: Which API to Use -- AI Reiter](https://aireiter.com/blog/deepseek-v4-flash-vs-deepseek-v4-pro)

---

## 6. 总结

DeepSeek V4-Flash-0731 超越 V4-Pro-Preview 这一事件，揭示了 AI 模型能力提升中的两个重要规律：

| 维度 | 关键发现 | 启示 |
|------|---------|------|
| 🧠 Post-Training（后训练）的力量 | 相同架构、相同参数，仅通过后训练即可实现 Agentic（智能体）能力数倍提升 | Post-Training（后训练）是释放模型潜力的关键环节，其重要性不亚于 Pre-Training |
| ⚖️ 规模与能力的错位 | 更大参数规模的 Pro 在 Agentic（智能体）任务上被 Flash 反超 | 参数规模并非能力的唯一决定因素，训练数据的质量和策略同样关键 |
| 🎯 Agentic（智能体）能力的特殊性 | Agentic（智能体）能力对训练数据的依赖远大于对参数规模的依赖 | Agentic（智能体）能力的提升可以通过针对性后训练实现，而不必依赖模型规模的扩大 |
| 💰 性价比的重新定义 | Flash-0731 以 1/3 的价格实现更高的 Agentic（智能体）性能 | 在选择模型时，需要结合具体任务场景和训练状态，而非仅凭参数规模判断 |

**核心结论**：Flash-0731 超越 Pro-Preview（预览版）的根源在于——**Post-Training（后训练）的时间差**。Flash 经过了 0731 版本的针对性后训练优化，而 Pro-Preview（预览版）仍停留在 4 月发布的初始预览版本。当 Pro 的正式版经过同样的后训练迭代后，两者的差距很可能会重新拉开。但这一事件已经充分证明：**Post-Training（后训练）是解锁模型 Agentic（智能体）能力的关键，其重要性甚至可能超越模型规模的扩大。**

---

**最后更新时间**：2026-08-11