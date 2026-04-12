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



## 3. 如何判断可迭代对象 ❓



## 4. 迭代器与可迭代对象的区别 🔄



## 5. 实际应用场景 💡



## 6. 总结 📌

---

最后更新时间：