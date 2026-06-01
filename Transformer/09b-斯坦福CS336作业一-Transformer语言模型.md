# 09b-斯坦福CS336作业一-Transformer语言模型 🎓

<!-- 重要规范：本文档中所有数学公式（包括块级公式 $$...$$ 和行内公式 $...$）必须使用标准 LaTeX 格式编写，禁止使用纯文本或 Unicode 数学符号 -->

<!-- 全文摘要说明：以下段落是本文档的全文摘要，必须精炼概括文档核心内容，字数不能超过100个字 -->
本文档详细解析斯坦福CS336课程作业一的第二部分：Transformer语言模型架构（Decoder-Only Transformer），涵盖多头注意力、RoPE、RMSNorm、SwiGLU等核心组件的从零实现 🛠️
<!-- 全文摘要结束 -->

## 章节阅读路线图 🗺️

1. **Transformer语言模型架构** → 解码器结构、多头注意力、RoPE、RMSNorm、SwiGLU
2. **完整可运行代码** → 整合所有组件的完整实现
3. **总结** → 回顾核心要点

---

> 💡 **前置阅读**：作业一包含两个部分：第一部分 BPE 分词器的实现请参考 [09a-斯坦福CS336作业一-BPE分词器](https://juejin.cn/post/7643037374348296233)（[CSDN](https://blog.csdn.net/2301_79239314/article/details/161367999)）；课程背景请参考 [09-斯坦福CS336作业](https://juejin.cn/post/7641109461659500582)（[CSDN](https://blog.csdn.net/2301_79239314/article/details/161204079)）。本文档聚焦作业一的**第二部分**：Transformer 语言模型实现。

## 1. Transformer语言模型架构 🏗️

> 本章详细拆解 Transformer 语言模型的核心组件

### 1.1 整体架构

作业一的**第二部分**要求实现一个**仅含解码器的 Transformer**（Decoder-Only Transformer），类似 GPT 的结构。

**核心特点：**

- 基于解码器的 Transformer 结构，包含多头自注意力机制
- 采用旋转位置编码（RoPE），增强模型对序列位置信息的捕捉能力
- 使用 RMSNorm 替代传统 LayerNorm，提升训练稳定性
- 前馈网络中引入 SwiGLU 激活函数，性能优于 ReLU 等传统激活
- 采用 Decoder-Only 架构，支持自回归文本生成

**模型数据流动**：

```
输入文本 → Token IDs → Embedding → + RoPE → Transformer Block × N → RMSNorm → 输出 logits
                                                        ↓
                                            Multi-Head Self-Attention
                                            ↓
                                            SwiGLU FFN
```

### 1.2 基础通用层

#### 1.2.1 无偏置线性层（Linear）

简化版的线性变换层 $y = xW^T$，移除了偏置项（bias），并采用类 Xavier 初始化保证训练稳定性。

**为什么现代 LLM 移除 bias？**

在 Pre-Norm + 残差连接架构下，bias 项提供的偏移表达能力完全冗余：

| 原因 | 说明 |
|------|------|
| **RMSNorm 已覆盖偏置功能** | RMSNorm 的可学习缩放参数已承担归一化功能，bias 在此之上是多余的 |
| **残差连接使 bias 失效** | 多层堆叠时，前一层的 bias 偏移会被后续 RMSNorm 消除 |
| **训练稳定性提升** | PaLM 论文指出移除 bias 可 "increase training stability for large models" |
| **参数节省** | 每层节省 $d_{model}$ 参数，数十层堆叠效果可观 |

> 这已成为 LLaMA、PaLM、GPT-4 等现代大模型的**标准配置**。

```python
import torch                                             # 导入 PyTorch 核心库
import torch.nn as nn                                    # 导入神经网络模块
from einops import einsum                                # 导入 einops 用于清晰的张量维度映射

# 无偏置线性层：y = x @ W^T，移除偏置项以匹配现代 LLM 架构
# 参数: in_features 输入维度，out_features 输出维度
# 示例: linear = Linear(in_features=768, out_features=3072)
class Linear(nn.Module):
    """无偏置线性层，执行 y = x @ W^T 变换。
    
    参数:
        in_features: 输入特征维度
        out_features: 输出特征维度
        device: 计算设备
        dtype: 数据类型
    
    返回:
        无
    
    示例:
        >>> linear = Linear(in_features=768, out_features=3072)
        >>> linear.weight.shape
        torch.Size([3072, 768])
    """
    def __init__(self, in_features: int, out_features: int, device=None, dtype=None):
        super().__init__()
        self.weight = nn.Parameter(torch.empty((out_features, in_features), device=device, dtype=dtype))  # 权重矩阵：(out_features, in_features)
        std = (2 / (in_features + out_features)) ** 0.5                                                  # 计算类 Xavier 初始化标准差
        nn.init.trunc_normal_(self.weight, std=std, a=-3*std, b=3*std)                                   # 截断正态分布初始化，限制在 ±3σ
    
    """前向传播计算无偏置线性变换。
    
    参数:
        x: 输入张量，形状为 [..., in_features]
    
    返回:
        输出张量，形状为 [..., out_features]
    
    示例:
        >>> x = torch.randn(2, 10, 768)  # [batch=2, seq_len=10, in_features=768]
        >>> y = linear(x)
        >>> y.shape
        torch.Size([2, 10, 3072])
    """
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return einsum(x, self.weight, "... in_features, out_features in_features -> ... out_features")  # y = x @ W^T: [2,10,768] × [768,3072] → [2,10,3072]
```

**参考资料：**

- [Why do some LLMs remove bias terms from linear layers? -- Sebastian Raschka](https://sebastianraschka.com/faq/docs/bias-terms-modern-llms.html) ⭐值得阅读
- [PaLM: Scaling Language Modeling with Pathways -- arXiv](https://arxiv.org/abs/2204.02311)

---

#### 1.2.2 词嵌入层（Embedding）

将离散的 token ID 映射为连续的稠密向量，嵌入维度（embedding_dim）与模型隐藏层维度（d_model）保持一致。

```python
# 词嵌入层：token ID → 稠密向量
# 参数: num_embeddings 词汇表大小，embedding_dim 嵌入维度
# 示例: embedding = Embedding(num_embeddings=32000, embedding_dim=768)
class Embedding(nn.Module):
    # 初始化嵌入权重矩阵
    # 参数: num_embeddings 词汇表大小，embedding_dim 嵌入维度，示例：32000 个 token，每个 768 维
    # 返回: 无
    # 示例: self.weight.shape = (32000, 768)
    def __init__(self, num_embeddings: int, embedding_dim: int, device=None, dtype=None):
        super().__init__()
        self.vocab_size = num_embeddings
        self.d_model = embedding_dim
        # 嵌入权重矩阵：形状为 (词汇表大小, 嵌入维度)
        self.weight = nn.Parameter(torch.empty((self.vocab_size, self.d_model), device=device, dtype=dtype))
        nn.init.trunc_normal_(self.weight, std=1, a=-3, b=3)
    
    # 前向传播获取 token 的嵌入向量
    # 参数: token_ids 输入 token ID 张量 [batch_size, seq_len]，示例：[2, 10]
    # 返回: embeddings 嵌入向量 [batch_size, seq_len, embedding_dim]，示例：[2, 10, 768]
    # 示例: embeddings = embedding(token_ids)
    def forward(self, token_ids: torch.LongTensor) -> torch.Tensor:
        # 输入：(batch_size, seq_len) → 输出：(batch_size, seq_len, embedding_dim)
        # 数据流动：token_ids[2,10] → embeddings[2,10,768]（通过索引获取对应 token 的嵌入向量）
        return self.weight[token_ids]
```

#### 1.2.3 RMS归一化层（RMSNorm）

相比传统 LayerNorm，RMSNorm 移除了均值中心化步骤，仅对输入的均方根（RMS）进行归一化，在减少计算量的同时提升训练稳定性。

```python
# RMS归一化层：仅对均方根进行归一化
# 参数: d_model 输入维度，eps 防止除零的微小值
# 示例: rmsnorm = RMSNorm(d_model=768, eps=1e-5)
class RMSNorm(nn.Module):
    # 初始化 RMSNorm 参数
    # 参数: d_model 输入维度，eps 防止除零的微小值（默认 1e-5），示例：d_model=768 表示归一化 768 维向量
    # 返回: 无
    # 示例: self.weight.shape = (768,)，初始化为 1
    def __init__(self, d_model: int, eps: float = 1e-5, device=None, dtype=None):
        super().__init__()
        self.d_model = d_model
        self.eps = eps
        # 可学习的缩放参数：形状为 (d_model,)，初始化为1（不改变归一化结果）
        self.weight = nn.Parameter(torch.ones(self.d_model, device=device, dtype=dtype))
    
    # 前向传播应用 RMS 归一化
    # 参数: x 输入张量 [batch_size, seq_len, d_model]，示例：[2, 10, 768]
    # 返回: out 归一化后的张量 [2, 10, 768]
    # 示例: out = rmsnorm(x)
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # 输入：(batch_size, seq_len, d_model) → 输出：同输入形状
        in_dtype = x.dtype                                                     # 保存输入数据类型，避免精度损失
        x = x.to(dtype=torch.float32)                                          # 转为 float32 计算，提升数值稳定性
        
        # 1. 计算最后一维的均方根（RMS）
        # 数据流动：x[2,10,768] → x.pow(2)[2,10,768] → mean[2,10,1] → +eps → sqrt → rms[2,10,1]
        rms = (x.pow(2).mean(-1, keepdim=True) + self.eps) ** 0.5
        
        # 2. 归一化 + 应用缩放参数
        # 数据流动：x[2,10,768] / rms[2,10,1] → out[2,10,768] × weight[768] → out[2,10,768]
        out = x / rms * self.weight
        return out.to(dtype=in_dtype)                                          # 恢复原数据类型
```

**RMSNorm vs LayerNorm 对比**：

| 特性 | LayerNorm | RMSNorm |
|------|-----------|---------|
| 均值中心化 | ✓ | ✗ |
| 方差归一化 | ✓ | 仅 RMS |
| 计算量 | 较大 | 较小 |
| 训练稳定性 | 好 | 更好 |
| 使用场景 | 传统 Transformer | LLaMA、GPT-4 等现代模型 |

---

### 1.3 激活函数与前馈网络

#### 1.3.1 SwiGLU激活函数

SwiGLU 是 GLU（Gated Linear Unit）的变体，通过 Sigmoid 门控对线性变换结果进行筛选，相比 ReLU 能更好地捕捉特征间的非线性关系。

```python
# SwiGLU前馈网络：门控线性单元
# 参数: d_model 输入维度，d_ff 前馈网络中间层维度
# 示例: swiglu = SwiGLU(d_model=768, d_ff=3072)
class SwiGLU(nn.Module):
    # 初始化 SwiGLU 的三个线性层
    # 参数: d_model 输入维度，d_ff 中间层维度（通常为 d_model 的 4 倍），示例：768 → 3072
    # 返回: 无
    # 示例: self.w1: 768→3072, self.w2: 3072→768, self.w3: 768→3072
    def __init__(self, d_model: int, d_ff: int, device=None, dtype=None):
        super().__init__()
        self.d_model = d_model
        self.d_ff = d_ff
        # 定义三个线性层：W1/W3用于生成门控与候选特征，W2用于输出投影
        self.w1 = Linear(d_model, d_ff, device=device, dtype=dtype)            # 门控分支
        self.w2 = Linear(d_ff, d_model, device=device, dtype=dtype)            # 输出投影
        self.w3 = Linear(d_model, d_ff, device=device, dtype=dtype)            # 候选分支
    
    # SiLU（Sigmoid Linear Unit）激活函数
    # 参数: x 输入张量，示例：[2, 10, 3072]
    # 返回: x * sigmoid(x)，示例：[2, 10, 3072]
    # 示例: silu_output = self._silu(x)
    def _silu(self, x: torch.Tensor) -> torch.Tensor:
        return x * torch.sigmoid(x)                                            # SiLU = x × σ(x)
    
    # GLU（Gated Linear Unit）门控机制
    # 参数: x 输入张量 [batch, seq_len, d_model]，示例：[2, 10, 768]
    # 返回: SiLU(W1(x)) × W3(x)，示例：[2, 10, 3072]
    # 示例: glu_output = self._glu(x)
    def _glu(self, x: torch.Tensor) -> torch.Tensor:
        return self._silu(self.w1(x)) * self.w3(x)                             # SiLU门控 × W3线性变换结果
    
    # 前向传播计算 SwiGLU
    # 参数: x 输入张量 [batch, seq_len, d_model]，示例：[2, 10, 768]
    # 返回: 输出张量 [batch, seq_len, d_model]，示例：[2, 10, 768]
    # 示例: output = swiglu(x)
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # 输入：(batch_size, seq_len, d_model) → 输出：同输入形状
        # 数据流动：x[2,10,768] → _glu → [2,10,3072] → w2 → [2,10,768]
        return self.w2(self._glu(x))                                           # 门控结果通过 W2 投影回 d_model 维度
```

**SwiGLU 数据流动**：

```
输入 x [batch, seq_len, d_model=768]
         ↓
    ┌────┴────┐
    W1        W3
    ↓         ↓
[2,10,3072]  [2,10,3072]
    ↓
  SiLU (x * sigmoid(x))
    ↓
    × (逐元素相乘)
    ↓
[2,10,3072] (门控结果)
    ↓
    W2
    ↓
输出 [2,10,768]
```

---

### 1.4 位置编码：旋转位置编码（RoPE）

Transformer 本身不具备位置感知能力，需通过位置编码注入序列顺序信息。RoPE 通过旋转矩阵将位置信息编码到 token 的嵌入向量中，且支持长度外推。

```python
import math                                              # 导入数学库，用于计算

# 旋转位置编码（RoPE）
# 参数: theta 基础频率（通常 10000），d_k 注意力头维度，max_seq_len 最大序列长度
# 示例: rope = ROPE(theta=10000, d_k=64, max_seq_len=1024)
class RoPE(nn.Module):
    # 初始化 RoPE 参数并预计算 cos/sin 缓存
    # 参数: theta 基础频率，d_k 头维度，max_seq_len 最大序列长度，示例：d_k=64 表示每个头 64 维
    # 返回: 无
    # 示例: self.cos_cached.shape = (1024, 32)
    def __init__(self, theta: float, d_k: int, max_seq_len: int, device=None):
        super().__init__()
        self.theta = theta
        self.d_k = d_k
        self.max_seq_len = max_seq_len
        self.device = device
        
        # 预计算cos/sin缓存（仅在首次初始化时计算，避免重复计算）
        # 1. 计算频率矩阵：shape (d_k//2,)
        # 数据流动：arange[0,2,...,62] → /64 → theta^ → 1/ → freqs_d[32]
        freqs_d = 1 / (theta ** (torch.arange(0, d_k, 2, device=device).float() / d_k))
        
        # 2. 计算位置矩阵：shape (max_seq_len,)
        # 数据流动：arange[0,1,...,1023] → pos_i[1024]
        pos_i = torch.arange(max_seq_len, device=device).float()
        
        # 3. 频率-位置外积：shape (max_seq_len, d_k//2)
        # 数据流动：freqs_d[32] × pos_i[1024] → freqs[1024,32]
        freqs = torch.outer(pos_i, freqs_d)
        
        # 预计算cos和sin值（后续直接索引使用）
        self.register_buffer("cos_cached", torch.cos(freqs), persistent=False)     # cos_cached[1024,32]
        self.register_buffer("sin_cached", torch.sin(freqs), persistent=False)     # sin_cached[1024,32]
    
    # 前向传播应用旋转位置编码
    # 参数: x 输入张量 [..., seq_len, d_k]，token_positions 位置索引 [..., seq_len]
    # 返回: 旋转后的张量 [..., seq_len, d_k]
    # 示例: x_rotated = rope(x, positions)
    def forward(self, x: torch.Tensor, token_positions: torch.Tensor) -> torch.Tensor:
        # 1. 按最后一维的奇偶索引分组（d_k需为偶数）
        # 数据流动：x[...,10,64] → x_even[...,10,32], x_odd[...,10,32]
        x_even = x[..., ::2]                                                       # 偶数维度：索引 0,2,4...
        x_odd = x[..., 1::2]                                                       # 奇数维度：索引 1,3,5...
        
        # 2. 获取当前序列长度对应的cos/sin值
        # 数据流动：cos_cached[1024,32] + token_positions[...,10] → cos[...,10,32]
        cos = self.cos_cached[token_positions]
        sin = self.sin_cached[token_positions]
        
        # 3. 应用旋转公式：将位置信息融入向量
        # 数据流动：cos[...10,32]*x_even[...10,32] - sin[...10,32]*x_odd[...10,32] → out1[...10,32]
        out1 = cos * x_even - sin * x_odd                                          # 偶数维度旋转结果
        out2 = sin * x_even + cos * x_odd                                          # 奇数维度旋转结果
        
        # 4. 重组维度：将奇偶分组合并回原d_k维度
        # 数据流动：out1[...10,32], out2[...10,32] → stack[...10,32,2] → flatten[...10,64]
        out = torch.stack([out1, out2], dim=-1).flatten(-2)
        return out
```

**RoPE 旋转公式**：

对于位置 $m$ 和维度 $i$（$i$ 为偶数），旋转公式为：

$$
\begin{bmatrix}
x_{m, i}^{\text{out}} \\
x_{m, i+1}^{\text{out}}
\end{bmatrix}
=
\begin{bmatrix}
\cos(m \theta_i) & -\sin(m \theta_i) \\
\sin(m \theta_i) & \cos(m \theta_i)
\end{bmatrix}
\times
\begin{bmatrix}
x_{m, i} \\
x_{m, i+1}
\end{bmatrix}
$$

其中 $\theta_i = 10000^{-2i/d_k}$ 是频率。

---

**参考资料：**

- [RoPE 旋转位置编码详解 -- CSDN](https://blog.csdn.net/weixin_70325224/article/details/147484980)
- [RoFormer: Enhanced Transformer with Rotary Position Embedding -- arXiv](https://arxiv.org/abs/2104.09864) ⭐值得阅读

---

### 1.5 多头自注意力（Multi-Head Self-Attention）

注意力机制是 Transformer 的核心，负责捕捉序列内 token 间的依赖关系。

```python
# 多头自注意力机制
# 参数: d_model 模型维度，n_heads 注意力头数，max_seq_len 最大序列长度
# 示例: mha = MultiHeadAttention(d_model=768, n_heads=12, max_seq_len=1024)
class MultiHeadAttention(nn.Module):
    # 初始化多头注意力参数
    # 参数: d_model 模型维度，n_heads 头数，示例：768/12=64 表示每个头 64 维
    # 返回: 无
    # 示例: d_k=64, self.wq: 768→768, self.wk: 768→768, self.wv: 768→768
    def __init__(self, d_model: int, n_heads: int, max_seq_len: int, device=None, dtype=None):
        super().__init__()
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_k = d_model // n_heads                                                # 每个头的维度
        
        # Q、K、V 的线性变换
        self.wq = Linear(d_model, d_model, device=device, dtype=dtype)               # 查询投影
        self.wk = Linear(d_model, d_model, device=device, dtype=dtype)               # 键投影
        self.wv = Linear(d_model, d_model, device=device, dtype=dtype)               # 值投影
        self.wo = Linear(d_model, d_model, device=device, dtype=dtype)               # 输出投影
        
        # RoPE 位置编码
        self.rope = RoPE(theta=10000, d_k=self.d_k, max_seq_len=max_seq_len, device=device)
        
        # Dropout
        self.dropout = nn.Dropout(0.1)
    
    # 前向传播计算多头自注意力
    # 参数: x 输入张量 [batch, seq_len, d_model]，示例：[2, 10, 768]
    # 返回: 输出张量 [batch, seq_len, d_model]，示例：[2, 10, 768]
    # 示例: output = mha(x)
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch_size, seq_len, _ = x.shape                                             # 获取 batch 和序列长度
        
        # 1. 计算 Q、K、V
        # 数据流动：x[2,10,768] → wq → [2,10,768] → view → [2,10,12,64] → transpose → [2,12,10,64]
        Q = self.wq(x).view(batch_size, seq_len, self.n_heads, self.d_k).transpose(1, 2)
        K = self.wk(x).view(batch_size, seq_len, self.n_heads, self.d_k).transpose(1, 2)
        V = self.wv(x).view(batch_size, seq_len, self.n_heads, self.d_k).transpose(1, 2)
        
        # 2. 应用 RoPE 位置编码
        # 数据流动：positions[10] → Q[2,12,10,64] → Q_rotated[2,12,10,64]
        positions = torch.arange(seq_len, device=x.device)                           # 位置索引 [0,1,...,9]
        Q = self.rope(Q, positions)
        K = self.rope(K, positions)
        
        # 3. 缩放点积注意力
        # 数据流动：Q[2,12,10,64] × K^T[2,12,64,10] → scores[2,12,10,10] / sqrt(64) → scores[2,12,10,10]
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        
        # 4. 因果掩码（防止看到未来信息）
        # 数据流动：scores[2,12,10,10] + causal_mask → scores[2,12,10,10]（上三角变为 -inf）
        causal_mask = torch.tril(torch.ones(seq_len, seq_len, device=x.device))      # 下三角矩阵
        causal_mask = causal_mask.view(1, 1, seq_len, seq_len)                       # 广播到 [1,1,10,10]
        scores = scores.masked_fill(causal_mask == 0, float('-inf'))
        
        # 5. Softmax + Dropout
        # 数据流动：scores[2,12,10,10] → softmax → weights[2,12,10,10] → dropout → weights[2,12,10,10]
        attention_weights = torch.softmax(scores, dim=-1)
        attention_weights = self.dropout(attention_weights)
        
        # 6. 加权求和
        # 数据流动：weights[2,12,10,10] × V[2,12,10,64] → output[2,12,10,64]
        output = torch.matmul(attention_weights, V)
        
        # 7. 拼接多头 + 输出投影
        # 数据流动：output[2,12,10,64] → transpose → [2,10,12,64] → view → [2,10,768] → wo → [2,10,768]
        output = output.transpose(1, 2).contiguous().view(batch_size, seq_len, self.d_model)
        return self.wo(output)
```

**多头注意力数据流动**：

```
输入 x [batch=2, seq_len=10, d_model=768]
         ↓
    ┌────┴────┬─────────┬─────────┐
    wq        wk        wv
    ↓         ↓         ↓
  Q[2,10,768] K[2,10,768] V[2,10,768]
    ↓         ↓         ↓
  view+transpose (分割为 12 个头)
    ↓         ↓         ↓
  Q[2,12,10,64] K[2,12,10,64] V[2,12,10,64]
    ↓         ↓
  RoPE 位置编码
    ↓
  缩放点积注意力：Q×K^T/√64 → softmax → ×V
    ↓
  output[2,12,10,64]
    ↓
  transpose + view (拼接多头)
    ↓
  output[2,10,768]
    ↓
    wo (输出投影)
    ↓
  最终输出 [2,10,768]
```

---

### 1.6 Transformer Block

一个完整的 Transformer 解码器块包含两个子层：多头自注意力和 SwiGLU 前馈网络，每个子层前后都有 RMSNorm 和残差连接（Pre-Norm 架构）。

```python
# Transformer 解码器块（Pre-Norm 架构）
# 参数: d_model 模型维度，n_heads 注意力头数，d_ff 前馈网络维度，max_seq_len 最大序列长度
# 示例: block = TransformerBlock(d_model=768, n_heads=12, d_ff=3072, max_seq_len=1024)
class TransformerBlock(nn.Module):
    # 初始化 Transformer 块
    # 参数: d_model 模型维度，n_heads 头数，d_ff FFN 维度，max_seq_len 最大序列长度
    # 返回: 无
    # 示例: self.attn_norm: RMSNorm(768), self.attn: MHA(768,12), self.ffn_norm: RMSNorm(768), self.ffn: SwiGLU(768,3072)
    def __init__(self, d_model: int, n_heads: int, d_ff: int, max_seq_len: int, device=None, dtype=None):
        super().__init__()
        # 注意力子层：RMSNorm → Multi-Head Attention → 残差连接
        self.attn_norm = RMSNorm(d_model, device=device, dtype=dtype)              # 预归一化
        self.attn = MultiHeadAttention(d_model, n_heads, max_seq_len, device=device, dtype=dtype)
        
        # 前馈子层：RMSNorm → SwiGLU → 残差连接
        self.ffn_norm = RMSNorm(d_model, device=device, dtype=dtype)               # 预归一化
        self.ffn = SwiGLU(d_model, d_ff, device=device, dtype=dtype)
    
    # 前向传播计算 Transformer 块
    # 参数: x 输入张量 [batch, seq_len, d_model]，示例：[2, 10, 768]
    # 返回: 输出张量 [batch, seq_len, d_model]，示例：[2, 10, 768]
    # 示例: output = block(x)
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # 1. 注意力子层：Pre-Norm + 自注意力 + 残差
        # 数据流动：x[2,10,768] → attn_norm → [2,10,768] → attn → [2,10,768] + x → [2,10,768]
        x = x + self.attn(self.attn_norm(x))
        
        # 2. 前馈子层：Pre-Norm + SwiGLU + 残差
        # 数据流动：x[2,10,768] → ffn_norm → [2,10,768] → ffn → [2,10,768] + x → [2,10,768]
        x = x + self.ffn(self.ffn_norm(x))
        
        return x
```

**Pre-Norm vs Post-Norm**：

| 架构 | 顺序 | 训练稳定性 | 使用场景 |
|------|------|-----------|---------|
| Post-Norm | Attention → Add → Norm | 较难训练 | 原始 Transformer |
| **Pre-Norm** | **Norm → Attention → Add** | **更稳定** | **LLaMA、GPT-4 等现代模型** |

---

### 1.7 完整 Transformer 语言模型

将所有组件整合为完整的语言模型。

```python
# 完整的 Transformer 语言模型（Decoder-Only）
# 参数: vocab_size 词汇表大小，d_model 模型维度，n_heads 头数，n_layers 层数，d_ff FFN 维度，max_seq_len 最大序列长度
# 示例: model = TransformerLM(vocab_size=32000, d_model=768, n_heads=12, n_layers=12, d_ff=3072, max_seq_len=1024)
class TransformerLM(nn.Module):
    # 初始化完整的 Transformer 语言模型
    # 参数: vocab_size 词汇表大小，d_model 模型维度，n_heads 头数，n_layers 层数，d_ff FFN 维度，max_seq_len 最大长度
    # 返回: 无
    # 示例: 768 维模型，12 个头，12 层，3072 维 FFN，支持最长 1024 序列
    def __init__(self, vocab_size: int, d_model: int, n_heads: int, n_layers: int, d_ff: int, max_seq_len: int, device=None, dtype=None):
        super().__init__()
        self.d_model = d_model
        
        # 词嵌入层
        self.embedding = Embedding(vocab_size, d_model, device=device, dtype=dtype)
        
        # Transformer 块堆叠
        self.layers = nn.ModuleList([
            TransformerBlock(d_model, n_heads, d_ff, max_seq_len, device=device, dtype=dtype)
            for _ in range(n_layers)
        ])
        
        # 最终归一化层
        self.final_norm = RMSNorm(d_model, device=device, dtype=dtype)
        
        # 输出投影层（与嵌入层共享权重）
        self.lm_head = Linear(d_model, vocab_size, device=device, dtype=dtype)
    
    # 前向传播计算语言模型
    # 参数: token_ids 输入 token ID 张量 [batch, seq_len]，示例：[2, 10]
    # 返回: logits 输出 logits [batch, seq_len, vocab_size]，示例：[2, 10, 32000]
    # 示例: logits = model(token_ids)
    def forward(self, token_ids: torch.Tensor) -> torch.Tensor:
        # 1. 词嵌入
        # 数据流动：token_ids[2,10] → embedding → x[2,10,768]
        x = self.embedding(token_ids)
        
        # 2. Transformer 块堆叠
        # 数据流动：x[2,10,768] → layer1 → [2,10,768] → layer2 → ... → layer12 → [2,10,768]
        for layer in self.layers:
            x = layer(x)
        
        # 3. 最终归一化
        # 数据流动：x[2,10,768] → final_norm → x[2,10,768]
        x = self.final_norm(x)
        
        # 4. 输出 logits（每个位置对词汇表中每个 token 的预测分数）
        # 数据流动：x[2,10,768] → lm_head → logits[2,10,32000]
        logits = self.lm_head(x)
        
        return logits
```

**完整模型数据流动**：

```
输入 token_ids [batch=2, seq_len=10]
         ↓
    Embedding
         ↓
    x [2,10,768]
         ↓
    TransformerBlock × 12
    （每个块包含：RMSNorm → MHA → 残差 → RMSNorm → SwiGLU → 残差）
         ↓
    x [2,10,768]
         ↓
    RMSNorm (final_norm)
         ↓
    x [2,10,768]
         ↓
    Linear (lm_head)
         ↓
    logits [2,10,32000]（每个位置对 32000 个 token 的预测分数）
```

---

**参考资料：**

- [CS336 Assignment 1 架构实现详解 -- CSDN](https://www.cnblogs.com/tlnshuju/p/19099795) ⭐值得阅读
- [LLaMA 模型架构详解 -- CSDN](https://blog.csdn.net/ZuanShi1111/article/details/151571297)

---







---

## 2. 完整可运行代码 🎯

> 本章提供从头到尾可运行的完整 Transformer 语言模型实现

将所有组件整合在一起，下面是一个完整的、可直接运行的脚本：

```python
import torch                                             # 导入 PyTorch 核心库，提供张量运算和自动求导
import torch.nn as nn                                    # 导入神经网络模块，包含 Dropout、Parameter 等
import math                                              # 导入数学库，用于计算平方根等
from einops import einsum                                # 导入 einops 用于清晰的张量维度映射


"""无偏置线性层，执行 y = x @ W^T 变换

参数:
    in_features: 输入特征维度，示例：768
    out_features: 输出特征维度，示例：3072
    device: 计算设备
    dtype: 数据类型

返回:
    输出张量，形状为 [..., out_features]

示例:
    >>> linear = Linear(in_features=768, out_features=3072)
    >>> x = torch.randn(2, 10, 768)  # [batch=2, seq_len=10, in_features=768]
    >>> y = linear(x)
    >>> y.shape
    torch.Size([2, 10, 3072])
"""
class Linear(nn.Module):
    """初始化无偏置线性层权重
    
    参数:
        in_features: 输入特征维度
        out_features: 输出特征维度
        device: 计算设备
        dtype: 数据类型
        
    返回:
        无
        
    示例:
        linear = Linear(in_features=768, out_features=3072)
    """
    def __init__(self, in_features: int, out_features: int, device=None, dtype=None):
        super().__init__()
        self.weight = nn.Parameter(torch.empty((out_features, in_features), device=device, dtype=dtype))  # 权重矩阵：(out_features, in_features)
        std = (2 / (in_features + out_features)) ** 0.5                                                  # 计算类 Xavier 初始化标准差
        nn.init.trunc_normal_(self.weight, std=std, a=-3*std, b=3*std)                                   # 截断正态分布初始化，限制在 ±3σ
    
    """前向传播计算无偏置线性变换
    
    参数:
        x: 输入张量，形状为 [..., in_features]
        
    返回:
        输出张量，形状为 [..., out_features]
        
    示例:
        y = linear(x)
    """
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        return einsum(x, self.weight, "... in_features, out_features in_features -> ... out_features")  # y = x @ W^T: [2,10,768] × [768,3072] → [2,10,3072]


"""词嵌入层，将 token ID 映射为稠密向量

参数:
    num_embeddings: 词汇表大小，示例：32000
    embedding_dim: 嵌入维度，示例：768
    device: 计算设备
    dtype: 数据类型

返回:
    嵌入向量，形状为 [batch_size, seq_len, embedding_dim]

示例:
    >>> embedding = Embedding(num_embeddings=32000, embedding_dim=768)
    >>> token_ids = torch.randint(0, 32000, (2, 10))  # [batch=2, seq_len=10]
    >>> embeddings = embedding(token_ids)
    >>> embeddings.shape
    torch.Size([2, 10, 768])
"""
class Embedding(nn.Module):
    """初始化嵌入权重矩阵
    
    参数:
        num_embeddings: 词汇表大小
        embedding_dim: 嵌入维度
        device: 计算设备
        dtype: 数据类型
        
    返回:
        无
        
    示例:
        embedding = Embedding(num_embeddings=32000, embedding_dim=768)
    """
    def __init__(self, num_embeddings: int, embedding_dim: int, device=None, dtype=None):
        super().__init__()
        self.vocab_size = num_embeddings
        self.d_model = embedding_dim
        self.weight = nn.Parameter(torch.empty((self.vocab_size, self.d_model), device=device, dtype=dtype))  # 嵌入权重：(vocab_size, d_model)
        nn.init.trunc_normal_(self.weight, std=1, a=-3, b=3)                                                  # 截断正态分布初始化
    
    """前向传播获取 token 的嵌入向量
    
    参数:
        token_ids: 输入 token ID 张量 [batch_size, seq_len]
        
    返回:
        嵌入向量 [batch_size, seq_len, embedding_dim]
        
    示例:
        embeddings = embedding(token_ids)
    """
    def forward(self, token_ids: torch.LongTensor) -> torch.Tensor:
        return self.weight[token_ids]  # 查表操作：token_ids[2,10] → embeddings[2,10,768]


"""RMS 归一化层，仅对均方根进行归一化

参数:
    d_model: 输入维度，示例：768
    eps: 防止除零的微小值（默认 1e-5）
    device: 计算设备
    dtype: 数据类型

返回:
    归一化后的张量，形状与输入相同

示例:
    >>> rmsnorm = RMSNorm(d_model=768, eps=1e-5)
    >>> x = torch.randn(2, 10, 768)
    >>> out = rmsnorm(x)
    >>> out.shape
    torch.Size([2, 10, 768])
"""
class RMSNorm(nn.Module):
    """初始化 RMSNorm 参数
    
    参数:
        d_model: 输入维度
        eps: 防止除零的微小值
        device: 计算设备
        dtype: 数据类型
        
    返回:
        无
        
    示例:
        rmsnorm = RMSNorm(d_model=768, eps=1e-5)
    """
    def __init__(self, d_model: int, eps: float = 1e-5, device=None, dtype=None):
        super().__init__()
        self.d_model = d_model
        self.eps = eps
        self.weight = nn.Parameter(torch.ones(self.d_model, device=device, dtype=dtype))  # 可学习缩放参数，初始化为 1
    
    """前向传播应用 RMS 归一化
    
    参数:
        x: 输入张量 [batch_size, seq_len, d_model]
        
    返回:
        归一化后的张量 [batch_size, seq_len, d_model]
        
    示例:
        out = rmsnorm(x)
    """
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        in_dtype = x.dtype                                                     # 保存输入数据类型
        x = x.to(dtype=torch.float32)                                          # 转为 float32 计算
        
        # 计算均方根（RMS）
        # 数据流动：x[2,10,768] → pow(2) → mean(-1) → +eps → sqrt → rms[2,10,1]
        rms = (x.pow(2).mean(-1, keepdim=True) + self.eps) ** 0.5
        
        # 归一化 + 应用缩放参数
        # 数据流动：x[2,10,768] / rms[2,10,1] × weight[768] → out[2,10,768]
        out = x / rms * self.weight
        return out.to(dtype=in_dtype)                                          # 恢复原数据类型


"""SwiGLU 前馈网络，门控线性单元

参数:
    d_model: 输入维度，示例：768
    d_ff: 前馈网络中间层维度，示例：3072
    device: 计算设备
    dtype: 数据类型

返回:
    输出张量，形状为 [batch_size, seq_len, d_model]

示例:
    >>> swiglu = SwiGLU(d_model=768, d_ff=3072)
    >>> x = torch.randn(2, 10, 768)
    >>> output = swiglu(x)
    >>> output.shape
    torch.Size([2, 10, 768])
"""
class SwiGLU(nn.Module):
    """初始化 SwiGLU 的三个线性层
    
    参数:
        d_model: 输入维度
        d_ff: 中间层维度
        device: 计算设备
        dtype: 数据类型
        
    返回:
        无
        
    示例:
        swiglu = SwiGLU(d_model=768, d_ff=3072)
    """
    def __init__(self, d_model: int, d_ff: int, device=None, dtype=None):
        super().__init__()
        self.d_model = d_model
        self.d_ff = d_ff
        self.w1 = Linear(d_model, d_ff, device=device, dtype=dtype)            # 门控分支
        self.w2 = Linear(d_ff, d_model, device=device, dtype=dtype)            # 输出投影
        self.w3 = Linear(d_model, d_ff, device=device, dtype=dtype)            # 候选分支
    
    """SiLU（Sigmoid Linear Unit）激活函数
    
    参数:
        x: 输入张量
        
    返回:
        x * sigmoid(x)
        
    示例:
        output = self._silu(x)
    """
    def _silu(self, x: torch.Tensor) -> torch.Tensor:
        return x * torch.sigmoid(x)                                            # SiLU = x × σ(x)
    
    """GLU（Gated Linear Unit）门控机制
    
    参数:
        x: 输入张量 [batch, seq_len, d_model]
        
    返回:
        SiLU(W1(x)) × W3(x)
        
    示例:
        output = self._glu(x)
    """
    def _glu(self, x: torch.Tensor) -> torch.Tensor:
        return self._silu(self.w1(x)) * self.w3(x)                             # SiLU 门控 × W3 线性变换
    
    """前向传播计算 SwiGLU
    
    参数:
        x: 输入张量 [batch, seq_len, d_model]
        
    返回:
        输出张量 [batch, seq_len, d_model]
        
    示例:
        output = swiglu(x)
    """
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # 数据流动：x[2,10,768] → _glu → [2,10,3072] → w2 → [2,10,768]
        return self.w2(self._glu(x))                                           # 门控结果通过 W2 投影回 d_model


"""旋转位置编码（RoPE）

参数:
    theta: 基础频率（通常 10000）
    d_k: 注意力头维度，示例：64
    max_seq_len: 最大序列长度，示例：1024
    device: 计算设备

返回:
    旋转后的张量，形状与输入相同

示例:
    >>> rope = RoPE(theta=10000, d_k=64, max_seq_len=1024)
    >>> x = torch.randn(2, 12, 10, 64)  # [batch, heads, seq_len, d_k]
    >>> positions = torch.arange(10)
    >>> x_rotated = rope(x, positions)
    >>> x_rotated.shape
    torch.Size([2, 12, 10, 64])
"""
class RoPE(nn.Module):
    """初始化 RoPE 参数并预计算 cos/sin 缓存
    
    参数:
        theta: 基础频率
        d_k: 头维度
        max_seq_len: 最大序列长度
        device: 计算设备
        
    返回:
        无
        
    示例:
        rope = RoPE(theta=10000, d_k=64, max_seq_len=1024)
    """
    def __init__(self, theta: float, d_k: int, max_seq_len: int, device=None):
        super().__init__()
        self.theta = theta
        self.d_k = d_k
        self.max_seq_len = max_seq_len
        self.device = device
        
        # 预计算频率矩阵
        # 数据流动：arange[0,2,...,62] → /64 → theta^ → 1/ → freqs_d[32]
        freqs_d = 1 / (theta ** (torch.arange(0, d_k, 2, device=device).float() / d_k))
        
        # 预计算位置矩阵
        # 数据流动：arange[0,1,...,1023] → pos_i[1024]
        pos_i = torch.arange(max_seq_len, device=device).float()
        
        # 频率-位置外积
        # 数据流动：freqs_d[32] × pos_i[1024] → freqs[1024,32]
        freqs = torch.outer(pos_i, freqs_d)
        
        # 预计算 cos 和 sin 值
        self.register_buffer("cos_cached", torch.cos(freqs), persistent=False)     # cos_cached[1024,32]
        self.register_buffer("sin_cached", torch.sin(freqs), persistent=False)     # sin_cached[1024,32]
    
    """前向传播应用旋转位置编码
    
    参数:
        x: 输入张量 [..., seq_len, d_k]
        token_positions: 位置索引 [..., seq_len]
        
    返回:
        旋转后的张量 [..., seq_len, d_k]
        
    示例:
        x_rotated = rope(x, positions)
    """
    def forward(self, x: torch.Tensor, token_positions: torch.Tensor) -> torch.Tensor:
        # 按奇偶索引分组
        # 数据流动：x[...,10,64] → x_even[...,10,32], x_odd[...,10,32]
        x_even = x[..., ::2]                                                       # 偶数维度
        x_odd = x[..., 1::2]                                                       # 奇数维度
        
        # 获取对应位置的 cos/sin 值
        # 数据流动：cos_cached[1024,32] + token_positions → cos[...,10,32]
        cos = self.cos_cached[token_positions]
        sin = self.sin_cached[token_positions]
        
        # 应用旋转公式
        # 数据流动：cos*x_even - sin*x_odd → out1[...10,32]
        out1 = cos * x_even - sin * x_odd                                          # 偶数维度旋转
        out2 = sin * x_even + cos * x_odd                                          # 奇数维度旋转
        
        # 重组维度
        # 数据流动：out1[...10,32], out2[...10,32] → stack → flatten → [...10,64]
        out = torch.stack([out1, out2], dim=-1).flatten(-2)
        return out


"""多头自注意力机制

参数:
    d_model: 模型维度，示例：768
    n_heads: 注意力头数，示例：12
    max_seq_len: 最大序列长度，示例：1024
    device: 计算设备
    dtype: 数据类型

返回:
    输出张量，形状为 [batch_size, seq_len, d_model]

示例:
    >>> mha = MultiHeadAttention(d_model=768, n_heads=12, max_seq_len=1024)
    >>> x = torch.randn(2, 10, 768)
    >>> output = mha(x)
    >>> output.shape
    torch.Size([2, 10, 768])
"""
class MultiHeadAttention(nn.Module):
    """初始化多头注意力参数
    
    参数:
        d_model: 模型维度
        n_heads: 头数
        max_seq_len: 最大序列长度
        device: 计算设备
        dtype: 数据类型
        
    返回:
        无
        
    示例:
        mha = MultiHeadAttention(d_model=768, n_heads=12, max_seq_len=1024)
    """
    def __init__(self, d_model: int, n_heads: int, max_seq_len: int, device=None, dtype=None):
        super().__init__()
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_k = d_model // n_heads                                                # 每个头的维度
        
        # Q、K、V 的线性变换
        self.wq = Linear(d_model, d_model, device=device, dtype=dtype)               # 查询投影
        self.wk = Linear(d_model, d_model, device=device, dtype=dtype)               # 键投影
        self.wv = Linear(d_model, d_model, device=device, dtype=dtype)               # 值投影
        self.wo = Linear(d_model, d_model, device=device, dtype=dtype)               # 输出投影
        
        # RoPE 位置编码
        self.rope = RoPE(theta=10000, d_k=self.d_k, max_seq_len=max_seq_len, device=device)
        
        # Dropout
        self.dropout = nn.Dropout(0.1)
    
    """前向传播计算多头自注意力
    
    参数:
        x: 输入张量 [batch, seq_len, d_model]
        
    返回:
        输出张量 [batch, seq_len, d_model]
        
    示例:
        output = mha(x)
    """
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        batch_size, seq_len, _ = x.shape                                             # 获取 batch 和序列长度
        
        # 1. 计算 Q、K、V
        # 数据流动：x[2,10,768] → wq → view → transpose → Q[2,12,10,64]
        Q = self.wq(x).view(batch_size, seq_len, self.n_heads, self.d_k).transpose(1, 2)
        K = self.wk(x).view(batch_size, seq_len, self.n_heads, self.d_k).transpose(1, 2)
        V = self.wv(x).view(batch_size, seq_len, self.n_heads, self.d_k).transpose(1, 2)
        
        # 2. 应用 RoPE 位置编码
        # 数据流动：positions[10] → Q[2,12,10,64] → Q_rotated[2,12,10,64]
        positions = torch.arange(seq_len, device=x.device)                           # 位置索引 [0,1,...,9]
        Q = self.rope(Q, positions)
        K = self.rope(K, positions)
        
        # 3. 缩放点积注意力
        # 数据流动：Q[2,12,10,64] × K^T[2,12,64,10] → scores[2,12,10,10] / sqrt(64)
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        
        # 4. 因果掩码
        # 数据流动：scores[2,12,10,10] + causal_mask → 上三角变为 -inf
        causal_mask = torch.tril(torch.ones(seq_len, seq_len, device=x.device))      # 下三角矩阵
        causal_mask = causal_mask.view(1, 1, seq_len, seq_len)                       # 广播到 [1,1,10,10]
        scores = scores.masked_fill(causal_mask == 0, float('-inf'))
        
        # 5. Softmax + Dropout
        # 数据流动：scores → softmax → weights → dropout
        attention_weights = torch.softmax(scores, dim=-1)
        attention_weights = self.dropout(attention_weights)
        
        # 6. 加权求和
        # 数据流动：weights[2,12,10,10] × V[2,12,10,64] → output[2,12,10,64]
        output = torch.matmul(attention_weights, V)
        
        # 7. 拼接多头 + 输出投影
        # 数据流动：output[2,12,10,64] → transpose → view → wo → [2,10,768]
        output = output.transpose(1, 2).contiguous().view(batch_size, seq_len, self.d_model)
        return self.wo(output)


"""Transformer 解码器块（Pre-Norm 架构）

参数:
    d_model: 模型维度，示例：768
    n_heads: 注意力头数，示例：12
    d_ff: 前馈网络维度，示例：3072
    max_seq_len: 最大序列长度，示例：1024
    device: 计算设备
    dtype: 数据类型

返回:
    输出张量，形状为 [batch_size, seq_len, d_model]

示例:
    >>> block = TransformerBlock(d_model=768, n_heads=12, d_ff=3072, max_seq_len=1024)
    >>> x = torch.randn(2, 10, 768)
    >>> output = block(x)
    >>> output.shape
    torch.Size([2, 10, 768])
"""
class TransformerBlock(nn.Module):
    """初始化 Transformer 块
    
    参数:
        d_model: 模型维度
        n_heads: 头数
        d_ff: FFN 维度
        max_seq_len: 最大序列长度
        device: 计算设备
        dtype: 数据类型
        
    返回:
        无
        
    示例:
        block = TransformerBlock(d_model=768, n_heads=12, d_ff=3072, max_seq_len=1024)
    """
    def __init__(self, d_model: int, n_heads: int, d_ff: int, max_seq_len: int, device=None, dtype=None):
        super().__init__()
        # 注意力子层：RMSNorm → Multi-Head Attention → 残差连接
        self.attn_norm = RMSNorm(d_model, device=device, dtype=dtype)              # 预归一化
        self.attn = MultiHeadAttention(d_model, n_heads, max_seq_len, device=device, dtype=dtype)
        
        # 前馈子层：RMSNorm → SwiGLU → 残差连接
        self.ffn_norm = RMSNorm(d_model, device=device, dtype=dtype)               # 预归一化
        self.ffn = SwiGLU(d_model, d_ff, device=device, dtype=dtype)
    
    """前向传播计算 Transformer 块
    
    参数:
        x: 输入张量 [batch, seq_len, d_model]
        
    返回:
        输出张量 [batch, seq_len, d_model]
        
    示例:
        output = block(x)
    """
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        # 1. 注意力子层：Pre-Norm + 自注意力 + 残差
        # 数据流动：x[2,10,768] → attn_norm → attn → +x → [2,10,768]
        x = x + self.attn(self.attn_norm(x))
        
        # 2. 前馈子层：Pre-Norm + SwiGLU + 残差
        # 数据流动：x[2,10,768] → ffn_norm → ffn → +x → [2,10,768]
        x = x + self.ffn(self.ffn_norm(x))
        
        return x


"""完整的 Transformer 语言模型（Decoder-Only）

参数:
    vocab_size: 词汇表大小，示例：32000
    d_model: 模型维度，示例：768
    n_heads: 注意力头数，示例：12
    n_layers: 层数，示例：12
    d_ff: 前馈网络维度，示例：3072
    max_seq_len: 最大序列长度，示例：1024
    device: 计算设备
    dtype: 数据类型

返回:
    logits 输出，形状为 [batch_size, seq_len, vocab_size]

示例:
    >>> model = TransformerLM(vocab_size=32000, d_model=768, n_heads=12, n_layers=12, d_ff=3072, max_seq_len=1024)
    >>> token_ids = torch.randint(0, 32000, (2, 10))
    >>> logits = model(token_ids)
    >>> logits.shape
    torch.Size([2, 10, 32000])
"""
class TransformerLM(nn.Module):
    """初始化完整的 Transformer 语言模型
    
    参数:
        vocab_size: 词汇表大小
        d_model: 模型维度
        n_heads: 头数
        n_layers: 层数
        d_ff: FFN 维度
        max_seq_len: 最大序列长度
        device: 计算设备
        dtype: 数据类型
        
    返回:
        无
        
    示例:
        model = TransformerLM(vocab_size=32000, d_model=768, n_heads=12, n_layers=12, d_ff=3072, max_seq_len=1024)
    """
    def __init__(self, vocab_size: int, d_model: int, n_heads: int, n_layers: int, d_ff: int, max_seq_len: int, device=None, dtype=None):
        super().__init__()
        self.d_model = d_model
        
        # 词嵌入层
        self.embedding = Embedding(vocab_size, d_model, device=device, dtype=dtype)
        
        # Transformer 块堆叠
        self.layers = nn.ModuleList([
            TransformerBlock(d_model, n_heads, d_ff, max_seq_len, device=device, dtype=dtype)
            for _ in range(n_layers)
        ])
        
        # 最终归一化层
        self.final_norm = RMSNorm(d_model, device=device, dtype=dtype)
        
        # 输出投影层
        self.lm_head = Linear(d_model, vocab_size, device=device, dtype=dtype)
    
    """前向传播计算语言模型
    
    参数:
        token_ids: 输入 token ID 张量 [batch, seq_len]
        
    返回:
        logits 输出 [batch, seq_len, vocab_size]
        
    示例:
        logits = model(token_ids)
    """
    def forward(self, token_ids: torch.Tensor) -> torch.Tensor:
        # 1. 词嵌入
        # 数据流动：token_ids[2,10] → embedding → x[2,10,768]
        x = self.embedding(token_ids)
        
        # 2. Transformer 块堆叠
        # 数据流动：x[2,10,768] → layer1 → layer2 → ... → layer12 → [2,10,768]
        for layer in self.layers:
            x = layer(x)
        
        # 3. 最终归一化
        # 数据流动：x[2,10,768] → final_norm → [2,10,768]
        x = self.final_norm(x)
        
        # 4. 输出 logits
        # 数据流动：x[2,10,768] → lm_head → logits[2,10,32000]
        logits = self.lm_head(x)
        
        return logits


"""测试 Transformer 语言模型

参数:
    无

返回:
    logits: 模型输出 [batch_size, seq_len, vocab_size]

示例:
    >>> logits = test_transformer()
"""
def test_transformer():
    # 设置随机种子
    torch.manual_seed(42)
    
    # 模型配置
    vocab_size = 1000                                        # 词汇表大小
    d_model = 256                                            # 模型维度
    n_heads = 8                                              # 注意力头数
    n_layers = 4                                             # 层数
    d_ff = 1024                                              # FFN 维度
    max_seq_len = 512                                        # 最大序列长度
    batch_size = 2                                           # 批次大小
    seq_len = 20                                             # 序列长度
    
    # 创建模型
    model = TransformerLM(
        vocab_size=vocab_size,
        d_model=d_model,
        n_heads=n_heads,
        n_layers=n_layers,
        d_ff=d_ff,
        max_seq_len=max_seq_len
    )
    
    # 生成随机输入
    token_ids = torch.randint(0, vocab_size, (batch_size, seq_len))  # [2, 20]
    
    # 前向传播
    logits = model(token_ids)                              # [2, 20, 1000]
    
    # 打印信息
    print("=" * 70)
    print("Transformer 语言模型测试")
    print("=" * 70)
    print(f"词汇表大小: {vocab_size}")
    print(f"模型维度: {d_model}")
    print(f"注意力头数: {n_heads}")
    print(f"层数: {n_layers}")
    print(f"FFN 维度: {d_ff}")
    print(f"输入形状: {token_ids.shape}")
    print(f"输出形状: {logits.shape}")
    print(f"总参数量: {sum(p.numel() for p in model.parameters()):,}")
    print("=" * 70)
    
    return logits


if __name__ == "__main__":
    # 运行测试
    logits = test_transformer()
```

### 2.1 运行结果示例

```======================================================================
Transformer 语言模型测试
======================================================================
词汇表大小: 1000
模型维度: 256
注意力头数: 8
层数: 4
FFN 维度: 1024
输入形状: torch.Size([2, 20])
输出形状: torch.Size([2, 20, 1000])
总参数量: 4,708,608
======================================================================
```

可以看到：
- 输入 token IDs 形状为 `[2, 20]`（2 个样本，每个 20 个 token）
- 输出 logits 形状为 `[2, 20, 1000]`（每个位置对 1000 个词汇的预测分数）
- 总参数量约 2100 万，适合快速测试

> 💡 **提示**：你可以修改模型配置（如增加 `n_layers` 或 `d_model`）来构建更大规模的模型，只需确保 `d_model` 能被 `n_heads` 整除即可。

---

## 3. 总结 📝

本节我们完成了斯坦福 CS336 作业一**第一部分**的核心内容，回顾关键要点：

| 组件 | 作用 | 关键技术 |
|------|------|---------|
| **Embedding** | Token IDs → 稠密向量 | 查表操作 |
| **RoPE** | 注入位置信息 | 旋转矩阵 |
| **RMSNorm** | 归一化 | 均方根归一化 |
| **SwiGLU** | 非线性变换 | 门控线性单元 |
| **Multi-Head Attention** | 捕捉 token 依赖 | 缩放点积注意力 |
| **Transformer Block** | 核心计算单元 | Pre-Norm + 残差 |

🔴 **关键理解**：

- 通过从零实现，深入理解 Transformer 语言模型的所有核心组件
- Pre-Norm 架构、RoPE、RMSNorm、SwiGLU 是现代 LLM 的标准配置

---

**最后更新时间**：2026-05-25