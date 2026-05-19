def count_word_frequency(text: str) -> dict:
    """
    统计文本中每个单词的出现频率
    
    参数:
        text: 原始文本字符串
    
    返回:
        dict: {单词: 频率}，例如 {"low": 5, "lower": 2}
    """
    words = text.split()  # 将文本按空格分割成单词列表
    word_freq = {}  # 初始化空字典存储单词频率
    
    for word in words:  # 遍历每个单词
        if word in word_freq:  # 如果单词已在字典中
            word_freq[word] += 1  # 出现次数 +1
        else:  # 如果单词不在字典中
            word_freq[word] = 1  # 初始化为 1
    
    return word_freq  # 返回频率字典


def convert_to_candidate_list(word_freq: dict) -> list:
    """
    将 {单词: 频率} 字典转换为 [{字符元组: 频率}, ...] 格式
    
    参数:
        word_freq: {单词: 频率} 字典
    
    返回:
        list: [{字符元组: 频率}, ...] 列表
    """
    candidates = []  # 初始化空列表存储候选词
    for word, freq in word_freq.items():  # 遍历每个单词及其频率
        word_tuple = tuple(word)  # 将单词字符串转换为字符元组
        candidates.append({word_tuple: freq})  # 添加 {字符元组: 频率} 到列表
    return candidates  # 返回候选词列表

    

if __name__ == '__main__':  # 主程序入口
    text = "low low low low low\nlower lower widest widest widest\nnewest newest newest newest newest newest\n"  # 测试文本
    result = count_word_frequency(text)  # 统计单词频率
    result = convert_to_candidate_list(result)  # 转换为候选词列表格式
    print(result)  # 输出结果
