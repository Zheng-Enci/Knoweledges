# P2E-Python字典操作完全指南-从增删改查到遍历嵌套的Python编程利器

## 📝 摘要

面向零基础，系统讲解 Python 字典（Dictionary）核心操作：增删改查、遍历、嵌套。通过生活化比喻与实战对比，掌握字典的高效操作方法，快速提升编程能力。

---

## 1. 前置知识点 📚

在深入学习 Python 字典之前，你需要了解以下基础概念：

- 📦 **变量（variable）**：用于存储数据的容器，就像生活中的 **盒子**，可以在里面存放不同的物品
- 🏷️ **数据类型（data type）**：Python 中的基本数据类型包括整数、浮点数、字符串等
- 🔑 **键值对（key-value pair）**：一种数据结构，由唯一的键（key）和对应的值（value）组成
- 🗂️ **哈希表（hash table）**：字典的底层数据结构，提供快速的查找性能

---

💡 **学习建议**：如果你已经掌握了 Python 变量和基本数据类型，就可以开始学习字典了。字典是 Python 最常用的数据结构之一，是后续学习 JSON、API 响应处理等内容的基础。

---

## 2. 什么是字典（Dictionary）📖

字典（Dictionary）是 Python 中最核心的映射类型数据结构 📚，它以 **键值对（key-value pairs）** 的形式存储数据，提供高效的查找能力 ⚡。你可以把它想象成生活中的 **通讯录** ——通过姓名（键）快速找到对应的电话号码（值），而不是像列表那样需要记住电话号码在第几位。

### 2.1 字典的核心特点 🔍

字典有以下几个重要特点：

- 🔑 **键值对结构**：每个元素都是一个键值对，由唯一的键（key）和对应的值（value）组成
- 🎯 **通过键访问**：使用键来存取值，而不是通过位置索引（如列表的 0、1、2）
- 🔄 **可变性**：字典是可变的，可以随时添加、修改或删除键值对
- 📋 **无序性**：字典中的元素没有固定的顺序（Python 3.7+ 保持插入顺序，但逻辑上仍视为无序）
- 🚫 **键的唯一性**：字典中的键必须是唯一的，不能重复
- 🔐 **键的可哈希性**：作为字典的键，必须是可哈希（hashable）的类型

### 2.1.1 什么是可哈希（Hashable）🤔

**可哈希（hashable）** 是指一个对象在它的生命周期内，哈希值（hash value）是固定的。Python 使用哈希值来快速查找字典中的键，所以只有可哈希的对象才能作为字典的键。

#### 2.1.1.1 可哈希的类型（可以作为字典的键）✅

| 类型 | 说明 | 示例 |
|------|------|------|
| **整数（int）** | 数字类型都是可哈希的 | `1`, `100`, `-5` |
| **浮点数（float）** | 浮点数也是可哈希的 | `3.14`, `2.5` |
| **字符串（str）** | 字符串是不可变的，所以可哈希 | `"name"`, `"key1"` |
| **布尔值（bool）** | True 和 False 都是可哈希的 | `True`, `False` |
| **元组（tuple）** | 元组是不可变的，但要求其中的元素也必须可哈希（原因见下文） | `(1, 2)`, `("a", "b")` ✅ |
| **frozenset** | 冻结集合，不可变的集合 | `frozenset([1, 2, 3])` |

#### 2.1.1.2 为什么元组内的元素也必须是可哈希的？❓

虽然元组本身是不可变的，但 Python 在计算元组的哈希值时，会递归地计算元组内所有元素的哈希值。如果元组内包含不可哈希的元素（比如列表），Python 就无法计算整个元组的哈希值，因此这个元组就不能作为字典的键。

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

| 类型 | 原因 | 示例 |
|------|------|------|
| **列表（list）** | 列表是可变的，内容可能改变 | `[1, 2, 3]` ❌ |
| **字典（dict）** | 字典是可变的 | `{"a": 1}` ❌ |
| **集合（set）** | 集合是可变的 | `{1, 2, 3}` ❌ |
| **包含可变元素的元组** | 元组中包含不可哈希的元素 | `(1, [2, 3])` ❌ |

### 2.1.1.4 如何判断对象是否可哈希 🔬

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

| 特性 | 字典（dict） | 列表（list） |
|------|-------------|-------------|
| 数据结构 | 键值对（key-value） | 有序序列 |
| 访问方式 | 通过键访问 | 通过索引访问 |
| 有序性 | 无序（Python 3.7+保持插入顺序） | 有序 |
| 查找性能 | O(1) 常量时间 | O(n) 线性时间 |
| 适用场景 | 快速查找、映射关系 | 顺序存储、遍历 |

### 2.1.3 实际应用场景 💡

字典在实际开发中非常常用，比如：

- **快速查询**：字典提供 O(1) 的平均时间复杂度进行查找操作，比列表的 O(n) 快得多。比如查字典、查用户信息、查配置项等
- **用户信息存储**：用用户名作为键，存储用户的年龄、邮箱等信息
- **配置项管理**：用配置名称作为键，存储对应的配置值
- **计数统计**：统计单词出现次数、商品销量等
- **JSON 数据处理**：JSON 对象在 Python 中就是字典类型

---

💡 **学习建议**：字典是 Python 最常用的数据结构之一，掌握它能让你的代码更高效、更易读。接下来我们将学习如何创建字典。

## 3. 字典创建（dict creation）✍️

字典（Dictionary）可以通过多种方式创建，选择合适的方法能让代码更简洁、更高效。本章我们将学习三种主要的创建方式。

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

字典的查询操作是使用字典的核心目的。字典之所以高效，正是因为它可以通过键快速找到对应的值，而不需要像列表那样遍历查找。本章我们将学习字典的几种查询方式。

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

### 7.1 pop() 方法 🏷️

### 7.2 popitem() 方法 📦

### 7.3 del 语句 ❌

### 7.4 clear() 方法 💣

## 8. 字典遍历（traversing）🚶

### 8.1 遍历键 🔑

### 8.2 遍历值 📊

### 8.3 遍历键值对 🔂

### 8.4 字典推导式遍历 🦾

## 9. 字典嵌套（nested dict）🏗️

### 9.1 什么是嵌套字典 🏗️

### 9.2 嵌套字典的增删改查 🔧

### 9.3 嵌套字典的遍历 🚶

### 9.4 实际应用场景 💡

## 10. 字典 vs 不用字典对比 ⚔️
## 11. 常见错误与对比修正 🚨
## 12. 选择建议与实践流程 📋
## 13. 参考资料与学习资源 📚
## 14. 总结 🎉

---

最后更新时间：2026-04-09
