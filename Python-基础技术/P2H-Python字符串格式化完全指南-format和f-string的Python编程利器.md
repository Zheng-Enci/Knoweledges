# P2H-Python字符串格式化完全指南-format和f-string的Python编程利器

## 📝 摘要



## 1. 概述 📚



## 2. % 格式化（旧式）📜

`%` 格式化是 Python 最古老的字符串格式化方式，源自 C 语言的 `printf` 函数，虽然未被废弃，但已不推荐在新项目中使用 🏛️

### 2.1 基本用法

```python
name = "Alice"
age = 25

# %s 表示字符串，%d 表示整数
print("Hello, %s! You are %d years old." % (name, age))
# 输出：Hello, Alice! You are 25 years old.
```

### 2.2 常见占位符

| 占位符 | 说明 | 例子 |
|--------|------|------|
| `%s` | 字符串 | `"%s" % "hello"` → `"hello"` |
| `%d` | 整数 | `"%d" % 3.14` → `"3"` |
| `%f` | 浮点数 | `"%.2f" % 3.1415` → `"3.14"` |
| `%r` | repr 字符串（带引号） | `"%r" % "hello"` → `"'hello'"` |

```python
# %s vs %r 的区别
print("%s" % "hello")  # hello（只是值）
print("%r" % "hello")  # 'hello'（带引号，repr 形式）
```

> 💡 `%r` 会显示对象的"官方表示形式"，字符串会带引号，常用于调试

```python
# 浮点数精度
pi = 3.1415926
print("%.2f" % pi)  # 3.14
print("%.3f" % pi)  # 3.142

# 宽度控制
print("%10s" % "hi")   # '        hi'（右对齐）
print("%-10s" % "hi")  # 'hi        '（左对齐）
```

### 2.3 用字典传参

```python
data = {"name": "Bob", "age": 30}
print("Name: %(name)s, Age: %(age)d" % data)
# 输出：Name: Bob, Age: 30
```

### 2.4 注意事项

- **过时但仍可用**：虽然现在推荐用 `format` 或 `f-string`，但 `%` 格式化依然被支持
- **与新式不兼容**：不能和 `format`、`f-string` 混合使用

> 💡 了解即可，现在推荐用 `f-string`！



## 3. format 方法 🎯

### 3.1 基本用法



### 3.2 位置参数



### 3.3 关键字参数



### 3.4 格式规格



## 4. f-string 方法 🔥

### 4.1 基本用法



### 4.2 表达式嵌入



### 4.3 格式规格



### 4.4 对齐与填充



## 5. 两者对比 ⚖️



## 6. 总结 📌

---

最后更新时间：
