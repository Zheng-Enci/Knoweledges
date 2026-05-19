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

    

if __name__ == '__main__':  # 主程序入口
    text = "low low low low low\nlower lower widest widest widest\nnewest newest newest newest newest newest\n"  # 测试语料
    result = count_word_frequency(text)  # 统计频率，{"low": 5, "lower": 2, "widest": 3, "newest": 6}
    result = convert_to_candidate_list(result)  # 转换格式
    print(result)  # 输出
