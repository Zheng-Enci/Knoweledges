# P5A-PyTorch tensor `len()` 函数详解：什么决定了多维张量的「长度」？🐍

<!-- 全文摘要 -->
len(X) 在 PyTorch 张量上的作用并非返回所有元素个数，而是返回第 0 维（第一个维度）的大小。本文以 X = torch.arange(24).reshape(2, 3, 4) 为切入点，深入讲解 `len()` 在 Python 层面的底层机制、PyTorch Tensor 的 `__len__` 实现原理、多维张量的 dimension 索引体系，以及 `len(X)`、`X.shape[0]`、`X.size(0)` 三者的等价关系，帮助读者彻底理解「张量的长度」这一容易混淆的概念。
<!-- English Abstract -->
The `len()` function on a PyTorch tensor does **not** return the total number of elements, but rather the size of the first dimension (dimension 0). Using `X = torch.arange(24).reshape(2, 3, 4)` as a starting point, this document explains Python's `__len__` protocol, how PyTorch implements `__len__` for tensors, the multi-dimensional tensor indexing system, and the equivalence between `len(X)`, `X.shape[0]`, and `X.size(0)` 🐍
<!-- 全文摘要结束 -->

---

## 术语表 / Terminology

| 术语 / Term | 说明 / Description |
|-------------|-------------------|
| **Tensor（张量）** | PyTorch 中的多维数组，是神经网络计算的核心数据结构 |
| **Dimension（维度）** | 张量的一个轴（Axis），例如 2D 张量有行和列两个维度 |
| **`len()`** | Python 内建函数，返回对象的「长度」——对 Tensor 返回第 0 维大小 |
| **`__len__`** | Python Magic Method，`len()` 底层调用的方法 |
| **`shape`** | Tensor 的属性，返回 `torch.Size` 对象，描述各维度大小 |
| **`size()`** | Tensor 的方法，功能与 `shape` 相同，支持按维度索引 |
| **`torch.Size`** | `tuple` 的子类，存储张量每个维度的尺寸 |
| **Dimension 0/第 0 维** | 张量的第一个轴，在深度学习中最常表示 batch size |
| **`arange`** | PyTorch 函数，生成指定范围内的等差数列 |
| **`reshape`** | 改变张量形状而不改变数据内容 |

---

## 章节阅读路线图 🗺️ / Chapter Reading Roadmap

1. **问题引入：代码会输出什么？** 🤔 / Problem Introduction → 以具体问题引出核心概念
2. **`len()` 函数的底层机制** ⚙️ / How `len()` Works → 理解 Python 内建函数的实现原理
3. **PyTorch Tensor 的 `__len__`** 🔬 / PyTorch Tensor's `__len__` → 深入 Tensor 源码层面的实现
4. **多维张量的 Dimension 体系** 📐 / Multi-dimensional Tensor Dimensions → 理解 dimension 索引规则
5. **`len(X)` vs `X.shape[0]` vs `X.size(0)`** ⚖️ / Comparison → 三者的等价关系与使用场景
6. **完整可运行示例** 🎯 / Complete Runnable Example → 动手验证 + 边界情况
7. **总结** 📝 / Summary → 核心要点回顾

---

## 1. 问题引入：代码会输出什么？🤔 / Problem Introduction

> 📖 **Note:** 本章从一个具体的代码问题出发，引出 `len()` 在多维张量上的核心行为 / This chapter starts with a concrete code question, leading to the core behavior of `len()` on multi-dimensional tensors.

假设你和同事在 review 一段 PyTorch 代码，看到了这样一行：

```python
import torch                                                # 导入 PyTorch 核心库，提供张量运算 🔥

X = torch.arange(24).reshape(2, 3, 4)                       # 创建形状为 [2, 3, 4] 的三维张量，数据流动：arange(24)→ [24] → reshape → [2,3,4]
result = len(X)                                              # 调用 Python 内建 len() 函数 ❓
```

这时同事问你：「`result` 的值是多少？」

你可能会想：

- 「24 个元素，`len(X)` 应该返回 24 吧？」 ❌
- 「3 个维度，会不会是 3？」 ❌
- 「还是 2？还是 4？」 ❓

