# Python 可迭代对象完全指南 - 从列表到生成器的Python编程利器

## 📝 摘要

可迭代对象是 Python 的核心概念之一，我们几乎每天都在使用它，但却很少深入理解它。本文将带你全面掌握可迭代对象，包括定义、常见类型、判断方法、迭代器区别以及实际应用场景。

## 1. 什么是可迭代对象 📚

**可迭代对象**（Iterable）是指可以直接作用于 `for` 循环的对象。换句话说，能用 `for ... in ...` 遍历的就是可迭代对象。

```python
# 下面这些都是可迭代对象
for item in [1, 2, 3]:
    print(item)

for char in "hello":
    print(char)

for key in {"a": 1, "b": 2}:
    print(key)
```

> 💡 可迭代对象本质：实现了 `__iter__()` 方法的对象

## 2. 常见可迭代对象类型 🔍

### 2.1 序列类型

| 类型 | 示例 | 说明 |
|------|------|------|
| 列表 | `[1, 2, 3]` | 可变、有序 |
| 元组 | `(1, 2, 3)` | 不可变、有序 |
| 字符串 | `"hello"` | 字符序列、有序 |

### 2.2 集合类型

| 类型 | 示例 | 说明 |
|------|------|------|
| 集合 | `{1, 2, 3}` | 无序、唯一 |
| 字典 | `{"a": 1}` | 键值对、键唯一 |

### 2.3 其他类型

| 类型 | 说明 |
|------|------|
| 生成器 | `yield` 创建的惰性序列 |
| 迭代器 | `iter()` 返回的对象 |
| 文件对象 | 读取文件内容 |

```python
# 文件也是可迭代对象
with open("file.txt") as f:
    for line in f:  # 一行一行读取
        print(line)
```

## 3. 如何判断可迭代对象 ❓

### 3.1 使用 `hasattr` 判断

```python
# 判断对象是否有 __iter__ 方法
print(hasattr([1, 2, 3], "__iter__"))  # True
print(hasattr("hello", "__iter__"))   # True
print(hasattr(123, "__iter__"))       # False
```

### 3.2 使用 `collections.abc` 判断

```python
from collections.abc import Iterable

print(isinstance([1, 2, 3], Iterable))  # True
print(isinstance("hello", Iterable))     # True
print(isinstance(123, Iterable))         # False
```

### 3.3 常见报错

```python
# 整数不是可迭代对象，会报错
for i in 123:
    print(i)
# TypeError: 'int' object is not iterable
```

## 4. 迭代器 vs 可迭代对象 🔄

很多人容易混淆这两个概念，它们其实不一样：

| 特征 | 可迭代对象 | 迭代器 |
|------|-----------|--------|
| 定义 | 实现了 `__iter__` | 实现了 `__iter__` 和 `__next__` |
| 遍历方式 | for 循环 | for 循环或 `next()` |
| 状态 | 每次遍历都是新的 | 有遍历位置状态 |
| 例子 | list, str, dict | 生成器、file 对象 |

```python
# 列表是可迭代对象，但不是迭代器
my_list = [1, 2, 3]
print(hasattr(my_list, "__next__"))  # False

# iter() 返回迭代器
my_iter = iter(my_list)
print(hasattr(my_iter, "__next__"))  # True

# 用 next() 获取元素
print(next(my_iter))  # 1
print(next(my_iter))  # 2
print(next(my_iter))  # 3
# next(my_iter)  # StopIteration
```

> 💡 简单理解：迭代器 = 可迭代对象 + 遍历状态

## 5. 转换为可迭代对象 🔄

### 5.1 `iter()` 函数

将可迭代对象转换为迭代器：

```python
my_list = [1, 2, 3]
my_iter = iter(my_list)

print(next(my_iter))  # 1
print(next(my_iter))  # 2
```

### 5.2 常见转换场景

```python
# 字符串转列表
list("hello")  # ['h', 'e', 'l', 'l', 'o']

# 字典转键列表
list({"a": 1, "b": 2})  # ['a', 'b']

# 集合转列表
list({1, 2, 3})  # [1, 2, 3]
```

## 6. 实际应用场景 💡

### 6.1 遍历数据

```python
# 遍历列表
for item in [1, 2, 3]:
    print(item)

# 遍历字典（默认遍历键）
for key in {"name": "Tom", "age": 20}:
    print(key)

# 遍历字典的值
for value in {"name": "Tom", "age": 20}.values():
    print(value)

# 遍历键值对
for key, value in {"name": "Tom", "age": 20}.items():
    print(f"{key}: {value}")
```

### 6.2 配合内置函数

```python
# map
result = list(map(str, [1, 2, 3]))  # ['1', '2', '3']

# filter
result = list(filter(lambda x: x > 2, [1, 2, 3]))  # [3]

# sum
total = sum([1, 2, 3])  # 6

# max / min
print(max([1, 2, 3]))  # 3
print(min([1, 2, 3]))  # 1
```

### 6.3 推导式

```python
# 列表推导式
squares = [x**2 for x in range(5)]  # [0, 1, 4, 9, 16]

# 字典推导式
sq_dict = {x: x**2 for x in range(3)}  # {0: 0, 1: 1, 2: 4}

# 集合推导式
sq_set = {x**2 for x in range(3)}  # {0, 1, 4}
```

### 6.4 生成器表达式

```python
# 生成器表达式（惰性求值）
gen = (x**2 for x in range(5))
print(list(gen))  # [0, 1, 4, 9, 16]
```

## 7. 总结 📌

可迭代对象是 Python 中最基础也是最重要的概念之一：

- ✅ 可迭代对象 = 实现了 `__iter__` 方法的对象
- ✅ 常见类型：列表、元组、字符串、字典、集合、生成器
- ✅ 判断方法：`hasattr(obj, "__iter__")` 或 `isinstance(obj, Iterable)`
- ✅ 迭代器 = 可迭代对象 + `__next__` 方法，有遍历状态
- ✅ 掌握可迭代对象，能更好地理解 Python 的很多高级特性

> 💡 知道了解就好，不用深究背后的底层实现

---

**相关链接：**

- [P2A-Python列表](file:///f:\BaiduSyncdisk\ZhengEnCi\Note\Knowledge\Knowledges\Python-基础技术\P2A-Python列表-什么是列表？切片为什么这么强大？怎么快速掌握增删改查？.md)
- [P2F-Python集合](file:///f:\BaiduSyncdisk\ZhengEnCi\Note\Knowledge\Knowledges\Python-基础技术\P2F-Python集合完全指南-从创建到去重集合运算的Python编程利器.md)
- [P5D-Python推导式](file:///f:\BaiduSyncdisk\ZhengEnCi\Note\Knowledge\Knowledges\Python-基础技术\P5D-Python_推导式完全指南-从列表推导式到字典推导式的Python编程利器.md)

---

最后更新时间：2026-04-12