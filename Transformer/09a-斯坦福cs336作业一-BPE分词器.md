---
trigger: manual
alwaysApply: false
---
# 09a-斯坦福 CS336 作业一：BPE 分词器 💻

本文档基于斯坦福大学 CS336（从零实现大语言模型）课程作业一，从零实现字节级 BPE（Byte Pair Encoding）分词器，涵盖算法原理、训练流程、编码解码实现及完整可运行的代码示例 🛠️

## 章节阅读路线图 🗺️

1. **环境准备** → 确认 Python 环境并导入必要库
2. **BPE算法原理** → 理解字节级 BPE 核心思想
3. **BPE分词器训练** → 实现完整训练流程（作业核心）
4. **编码与解码实现** → 实现 encode 和 decode 功能（作业核心）
5. **完整可运行示例** → 整合所有代码

**阅读顺序说明**：按 1→5 顺序阅读，第 3、4 章是作业的核心实现

---

## 1. 环境准备 🧰

> 确认 Python 3.8+ 环境并导入必要库

```python
import regex as re                                                # 增强版正则，支持 Unicode 属性匹配
import os                                                         # 文件路径和大小操作
from collections import defaultdict                               # 默认字典，简化计数逻辑
from typing import BinaryIO, List, Tuple, Dict                    # 类型注解
from multiprocessing import Pool                                  # 多进程并行处理
import time                                                       # 性能测量
```

> 💡 如果未安装 regex：`pip install regex`

---

## 2. BPE 算法原理 🔬

### 2.1 什么是字节级 BPE？📝

BPE（Byte Pair Encoding）最初是数据压缩算法，2016 年被 OpenAI 引入 NLP 领域用于 GPT 模型。

**核心思想**：通过迭代合并训练语料中出现频率最高的相邻字节对，逐步构建词汇表。

**字节级的优势**：
- 可以表示任意文本（包括多语言、特殊字符）
- 初始词表固定为 256（所有可能的单字节）
- 有效处理未登录词（OOV）

> 💡 **什么是单字节？**  
> 单字节是指 8 位二进制数（0-255），可以表示 256 种不同的值。在 UTF-8 编码中：  
> - `0-127`：标准 ASCII（英文字母、数字、标点），例如 `"a"` → `97`  
> - `128-255`：用于多字节字符的一部分（如中文需要 3 个字节）  
> 字节级 BPE 以所有 256 个可能的单字节作为初始词表，因此可以表示任意文本

### 2.2 BPE 训练流程 🔄

BPE 训练包含三个核心步骤：

1. **初始化词表**：包含 256 个单字节（0-255）+ 特殊 token（如 `<|endoftext|>`）
2. **预分词**：使用 GPT-2 风格正则将文本分割为 token，避免 "dog!" 和 "dog." 分词不一致
3. **迭代合并**：统计字节对频率，合并最高频的 pair，直到达到目标词表大小

**频率相同时的处理**：选择字典序最大的字节对

**合并轮数计算**：
```python
合并轮数 = 目标词表大小 - 初始词表大小
# 例如：vocab_size=500，初始词表=257 → 合并 243 轮
```

---

## 3. BPE 分词器训练 🏋️

> 从零实现高效的 BPE 训练器，包含并行处理优化

### 3.1 关键优化点 🔑

在处理大规模训练语料（如 TinyStories 数据集约 6MB，或生产环境几十 GB 文本）时，朴素的 BPE 实现可能需要数小时。为了提升训练效率，**我们在后面的完整代码中采用了三个主要优化策略**：

1. **文件分块边界对齐**：在特殊 token 处分割文件，确保并行处理结果与单进程完全一致
2. **倒排索引**：记录每个 pair（相邻字节对，如 `(b'e', b's')`）出现在哪些 token 中，合并时只更新受影响的 token，避免每轮重新统计
3. **多进程并行**：使用 `multiprocessing.Pool` 突破 Python GIL 限制，真正并行处理 CPU 密集型任务

