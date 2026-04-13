# P2H-Python字符串格式化完全指南-format和f-string的Python编程利器

## 📝 摘要

本文全面讲解 Python 三种字符串格式化方式：% 格式化（旧式）、format 方法（新式）和 f-string（现代）。通过对比分析，帮助读者掌握从基础到高级的字符串处理技能，特别推荐 Python 3.6+ 的 f-string 作为首选方案，享受简洁语法和极致性能。



## 1. 概述 📚

字符串格式化是编程中最常用的操作之一，Python 提供了三种格式化方式，各有特点和适用场景。😊

从 Python 诞生之初的 `%` 格式化，到 Python 2.6 引入的 `format` 方法，再到 Python 3.6 推出的 `f-string`，字符串格式化工具不断演进，朝着更简洁、更强大、更高效的方向发展。🚀

本文将系统讲解这三种格式化方式，帮助你：
- 📖 理解每种方式的语法和用法
- ⚖️ 掌握它们之间的区别和优劣
- 🎯 学会在不同场景选择最佳方案
- 💡 运用最佳实践写出优雅的代码



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

> 💡 f-string 支持直接嵌入 Python 表达式，**表达式会在运行时计算，使用其最终返回值**插入到字符串中，这是它最强大的特点！

```python
# 表达式求值示例
a = 5
b = 3
print(f"{a} + {b} = {a + b}")  # 5 + 3 = 8

# 变量引用
words = ["hello", "world"]
print(f"Words: {words}")  # Words: ['hello', 'world']

# 条件表达式
age = 20
status = "adult" if age >= 18 else "minor"
print(f"Status: {status}")  # Status: adult

# 函数调用
def greet(name):
    return f"Hello, {name}!"

name = "Alice"
print(f"Message: {greet(name)}")  # Message: Hello, Alice!

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

# 进制转换（c=character字符，d=decimal十进制，x=hexadecimal十六进制，b=binary二进制，o=octal八进制）
print(f"Char: {66:#c}")  # Char: B
print(f"Dec: {255:#d}")  # Dec: 255
print(f"Hex: {255:#x}")  # Hex: 0xff
print(f"Bin: {255:#b}")  # Bin: 0b11111111
print(f"Oct: {255:#o}")  # Oct: 0o377
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
print(f"{-42:05d}") # 负数示例 → -0042（负号占一位）
print(f"{42:+5d}")  # 显示正负号 → '  +42'
print(f"{-42:+5d}") # 负数示例 → ' -42'
```

### 4.5 调试模式（= 说明符）🔍

Python 3.8 引入的 `=` 说明符是调试神器，可以同时显示变量名和值 📝

```python
name = "Alice"
score = 95.5

# 常规方式：需要手动写变量名
print(f"name={name}, score={score}")
# 输出：name=Alice, score=95.5

# 使用 = 说明符：自动显示变量名
print(f"{name=}, {score=}")
# 输出：name='Alice', score=95.5

# 表达式也可以用
x = 10
print(f"{x * 2 = }")
# 输出：x * 2 = 20
```

> 💡 这个功能对于调试代码特别方便，一行代码就能看到变量名和值！

### 4.6 字典与对象访问 📂

f-string 可以直接访问字典和对象的属性 👀

```python
# 访问字典
user_info = {"name": "Bob", "id": 123}
print(f"User: {user_info['name']}, ID: {user_info['id']}")
# 输出：User: Bob, ID: 123

# 访问对象属性
class User:
    def __init__(self, name):
        self.name = name

user = User("Charlie")
print(f"Object name: {user.name}")
# 输出：Object name: Charlie
```

### 4.7 多行 f-string 📄

用三引号 `"""` 或 `'''` 创建多行字符串 🖊️

```python
name = "Alice"
age = 25

# 使用三引号
bio = f"""
    Name: {name}
    Age: {age}
    Profession: Python Developer
"""

print(bio)
# 输出：
#
#     Name: Alice
#     Age: 25
#     Profession: Python Developer
```

### 4.8 转义字符 🎯

想在 f-string 中显示花括号或引号需要特殊处理 ⚠️

```python
# 显示花括号：用双花括号 {{ }}
print(f"使用花括号: {{ }}")
# 输出：使用花括号: { }

# 显示双引号：外层用单引号
print(f'双引号: "hello"')
# 输出：双引号: "hello"

# 显示单引号：外层用双引号
print(f"单引号: 'hello'")
# 输出：单引号: 'hello'
```

> 💡 注意：f-string 的花括号内不能使用反斜杠 `\` 转义！

> 📖 想了解更多转义字符知识，请阅读：[Python转义字符完全指南](https://juejin.cn/post/7564634569261989951)

### 4.9 日期时间格式化 📅

f-string 可以直接格式化 datetime 对象 🕐

```python
from datetime import datetime

now = datetime.now()

# 完整日期时间
print(f"当前时间：{now:%Y-%m-%d %H:%M:%S}")
# 输出：当前时间：2024-05-20 14:30:00

