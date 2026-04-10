# P2F-Python集合完全指南-从创建到去重集合运算的Python编程利器

## 📝 摘要



---

## 1. 前置知识点 📚



---

## 2. 什么是集合（Set）📖



### 2.1 集合的核心特点 🔍

集合这货啊，简单来说就是"无序且不重复"的元素容器 🔩。它有四个核心特点，我们来一个个看：

**1. 无序性** 🎲

集合里的元素没有固定顺序，不支持下标访问。也就是说，我们不能用 `set[0]` 这种方式来取元素。那怎么访问呢？只能通过遍历或者直接判断元素是否存在。好处是什么呢？就是我们不需要关心元素的排列顺序，只要关心"这个元素在不在集合里"就行。

```python
s = {'a', 'b', 'c', 'd', 'e', 'f'}
print(s)  # 每次输出顺序可能不同，例如: {'c', 'a', 'f', 'd', 'b', 'e'}
```

**2. 唯一性** ✨

这是集合最迷人的特点——自动去重！当我们往集合里添加重复元素时，Python 会自动忽略它。这个特性在实际开发中超级实用，比如我们想找出列表中不重复的元素，直接转成集合就搞定了。

```python
s = {1, 2, 3, 2, 1, 4, 3}
print(s)  # 输出: {1, 2, 3, 4} - 自动去重了！
```

**3. 可变性** 🔧

集合本身是可以修改的，我们可以随时添加或删除元素。不过要注意，集合里的元素必须是**不可变类型**，比如字符串、数字、元组等。列表和字典这种可变类型是不能作为集合元素的，因为我们没办法确定它的哈希值。

那什么是不可变类型呢？简单来说，就是"创建后不能改变"的数据类型。在 Python 中：

- **可哈希（hashable）的类型**：int、float、str、bool、None、tuple（且元组内全是不可变元素）、frozenset
- **不可哈希（unhashable）的类型**：list、dict、set

为什么集合元素必须可哈希呢？因为集合底层用到了哈希表技术，它需要通过元素的哈希值来快速定位元素。如果元素是可以改变的，那它的哈希值就可能变化，集合就乱了套了。所以 Python 直接规定：集合元素必须是不可变类型！

```python
# 这些可以：
s1 = {1, 2, 3}                    # 整数
s2 = {'a', 'b', 'c'}               # 字符串
s3 = {(1, 2), (3, 4)}              # 元组（元素都是不可变的）

# 这些会报错：
s4 = {[1, 2], [3, 4]}              # ❌ TypeError: unhashable type: 'list'
s5 = {{'a': 1}}                    # ❌ TypeError: unhashable type: 'dict'
s6 = {{1, 2}}                      # ❌ TypeError: unhashable type: 'set'
```

**4. 高效操作** ⚡

集合底层基于哈希表实现，这意味着查找、添加、删除元素的时间复杂度都是 O(1)，也就是常数时间。无论集合里有100个元素还是100万个元素，操作速度都差不多。这可比列表的线性查找快多了！

---

### 2.2 集合 vs 列表 vs 元组对比 ⚖️

光说集合可能不太好理解，我们来把它和列表、元组放一起对比看看 📊：

| 特性 | 集合（set） | 列表（list） | 元组（tuple） |
|------|-------------|--------------|---------------|
| 有序性 | ❌ 无序 | ✅ 有序 | ✅ 有序 |
| 唯一性 | ✅ 自动去重 | ❌ 可以重复 | ❌ 可以重复 |
| 可变性 | ✅ 可变 | ✅ 可变 | ❌ 不可变 |
| 索引访问 | ❌ 不支持 | ✅ 支持 | ✅ 支持 |
| 元素类型 | 必须是不可变类型 | 可以是任意类型 | 可以是任意类型 |
| 查找效率 | O(1) 极快 | O(n) 较慢 | O(n) 较慢 |
| 内存占用 | 较高 | 较低 | 最低 |

从表格能看出来，集合最适合的场景就是：**需要快速查找、需要去重、需要集合运算**的时候 🏆。如果你需要保持元素顺序或者通过索引访问，那就用列表；如果你需要存储固定数据、追求极致性能，那就用元组。

---

## 3. 集合创建（set creation）✍️



### 3.1 使用花括号创建 🅰️

这是最直接的方式，直接用花括号把元素括起来，元素之间用逗号分隔：

```python
# 基本创建
fruits = {"apple", "banana", "orange"}
print(fruits)  # {'banana', 'orange', 'apple'}

# 数字集合
numbers = {1, 2, 3, 4, 5}
print(numbers)  # {1, 2, 3, 4, 5}

# 混合类型（只要是不可变类型就行）
mixed = {"hello", 123, (1, 2, 3)}
print(mixed)  # {'hello', 123, (1, 2, 3)}
```

