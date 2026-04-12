# P2B-Python可迭代对象完全指南-从列表到生成器的Python编程利器

## 📝 摘要



## 1. 什么是可迭代对象 📚

**可迭代对象（Iterable）** 就是可以用 `for` 循环遍历的对象 🔁

通俗来说，就是"能一个一个取出元素的对象"：

```python
# 列表是可迭代对象
for item in [1, 2, 3]:
    print(item)  # 依次输出 1, 2, 3

# 字符串是可迭代对象
for char in "hello":
    print(char)  # 依次输出 h, e, l, l, o

# 字典是可迭代对象
for key in {"name": "Tom", "age": 18}:
    print(key)  # 依次输出 name, age
```

### 技术定义

从代码层面来说，**实现了 `__iter__` 方法的对象就是可迭代对象**：

```python
# 查看列表的__iter__方法
print([].__iter__)  # <method-wrapper '__iter__' of list object at 0x...>
```

这个方法的作用是返回一个**迭代器**（Iterator），然后我们就可以用迭代器逐个获取元素啦~



## 2. 常见可迭代对象类型 🔍

Python 中的可迭代对象非常丰富，主要分为以下几类 📋

### 2.1 内置序列类型

| 类型 | 示例 | 说明 |
|------|------|------|
| 列表 | `[1, 2, 3]` | 有序、可变 |
| 元组 | `(1, 2, 3)` | 有序、不可变 |
| 字符串 | `"hello"` | 有序、字符序列 |
| range | `range(5)` | 整数序列 |

```python
# 列表
for i in [1, 2, 3]:
    print(i)

# 元组
for i in (1, 2, 3):
    print(i)

# 字符串
for c in "abc":
    print(c)

# range
for i in range(3):
    print(i)  # 0, 1, 2
```

### 2.2 集合类型

| 类型 | 示例 | 说明 |
|------|------|------|
| 集合 | `{1, 2, 3}` | 无序、唯一 |
| 字典 | `{"a": 1}` | 键值对 |

```python
# 集合（遍历的是键）
for i in {1, 2, 3}:
    print(i)

# 字典（默认遍历键）
for key in {"name": "Tom", "age": 18}:
    print(key)  # name, age
```

### 2.3 特殊类型

| 类型 | 示例 | 说明 |
|------|------|------|
| 文件对象 | `open("file.txt")` | 逐行读取 |
| 生成器 | `(i for i in range(5))` | 惰性生成，按需取值 |
| 迭代器 | `iter([1,2,3])` | 消耗性遍历，用完就没 |

**什么是消耗性遍历？**

> 💡 知道了解就好，不用深究

迭代器只能遍历**一次**，用完就没了 🚫

```python
it = iter([1, 2, 3])
for i in it:
    print(i)  # 1, 2, 3
for i in it:  # 什么都没了
    print(i)  # 不输出
```

**什么是惰性生成？**

> 💡 知道了解就好，不用深究

简单说，生成器**记录了数据怎么生成的规则**，只有当你**用 `next()` 或遍历时**，才会**根据这个规则生成具体的值** 🏭

- **列表** `[1,2,3]` → 直接存了3个值
- **生成器** `(x for x in range(3))` → 只存了"怎么生成"的规则，用到时才算

```python
# 列表 → 直接存值
lst = [1, 2, 3]

# 生成器 → 记录生成规则，用next()才取值
gen = (x * 2 for x in range(3))
print(next(gen))  # 0
print(next(gen))  # 2
print(next(gen))  # 4
```

```python
# 生成器表达式
gen = (i * 2 for i in range(3))
for i in gen:
    print(i)  # 0, 2, 4

# range 对象
for i in range(5):
    print(i)
```

> 💡 **Tip**：几乎所有可以"逐个访问"的数据结构都是可迭代对象！



## 3. 如何判断可迭代对象 ❓



## 4. 迭代器与可迭代对象的区别 🔄



## 5. 实际应用场景 💡



## 6. 总结 📌

---

最后更新时间：