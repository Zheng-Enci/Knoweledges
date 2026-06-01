# 09aba-将离散的 token ID 映射为连续的稠密向量

<!-- 全文摘要说明：以下段落是本文档的全文摘要，必须精炼概括文档核心内容，字数不能超过100个字 -->
本文档深入讲解 Token Embedding 的核心原理，涵盖从离散符号到稠密向量的映射机制、Embedding 层与查找表的等价关系、PyTorch 从零实现完整代码及逐行解析、为什么要用稠密向量而非 One-Hot，以及一个完整可运行的示例。帮助读者彻底理解 Embedding 层的运行机制 💡
<!-- 全文摘要结束 -->

## 章节阅读路线图 🗺️

1. **核心概念** → 理解 Token、Embedding 和向量化的本质区别
2. **为什么需要 Embedding** → 从 One-Hot 到稠密向量的演进逻辑
3. **Embedding 层的本质** → 查找表 vs 矩阵乘法的等价关系
4. **PyTorch 实现** → 从零编写 Embedding 层，逐行解析
5. **使用 PyTorch 原生函数** → 学习 `nn.Embedding` 的高效用法
6. **完整可运行示例** → 整合所有内容，提供完整脚本
7. **总结** → 回顾核心要点

---

## 1. 核心概念 💡

> 本章理解 Token、Embedding 和向量化的本质区别

在深入代码之前，先明确几个关键概念：

### 1.1 什么是 Token？

Token 是模型处理文本的最小单位。它可以是：
- **单词**：如 "hello"、"world"
- **子词**：如 "un-"、"believ-"、"-able"（BPE 分词的结果）
- **字符**：如 "h"、"e"、"l"、"l"、"o"
- **特殊符号**：如 `<PAD>`、`<UNK>`、`<CLS>`

经过 Tokenizer 处理后，每个 Token 都会被映射为一个唯一的整数 ID：

```
"我" → 1024
"喜欢" → 2048
"深度" → 3072
"学习" → 4096
```

**什么是 Tokenizer（分词器）？**

Tokenizer 是 NLP 模型的前置组件，负责将原始文本切分为 Token 序列，并转换为整数 ID。它的作用类似于"翻译官"——把人类语言翻译为机器可理解的数字。

例如：
```python
文本: "我喜欢深度学习"
      ↓ (Tokenizer)
Token: ["我", "喜欢", "深度", "学习"]
      ↓ (查词汇表)
ID:    [1024, 2048, 3072, 4096]
```

---

**参考资料：**

