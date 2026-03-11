# P2I-Python正则表达式-什么是正则表达式？为什么程序员都在用re模块？怎么快速掌握模式匹配和替换？

## 📝 摘要

面向零基础，系统讲解 Python 正则表达式（re 模块）核心技能：模式匹配、搜索、替换。通过生活化比喻与实战对比，掌握强大的文本处理工具，快速提升数据提取和验证能力。

---

## 目录

- [1. 前置知识点](#1-前置知识点)
- [2. 快速上手（3 分钟）](#2-快速上手3-分钟)
- [3. 什么是正则表达式（Regular Expression（正则表达式））](#3-什么是正则表达式regular-expression正则表达式)
- [4. re 模块导入](#4-re-模块导入)
- [5. 正则表达式基础语法](#5-正则表达式基础语法)
  - [5.1 元字符（Metacharacters（元字符））](#51-元字符metacharacters元字符)
  - [5.2 限定符（Quantifiers（限定符））](#52-限定符quantifiers限定符)
  - [5.3 字符类（Character Classes（字符类））](#53-字符类character-classes字符类)
  - [5.4 原始字符串（Raw String（原始字符串））](#54-原始字符串raw-string原始字符串)
- [6. 模式匹配（Pattern Matching（模式匹配））](#6-模式匹配pattern-matching模式匹配)
  - [6.1 re.match() 方法](#61-rematch-方法)
  - [6.2 re.search() 方法](#62-research-方法)
  - [6.3 match() vs search() 对比](#63-match-vs-search-对比)
- [7. 搜索所有匹配（Finding All Matches（搜索所有匹配））](#7-搜索所有匹配finding-all-matches搜索所有匹配)
  - [7.1 re.findall() 方法](#71-refindall-方法)
  - [7.2 re.finditer() 方法](#72-refinditer-方法)
  - [7.3 findall() vs finditer() 对比](#73-findall-vs-finditer-对比)
- [8. 替换（Substitution（替换））](#8-替换substitution替换)
  - [8.1 re.sub() 方法](#81-resub-方法)
  - [8.2 re.subn() 方法](#82-resubn-方法)
  - [8.3 替换中使用分组](#83-替换中使用分组)
- [9. 分割字符串（Splitting（分割））](#9-分割字符串splitting分割)
  - [9.1 re.split() 方法](#91-resplit-方法)
- [10. 编译正则表达式（Compiling（编译））](#10-编译正则表达式compiling编译)
  - [10.1 re.compile() 方法](#101-recompile-方法)
  - [10.2 何时使用 compile()](#102-何时使用-compile)
- [11. 分组与捕获（Grouping and Capturing（分组与捕获））](#11-分组与捕获grouping-and-capturing分组与捕获)
  - [11.1 基本分组](#111-基本分组)
  - [11.2 命名分组](#112-命名分组)
  - [11.3 非捕获分组](#113-非捕获分组)
- [12. 标志（Flags（标志））](#12-标志flags标志)
  - [12.1 re.IGNORECASE（忽略大小写）](#121-reignorecase忽略大小写)
  - [12.2 re.MULTILINE（多行模式）](#122-remultiline多行模式)
  - [12.3 re.DOTALL（点号匹配换行）](#123-redotall点号匹配换行)
  - [12.4 组合使用多个标志](#124-组合使用多个标志)
- [13. 贪婪与非贪婪匹配（Greedy vs Non-greedy（贪婪与非贪婪匹配））](#13-贪婪与非贪婪匹配greedy-vs-non-greedy贪婪与非贪婪匹配)
  - [13.1 贪婪匹配](#131-贪婪匹配)
  - [13.2 非贪婪匹配](#132-非贪婪匹配)
- [14. 常见模式示例](#14-常见模式示例)
  - [14.1 匹配邮箱地址](#141-匹配邮箱地址)
  - [14.2 匹配电话号码](#142-匹配电话号码)
  - [14.3 匹配日期](#143-匹配日期)
  - [14.4 匹配 URL](#144-匹配-url)
- [15. 正则表达式 vs 不使用正则表达式对比](#15-正则表达式-vs-不使用正则表达式对比)
- [16. 常见错误与对比修正](#16-常见错误与对比修正)
- [17. 选择建议与实践流程](#17-选择建议与实践流程)
- [18. 📚 参考资料与学习资源](#18-参考资料与学习资源)
- [19. 总结](#19-总结)

---

## 1. 前置知识点

在深入学习 Python 正则表达式之前，你需要了解以下基础概念：

- **字符串（string（字符串））**：文本数据的基本类型，就像生活中的 **文字内容**，例如"Hello World"、"电话号码：13800138000"等
- **模块导入（module import（模块导入））**：使用 `import` 语句导入 Python 内置模块，就像从工具箱中取出需要的工具
- **基本字符串操作**：字符串查找、替换等基础操作（本概念在本文档后续章节有详细介绍）
- **转义字符（escape character（转义字符））**：如 `\n`（换行）、`\t`（制表符）等，在正则表达式中使用原始字符串（`r""`）可以避免转义问题

---

💡 **学习建议**：如果你已经掌握了 Python 字符串的基本操作，就可以开始学习正则表达式了。正则表达式是文本处理的高级工具，广泛应用于数据验证、信息提取、文本清洗等场景。

---

## 2. 快速上手（3 分钟）

让我们通过一个简单的例子快速了解正则表达式的强大功能：

```python
import re  # 导入 re 模块

# 示例 1：从文本中提取所有数字
text = "我的电话号码是 138-0013-8000，QQ 号是 123456789"
numbers = re.findall(r'\d+', text)  # 匹配一个或多个数字
print(f"找到的数字：{numbers}")
# 输出：找到的数字：['138', '0013', '8000', '123456789']

# 示例 2：验证邮箱格式
email = "user@example.com"
pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
if re.match(pattern, email):
    print("✅ 邮箱格式正确")
else:
    print("❌ 邮箱格式错误")

# 示例 3：替换敏感信息
text = "我的身份证号是 320123199001011234"
# 将身份证号中间部分替换为星号
result = re.sub(r'(\d{6})\d{8}(\d{4})', r'\1********\2', text)
print(f"脱敏后：{result}")
# 输出：脱敏后：我的身份证号是 320123********1234
```

**快速理解**：
- `\d+`：匹配一个或多个数字
- `re.findall()`：找出所有匹配的内容
- `re.match()`：验证字符串是否符合模式
- `re.sub()`：替换匹配的内容

这就是正则表达式的核心功能！接下来我们将详细学习每个部分。

---

## 3. 什么是正则表达式（Regular Expression（正则表达式））

**正则表达式**（Regular Expression，简称 **regex** 或 **RE**）是一种用于描述字符串匹配模式的工具，它使用特定的语法规则来匹配、查找、替换文本中的内容。

### 生活化比喻

想象一下：

- **传统查找**：就像在一本书中逐页逐字查找某个词，需要人工一个一个对比（效率低、容易出错）
- **正则表达式**：就像使用 **智能搜索引擎**，输入一个"搜索模板"，系统自动帮你找到所有符合条件的内容（效率高、准确）

**举个例子**：

```python
# ❌ 不使用正则表达式（繁琐且容易出错）
text = "我的电话号码是 138-0013-8000"
# 需要写很多代码来提取数字，还要处理各种格式变化

# ✅ 使用正则表达式（简洁高效）
import re
numbers = re.findall(r'\d+', text)
print(numbers)  # 输出：['138', '0013', '8000']
```

### 正则表达式的特点

1. **强大的模式匹配**：可以用简单的表达式描述复杂的文本模式
2. **高效的文本处理**：适合批量处理大量文本数据
3. **广泛的应用场景**：数据验证、信息提取、文本清洗、日志分析等

### 为什么程序员都在用 re 模块？

- ✅ **内置模块**：Python 自带，无需安装第三方库
- ✅ **功能强大**：支持复杂的文本匹配和替换
- ✅ **性能优秀**：经过优化的 C 语言实现
- ✅ **标准工具**：是文本处理的标准解决方案

---

## 4. re 模块导入

Python 的 `re` 模块是标准库（standard library（标准库））的一部分，无需安装，直接导入即可使用。

**基本导入方式**：

```python
import re  # 导入 re 模块
```

**导入后的使用方式**：

```python
import re

# 方式一：直接使用 re 模块的函数
result = re.search(r'\d+', 'abc123def')

# 方式二：先编译模式，再使用（推荐在多次使用时）
pattern = re.compile(r'\d+')
result = pattern.search('abc123def')
```

**为什么使用 `import re`**：

- ✅ **简洁明了**：直接表明使用的是正则表达式功能
- ✅ **标准做法**：Python 社区的标准导入方式
- ✅ **避免冲突**：不会与其他变量名冲突

---

## 5. 正则表达式基础语法

### 5.1 元字符（Metacharacters（元字符））

**元字符**（metacharacters（元字符））是正则表达式中具有特殊含义的字符，它们不代表字面意思，而是用来描述匹配规则。

**常用元字符**：

| 元字符 | 含义 | 示例 | 匹配结果 |
|--------|------|------|----------|
| `.` | 匹配除换行符外的任意字符 | `a.c` | `abc`、`a1c`、`a#c` |
| `^` | 匹配字符串开始 | `^hello` | `hello world`（匹配开头的 hello） |
| `$` | 匹配字符串结束 | `world$` | `hello world`（匹配结尾的 world） |
| `\d` | 匹配数字（0-9） | `\d+` | `123`、`456` |
| `\w` | 匹配字母、数字、下划线、汉字 | `\w+` | `hello`、`user123`、`用户` |
| `\s` | 匹配空白符（空格、制表符、换行等） | `\s+` | ` `（空格）、`\t`（制表符） |
| `\D` | 匹配非数字 | `\D+` | `abc`、`hello` |
| `\W` | 匹配非字母、数字、下划线 | `\W+` | `!!!`、`@#$` |
| `\S` | 匹配非空白符 | `\S+` | `hello`、`123` |

**示例代码**：

```python
import re

# 匹配任意字符
text = "cat bat hat"
result = re.findall(r'.at', text)
print(f"匹配 .at：{result}")  # 输出：['cat', 'bat', 'hat']

# 匹配字符串开头
text = "hello world"
if re.match(r'^hello', text):
    print("✅ 字符串以 hello 开头")

# 匹配字符串结尾
if re.search(r'world$', text):
    print("✅ 字符串以 world 结尾")

# 匹配数字
text = "我有 3 个苹果和 5 个橙子"
numbers = re.findall(r'\d+', text)
print(f"找到的数字：{numbers}")  # 输出：['3', '5']

# 匹配字母和数字
text = "用户名：user123"
result = re.findall(r'\w+', text)
print(f"找到的单词：{result}")  # 输出：['用户名', 'user123']

# 匹配空白符
text = "hello   world"
result = re.findall(r'\s+', text)
print(f"找到的空白符：{result}")  # 输出：['   ']
```

### 5.2 限定符（Quantifiers（限定符））

**限定符**（quantifiers（限定符））用于指定前面字符或模式的重复次数。

**常用限定符**：

| 限定符 | 含义 | 示例 | 匹配结果 |
|--------|------|------|----------|
| `*` | 匹配 0 次或多次（尽可能多） | `a*` | `""`、`a`、`aa`、`aaa` |
| `+` | 匹配 1 次或多次（尽可能多） | `a+` | `a`、`aa`、`aaa`（不匹配空字符串） |
| `?` | 匹配 0 次或 1 次 | `a?` | `""`、`a` |
| `{n}` | 恰好匹配 n 次 | `a{3}` | `aaa` |
| `{n,}` | 至少匹配 n 次 | `a{2,}` | `aa`、`aaa`、`aaaa` |
| `{n,m}` | 至少匹配 n 次，至多匹配 m 次 | `a{2,4}` | `aa`、`aaa`、`aaaa` |

**示例代码**：

```python
import re

# * 匹配 0 次或多次
text = "a aa aaa aaaa"
result = re.findall(r'a*', text)
print(f"匹配 a*：{result}")  # 输出：['a', '', 'aa', '', 'aaa', '', 'aaaa', '']

# + 匹配 1 次或多次（更常用）
result = re.findall(r'a+', text)
print(f"匹配 a+：{result}")  # 输出：['a', 'aa', 'aaa', 'aaaa']

# ? 匹配 0 次或 1 次
text = "color colour"
result = re.findall(r'colou?r', text)
print(f"匹配 colou?r：{result}")  # 输出：['color', 'colour']

# {n} 恰好匹配 n 次
text = "123 1234 12345 123456"
result = re.findall(r'\d{4}', text)  # 匹配恰好 4 位数字
print(f"匹配 \\d{{4}}：{result}")  # 输出：['1234', '1234', '1234', '1234']

# {n,m} 匹配 n 到 m 次
result = re.findall(r'\d{3,5}', text)  # 匹配 3 到 5 位数字
print(f"匹配 \\d{{3,5}}：{result}")  # 输出：['123', '1234', '12345', '12345']

# 实际应用：匹配电话号码（11 位数字）
phone = "我的电话是 13800138000"
result = re.findall(r'\d{11}', phone)
print(f"找到的电话号码：{result}")  # 输出：['13800138000']
```

**生活化比喻**：

- `*`：就像说"可以有，也可以没有，有多少要多少"（贪心）
- `+`：就像说"至少要有一个，越多越好"（贪心）
- `?`：就像说"有也行，没有也行，但最多一个"
- `{n}`：就像说"必须恰好 n 个，不多不少"

### 5.3 字符类（Character Classes（字符类））

**字符类**（character classes（字符类））用于匹配一组字符中的任意一个。

**常用字符类**：

| 字符类 | 含义 | 示例 | 匹配结果 |
|--------|------|------|----------|
| `[abc]` | 匹配 a、b 或 c | `[abc]` | `a`、`b`、`c` |
| `[0-9]` | 匹配 0 到 9 的数字 | `[0-9]+` | `123`、`456` |
| `[a-z]` | 匹配小写字母 | `[a-z]+` | `hello`、`world` |
| `[A-Z]` | 匹配大写字母 | `[A-Z]+` | `HELLO`、`WORLD` |
| `[a-zA-Z]` | 匹配所有字母 | `[a-zA-Z]+` | `Hello`、`World` |
| `[0-9a-fA-F]` | 匹配十六进制字符 | `[0-9a-fA-F]+` | `ff00ff`、`FF00FF` |
| `[^abc]` | 匹配除 a、b、c 外的任意字符 | `[^abc]` | `d`、`e`、`1`、`@` |

**示例代码**：

```python
import re

# 匹配指定字符
text = "cat bat hat"
result = re.findall(r'[cbh]at', text)
print(f"匹配 [cbh]at：{result}")  # 输出：['cat', 'bat', 'hat']

# 匹配数字范围
text = "成绩：85 分，排名：3 名"
result = re.findall(r'[0-9]+', text)
print(f"找到的数字：{result}")  # 输出：['85', '3']

# 匹配字母
text = "Hello World Python"
result = re.findall(r'[a-zA-Z]+', text)
print(f"找到的单词：{result}")  # 输出：['Hello', 'World', 'Python']

# 匹配十六进制颜色
text = "颜色：#ff00ff 和 #FF00FF"
result = re.findall(r'#[0-9a-fA-F]{6}', text)
print(f"找到的颜色：{result}")  # 输出：['#ff00ff', '#FF00FF']

# 排除特定字符（使用 ^）
text = "abc123def456"
result = re.findall(r'[^0-9]+', text)  # 匹配非数字
print(f"非数字部分：{result}")  # 输出：['abc', 'def']
```

**生活化比喻**：

- `[abc]`：就像选择题的选项，可以选择 a、b 或 c 中的任意一个
- `[0-9]`：就像选择 0 到 9 中的任意一个数字
- `[^abc]`：就像"除了 a、b、c 之外的都可以"

### 5.4 原始字符串（Raw String（原始字符串））

**原始字符串**（raw string（原始字符串））是以 `r` 或 `R` 开头的字符串，Python 不会处理其中的转义字符。

**为什么使用原始字符串**：

正则表达式中经常使用反斜杠（`\`），例如 `\d`（匹配数字）、`\w`（匹配单词字符）等。如果不使用原始字符串，反斜杠会被 Python 解释为转义字符，导致错误。

**对比示例**：

```python
import re

# ❌ 不使用原始字符串（容易出错）
pattern1 = "\\d+"  # 需要两个反斜杠
result1 = re.findall(pattern1, "abc123")
print(f"结果 1：{result1}")  # 输出：['123']

# ✅ 使用原始字符串（推荐）
pattern2 = r"\d+"  # 只需要一个反斜杠，更简洁
result2 = re.findall(pattern2, "abc123")
print(f"结果 2：{result2}")  # 输出：['123']

# 复杂模式对比
# ❌ 不使用原始字符串（难以阅读）
pattern3 = "\\\\w+\\\\s+\\\\d+"  # 匹配单词+空格+数字
# ✅ 使用原始字符串（清晰易读）
pattern4 = r"\w+\s+\d+"  # 匹配单词+空格+数字

text = "hello 123 world 456"
result4 = re.findall(pattern4, text)
print(f"结果 4：{result4}")  # 输出：['hello 123', 'world 456']
```

**最佳实践**：

- ✅ **总是使用原始字符串**：在定义正则表达式模式时，总是使用 `r""` 或 `R""`
- ✅ **避免转义问题**：原始字符串可以避免反斜杠转义的困扰
- ✅ **提高可读性**：代码更清晰，更容易理解和维护

**示例**：

```python
import re

# ✅ 推荐写法
pattern = r"\d{3}-\d{4}-\d{4}"  # 匹配电话号码格式：123-4567-8901
text = "我的电话：138-0013-8000"
result = re.findall(pattern, text)
print(f"找到的电话：{result}")  # 输出：['138-0013-8000']
```

---

## 6. 模式匹配（Pattern Matching（模式匹配））
<p align="right"><span style="background:#4caf50;color:#fff;padding:2px 6px;border-radius:4px">✅ Must（必做实践）｜依赖：Python 3.x</span></p>

**模式匹配**（pattern matching（模式匹配））是正则表达式的核心功能，用于在字符串中查找符合特定模式的内容。

### 6.1 re.match() 方法
<p align="right"><span style="background:#4caf50;color:#fff;padding:2px 6px;border-radius:4px">✅ Must（必做实践）</span></p>

`re.match()` 方法从字符串的 **开头** 开始匹配，如果开头匹配成功，返回匹配对象（match object（匹配对象））；否则返回 `None`。

**基本语法**：

```python
re.match(pattern, string, flags=0)
```

**生活化比喻**：就像检查一篇文章是否以特定标题开头。

**示例代码**：

```python
import re

# 匹配字符串开头
text1 = "hello world"
result1 = re.match(r'hello', text1)
if result1:
    print(f"✅ 匹配成功：{result1.group()}")  # 输出：✅ 匹配成功：hello
else:
    print("❌ 匹配失败")

# 不匹配开头的情况
text2 = "world hello"
result2 = re.match(r'hello', text2)
if result2:
    print(f"✅ 匹配成功：{result2.group()}")
else:
    print("❌ 匹配失败")  # 输出：❌ 匹配失败（因为 hello 不在开头）

# 匹配对象的方法
text3 = "2025-11-03 今天是周一"
result3 = re.match(r'(\d{4})-(\d{2})-(\d{2})', text3)
if result3:
    print(f"完整匹配：{result3.group()}")  # 输出：完整匹配：2025-11-03
    print(f"第一个分组：{result3.group(1)}")  # 输出：第一个分组：2025
    print(f"所有分组：{result3.groups()}")  # 输出：所有分组：('2025', '11', '03')
    print(f"匹配位置：{result3.span()}")  # 输出：匹配位置：(0, 10)
```

**匹配对象的常用方法**：

| 方法 | 说明 | 示例 |
|------|------|------|
| `group()` | 返回匹配的完整字符串 | `result.group()` → `'2025-11-03'` |
| `group(n)` | 返回第 n 个分组 | `result.group(1)` → `'2025'` |
| `groups()` | 返回所有分组的元组 | `result.groups()` → `('2025', '11', '03')` |
| `span()` | 返回匹配位置的元组（开始，结束） | `result.span()` → `(0, 10)` |
| `start()` | 返回匹配开始位置 | `result.start()` → `0` |
| `end()` | 返回匹配结束位置 | `result.end()` → `10` |

### 6.2 re.search() 方法
<p align="right"><span style="background:#4caf50;color:#fff;padding:2px 6px;border-radius:4px">✅ Must（必做实践）</span></p>

`re.search()` 方法扫描整个字符串，返回第一个匹配的对象；如果未找到，返回 `None`。

**基本语法**：

```python
re.search(pattern, string, flags=0)
```

**生活化比喻**：就像在一篇文章中搜索关键词，找到第一个出现的位置。

**示例代码**：

```python
import re

# 搜索整个字符串
text = "我的电话是 138-0013-8000，QQ 号是 123456789"
result = re.search(r'\d{11}', text)  # 搜索 11 位数字
if result:
    print(f"✅ 找到电话号码：{result.group()}")  # 输出：✅ 找到电话号码：13800138000
    print(f"位置：{result.span()}")  # 输出：位置：(5, 16)
else:
    print("❌ 未找到")

# 搜索多个数字
text2 = "价格：99 元，折扣：8.5 折"
result2 = re.search(r'\d+\.?\d*', text2)  # 匹配数字（包括小数）
if result2:
    print(f"找到的数字：{result2.group()}")  # 输出：找到的数字：99（只返回第一个匹配）

# 使用分组提取信息
text3 = "姓名：张三，年龄：25 岁"
result3 = re.search(r'姓名：(\w+)，年龄：(\d+)', text3)
if result3:
    name, age = result3.groups()
    print(f"姓名：{name}，年龄：{age}")  # 输出：姓名：张三，年龄：25
```

### 6.3 match() vs search() 对比
<p align="right"><span style="background:#2196f3;color:#fff;padding:2px 6px;border-radius:4px">⭐ Should（建议实践）</span></p>

**核心区别**：

| 方法 | 匹配位置 | 返回值 | 使用场景 |
|------|---------|--------|----------|
| `re.match()` | 只匹配字符串开头 | 开头匹配成功返回匹配对象，否则返回 `None` | 验证字符串格式、检查开头 |
| `re.search()` | 搜索整个字符串 | 找到第一个匹配返回匹配对象，否则返回 `None` | 查找字符串中的内容 |

**对比示例**：

```python
import re

text = "hello world hello python"

# match() 只匹配开头
result_match = re.match(r'hello', text)
print(f"match() 结果：{result_match.group() if result_match else 'None'}")  # 输出：hello

result_match2 = re.match(r'world', text)
print(f"match() 结果：{result_match2.group() if result_match2 else 'None'}")  # 输出：None（world 不在开头）

# search() 搜索整个字符串
result_search = re.search(r'world', text)
print(f"search() 结果：{result_search.group() if result_search else 'None'}")  # 输出：world

result_search2 = re.search(r'python', text)
print(f"search() 结果：{result_search2.group() if result_search2 else 'None'}")  # 输出：python

# 实际应用场景
# ✅ 使用 match() 验证格式
email = "user@example.com"
if re.match(r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$', email):
    print("✅ 邮箱格式正确")

# ✅ 使用 search() 查找内容
log = "2025-11-03 ERROR: Database connection failed"
error = re.search(r'ERROR: (.+)', log)
if error:
    print(f"错误信息：{error.group(1)}")  # 输出：错误信息：Database connection failed
```

**选择建议**：

- **使用 `match()`**：当需要验证字符串是否符合特定格式，且必须从开头匹配时
- **使用 `search()`**：当需要在字符串中查找特定内容，不管位置时（**更常用**）

---

## 7. 搜索所有匹配（Finding All Matches（搜索所有匹配））

### 7.1 re.findall() 方法
<p align="right"><span style="background:#4caf50;color:#fff;padding:2px 6px;border-radius:4px">✅ Must（必做实践）</span></p>

`re.findall()` 方法返回字符串中所有与正则表达式匹配的非重叠子串列表（list（列表））。

**基本语法**：

```python
re.findall(pattern, string, flags=0)
```

**返回值**：如果模式包含分组（groups（分组）），返回所有分组的元组列表；如果不包含分组，返回匹配字符串的列表；如果没有匹配，返回空列表。

**生活化比喻**：就像用筛子筛东西，把所有符合条件的内容都筛选出来，装在一个篮子里。

**示例代码**：

```python
import re

# 查找所有数字
text = "我有 3 个苹果、5 个橙子和 8 个香蕉"
numbers = re.findall(r'\d+', text)
print(f"找到的数字：{numbers}")  # 输出：['3', '5', '8']

# 查找所有邮箱地址
text2 = "联系邮箱：admin@example.com 和 support@test.org"
emails = re.findall(r'[\w.-]+@[\w.-]+\.\w+', text2)
print(f"找到的邮箱：{emails}")  # 输出：['admin@example.com', 'support@test.org']

# 使用分组（返回分组内容）
text3 = "日期：2025-11-03 和 2025-12-25"
dates = re.findall(r'(\d{4})-(\d{2})-(\d{2})', text3)
print(f"找到的日期：{dates}")  # 输出：[('2025', '11', '03'), ('2025', '12', '25')]

# 不使用分组（返回完整匹配）
dates_full = re.findall(r'\d{4}-\d{2}-\d{2}', text3)
print(f"完整日期：{dates_full}")  # 输出：['2025-11-03', '2025-12-25']

# 没有匹配时返回空列表
text4 = "这里没有任何数字"
result = re.findall(r'\d+', text4)
print(f"结果：{result}")  # 输出：[]（空列表）
```

**注意事项**：

- ✅ **返回列表**：无论匹配多少项，都返回列表（list（列表））
- ✅ **非重叠匹配**：匹配的子串不会重叠，例如 `r'\w+'` 匹配 "hello world" 会得到 `['hello', 'world']`，而不是重叠的结果
- ✅ **分组行为**：如果模式包含分组（parentheses（圆括号）），返回分组的元组列表，而不是完整匹配

### 7.2 re.finditer() 方法
<p align="right"><span style="background:#fb8c00;color:#fff;padding:2px 6px;border-radius:4px">⭐ Should（建议实践）</span></p>

`re.finditer()` 方法返回一个迭代器（iterator（迭代器）），包含字符串中所有非重叠匹配的匹配对象。

**基本语法**：

```python
re.finditer(pattern, string, flags=0)
```

**返回值**：一个迭代器，每个元素是一个匹配对象（match object（匹配对象）），可以访问匹配的内容、位置等信息。

**生活化比喻**：就像用探照灯扫描，每找到一个匹配就停下来告诉你位置和内容，然后继续扫描下一个。

**示例代码**：

```python
import re

# 查找所有数字及其位置
text = "价格：99 元，折扣：8.5 折，运费：10 元"
matches = re.finditer(r'\d+\.?\d*', text)  # 匹配整数或小数

for match in matches:
    print(f"找到：{match.group()}，位置：{match.span()}，开始：{match.start()}，结束：{match.end()}")
# 输出：
# 找到：99，位置：(3, 5)，开始：3，结束：5
# 找到：8.5，位置：(10, 13)，开始：10，结束：13
# 找到：10，位置：(18, 20)，开始：18，结束：20

# 提取所有邮箱及其详细信息
text2 = "联系 admin@example.com 或 support@test.org"
email_pattern = r'([\w.-]+)@([\w.-]+)\.(\w+)'
for match in re.finditer(email_pattern, text2):
    username, domain, ext = match.groups()
    print(f"用户名：{username}，域名：{domain}.{ext}，完整：{match.group()}")
# 输出：
# 用户名：admin，域名：example.com，完整：admin@example.com
# 用户名：support，域名：test.org，完整：support@test.org

# 获取所有匹配的详细信息列表
text3 = "Python 3.9, Python 3.10, Python 3.11"
matches = list(re.finditer(r'Python (\d+\.\d+)', text3))
print(f"找到 {len(matches)} 个匹配")
for i, match in enumerate(matches, 1):
    print(f"第 {i} 个：版本 {match.group(1)}，位置 {match.span()}")
```

**finditer() 的优势**：

- ✅ **内存效率**：对于大量匹配，使用迭代器可以节省内存（lazy evaluation（惰性求值））
- ✅ **详细信息**：可以访问每个匹配的位置、分组等详细信息
- ✅ **灵活处理**：可以在找到匹配时立即处理，不需要等待所有匹配完成

### 7.3 findall() vs finditer() 对比
<p align="right"><span style="background:#2196f3;color:#fff;padding:2px 6px;border-radius:4px">⭐ Should（建议实践）</span></p>

**核心区别**：

| 方法 | 返回值 | 数据类型 | 适用场景 | 内存效率 |
|------|--------|----------|----------|----------|
| `re.findall()` | 列表（list（列表）） | 字符串或元组列表 | 需要所有匹配结果 | 需要一次性加载所有结果 |
| `re.finditer()` | 迭代器（iterator（迭代器）） | 匹配对象迭代器 | 需要匹配位置信息或逐个处理 | 更节省内存（惰性求值） |

**对比示例**：

```python
import re

text = "Python 3.9, Python 3.10, Python 3.11, Python 3.12"

# 使用 findall()：直接获取所有版本号
versions_all = re.findall(r'Python (\d+\.\d+)', text)
print(f"所有版本：{versions_all}")  # 输出：['3.9', '3.10', '3.11', '3.12']

# 使用 finditer()：逐个处理，获取位置信息
print("\n使用 finditer() 逐个处理：")
for match in re.finditer(r'Python (\d+\.\d+)', text):
    version = match.group(1)
    start, end = match.span()
    print(f"版本 {version} 在位置 {start}-{end}")

# 实际应用场景对比
# ✅ 使用 findall()：只需要匹配内容，不需要位置
emails = re.findall(r'[\w.-]+@[\w.-]+\.\w+', "联系 admin@test.com 或 user@example.org")
print(f"\n邮箱列表：{emails}")  # 输出：['admin@test.com', 'user@example.org']

# ✅ 使用 finditer()：需要位置信息或逐个处理大量数据
log_text = "ERROR: 第 10 行有问题\nWARNING: 第 25 行有警告\nERROR: 第 50 行有错误"
errors = []
for match in re.finditer(r'ERROR: (.+)', log_text):
    errors.append({
        'message': match.group(1),
        'position': match.span(),
        'line': log_text[:match.start()].count('\n') + 1
    })
print(f"\n错误信息：{errors}")
```

**选择建议**：

- **使用 `findall()`**：当只需要匹配的文本内容，不需要位置信息，且匹配数量不多时
- **使用 `finditer()`**：当需要匹配的位置信息、分组详情，或需要处理大量匹配以节省内存时（**推荐用于大数据场景**）

---

## 8. 替换（Substitution（替换））
<p align="right"><span style="background:#4caf50;color:#fff;padding:2px 6px;border-radius:4px">✅ Must（必做实践）</span></p>

**替换**（substitution（替换））是正则表达式的重要功能，用于将匹配的文本替换为新的内容。

### 8.1 re.sub() 方法
<p align="right"><span style="background:#4caf50;color:#fff;padding:2px 6px;border-radius:4px">✅ Must（必做实践）</span></p>

`re.sub()` 方法用于替换字符串中所有与正则表达式匹配的子串，返回替换后的新字符串。

**基本语法**：

```python
re.sub(pattern, repl, string, count=0, flags=0)
```

**参数说明**：
- `pattern`：正则表达式模式
- `repl`：替换内容，可以是字符串或函数（function（函数））
- `string`：要被处理的字符串
- `count`：最大替换次数（0 表示替换所有匹配）
- `flags`：标志（flags（标志））

**生活化比喻**：就像文字处理软件中的"查找和替换"功能，自动把所有符合条件的内容替换成新的内容。

**示例代码**：

```python
import re

# 简单替换：将所有数字替换为 "数字"
text = "我有 3 个苹果和 5 个橙子"
result = re.sub(r'\d+', "数字", text)
print(f"替换后：{result}")  # 输出：我有 数字 个苹果和 数字 个橙子

# 限制替换次数
text2 = "1 2 3 4 5"
result2 = re.sub(r'\d+', "数字", text2, count=2)  # 只替换前 2 个
print(f"替换后：{result2}")  # 输出：数字 数字 3 4 5

# 替换邮箱域名
text3 = "联系 admin@example.com 或 user@test.org"
result3 = re.sub(r'@[\w.-]+', "@newdomain.com", text3)
print(f"替换后：{result3}")  # 输出：联系 admin@newdomain.com 或 user@newdomain.com

# 使用函数进行替换（动态替换）
def double_number(match):
    """将匹配的数字乘以 2"""
    num = int(match.group())
    return str(num * 2)

text4 = "价格：10 元，折扣：5 元"
result4 = re.sub(r'\d+', double_number, text4)
print(f"替换后：{result4}")  # 输出：价格：20 元，折扣：10 元

# 脱敏处理：隐藏手机号中间部分
def mask_phone(match):
    """将手机号中间 4 位替换为星号"""
    phone = match.group()
    return phone[:3] + "****" + phone[7:]

text5 = "我的电话：13800138000，备用：13900139000"
result5 = re.sub(r'\d{11}', mask_phone, text5)
print(f"脱敏后：{result5}")  # 输出：我的电话：138****8000，备用：139****9000
```

**使用函数替换的优势**：

- ✅ **动态替换**：可以根据匹配内容动态生成替换结果
- ✅ **复杂逻辑**：可以实现复杂的替换逻辑
- ✅ **格式化处理**：可以对匹配内容进行格式化处理

### 8.2 re.subn() 方法
<p align="right"><span style="background:#2196f3;color:#fff;padding:2px 6px;border-radius:4px">⭐ Should（建议实践）</span></p>

`re.subn()` 方法与 `re.sub()` 功能相同，但会返回一个元组（tuple（元组）），包含替换后的字符串和替换次数。

**基本语法**：

```python
re.subn(pattern, repl, string, count=0, flags=0)
```

**返回值**：`(新字符串, 替换次数)` 元组。

**生活化比喻**：就像替换时不仅告诉你替换后的结果，还告诉你替换了多少处。

**示例代码**：

```python
import re

# 基本使用
text = "Python 3.9, Python 3.10, Python 3.11"
result, count = re.subn(r'Python', "Java", text)
print(f"替换后：{result}")  # 输出：Java 3.9, Java 3.10, Java 3.11
print(f"替换次数：{count}")  # 输出：3

# 限制替换次数
text2 = "1 2 3 4 5"
result2, count2 = re.subn(r'\d+', "数字", text2, count=2)
print(f"替换后：{result2}")  # 输出：数字 数字 3 4 5
print(f"替换次数：{count2}")  # 输出：2

# 实际应用：统计替换操作
text3 = "错误：数据库连接失败\n错误：文件未找到\n警告：内存不足"
result3, error_count = re.subn(r'错误：', "ERROR: ", text3)
print(f"处理后的日志：\n{result3}")
print(f"共替换 {error_count} 处错误标识")

# 验证替换是否成功
if error_count > 0:
    print(f"✅ 成功处理 {error_count} 处错误")
else:
    print("⚠️ 未找到错误信息")
```

**subn() 的优势**：

- ✅ **替换统计**：可以知道替换了多少处，便于验证和调试
- ✅ **操作反馈**：确认替换操作是否成功执行
- ✅ **日志记录**：可以记录替换操作的次数

### 8.3 替换中使用分组
<p align="right"><span style="background:#fb8c00;color:#fff;padding:2px 6px;border-radius:4px">⭐ Should（建议实践）</span></p>

在替换字符串中，可以使用 `\n`（n 为分组编号）或 `\g<n>` 来引用分组（groups（分组））内容，实现灵活的替换。

**基本语法**：

- `\1`, `\2`, `\3` 等：引用第 1、2、3 个分组
- `\g<1>`, `\g<2>` 等：引用分组（更明确的写法）
- `\g<name>`：引用命名分组（named group（命名分组））

**生活化比喻**：就像填写模板，把原文的一部分内容提取出来，重新排列或修改格式。

**示例代码**：

```python
import re

# 重新排列日期格式：从 YYYY-MM-DD 改为 DD/MM/YYYY
text = "日期：2025-11-03 和 2025-12-25"
result = re.sub(r'(\d{4})-(\d{2})-(\d{2})', r'\3/\2/\1', text)
print(f"转换后：{result}")  # 输出：日期：03/11/2025 和 25/12/2025

# 交换姓名顺序：从 "姓 名" 改为 "名, 姓"
text2 = "姓名：张 三"
result2 = re.sub(r'(\w+) (\w+)', r'\2, \1', text2)
print(f"转换后：{result2}")  # 输出：姓名：三, 张

# 格式化电话号码：从 "13800138000" 改为 "138-0013-8000"
text3 = "电话：13800138000"
result3 = re.sub(r'(\d{3})(\d{4})(\d{4})', r'\1-\2-\3', text3)
print(f"格式化后：{result3}")  # 输出：电话：138-0013-8000

# 使用命名分组（更清晰）
text4 = "日期：2025-11-03"
result4 = re.sub(
    r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})',
    r'\g<day>/\g<month>/\g<year>',
    text4
)
print(f"转换后：{result4}")  # 输出：日期：03/11/2025

# 实际应用：提取并格式化邮箱
def format_email(match):
    """格式化邮箱显示"""
    username = match.group(1)
    domain = match.group(2)
    return f"{username} [at] {domain.replace('.', ' [dot] ')}"

text5 = "联系 admin@example.com"
result5 = re.sub(r'([\w.-]+)@([\w.-]+\.\w+)', format_email, text5)
print(f"格式化后：{result5}")  # 输出：联系 admin [at] example [dot] com

# 组合使用：保留部分内容，替换部分内容
text6 = "价格：100 元，折扣：50 元"
# 将价格增加 10%，但保留"元"字
result6 = re.sub(r'(\d+)', lambda m: str(int(m.group(1)) * 110 // 100), text6)
print(f"调整后：{result6}")  # 输出：价格：110 元，折扣：55 元
```

**分组替换的优势**：

- ✅ **保留原内容**：可以提取原文的一部分，重新组合
- ✅ **格式转换**：轻松实现不同格式之间的转换
- ✅ **灵活重组**：可以任意重新排列匹配的内容

**注意事项**：

- ✅ **分组编号**：从左到右，第一个 `()` 是 `\1`，第二个是 `\2`，依此类推
- ✅ **转义问题**：在替换字符串中使用 `\1` 等，需要使用原始字符串 `r''` 或双反斜杠 `\\1`

---

## 9. 分割字符串（Splitting（分割））
<p align="right"><span style="background:#4caf50;color:#fff;padding:2px 6px;border-radius:4px">✅ Must（必做实践）</span></p>

### 9.1 re.split() 方法
<p align="right"><span style="background:#4caf50;color:#fff;padding:2px 6px;border-radius:4px">✅ Must（必做实践）</span></p>

`re.split()` 方法根据正则表达式匹配的模式分割字符串，返回分割后的列表（list（列表））。

**基本语法**：

```python
re.split(pattern, string, maxsplit=0, flags=0)
```

**参数说明**：
- `pattern`：正则表达式模式（用作分割符（delimiter（分隔符）））
- `string`：要被分割的字符串
- `maxsplit`：最大分割次数（0 表示不限制）
- `flags`：标志（flags（标志））

**生活化比喻**：就像用剪刀沿着指定的线（正则模式）剪断绳子，把绳子分成若干段。

**示例代码**：

```python
import re

# 基本分割：按空白符分割
text = "Python  Java   C++  Go"
result = re.split(r'\s+', text)  # 匹配一个或多个空白符
print(f"分割结果：{result}")  # 输出：['Python', 'Java', 'C++', 'Go']

# 按多个分隔符分割：逗号、分号、空格
text2 = "苹果,香蕉;橙子 葡萄"
result2 = re.split(r'[,;\s]+', text2)
print(f"分割结果：{result2}")  # 输出：['苹果', '香蕉', '橙子', '葡萄']

# 限制分割次数
text3 = "1-2-3-4-5"
result3 = re.split(r'-', text3, maxsplit=2)  # 最多分割 2 次
print(f"分割结果：{result3}")  # 输出：['1', '2', '3-4-5']

# 保留分隔符（使用分组）
text4 = "2025-11-03"
result4 = re.split(r'(-)', text4)  # 用括号包裹分隔符，会保留在结果中
print(f"分割结果：{result4}")  # 输出：['2025', '-', '11', '-', '03']

# 处理连续分隔符（自动去除空字符串）
text5 = "a,,b,,,c"
result5 = re.split(r',+', text5)  # 匹配一个或多个逗号
print(f"分割结果：{result5}")  # 输出：['a', 'b', 'c']

# 实际应用：解析日志行
log_line = "2025-11-03 10:30:45 ERROR: Database connection failed"
parts = re.split(r'\s+', log_line, maxsplit=3)
print(f"时间：{parts[0]} {parts[1]}")
print(f"级别：{parts[2]}")
print(f"消息：{parts[3]}")

# 分割时使用复杂模式
text6 = "姓名:张三,年龄:25,城市:北京"
result6 = re.split(r'[,:]', text6)  # 按逗号或冒号分割
print(f"分割结果：{result6}")  # 输出：['姓名', '张三', '年龄', '25', '城市', '北京']
```

**split() vs 字符串 split() 方法对比**：

```python
import re

text = "Python,Java,C++,Go"

# ❌ 字符串 split()：只能按固定字符分割
result1 = text.split(',')
print(f"字符串 split()：{result1}")  # 输出：['Python', 'Java', 'C++', 'Go']

# ✅ re.split()：可以按模式分割，更灵活
text2 = "Python, Java; C++  Go"
result2 = re.split(r'[,;\s]+', text2)  # 按逗号、分号、空白符分割
print(f"re.split()：{result2}")  # 输出：['Python', 'Java', 'C++', 'Go']
```

**注意事项**：

- ✅ **空字符串**：如果字符串开头或结尾匹配模式，会在结果列表开头或结尾产生空字符串
- ✅ **分组保留**：如果模式包含分组（parentheses（圆括号）），分组内容会保留在结果中
- ✅ **性能考虑**：简单分割使用字符串 `split()` 方法更高效，复杂模式才使用 `re.split()`

---

## 10. 编译正则表达式（Compiling（编译））
<p align="right"><span style="background:#2196f3;color:#fff;padding:2px 6px;border-radius:4px">⭐ Should（建议实践）</span></p>

### 10.1 re.compile() 方法
<p align="right"><span style="background:#2196f3;color:#fff;padding:2px 6px;border-radius:4px">⭐ Should（建议实践）</span></p>

`re.compile()` 方法将正则表达式模式编译为一个正则表达式对象（pattern object（模式对象）），可以重复使用，提高性能。

**基本语法**：

```python
re.compile(pattern, flags=0)
```

**返回值**：一个正则表达式对象（pattern object（模式对象）），可以使用 `match()`、`search()`、`findall()` 等方法。

**生活化比喻**：就像先把模板准备好（编译），然后可以多次使用这个模板来匹配不同的文本，比每次都重新制作模板更高效。

**示例代码**：

```python
import re

# 编译正则表达式
pattern = re.compile(r'\d{3}-\d{4}-\d{4}')  # 编译电话号码模式

# 重复使用编译后的模式
text1 = "电话：138-0013-8000"
text2 = "备用：139-0014-9000"
text3 = "工作：150-0025-6000"

# 使用编译后的模式进行匹配
match1 = pattern.search(text1)
match2 = pattern.search(text2)
match3 = pattern.search(text3)

if match1:
    print(f"找到电话：{match1.group()}")  # 输出：找到电话：138-0013-8000
if match2:
    print(f"找到备用：{match2.group()}")  # 输出：找到备用：139-0014-9000
if match3:
    print(f"找到工作：{match3.group()}")  # 输出：找到工作：150-0025-6000

# 编译后的模式可以使用所有方法
email_pattern = re.compile(r'[\w.-]+@[\w.-]+\.\w+')
text = "联系 admin@example.com 或 support@test.org"

# 使用 findall()
emails = email_pattern.findall(text)
print(f"所有邮箱：{emails}")  # 输出：['admin@example.com', 'support@test.org']

# 使用 finditer()
for match in email_pattern.finditer(text):
    print(f"邮箱：{match.group()}，位置：{match.span()}")

# 使用 sub()
result = email_pattern.sub("***@***.***", text)
print(f"脱敏后：{result}")  # 输出：联系 ***@***.*** 或 ***@***.***

# 编译时指定标志
case_insensitive_pattern = re.compile(r'python', re.IGNORECASE)
text = "Python is great, PYTHON is powerful, python is simple"
matches = case_insensitive_pattern.findall(text)
print(f"匹配结果：{matches}")  # 输出：['Python', 'PYTHON', 'python']
```

### 10.2 何时使用 compile()
<p align="right"><span style="background:#1e88e5;color:#fff;padding:2px 6px;border-radius:4px">💡 Could（可选实践）</span></p>

**使用 `compile()` 的场景**：

| 场景 | 是否使用 compile() | 原因 |
|------|------------------|------|
| 模式只使用一次 | ❌ 不使用 | 直接使用 `re.match()` 等函数更简洁 |
| 模式重复使用多次 | ✅ 使用 | 编译一次，多次使用，性能更好 |
| 需要设置标志（flags） | ✅ 使用 | 可以在编译时一次性设置所有标志 |
| 代码可读性要求高 | ✅ 使用 | 模式名称可以增加代码可读性 |

**性能对比示例**：

```python
import re
import time

text = "Python 3.9, Python 3.10, Python 3.11, Python 3.12"
pattern_str = r'Python (\d+\.\d+)'

# 方式一：不使用 compile()（每次调用都重新编译）
start1 = time.time()
for _ in range(10000):
    result = re.findall(pattern_str, text)
time1 = time.time() - start1

# 方式二：使用 compile()（只编译一次）
pattern_obj = re.compile(pattern_str)
start2 = time.time()
for _ in range(10000):
    result = pattern_obj.findall(text)
time2 = time.time() - start2

print(f"不使用 compile()：{time1:.4f} 秒")
print(f"使用 compile()：{time2:.4f} 秒")
print(f"性能提升：{(time1 - time2) / time1 * 100:.1f}%")

# 输出示例：
# 不使用 compile()：0.0123 秒
# 使用 compile()：0.0089 秒
# 性能提升：27.6%
```

**实际应用建议**：

```python
import re

# ✅ 推荐：模式在函数或类中重复使用
class EmailValidator:
    def __init__(self):
        # 编译一次，多次使用
        self.email_pattern = re.compile(r'^[\w.-]+@[\w.-]+\.\w+$')
    
    def validate(self, email):
        return self.email_pattern.match(email) is not None

validator = EmailValidator()
print(validator.validate("user@example.com"))  # 输出：True
print(validator.validate("invalid-email"))  # 输出：False

# ✅ 推荐：需要组合多个标志
multiline_pattern = re.compile(
    r'^\d+\.\s+.+$',  # 匹配"数字. 文本"格式
    flags=re.MULTILINE | re.IGNORECASE
)

# ❌ 不推荐：只使用一次的模式
text = "价格：100 元"
result = re.findall(r'\d+', text)  # 直接使用即可，不需要 compile()
```

**最佳实践总结**：

- ✅ **重复使用**：当同一个模式需要多次使用时，使用 `compile()` 可以提高性能
- ✅ **代码组织**：使用 `compile()` 可以让代码更清晰，模式名称具有语义化
- ✅ **标志设置**：需要在多个地方使用相同标志时，在编译时设置更方便
- ❌ **一次性使用**：如果模式只使用一次，直接使用 `re.match()` 等函数即可，更简洁

---

## 11. 分组与捕获（Grouping and Capturing（分组与捕获））
<p align="right"><span style="background:#fb8c00;color:#fff;padding:2px 6px;border-radius:4px">⭐ Should（建议实践）</span></p>

**分组**（grouping（分组））是正则表达式的重要特性，可以将部分模式用圆括号 `()` 包裹，形成一个分组，便于提取和引用匹配的内容。

### 11.1 基本分组
<p align="right"><span style="background:#fb8c00;color:#fff;padding:2px 6px;border-radius:4px">⭐ Should（建议实践）</span></p>

**基本分组**使用圆括号 `()` 将模式的一部分包裹起来，形成分组。分组可以用于提取匹配的内容，也可以用于替换时引用。

**基本语法**：`(pattern)` - 创建一个分组。

**生活化比喻**：就像给文件分类，把相关的文件放在一个文件夹（分组）里，便于管理和查找。

**示例代码**：

```python
import re

# 提取日期各部分
text = "日期：2025-11-03"
match = re.search(r'(\d{4})-(\d{2})-(\d{2})', text)
if match:
    print(f"完整匹配：{match.group()}")  # 输出：2025-11-03
    print(f"年份：{match.group(1)}")  # 输出：2025
    print(f"月份：{match.group(2)}")  # 输出：11
    print(f"日期：{match.group(3)}")  # 输出：03
    print(f"所有分组：{match.groups()}")  # 输出：('2025', '11', '03')

# 提取邮箱用户名和域名
text2 = "联系 admin@example.com"
match2 = re.search(r'([\w.-]+)@([\w.-]+\.\w+)', text2)
if match2:
    username, domain = match2.groups()
    print(f"用户名：{username}")  # 输出：admin
    print(f"域名：{domain}")  # 输出：example.com

# 使用分组进行条件匹配
text3 = "color colour"
# colou?r 表示 u 可选，用分组可以更明确
match3 = re.findall(r'colou?r', text3)
print(f"匹配结果：{match3}")  # 输出：['color', 'colour']

# 分组用于提取电话号码各部分
text4 = "电话：138-0013-8000"
match4 = re.search(r'(\d{3})-(\d{4})-(\d{4})', text4)
if match4:
    area_code, middle, last = match4.groups()
    print(f"区号：{area_code}，中间：{middle}，后四位：{last}")
```

**分组编号**：
- `group(0)` 或 `group()`：完整的匹配内容
- `group(1)`：第一个分组
- `group(2)`：第二个分组
- 依此类推...

### 11.2 命名分组
<p align="right"><span style="background:#1e88e5;color:#fff;padding:2px 6px;border-radius:4px">💡 Could（可选实践）</span></p>

**命名分组**（named group（命名分组））使用 `(?P<name>pattern)` 语法，给分组指定名称，使代码更清晰易读。

**基本语法**：`(?P<name>pattern)` - 创建一个命名分组。

**生活化比喻**：就像给文件夹起名字，使用有意义的名称，比使用编号更容易理解和维护。

**示例代码**：

```python
import re

# 使用命名分组提取日期
text = "日期：2025-11-03"
match = re.search(r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})', text)
if match:
    print(f"年份：{match.group('year')}")  # 输出：2025
    print(f"月份：{match.group('month')}")  # 输出：11
    print(f"日期：{match.group('day')}")  # 输出：03
    print(f"所有命名分组：{match.groupdict()}")  # 输出：{'year': '2025', 'month': '11', 'day': '03'}

# 提取邮箱信息
text2 = "联系 admin@example.com"
match2 = re.search(r'(?P<username>[\w.-]+)@(?P<domain>[\w.-]+\.\w+)', text2)
if match2:
    print(f"用户名：{match2.group('username')}")  # 输出：admin
    print(f"域名：{match2.group('domain')}")  # 输出：example.com

# 命名分组在替换中的使用
text3 = "日期：2025-11-03"
result = re.sub(
    r'(?P<year>\d{4})-(?P<month>\d{2})-(?P<day>\d{2})',
    r'\g<day>/\g<month>/\g<year>',
    text3
)
print(f"转换后：{result}")  # 输出：日期：03/11/2025
```

**命名分组的优势**：
- ✅ **代码可读性**：使用有意义的名称，代码更容易理解
- ✅ **维护性**：不依赖分组位置，修改正则表达式时更安全
- ✅ **易于调试**：`groupdict()` 方法返回字典，便于查看所有分组

### 11.3 非捕获分组
<p align="right"><span style="background:#1e88e5;color:#fff;padding:2px 6px;border-radius:4px">💡 Could（可选实践）</span></p>

**非捕获分组**（non-capturing group（非捕获分组））使用 `(?:pattern)` 语法，用于分组但不捕获内容，不会在 `groups()` 中出现。

**基本语法**：`(?:pattern)` - 创建一个非捕获分组。

**生活化比喻**：就像临时文件夹，临时组织文件但不保留，不需要的时候就不保存。

**示例代码**：

```python
import re

# 使用非捕获分组
text = "颜色：red 或 colour：blue"
# 使用 (?:u)? 表示 u 可选但不捕获
match = re.findall(r'colou?r', text)  # 不使用分组
print(f"匹配结果：{match}")  # 输出：['color', 'colour']

# 对比：捕获分组 vs 非捕获分组
text2 = "Python 3.9 和 Python 3.10"

# 捕获分组：会返回分组内容
result1 = re.findall(r'(Python) (\d+\.\d+)', text2)
print(f"捕获分组：{result1}")  # 输出：[('Python', '3.9'), ('Python', '3.10')]

# 非捕获分组：不返回分组内容，只用于逻辑分组
result2 = re.findall(r'(?:Python) (\d+\.\d+)', text2)
print(f"非捕获分组：{result2}")  # 输出：['3.9', '3.10']（只返回第二个分组）

# 实际应用：匹配但不保存重复部分
text3 = "日期：2025-11-03 和 2025-12-25"
# 只提取月份和日期，不提取年份
result3 = re.findall(r'\d{4}-(\d{2})-(\d{2})', text3)
print(f"只提取月日：{result3}")  # 输出：[('11', '03'), ('12', '25')]

# 使用非捕获分组优化性能（减少内存占用）
pattern = re.compile(r'(?:https?://)?([\w.-]+\.\w+)')  # 可选协议，只捕获域名
text4 = "访问 https://example.com 或 http://test.org"
domains = pattern.findall(text4)
print(f"域名：{domains}")  # 输出：['example.com', 'test.org']
```

**非捕获分组的优势**：
- ✅ **性能优化**：减少捕获的分组数量，节省内存
- ✅ **逻辑分组**：可以用于分组但不保存，只用于控制匹配逻辑
- ✅ **清晰意图**：明确表示某些分组不需要提取

---

## 12. 标志（Flags（标志））
<p align="right"><span style="background:#fb8c00;color:#fff;padding:2px 6px;border-radius:4px">⭐ Should（建议实践）</span></p>

**标志**（flags（标志））用于修改正则表达式的匹配行为，如忽略大小写、多行模式等。

### 12.1 re.IGNORECASE（忽略大小写）
<p align="right"><span style="background:#fb8c00;color:#fff;padding:2px 6px;border-radius:4px">⭐ Should（建议实践）</span></p>

`re.IGNORECASE`（简写 `re.I`）标志使匹配忽略大小写（case-insensitive（不区分大小写））。

**示例代码**：

```python
import re

# 不使用标志：区分大小写
text = "Python is great, PYTHON is powerful, python is simple"
result1 = re.findall(r'python', text)
print(f"区分大小写：{result1}")  # 输出：['python']（只匹配小写）

# 使用 IGNORECASE 标志：忽略大小写
result2 = re.findall(r'python', text, re.IGNORECASE)
print(f"忽略大小写：{result2}")  # 输出：['Python', 'PYTHON', 'python']

# 使用简写形式
result3 = re.findall(r'python', text, re.I)
print(f"使用简写：{result3}")  # 输出：['Python', 'PYTHON', 'python']

# 编译时设置标志
pattern = re.compile(r'python', re.I)
result4 = pattern.findall(text)
print(f"编译时设置：{result4}")  # 输出：['Python', 'PYTHON', 'python']
```

### 12.2 re.MULTILINE（多行模式）
<p align="right"><span style="background:#fb8c00;color:#fff;padding:2px 6px;border-radius:4px">⭐ Should（建议实践）</span></p>

`re.MULTILINE`（简写 `re.M`）标志使 `^` 和 `$` 匹配每一行的开始和结束，而不仅仅是整个字符串的开始和结束。

**示例代码**：

```python
import re

text = """第一行：Python
第二行：Java
第三行：Python"""

# 不使用 MULTILINE：只匹配整个字符串
result1 = re.findall(r'^Python', text)
print(f"不使用 MULTILINE：{result1}")  # 输出：['Python']（只匹配开头）

# 使用 MULTILINE：匹配每行开头
result2 = re.findall(r'^Python', text, re.MULTILINE)
print(f"使用 MULTILINE：{result2}")  # 输出：['Python', 'Python']（匹配两行）

# 匹配每行结尾
result3 = re.findall(r'Python$', text, re.M)
print(f"匹配行尾：{result3}")  # 输出：['Python', 'Python']
```

### 12.3 re.DOTALL（点号匹配换行）
<p align="right"><span style="background:#1e88e5;color:#fff;padding:2px 6px;border-radius:4px">💡 Could（可选实践）</span></p>

`re.DOTALL`（简写 `re.S`）标志使 `.` 匹配包括换行符在内的所有字符（默认情况下 `.` 不匹配换行符 `\n`）。

**示例代码**：

```python
import re

text = """开始
中间内容
结束"""

# 不使用 DOTALL：. 不匹配换行符
result1 = re.search(r'开始.+结束', text)
print(f"不使用 DOTALL：{result1}")  # 输出：None（无法跨行匹配）

# 使用 DOTALL：. 匹配包括换行符在内的所有字符
result2 = re.search(r'开始.+结束', text, re.DOTALL)
if result2:
    print(f"使用 DOTALL：{result2.group()}")  # 输出：开始\n中间内容\n结束

# 使用简写形式
result3 = re.search(r'开始.+结束', text, re.S)
if result3:
    print(f"使用简写：{result3.group()}")
```

### 12.4 组合使用多个标志
<p align="right"><span style="background:#1e88e5;color:#fff;padding:2px 6px;border-radius:4px">💡 Could（可选实践）</span></p>

可以使用 `|` 运算符组合多个标志（flags（标志）），实现同时使用多个标志。

**示例代码**：

```python
import re

text = """第一行：python
第二行：PYTHON
第三行：Python"""

# 组合使用多个标志：忽略大小写 + 多行模式
pattern = re.compile(r'^python$', re.IGNORECASE | re.MULTILINE)
result = pattern.findall(text)
print(f"组合标志：{result}")  # 输出：['python', 'PYTHON', 'Python']

# 三种方式组合：忽略大小写 + 多行 + 点号匹配换行
text2 = """开始
中间 Python 内容
结束"""
pattern2 = re.compile(r'开始.+Python.+结束', re.I | re.M | re.S)
result2 = pattern2.search(text2)
if result2:
    print(f"三标志组合：{result2.group()}")
```

**常用标志总结**：

| 标志 | 简写 | 说明 |
|------|------|------|
| `re.IGNORECASE` | `re.I` | 忽略大小写 |
| `re.MULTILINE` | `re.M` | 多行模式（`^` 和 `$` 匹配每行） |
| `re.DOTALL` | `re.S` | 点号匹配包括换行符在内的所有字符 |
| `re.VERBOSE` | `re.X` | 详细模式（允许在正则表达式中添加注释） |
| `re.ASCII` | `re.A` | 使 `\w`、`\W`、`\b`、`\B` 只匹配 ASCII 字符 |

---

## 13. 贪婪与非贪婪匹配（Greedy vs Non-greedy（贪婪与非贪婪匹配））
<p align="right"><span style="background:#fb8c00;color:#fff;padding:2px 6px;border-radius:4px">⭐ Should（建议实践）</span></p>

**贪婪匹配**（greedy matching（贪婪匹配））和非贪婪匹配（non-greedy matching（非贪婪匹配））是正则表达式中重要的匹配策略。

### 13.1 贪婪匹配

**贪婪匹配**是默认的匹配模式，会尽可能多地匹配字符。

**生活化比喻**：就像贪心的人，总是想要尽可能多的东西。

**示例代码**：

```python
import re

# 贪婪匹配：.* 会匹配尽可能多的字符
text = "<div>内容1</div><div>内容2</div>"
result = re.search(r'<div>.*</div>', text)
if result:
    print(f"贪婪匹配：{result.group()}")
    # 输出：<div>内容1</div><div>内容2</div>（匹配了整个字符串）

# 贪婪匹配数字
text2 = "数字：12345"
result2 = re.search(r'\d+', text2)
if result2:
    print(f"贪婪匹配数字：{result2.group()}")  # 输出：12345（匹配所有数字）
```

### 13.2 非贪婪匹配
<p align="right"><span style="background:#fb8c00;color:#fff;padding:2px 6px;border-radius:4px">⭐ Should（建议实践）</span></p>

**非贪婪匹配**（也称为惰性匹配（lazy matching（惰性匹配）））使用 `?` 后缀（如 `*?`、`+?`、`??`），会尽可能少地匹配字符。

**基本语法**：
- `*?`：非贪婪的 `*`（匹配 0 次或多次，尽可能少）
- `+?`：非贪婪的 `+`（匹配 1 次或多次，尽可能少）
- `??`：非贪婪的 `?`（匹配 0 次或 1 次，尽可能少）
- `{n,m}?`：非贪婪的 `{n,m}`（匹配 n 到 m 次，尽可能少）

**生活化比喻**：就像节俭的人，只要够用就行，不会贪多。

**示例代码**：

```python
import re

# 非贪婪匹配：.*? 会匹配尽可能少的字符
text = "<div>内容1</div><div>内容2</div>"
result = re.search(r'<div>.*?</div>', text)
if result:
    print(f"非贪婪匹配：{result.group()}")
    # 输出：<div>内容1</div>（只匹配第一个）

# 对比：贪婪 vs 非贪婪
text2 = "数字：12345"

# 贪婪匹配
result_greedy = re.search(r'\d+', text2)
if result_greedy:
    print(f"贪婪：{result_greedy.group()}")  # 输出：12345

# 非贪婪匹配（这里效果相同，因为只匹配一次）
result_non_greedy = re.search(r'\d+?', text2)
if result_non_greedy:
    print(f"非贪婪：{result_non_greedy.group()}")  # 输出：1（只匹配一个数字）

# 实际应用：提取所有标签内容
text3 = "<div>内容1</div><div>内容2</div><div>内容3</div>"
# 使用非贪婪匹配提取所有标签
results = re.findall(r'<div>(.*?)</div>', text3)
print(f"所有内容：{results}")  # 输出：['内容1', '内容2', '内容3']

# 贪婪匹配（错误示例）
results_greedy = re.findall(r'<div>(.*)</div>', text3)
print(f"贪婪匹配（错误）：{results_greedy}")  # 输出：['内容1</div><div>内容2</div><div>内容3']
```

**贪婪 vs 非贪婪对比**：

| 模式 | 类型 | 行为 | 示例 |
|------|------|------|------|
| `.*` | 贪婪 | 尽可能多匹配 | `"abc123"` → 匹配 `"abc123"` |
| `.*?` | 非贪婪 | 尽可能少匹配 | `"abc123"` → 匹配 `""`（空字符串） |
| `\d+` | 贪婪 | 尽可能多匹配数字 | `"123"` → 匹配 `"123"` |
| `\d+?` | 非贪婪 | 尽可能少匹配数字 | `"123"` → 匹配 `"1"` |

**选择建议**：
- ✅ **使用贪婪匹配**：当需要匹配尽可能多的内容时（如提取整个段落）
- ✅ **使用非贪婪匹配**：当需要匹配最短的内容时（如提取 HTML 标签内容，避免跨标签匹配）

---

## 14. 常见模式示例
<p align="right"><span style="background:#4caf50;color:#fff;padding:2px 6px;border-radius:4px">✅ Must（必做实践）</span></p>

### 14.1 匹配邮箱地址
<p align="right"><span style="background:#4caf50;color:#fff;padding:2px 6px;border-radius:4px">✅ Must（必做实践）</span></p>

**邮箱地址模式**：用于验证和提取邮箱地址。

**常用模式**：

```python
import re

# 基本邮箱模式
email_pattern = r'[\w.-]+@[\w.-]+\.\w+'

# 更严格的邮箱模式（推荐）
strict_email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'

# 示例
text = "联系 admin@example.com 或 support@test.org"
emails = re.findall(email_pattern, text)
print(f"找到的邮箱：{emails}")  # 输出：['admin@example.com', 'support@test.org']

# 验证邮箱格式
email = "user@example.com"
if re.match(strict_email_pattern, email):
    print("✅ 邮箱格式正确")
else:
    print("❌ 邮箱格式错误")
```

### 14.2 匹配电话号码
<p align="right"><span style="background:#4caf50;color:#fff;padding:2px 6px;border-radius:4px">✅ Must（必做实践）</span></p>

**电话号码模式**：用于匹配不同格式的电话号码。

**常用模式**：

```python
import re

# 中国手机号（11 位）
phone_pattern = r'1[3-9]\d{9}'

# 带分隔符的电话号码
phone_with_sep = r'1[3-9]\d[- ]?\d{4}[- ]?\d{4}'

# 示例
text = "电话：13800138000 或 139-0013-9000"
phones = re.findall(phone_pattern, text)
print(f"找到的电话：{phones}")  # 输出：['13800138000', '13900139000']

# 匹配带分隔符的电话
text2 = "电话：138-0013-8000 或 139 0014 9000"
phones2 = re.findall(phone_with_sep, text2)
print(f"找到的电话：{phones2}")  # 输出：['138-0013-8000', '139 0014 9000']
```

### 14.3 匹配日期
<p align="right"><span style="background:#4caf50;color:#fff;padding:2px 6px;border-radius:4px">✅ Must（必做实践）</span></p>

**日期模式**：用于匹配和提取日期信息。

**常用模式**：

```python
import re

# YYYY-MM-DD 格式
date_pattern = r'\d{4}-\d{2}-\d{2}'

# 带分组的日期模式（便于提取各部分）
date_with_groups = r'(\d{4})-(\d{2})-(\d{2})'

# 示例
text = "日期：2025-11-03 和 2025-12-25"
dates = re.findall(date_pattern, text)
print(f"找到的日期：{dates}")  # 输出：['2025-11-03', '2025-12-25']

# 提取日期各部分
dates_parts = re.findall(date_with_groups, text)
for year, month, day in dates_parts:
    print(f"年份：{year}，月份：{month}，日期：{day}")
```

### 14.4 匹配 URL
<p align="right"><span style="background:#fb8c00;color:#fff;padding:2px 6px;border-radius:4px">⭐ Should（建议实践）</span></p>

**URL 模式**：用于匹配和提取 URL 地址。

**常用模式**：

```python
import re

# 基本 URL 模式
url_pattern = r'https?://[\w.-]+(?:\.[\w.-]+)*(?:/[\w.-]*)*(?:\?[\w&=.-]*)?(?:#[\w.-]*)?'

# 更详细的 URL 模式（带分组）
detailed_url_pattern = r'(https?)://([\w.-]+(?:\.[\w.-]+)*)(/[\w.-]*)?'

# 示例
text = "访问 https://www.example.com/page 或 http://test.org"
urls = re.findall(url_pattern, text)
print(f"找到的 URL：{urls}")

# 提取 URL 各部分
matches = re.finditer(detailed_url_pattern, text)
for match in matches:
    protocol, domain, path = match.groups()
    print(f"协议：{protocol}，域名：{domain}，路径：{path or '/'}")
```

---

## 15. 正则表达式 vs 不使用正则表达式对比

通过对比展示正则表达式的优势和必要性。

**示例：提取电话号码**

```python
import re

text = "我的电话：138-0013-8000，备用：139 0014 9000"

# ❌ 不使用正则表达式（繁琐且容易出错）
def extract_phone_manual(text):
    """手动提取电话号码（不推荐）"""
    phones = []
    i = 0
    while i < len(text):
        if text[i].isdigit():
            phone = ""
            # 需要处理各种格式...
            # 代码复杂且容易出错
            pass
        i += 1
    return phones

# ✅ 使用正则表达式（简洁高效）
phones = re.findall(r'1[3-9]\d[- ]?\d{4}[- ]?\d{4}', text)
print(f"找到的电话：{phones}")  # 输出：['138-0013-8000', '139 0014 9000']
```

**示例：验证邮箱格式**

```python
import re

email = "user@example.com"

# ❌ 不使用正则表达式（代码冗长）
def validate_email_manual(email):
    """手动验证邮箱（不推荐）"""
    if '@' not in email:
        return False
    parts = email.split('@')
    if len(parts) != 2:
        return False
    username, domain = parts
    if '.' not in domain:
        return False
    # 需要检查更多规则...
    return True

# ✅ 使用正则表达式（简洁清晰）
email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
is_valid = re.match(email_pattern, email) is not None
print(f"邮箱格式：{'正确' if is_valid else '错误'}")
```

**对比总结**：

| 方面 | 不使用正则表达式 | 使用正则表达式 |
|------|----------------|---------------|
| 代码量 | 多（需要大量判断逻辑） | 少（一行模式即可） |
| 可读性 | 低（逻辑分散） | 高（模式清晰） |
| 维护性 | 低（修改困难） | 高（修改模式即可） |
| 性能 | 取决于实现 | 经过优化的 C 实现 |
| 适用场景 | 简单固定格式 | 复杂灵活模式 |

---

## 16. 常见错误与对比修正

### 错误 1：忘记使用原始字符串

**❌ 错误示例**：

```python
import re

# 错误：不使用原始字符串
pattern = "\d+"  # 反斜杠会被解释为转义字符
result = re.findall(pattern, "abc123")
# 可能产生错误或意外结果
```

**✅ 正确示例**：

```python
import re

# 正确：使用原始字符串
pattern = r"\d+"  # 使用 r"" 原始字符串
result = re.findall(pattern, "abc123")
print(result)  # 输出：['123']
```

### 错误 2：混淆 match() 和 search()

**❌ 错误示例**：

```python
import re

text = "hello world"
# 错误：使用 match() 查找中间的内容
result = re.match(r'world', text)
if result:
    print(result.group())
else:
    print("未找到")  # 输出：未找到（因为 match() 只匹配开头）
```

**✅ 正确示例**：

```python
import re

text = "hello world"
# 正确：使用 search() 查找任意位置
result = re.search(r'world', text)
if result:
    print(result.group())  # 输出：world
```

### 错误 3：贪婪匹配导致意外结果

**❌ 错误示例**：

```python
import re

text = "<div>内容1</div><div>内容2</div>"
# 错误：使用贪婪匹配，匹配了整个字符串
result = re.findall(r'<div>(.*)</div>', text)
print(result)  # 输出：['内容1</div><div>内容2']（错误！）
```

**✅ 正确示例**：

```python
import re

text = "<div>内容1</div><div>内容2</div>"
# 正确：使用非贪婪匹配
result = re.findall(r'<div>(.*?)</div>', text)
print(result)  # 输出：['内容1', '内容2']（正确！）
```

### 错误 4：分组返回结果混淆

**❌ 错误示例**：

```python
import re

text = "日期：2025-11-03"
# 错误：不理解分组返回结果
result = re.findall(r'(\d{4})-(\d{2})-(\d{2})', text)
print(result[0])  # 输出：('2025', '11', '03')（是元组，不是字符串）
# 如果期望字符串，会出错
```

**✅ 正确示例**：

```python
import re

text = "日期：2025-11-03"
# 方式一：不使用分组（返回完整匹配）
result1 = re.findall(r'\d{4}-\d{2}-\d{2}', text)
print(result1)  # 输出：['2025-11-03']

# 方式二：使用分组（返回分组元组）
result2 = re.findall(r'(\d{4})-(\d{2})-(\d{2})', text)
print(result2)  # 输出：[('2025', '11', '03')]
year, month, day = result2[0]  # 正确使用元组解包
```

---

## 17. 选择建议与实践流程

### 何时使用正则表达式

**✅ 适合使用正则表达式的场景**：
- 数据验证（邮箱、电话号码、身份证号等）
- 文本提取（从日志、HTML、文档中提取信息）
- 文本替换（格式化、脱敏处理等）
- 模式匹配（查找特定格式的内容）

**❌ 不适合使用正则表达式的场景**：
- 简单的字符串操作（如 `str.split()`, `str.replace()`）
- 解析复杂的结构化数据（如 JSON、XML，应使用专门的解析库）
- 需要语义理解的文本处理（如自然语言处理）

### 实践流程建议

1. **分析需求**：明确要匹配的模式和格式
2. **设计模式**：从简单开始，逐步完善正则表达式
3. **测试验证**：使用测试数据验证模式是否正确
4. **优化性能**：对于重复使用的模式，使用 `compile()` 编译
5. **代码审查**：确保模式清晰可读，必要时添加注释

---

## 18. 📚 参考资料与学习资源

### 官方文档

- [Python 官方文档 - re 模块](https://docs.python.org/3/library/re.html)
- [Python 正则表达式 HOWTO](https://docs.python.org/3/howto/regex.html)

### 在线工具

- [Regex101](https://regex101.com/) - 正则表达式在线测试和调试工具
- [Regexr](https://regexr.com/) - 交互式正则表达式学习和测试平台

### 学习资源

- [正则表达式 30 分钟入门教程](https://deerchao.cn/tutorials/regex/regex.htm) - 中文教程
- [Python 正则表达式教程 - 菜鸟教程](https://www.runoob.com/python/python-reg-expressions.html)

### 参考书籍

- 《精通正则表达式》（Mastering Regular Expressions）- Jeffrey Friedl 著

---

## 19. 总结

正则表达式（re 模块）是 Python 中强大的文本处理工具，掌握它能够显著提升文本处理的效率和灵活性。

**核心要点回顾**：

1. **基础方法**：`match()`、`search()`、`findall()`、`finditer()`、`sub()`、`split()`
2. **基础语法**：元字符、限定符、字符类、分组、原始字符串
3. **高级特性**：分组与捕获、标志使用、贪婪与非贪婪匹配
4. **最佳实践**：使用原始字符串、合理使用 `compile()`、理解匹配模式

**学习建议**：

- ✅ **多实践**：通过实际项目练习，加深理解
- ✅ **循序渐进**：从简单模式开始，逐步掌握复杂模式
- ✅ **善用工具**：使用在线工具测试和调试正则表达式
- ✅ **阅读文档**：遇到问题及时查阅官方文档

**鼓励与展望**：

正则表达式虽然初学有些复杂，但一旦掌握，就能在文本处理中游刃有余。无论是数据验证、日志分析还是文本清洗，正则表达式都能帮助你高效完成任务。相信通过不断的练习和实践，你一定能够熟练掌握这个强大的工具！

继续加油，你离成为文本处理高手又近了一步！🚀

---

**厦门工学院人工智能创作坊 -- 郑恩赐**  
**2025 年 11 月 03 日**