下面逐一讲解这些优化策略的目的和实现思路。

---

**优化 1：文件分块边界对齐**

**为什么要在特殊 token 处分割？**

核心目的：**确保每个 chunk 是自包含的（self-contained），并行处理结果与单进程处理完全一致**。

如果不在文档边界分割，会出现问题：
- ❌ **跨文档合并**：chunk1 末尾的词 + chunk2 开头的词会被错误地统计为一个 pair
- ❌ **频率统计偏差**：同一个文档被切断后，词频会被分散到两个 chunk
- ❌ **最终词表质量下降**：不同文档的语义被错误关联

**示例**：
```
原始数据：
文档1: "I love AI<|endoftext|>"
文档2: "Python is great<|endoftext|>"

❌ 错误分割（在中间切开）：
Chunk1: "I love AI<|endoft"     ← 文档被切断
Chunk2: "ext|>Python is great"  ← 语义混乱

✅ 正确分割（在特殊 token 处）：
Chunk1: "I love AI<|endoftext|>"  ← 完整文档
Chunk2: "Python is great<|endoftext|>"  ← 完整文档
```

这样每个进程独立处理完整文档，合并后的频率统计与单进程处理完全相同。

**块大小的浮动性**：

初始边界是均匀分布的（如每块 3000 字节），但调整到特殊 token 处后，**块大小会在目标值附近浮动**：

```
目标块大小：3000 字节

实际块大小：
块 0: 0 → 3150  (大小 3150，比目标大 150)
块 1: 3150 → 6080  (大小 2930，比目标小 70)
块 2: 6080 → 9200  (大小 3120，比目标大 120)
块 3: 9200 → 12000  (大小 2800，比目标小 200)
```

这种设计**牺牲了块大小的均匀性**，但**保证了文档完整性**和**并行结果的正确性**。块大小差异通常不大（±10% 以内），不会影响负载均衡。

