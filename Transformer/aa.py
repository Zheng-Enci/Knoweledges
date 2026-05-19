"""
统计文本中每个单词的出现频率

参数:
    text: 原始文本字符串

返回:
    dict: {单词: 频率}，例如 {"low": 5, "lower": 2}
"""
def count_word_frequency(text: str) -> dict:
    words = text.split()  # 分割文本，示例："low low lower" → ["low", "low", "lower"]
    word_freq = {}  # 初始化空字典
    
    for word in words:  # 遍历单词，示例：["low", "low", "lower"]
        if word in word_freq:  # 判断是否已统计，示例：word_freq={"low": 1}
            word_freq[word] += 1  # 计数+1，示例：{"low": 1} → {"low": 2}
        else:  # 新单词
            word_freq[word] = 1  # 初始化，示例：{} → {"lower": 1}
    
    return word_freq  # 返回频率字典，示例：{"low": 2, "lower": 1}


"""
将 {单词: 频率} 字典转换为 [{字符元组: 频率}, ...] 格式

参数:
    word_freq: {单词: 频率} 字典

返回:
    list: [{字符元组: 频率}, ...] 列表
"""
def convert_to_candidate_list(word_freq: dict) -> list:
    candidates = []  # 初始化空列表
    for word, freq in word_freq.items():  # 遍历字典，示例：{"low": 2, "lower": 1}
        word_tuple = tuple(word)  # 转元组，示例："low" → ('l', 'o', 'w')
        candidates.append({word_tuple: freq})  # 添加，示例：[{"lo": 2}] → [{"lo": 2}, {('l', 'o', 'w', 'e', 'r'): 1}]
    return candidates  # 返回列表

"""
统计候选词列表中所有相邻字符对的频率

参数:
    candidates: 候选词列表，格式为 [{字符元组: 频率}, ...]

返回:
    dict: {(字符, 字符): 总频率} 字典
"""
def count_pair_frequencies(candidates: list) -> dict:
    pair_frequencies = {}  # 初始化字符对频率字典
    for candidate in candidates:  # 遍历候选词，示例：[{("l", "o"): 2}]
        char_tuple = list(candidate.keys())[0]  # 获取字符元组，示例：("l", "o", "w")
        freq = list(candidate.values())[0]  # 获取频率值，示例：2
        for index in range(len(char_tuple) - 1):  # 遍历相邻字符对
            char_pair = (char_tuple[index], char_tuple[index + 1])  # 提取字符对，示例：('l', 'o')
            pair_frequencies[char_pair] = pair_frequencies.get(char_pair, 0) + freq  # 累加频率，示例：{('l', 'o'): 0} → {('l', 'o'): 2}

    return pair_frequencies  # 返回字符对频率字典


"""
找到最高频字符对在候选词中的合并位置

参数:
    pair_frequencies: {(字符, 字符): 频率} 字典
    candidates: [{字符元组: 频率}, ...] 候选词列表

返回:
    list: [(候选词索引, 合并起始位置, 合并结束位置), ...]，例如 [(2, 4, 6), (3, 4, 6)]
"""
def find_merge_positions(pair_frequencies: dict, candidates: list) -> list:
    max_freq = max(pair_frequencies.values())  # 找到最高频率，示例：9
    top_pairs = [pair for pair, freq in pair_frequencies.items() if freq == max_freq]  # 获取所有最高频字符对
    top_pairs.sort()  # 按字典序排序
    top_pair = top_pairs[0]  # 取字典序最小的字符对，示例：('e', 's')
    merge_positions = []  # 初始化合并位置列表
    
    for cand_idx, candidate in enumerate(candidates):  # 遍历候选词，示例：cand_idx=2, candidate={('n', 'e', 'w', 'e', 's', 't'): 6}
        char_tuple = list(candidate.keys())[0]  # 获取字符元组，示例：('n', 'e', 'w', 'e', 's', 't')
        freq = list(candidate.values())[0]  # 获取频率值
        
        for i in range(len(char_tuple) - 1):  # 遍历相邻字符位置，示例：i=0 时检查 ('n', 'e')
            current_pair = (char_tuple[i], char_tuple[i + 1])  # 当前字符对，示例：('n', 'e')
            if current_pair == top_pair:  # 判断是否为最高频字符对
                start, end = i, i + 2  # 合并位置：(起始索引, 结束索引+1)
                merge_positions.append((cand_idx, start, end))  # 记录：示例 [(2, 4, 6)] 表示第3个词的第5-7个字符
    
    return merge_positions  # 返回合并位置列表

if __name__ == '__main__':  # 主程序入口
    text = "low low low low low\nlower lower widest widest widest\nnewest newest newest newest newest newest\n"  # 测试语料
    word_freq = count_word_frequency(text)  # 统计频率，示例：{"low": 5, "lower": 2}
    candidates = convert_to_candidate_list(word_freq)  # 转换为 [{元组: 频率}]
    print(candidates)
    pair_frequencies = count_pair_frequencies(candidates)  # 统计字符对，示例：{('l', 'o'): 7}
    print(pair_frequencies)  # 输出字符对频率字典
