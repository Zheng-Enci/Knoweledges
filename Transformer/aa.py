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


if __name__ == "__main__":                                        # 主程序入口
    # 创建测试数据目录
    test_dir = "./test_bpe_data"                                  # 测试数据目录路径
    os.makedirs(test_dir, exist_ok=True)                          # 创建目录（如不存在）

    # 写入测试语料
    test_file = os.path.join(test_dir, "test.txt")                # 测试文件路径
    with open(test_file, "wb") as f:                              # 以二进制写入模式打开
        # 写入测试文本（包含特殊 token 分隔的多个文档）
        # 第 1 个文档
        f.write(b"The quick brown fox jumps over the lazy dog.<|endoftext|>")
        # 第 2 个文档
        f.write(b"Python is a great programming language.<|endoftext|>")
        # 第 3 个文档
        f.write(b"Deep learning requires lots of data.<|endoftext|>")
        # 第 4 个文档
        f.write(b"The best test is the best.<|endoftext|>")

    print("=" * 60)                                               # 输出分隔线
    print("BPE 分词器训练测试")                                     # 输出测试标题
    print("=" * 60)                                               # 输出分隔线

    # 训练 BPE 分词器
    vocab, merges = train_bpe(
        input_path=test_file,                                     # 输入测试文件
        # 目标词表大小（256 + 44 个新 token）
        vocab_size=300,
        special_tokens=["<|endoftext|>"],                         # 特殊 token 列表
        num_processes=2                                           # 使用 2 个进程并行处理
    )

    # 查看训练结果
    print("\n" + "=" * 60)                                        # 输出分隔线
    print("词表示例（前 10 个）：")                                  # 输出标题
    print("=" * 60)                                               # 输出分隔线
    for i in range(10):                                           # 遍历前 10 个 token
        # 输出 token ID 和内容
        print(f"{i}: {vocab[i]}")

    print("\n" + "=" * 60)                                        # 输出分隔线
    print("合并规则示例（前 10 个）：")                              # 输出标题
    print("=" * 60)                                               # 输出分隔线
    # 遍历前 10 个合并规则
    for i, (a, b) in enumerate(merges[:10]):
        print(f"{i}: {a} + {b} → {a + b}")                        # 输出合并过程

    print("\n" + "=" * 60)                                        # 输出分隔线
    print(f"总词表大小: {len(vocab)}")                              # 输出词表大小
    print(f"总合并规则数: {len(merges)}")                           # 输出合并规则数
    print("=" * 60)                                               # 输出分隔线
