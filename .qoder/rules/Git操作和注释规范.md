---
trigger: always_on
---
# Git 操作规范

## 执行目录

所有 git 命令在本项目**根目录**下执行即可。

## 文件变更提交

每次修改、创建或删除文件后，**必须自动执行** `git add` 和 `git commit`（提交信息使用中文）。

> ⚠️ 注意：禁止自动执行 `git push`

## 用户修改代码后执行 Git

当用户说"修改了代码"或类似表述，要求执行 git 时：
1. 执行 `git status` 查看变更状态
2. 执行 `git diff -- "本项目/src" > "本项目/git_diff.diff"` 将差异输出到 diff 文件
3. 查看 diff 内容了解变更后(必须阅读"本项目/git_diff.diff"了解变更内容)，进行 `git add` 和 `git commit`
4. 提交完成后**FrontEnd/git_diff.diff 文件**不用删除

> ⚠️ 注意：禁止使用 `git diff -p --output`，会造成递归嵌套问题

## Git提交规范

格式：type(scope): subject
类型：feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert|types|wip|release
规则：type小写 | subject非空 | 无句号 | subject最长72 | header最长100


## git_diff.diff 文件管理

- `git_diff.diff` 文件仅用于本地查看变更，**不需要跟踪**
- 该文件**不需要上传到 git**
- 每次生成新的 diff 文件时会自动覆盖旧内容，保持最新变更记录

---

# 代码注释规范

## 基本原则

- **每行代码都要有注释**：代码的右侧添加注释说明该行代码的作用
- **函数/类级注释写在外部上方**：使用文档字符串（docstring）形式，写在函数或类的外部上方

## 行内注释规范

行内注释写在代码的右侧，用 `#` 开头，说明该行代码的作用。

### 正确示例

```python
def calculate_sum(a, b):
    """计算两个数的和"""
    result = a + b  # 将 a 和 b 相加得到结果
    return result  # 返回计算结果
```

### 错误示例

```python
def calculate_sum(a, b):
    """计算两个数的和"""
    # 计算两个数的和
    result = a + b
    return result
```

### 行内注释位置

- 注释与代码之间用**两个空格**分隔
- 注释从第 50 列开始对齐（如果有更长的变量名，适当调整）
- 单行注释尽量简洁，一行不超过 100 字符

```python
def preprocess_text(text):
    """对文本进行预处理"""
    text = text.strip()  # 去除首尾空白字符
    text = text.lower()  # 转换为小写
    words = text.split()  # 按空格分割成单词列表
    return words  # 返回处理后的单词列表
```

## 函数注释规范

### 位置

函数注释写在函数定义的**外部上方**，使用三引号文档字符串。

### 必需内容

1. **功能描述**：一句话说明函数的作用
2. **参数说明**：每个参数的类型和作用（使用 `参数:` 或 `Args:`
3. **返回值说明**：返回值的类型和内容（使用 `返回:` 或 `Returns:`
4. **使用示例**（可选）：简单的调用示例

### 正确示例

```python
def count_word_frequency(text: str) -> dict:
    """
    统计文本中每个单词的出现频率
    
    参数:
        text: 原始文本字符串
    
    返回:
        dict: {单词: 频率}，例如 {"hello": 3}
    """
    words = text.split()  # 将文本按空格分割成单词列表
    word_freq = {}  # 初始化空字典存储单词频率
    
    for word in words:  # 遍历每个单词
        if word in word_freq:  # 如果单词已在字典中
            word_freq[word] += 1  # 出现次数 +1
        else:  # 如果单词不在字典中
            word_freq[word] = 1  # 初始化为 1
    
    return word_freq  # 返回频率字典
```

## 类注释规范

### 位置

类注释写在类定义的**外部上方**，使用三引号文档字符串。

### 必需内容

1. **类功能描述**：说明类的职责和作用
2. **类属性说明**：主要属性的类型和作用
3. **使用示例**（可选）：简单的使用示例

### 正确示例

```python
class WordCounter:
    """
    单词计数器类，用于统计文本中单词的出现频率
    
    属性:
        text: 原始文本
        word_freq: 单词频率字典
    """
    
    def __init__(self, text: str):  # 初始化方法
        """初始化计数器"""
        self.text = text  # 保存原始文本
        self.word_freq = {}  # 初始化空字典
    
    def count(self) -> dict:  # 统计方法
        """执行统计并返回结果"""
        self.word_freq = count_word_frequency(self.text)  # 调用统计函数
        return self.word_freq  # 返回结果字典
```

## 循环和条件注释规范

### for 循环

```python
for item in items:  # 遍历列表中的每个元素
    process(item)  # 处理当前元素
```

### if-else 条件

```python
if condition:  # 如果满足条件
    do_something()  # 执行操作 A
else:  # 否则
    do_other()  # 执行操作 B
```

### while 循环

```python
while index < len(items):  # 当索引小于列表长度时循环
    item = items[index]  # 获取当前元素
    process(item)  # 处理元素
    index += 1  # 索引 +1
```

## 变量命名与注释配合

### 变量名应具有描述性

```python
# 推荐的变量名
user_name = "Alice"  # 用户名字
total_price = 100.0  # 总价格
is_valid = True  # 是否有效

# 不推荐的变量名（单字母除非是循环索引）
a = "Alice"  # 什么 a？
```

### 复杂表达式应分行并注释

```python
# 计算加权平均分：(成绩 × 权重) 的和 ÷ 权重的和
weighted_sum = sum(score * weight for score, weight in zip(scores, weights))  # 加权求和
weight_sum = sum(weights)  # 权重总和
average = weighted_sum / weight_sum if weight_sum > 0 else 0  # 加权平均（避免除零）
```

## 注释语言规范

- **注释使用中文**：与项目文档语言保持一致
- **标点符号**：中文文档使用中文标点，代码注释尽量使用中文
- **术语统一**：使用项目统一的术语，如 BPE、Token、Embedding 等可直接使用英文

## 注释示例：完整函数

```python
def merge_pair(candidates: list, pair: tuple) -> tuple:
    """
    合并候选词列表中的指定字符对
    
    参数:
        candidates: 候选词列表 [{字符元组: 频率}, ...]
        pair: 要合并的字符对元组，例如 ('e', 's')
    
    返回:
        tuple: (更新后的候选词列表, 本次合并的字符对)
    """
    new_candidates = []  # 初始化新的候选词列表
    
    for cand in candidates:  # 遍历每个候选词
        key = list(cand.keys())[0]  # 获取字符元组
        freq = list(cand.values())[0]  # 获取频率
        
        if pair_in_key(key, pair):  # 如果字符元组包含目标 pair
            merged = merge_in_key(key, pair)  # 执行合并操作
            new_candidates.append({merged: freq})  # 添加合并后的新词
        else:  # 如果不包含目标 pair
            new_candidates.append({key: freq})  # 保持原词不变
    
    return new_candidates, pair  # 返回更新后的列表和合并的 pair
```