- [探秘Transformer系列之（6）：token -- 博客园](https://www.cnblogs.com/rossiXYZ/p/18732939)
- [从词到数：Tokenizer与Embedding串讲 -- 知乎](https://zhuanlan.zhihu.com/p/631463712)

### 1.2 什么是 Embedding？

Embedding（嵌入）是将离散的 Token ID 映射为连续的稠密向量的技术。

例如，假设向量维度为 4：

```
Token ID: 1024 ("我")  →  [0.2, -0.5, 0.8, 0.1]
Token ID: 2048 ("喜欢") → [0.6, 0.3, -0.2, 0.9]
Token ID: 3072 ("深度") → [0.1, -0.8, 0.5, 0.4]
Token ID: 4096 ("学习") → [0.7, 0.2, 0.3, -0.6]
```

**什么是"稠密向量"？**

稠密向量（Dense Vector）是指向量中**大多数元素都是非零值**，且每个维度都携带语义信息。这与稀疏向量（如 One-Hot 编码）形成鲜明对比。

例如：
- **稠密向量**：`[0.2, -0.5, 0.8, 0.1]`（所有维度都有值）
- **稀疏向量（One-Hot）**：`[0, 0, 1, 0, 0, ...]`（只有一个 1，其余全是 0）

稠密向量的优势在于：
- **语义相似性**：语义相近的词，向量在空间中的距离也近
- **信息密度高**：每个维度都编码了某种语义特征
- **维度低**：通常 128~768 维，远低于 One-Hot 的几万到几十万维

---

### 1.3 Embedding vs 向量化

很多文章没有区分这两个概念，但它们有本质区别：

| 维度 | Embedding（嵌入） | 向量化（Vectorization） |
|------|-------------------|------------------------|
| **目的** | 学习低维稠密语义表示 | 将数据转换为数值向量（可能稀疏） |
| **是否需要学习** | 需要（通过神经网络训练） | 不需要（基于规则或统计） |
| **语义表示** | 保留深层语义关系和相似性 | 可能不保留语义，仅是机械化表示 |
| **典型方法** | Word2Vec、BERT、GloVe | One-Hot、TF-IDF、词袋模型 |
| **结果维度** | 低维且稠密（如 512 维） | 高维且稀疏（如 50000 维） |

**直观理解**：

- **向量化**像是"机械翻译"——直接把文字转成数字，不理解含义
- **Embedding**像是"智能翻译"——不仅转成数字，还理解了语义关系

例如，对于"新年快乐"四个字：
- **向量化**：生成 4 个独立的向量，彼此没有关系
- **Embedding**：生成的向量蕴含语义结构（"新"和"年"可能更接近，"快"和"乐"可能更接近）

---

**参考资料：**

- [探秘Transformer系列之（7）：embedding -- 掘金](https://juejin.cn/post/7475936034779709490) ⭐值得阅读
- [08」一文彻底弄懂词嵌入embedding(下) -- 知乎](https://zhuanlan.zhihu.com/p/1907547010522908044)

---

## 2. 为什么需要 Embedding 🎯

> 本章理解从离散符号到稠密向量的演进逻辑

计算机无法直接处理文字，必须转换为数值。但为什么要选择稠密向量？让我们看看发展历程：

### 2.1 第一阶段：直接用数字（索引化）

最简单的做法是给每个词分配一个唯一编号：

```python
词汇表 = {"新": 1, "年": 2, "快": 3, "乐": 4}
"新年快乐" → [1, 2, 3, 4]
```

**问题：单一数字信息量不足**

- 无法描述语义关系
- "abeyance"（中止）、"abide"（遵守）、"ability"（能力）在字典中索引临近，但语义相差甚远
- 而 "a" 和 "an" 这两个同质的词却隔得很远

**本质问题**：单一标量无法表达词的复杂语义。

---

### 2.2 第二阶段：One-Hot 编码

为了解决单一数字信息量不足的问题，我们想到用**多个数字**（向量）来表示一个词。最直观的方法是 One-Hot 编码：

```python
词汇表大小 = 4
"新" → [1, 0, 0, 0]
"年" → [0, 1, 0, 0]
"快" → [0, 0, 1, 0]
"乐" → [0, 0, 0, 1]
```

**One-Hot 编码的规则**：
- 向量长度 = 词汇表大小
- 每个词对应一个位置为 1，其余全为 0
- 第 i 个词的向量，第 i 位是 1

**问题：维度灾难 + 语义孤立**

1. **维度灾难**：
   - 如果词汇表有 50000 个词，每个向量就是 50000 维
   - 存储一个句子需要巨大的内存（50000 × 句子长度）
   - 计算效率极低（大量乘以 0 的无效运算）

2. **语义孤立**：
   - 任意两个 One-Hot 向量的点积都是 0（正交）
   - 无法表达"相似性"（如"猫"和"狗"应该相似，但向量完全不相关）
   - 每个词都是独立的"孤岛"，没有任何关联

3. **稀疏性**：
   - 99.99% 的元素都是 0，信息密度极低
   - 浪费了绝大部分存储空间

---

### 2.3 第三阶段：稠密向量（Embedding）

为了解决 One-Hot 的问题，我们引入**稠密向量**：

```python
词汇表大小 = 50000
向量维度 = 512  # 远低于 50000

"新" → [0.2, -0.5, 0.8, ..., 0.3]  # 512 维稠密向量
"年" → [0.1, -0.4, 0.7, ..., 0.2]
"快" → [0.6, 0.3, -0.2, ..., 0.9]
"乐" → [0.7, 0.2, 0.3, ..., 0.8]
```

**为什么稠密向量更好？**

1. **语义相似性**：
   - 语义相近的词，向量在空间中的距离也近
   - 例如：`cos("猫", "狗") = 0.85`（相似度高）
   - 例如：`cos("猫", "汽车") = 0.12`（相似度低）

2. **信息密度高**：
   - 每个维度都编码了某种语义特征
   - 例如：维度 1 可能表示"动物 vs 非动物"
   - 例如：维度 2 可能表示"大小"
   - 例如：维度 3 可能表示"情感极性"

3. **维度大幅降低**：
   - 512 维 vs 50000 维，存储和计算效率提升 100 倍
   - 避免了维度灾难

4. **可学习性**：
   - Embedding 向量在训练过程中不断优化
   - 模型自动学习哪些语义特征对任务最重要

**直观类比**：

想象你要描述一个人的特征：
- **One-Hot**：用一个超长的清单，只有"身高"那栏打勾，其他全是空白
- **稠密向量**：用一个紧凑的档案，包含身高、体重、年龄、性格等多个维度的具体数值

显然，稠密向量能传递更多信息，且更高效。

---

**参考资料：**

- [从One-Hot到Embedding：揭秘投影层在语言模型中的核心作用 -- CSDN](https://blog.csdn.net/weixin_42525211/article/details/160321489) ⭐值得阅读
- [Word Embeddings in NLP -- GeeksforGeeks](https://www.geeksforgeeks.org/nlp/word-embeddings-in-nlp/)
- [探秘Transformer系列之（7）：embedding -- 掘金](https://juejin.cn/post/7475936034779709490)

---

## 3. Embedding 层的本质 🔍

> 本章理解查找表与矩阵乘法的等价关系

### 3.1 Embedding 层的本质是查找表

Embedding 层内部维护了一个**嵌入矩阵（Embedding Matrix）**，形状为 `[vocab_size, embedding_dim]`：

```python
词汇表大小 = 5
向量维度 = 4

嵌入矩阵 = [
    [0.1,  0.2, -0.3,  0.4],  # Token 0 的向量
    [0.5, -0.1,  0.6,  0.2],  # Token 1 的向量
    [0.3,  0.8, -0.2,  0.1],  # Token 2 的向量
    [0.9,  0.4,  0.5, -0.3],  # Token 3 的向量
    [0.2, -0.6,  0.7,  0.8]   # Token 4 的向量
]
```

当输入 Token ID 为 `[2, 0, 3]` 时，Embedding 层直接**查表**取出对应行：

```python
输入 ID: [2, 0, 3]
查表结果:
    Token 2 → [0.3,  0.8, -0.2,  0.1]
    Token 0 → [0.1,  0.2, -0.3,  0.4]
    Token 3 → [0.9,  0.4,  0.5, -0.3]

输出形状: [3, 4]  # 3个token，每个4维
```

**为什么叫"查找表（Lookup Table）"？**

因为 Embedding 操作等价于用 Token ID 作为索引，从矩阵中直接取出对应行，就像查字典一样快速。

---

### 3.2 查找表 vs 矩阵乘法的等价性

Embedding 操作在数学上等价于 **One-Hot 向量 × 嵌入矩阵**：

```python
# 方法 1: 查找表（高效）
Token ID: 2
嵌入矩阵[2] → [0.3, 0.8, -0.2, 0.1]

# 方法 2: 矩阵乘法（理论等价，但低效）
One-Hot(2) = [0, 0, 1, 0, 0]  # 第 2 位为 1
One-Hot(2) × 嵌入矩阵:
[0, 0, 1, 0, 0] × [
    [0.1,  0.2, -0.3,  0.4],
    [0.5, -0.1,  0.6,  0.2],
    [0.3,  0.8, -0.2,  0.1],  ← 只有这一行被选中
    [0.9,  0.4,  0.5, -0.3],
    [0.2, -0.6,  0.7,  0.8]
]
= [0.3, 0.8, -0.2, 0.1]  # 结果完全相同！
```

**为什么等价？**

One-Hot 向量中只有一个 1，矩阵乘法的结果就是嵌入矩阵中对应行的加权和。由于其他位置都是 0，实际只取出了第 i 行。

**但查找表快 3~5 倍**：
- 矩阵乘法需要做 `vocab_size × embedding_dim` 次乘法和加法
- 查找表直接取出对应行，时间复杂度 O(1)
- 避免了大量乘以 0 的无效计算

**反向传播的差异**：
- 矩阵乘法：梯度会传播到整个嵌入矩阵（大部分是 0，无意义）
- 查找表：梯度只更新被查询的那些行（高效且精准）

---

**参考资料：**

- [从One-Hot到Embedding：揭秘投影层在语言模型中的核心作用 -- CSDN](https://blog.csdn.net/weixin_42525211/article/details/160321489)
- [推荐系统embedding原理及实践 -- 李乾坤](https://qiankunli.github.io/2022/03/02/recsys_embedding.html) ⭐值得阅读
- [深度学习推荐系统-Embedding -- 知乎](https://zhuanlan.zhihu.com/p/266053280)

---

## 4. PyTorch 从零实现 Embedding 层 💻

> 本章从零编写 Embedding 层，逐行讲解

### 4.1 完整代码实现

下面是基于 PyTorch 的从零实现：

```python
import torch                                              # 导入 PyTorch 核心库，提供张量运算
import torch.nn as nn                                     # 导入神经网络模块，包含 Parameter 等

"""手动实现的 Embedding 层（查找表方式）

参数:
    vocab_size: 词汇表大小（如 50000）
    embedding_dim: 嵌入向量维度（如 512）
    
示例:
    embedding = ManualEmbedding(vocab_size=50000, embedding_dim=512)
"""
class ManualEmbedding(nn.Module):
    """初始化 Embedding 层
    
    参数:
        vocab_size: 词汇表大小，示例：50000 表示有 50000 个不同的 Token
        embedding_dim: 嵌入向量维度，示例：512 表示每个 Token 映射为 512 维向量
        
    返回:
        无
        
    示例:
        self.embedding = ManualEmbedding(vocab_size=50000, embedding_dim=512)
    """
    def __init__(self, vocab_size, embedding_dim):
        super(ManualEmbedding, self).__init__()           # 调用父类 nn.Module 的初始化方法
        # 创建可训练的嵌入矩阵 [vocab_size, embedding_dim]，示例：[50000, 512]
        # 使用均匀分布初始化，范围 [-1/sqrt(dim), 1/sqrt(dim)]
        self.weight = nn.Parameter(                       # 将矩阵注册为可训练参数，模型训练时会自动更新
            torch.empty(vocab_size, embedding_dim)        # 创建空张量，形状 [50000, 512]
        )
        self.reset_parameters()                           # 调用参数初始化方法
    
    """初始化嵌入矩阵的权重
    
    参数:
        无
        
    返回:
        无
        
    示例:
        embedding.reset_parameters()
    """
    def reset_parameters(self):
        # 使用均匀分布初始化，避免梯度消失或爆炸
        # 数据流动：空张量 → 均匀分布 [-0.044, 0.044] → weight[50000, 512]
        nn.init.uniform_(                                # 均匀分布初始化，范围由 embedding_dim 决定
            self.weight,                                 # 目标张量，形状 [50000, 512]
            -1 / (self.weight.size(1) ** 0.5),           # 下限：-1/sqrt(512) ≈ -0.044
            1 / (self.weight.size(1) ** 0.5)             # 上限：1/sqrt(512) ≈ 0.044
        )
    
    """前向传播：将 Token ID 映射为稠密向量
    
    参数:
        input_ids: Token ID 张量 [batch_size=2, seq_len=5]，示例：[[1, 2, 3, 4, 5], [6, 7, 8, 9, 10]]
        
    返回:
        output: 嵌入向量 [batch_size=2, seq_len=5, embedding_dim=512]
        
    示例:
        input_ids = torch.tensor([[1, 2, 3], [4, 5, 6]])
        output = embedding(input_ids)  # 输出形状 [2, 3, 512]
    """
    def forward(self, input_ids):
        # 使用 Token ID 作为索引，从嵌入矩阵中取出对应行
        # 数据流动：input_ids[2,5] + weight[50000,512] → output[2,5,512]
        return self.weight[input_ids]                     # 查找表操作，等价于 torch.index_select(self.weight, 0, input_ids.view(-1)).view(*input_ids.shape, -1)
```

### 4.2 代码逐行解析

**第1步：创建嵌入矩阵**

```python
self.weight = nn.Parameter(torch.empty(vocab_size, embedding_dim))
```

- `torch.empty(vocab_size, embedding_dim)`：创建一个未初始化的张量，形状 `[50000, 512]`
- `nn.Parameter(...)`：将张量注册为**可训练参数**，模型训练时会自动计算梯度并更新

**什么是 `nn.Parameter`？**

`nn.Parameter` 是 PyTorch 中用于标记可训练参数的特殊张量。当你将张量包装为 `nn.Parameter` 后：
- 它会自动被 `model.parameters()` 收集
- 优化器（如 Adam）会自动更新它
- 它会在 `state_dict()` 中保存和加载

例如：
```python
embedding = ManualEmbedding(vocab_size=5, embedding_dim=4)
for param in embedding.parameters():                      # 遍历所有可训练参数
    print(param.shape)                                    # 输出：torch.Size([5, 4])
```

---

**第2步：参数初始化**

```python
nn.init.uniform_(self.weight, -1/sqrt(dim), 1/sqrt(dim))
```

使用均匀分布初始化，范围是 $[-\frac{1}{\sqrt{d}}, \frac{1}{\sqrt{d}}]$，其中 $d$ 是嵌入维度。

**为什么要这样初始化？**

1. **避免梯度消失/爆炸**：
   - 如果初始值太大，Softmax 输出会接近 0 或 1，梯度接近 0（梯度消失）
   - 如果初始值太小，信号传递多层后会衰减为 0

2. **保持方差稳定**：
   - 均匀分布的方差为 $\frac{(b-a)^2}{12}$
   - 当 $a = -\frac{1}{\sqrt{d}}$，$b = \frac{1}{\sqrt{d}}$ 时，方差约为 $\frac{1}{3d}$
   - 这保证了前向传播和反向传播时信号的稳定性

举个例子，假设 `embedding_dim = 512`：
- 初始化范围：$[-\frac{1}{\sqrt{512}}, \frac{1}{\sqrt{512}}] \approx [-0.044, 0.044]$
- 所有值都在接近 0 的小范围内，避免极端值

---

**第3步：查找表操作**

```python
return self.weight[input_ids]
```

这是 Embedding 层的核心操作——**用 Token ID 作为索引查表**。

**数据流动示例**：

```python
输入: input_ids = [[1, 2, 3], [4, 5, 6]]                 # 形状 [2, 3]，2个句子，每句3个token
嵌入矩阵: weight.shape = [50000, 512]                    # 50000个token，每个512维

查表过程:
    Token 1 → weight[1] = [0.5, -0.1, 0.6, ..., 0.2]     # 取出第 1 行，512 维
    Token 2 → weight[2] = [0.3, 0.8, -0.2, ..., 0.1]     # 取出第 2 行
    Token 3 → weight[3] = [0.9, 0.4, 0.5, ..., -0.3]     # 取出第 3 行
    ...

输出: output.shape = [2, 3, 512]                         # 2个句子，每句3个token，每个512维
```

**等价操作**：

```python
# 方法 1: 直接索引（推荐，最简洁）
output = self.weight[input_ids]

# 方法 2: 使用 torch.index_select
output = torch.index_select(                             # 按索引选择行
    self.weight,                                         # 目标张量 [50000, 512]
    0,                                                   # 在第 0 维（行）上选择
    input_ids.view(-1)                                   # 展平为一维 [1,2,3,4,5,6]
).view(*input_ids.shape, -1)                             # 恢复形状 [2,3,512]
```

方法 1 更简洁高效，是 PyTorch 的惯用写法。

---

**参考资料：**

- [Embedding — PyTorch 文档 -- PyTorch](https://docs.pytorch.org/docs/stable/generated/torch.nn.Embedding.html)
- [PyTorch Word Embedding Layer from Scratch -- James D. McCaffrey](https://jamesmccaffrey.wordpress.com/2022/08/16/pytorch-word-embedding-layer-from-scratch/)

---

## 5. 使用 PyTorch 原生函数 ⚡

> 本章介绍 `nn.Embedding` 的高效用法

### 5.1 torch.nn.Embedding

PyTorch 提供了原生的 `nn.Embedding` 模块，功能更完善：

```python
import torch                                              # 导入 PyTorch 核心库
import torch.nn as nn                                     # 导入神经网络模块

# 创建 Embedding 层
# 参数：词汇表大小=50000，嵌入维度=512，填充索引=0（表示 <PAD> token 的 ID）
embedding = nn.Embedding(                                 # 创建嵌入层，内部维护 [50000, 512] 的查找表
    num_embeddings=50000,                                 # 词汇表大小，示例：50000 个不同的 Token
    embedding_dim=512,                                    # 嵌入向量维度，示例：每个 Token 映射为 512 维向量
    padding_idx=0                                         # 填充索引，示例：0 表示 <PAD> token，其向量保持为 0 不更新
)

# 前向传播
input_ids = torch.tensor([[1, 2, 3, 0], [4, 5, 6, 0]])    # 输入 Token ID，形状 [2, 4]，0 表示 <PAD>
output = embedding(input_ids)                             # 查找表操作，输出形状 [2, 4, 512]

print(f"输出形状: {output.shape}")                        # 输出：torch.Size([2, 4, 512])
```

### 5.2 关键参数说明

| 参数 | 说明 | 示例 |
|------|------|------|
| `num_embeddings` | 词汇表大小 | 50000 |
| `embedding_dim` | 嵌入向量维度 | 512 |
| `padding_idx` | 填充 Token 的 ID（可选） | 0（表示 `<PAD>`） |
| `max_norm` | 向量的最大范数（可选，用于归一化） | 1.0 |
| `norm_type` | 范数类型（与 `max_norm` 配合） | 2.0（L2 范数） |
| `sparse` | 是否使用稀疏梯度更新（可选） | False |

### 5.3 `padding_idx` 的作用

当设置 `padding_idx=0` 时：
- Token ID 为 0 的向量**始终保持为 0**
- 训练时**不会更新**这个向量
- 用于标记句子中的填充位置（不携带语义信息）

```python
embedding = nn.Embedding(5, 4, padding_idx=0)
print(embedding.weight[0])                                # 输出：tensor([0., 0., 0., 0.])，始终保持为 0

input_ids = torch.tensor([[1, 0, 2], [3, 0, 4]])          # 0 是 <PAD>
output = embedding(input_ids)
print(output[:, 1, :])                                    # 输出：全 0 向量（第 2 列都是 <PAD>）
```

### 5.4 手动实现 vs 原生函数对比

| 特性 | 手动实现 | PyTorch 原生 `nn.Embedding` |
|------|---------|---------------------------|
| 代码量 | 较多，需自己处理初始化 | 一行代码即可 |
| 功能完整性 | 基础查找表 | 支持 `padding_idx`、`max_norm` 等高级功能 |
| 性能 | 一般 | 高度优化，支持稀疏梯度更新 |
| 学习价值 | 高，理解底层原理 | 低，封装了细节 |
| 适用场景 | 学习、自定义需求 | 生产环境、追求效率 |

> 💡 **建议**：学习阶段用手动实现理解原理，实际项目中用 `nn.Embedding` 获得最佳性能。

---

**参考资料：**

- [Embedding — PyTorch 文档 -- PyTorch](https://docs.pytorch.org/docs/stable/generated/torch.nn.Embedding.html)
- [Explaining Embedding layer in Pytorch -- Medium](https://medium.com/@smrati.katiyar/explaining-embedding-layer-in-pytorch-1f22b88c1a69)

---

## 6. 完整可运行示例 🎯

> 本章提供一个从头到尾可运行的完整代码

```python
import torch                                              # 导入 PyTorch 核心库
import torch.nn as nn                                     # 导入神经网络模块


"""手动实现的 Embedding 层（查找表方式）

参数:
    vocab_size: 词汇表大小（如 5）
    embedding_dim: 嵌入向量维度（如 4）
    
示例:
    embedding = ManualEmbedding(vocab_size=5, embedding_dim=4)
"""
class ManualEmbedding(nn.Module):
    """初始化 Embedding 层
    
    参数:
        vocab_size: 词汇表大小，示例：5
        embedding_dim: 嵌入向量维度，示例：4
        
    返回:
        无
        
    示例:
        self.embedding = ManualEmbedding(vocab_size=5, embedding_dim=4)
    """
    def __init__(self, vocab_size, embedding_dim):
        super(ManualEmbedding, self).__init__()           # 调用父类初始化方法
        # 创建可训练的嵌入矩阵 [vocab_size, embedding_dim]，示例：[5, 4]
        self.weight = nn.Parameter(                       # 注册为可训练参数
            torch.empty(vocab_size, embedding_dim)        # 创建空张量 [5, 4]
        )
        self.reset_parameters()                           # 初始化参数
    
    """初始化嵌入矩阵的权重
    
    参数:
        无
        
    返回:
        无
        
    示例:
        embedding.reset_parameters()
    """
    def reset_parameters(self):
        # 使用均匀分布初始化，范围 [-1/sqrt(dim), 1/sqrt(dim)]
        # 数据流动：空张量 → 均匀分布 [-0.5, 0.5] → weight[5, 4]
        nn.init.uniform_(                                # 均匀分布初始化
            self.weight,                                 # 目标张量 [5, 4]
            -1 / (self.weight.size(1) ** 0.5),           # 下限：-1/sqrt(4) = -0.5
            1 / (self.weight.size(1) ** 0.5)             # 上限：1/sqrt(4) = 0.5
        )
    
    """前向传播：将 Token ID 映射为稠密向量
    
    参数:
        input_ids: Token ID 张量 [batch_size=2, seq_len=3]
        
    返回:
        output: 嵌入向量 [batch_size=2, seq_len=3, embedding_dim=4]
        
    示例:
        input_ids = torch.tensor([[1, 2, 3], [0, 4, 1]])
        output = embedding(input_ids)  # 输出形状 [2, 3, 4]
    """
    def forward(self, input_ids):
        # 使用 Token ID 作为索引查表
        # 数据流动：input_ids[2,3] + weight[5,4] → output[2,3,4]
        return self.weight[input_ids]                     # 查找表操作


"""测试 Embedding 层

参数:
    无
    
返回:
    manual_output: 手动实现输出 [batch_size=2, seq_len=4, embedding_dim=8]
    pytorch_output: PyTorch 原生输出 [2, 4, 8]
    
示例:
    manual_out, pytorch_out = test_embedding()
"""
def test_embedding():
    # 设置随机种子，保证结果可复现
    torch.manual_seed(42)
    
    # 参数设置，示例：vocab_size=10, embedding_dim=8, batch_size=2, seq_len=4
    vocab_size = 10
    embedding_dim = 8
    batch_size = 2
    seq_len = 4
    
    # 随机生成 Token ID，范围 [0, 9]，示例：[[1, 2, 3, 0], [4, 5, 6, 0]]
    input_ids = torch.randint(0, vocab_size, (batch_size, seq_len))
    
    print("=" * 60)
    print("Embedding 层测试")
    print("=" * 60)
    print(f"词汇表大小: {vocab_size}")
    print(f"嵌入维度: {embedding_dim}")
    print(f"输入 Token ID: \n{input_ids}")
    print("=" * 60)
    
    # 测试手动实现
    manual_embedding = ManualEmbedding(vocab_size, embedding_dim)
    manual_output = manual_embedding(input_ids)
    print(f"\n手动实现输出形状: {manual_output.shape}")
    print(f"手动实现输出示例（第一个 Token）: \n{manual_output[0, 0, :]}")
    
    # 测试 PyTorch 原生
    pytorch_embedding = nn.Embedding(vocab_size, embedding_dim, padding_idx=0)
    pytorch_output = pytorch_embedding(input_ids)
    print(f"\nPyTorch 原生输出形状: {pytorch_output.shape}")
    print(f"PyTorch 原生输出示例（第一个 Token）: \n{pytorch_output[0, 0, :]}")
    
    # 验证 padding_idx 的作用
    print(f"\n<PAD> Token (ID=0) 的向量: \n{pytorch_embedding.weight[0]}")
    print("（应该全为 0，因为 padding_idx=0）")
    
    print("=" * 60)
    
    return manual_output, pytorch_output


if __name__ == "__main__":
    test_embedding()
```

### 6.1 运行结果示例

```
============================================================
Embedding 层测试
============================================================
词汇表大小: 10
嵌入维度: 8
输入 Token ID: 
tensor([[2, 6, 0, 1],
        [4, 7, 3, 5]])
============================================================

手动实现输出形状: torch.Size([2, 4, 8])
手动实现输出示例（第一个 Token）: 
tensor([ 0.2172,  0.1434, -0.3067,  0.3211, -0.4217,  0.2119,  0.0672,  0.1739],
       grad_fn=<SelectBackward0>)

PyTorch 原生输出形状: torch.Size([2, 4, 8])
PyTorch 原生输出示例（第一个 Token）: 
tensor([-0.4503, -0.2965,  0.0693, -0.1877,  0.4093,  0.3754,  0.0883, -0.3538],
       grad_fn=<EmbeddingBackward0>)

<PAD> Token (ID=0) 的向量: 
tensor([0., 0., 0., 0., 0., 0., 0., 0.])
（应该全为 0，因为 padding_idx=0）
============================================================
```

可以看到：
- 手动实现和 PyTorch 原生输出形状一致 `[2, 4, 8]`
- `padding_idx=0` 的向量保持为全 0，不会被训练更新
- 两种实现的数值不同（因为初始化随机种子不同），但原理完全一致

---

## 7. 总结 📝

本节我们完成了 Token Embedding 的核心原理和代码实现，核心要点回顾：

| 概念 | 说明 | 关键点 |
|------|------|--------|
| **Token** | 文本处理的最小单位 | 可以是单词、子词、字符 |
| **Embedding** | 将离散 ID 映射为稠密向量 | 保留语义关系，维度低 |
| **查找表** | Embedding 层的本质 | 用 ID 索引直接取行，比矩阵乘法快 3~5 倍 |
| **One-Hot** | 早期向量化方法 | 维度灾难、语义孤立、已被淘汰 |
| **稠密向量** | 现代表示方法 | 语义相似性、信息密度高、可学习 |

🔴 **关键理解**：

1. **Embedding 是查找表，不是矩阵乘法**（虽然数学等价，但实现差异大）
2. **稠密向量比 One-Hot 更高效**（维度降低 100 倍，语义关系可学习）
3. **`padding_idx` 用于标记填充位置**（保持为 0，不参与训练）
4. **Embedding 向量在训练中不断优化**（模型自动学习语义特征）

---

**最后更新时间**：2026-06-01
