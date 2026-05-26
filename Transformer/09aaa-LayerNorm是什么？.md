<!--
  文档：09aaa-LayerNorm是什么？.md
  说明：详细解释层归一化（Layer Normalization）的概念、原理、数学公式与计算步骤，帮助读者理解 Transformer 中归一化机制的作用
-->

# 09aaa-LayerNorm是什么？📊

<!-- 重要规范：本文档中所有数学公式（包括块级公式 $$...$$ 和行内公式 $...$）必须使用标准 LaTeX 格式编写，禁止使用纯文本或 Unicode 数学符号 -->

<!-- 全文摘要说明：以下段落是本文档的全文摘要，必须精炼概括文档核心内容，字数不能超过100个字 -->
本文档详细解释层归一化（Layer Normalization, LayerNorm）的核心概念，涵盖数学定义、计算步骤、与 BatchNorm 的核心区别，以及 Transformer 选择 LayerNorm 的原因，最后提供 PyTorch 代码示例 🛠️
<!-- 全文摘要结束 -->

## 1. 什么是 LayerNorm？🤔

> 本章解释 LayerNorm 的基本概念和核心思想

**Layer Normalization（层归一化）** 是一种对神经网络的每一层输出进行归一化的技术，由 Jimmy Lei Ba、Jamie Ryan Kiros 和 Geoffrey E. Hinton 于 2016 年提出。

它的核心思想非常简单：**对单个样本的所有特征维度计算均值和方差，进行 Z-score 标准化，再通过可学习的缩放参数 $\gamma$ 和偏移参数 $\beta$ 恢复表达能力。**

直观理解：假设一个 token 的特征向量为 $\mathbf{x} = [x_1, x_2, \ldots, x_d]$，LayerNorm 先把这个向量变成均值为 0、方差为 1 的标准形式，然后让网络自己学习怎么缩放（$\gamma$）和平移（$\beta$）到最佳位置。

## 2. 核心公式 📝

> 本章给出 LayerNorm 的完整数学表达式并拆解每一步

LayerNorm 的计算分为三步：

**第1步：计算均值**

<!-- 数学公式必须使用 LaTeX 格式 -->
$$
\mu = \frac{1}{d} \sum_{i=1}^{d} x_i
$$
<!-- 数学公式必须使用 LaTeX 格式 -->

**第2步：计算方差**

<!-- 数学公式必须使用 LaTeX 格式 -->
$$
\sigma^2 = \frac{1}{d} \sum_{i=1}^{d} (x_i - \mu)^2
$$
<!-- 数学公式必须使用 LaTeX 格式 -->

**第3步：归一化 + 仿射变换**

<!-- 数学公式必须使用 LaTeX 格式 -->
$$
\text{LayerNorm}(\mathbf{x}) = \gamma \odot \frac{\mathbf{x} - \mu}{\sqrt{\sigma^2 + \epsilon}} + \beta
$$
<!-- 数学公式必须使用 LaTeX 格式 -->

其中：
- $d$ 是特征维度的大小
- $\mu$ 是该样本所有特征的均值，$\sigma^2$ 是方差
- $\epsilon$ 是很小的常数（如 $10^{-5}$），防止除以零
- $\gamma$（缩放）和 $\beta$（偏移）是可学习参数，形状与特征维度相同

## 3. 计算示例 🔍

> 本章通过一个具体数值演示 LayerNorm 的计算过程

假设输入向量 $\mathbf{x} = [2.0, 4.0, 6.0]$，$\epsilon = 10^{-5}$：

- **均值**：$\mu = \frac{2.0 + 4.0 + 6.0}{3} = 4.0$
- **方差**：$\sigma^2 = \frac{(2.0-4.0)^2 + (4.0-4.0)^2 + (6.0-4.0)^2}{3} \approx 2.667$
- **归一化**：$\hat{\mathbf{x}} = \frac{[2.0, 4.0, 6.0] - 4.0}{\sqrt{2.667 + 10^{-5}}} \approx [-1.225, 0, 1.225]$
- **仿射变换**：$\mathbf{y} = \gamma \odot [-1.225, 0, 1.225] + \beta$

如果 $\gamma = [1,1,1]$，$\beta = [0,0,0]$，则输出为 $[-1.225, 0, 1.225]$——均值为 0，方差为 1。网络通过训练 $\gamma$ 和 $\beta$ 来适应不同数据的需要。

## 4. LayerNorm vs BatchNorm ⚔️

> 本章对比 LayerNorm 和 BatchNorm 的核心区别

两者的本质区别在于**归一化的维度不同**：

| 特性 | BatchNorm | LayerNorm |
|------|-----------|-----------|
| 归一化维度 | 沿 **batch 维度** | 沿 **特征维度** |
| 统计量依赖 | 依赖 batch 中其他样本 | 仅依赖当前样本 |
| 受 batch size 影响 | 是（batch 小时效果差） | 否 |
| 训练/推理行为 | 不同（需 running stats） | 一致 |
| 适用领域 | CV（图像分类等） | NLP（Transformer、RNN 等） |

### 为什么 Transformer 选择 LayerNorm？

在 NLP 任务中，语义特征是由**上下文决定**的——同一个词在不同句子中含义不同。LayerNorm 只在单个样本内部归一化，保留了句内各 token 特征之间的相对关系，不破坏语义结构。而 BatchNorm 沿 batch 方向归一化，会混合不同句子的特征，破坏了句内语义。

此外，NLP 中句子长度不一致、batch size 通常较小，LayerNorm 不受这些因素影响。

## 5. PyTorch 代码示例 💻

> 本章通过一个简单的代码示例展示 LayerNorm 的使用

```python
import torch                                              # 导入 PyTorch 核心库，提供张量运算
import torch.nn as nn                                     # 导入神经网络模块，包含 LayerNorm 层

# 使用 PyTorch 原生 LayerNorm
d_model = 512                                             # 特征维度大小，示例：Transformer 中 d_model=512
layernorm = nn.LayerNorm(normalized_shape=d_model)        # 创建 LayerNorm 层，示例：对 512 维特征归一化

# 模拟输入：batch_size=2, seq_len=10, d_model=512
x = torch.randn(2, 10, d_model)                           # 随机生成输入张量，形状 [2,10,512]
output = layernorm(x)                                     # 前向传播，数据流动：[2,10,512] → [2,10,512]

# 验证归一化效果：取第一个 batch 第一个 token 的特征向量
print(f"均值: {output[0,0].mean():.4f}")                  # 应接近 0.0000
print(f"方差: {output[0,0].var():.4f}")                   # 应接近 1.0000
```

在 Transformer 的[编码器结构](https://juejin.cn/post/7641031588095049764)（[CSDN](https://blog.csdn.net/2301_79239314/article/details/161198385)）中，LayerNorm 出现在每个子层之后的 **Add & Norm** 操作中，负责稳定训练过程。

---

**最后更新时间**：2026-05-25
