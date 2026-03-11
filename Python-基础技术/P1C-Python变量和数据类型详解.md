# P1C-Python变量和数据类型详解

## 目录

- [1. 变量基础](#1-变量基础)
- [2. 变量命名规则](#2-变量命名规则)
- [3. 数据类型概述](#3-数据类型概述)
- [4. 数值类型](#4-数值类型)
- [5. 字符串类型](#5-字符串类型)
- [6. 布尔类型](#6-布尔类型)
- [7. 序列类型](#7-序列类型)
- [8. 映射类型](#8-映射类型)
- [9. 集合类型](#9-集合类型)
- [10. 类型转换](#10-类型转换)
- [11. 内存管理](#11-内存管理)
- [12. 最佳实践](#12-最佳实践)

## 1. 变量基础

在Python中，变量是用来存储数据的标识符。Python是动态类型语言，这意味着变量的类型在运行时确定，不需要显式声明类型。

### 基本变量赋值

```python
# 基本变量赋值
name = "张三"
age = 25
height = 175.5
is_student = True

print(name)      # 输出: 张三
print(age)       # 输出: 25
print(height)    # 输出: 175.5
print(is_student) # 输出: True
```

**特点：**

- Python变量不需要声明类型
- 变量名是引用，指向内存中的对象
- 同一个变量可以重新赋值为不同类型的值
- Python使用引用计数进行垃圾回收

## 2. 变量命名规则

Python变量命名遵循以下规则：

### 命名规则示例

```python
# 正确的变量命名
user_name = "张三"           # 使用下划线分隔
userAge = 25                # 驼峰命名法
user_id = 12345             # 包含数字
_private_var = "私有变量"    # 下划线开头表示私有
__very_private = "很私有"   # 双下划线开头

# 错误的变量命名
# 2user = "错误"            # 不能以数字开头
# user-name = "错误"        # 不能包含连字符
# class = "错误"            # 不能使用关键字
```

**命名规范：**

- 变量名只能包含字母、数字和下划线
- 变量名不能以数字开头
- 变量名区分大小写
- 不能使用Python关键字作为变量名
- 建议使用有意义的描述性名称

## 3. 数据类型概述

Python内置了多种数据类型，主要分为以下几类：

| 类型分类 | 数据类型 | 描述 | 示例 |
|---------|---------|------|------|
| 数值类型 | int | 整数 | 42, -10, 0 |
| 数值类型 | float | 浮点数 | 3.14, -2.5, 0.0 |
| 数值类型 | complex | 复数 | 3+4j, 1-2j |
| 文本类型 | str | 字符串 | "Hello", 'World' |
| 布尔类型 | bool | 布尔值 | True, False |
| 序列类型 | list | 列表 | [1, 2, 3], ['a', 'b'] |
| 序列类型 | tuple | 元组 | (1, 2, 3), ('a', 'b') |
| 序列类型 | range | 范围 | range(5), range(1, 10) |
| 映射类型 | dict | 字典 | {'name': '张三', 'age': 25} |
| 集合类型 | set | 集合 | {1, 2, 3}, {'a', 'b'} |
| 集合类型 | frozenset | 不可变集合 | frozenset({1, 2, 3}) |

## 4. 数值类型

### 4.1 整数 (int)

```python
# 整数类型
positive_int = 42
negative_int = -10
zero = 0
large_int = 999999999999999999999999999999

print(type(positive_int))  # <class 'int'>
print(positive_int + negative_int)  # 32
print(large_int)  # Python支持任意大的整数
```

### 4.2 浮点数 (float)

```python
# 浮点数类型
pi = 3.14159
negative_float = -2.5
scientific = 1.23e4  # 科学计数法: 12300.0
zero_float = 0.0

print(type(pi))  # <class 'float'>
print(scientific)  # 12300.0
print(pi + negative_float)  # 0.64159
```

### 4.3 复数 (complex)

```python
# 复数类型
complex_num = 3 + 4j
another_complex = complex(1, 2)  # 1 + 2j

print(type(complex_num))  # <class 'complex'>
print(complex_num.real)   # 3.0 (实部)
print(complex_num.imag)   # 4.0 (虚部)
print(abs(complex_num))   # 5.0 (模长)
```

⚠️ **注意：**浮点数运算可能存在精度问题，如 `0.1 + 0.2` 可能不等于 `0.3`。

## 5. 字符串类型 (str)

字符串是Python中用于存储文本数据的数据类型。

### 5.1 字符串创建

```python
# 字符串创建方式
single_quote = 'Hello World'
double_quote = "Hello World"
triple_quote = """多行字符串
可以跨越多行
保持格式"""
raw_string = r"C:\Users\Name"  # 原始字符串，不转义

print(single_quote)
print(triple_quote)
print(raw_string)
```

### 5.2 字符串操作

```python
# 字符串基本操作
text = "Python Programming"

# 长度
print(len(text))  # 18

# 索引和切片
print(text[0])     # P (第一个字符)
print(text[-1])    # g (最后一个字符)
print(text[0:6])   # Python (切片)

# 字符串方法
print(text.upper())        # PYTHON PROGRAMMING
print(text.lower())        # python programming
print(text.replace("Python", "Java"))  # Java Programming
print(text.split())        # ['Python', 'Programming']
```

### 5.3 字符串格式化

```python
# 字符串格式化
name = "张三"
age = 25

# 方法1: % 格式化
message1 = "我叫%s，今年%d岁" % (name, age)

# 方法2: format() 方法
message2 = "我叫{}，今年{}岁".format(name, age)

# 方法3: f-string (推荐)
message3 = f"我叫{name}，今年{age}岁"

print(message1)
print(message2)
print(message3)
```

## 6. 布尔类型 (bool)

布尔类型只有两个值：`True` 和 `False`。

```python
# 布尔类型
is_student = True
is_working = False

print(type(is_student))  # <class 'bool'>
print(is_student)        # True
print(not is_student)    # False

# 布尔运算
print(True and False)    # False
print(True or False)     # True
print(not True)          # False

# 其他类型转换为布尔值
print(bool(1))           # True
print(bool(0))           # False
print(bool(""))          # False
print(bool("Hello"))     # True
print(bool([]))          # False
print(bool([1, 2, 3]))   # True
```

**布尔值转换规则：**

- 数字：0为False，非0为True
- 字符串：空字符串为False，非空为True
- 列表/元组：空序列为False，非空为True
- None：始终为False

## 7. 序列类型

### 7.1 列表 (list)

```python
# 列表 - 可变序列
numbers = [1, 2, 3, 4, 5]
mixed_list = [1, "Hello", 3.14, True]
empty_list = []

# 列表操作
print(len(numbers))      # 5
print(numbers[0])        # 1
print(numbers[-1])       # 5
print(numbers[1:3])      # [2, 3]

# 修改列表
numbers.append(6)        # 添加元素
numbers.insert(0, 0)     # 在索引0处插入0
numbers.remove(3)        # 删除第一个3
del numbers[0]           # 删除索引0的元素

print(numbers)           # [1, 2, 4, 5, 6]
```

### 7.2 元组 (tuple)

```python
# 元组 - 不可变序列
coordinates = (10, 20)
single_tuple = (42,)     # 单元素元组需要逗号
empty_tuple = ()

# 元组操作
print(len(coordinates))  # 2
print(coordinates[0])    # 10
print(coordinates[1])    # 20

# 元组解包
x, y = coordinates
print(f"x = {x}, y = {y}")  # x = 10, y = 20

# 元组不能修改
# coordinates[0] = 5  # 错误！元组不可变
```

### 7.3 范围 (range)

```python
# 范围对象
r1 = range(5)           # 0, 1, 2, 3, 4
r2 = range(1, 6)        # 1, 2, 3, 4, 5
r3 = range(0, 10, 2)    # 0, 2, 4, 6, 8

print(list(r1))         # [0, 1, 2, 3, 4]
print(list(r2))         # [1, 2, 3, 4, 5]
print(list(r3))         # [0, 2, 4, 6, 8]

# 在循环中使用
for i in range(3):
    print(f"第{i+1}次循环")
```

## 8. 映射类型 - 字典 (dict)

字典是键值对的集合，用于存储映射关系。

```python
# 字典创建
person = {
    "name": "张三",
    "age": 25,
    "city": "北京"
}

# 访问字典
print(person["name"])        # 张三
print(person.get("age"))     # 25
print(person.get("salary", "未知"))  # 未知 (默认值)

# 修改字典
person["age"] = 26           # 修改值
person["salary"] = 5000      # 添加新键值对

# 字典方法
print(person.keys())         # dict_keys(['name', 'age', 'city', 'salary'])
print(person.values())       # dict_values(['张三', 26, '北京', 5000])
print(person.items())        # dict_items([('name', '张三'), ...])

# 删除元素
del person["city"]           # 删除键值对
age = person.pop("age")      # 删除并返回值
```

**字典特点：**

- 键必须是不可变类型（字符串、数字、元组等）
- 键不能重复
- 值可以是任意类型
- 字典是无序的（Python 3.7+保持插入顺序）

## 9. 集合类型

### 9.1 集合 (set)

```python
# 集合 - 可变集合
fruits = {"apple", "banana", "orange"}
numbers = {1, 2, 3, 4, 5}
empty_set = set()  # 空集合

# 集合操作
fruits.add("grape")        # 添加元素
fruits.remove("banana")    # 删除元素
fruits.discard("kiwi")     # 安全删除（不存在不报错）

print(fruits)              # {'apple', 'orange', 'grape'}

# 集合运算
set1 = {1, 2, 3, 4}
set2 = {3, 4, 5, 6}

print(set1 | set2)         # 并集: {1, 2, 3, 4, 5, 6}
print(set1 & set2)         # 交集: {3, 4}
print(set1 - set2)         # 差集: {1, 2}
print(set1 ^ set2)         # 对称差集: {1, 2, 5, 6}
```

### 9.2 不可变集合 (frozenset)

```python
# 不可变集合
frozen = frozenset([1, 2, 3, 4])
print(frozen)              # frozenset({1, 2, 3, 4})

# 可以作为字典的键
dict_with_frozen = {frozen: "value"}
print(dict_with_frozen[frozen])  # value
```

**集合特点：**

- 元素唯一，自动去重
- 元素必须是不可变类型
- 集合是无序的
- 支持数学集合运算

## 10. 类型转换

Python提供了内置函数进行类型转换：

```python
# 数值类型转换
int_num = int(3.14)        # 3
float_num = float("3.14")  # 3.14
str_num = str(42)          # "42"

# 字符串转换
text = "Hello World"
list_chars = list(text)    # ['H', 'e', 'l', 'l', 'o', ' ', 'W', 'o', 'r', 'l', 'd']
tuple_chars = tuple(text)  # ('H', 'e', 'l', 'l', 'o', ' ', 'W', 'o', 'r', 'l', 'd')

# 列表和元组转换
my_list = [1, 2, 3]
my_tuple = tuple(my_list)  # (1, 2, 3)
back_to_list = list(my_tuple)  # [1, 2, 3]

# 集合转换
my_set = set([1, 2, 2, 3, 3])  # {1, 2, 3} (自动去重)
back_to_list = list(my_set)    # [1, 2, 3]

# 布尔转换
print(bool(0))             # False
print(bool(1))             # True
print(bool(""))            # False
print(bool("Hello"))       # True
```

⚠️ **转换注意事项：**

- 字符串转数字时，字符串必须是有效的数字格式
- 浮点数转整数会截断小数部分
- 某些转换可能丢失精度或信息

## 11. 内存管理

Python使用引用计数和垃圾回收机制管理内存：

```python
# 引用和对象
a = [1, 2, 3]  # a是引用，指向列表对象
b = a          # b也指向同一个对象
print(a is b)  # True (同一个对象)

# 修改会影响所有引用
a.append(4)
print(b)       # [1, 2, 3, 4]

# 重新赋值会创建新的引用
a = [5, 6, 7]  # a现在指向新的列表对象
print(a)       # [5, 6, 7]
print(b)       # [1, 2, 3, 4] (b仍然指向原对象)

# 检查对象身份
print(id(a))   # 对象的内存地址
print(id(b))   # 不同的内存地址
```

**内存管理要点：**

- 变量是引用，不是对象本身
- 多个变量可以引用同一个对象
- 当引用计数为0时，对象被垃圾回收
- 使用 `is` 检查对象身份
- 使用 `==` 检查值相等

## 12. 最佳实践

### 12.1 变量命名

```python
# 好的命名示例
user_name = "张三"           # 描述性名称
max_retry_count = 3         # 清晰的含义
is_logged_in = True         # 布尔值用is_开头

# 避免的命名
a = "张三"                  # 无意义
x1 = 3                      # 不清晰
temp = "Hello"              # 临时变量名
```

### 12.2 类型检查

```python
# 使用type()检查类型
value = 42
if type(value) == int:
    print("是整数")

# 使用isinstance()检查类型（推荐）
if isinstance(value, int):
    print("是整数")

# 检查多个类型
if isinstance(value, (int, float)):
    print("是数值类型")
```

### 12.3 常量定义

```python
# 常量通常用全大写命名
PI = 3.14159
MAX_CONNECTIONS = 100
DEFAULT_TIMEOUT = 30

# 在函数中使用常量
def calculate_circle_area(radius):
    return PI * radius ** 2
```

**最佳实践总结：**

- 使用描述性的变量名
- 遵循PEP 8命名规范
- 使用 `isinstance()` 而不是 `type()`
- 常量使用全大写命名
- 避免使用单字母变量名（除了循环变量）
- 保持代码的可读性和可维护性

## 总结

Python的变量和数据类型是编程的基础。掌握这些概念对于编写Python程序至关重要：

- **变量**是存储数据的标识符，Python是动态类型语言
- **数据类型**包括数值、字符串、布尔、序列、映射和集合类型
- **类型转换**允许在不同数据类型之间转换
- **内存管理**通过引用计数和垃圾回收自动处理
- **最佳实践**帮助编写更清晰、可维护的代码

通过不断练习和实际应用，您将能够熟练使用Python的各种数据类型，为后续学习更高级的Python特性打下坚实基础。

---

**厦门工学院人工智能创作坊 --郑恩赐**
