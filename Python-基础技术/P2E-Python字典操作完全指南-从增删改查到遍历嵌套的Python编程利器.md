# P2E-Python字典操作完全指南-从增删改查到遍历嵌套的Python编程利器

## 📝 摘要

面向零基础，系统讲解 Python 字典（Dictionary）核心操作：增删改查、遍历、嵌套。通过生活化比喻与实战对比，掌握字典的高效操作方法，快速提升编程能力。

---

## 1. 前置知识点 📚

我们在深入学习 Python 字典之前，需要先了解以下基础概念：

- 📦 **变量（variable）**：用于存储数据的容器，就像生活中的 **盒子**，可以在里面存放不同的物品
- 🏷️ **数据类型（data type）**：Python 中的基本数据类型包括整数、浮点数、字符串等
- 🔑 **键值对（key-value pair）**：一种数据结构，由唯一的键（key）和对应的值（value）组成
- 🗂️ **哈希表（hash table）**：字典的底层数据结构，提供快速的查找性能

---

💡 **学习建议**：我们需要掌握了 Python 变量和基本数据类型后，就可以开始学习字典了。字典是 Python 最常用的数据结构之一，是后续学习 JSON、API 响应处理等内容的基础。

---

## 2. 什么是字典（Dictionary）📖

我们接下来要学习的字典（Dictionary）是 Python 中最核心的映射类型数据结构 📚，它以 **键值对（key-value pairs）** 的形式存储数据，提供高效的查找能力 ⚡。我们可以把它想象成生活中的 **通讯录** ——通过姓名（键）快速找到对应的电话号码（值），而不是像列表那样需要记住电话号码在第几位。

### 2.1 字典的核心特点 🔍

我们需要掌握字典的几个重要特点：

- 🔑 **键值对结构**：每个元素都是一个键值对，由唯一的键（key）和对应的值（value）组成
- 🎯 **通过键访问**：我们使用键来存取值，而不是通过位置索引（如列表的 0、1、2）
- 🔄 **可变性**：字典是可变的，我们可以随时添加、修改或删除键值对
- 📋 **无序性**：字典中的元素没有固定的顺序（Python 3.7+ 保持插入顺序，但逻辑上仍视为无序）
- 🚫 **键的唯一性**：字典中的键必须是唯一的，不能重复
- 🔐 **键的可哈希性**：作为字典的键，必须是可哈希（hashable）的类型

### 2.1.1 什么是可哈希（Hashable）🤔

我们在使用字典时，需要注意一个重要概念：**可哈希（hashable）**。可哈希是指一个对象在它的生命周期内，哈希值（hash value）是固定的。Python 使用哈希值来快速查找字典中的键，所以我们需要使用可哈希的对象作为字典的键。

#### 2.1.1.1 可哈希的类型（可以作为字典的键）✅

我们需要知道，以下类型是可以作为字典的键的：

| 类型 | 说明 | 示例 |
|------|------|------|
| **整数（int）** | 数字类型都是可哈希的 | `1`, `100`, `-5` |
| **浮点数（float）** | 浮点数也是可哈希的 | `3.14`, `2.5` |
| **字符串（str）** | 字符串是不可变的，所以可哈希 | `"name"`, `"key1"` |
| **布尔值（bool）** | True 和 False 都是可哈希的 | `True`, `False` |
| **元组（tuple）** | 元组是不可变的，但要求其中的元素也必须可哈希（原因见下文） | `(1, 2)`, `("a", "b")` ✅ |
| **frozenset** | 冻结集合，不可变的集合 | `frozenset([1, 2, 3])` |

#### 2.1.1.2 为什么元组内的元素也必须是可哈希的？❓

虽然元组本身是不可变的，但 Python 在计算元组的哈希值时，会递归地计算元组内所有元素的哈希值。如果元组内包含不可哈希的元素（比如列表），Python 就无法计算整个元组的哈希值，因此这个元组就不能作为字典的键。我们需要注意这一点。

**举个例子**：

```python
# ✅ 合法：元组内所有元素都是可哈希的
locations = {
    (35.68, 139.69): "东京",  # 元组内是两个浮点数
    (40.71, -74.01): "纽约"   # 元组内是两个浮点数
}

# ❌ 非法：元组内包含列表（不可哈希）
locations = {
    ([35.68, 139.69]): "东京"  # TypeError: unhashable type: 'list'
}
```

**原理**：字典使用哈希表来存储键值对，当添加一个键时，Python 会先计算这个键的哈希值，然后根据哈希值确定存储位置。如果键本身或它的任何组成部分是可变的，哈希值就可能改变，这会导致字典无法正确找到对应的值。

### 2.1.1.3 不可哈希的类型（不能作为字典的键）❌

我们需要避免使用以下类型作为字典的键：

| 类型 | 原因 | 示例 |
|------|------|------|
| **列表（list）** | 列表是可变的，内容可能改变 | `[1, 2, 3]` ❌ |
| **字典（dict）** | 字典是可变的 | `{"a": 1}` ❌ |
| **集合（set）** | 集合是可变的 | `{1, 2, 3}` ❌ |
| **包含可变元素的元组** | 元组中包含不可哈希的元素 | `(1, [2, 3])` ❌ |

