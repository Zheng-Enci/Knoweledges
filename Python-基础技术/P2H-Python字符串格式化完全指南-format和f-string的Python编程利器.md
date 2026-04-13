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
# 浮点数精度（小数点后保留几位）
pi = 3.1415926
print("%.2f" % pi)  # .2f 表示保留2位小数 → 3.14
print("%.3f" % pi)  # .3f 表示保留3位小数 → 3.142

# 宽度控制（总宽度，正数右对齐，负数左对齐）
print("%10s" % "hi")   # 10 表示总宽度10字符，右对齐 → '        hi'
print("%-10s" % "hi")  # -10 表示左对齐 → 'hi        '
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

`format` 方法是 Python 2.6 引入的格式化方式，比 `%` 更灵活强大 💪

### 3.1 基本用法

```python
# 空的占位符，按顺序填充
print("Hello, {}!".format("Alice"))  # Hello, Alice!

# 多个占位符
print("{} + {} = {}".format(1, 2, 3))  # 1 + 2 = 3
```

### 3.2 位置参数

用 `{0}`、`{1}` 等数字指定参数位置（0 表示第1个参数，1 表示第2个，以此类推）：

```python
# 使用索引
print("{0} {1} {0}".format("Hello", "World"))
# 输出：Hello World Hello

# 调换顺序
print("{1} {0}".format("World", "Hello"))  # Hello World
```

### 3.3 关键字参数

通过名称指定参数：

```python
# 使用关键字参数
print("{name} is {age} years old".format(name="Tom", age=20))
# 输出：Tom is 20 years old

# 混合使用
print("{0} is {age} years old".format("Bob", age=25))
# 输出：Bob is 25 years old

# 用字典传参
data = {"name": "Lily", "age": 18}
print("{name} is {age}".format(**data))
# 输出：Lily is 18
```

> 💡 如果不了解 `**` 解包语法，可以查看 [P3C-参数与可变参数](https://juejin.cn/post/7569886315197431859) 📝

### 3.4 格式规格

> 💡 用法和上面 % 格式化一致，数字含义相同

控制数字格式：

```python
# 浮点数精度（:.数字f，:后是数字，f表示浮点数）
print("{:.2f}".format(3.14159))  # .2f 表示保留2位小数 → 3.14
print("{:.3f}".format(3.14159))  # .3f 表示保留3位小数 → 3.142

# 对齐与宽度（:数字表示宽度，>右 <左 ^中）
print("{:>10}".format("hi"))       # > 右对齐 → '        hi'
print("{:10}".format("hi"))        # 默认左对齐 → 'hi        '
print("{:^10}".format("hi"))       # ^ 居中 → '    hi    '

# 填充（填充字符 + 对齐符号 + 宽度）
print("{:*>10}".format("hi"))      # * 填充，> 右对齐 → '********hi'
print("{:*<10}".format("hi"))      # * 填充，< 左对齐 → 'hi********'
print("{:*^10}".format("hi"))      # * 填充，^ 居中 → '****hi****'

# 千位分隔符（,）
print("{:,}".format(1000000))      # , 添加千位分隔符 → 1,000,000

# 百分比（.数字%）
print("{:.1%}".format(0.25))       # .1% 表示保留1位小数，乘以100加%符号 → 25.0%
```



## 4. f-string 方法 🔥

f-string 是 Python 3.6 引入的格式化方式，语法最简洁、性能最优，推荐使用！🚀

### 4.1 基本用法

在字符串前加 `f` 或 `F`，用 `{}` 嵌入变量：

```python
name = "Alice"
age = 25

# f-string 基本语法
print(f"Hello, {name}! You are {age} years old.")
# 输出：Hello, Alice! You are 25 years old.
```

### 4.2 表达式嵌入

> 💡 f-string 支持直接嵌入 Python 表达式，这是它最强大的特点！

```python
# 算术运算
a = 5
b = 3
print(f"{a} + {b} = {a + b}")  # 5 + 3 = 8

# 函数调用
words = ["hello", "world"]
print(f"Words: {words}")  # Words: ['hello', 'world']

# 条件表达式
age = 20
status = "adult" if age >= 18 else "minor"
print(f"Status: {status}")  # Status: adult

# 调用字符串方法
name = "alice"
print(f"Name: {name.title()}")  # Name: Alice
```

### 4.3 格式规格

> 💡 用法和 format 方法一致，可以参考上面说明

```python
# 浮点数精度（:.数字f）
pi = 3.14159
print(f"Pi: {pi:.2f}")  # Pi: 3.14

# 千位分隔符（,）
print(f"Number: {1000000:,}")  # Number: 1,000,000

# 百分比（.数字%）
print(f"Percent: {0.25:.1%}")  # Percent: 25.0%

# 进制转换（:#x 十六进制，:#b 二进制）
print(f"Hex: {255:#x}")  # Hex: 0xff
print(f"Bin: {255:#b}")  # Bin: 0b11111111
```

### 4.4 对齐与填充

> 💡 用法和 format 方法一致，可以参考上面说明

```python
# 对齐方式（:数字 默认左对齐，:>数字 右对齐，:^数字 居中）
print(f"{'hi':>10}")   # 右对齐 → '        hi'
print(f"{'hi':<10}")   # 左对齐 → 'hi        '
print(f"{'hi':^10}")   # 居中 → '    hi    '

# 填充字符（填充字符 + 对齐符号 + 宽度）
print(f"{'hi':*>10}")  # * 填充，右对齐 → '********hi'
print(f"{'hi':*<10}")  # * 填充，左对齐 → 'hi********'
print(f"{'hi':*^10}")  # * 填充，居中 → '****hi****'

# 数字填充
print(f"{42:05d}")  # 5位数字，不足补0 → 00042
print(f"{42:+5d}")  # 显示正负号 → '  +42'
```



### 4.2 表达式嵌入



### 4.3 格式规格



### 4.4 对齐与填充



## 5. 两者对比 ⚖️



## 6. 总结 📌

---

最后更新时间：2026-04-12