还有一点很方便——自动去重！如果我们写重复的元素，Python 会自动帮我们去掉：

```python
s = {1, 2, 3, 2, 1, 4, 3}
print(s)  # {1, 2, 3, 4} - 自动去重了！
```

不过这里有个坑：**空的花括号 `{}` 创建的不是空集合，而是空字典！** 要创建空集合必须用 `set()`（详见 [3.2 使用 set() 函数创建](#32-使用-set-函数创建-🅱️)）。

```python
# ❌ 这是字典，不是集合！
empty_dict = {}
print(type(empty_dict))  # <class 'dict'>

# ✅ 这才是空集合
empty_set = set()
print(type(empty_set))  # <class 'set'>
print(empty_set)  # set()
```

---

### 3.2 使用 set() 函数创建 🅱️

`set()` 函数可以创建集合，还有几个常用用法：

**1. 创建空集合**

```python
empty_set = set()
print(empty_set)  # set()
```

**2. 从列表、元组、字符串转换**

这个功能超级实用！我们可以把其他可迭代对象转成集合，自动去重：

```python
# 从列表创建（自动去重）
lst = [1, 2, 3, 2, 1, 4]
s1 = set(lst)
print(s1)  # {1, 2, 3, 4}

# 从元组创建
tup = (1, 2, 3, 2, 1)
s2 = set(tup)
print(s2)  # {1, 2, 3}

# 从字符串创建（把字符拆成集合，自动去重）
text = "hello"
s3 = set(text)
print(s3)  # {'h', 'e', 'l', 'o'} - 注意 'l' 只出现一次
```

**3. 从集合创建（复制）**

```python
original = {1, 2, 3}
copied = set(original)
print(copied)  # {1, 2, 3}
```

---

### 3.3 集合推导式创建 🦾

和列表推导式类似，集合也有推导式！语法几乎一样，只是把方括号换成花括号。如果你想了解更多推导式的细节，可以看看 [P5D-Python_推导式完全指南](https://juejin.cn/post/7563597691680489491) 📚：

```python
# 基本语法
squares = {x**2 for x in range(1, 6)}
print(squares)  # {16, 1, 4, 9, 25}

# 带条件筛选
even_squares = {x**2 for x in range(1, 10) if x % 2 == 0}
print(even_squares)  # {16, 4, 36, 64}

# 从字符串过滤
text = "hello world"
unique_vowels = {char for char in text if char in 'aeiou'}
print(unique_vowels)  # {'e', 'o'}

# 复杂一点的条件
pairs = {(x, y) for x in range(3) for y in range(3)}
print(pairs)  # {(0, 0), (0, 1), (0, 2), (1, 0), ...}
```

集合推导式和列表推导式的区别：
- 列表推导式用方括号 `[]`
- 集合推导式用花括号 `{}`
- 集合会自动去重，列表不会

---

### 3.4 集合创建方式对比 📊

我们来对比一下这三种创建方式：

| 创建方式 | 适用场景 | 示例 |
|---------|---------|------|
| 花括号 `{}` | 已知具体元素，直观简洁 | `{1, 2, 3}` |
| `set()` 函数 | 从其他数据转换、创建空集合 | `set([1,2,3])`、`set()` |
| 集合推导式 | 批量生成、有筛选逻辑 | `{x**2 for x in range(5)}` |

使用建议：
- 如果知道具体元素，用花括号最直观
- 如果要从列表去重，用 `set()`
- 如果要批量生成有规律的元素，用推导式



---

## 4. 集合基本操作 🛠️



### 4.1 访问集合中的元素

我们前面说过，集合是无序的，所以不能用索引来访问元素。那怎么访问呢？两个办法：**遍历**和**成员检测** 🔍

**1. 遍历集合**

```python
fruits = {"apple", "banana", "orange"}

# 用 for 循环遍历
for fruit in fruits:
    print(fruit)  # 每次顺序可能不同
```

**2. 成员检测**

想知道某个元素在不在集合里？用 `in` 操作符，超快！

```python
fruits = {"apple", "banana", "orange"}

print("apple" in fruits)    # True
print("grape" in fruits)   # False
```

这就是集合最强大的地方——成员检测超级快！无论集合里有10个还是100万个元素，`in` 操作都是 O(1) 复杂度。

---

### 4.2 添加元素 ➕

往集合里添加元素有两种方式：

**1. add() - 添加单个元素**

```python
s = {1, 2, 3}
s.add(4)
print(s)  # {1, 2, 3, 4}

# 如果添加已存在的元素，什么都不会发生（自动去重）
s.add(2)
print(s)  # {1, 2, 3, 4} - 2 已经在集合里了
```

**2. update() - 添加多个元素**

```python
s = {1, 2, 3}
s.update([4, 5, 6])       # 从列表添加
print(s)  # {1, 2, 3, 4, 5, 6}

s.update((7, 8))          # 从元组添加
print(s)  # {1, 2, 3, 4, 5, 6, 7, 8}

s.update({9, 10})         # 从集合添加
print(s)  # {1, 2, 3, 4, 5, 6, 7, 8, 9, 10}

s.update("hello")         # 从字符串添加（每个字符）
print(s)  # {1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 'h', 'e', 'l', 'o'}
```

---

### 4.3 删除元素 🗑️

删除元素有四种方式，各有特点：

**1. remove() - 删除指定元素（元素不存在会报错）**

```python
s = {1, 2, 3, 4, 5}
s.remove(3)
print(s)  # {1, 2, 4, 5}

# 如果元素不存在，会抛出 KeyError
s.remove(100)  # KeyError: 100
```

**2. discard() - 删除指定元素（元素不存在不会报错）**

```python
s = {1, 2, 3, 4, 5}
s.discard(3)
print(s)  # {1, 2, 4, 5}

# 元素不存在也不会报错，安全感满满！
s.discard(100)  # 什么都不发生，程序继续运行
```

**3. pop() - 随机删除并返回一个元素**

```python
s = {1, 2, 3, 4, 5}
removed = s.pop()
print(f"删除的元素: {removed}")  # 随机一个元素
print(f"剩余集合: {s}")

# 空集合调用 pop() 会报错
empty_set = set()
empty_set.pop()  # KeyError: 'pop from an empty set'
```

**4. clear() - 清空集合**

```python
s = {1, 2, 3, 4, 5}
s.clear()
print(s)  # set() - 变成空集合了
```

---

### 4.4 计算集合长度

想知道集合里有多少个元素？用 `len()` 函数：

```python
s = {1, 2, 3, 4, 5}
print(len(s))  # 5

# 自动去重，所以长度会变
s = {1, 1, 1, 2, 2, 3}
print(len(s))  # 3
```

我们来看个对比表格 🧮：

| 方法 | 作用 | 特点 |
|------|------|------|
| `add(x)` | 添加单个元素 | 元素已存在则忽略 |
| `update(iterable)` | 添加多个元素 | 可接受列表、元组、集合、字符串 |
| `remove(x)` | 删除指定元素 | 元素不存在会报错 |
| `discard(x)` | 删除指定元素 | 元素不存在不报错 |
| `pop()` | 随机删除一个 | 返回被删除的元素，空集合报错 |
| `clear()` | 清空集合 | 集合变为空集合 |



---

## 5. 集合运算 ⚔️



### 5.1 并集（Union）🔗

并集就是把两个集合的所有元素合并在一起，重复的只保留一个。想象一下两个班的学生，合并成一个班 🎉

**运算符方式**

```python
set1 = {1, 2, 3}
set2 = {3, 4, 5}

# 用 | 运算符
result = set1 | set2
print(result)  # {1, 2, 3, 4, 5}
```

**方法方式**

```python
set1 = {1, 2, 3}
set2 = {3, 4, 5}

# 用 union() 方法
result = set1.union(set2)
print(result)  # {1, 2, 3, 4, 5}

# union() 可以接收多个参数
result = set1.union(set2, {6, 7})
print(result)  # {1, 2, 3, 4, 5, 6, 7}
```

我们来看个图示 🎨：

```mermaid
flowchart LR
    subgraph A[集合 A: {1, 2, 3}]
        direction TB
        A1["1"]
        A2["2"]
        A3["3"]
    end
    subgraph B[集合 B: {3, 4, 5}]
        direction TB
        B1["3"]
        B2["4"]
        B3["5"]
    end
    subgraph Result[并集 A | B: {1, 2, 3, 4, 5}]
        direction TB
        R1["1"]
        R2["2"]
        R3["3"]
        R4["4"]
        R5["5"]
    end
    A --> Result
    B --> Result
```

---

### 5.2 交集（Intersection）🎯

交集就是两个集合中都有的元素。想象一下两个班都参加了某项活动的学生 👥

**运算符方式**

```python
set1 = {1, 2, 3}
set2 = {3, 4, 5}

# 用 & 运算符
result = set1 & set2
print(result)  # {3}
```

**方法方式**

```python
set1 = {1, 2, 3}
set2 = {3, 4, 5}

# 用 intersection() 方法
result = set1.intersection(set2)
print(result)  # {3}

# intersection() 可以接收多个参数
set3 = {3, 5, 6}
result = set1.intersection(set2, set3)
print(result)  # {3}
```

图示 🎨：

```mermaid
flowchart LR
    subgraph A[集合 A: {1, 2, 3}]
        direction TB
        A1["1"]
        A2["2"]
        A3["3"]
    end
    subgraph B[集合 B: {3, 4, 5}]
        direction TB
        B1["3"]
        B2["4"]
        B3["5"]
    end
    subgraph Result[交集 A & B: {3}]
        direction TB
        R1["3"]
    end
    A3 --> Result
    B1 --> Result
```

---

### 5.3 差集（Difference）➖

差集就是 A 集合中有但 B 集合中没有的元素。想象一下参加了A活动但没参加B活动的学生 📋

**运算符方式**

```python
set1 = {1, 2, 3}
set2 = {3, 4, 5}

# 用 - 运算符
result = set1 - set2
print(result)  # {1, 2}

# 注意顺序：set2 - set1 结果不同
result = set2 - set1
print(result)  # {4, 5}
```

**方法方式**

```python
set1 = {1, 2, 3}
set2 = {3, 4, 5}

# 用 difference() 方法
result = set1.difference(set2)
print(result)  # {1, 2}
```

图示 🎨：

```mermaid
flowchart LR
    subgraph A[集合 A: {1, 2, 3}]
        direction TB
        A1["1"]
        A2["2"]
        A3["3"]
    end
    subgraph B[集合 B: {3, 4, 5}]
        direction TB
        B1["3"]
        B2["4"]
        B3["5"]
    end
    subgraph Result[差集 A - B: {1, 2}]
        direction TB
        R1["1"]
        R2["2"]
    end
    A1 --> Result
    A2 --> Result
    A3 -.->|被排除| B1
```

---

### 5.4 对称差集（Symmetric Difference）🔄

对称差集就是 A 和 B 的并集减去交集，也就是只属于其中一个集合的元素。想象一下参加了A或B活动（但不同时参加两个）的学生 🤔

**运算符方式**

```python
set1 = {1, 2, 3}
set2 = {3, 4, 5}

# 用 ^ 运算符
result = set1 ^ set2
print(result)  # {1, 2, 4, 5}
```

**方法方式**

```python
set1 = {1, 2, 3}
set2 = {3, 4, 5}

# 用 symmetric_difference() 方法
result = set1.symmetric_difference(set2)
print(result)  # {1, 2, 4, 5}
```

图示 🎨：

```mermaid
flowchart LR
    subgraph A[集合 A: {1, 2, 3}]
        direction TB
        A1["1"]
        A2["2"]
        A3["3"]
    end
    subgraph B[集合 B: {3, 4, 5}]
        direction TB
        B1["3"]
        B2["4"]
        B3["5"]
    end
    subgraph Result[对称差集 A ^ B: {1, 2, 4, 5}]
        direction TB
        R1["1"]
        R2["2"]
        R3["4"]
        R4["5"]
    end
    A1 --> Result
    A2 --> Result
    B2 --> Result
    B3 --> Result
    A3 -.->|被排除| B1
```

---

### 5.5 子集和超集 📊

子集和超集用来判断集合之间的关系：

- **子集**：A 是 B 的子集，说明 A 的所有元素 B 都有
- **超集**：A 是 B 的超集，说明 A 包含了 B 的所有元素

**子集判断**

```python
A = {1, 2, 3}
B = {1, 2, 3, 4, 5}

# 用 <= 判断 A 是否是 B 的子集
print(A <= B)           # True
print(A.issubset(B))   # True

# 用 < 判断 A 是否是 B 的真子集（不是相等的情况）
print(A < B)            # True
print(A == B)          # False
```

**超集判断**

```python
A = {1, 2, 3, 4, 5}
B = {1, 2, 3}

# 用 >= 判断 A 是否是 B 的超集
print(A >= B)           # True
print(A.issuperset(B)) # True

# 用 > 判断 A 是否是 B 的真超集
print(A > B)            # True
print(A == B)          # False
```

我们来看个总结表格 📊：

| 运算 | 运算符 | 方法 | 说明 |
|------|--------|------|------|
| 并集 | `\|` | `union()` | 所有元素合并 |
| 交集 | `&` | `intersection()` | 共同元素 |
| 差集 | `-` | `difference()` | A有B没有 |
| 对称差集 | `^` | `symmetric_difference()` | 仅属于其中一个 |
| 子集 | `<=` | `issubset()` | A全在B里 |
| 真子集 | `<` | - | A全在B里且不相等 |
| 超集 | `>=` | `issuperset()` | B全在A里 |
| 真超集 | `>` | - | B全在A里且不相等 |



---

## 6. 集合方法 🔧



### 6.1 增删方法



### 6.2 运算方法



---

## 7. 集合去重应用 💡



### 7.1 列表去重



### 7.2 字符串去重



### 7.3 复杂数据去重



---

## 8. frozenset：不可变集合 🔐



### 8.1 frozenset 的创建



### 8.2 frozenset 的使用场景



---

## 9. 实际应用场景 🚀



### 9.1 成员检测



### 9.2 数据去重



### 9.3 数学集合运算



### 9.4 关系对比



---

## 10. 总结 🎉



---

最后更新时间：2026-04-10