**参考资料**：
- [Building a Fast BPE Tokenizer from Scratch -- Jun Yu Tan](https://jytan.net/blog/2025/bpe/) ⭐值得阅读

**优化 2：倒排索引**

```python
pair_to_indices = defaultdict(set)  # pair → token 索引集合
```

- **优化前**：每轮合并遍历所有 token → O(N × V)
- **优化后**：只更新受影响的 token → O(受影响 token 数)

**优化 3：多进程并行**

使用 `multiprocessing.Pool` 而非 `threading`，因为 Python GIL 限制多线程无法真正并行 CPU 密集型任务。

---

### 3.2 完整训练代码实现 💻

下面整合上述优化策略，提供完整的生产级 BPE 训练器实现：

**数据流动流程图**：

```mermaid
graph TD
    A[原始文件<br/>二进制格式] --> B[1. find_chunk_boundaries<br/>文件分块]
    B --> C[边界列表<br/>0, 3150, 6080, 9200, ...]
    C --> D[2. process_chunk<br/>并行预分词 多进程]
    
    D --> D1[读取块数据<br/>解码为字符串]
    D1 --> D2[按特殊token分割<br/>独立文档列表]
    D2 --> D3[正则预分词<br/>token列表]
    D3 --> D4[拆分为单字节<br/>字节序列列表]
    
    D4 --> E[pre_tokens_bytes<br/>b'I', b'l',b'o',b'v',b'e', ...]
    E --> F[3. 统计初始频率<br/>构建倒排索引]
    
    F --> F1[counts字典<br/>b'l',b'o': 5, ...]
    F --> F2[pair_to_indices<br/>b'l',b'o': 0,5,12, ...]
    
    F1 --> G[4. 迭代合并<br/>while idx < vocab_size]
    F2 --> G
    
    G --> G1[找最高频pair<br/>b'e',b's' 频率=9]
    G1 --> G2[合并字节对<br/>b'e' + b's' → b'es']
    G2 --> G3[更新词表<br/>vocab[257] = b'es']
    G3 --> G4[更新受影响token<br/>newest → new + est]
    G4 --> G5[更新counts和<br/>pair_to_indices]
    G5 --> G
    
    G --> H[5. 返回结果]
    H --> H1[vocab字典<br/>0: b'\\x00', 257: b'es', ...]
    H --> H2[merges列表<br/>b'e',b's', b'es',b't', ...]
```

**流程说明**：
1. **文件分块**：在特殊 token 处分割文件，确保文档完整性
2. **并行预分词**：多进程处理每个块，将文本转换为字节序列
3. **统计频率**：构建字节对频率字典和倒排索引
4. **迭代合并**：循环合并最高频字节对，更新词表和 token
5. **返回结果**：得到最终词表 vocab 和合并规则 merges

```python
import regex as re                                                # 导入增强版正则表达式库，支持 Unicode 属性匹配
import os                                                         # 导入操作系统接口模块，用于文件路径和大小操作
from multiprocessing import Pool                                  # 导入多进程池，用于并行处理大规模文本
from typing import BinaryIO, List, Tuple, Dict                    # 导入类型注解，提升代码可读性
from collections import defaultdict                               # 导入默认字典，简化计数逻辑
import time                                                       # 导入时间模块，用于性能测量


# 将文件分块，找到块边界，便于并行处理
# 参数: file 二进制文件对象, desired_num_chunks 期望的块数量, split_special_token 用于分割的特殊 token（如 <|endoftext|>）
# 返回: chunk_boundaries 块的起始位置列表
# 示例: boundaries = find_chunk_boundaries(file, num_processes, b'<|endoftext|>')
def find_chunk_boundaries(
    file: BinaryIO,                                               # 二进制文件对象，示例：open("data.txt", "rb")
    desired_num_chunks: int,                                      # 期望的块数量，示例：16
    split_special_token: bytes,                                   # 用于分割的特殊 token，示例：b'<|endoftext|>'
) -> list[int]:                                                   # 返回块的起始位置列表，示例：[0, 1000, 2000, 3000]
    # 断言检查：特殊 token 必须以 bytes 表示
    assert isinstance(split_special_token, bytes), "特殊 token 必须以 bytes 表示"
    
    # 获取文件大小
    file.seek(0, os.SEEK_END)                                     # 移动文件指针到末尾
    file_size = file.tell()                                       # 获取文件大小（字节数），示例：48000
    file.seek(0)                                                  # 重置文件指针到开头
    
    # 计算每个块的大小
    chunk_size = file_size // desired_num_chunks                  # 整除计算块大小，示例：48000 // 16 = 3000
    
    # 初始边界猜测，均匀分布
    chunk_boundaries = [i * chunk_size for i in range(desired_num_chunks + 1)]  # 生成均匀分布的边界，示例：[0, 3000, 6000, ...]
    chunk_boundaries[-1] = file_size                              # 最后一个边界设为文件大小，示例：48000
    
    mini_chunk_size = 4096                                        # 每次读取 4KB，用于搜索特殊 token
    
    # 调整边界，确保在特殊 token 处分割
    # 从 1 开始的原因：文档起点（第 0 个边界）和文档终点（最后 1 个边界）已经是自然边界，不需要调整
    for bi in range(1, len(chunk_boundaries) - 1):                # 遍历所有中间边界（除了首尾），示例：bi=1,2,3,...,15
        initial_position = chunk_boundaries[bi]                   # 记录初始边界位置，示例：3000
        file.seek(initial_position)                               # 移动文件指针到该位置
        while True:                                               # 循环搜索特殊 token
            mini_chunk = file.read(mini_chunk_size)               # 读取 4KB 数据，示例：b'...<|endoftext|>...'
            
            if mini_chunk == b"":                                 # 如果读到文件末尾
                chunk_boundaries[bi] = file_size                  # 边界设为文件大小
                break
            
            # 在 mini chunk 中查找特殊 token
            found_at = mini_chunk.find(split_special_token)       # 查找特殊 token 位置，示例：找到在偏移 512 处
            if found_at != -1:                                    # 如果找到了特殊 token
                chunk_boundaries[bi] = initial_position + found_at  # 调整边界到特殊 token 处，示例：3000 + 512 = 3512
                break
            initial_position += mini_chunk_size                   # 未找到，继续读取下一个 4KB
    
    return sorted(set(chunk_boundaries))                          # 返回去重并排序的边界列表


# 处理一个文本块，进行预分词并返回字节序列
# 参数: args 元组 (input_path, start, end, special_tokens)
# 返回: pre_tokens_bytes 预分词后的字节序列列表
# 示例: result = process_chunk(("data.txt", 0, 1000, ["<|endoftext|>"]))
def process_chunk(args: tuple[str, int, int, list[str]]) -> list[list[bytes]]:  # 参数元组，示例：("data.txt", 0, 3000, ["<|endoftext|>"])
    # 解包参数
    input_path, start, end, special_tokens = args                 # 解包元组，示例：input_path="data.txt", start=0, end=3000
    
    with open(input_path, "rb") as file:                          # 以二进制模式打开文件
        file.seek(start)                                          # 移动文件指针到起始位置
        chunk = file.read(end - start).decode("utf-8", errors="ignore")  # 读取块数据并解码为字符串，示例：读取 3000 字节
    
    # 1. 移除特殊 token
    pattern = "|".join(re.escape(tok) for tok in special_tokens)  # 构建正则表达式模式，示例：'<\|endoftext\|>'
    documents = re.split(pattern, chunk)                          # 按特殊 token 分割文本，示例：["doc1", "doc2"]
    
    # 2. 预分词
    pre_tokens_bytes: list[list[bytes]] = []                      # 初始化预分词结果列表
    # GPT-2 风格的正则表达式
    PAT = r"""'(?:[sdmt]|ll|ve|re)| ?\p{L}+| ?\p{N}+| ?[^\s\p{L}\p{N}]+|\s+(?!\S)|\s+"""  # 匹配缩写、字母、数字、标点、空白
    
    for doc in documents:                                         # 遍历每个文档，示例：doc="I love AI"
        tokens = [match.group(0).encode("utf-8") for match in re.finditer(PAT, doc)]  # 正则匹配并编码为字节，示例：[b'I', b'love', b'AI']
        for token in tokens:                                      # 遍历每个 token
            token_bytes = [bytes([b]) for b in token]             # 将 token 拆分为单字节列表，示例：b'I' → [b'I']
            pre_tokens_bytes.append(token_bytes)                  # 添加到结果列表
    
    return pre_tokens_bytes                                       # 返回预分词后的字节序列列表，示例：[[b'I'], [b'l', b'o', b'v', b'e'], [b'A', b'I']]


# 在给定语料上训练 BPE 分词器
# 参数: input_path 训练语料文件路径, vocab_size 目标词表大小, special_tokens 特殊 token 列表, num_processes 并行进程数
# 返回: vocab 词表字典 {token_id: token_bytes}, merges 合并列表 [(byte_a, byte_b), ...]
# 示例: vocab, merges = train_bpe("data.txt", vocab_size=500, special_tokens=["<|endoftext|>"], num_processes=16)
def train_bpe(
    input_path: str,                                              # 训练语料文件路径，示例："data.txt"
    vocab_size: int,                                              # 目标词表大小，示例：500
    special_tokens: list[str],                                    # 特殊 token 列表，示例：["<|endoftext|>"]
    num_processes: int = 16                                       # 并行进程数，默认 16
) -> tuple[dict[int, bytes], list[tuple[bytes, bytes]]]:          # 返回词表和合并列表
    # 记录开始时间
    start_time = time.time()                                      # 记录训练开始时间，示例：1620000000.123
    
    # 1. 初始化词表：256 个单字节 token
    vocab = {i: bytes([i]) for i in range(256)}                   # 初始化 256 个单字节 token，示例：0→b'\x00', 255→b'\xff'
    # 添加特殊 token 到词表
    for token in special_tokens:                                  # 遍历特殊 token 列表，示例：["<|endoftext|>"]
        vocab[len(vocab)] = token.encode("utf-8")                 # 添加特殊 token 到词表，示例：256→b'<|endoftext|>'
    
    # 2. 文件分块
    with open(input_path, "rb") as f:                             # 以二进制模式打开训练语料
        boundaries = find_chunk_boundaries(f, num_processes, "<|endoftext|>".encode("utf-8"))  # 计算文件分块边界，示例：[0, 3000, 6000, ...]
    
    # 3. 并行预分词
    task_args = [(input_path, start, end, special_tokens)         # 构建任务参数列表
                 for start, end in zip(boundaries[:-1], boundaries[1:])]  # 使用相邻边界创建任务，示例：[(0,3000), (3000,6000), ...]
    
    with Pool(processes=num_processes) as pool:                   # 创建多进程池，示例：16 个进程
        chunk_results = pool.map(process_chunk, task_args)        # 并行处理所有块，返回预分词结果列表
    
    # 4. 合并所有块的预分词结果
    pre_tokens_bytes: list[list[bytes]] = [                       # 展平嵌套列表
        token for chunk in chunk_results for token in chunk       # 将所有块的结果合并为一个列表
    ]
    
    # 5. 统计初始字节对频率
    counts = defaultdict(int)                                     # 初始化字节对频率字典，示例：defaultdict(<class 'int'>, {})
    pair_to_indices = defaultdict(set)                            # 倒排索引：pair → 包含它的 token 索引，示例：defaultdict(<class 'set'>, {})
    
    for idx, token in enumerate(pre_tokens_bytes):                # 遍历所有 token，示例：idx=0, token=[b'I']
        for i in range(len(token) - 1):                           # 遍历 token 中的相邻字节对
            pair = (token[i], token[i + 1])                       # 提取字节对，示例：(b'l', b'o')
            counts[pair] += 1                                     # 累加频率，示例：counts[(b'l', b'o')] = 5
            pair_to_indices[pair].add(idx)                        # 记录包含该 pair 的 token 索引，示例：pair_to_indices[(b'l', b'o')] = {0, 5, 12}
    
    # 6. 迭代合并
    merges: list[tuple[bytes, bytes]] = []                        # 初始化合并列表，记录所有合并操作
    idx = len(vocab)                                              # 初始化 token ID 索引，从当前词表大小开始，示例：257
    
    while idx < vocab_size:                                       # 循环直到达到目标词表大小，示例：257 < 500
        if not counts:                                            # 如果没有更多字节对可合并
            break
        
        # 找到频率最高的字节对（频率相同时选字典序最大的）
        max_pair: tuple[bytes, bytes] = None                      # 初始化最高频字节对
        max_cnt = -1                                              # 初始化最高频率
        for pair, cnt in counts.items():                          # 遍历所有字节对及其频率
            if cnt > max_cnt:                                     # 如果当前频率更高
                max_pair = pair                                   # 更新最高频字节对，示例：(b'e', b's')
                max_cnt = cnt                                     # 更新最高频率，示例：9
            elif cnt == max_cnt:                                  # 如果频率相同
                if max_pair is None or pair > max_pair:           # 选择字典序更大的
                    max_pair = pair
        
        # 记录合并
        merges.append(max_pair)                                   # 添加到合并列表，示例：merges=[(b'e', b's'), ...]
        a, b = max_pair                                           # 解包字节对，示例：a=b'e', b=b's'
        new_token = a + b                                         # 合并为新 token，示例：b'es'
        vocab[idx] = new_token                                    # 添加到词表，示例：vocab[257] = b'es'
        idx += 1                                                  # 递增 token ID，示例：257 → 258
        
        # 更新受影响的 token
        affected_indices = pair_to_indices[max_pair].copy()       # 获取包含该 pair 的所有 token 索引，示例：{0, 5, 12, 23}
        for j in affected_indices:                                # 遍历受影响的 token
            token = pre_tokens_bytes[j]                           # 获取 token，示例：[b'n', b'e', b'w', b'e', b's', b't']
            
            # 移除旧的 pair 计数
            for i in range(len(token) - 1):                       # 遍历 token 中的所有相邻字节对
                old_pair = (token[i], token[i + 1])               # 提取旧字节对，示例：(b'e', b's')
                pair_to_indices[old_pair].discard(j)              # 从倒排索引中移除该 token 索引
                counts[old_pair] -= 1                             # 频率减 1，示例：9 → 8
                if counts[old_pair] == 0:                         # 如果频率降为 0
                    counts.pop(old_pair)                          # 从频率字典中删除
                    pair_to_indices.pop(old_pair, None)           # 从倒排索引中删除
            
            # 执行合并
            merged = []                                           # 初始化合并后的 token 列表
            i = 0                                                 # 从头开始遍历
            while i < len(token):                                 # 只要还有字节
                if i < len(token) - 1 and token[i] == a and token[i+1] == b:  # 如果匹配要合并的字节对
                    merged.append(new_token)                      # 添加合并后的新 token，示例：b'es'
                    i += 2                                        # 跳过两个字节
                else:                                             # 不匹配
                    merged.append(token[i])                       # 添加原字节
                    i += 1                                        # 跳过一个字节
            
            pre_tokens_bytes[j] = merged                          # 更新合并后的 token，示例：[b'n', b'e', b'w', b'es', b't']
            
            # 更新新 token 中的 pair 计数
            token = pre_tokens_bytes[j]                           # 获取更新后的 token
            for i in range(len(token) - 1):                       # 遍历新的相邻字节对
                pair = (token[i], token[i + 1])                   # 提取新字节对，示例：(b'n', b'e')
                counts[pair] += 1                                 # 累加频率
                pair_to_indices[pair].add(j)                      # 添加到倒排索引
    
    elapsed_time = time.time() - start_time                       # 计算训练耗时，示例：12.34 秒
    print(f"训练完成！词表大小: {len(vocab)}, 耗时: {elapsed_time:.2f}秒")  # 输出统计信息
    
    return vocab, merges                                          # 返回词表和合并列表
```

---

## 4. 总结 📝

本节我们完成了 BPE 分词器的完整实现，核心要点回顾：

| 步骤 | 操作 | 代码对应 |
|------|------|---------|
| 1 | 初始化词表（256 字节 + 特殊 token） | `vocab = {i: bytes([i]) for i in range(256)}` |
| 2 | 文件分块与边界对齐 | `find_chunk_boundaries()` |
| 3 | 并行预分词 | `process_chunk()` + `Pool.map()` |
| 4 | 统计字节对频率 | `counts[pair] += 1` |
| 5 | 迭代合并最高频字节对 | `while idx < vocab_size:` |

🔴 **关键理解**：

- **BPE 是一种子词分割算法**：平衡词表大小和未登录词处理能力
- **训练过程是迭代合并**：每次合并频率最高的字节对
- **并行化是大规模训练的关键**：文件分块 + 多进程 + 倒排索引

💡 **实践建议**：

- 学习阶段：使用小语料（几 KB）理解算法流程
- 生产环境：使用 Hugging Face 的 `tokenizers` 库（Rust 实现，性能极高）
- 调试技巧：打印每轮合并的 pair 和频率，观察词表构建过程

---

**最后更新时间**：2026-05-22