### 2.1.1.4 如何判断对象是否可哈希 🔬

我们在实际使用中，可以通过以下方法判断对象是否可哈希：

```python
# 方法1：使用 hash() 函数
print(hash("hello"))  # ✅ 可以，输出哈希值
print(hash([1, 2, 3]))  # ❌ TypeError: unhashable type: 'list'

# 方法2：使用 isinstance() 检查
from collections.abc import Hashable
print(isinstance("hello", Hashable))  # ✅ True
print(isinstance([1, 2, 3], Hashable))  # ❌ False
```

### 2.1.2 字典 vs 列表对比 ⚖️

我们在选择数据结构时，需要了解字典和列表的区别：

| 特性 | 字典（dict） | 列表（list） |
|------|-------------|-------------|
| 数据结构 | 键值对（key-value） | 有序序列 |
| 访问方式 | 通过键访问 | 通过索引访问 |
| 有序性 | 无序（Python 3.7+保持插入顺序） | 有序 |
| 查找性能 | O(1) 常量时间 | O(n) 线性时间 |
| 适用场景 | 快速查找、映射关系 | 顺序存储、遍历 |

### 2.1.3 实际应用场景 💡

我们在实际开发中经常会用到字典，以下是常见的应用场景：

- **快速查询**：字典提供 O(1) 的平均时间复杂度进行查找操作，比列表的 O(n) 快得多。比如查字典、查用户信息、查配置项等
- **用户信息存储**：用用户名作为键，存储用户的年龄、邮箱等信息
- **配置项管理**：用配置名称作为键，存储对应的配置值
- **计数统计**：统计单词出现次数、商品销量等
- **JSON 数据处理**：JSON 对象在 Python 中就是字典类型

---

💡 **学习建议**：我们需要掌握字典是 Python 最常用的数据结构之一，它能让我们的代码更高效、更易读。接下来我们将学习如何创建字典。

## 3. 字典创建（dict creation）✍️

我们在前面了解了字典的概念，现在来学习如何创建字典。字典可以通过多种方式创建，选择合适的方法能让代码更简洁、更高效。本章我们将学习三种主要的创建方式。

### 3.1 基本创建方式 🛠️

#### 3.1.1 使用花括号 `{}` 创建 🅰️

使用花括号 `{}` 是创建字典最直接、最常用的方式。在花括号内，使用冒号 `:` 分隔键和值，多个键值对之间用逗号 `,` 分隔。

```python
# 创建空字典
empty_dict = {}

# 创建带初始值的字典
student = {
    "name": "张三",
    "age": 18,
    "score": 95
}
print(student)  # 输出: {'name': '张三', 'age': 18, 'score': 95}
```

**特点**：
- 语法简洁直观
- 适合创建时已知所有键值对的场景
- 花括号是字典的标志性符号，一眼就能识别

#### 3.1.2 使用 dict() 构造函数创建 🅱️

`dict()` 是 Python 的内置构造函数，提供了另一种创建字典的方式。

```python
# 创建空字典
empty_dict = dict()

# 使用关键字参数创建
student = dict(name="李四", age=20, score=88)
print(student)  # 输出: {'name': '李四', 'age': 20, 'score': 88}

# 从键值对序列创建
pairs = [("name", "王五"), ("age", 22), ("score", 92)]
student = dict(pairs)
print(student)  # 输出: {'name': '王五', 'age': 22, 'score': 92}

# 从另一个字典创建
original = {"a": 1, "b": 2}
copy_dict = dict(original)
print(copy_dict)  # 输出: {'a': 1, 'b': 2}
```

**特点**：
- 适合从其他数据结构（如列表、元组）转换而来
- 使用关键字参数时，键必须是字符串
- 可以从现有的字典复制创建新字典

#### 3.1.3 使用 fromkeys() 方法创建 🔄

`fromkeys()` 是 `dict` 类的类方法，用于创建一个新字典，将所有键设置为相同的默认值。

```python
# 创建所有键值都为 None 的字典
keys = ["name", "age", "score"]
student = dict.fromkeys(keys)
print(student)  # 输出: {'name': None, 'age': None, 'score': None}

# 创建所有键值都为指定默认值的字典
student = dict.fromkeys(keys, 0)
print(student)  # 输出: {'name': 0, 'age': 0, 'score': 0}
```

**特点**：
- 适合需要初始化多个键为相同默认值的场景
- 如果不指定默认值，默认为 `None`
- 所有键共享同一个默认值对象（注意可变对象的引用问题）

#### 3.1.4 字典创建方式对比 📊

| 创建方式 | 适用场景 | 优点 | 缺点 |
|---------|---------|------|------|
| `{}` | 已知所有键值对 | 语法简洁、性能好 | 键必须是字面量 |
| `dict()` | 从其他数据结构转换 | 灵活、可读性好 | 语法稍复杂 |
| `fromkeys()` | 初始化多个键为相同值 | 简洁高效 | 所有键值相同 |

### 3.2 字典推导式创建 🦾

字典推导式（Dictionary Comprehension）是 Python 中一种简洁高效的语法结构，用于通过表达式快速生成字典 🦾。它将"遍历、计算与构造"浓缩成一行表达式，是 Pythonic 代码的代表写法之一。