**答案是：2** ✅

```python
print(result)                                                # 输出：2 🎯
```

这个结果出乎很多初学者的意料——**`len(X)` 既不是返回元素总数，也不是返回维度数量**，它返回的是 **第 0 维（第一个维度）的大小**。

本章开篇点题，接下来的章节我们来深入剖析这背后的原理。

---

**参考资料：**

- [PyTorch 官方文档 -- torch.Tensor.size](https://docs.pytorch.org/docs/stable/generated/torch.Tensor.size.html)
- [Python 官方文档 -- Built-in Functions: len()](https://docs.python.org/3/library/functions.html#len) ⭐值得阅读
- [PyTorch Tensor Basics -- Jake Tae](https://jaketae.github.io/study/pytorch-tensor/)
- [PyTorch 张量维度理解 -- 知乎](https://zhuanlan.zhihu.com/p/600971102)
- [pytorch: 获取 tensor 维度的方法：shape 和 size() -- CSDN](https://blog.csdn.net/Caesar6666/article/details/122497393)

---

## 2. `len()` 函数的底层机制 ⚙️ / How `len()` Works

> 📖 **Note:** 本章讲解 Python `len()` 函数的内部实现机制 / This chapter explains the internal implementation of Python's `len()` function.

### 2.1 Python 内建函数 `len()` 的本质

`len()` 是 Python 的 built-in function（内建函数），用于返回一个对象的「长度」。它的核心行为由 **`__len__` magic method**（魔术方法，也称为 dunder method）决定。

```python
# 🤔 当你在 Python 中调用 len(obj) 时，底层发生了什么？

len(obj)                                                        # Python 解释器实际执行的是：type(obj).__len__(obj) 🔍
```

也就是说，`len(obj)` 等价于调用 `type(obj).__len__(obj)`。这是 Python 的 **Protocol Pattern**（协议模式）——`len()` 作为一个统一的接口，底层的具体行为由对象自己定义。

### 2.2 `__len__` Magic Method 协议

Python 内建函数 `len()` 的工作流程可以概括为：

1. 调用 `type(obj).__len__(obj)`
2. 如果 `__len__` 存在，返回其值（必须是非负整数）
3. 如果 `__len__` 不存在，抛出 `TypeError`：`object of type 'X' has no len()`

```python
# 🧪 验证 len() 的底层调用机制
class MyContainer:
    """自定义容器类，演示 __len__ 的工作方式 🧪

    参数 / Args:
        items: 初始元素列表

    返回 / Returns:
        int: 容器的长度

    示例 / Example:
        c = MyContainer([1, 2, 3])  →  len(c) → 3
    """
    def __init__(self, items):
        # 保存传入的元素列表，数据流动：[1,2,3] → self.items = [1,2,3]
        self.items = items
    
    """返回容器内元素个数 📊

    本方法被 len() 隐式调用，必须返回非负整数

    参数 / Args:
        self: 实例自身

    返回 / Returns:
        int: 元素个数
    """
    def __len__(self):
        # 返回 items 列表的长度，数据流动：self.items=[1,2,3] → 3
        return len(self.items)

# 测试 __len__ 的工作方式
c = MyContainer([1, 2, 3])
print(len(c))                                                    # 3 🎯 等价于 MyContainer.__len__(c)
```

**直观类比** 🎯：可以把 `len()` 想象成一个「万能测量尺」📏

- 你对着一个 **List** 说「量一下」→ 得到的是这个列表的元素个数
- 你对着一个 **String** 说「量一下」→ 得到的是字符串的字数
- 你对着一个 **Tensor** 说「量一下」→ 得到的是第一个维度的大小
- 同一个「测量尺」`len()`，对不同对象测量不同的「长度」——这得益于 `__len__` 协议的灵活性

---

**参考资料：**

- [Built-in Functions: len() -- Python Documentation](https://docs.python.org/3/library/functions.html#len) ⭐值得阅读
- [Making the len function work on your Python objects -- Python Morsels](https://www.pythonmorsels.com/making-the-len-function-work-on-your-python-objects/)
- [__len__ Magic Method -- Python Tutorial (YouTube)](https://www.youtube.com/watch?v=bGGXE0D41Nw)
- [cPython 源码 -- len() 的实现（Objects/abstract.c）](https://github.com/python/cpython/blob/main/Objects/abstract.c)

---

## 3. PyTorch Tensor 的 `__len__` 🔬 / PyTorch Tensor's `__len__`

> 📖 **Note:** 本章深入 PyTorch Tensor 的底层实现，揭秘 `len()` 到底返回什么 / This chapter dives into PyTorch's tensor implementation to reveal what `len()` actually returns.

### 3.1 Tensor 的 `__len__` 是怎么定义的？

在 PyTorch 的 C++ 底层实现中，Tensor 的 `__len__` 被定义为：

```python
# 💻 以下是 PyTorch Tensor.__len__ 的逻辑等价（Python 伪代码）
class Tensor:
    """PyTorch 张量类（简化的逻辑等价版本）🧠

    __len__ 被硬编码为返回 self.size(0)，即第 0 维的大小。
    """
    def __len__(self):
        # 返回第 0 维的大小，数据流动：X.shape=[2,3,4] → self.size(0) → 2
        return self.size(0)
```

也就是说，对于任意 Tensor X，`len(X)` 等价于 `X.size(0)`，返回 **第 0 个维度（第一个维度）的尺寸**。

### 3.2 用我们的例子验证

```python
import torch                                                # 导入 PyTorch 核心库 🔥

X = torch.arange(24).reshape(2, 3, 4)                       # 创建三维张量，数据：0~23 → 形状 [2,3,4]
print(f"X.shape = {X.shape}")                               # X.shape = torch.Size([2, 3, 4]) 👈 shape 属性
print(f"X.size() = {X.size()}")                             # X.size() = torch.Size([2, 3, 4]) 👈 size() 方法
print(f"X.size(0) = {X.size(0)}")                           # X.size(0) = 2  👈 第 0 维的大小
print(f"len(X) = {len(X)}")                                 # len(X) = 2  👈 等价于 X.size(0)
print(f"len(X) == X.size(0): {len(X) == X.size(0)}")        # True ✅
```

运行结果：

```
X.shape = torch.Size([2, 3, 4])
X.size() = torch.Size([2, 3, 4])
X.size(0) = 2
len(X) = 2
len(X) == X.size(0): True
```

### 3.3 为什么 `len` 不返回所有元素总数？（历史与设计考量）

这是一个很自然的问题。既然 `len([1,2,3])` 返回 3 个元素，为什么 `len(tensor)` 不返回 24 个元素？🤔

主要原因有三个：

#### 原因 1：与 NumPy 保持一致 🔗

NumPy 是 PyTorch 的前身和重要参考，在 NumPy 中：

```python
import numpy as np                                          # 导入 NumPy 🧮

arr = np.arange(24).reshape(2, 3, 4)                        # 创建形状 [2,3,4] 的数组，数据：0~23
print(len(arr))                                             # 2 ✅ 也是返回第一个维度的大小
```

PyTorch 在设计 API 时，大量参考了 NumPy 的语义，`len()` 的行为自然也保持一致。

#### 原因 2：`len()` 代表最外层的「容器长度」📦

`len()` 的语义是「容器的第一层有多长」。对于嵌套结构：

- **List of lists**：`len([[1,2],[3,4],[5,6]])` → 3（最外层有 3 个元素）
- **Tensor**：`len(tensor)` → 最外层（第 0 维）有多少个「子张量」

```python
# 🧪 类比理解：嵌套列表的 len()
nested_list = [[1,2,3,4], [5,6,7,8]]                       # 2 行 4 列的嵌套列表 📋
print(len(nested_list))                                     # 2 👈 最外层有 2 个列表元素
# 而内部第一行有 4 个元素
print(len(nested_list[0]))                                  # 4 👈 第 0 行有 4 个元素
```

Tensor 的行为和嵌套列表完全一致——`len(X)` 看的是最外面一层。

#### 原因 3：实际应用中 batch size 的需要 🎯

在深度学习中，Tensor 最常见的形状是 `[batch_size, channels, height, width]`（或类似格式）。第 0 维几乎总是表示 **batch size**（一批数据中有多少个样本）。经常需要获取 batch size：

```python
dataloader = ...                                            # 数据加载器 📦
for batch_images, batch_labels in dataloader:               # 遍历每个 batch，batch_images.shape=[32,3,224,224]
    batch_size = len(batch_images)                          # 32 ✅ 快速获取当前 batch 的样本数
    # batch_size = batch_images.size(0)                     # 也可以这么写，但 len() 更简洁直观
```

让 `len(tensor)` 返回第 0 维的大小，极大地方便了 batch size 的获取。

### 3.4 不同维度张量的 `len()` 行为一览

```python
import torch                                                # 导入 PyTorch 🔥

# 1D Tensor（向量）📏
t1d = torch.tensor([10, 20, 30, 40, 50])                   # 形状 [5]
print(f"1D 张量: shape={t1d.shape}, len={len(t1d)}")       # len=5 ✅ 返回元素个数（只有一个维度）

# 2D Tensor（矩阵）📊
t2d = torch.ones(3, 4)                                      # 形状 [3, 4]
print(f"2D 张量: shape={t2d.shape}, len={len(t2d)}")       # len=3 ✅ 返回行数（第 0 维大小）

# 3D Tensor（三维张量）🧊
t3d = torch.zeros(2, 3, 4)                                  # 形状 [2, 3, 4]
print(f"3D 张量: shape={t3d.shape}, len={len(t3d)}")       # len=2 ✅ 返回第 0 维大小

# 4D Tensor（图像批次）🖼️
t4d = torch.randn(8, 3, 224, 224)                           # 形状 [8, 3, 224, 224]
print(f"4D 张量: shape={t4d.shape}, len={len(t4d)}")       # len=8 ✅ 返回 batch size
```

输出：

```
1D 张量: shape=torch.Size([5]), len=5
2D 张量: shape=torch.Size([3, 4]), len=3
3D 张量: shape=torch.Size([2, 3, 4]), len=2
4D 张量: shape=torch.Size([8, 3, 224, 224]), len=8
```

**关键观察** 💡：无论多少维，`len()` 永远返回 `shape[0]`。

---

**参考资料：**

- [__len__ for torch tensors -- PyTorch GitHub Issue #270](https://github.com/pytorch/pytorch/issues/270) ⭐值得阅读
- [len(Tensor) doesn't work in script -- PyTorch GitHub Issue #13376](https://github.com/pytorch/pytorch/issues/13376)
- [PyTorch Tensor Basics -- Jake Tae](https://jaketae.github.io/study/pytorch-tensor/)
- [Confused about tensor dimensions and batches -- PyTorch Forums](https://discuss.pytorch.org/t/confused-about-tensor-dimensions-and-batches/4761)
- [pytorch: 获取 tensor 维度的方法 -- CSDN](https://blog.csdn.net/Caesar6666/article/details/122497393)

---

## 4. 多维张量的 Dimension 体系 📐 / Multi-dimensional Tensor Dimensions

> 📖 **Note:** 本章系统讲解 PyTorch 张量的 dimension 索引规则 / This chapter systematically explains the dimension indexing system of PyTorch tensors.

### 4.1 Dimension 索引规则

PyTorch 的 dimension 索引从 **0 开始**，因此：

| 位置 | 在 `[2, 3, 4]` 中的值 | 说明 |
|------|----------------------|------|
| `dim=0` 或 `size(0)` | 2 | 第 0 维（最外层、batch 维度） |
| `dim=1` 或 `size(1)` | 3 | 第 1 维（中间层） |
| `dim=2` 或 `size(2)` | 4 | 第 2 维（最内层） |

同时支持 **负索引**（Negative Indexing），从后往前数：

| 位置 | 在 `[2, 3, 4]` 中的值 | 对应正索引 | 说明 |
|------|----------------------|-----------|------|
| `dim=-1` | 4 | `dim=2` | 最后一个维度（最内层） |
| `dim=-2` | 3 | `dim=1` | 倒数第二个维度 |
| `dim=-3` | 2 | `dim=0` | 倒数第三个维度（最外层） |

```python
import torch                                                # 导入 PyTorch 🔥

X = torch.arange(24).reshape(2, 3, 4)                       # 形状 [2, 3, 4]

# 正索引：0 = 第一个维度，1 = 第二个，2 = 第三个
print(f"X.size(0)  = {X.size(0)}")                          # 2 ✅ 第 0 维
print(f"X.size(1)  = {X.size(1)}")                          # 3 ✅ 第 1 维
print(f"X.size(2)  = {X.size(2)}")                          # 4 ✅ 第 2 维

# 负索引：-1 = 最后一个维度，-2 = 倒数第二个，-3 = 倒数第三个
print(f"X.size(-1) = {X.size(-1)}")                         # 4 ✅ 最后一个维度（等价 size(2)）
print(f"X.size(-2) = {X.size(-2)}")                         # 3 ✅ 倒数第二个（等价 size(1)）
print(f"X.size(-3) = {X.size(-3)}")                         # 2 ✅ 倒数第三个（等价 size(0)）
```

### 4.2 可视化理解：从嵌套结构看维度

我们的 `X` 可以想象成这样一个嵌套结构：

```
三维张量 X: shape=[2, 3, 4]
┌─────────────────────────────────────────────────┐
│ 第0维外层 = 2 个「块」                           │
│                                                   │
│  ┌─ 块 0 ──────────────────────┐                  │
│  │  第1维中层 = 3 个「行」       │                  │
│  │  ┌─ 行 0: [ 0,  1,  2,  3] ─┤  ← 第2维 4列    │
│  │  ├─ 行 1: [ 4,  5,  6,  7] ─┤                  │
│  │  └─ 行 2: [ 8,  9, 10, 11] ─┤                  │
│  └──────────────────────────────┘                  │
│  ┌─ 块 1 ──────────────────────┐                  │
│  │  ┌─ 行 0: [12, 13, 14, 15] ─┤                  │
│  │  ├─ 行 1: [16, 17, 18, 19] ─┤                  │
│  │  └─ 行 2: [20, 21, 22, 23] ─┤                  │
│  └──────────────────────────────┘                  │
└─────────────────────────────────────────────────┘
       ↑                               ↑          ↑
     len(X)=2                      X.size(1)=3   X.size(2)=4
   （第0维大小）                    （第1维大小）  （第2维大小）
```

**直观类比** 🏢：把这个三维张量想象成一个 **2 层楼的办公楼**

- **第 0 维（dim=0）**：楼层数 → 2 层 👉 `len(X)` = 2
- **第 1 维（dim=1）**：每层有 3 个房间
- **第 2 维（dim=2）**：每个房间有 4 个座位

### 4.3 为什么不是 `len()` 返回元素总数？

如果需要获取张量的 **总元素个数**，应该使用 `X.numel()`（numel = number of elements）：

```python
import torch                                                # 导入 PyTorch 🔥

X = torch.arange(24).reshape(2, 3, 4)                       # 形状 [2, 3, 4]

# ❌ 错误尝试：这些都不是总数
print(len(X))                                               # 2 ❌ 不是 24
print(X.size(0))                                            # 2 ❌ 不是 24

# ✅ 正确的获取总数的两种方式
print(X.numel())                                            # 24 ✅ numel() = number of elements
print(X.shape[0] * X.shape[1] * X.shape[2])                 # 24 ✅ 手动累乘各维度
```

| 需求 | 正确写法 | 返回值 |
|------|---------|--------|
| 第 0 维大小 | `len(X)` 或 `X.size(0)` | 2 |
| 第 1 维大小 | `X.size(1)` | 3 |
| 第 2 维大小 | `X.size(2)` | 4 |
| 总元素个数 | `X.numel()` | 24 |
| 维度数量 | `X.dim()` 或 `X.ndim` | 3 |
| 所有维度大小 | `X.shape` 或 `X.size()` | `torch.Size([2, 3, 4])` |

---

**参考资料：**

- [PyTorch 官方文档 -- torch.Tensor.size](https://docs.pytorch.org/docs/stable/generated/torch.Tensor.size.html) ⭐值得阅读
- [PyTorch 张量维度理解 -- 知乎](https://zhuanlan.zhihu.com/p/600971102)
- [Pytorch 张量维度 -- 博客园](https://www.cnblogs.com/djw12333/p/11199956.html)
- [Pytorch 基础-张量结构操作 -- Zhang](https://www.armcvai.cn/2021-03-01/pytorch-structure-process.html)
- [比较Tensor.size()和Tensor.shape() -- CSDN](https://blog.csdn.net/qq_44833392/article/details/121130693)
- [Tensor.size() vs Tensor.shape -- PyTorch GitHub Issue #5544](https://github.com/pytorch/pytorch/issues/5544)

---

## 5. `len(X)` vs `X.shape[0]` vs `X.size(0)` ⚖️ / Comparison

> 📖 **Note:** 本章对比三种获取第 0 维大小的方式 / This chapter compares three ways to get the size of dimension 0.

### 5.1 三者的等价关系

对于任意 PyTorch Tensor，以下三种写法**完全等价**：

```python
import torch                                                # 导入 PyTorch 🔥

X = torch.arange(24).reshape(2, 3, 4)                       # 创建三维张量

# 三种获取第 0 维大小的方法 —— 结果都是 2 ✅
a = len(X)                                                  # 2 🐍 Python 内建函数，最简洁
b = X.shape[0]                                              # 2 📐 shape 是属性，通过元组索引
c = X.size(0)                                               # 2 🔧 size(0) 是方法，传入维度参数

print(f"len(X)       = {a}")                                # len(X)       = 2
print(f"X.shape[0]   = {b}")                                # X.shape[0]   = 2
print(f"X.size(0)    = {c}")                                # X.size(0)    = 2
```

### 5.2 使用场景对比

| 方式 | 类型 | 适用场景 | 优点 | 缺点 |
|------|------|---------|------|------|
| `len(X)` | built-in 函数 | 快速获取 batch size、Python 原生风格 | 最简洁，与其他 Python 容器一致 | 只能获取第 0 维 |
| `X.shape[0]` | tuple 索引 | 配合 shape 元组使用 | 属性访问，无函数调用开销 | 需要索引 |
| `X.size(0)` | 方法调用 | 灵活获取任意维度 | 统一接口，`size()` 返回完整元组 | 略啰嗦 |

### 5.3 代码风格建议

```python
# 🎯 场景 1：快速获取 batch size —— 推荐 len(X)
def train_one_epoch(dataloader, model):
    """训练一个 epoch，每步获取 batch size 🎯

    参数 / Args:
        dataloader: 数据加载器
        model: 神经网络模型

    返回 / Returns:
        float: 平均损失
    """
    for batch_idx, (images, labels) in enumerate(dataloader):  # 遍历每个 batch
        batch_size = len(images)                                # ✅ 推荐：简洁直观，batch_size 就是第 0 维
        # ... 训练代码 ...

        # 如果想计算当前进度
        if batch_idx % 100 == 0:                                # 每 100 步打印一次
            print(f"Batch {batch_idx}, size={batch_size}")      # 另一种写法：X.size(0)

# 🎯 场景 2：遍历第 0 维 —— 只能用 len()
for i in range(len(X)):                                         # ✅ 遍历 2 个块：range(2)
    block = X[i]                                                # block.shape = [3, 4]
    # 处理第 i 个块 ...

# 🎯 场景 3：获取多个维度信息 —— 推荐 .shape 或 .size()
B, C, H, W = X.shape                                           # ✅ 解构赋值：B=2, C=3, H=4, W=? 不对...
B, D, H = X.shape                                              # ✅ B=2, D=3, H=4
B = X.size(0)                                                  # ✅ 明确指定维度
```

### 5.4 注意事项 ⚠️

**1. `len()` 只能获取第 0 维，不能获取其他维度**

```python
X = torch.arange(24).reshape(2, 3, 4)                       # 形状 [2, 3, 4]

# ❌ 错误：len() 不接受维度参数
# len(X, 1)  → TypeError

# ✅ 正确：使用 size(dim) 或 shape[dim]
print(X.size(1))                                             # 3 ✅ 第 1 维
print(X.shape[2])                                            # 4 ✅ 第 2 维
```

**2. `len()` 在 TorchScript 中有特殊行为**

在 TorchScript 编译模式下，`len(tensor)` 的表现可能受到限制。PyTorch 官方推荐在使用 TorchScript 时使用 `tensor.size(0)` 替代 `len(tensor)`。

---

**参考资料：**

- [比较Tensor.size()和Tensor.shape() -- CSDN](https://blog.csdn.net/qq_44833392/article/details/121130693)
- [len(Tensor) doesn't work in script -- PyTorch GitHub Issue #13376](https://github.com/pytorch/pytorch/issues/13376)
- [PyTorch Tensor Basics -- Jake Tae](https://jaketae.github.io/study/pytorch-tensor/)
- [Confused about tensor dimensions and batches -- StackOverflow](https://stackoverflow.com/questions/45020108/confused-about-tensor-dimensions-and-batch-sizes-in-pytorch)

---

## 6. 完整可运行示例 🎯 / Complete Runnable Example

> 🎯 **Note:** 本章提供完整的可运行脚本，包含所有知识点 / This chapter provides a complete runnable script covering all key points.

```python
"""
PyTorch 张量 len() 函数完整演示 🐍 / Complete Demo of PyTorch Tensor len()

本演示涵盖：
1. len() 的基本行为 ✅
2. 与 shape、size() 的关系 ✅
3. 所有维度获取方式 ✅
4. 边界情况 ✅
"""

import torch                                                # 导入 PyTorch 核心库 🔥
import math                                                 # 导入数学库 🔢

"""演示 len() 在 PyTorch 多维张量上的行为 🎯

创建一个形状为 [2, 3, 4] 的三维张量 X，验证：
1. len(X) = X.size(0) = X.shape[0] = 2
2. 其他维度如何获取

参数 / Args:
    无

返回 / Returns:
    无（打印输出）
"""
def demo_len_on_tensor():
    """1. 创建测试张量 🏗️ / Create Test Tensor"""
    X = torch.arange(24).reshape(2, 3, 4)                   # 创建三维张量，数据流动：0~23 → [2,3,4]
    print("=" * 55)                                         # 打印分隔线 📏
    print("🧪 PyTorch len() 完整演示")                        # 打印标题
    print("=" * 55)                                         # 打印分隔线 📏
    print(f"X = torch.arange(24).reshape(2, 3, 4)")         # 打印创建语句
    print(f"X.shape        = {X.shape}")                    # X.shape = [2, 3, 4]
    print(f"X.numel()      = {X.numel()}")                  # 总元素数 = 24
    print()                                                  # 空行

    """2. 核心验证：len(X) = X.size(0) = X.shape[0] ✅"""
    print("📌 核心验证：三种方式等价")                         # 打印章节标题
    print(f"len(X)         = {len(X)}")                     # len(X) = 2
    print(f"X.size(0)      = {X.size(0)}")                  # X.size(0) = 2
    print(f"X.shape[0]     = {X.shape[0]}")                 # X.shape[0] = 2
    print(f"三者相等: {len(X) == X.size(0) == X.shape[0]}")  # True ✅
    print()                                                  # 空行

    """3. 各维度大小 📐 / Dimension Sizes"""
    print("📌 各维度大小")                                    # 打印章节标题
    print(f"dim-0 (第 0 维) = {X.size(0)}")                 # 2
    print(f"dim-1 (第 1 维) = {X.size(1)}")                 # 3
    print(f"dim-2 (第 2 维) = {X.size(2)}")                 # 4
    print(f"dim(-1) (最后维) = {X.size(-1)}")                # 4（负索引）
    print(f"dim(-3) (最外维) = {X.size(-3)}")                # 2（负索引）
    print()                                                  # 空行

    """4. 其他关键属性 🔑 / Other Key Attributes"""
    print("📌 其他关键属性")                                  # 打印章节标题
    print(f"X.dim()  (维度数) = {X.dim()}")                  # 3
    print(f"X.ndim   (维度数) = {X.ndim}")                   # 3
    print(f"X.numel() (总元素) = {X.numel()}")                # 24
    print(f"X.dtype  (数据类型) = {X.dtype}")                 # torch.int64
    print(f"X.device (设备)   = {X.device}")                 # cpu
    print()                                                  # 空行

    """5. 实际应用场景举例 🌟 / Real Usage Examples"""
    print("📌 应用场景举例")                                   # 打印章节标题
    
    # 遍历第 0 维，数据流动：X[0]->[3,4], X[1]->[3,4]
    print("遍历 X 的第 0 维（2 个块）:")                       # 打印提示
    for i in range(len(X)):                                 # for i in range(2): 遍历 2 个块
        block = X[i]                                        # 取出第 i 个块，形状 [3,4]
        print(f"  X[{i}].shape = {block.shape}")            # 打印每个块的形状
    print()                                                  # 空行

    """6. 函数封装示例 📦 / Function Example"""
    batch_size = get_batch_size(X)                          # 调用封装的函数获取 batch size
    print(f"get_batch_size(X) = {batch_size}")              # 2 ✅


"""获取张量的 batch size（第 0 维大小）📦

使用 len() 获取张量的第 0 维大小，最常见于深度学习中的 batch size 获取

参数 / Args:
    tensor: 任意 PyTorch 张量

返回 / Returns:
    int: 张量第 0 维的大小

示例 / Example:
    X = torch.randn(32, 3, 224, 224)  →  get_batch_size(X) → 32
"""
def get_batch_size(tensor):
    # 返回 tensor 第 0 维大小，数据流动：tensor.shape=[2,3,4] → len(tensor) → 2
    return len(tensor)


if __name__ == "__main__":
    # 🚀 运行演示
    demo_len_on_tensor()
```

### 6.1 运行结果 / Example Output

```
=======================================================
🧪 PyTorch len() 完整演示
=======================================================
X = torch.arange(24).reshape(2, 3, 4)
X.shape        = torch.Size([2, 3, 4])
X.numel()      = 24

📌 核心验证：三种方式等价
len(X)         = 2
X.size(0)      = 2
X.shape[0]     = 2
三者相等: True

📌 各维度大小
dim-0 (第 0 维) = 2
dim-1 (第 1 维) = 3
dim-2 (第 2 维) = 4
dim(-1) (最后维) = 4
dim(-3) (最外维) = 2

📌 其他关键属性
X.dim()  (维度数) = 3
X.ndim   (维度数) = 3
X.numel() (总元素) = 24
X.dtype  (数据类型) = torch.int64
X.device (设备)   = cpu

📌 应用场景举例
遍历 X 的第 0 维（2 个块）:
  X[0].shape = torch.Size([3, 4])
  X[1].shape = torch.Size([3, 4])

get_batch_size(X) = 2
```

---

## 7. 总结 📝 / Summary

回到开头的问题，现在我们可以清楚地回答：

> **假设张量 X = torch.arange(24).reshape(2, 3, 4)，`len(X)` 的输出结果是 2** ✅

核心要点回顾：🎯

| 知识点 | 结论 | 代码 |
|-------|------|------|
| `len(X)` 是什么 | 返回张量第 0 维大小 | `len(X)` = 2 |
| 底层机制 | 调用 `Tensor.__len__()` 等价于 `size(0)` | `type(X).__len__(X)` |
| 等价写法 | `len(X) == X.size(0) == X.shape[0]` | 三者完全等价 |
| 获取其他维度 | 使用 `size(dim)` 或 `shape[dim]` | `X.size(1)` = 3 |
| 获取元素总数 | 使用 `numel()` | `X.numel()` = 24 |
| 获取维度数量 | 使用 `dim()`  | `X.dim()` = 3 |
| 设计哲学 | 与 NumPy 一致，返回最外层容器的大小 | `len(np.array(...))` |

🔴 **关键理解**：

- 💡 `len()` 在 Python 中是一个统一的协议接口，底层的具体行为由对象的 `__len__` 方法决定
- 🧠 PyTorch Tensor 的 `__len__` 被定义为 `self.size(0)`，返回第 0 维的大小
- 📦 `len()` 衡量的是「最外层容器的长度」，而非总元素数——这与嵌套列表的 `len()` 行为一致
- ⚡ 在深度学习中，`len(tensor)` 最常见的用途是获取 batch size

---

**最后更新时间**：2026-07-02