# 仅日期
print(f"今日日期：{now:%Y年%m月%d日}")
# 输出：今日日期：2024年05月20日

# 星期几
print(f"今天是：{now:%A}")
# 输出：今天是：Monday（英文）

print(f"今天是：{now:%w}")
# 输出：今天是：1（数字，0为周日）
```



## 5. 两者对比 ⚖️

### 5.1 语法对比 📊

| 特性 | format 方法 | f-string |
|------|-------------|----------|
| **语法** | `"Hello, {}".format(name)` | `f"Hello, {name}"` |
| **变量嵌入** | 需要传参 | 直接嵌入 |
| **表达式支持** | 有限 | 完整支持 |
| **可读性** | 较好 | 最佳 |
| **Python版本** | 2.6+ | 3.6+ |

### 5.2 性能对比 🚀

f-string 是三者中性能最优的！💪

| 方法 | 相对速度 | 说明 |
|------|----------|------|
| **f-string** | 100%（最快） | 编译期直接解析，运行时直接求值 |
| **format 方法** | 约 50-70% | 需要运行时解析模板 |
| **% 格式化** | 约 30-50% | 最慢，已不推荐 |

> 💡 实测数据显示：f-string 比 format 方法快约 30-50%，比 % 格式化快 2-3 倍！

### 5.3 使用场景对比 🎯

**什么时候用 f-string？** ✅
- Python 3.6+ 项目
- 需要嵌入表达式计算
- 追求代码简洁和可读性
- 性能敏感的场景（如日志、循环）

**什么时候用 format 方法？** ✅
- 需要兼容 Python 3.5 及以下
- 模板需要复用多次
- 动态字段名（如 `"{data[key]}".format(data=data, key=key)`）
- 模板来自外部（配置文件、用户输入）

**什么时候用 % 格式化？** ❌
- 维护 legacy 代码
- 新项目不推荐！

### 5.4 代码示例对比 📝

```python
name = "Alice"
age = 25

# f-string（推荐）
print(f"{name} is {age} years old")

# format 方法
print("{} is {} years old".format(name, age))
print("{0} is {1} years old".format(name, age))
print("{name} is {age} years old".format(name=name, age=age))

# % 格式化（不推荐）
print("%s is %d years old" % (name, age))
```

### 5.5 选择建议 💡

> 🏆 **新项目首选 f-string**，它是 Python 3.6+ 的最佳实践！
> 
> ⚠️ **需要兼容旧版本时用 format 方法**
> 
> 🚫 **避免使用 % 格式化**（除非维护老代码）



## 6. 总结 📌

通过本文的学习，我们掌握了 Python 三种字符串格式化方式：😊

### 6.1 核心要点回顾 📝

| 格式化方式 | 推荐指数 | 适用场景 | 核心特点 |
|-----------|---------|---------|---------|
| **f-string** | ⭐⭐⭐⭐⭐ | Python 3.6+ 项目 | 语法简洁、性能最优、支持表达式 |
| **format 方法** | ⭐⭐⭐⭐ | 兼容旧版本、动态模板 | 功能强大、灵活可控 |
| **% 格式化** | ⭐⭐ | 维护 legacy 代码 | 历史悠久、已不推荐 |

### 6.2 最佳实践建议 💡

**✅ 应该做的：**
- 🏆 **新项目无条件使用 f-string**，享受简洁语法和极致性能
- 📝 **复杂格式化使用 format 方法**，如动态字段、模板复用
- 🐛 **调试时善用 `=` 说明符**，如 `f"{x=}"` 快速查看变量值
- 🎯 **统一团队代码风格**，保持项目一致性

**❌ 不应该做的：**
- 🚫 **避免在 f-string 花括号内使用反斜杠** `\` 转义
- 🚫 **不要将用户输入直接用于 f-string**，防止代码注入风险
- 🚫 **不要在生产环境遗留 % 格式化代码**，逐步迁移到现代方式

### 6.3 学习路径建议 🗺️

如果你是 Python 初学者，建议按以下顺序学习：😊

1. **先掌握 f-string 基础** — 满足 90% 的日常需求
2. **了解 format 方法** — 应对兼容性和动态场景
3. **认识 % 格式化** — 能读懂老代码即可

### 6.4 下一步学习 📚

掌握了字符串格式化后，你可以继续学习：😊

- 📖 [Python转义字符完全指南](https://juejin.cn/post/7564634569261989951) — 深入了解 `\n`、 `\t` 等特殊字符
- 📖 [Python字符串方法完全指南](https://juejin.cn/post/7627870163740753970) — 学习 split、join、replace 等方法
- 📖 [Python正则表达式](https://juejin.cn/post/7567769662478761993) — 掌握强大的模式匹配能力

> 🎉 **恭喜！你已经掌握了 Python 字符串格式化的精髓！**

---

最后更新时间：2026-04-13