#### 3.2.1 基本语法 📝

字典推导式的基本语法如下：

```python
{key: value for item in iterable}
```

- `key`：生成字典的键
- `value`：生成字典的值
- `item`：遍历的元素
- `iterable`：可迭代对象

#### 3.2.2 基础示例 💡

```python
# 示例1：从列表创建字典（键为数，值为数的平方）
squares = {x: x**2 for x in range(5)}
print(squares)  # 输出: {0: 0, 1: 1, 2: 4, 3: 9, 4: 16}

# 示例2：将两个列表组合成字典
keys = ["name", "age", "city"]
values = ["张三", 25, "北京"]
person = dict(zip(keys, values))
print(person)  # 输出: {'name': '张三', 'age': 25, 'city': '北京'}

# 示例3：将字符串转换为字符计数字典
word = "hello"
char_count = {char: word.count(char) for char in word}
print(char_count)  # 输出: {'h': 1, 'e': 1, 'l': 2, 'o': 1}
```

#### 3.2.3 带条件的字典推导式 🔣

可以在推导式中添加条件来过滤元素：

```python
# 示例1：只保留偶数的平方
even_squares = {x: x**2 for x in range(10) if x % 2 == 0}
print(even_squares)  # 输出: {0: 0, 2: 4, 4: 16, 6: 36, 8: 64}

# 示例2：根据条件转换数据
scores = {"语文": 85, "数学": 92, "英语": 78, "物理": 90}
pass_scores = {subject: score for subject, score in scores.items() if score >= 80}
print(pass_scores)  # 输出: {'语文': 85, '数学': 92, '物理': 90}
```

#### 3.2.4 复杂的字典推导式 🧩

```python
# 示例1：嵌套循环创建字典
pairs = {(x, y): x + y for x in range(3) for y in range(3)}
print(pairs)  # 输出: {(0, 0): 0, (0, 1): 1, (0, 2): 2, (1, 0): 1, ...}

# 示例2：使用条件表达式（三元运算符）
numbers = [1, 2, 3, 4, 5]
label = {n: "偶数" if n % 2 == 0 else "奇数" for n in numbers}
print(label)  # 输出: {1: '奇数', 2: '偶数', 3: '奇数', 4: '偶数', 5: '奇数'}

# 示例3：从字典推导新字典
original = {"a": 1, "b": 2, "c": 3}
doubled = {k: v * 2 for k, v in original.items()}
print(doubled)  # 输出: {'a': 2, 'b': 4, 'c': 6}
```

#### 3.2.5 字典推导式 vs 传统循环对比 ⚖️

| 写法 | 示例 | 优点 |
|-----|------|------|
| 字典推导式 | `{x: x**2 for x in range(5)}` | 简洁、可读性好、性能好 |
| 传统循环 | `squares = {}` + `for x in range(5):` + `    squares[x] = x**2` | 易于理解、适合复杂逻辑 |

---

💡 **学习建议**：字典推导式是 Python 的特色语法，建议熟练掌握。它的语法和列表推导式类似，学会一个就能轻松上手另一个。如果你想系统学习推导式（包括列表推导式、集合推导式），可以查阅 [P5D-Python_推导式完全指南](https://juejin.cn/post/7563597691680489491)。

## 4. 字典查询（finding elements）🔍

我们在前面学习了如何创建字典，现在来学习如何查询字典中的数据。字典的查询操作是使用字典的核心目的。字典之所以高效，正是因为它可以通过键快速找到对应的值，而不需要像列表那样遍历查找。本章我们将学习字典的几种查询方式。

### 4.1 通过键获取值 🔑

最直接的查询方式是使用方括号 `[]` 加键名来获取对应的值。

```python
# 创建字典
student = {"name": "张三", "age": 18, "score": 95}

# 通过键获取值
print(student["name"])  # 输出: 张三
print(student["age"])   # 输出: 18
print(student["score"])  # 输出: 95
```

**⚠️ 注意**：如果键不存在，使用 `[]` 会抛出 `KeyError` 异常。

```python
# 键不存在时，会报错
print(student["gender"])  # ❌ KeyError: 'gender'
```

### 4.2 get() 方法 🛡️

为了避免 `KeyError` 异常，字典提供了 `get()` 方法。当键不存在时，它会返回 `None`（或者指定的默认值），而不是抛出异常。

```python
student = {"name": "张三", "age": 18, "score": 95}

# 使用 get() 方法获取值
print(student.get("name"))    # 输出: 张三
print(student.get("gender"))  # 输出: None（键不存在）

# 指定默认值
print(student.get("gender", "未知"))  # 输出: 未知
```

**`get()` 方法的特点**：
- 如果键存在，返回对应的值
- 如果键不存在，返回 `None`（或指定的默认值）
- 不会抛出异常，代码更安全

**使用场景建议**：
- 不确定键是否存在时，使用 `get()` 方法
- 需要设置默认值时，使用 `get(key, default)`

### 4.3 keys()、values()、items() 方法 📋

这三个方法用于获取字典的不同视图（view），方便遍历和操作字典。

```python
student = {"name": "张三", "age": 18, "score": 95}

# keys()：获取所有键
print(student.keys())   # 输出: dict_keys(['name', 'age', 'score'])

# values()：获取所有值
print(student.values()) # 输出: dict_values(['张三', 18, 95])

# items()：获取所有键值对
print(student.items())  # 输出: dict_items([('name', '张三'), ('age', 18), ('score', 95)])
```

**遍历示例**：

```python
# 遍历所有键
for key in student.keys():
    print(key)

# 遍历所有值
for value in student.values():
    print(value)

# 遍历所有键值对
for key, value in student.items():
    print(f"{key}: {value}")
```

**特点说明**：
- 返回的是**视图对象**，不是列表
- 视图是动态的：字典改变，视图也会跟着变
- 如果需要列表，可以手动转换：`list(student.keys())`

### 4.4 in 和 not in 运算符 ✅

在 Python 中，可以使用 `in` 和 `not in` 运算符来检查键是否存在于字典中。这是 Python 官方推荐的检测方式，时间复杂度为 O(1)。

```python
student = {"name": "张三", "age": 18, "score": 95}

# 检查键是否存在
print("name" in student)     # 输出: True
print("gender" in student)   # 输出: False

# 检查键是否不存在
print("gender" not in student)  # 输出: True
```

**实际应用**：

```python
# 场景1：先检查再获取（避免 KeyError）
if "gender" in student:
    print(student["gender"])
else:
    print("性别未知")

# 场景2：条件判断
if "score" in student and student["score"] >= 60:
    print("考试及格")
else:
    print("需要补考")
```

**`in` vs `get()` 对比**：

| 方法 | 适用场景 | 返回值 |
|------|---------|--------|
| `in` | 只检查键是否存在 | 布尔值 |
| `get()` | 检查并获取值 | 值或默认值 |

---

💡 **学习建议**：在实际开发中，如果只是检查键是否存在，用 `in`；如果需要获取值，用 `get()` 更安全。

## 5. 字典增加（adding elements）➕

我们在前面学习了如何查询字典，现在来学习如何向字典中添加新元素。

### 5.1 直接赋值添加 ✍️

向字典中添加元素最简单的方式是直接通过键赋值。如果键不存在，就会添加新的键值对；如果键已存在，则会更新值。

```python
# 创建空字典
student = {}

# 添加单个键值对
student["name"] = "张三"
student["age"] = 18
student["score"] = 95

print(student)  # 输出: {'name': '张三', 'age': 18, 'score': 95}

# 多次赋值可以继续添加
student["city"] = "北京"
print(student)  # 输出: {'name': '张三', 'age': 18, 'score': 95, 'city': '北京'}
```

**⚠️ 注意**：如果键已存在，直接赋值会**覆盖**原来的值（这属于修改操作，见第6章）。

**特点**：
- 语法简洁，一目了然
- 适合逐个添加键值对
- 键不存在则添加，键存在则覆盖

### 5.2 setdefault() 方法 🔐

`setdefault()` 方法用于设置字典的默认值。如果键不存在，它会添加键并设置默认值；如果键已存在，则保持原有值不变。

```python
student = {"name": "张三", "age": 18}

# 键不存在，添加新键值对
result = student.setdefault("score", 95)
print(result)        # 输出: 95（返回设置的值）
print(student)       # 输出: {'name': '张三', 'age': 18, 'score': 95}

# 键已存在，不改变原有值
result = student.setdefault("name", "李四")
print(result)        # 输出: 张三（返回原有值）
print(student)       # 输出: {'name': '张三', 'age': 18, 'score': 95}（name 未被修改）

# 只传一个参数时，默认值为 None
student.setdefault("address")
print(student)       # 输出: {'name': '张三', 'age': 18, 'score': 95, 'address': None}
```

**`setdefault()` 的特点**：
- 如果键不存在，添加键并设置默认值
- 如果键已存在，返回原有值，**不修改**字典
- 适合用于初始化字典，确保某个键有默认值

**实际应用场景**：

```python
# 场景1：统计水果出现次数
fruits = ["苹果", "香蕉", "苹果", "橙子", "香蕉", "苹果"]
count = {}

for fruit in fruits:
    count.setdefault(fruit, 0)  # 如果键不存在，初始化为 0
    count[fruit] += 1          # 然后加 1

print(count)  # 输出: {'苹果': 3, '香蕉': 2, '橙子': 1}

# 场景2：分组数据
students = [
    {"name": "张三", "class": "A"},
    {"name": "李四", "class": "B"},
    {"name": "王五", "class": "A"}
]

groups = {}
for student in students:
    cls = student["class"]
    groups.setdefault(cls, []).append(student["name"])

print(groups)  # 输出: {'A': ['张三', '王五'], 'B': ['李四']}
```

### 5.3 update() 方法 🔁

`update()` 方法用于将另一个字典或键值对序列合并到当前字典中。它可以一次性添加多个键值对，非常适合批量更新字典。

```python
student = {"name": "张三", "age": 18}

# 使用字典更新
student.update({"score": 95, "city": "北京"})
print(student)  # 输出: {'name': '张三', 'age': 18, 'score': 95, 'city': '北京'}

# 使用关键字参数更新
student.update(grade="A", status="active")
print(student)  # 输出: {'name': '张三', 'age': 18, 'score': 95, 'city': '北京', 'grade': 'A', 'status': 'active'}

# 使用键值对序列更新（列表、元组均可）
pairs = [("gender", "男"), ("height", 175)]
student.update(pairs)
print(student)  # 输出: {'name': '张三', 'age': 18, 'score': 95, 'city': '北京', 'grade': 'A', 'status': 'active', 'gender': '男', 'height': 175}

# update() 也会覆盖已存在的键
student.update({"age": 20, "name": "李四"})
print(student)  # 输出: {'name': '李四', 'age': 20, 'score': 95, ...}
```

**`update()` 的特点**：
- 可以一次性添加或更新多个键值对
- 如果键已存在，会覆盖原有的值
- 支持多种参数形式：字典、关键字参数、键值对序列

**对比总结**：

| 方法 | 适用场景 | 键存在时的行为 |
|------|---------|---------------|
| `dict[key] = value` | 添加或修改单个键值对 | 覆盖原有值 |
| `setdefault(key, value)` | 确保键有默认值 | 不改变原有值 |
| `update({...})` | 批量添加或修改 | 覆盖原有值 |

## 6. 字典修改（modifying elements）✏️

我们在前面学习了如何添加元素，现在来学习如何修改字典中已有的值。

### 6.1 通过键修改值 🖊️

字典的值可以通过键直接修改。直接赋值时，如果键存在，则更新值；如果键不存在，则添加新键值对（在第五章中我们学过，键不存在时就是添加）。

```python
student = {"name": "张三", "age": 18, "score": 95}

# 修改已存在的键的值
student["age"] = 20
student["score"] = 88

print(student)  # 输出: {'name': '张三', 'age': 20, 'score': 88}
```

**⚠️ 注意**：这里的"修改"和"添加"使用的是同样的语法，区别在于键是否存在：
- 键不存在 → 添加新键值对
- 键已存在 → 修改原有值

**修改嵌套字典中的值**：

```python
# 嵌套字典
user = {
    "name": "张三",
    "profile": {
        "email": "zhangsan@example.com",
        "age": 18
    }
}

# 修改嵌套字典中的值
user["profile"]["age"] = 20
user["profile"]["email"] = "new_email@example.com"

print(user)
# 输出: {'name': '张三', 'profile': {'email': 'new_email@example.com', 'age': 20}}
```

### 6.2 update() 方法修改 🔁

`update()` 方法不仅可以添加元素（第五章学过），还可以用来修改元素。当提供的键在字典中已存在时，就会覆盖原来的值。

```python
student = {"name": "张三", "age": 18, "score": 95}

# 使用字典修改多个值
student.update({"age": 20, "score": 88})

print(student)  # 输出: {'name': '张三', 'age': 20, 'score': 88}

# 使用关键字参数修改
student.update(age=22, status="graduated")

print(student)  # 输出: {'name': '张三', 'age': 22, 'score': 88, 'status': 'graduated'}
```

**对比总结**：

| 方法 | 适用场景 | 键不存在时的行为 |
|------|---------|---------------|
| `dict[key] = value` | 修改单个值 | 添加新键值对 |
| `update({key: value})` | 批量修改多个值 | 添加新键值对 |

---

💡 **学习建议**：字典的"增"和"改"使用相同的语法（直接赋值或 update），区别在于键是否已存在。理解这一点，就掌握了字典操作的核心逻辑。

## 7. 字典删除（removing elements）🗑️

我们在前面学习了如何添加和修改字典，现在来学习如何删除字典中的元素。

### 7.1 pop() 方法 🏷️

`pop()` 方法用于删除指定键的键值对，并返回对应的值。如果键不存在，会抛出 `KeyError` 异常。

```python
student = {"name": "张三", "age": 18, "score": 95}

# 删除键值对，并获取被删除的值
removed_value = student.pop("age")
print(removed_value)  # 输出: 18
print(student)       # 输出: {'name': '张三', 'score': 95}

# 键不存在时，会抛出 KeyError
# student.pop("gender")  # ❌ KeyError: 'gender'

# 可以设置默认值，避免异常
removed_value = student.pop("gender", None)
print(removed_value)  # 输出: None（键不存在，返回默认值）
```

**`pop()` 的特点**：
- 删除指定键的键值对
- 返回被删除的值
- 键不存在时抛出异常（可以设置默认值避免）

**使用场景**：当你需要删除某个键值对，同时可能需要用到被删除的值时，使用 `pop()` 最合适。

### 7.2 popitem() 方法 📦

`popitem()` 方法用于删除字典中最后一个键值对（Python 3.7+），并以元组形式返回删除的键和值。在 Python 3.7 之前，字典是无序的，删除的是任意键值对。

```python
student = {"name": "张三", "age": 18, "score": 95}

# 删除最后一个键值对
removed = student.popitem()
print(removed)   # 输出: ('score', 95)（返回键值对元组）
print(student)   # 输出: {'name': '张三', 'age': 18}

# 继续删除
removed = student.popitem()
print(removed)   # 输出: ('age', 18)
print(student)   # 输出: {'name': '张三'}

# 字典为空时，抛出 KeyError
# student.popitem()  # ❌ KeyError: 'popitem(): dictionary is empty'
```

**`popitem()` 的特点**：
- 删除并返回最后一个键值对（以元组形式）
- Python 3.7+ 保证删除顺序与插入顺序一致
- 字典为空时抛出 `KeyError`

**使用场景**：
- 想要按插入顺序删除键值对时
- 实现 LRU 缓存（最近最少使用）等数据结构时

### 7.3 del 语句 ❌

`del` 语句用于删除字典中指定键的键值对，或者删除整个字典。

```python
student = {"name": "张三", "age": 18, "score": 95}

# 删除指定的键值对
del student["age"]
print(student)  # 输出: {'name': '张三', 'score': 95}

# 删除不存在的键会抛出异常
# del student["gender"]  # ❌ KeyError: 'gender'

# 删除整个字典
del student
# print(student)  # ❌ NameError: name 'student' is not defined
```

**`del` 的特点**：
- 删除指定键的键值对
- 可以删除整个字典
- 键不存在时抛出 `KeyError`

**使用场景**：
- 明确知道要删除某个键值对
- 需要完全删除字典变量时

### 7.4 clear() 方法 💣

`clear()` 方法用于清空字典中的所有键值对，使字典变为空字典。与 `del` 不同的是，`clear()` 只删除字典中的内容，字典变量本身仍然存在。

```python
student = {"name": "张三", "age": 18, "score": 95}

# 清空字典
student.clear()
print(student)  # 输出: {}（空字典）
print(len(student))  # 输出: 0

# 字典变量仍然存在，可以继续使用
student["name"] = "李四"
print(student)  # 输出: {'name': '李四'}
```

**`clear()` 的特点**：
- 删除字典中所有键值对
- 字典变为空字典 `{}`
- 字典变量本身仍然存在

**对比总结**：

| 方法/语句 | 删除内容 | 返回值 | 键不存在时 |
|----------|---------|-------|----------|
| `pop(key)` | 指定键的键值对 | 返回被删除的值 | 抛出 KeyError |
| `popitem()` | 最后一个键值对 | 返回键值对元组 | 抛出 KeyError |
| `del dict[key]` | 指定键的键值对 | 无返回值 | 抛出 KeyError |
| `clear()` | 所有键值对 | 无返回值 | 不报错 |

---

💡 **学习建议**：删除操作要小心，特别是 `del` 语句会直接删除变量。如果不确定键是否存在，我们可以使用 `pop(key, default)` 设置默认值，避免异常。

## 8. 字典遍历（traversing）🚶

我们在前面学习了字典的增删改查操作，现在来学习如何遍历字典中的所有数据。

### 8.1 遍历键 🔑

遍历字典的键是最常见的操作之一。可以直接遍历字典（默认遍历的就是键），也可以使用 `keys()` 方法明确指定遍历键。

```python
student = {"name": "张三", "age": 18, "score": 95, "city": "北京"}

# 方法1：直接遍历字典（默认遍历键）
for key in student:
    print(key)
# 输出:
# name
# age
# score
# city

# 方法2：使用 keys() 方法
for key in student.keys():
    print(key)
# 输出同上

# 在需要明确语义时，使用 keys() 更清晰
print("学生信息包含以下字段：")
for key in student.keys():
    print(f"  - {key}")
```

**使用场景**：
- 只关心有哪些键（字段名）
- 需要判断某个键是否存在（结合 `in` 运算符）

### 8.2 遍历值 📊

如果只关心字典中的值，可以使用 `values()` 方法进行遍历。

```python
student = {"name": "张三", "age": 18, "score": 95, "city": "北京"}

# 遍历所有值
for value in student.values():
    print(value)
# 输出:
# 张三
# 18
# 95
# 北京

# 实际应用：计算平均分
scores = {"语文": 85, "数学": 92, "英语": 78, "物理": 90}
total = sum(scores.values())
count = len(scores)
average = total / count
print(f"平均分: {average}")  # 输出: 平均分: 86.25

# 找出最高分
max_score = max(scores.values())
print(f"最高分: {max_score}")  # 输出: 最高分: 92
```

**使用场景**：
- 只关心值，不需要键
- 统计、计算类操作（如求和、平均值、最大值、最小值）

### 8.3 遍历键值对 🔂

如果需要同时获取键和值，可以使用 `items()` 方法，它返回键值对元组。

```python
student = {"name": "张三", "age": 18, "score": 95, "city": "北京"}

# 遍历所有键值对
for key, value in student.items():
    print(f"{key}: {value}")
# 输出:
# name: 张三
# age: 18
# score: 95
# city: 北京

# 实际应用：筛选符合条件的数据
scores = {"语文": 85, "数学": 92, "英语": 78, "物理": 90}
print("及格的科目：")
for subject, score in scores.items():
    if score >= 80:
        print(f"  {subject}: {score}分")
# 输出:
# 及格的科目：
#   语文: 85分
#   数学: 92分
#   物理: 90分

# 实际应用：构建新字典
original = {"a": 1, "b": 2, "c": 3}
doubled = {}
for key, value in original.items():
    doubled[key] = value * 2
print(doubled)  # 输出: {'a': 2, 'b': 4, 'c': 6}
```

**使用场景**：
- 需要同时使用键和值
- 复杂的数据转换和筛选

### 8.4 字典推导式遍历 🦾

字典推导式不仅可以创建字典（第三章学过），还可以用于遍历和转换数据。它的语法简洁，效率也更高。

```python
# 示例1：遍历键值对并筛选
scores = {"语文": 85, "数学": 92, "英语": 78, "物理": 90}
pass_scores = {subject: score for subject, score in scores.items() if score >= 80}
print(pass_scores)  # 输出: {'语文': 85, '数学': 92, '物理': 90}

# 示例2：遍历键值对并转换
student = {"name": "张三", "age": 18, "score": 95}
formatted = {f"学生{k}": f"值{v}" for k, v in student.items()}
print(formatted)  # 输出: {'学生name': '值张三', '学生age': '值18', '学生score': '值95'}

# 示例3：键值互换
original = {"a": 1, "b": 2, "c": 3}
reversed_dict = {v: k for k, v in original.items()}
print(reversed_dict)  # 输出: {1: 'a', 2: 'b', 3: 'c'}

# 示例4：合并两个字典（键不同时）
dict1 = {"a": 1, "b": 2}
dict2 = {"c": 3, "d": 4}
merged = {k: v for d in [dict1, dict2] for k, v in d.items()}
print(merged)  # 输出: {'a': 1, 'b': 2, 'c': 3, 'd': 4}
```

**对比总结**：

| 遍历方式 | 适用场景 | 示例 |
|---------|---------|------|
| `for key in dict` | 只遍历键 | 遍历字段名 |
| `for key in dict.keys()` | 明确遍历键 | 需要键的列表 |
| `for value in dict.values()` | 只遍历值 | 统计计算 |
| `for k, v in dict.items()` | 同时遍历键值 | 数据筛选转换 |
| 字典推导式 | 简洁的转换筛选 | 一行代码完成转换 |

## 9. 字典嵌套（nested dict）🏗️

### 9.1 什么是嵌套字典 🏗️

我们在前面学习了普通字典，它的特点是一个键对应一个值。但在实际开发中，我们经常会遇到更复杂的数据——一个键对应多个值，或者数据本身有层级关系。这就是我们接下来要学习的嵌套字典。

嵌套字典是指字典中的值本身也是一个字典。换句话说，就是字典里面嵌套字典，形成多层次的数据结构。它可以以层次结构的方式组织和存储数据，非常适合表示复杂的关系型数据。

```python
# 简单字典（键对应单个值）
student = {"name": "张三", "age": 18}

# 嵌套字典（键对应一个字典）
student = {
    "name": "张三",
    "profile": {
        "age": 18,
        "city": "北京",
        "email": "zhangsan@example.com"
    },
    "scores": {
        "语文": 85,
        "数学": 92,
        "英语": 78
    }
}
```

**嵌套字典的结构**：

```
外层字典
├── name: "张三"
├── profile: 内层字典1
│   ├── age: 18
│   ├── city: "北京"
│   └── email: "zhangsan@example.com"
└── scores: 内层字典2
    ├── 语文: 85
    ├── 数学: 92
    └── 英语: 78
```

**常见的嵌套场景**：
- 多个学生的信息：每个学生是一个字典，所有学生组成一个大字典
- JSON 数据：JSON 对象本身就是嵌套字典
- 配置信息：多级分类的配置项

### 9.2 嵌套字典的增删改查 🔧

嵌套字典的操作与普通字典类似，但需要指定多层键。

```python
# 创建嵌套字典
company = {
    "部门A": {"员工数": 10, "预算": 50000},
    "部门B": {"员工数": 15, "预算": 80000}
}

# 查：访问嵌套字典中的值
print(company["部门A"])              # 输出: {'员工数': 10, '预算': 50000}
print(company["部门A"]["员工数"])     # 输出: 10

# 增：添加新的嵌套字典
company["部门C"] = {"员工数": 8, "预算": 30000}
print(company)
# 输出: {'部门A': {...}, '部门B': {...}, '部门C': {...}}

# 改：修改嵌套字典中的值
company["部门A"]["预算"] = 60000
print(company["部门A"])  # 输出: {'员工数': 10, '预算': 60000}

# 增：在嵌套字典中添加新键值对
company["部门A"]["负责人"] = "张三"
print(company["部门A"])  # 输出: {'员工数': 10, '预算': 60000, '负责人': '张三'}

# 删：删除嵌套字典中的键值对
del company["部门B"]["员工数"]
print(company["部门B"])  # 输出: {'预算': 80000}

# 使用 pop() 删除并获取值
removed = company["部门C"].pop("预算")
print(removed)    # 输出: 30000
print(company["部门C"])  # 输出: {'员工数': 8}
```

**⚠️ 注意**：访问嵌套字典时，如果中间层的键不存在，会抛出 `KeyError`。可以使用 `get()` 方法安全访问：

```python
# 安全访问嵌套字典
print(company.get("部门D", {}))           # 输出: {}（键不存在返回默认值）
print(company.get("部门A", {}).get("预算"))  # 输出: 60000

# 链式调用需要注意：任何一个 get() 返回默认值都会继续调用
print(company.get("部门D", {}).get("预算"))  # 输出: None（不会报错）
```

### 9.3 嵌套字典的遍历 🚶

遍历嵌套字典需要使用嵌套循环，或者通过递归处理。

```python
# 嵌套字典
company = {
    "部门A": {"员工数": 10, "预算": 50000},
    "部门B": {"员工数": 15, "预算": 80000}
}

# 遍历外层字典的所有键值对
print("=== 遍历所有部门及其信息 ===")
for dept, info in company.items():
    print(f"部门: {dept}")
    for key, value in info.items():
        print(f"  {key}: {value}")
# 输出:
# 部门: 部门A
#   员工数: 10
#   预算: 50000
# 部门: 部门B
#   员工数: 15
#   预算: 80000

# 遍历所有值（嵌套字典的值）
print("\n=== 遍历所有详细信息 ===")
for dept, info in company.items():
    for value in info.values():
        print(value)
# 输出: 10, 50000, 15, 80000

# 使用字典推导式创建新嵌套字典
doubled = {dept: {k: v * 2 for k, v in info.items()} for dept, info in company.items()}
print(doubled)
# 输出: {'部门A': {'员工数': 20, '预算': 100000}, '部门B': {'员工数': 30, '预算': 160000}}

# 统计所有部门的总预算
total_budget = sum(info["预算"] for info in company.values())
print(f"总预算: {total_budget}")  # 输出: 总预算: 130000

# 找出员工数最多的部门
# company.items() 返回键值对元组：(键, 值) = (部门名称, {'员工数': 10, '预算': 50000})
# x[0] 是部门名称（键），x[1] 是员工数和预算（值，是一个字典）
max_staff_dept = max(company.items(), key=lambda x: x[1]["员工数"])
print(f"员工最多的部门: {max_staff_dept[0]}")  # 输出: 员工最多的部门: 部门B
```

### 9.4 实际应用场景 💡

嵌套字典在实际开发中非常常见，下面列举几个典型场景：

**场景1：学生成绩管理系统**

```python
students = {
    "张三": {
        "语文": 85,
        "数学": 92,
        "英语": 78
    },
    "李四": {
        "语文": 90,
        "数学": 88,
        "英语": 95
    },
    "王五": {
        "语文": 75,
        "数学": 82,
        "英语": 80
    }
}

# 查询某个学生的成绩
print(students["张三"]["数学"])  # 输出: 92

# 计算每个学生的平均分
for name, scores in students.items():
    avg = sum(scores.values()) / len(scores)
    print(f"{name}的平均分: {avg:.1f}")

# 找出每科最高分
subjects = ["语文", "数学", "英语"]
for subject in subjects:
    max_score = max(students[name][subject] for name in students)
    print(f"{subject}最高分: {max_score}")
```

**场景2：电商订单信息**

```python
orders = {
    "订单001": {
        "商品": "iPhone 15",
        "数量": 2,
        "价格": 5999,
        "客户": {
            "姓名": "张三",
            "电话": "13800138000",
            "地址": "北京市朝阳区"
        }
    },
    "订单002": {
        "商品": "MacBook Pro",
        "数量": 1,
        "价格": 12999,
        "客户": {
            "姓名": "李四",
            "电话": "13900139000",
            "地址": "上海市浦东新区"
        }
    }
}

# 访问嵌套的客户信息
print(orders["订单001"]["客户"]["姓名"])  # 输出: 张三

# 统计总收入
total = sum(order["价格"] * order["数量"] for order in orders.values())
print(f"总收入: {total}")  # 输出: 总收入: 24997
```

**场景3：多层分类配置**

```python
config = {
    "数据库": {
        "MySQL": {
            "host": "localhost",
            "port": 3306,
            "max_connections": 100
        },
        "Redis": {
            "host": "localhost",
            "port": 6379
        }
    },
    "日志": {
        "级别": "INFO",
        "文件路径": "/var/log/app.log",
        "最大大小": "100MB"
    }
}

# 访问深层配置
print(config["数据库"]["MySQL"]["host"])  # 输出: localhost
```

---

💡 **学习建议**：嵌套字典是处理复杂数据结构的利器。在实际使用中，我们要注意层级的合理性——过深的嵌套会增加代码复杂度。如果我们发现嵌套太深，可以考虑拆分成多个字典或使用类来组织数据。

## 10. 总结 🎉

我们在本章学习了 Python 字典的核心操作，主要包括以下几个方面：

- **字典创建**：使用 `{}`、`dict()`、`fromkeys()`、字典推导式
- **字典查询**：通过键获取值、`get()` 方法、`keys()/values()/items()`、`in` 运算符
- **字典增加**：直接赋值、`setdefault()`、`update()`
- **字典修改**：通过键修改、`update()`
- **字典删除**：`pop()`、`popitem()`、`del`、`clear()`
- **字典遍历**：遍历键、值、键值对，字典推导式
- **嵌套字典**：多层级的字典结构及其操作

掌握这些操作后，我们就可以在实际开发中高效地使用字典来处理各种数据了。

---

最后更新时间：2026-04-10
