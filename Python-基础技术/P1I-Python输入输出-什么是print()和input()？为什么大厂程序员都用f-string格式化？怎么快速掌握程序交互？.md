# P1I-Python输入输出-什么是print()和input()？为什么大厂程序员都用f-string格式化？怎么快速掌握程序交互？

## 📝 摘要

面向零基础，系统讲解 Python 输入输出核心：`print()` 输出、`input()` 输入、三种格式化方法（`%`、`format()`、f-string）。通过生活化比喻与实战对比，掌握程序交互基础。

---

## 目录

- [1. 前置知识点](#1-前置知识点)
- [2. 快速上手（3 分钟）](#2-快速上手3-分钟)
- [3. print() 函数详解（输出（output（输出）））](#3-print-函数详解输出output输出)
- [4. input() 函数详解（输入（input（输入）））](#4-input-函数详解输入input输入)
- [5. 格式化输出（formatted output（格式化输出））](#5-格式化输出formatted-output格式化输出)
  - [5.1 使用 `%` 操作符格式化](#51-使用--操作符格式化)
  - [5.2 使用 `format()` 方法格式化](#52-使用-format-方法格式化)
  - [5.3 使用 f-string 格式化（推荐）](#53-使用-f-string-格式化推荐)
- [6. 输入输出实战应用](#6-输入输出实战应用)
- [7. 常见错误与对比修正](#7-常见错误与对比修正)
- [8. 选择建议与实践流程](#8-选择建议与实践流程)
- [9. 📚 参考资料与学习资源](#9-参考资料与学习资源)
- [10. 总结](#10-总结)

---

## 1. 前置知识点

在深入学习 Python 输入输出之前，你需要了解以下基础概念：

- **字符串（string（字符串））**：用于表示文本数据，可以用单引号、双引号或三引号创建
- **变量（variable（变量））**：用于存储数据的容器，就像生活中的 **盒子**，可以在里面存放不同的物品
- **函数（function（函数））**：一段可重复使用的代码块，`print()` 和 `input()` 都是 Python 内置函数（built-in functions（内置函数））
- **类型转换（type conversion（类型转换））**：将一种数据类型转换为另一种类型，例如将字符串 `"25"` 转换为整数 `25`

---

## 2. 快速上手（3 分钟）
<p align="right"><span style="background:#e53935;color:#fff;padding:2px 6px;border-radius:4px">🔥 Must（必做实践）｜依赖：Python 3.6+</span></p>

目的：用一个最小示例快速了解输入输出的基本用法——

- **输出**：使用 `print()` 显示信息到控制台
- **输入**：使用 `input()` 获取用户输入
- **格式化**：使用 f-string 将变量插入字符串

```python
# 输出信息：就像在屏幕上显示文字
print("欢迎来到 Python 世界！")
print("Hello", "World")  # 多个参数用空格分隔

# 获取用户输入：就像询问用户并等待回答
name = input("请输入您的名字：")
print(f"您好，{name}！")  # 使用 f-string 格式化输出

# 输入数字并计算：注意需要类型转换
age = int(input("请输入您的年龄："))
print(f"您今年 {age} 岁，明年将 {age + 1} 岁")
```

输出结果（假设用户输入 "张三" 和 "25"）：

```text
欢迎来到 Python 世界！
Hello World
请输入您的名字：张三
您好，张三！
请输入您的年龄：25
您今年 25 岁，明年将 26 岁
```

**输入输出的价值：让程序能够与用户互动**

输入输出就像程序与用户之间的 **对话桥梁**，让程序不再是"自言自语"，而是能够：
- 向用户展示信息和结果
- 接收用户的指令和数据
- 实现真正的交互式程序

---

## 3. print() 函数详解（输出（output（输出）））
<p align="right"><span style="background:#e53935;color:#fff;padding:2px 6px;border-radius:4px">🔥 Must（必做实践）｜依赖：任意 Python 3 版本</span></p>

`print()` 函数就像程序的 **嘴巴**，用于将信息显示在屏幕上，让程序能够与用户交流。

### 3.1 基本用法

**`print()` 函数的基本语法**：

```python
print(value1, value2, ..., sep=' ', end='\n', file=sys.stdout, flush=False)
```

**最简单的用法**：直接输出文本或变量

```python
# 输出字符串
print("Hello, Python!")
print(123)  # 输出数字
print(3.14)  # 输出浮点数

# 输出变量
name = "张三"
print(name)  # 输出：张三
```

输出结果：

```text
Hello, Python!
123
3.14
张三
```

### 3.2 多个参数输出

`print()` 可以接受多个参数（arguments（参数）），默认用空格分隔：

```python
print("Hello", "World", "Python")  # 多个参数，默认空格分隔
print("姓名：", "张三", "年龄：", 25)  # 混合类型也可以
```

输出结果：

```text
Hello World Python
姓名： 张三 年龄： 25
```

**生活化比喻**：多个参数就像说一句话中的多个词语，`print()` 会自动在它们之间加上空格，就像说话时的停顿。

### 3.3 常用参数：`sep` 和 `end`

**`sep` 参数（separator（分隔符））**：指定多个参数之间的分隔符，默认为空格

```python
# 使用默认分隔符（空格）
print("a", "b", "c")  # 输出：a b c

# 自定义分隔符
print("a", "b", "c", sep="-")  # 输出：a-b-c
print("2025", "11", "02", sep="/")  # 输出：2025/11/02
print("姓名", "张三", sep="：")  # 输出：姓名：张三
```

输出结果：

```text
a b c
a-b-c
2025/11/02
姓名：张三
```

**`end` 参数**：指定输出结束时的字符，默认为换行符 `\n`

```python
# 默认换行
print("第一行")
print("第二行")

# 不换行，使用空格结尾
print("Hello", end=" ")
print("World")

# 不换行，使用其他字符结尾
print("加载中", end="...")
print("完成")
```

输出结果：

```text
第一行
第二行
Hello World
加载中...完成
```

**实际应用场景**：进度条显示

```python
print("下载进度：", end="")
for i in range(5):
    print(".", end="", flush=True)  # flush=True 立即刷新输出
    import time
    time.sleep(0.5)  # 模拟下载过程
print(" 完成！")
```

输出结果（动态显示）：

```text
下载进度：..... 完成！
```

### 3.4 输出不同类型的数据

`print()` 可以输出任何类型的数据，Python 会自动转换为字符串显示：

```python
# 输出不同类型
print("字符串：", "Hello")  # 字符串
print("整数：", 100)  # 整数
print("浮点数：", 3.14)  # 浮点数
print("布尔值：", True, False)  # 布尔值
print("列表：", [1, 2, 3])  # 列表
print("字典：", {"name": "张三", "age": 25})  # 字典
```

输出结果：

```text
字符串： Hello
整数： 100
浮点数： 3.14
布尔值： True False
列表： [1, 2, 3]
字典： {'name': '张三', 'age': 25}
```

### 3.5 对比示例：使用 `print()` vs 不使用 `print()`

**对比目的**：展示 `print()` 函数在程序交互中的重要性

```python
# ✅ 使用 print() 函数（清晰直观）
name = "张三"
age = 25
print(f"姓名：{name}，年龄：{age}")  # 输出：姓名：张三，年龄：25

# 可以输出多行信息
print("=== 用户信息 ===")
print(f"姓名：{name}")
print(f"年龄：{age}")
```

输出结果：

```text
姓名：张三，年龄：25
=== 用户信息 ===
姓名：张三
年龄：25
```

```python
# ❌ 不使用 print() 函数（程序无法与用户交互）
name = "张三"
age = 25
# 程序执行了，但用户看不到任何信息
# 程序就像"沉默"了，用户不知道程序在做什么

# 即使计算了结果，也无法显示
result = age + 1
# 用户看不到 result 的值
```

**对比结论**：`print()` 函数是程序与用户交互的基础工具。没有它，程序就像"哑巴"一样，无法向用户展示任何信息。使用 `print()` 可以让程序"开口说话"，将计算结果、状态信息等清晰地展示给用户。

---

## 4. input() 函数详解（输入（input（输入）））
<p align="right"><span style="background:#e53935;color:#fff;padding:2px 6px;border-radius:4px">🔥 Must（必做实践）｜依赖：任意 Python 3 版本</span></p>

`input()` 函数就像程序的 **耳朵**，用于接收用户的输入，让程序能够"听到"用户的指令和数据。

### 4.1 基本用法

**`input()` 函数的基本语法**：

```python
input([prompt])
```

**`prompt` 参数（提示信息（prompt（提示信息）））**：可选参数，用于显示提示信息，告诉用户应该输入什么

```python
# 基本用法：不带提示信息
name = input()  # 程序会等待用户输入，但没有任何提示

# 推荐用法：带提示信息
name = input("请输入您的名字：")  # 显示提示信息，用户体验更好
print(f"您好，{name}！")
```

运行示例（用户输入 "张三"）：

```text
请输入您的名字：张三
您好，张三！
```

**生活化比喻**：`input()` 函数就像餐厅服务员询问顾客："请问您要点什么菜？"（提示信息），然后等待顾客回答（用户输入）。

### 4.2 返回值类型

**重要特性**：`input()` 函数**始终返回字符串类型**（string（字符串）），即使输入的是数字。

```python
# 输入数字，但返回的是字符串
age_str = input("请输入您的年龄：")
print(type(age_str))  # 输出：<class 'str'>
print(age_str)  # 输出：25（但这是字符串 "25"，不是数字 25）

# 如果需要进行数学运算，必须进行类型转换
age = int(age_str)  # 将字符串转换为整数
print(f"明年您将 {age + 1} 岁")  # 现在可以进行数学运算了
```

运行示例（用户输入 "25"）：

```text
请输入您的年龄：25
<class 'str'>
25
明年您将 26 岁
```

### 4.3 类型转换（type conversion（类型转换））

由于 `input()` 返回的是字符串，如果需要进行数值计算，必须进行类型转换：

```python
# 转换为整数（integer（整数））
age = int(input("请输入您的年龄："))
print(f"您今年 {age} 岁")

# 转换为浮点数（float（浮点数））
height = float(input("请输入您的身高（米）："))
print(f"您的身高是 {height} 米")

# 转换为布尔值（boolean（布尔值））
is_student = input("您是学生吗？（输入 yes 或 no）：")
if is_student.lower() == "yes":
    is_student_bool = True
else:
    is_student_bool = False
print(f"学生状态：{is_student_bool}")
```

运行示例：

```text
请输入您的年龄：25
您今年 25 岁
请输入您的身高（米）：1.75
您的身高是 1.75 米
您是学生吗？（输入 yes 或 no）：yes
学生状态：True
```

### 4.4 常见类型转换方法

| 转换函数 | 功能 | 示例 |
|---------|------|------|
| `int()` | 将字符串转换为整数 | `int("25")` → `25` |
| `float()` | 将字符串转换为浮点数 | `float("3.14")` → `3.14` |
| `str()` | 将其他类型转换为字符串（通常不需要，因为 `input()` 已返回字符串） | `str(25)` → `"25"` |
| `bool()` | 将值转换为布尔值 | `bool("True")` → `True` |

**注意事项**：如果输入的字符串无法转换为目标类型，会抛出异常（exception（异常））：

```python
# ❌ 错误示例：输入非数字字符串时转换失败
age = int(input("请输入您的年龄："))  # 如果用户输入 "abc"，会报错
# ValueError: invalid literal for int() with base 10: 'abc'
```

**正确的做法**：使用异常处理（try-except（尝试-捕获））或验证输入

```python
# ✅ 正确做法：使用异常处理
try:
    age = int(input("请输入您的年龄："))
    print(f"您今年 {age} 岁")
except ValueError:
    print("输入错误，请输入有效的数字！")
```

### 4.5 输入多个值

可以通过分隔符将用户输入拆分成多个值：

```python
# 方法 1：使用 split() 方法（默认按空格分隔）
data = input("请输入姓名和年龄（用空格分隔）：")
parts = data.split()  # 按空格分割
name = parts[0]
age = int(parts[1])
print(f"姓名：{name}，年龄：{age}")

# 方法 2：使用指定的分隔符
data = input("请输入姓名和年龄（用逗号分隔）：")
parts = data.split(",")  # 按逗号分割
name = parts[0].strip()  # 去除首尾空格
age = int(parts[1].strip())
print(f"姓名：{name}，年龄：{age}")

# 方法 3：分别输入（推荐，更清晰）
name = input("请输入您的姓名：")
age = int(input("请输入您的年龄："))
print(f"姓名：{name}，年龄：{age}")
```

运行示例（方法 3）：

```text
请输入您的姓名：张三
请输入您的年龄：25
姓名：张三，年龄：25
```

### 4.6 对比示例：使用 `input()` vs 不使用 `input()`

**对比目的**：展示 `input()` 函数如何让程序变得交互式

```python
# ✅ 使用 input() 函数（交互式，灵活）
name = input("请输入您的名字：")
age = int(input("请输入您的年龄："))
print(f"您好，{name}！您今年 {age} 岁。")
# 每次运行程序，都可以输入不同的值
```

运行示例：

```text
请输入您的名字：李四
请输入您的年龄：30
您好，李四！您今年 30 岁。
```

```python
# ❌ 不使用 input() 函数（硬编码，不灵活）
name = "张三"  # 值固定，无法改变
age = 25  # 值固定，无法改变
print(f"您好，{name}！您今年 {age} 岁。")
# 每次运行程序，输出都是一样的
# 程序无法根据用户的需求动态调整
```

输出结果：

```text
您好，张三！您今年 25 岁。
（无论运行多少次，结果都一样）
```

**对比结论**：`input()` 函数让程序从"死板的剧本"变成了"灵活的对话"。使用 `input()`，程序可以根据用户的输入做出不同的响应，实现真正的交互式程序。没有它，程序只能按照预设的"剧本"执行，无法适应不同的用户需求。

---

## 5. 格式化输出（formatted output（格式化输出））
<p align="right"><span style="background:#e53935;color:#fff;padding:2px 6px;border-radius:4px">🔥 Must（必做实践）｜依赖：Python 3.6+（f-string）</span></p>

格式化输出就像 **排版工具**，用于将变量值插入到字符串中，让输出内容更加美观和易读。Python 提供了三种主要的格式化方法，每种方法都有其适用场景。

**生活化比喻**：格式化输出就像填写表格，将变量值填入模板中的空白处，最终生成格式整齐的文档。

### 5.1 使用 `%` 操作符格式化
<p align="right"><span style="background:#fb8c00;color:#fff;padding:2px 6px;border-radius:4px">⚙️ Should（建议实践）｜依赖：任意 Python 3 版本</span></p>

`%` 操作符格式化类似于 C 语言的 `printf`，使用占位符（placeholder（占位符））表示变量位置。

**基本语法**：

```python
"格式字符串" % (值1, 值2, ...)
```

**常用格式化符号**：

| 符号 | 含义 | 示例 |
|------|------|------|
| `%s` | 字符串（string（字符串）） | `"姓名：%s" % "张三"` → `"姓名：张三"` |
| `%d` | 整数（decimal（十进制）） | `"年龄：%d" % 25` → `"年龄：25"` |
| `%f` | 浮点数（float（浮点数）） | `"价格：%f" % 99.99` → `"价格：99.990000"` |
| `%.2f` | 保留 2 位小数的浮点数 | `"价格：%.2f" % 99.99` → `"价格：99.99"` |
| `%x` | 十六进制整数 | `"十六进制：%x" % 255` → `"十六进制：ff"` |

**示例代码**：

```python
name = "张三"
age = 25
height = 1.75
price = 99.99

# 单个变量
print("姓名：%s" % name)  # 输出：姓名：张三

# 多个变量（使用元组）
print("姓名：%s，年龄：%d 岁" % (name, age))  # 输出：姓名：张三，年龄：25 岁

# 浮点数格式化
print("身高：%.2f 米" % height)  # 输出：身高：1.75 米
print("价格：%.2f 元" % price)  # 输出：价格：99.99 元
```

输出结果：

```text
姓名：张三
姓名：张三，年龄：25 岁
身高：1.75 米
价格：99.99 元
```

**优点**：语法简洁，类似 C 语言，适合从 C 语言转过来的开发者  
**缺点**：可读性较差，参数顺序容易出错，Python 3 中不推荐使用（但仍支持）

### 5.2 使用 `format()` 方法格式化
<p align="right"><span style="background:#fb8c00;color:#fff;padding:2px 6px;border-radius:4px">⚙️ Should（建议实践）｜依赖：任意 Python 3 版本</span></p>

`format()` 方法提供了更灵活、更强大的字符串格式化方式，使用花括号 `{}` 作为占位符。

**基本语法**：

```python
"格式字符串".format(值1, 值2, ...)
```

**示例代码**：

```python
name = "张三"
age = 25
height = 1.75

# 方法 1：按顺序填充（位置参数（positional arguments（位置参数）））
print("姓名：{}，年龄：{} 岁".format(name, age))  # 输出：姓名：张三，年龄：25 岁

# 方法 2：使用索引指定位置
print("姓名：{0}，年龄：{1} 岁，姓名重复：{0}".format(name, age))
# 输出：姓名：张三，年龄：25 岁，姓名重复：张三

# 方法 3：使用命名参数（关键字参数（keyword arguments（关键字参数）））
print("姓名：{name}，年龄：{age} 岁".format(name="李四", age=30))
# 输出：姓名：李四，年龄：30 岁

# 方法 4：格式化数字（控制小数位数）
print("身高：{:.2f} 米".format(height))  # 输出：身高：1.75 米
print("价格：{:.2f} 元".format(99.99))  # 输出：价格：99.99 元

# 方法 5：对齐和填充
print("|{:<10}|".format("左对齐"))  # 输出：|左对齐      |
print("|{:>10}|".format("右对齐"))  # 输出：|      右对齐|
print("|{:^10}|".format("居中"))    # 输出：|    居中    |
```

输出结果：

```text
姓名：张三，年龄：25 岁
姓名：张三，年龄：25 岁，姓名重复：张三
姓名：李四，年龄：30 岁
身高：1.75 米
价格：99.99 元
|左对齐      |
|      右对齐|
|    居中    |
```

**优点**：功能强大、灵活，支持索引和命名参数  
**缺点**：语法相对复杂，Python 3.6+ 后推荐使用 f-string

### 5.3 使用 f-string 格式化（推荐）
<p align="right"><span style="background:#e53935;color:#fff;padding:2px 6px;border-radius:4px">🔥 Must（必做实践）｜依赖：Python 3.6+</span></p>

f-string（formatted string literal（格式化字符串字面量））是 Python 3.6 引入的格式化方法，使用最简洁、最直观，**推荐优先使用**。

**基本语法**：在字符串前加上 `f` 或 `F`，然后在花括号 `{}` 中直接写入变量或表达式

```python
f"格式字符串"
```

**示例代码**：

```python
name = "张三"
age = 25
height = 1.75
price = 99.99

# 基本用法：直接嵌入变量
print(f"姓名：{name}，年龄：{age} 岁")  # 输出：姓名：张三，年龄：25 岁

# 支持表达式计算
print(f"明年将 {age + 1} 岁")  # 输出：明年将 26 岁
print(f"身高：{height * 100} 厘米")  # 输出：身高：175.0 厘米

# 格式化数字（控制小数位数）
print(f"身高：{height:.2f} 米")  # 输出：身高：1.75 米
print(f"价格：{price:.2f} 元")  # 输出：价格：99.99 元

# 对齐和填充
print(f"|{name:<10}|")  # 输出：|张三        |
print(f"|{name:>10}|")  # 输出：|        张三|
print(f"|{name:^10}|")  # 输出：|    张三    |

# 千位分隔符
large_number = 1234567890
print(f"大数字：{large_number:,}")  # 输出：大数字：1,234,567,890

# 调用方法
print(f"姓名大写：{name.upper()}")  # 输出：姓名大写：张三（如果 name 包含小写字母会转大写）

# 嵌套引号
print(f'他说："我是 {name}"')  # 输出：他说："我是 张三"
```

输出结果：

```text
姓名：张三，年龄：25 岁
明年将 26 岁
身高：175.0 厘米
身高：1.75 米
价格：99.99 元
|张三        |
|        张三|
|    张三    |
大数字：1,234,567,890
姓名大写：张三
他说："我是 张三"
```

**f-string 的对比优势**：

```python
# ✅ 使用 f-string（最简洁直观）
name = "张三"
age = 25
print(f"姓名：{name}，年龄：{age} 岁")  # 一行搞定，清晰易读
```

```python
# ❌ 使用 % 操作符（较繁琐）
name = "张三"
age = 25
print("姓名：%s，年龄：%d 岁" % (name, age))  # 需要记住格式化符号
```

```python
# ❌ 使用 format() 方法（较冗长）
name = "张三"
age = 25
print("姓名：{}，年龄：{} 岁".format(name, age))  # 需要在后面列出变量
```

**对比结论**：f-string 是最现代、最简洁的格式化方法。它让代码更接近自然语言，变量名直接出现在字符串中，可读性最强。**强烈推荐在 Python 3.6+ 中使用 f-string**。

**优点**：
- 语法最简洁直观
- 可读性最强，变量名直接可见
- 支持表达式计算
- 性能最好（编译时优化）
- Python 官方推荐

**缺点**：
- 需要 Python 3.6+（但这是现在的主流版本）

---

## 6. 输入输出实战应用
<p align="right"><span style="background:#fb8c00;color:#fff;padding:2px 6px;border-radius:4px">⚙️ Should（建议实践）｜依赖：Python 3.6+</span></p>

在实际开发中，输入输出常常组合使用，实现交互式程序。以下是几个常见的实战场景：

### 6.1 用户注册信息收集

```python
# 收集用户信息并格式化输出
print("=== 用户注册 ===")
name = input("请输入您的姓名：")
age = int(input("请输入您的年龄："))
email = input("请输入您的邮箱：")

# 使用 f-string 格式化输出
print("\n注册信息确认：")
print(f"姓名：{name}")
print(f"年龄：{age} 岁")
print(f"邮箱：{email}")
print("注册成功！")
```

运行示例：

```text
=== 用户注册 ===
请输入您的姓名：张三
请输入您的年龄：25
请输入您的邮箱：zhangsan@example.com

注册信息确认：
姓名：张三
年龄：25 岁
邮箱：zhangsan@example.com
注册成功！
```

### 6.2 计算器程序

```python
# 简单的计算器
print("=== 简单计算器 ===")
num1 = float(input("请输入第一个数字："))
operator = input("请输入运算符（+、-、*、/）：")
num2 = float(input("请输入第二个数字："))

if operator == "+":
    result = num1 + num2
elif operator == "-":
    result = num1 - num2
elif operator == "*":
    result = num1 * num2
elif operator == "/":
    if num2 != 0:
        result = num1 / num2
    else:
        result = "错误：除数不能为 0"
else:
    result = "错误：不支持的运算符"

print(f"结果：{num1} {operator} {num2} = {result}")
```

运行示例：

```text
=== 简单计算器 ===
请输入第一个数字：10
请输入运算符（+、-、*、/）：+
请输入第二个数字：5
结果：10.0 + 5.0 = 15.0
```

### 6.3 格式化输出表格

```python
# 格式化输出学生成绩表
students = [
    ("张三", 85, 90, 88),
    ("李四", 92, 87, 91),
    ("王五", 78, 85, 80)
]

print("=" * 50)
print(f"{'姓名':<10} {'语文':<10} {'数学':<10} {'英语':<10} {'平均分':<10}")
print("=" * 50)

for name, chinese, math, english in students:
    avg = (chinese + math + english) / 3
    print(f"{name:<10} {chinese:<10} {math:<10} {english:<10} {avg:<10.2f}")

print("=" * 50)
```

输出结果：

```text
==================================================
姓名       语文       数学       英语       平均分      
==================================================
张三       85        90        88        87.67     
李四       92        87        91        90.00     
王五       78        85        80        81.00     
==================================================
```

### 6.4 带输入验证的程序

```python
# 输入验证示例
while True:
    try:
        age = int(input("请输入您的年龄（18-100）："))
        if 18 <= age <= 100:
            print(f"您输入的年龄是：{age} 岁")
            break
        else:
            print("年龄必须在 18-100 之间，请重新输入！")
    except ValueError:
        print("输入错误，请输入有效的数字！")
```

运行示例：

```text
请输入您的年龄（18-100）：abc
输入错误，请输入有效的数字！
请输入您的年龄（18-100）：15
年龄必须在 18-100 之间，请重新输入！
请输入您的年龄（18-100）：25
您输入的年龄是：25 岁
```

---

## 7. 常见错误与对比修正

在实际编程中，输入输出相关的常见错误及修正方法：

### 7.1 错误：忘记类型转换

**错误示例**：

```python
# ❌ 错误：直接对字符串进行数学运算
age = input("请输入您的年龄：")
next_age = age + 1  # 错误：无法将字符串和整数相加
# TypeError: can only concatenate str (not "int") to str
```

**正确做法**：

```python
# ✅ 正确：先进行类型转换
age = int(input("请输入您的年龄："))
next_age = age + 1  # 正确：整数相加
print(f"明年您将 {next_age} 岁")
```

### 7.2 错误：f-string 语法错误

**错误示例**：

```python
# ❌ 错误：忘记在字符串前加 f
name = "张三"
age = 25
print("姓名：{name}，年龄：{age} 岁")  # 输出：姓名：{name}，年龄：{age} 岁（原样输出）
```

**正确做法**：

```python
# ✅ 正确：使用 f-string
name = "张三"
age = 25
print(f"姓名：{name}，年龄：{age} 岁")  # 输出：姓名：张三，年龄：25 岁
```

### 7.3 错误：输入验证不足

**错误示例**：

```python
# ❌ 错误：没有验证输入，可能崩溃
age = int(input("请输入您的年龄："))  # 如果输入 "abc"，程序会崩溃
print(f"您今年 {age} 岁")
```

**正确做法**：

```python
# ✅ 正确：使用异常处理验证输入
while True:
    try:
        age = int(input("请输入您的年龄："))
        print(f"您今年 {age} 岁")
        break
    except ValueError:
        print("输入错误，请输入有效的数字！")
```

### 7.4 错误：格式化方法混用

**错误示例**：

```python
# ❌ 错误：f-string 中混用 % 操作符
name = "张三"
print(f"姓名：%s" % name)  # 语法错误或逻辑混乱
```

**正确做法**：

```python
# ✅ 正确：统一使用 f-string
name = "张三"
print(f"姓名：{name}")  # 简洁清晰
```

### 7.5 错误：print() 参数使用错误

**错误示例**：

```python
# ❌ 错误：sep 和 end 参数位置错误
print("Hello", "World", "sep=-")  # sep 被当作普通字符串输出
```

**正确做法**：

```python
# ✅ 正确：使用关键字参数
print("Hello", "World", sep="-")  # 输出：Hello-World
```

---

## 8. 选择建议与实践流程

### 8.1 格式化方法选择建议

**推荐优先级**：

1. **f-string（Python 3.6+）** ⭐⭐⭐⭐⭐
   - **适用场景**：所有 Python 3.6+ 项目
   - **优势**：最简洁、可读性最强、性能最好
   - **示例**：`f"姓名：{name}，年龄：{age} 岁"`

2. **format() 方法（Python 3.0+）** ⭐⭐⭐⭐
   - **适用场景**：需要 Python 3.5 及以下版本支持时
   - **优势**：功能强大、灵活
   - **示例**：`"姓名：{}，年龄：{} 岁".format(name, age)`

3. **% 操作符（不推荐）** ⭐⭐
   - **适用场景**：仅用于维护旧代码
   - **劣势**：可读性差、易出错
   - **示例**：`"姓名：%s，年龄：%d 岁" % (name, age)`

### 8.2 实践流程建议

**初学者学习路径**：

1. **第一步**：掌握 `print()` 基本用法
   - 学会输出字符串、变量
   - 理解 `sep` 和 `end` 参数

2. **第二步**：掌握 `input()` 基本用法
   - 学会获取用户输入
   - 理解类型转换的重要性

3. **第三步**：学习 f-string 格式化
   - 优先学习 f-string（Python 3.6+）
   - 掌握基本格式化和表达式计算

4. **第四步**：综合应用
   - 实现简单的交互式程序
   - 添加输入验证和错误处理

**实践项目建议**：

- **入门级**：用户信息收集程序、简单计算器
- **进阶级**：菜单驱动的交互程序、数据录入系统
- **高级**：命令行工具、交互式脚本

### 8.3 最佳实践总结

1. **始终使用 f-string**（Python 3.6+）
2. **为 `input()` 添加提示信息**，提升用户体验
3. **进行输入验证**，使用异常处理
4. **类型转换要谨慎**，确保类型匹配
5. **格式化输出要清晰**，便于用户理解

---

## 9. 📚 参考资料与学习资源

### 官方文档

- **Python 官方文档 - 内置函数**：
  - `print()` 函数：https://docs.python.org/zh-cn/3/library/functions.html#print
  - `input()` 函数：https://docs.python.org/zh-cn/3/library/functions.html#input
- **Python 官方教程 - 输入输出**：
  - https://docs.python.org/zh-cn/3/tutorial/inputoutput.html
- **PEP 498 - 格式化字符串字面量（f-string）**：
  - https://peps.python.org/pep-0498/

### 在线教程

- **Python 教程 - 廖雪峰**：
  - 输入和输出：https://www.liaoxuefeng.com/wiki/1016959663602400/1017499532944768
- **Python 3 教程 - 菜鸟教程**：
  - 输入和输出：https://www.runoob.com/python3/python3-inputoutput.html
- **Real Python - f-string 教程**：
  - https://realpython.com/python-f-strings/

### 推荐书籍

- 《Python 编程：从入门到实践》- Eric Matthes（适合零基础）
- 《Python 基础教程（第 3 版）》- Magnus Lie Hetland

### 实践平台

- **在线练习**：
  - Python Challenge：http://www.pythonchallenge.com/
  - HackerRank Python：https://www.hackerrank.com/domains/python
  - LeetCode Python 题目：https://leetcode.cn/problemset/all/

---

## 10. 总结

Python 输入输出是程序与用户交互的基础，掌握 `print()`、`input()` 和格式化输出是每个 Python 开发者的必备技能。

### 核心要点回顾

1. **`print()` 函数**：程序的"嘴巴"，用于输出信息到控制台
   - 支持多个参数，默认空格分隔
   - 使用 `sep` 参数自定义分隔符
   - 使用 `end` 参数控制结束符

2. **`input()` 函数**：程序的"耳朵"，用于接收用户输入
   - 始终返回字符串类型
   - 需要类型转换才能进行数值计算
   - 添加提示信息提升用户体验

3. **格式化输出**：让输出更美观易读
   - **推荐使用 f-string**（Python 3.6+）：最简洁、可读性最强
   - `format()` 方法：功能强大、灵活
   - `%` 操作符：不推荐，仅用于维护旧代码

### 学习建议

- **初学者**：先掌握 `print()` 和 `input()` 基本用法，然后学习 f-string 格式化
- **进阶学习**：掌握输入验证、异常处理，实现复杂的交互式程序
- **最佳实践**：始终使用 f-string，为输入添加验证，输出信息清晰明了

### 下一步学习方向

掌握了输入输出后，建议继续学习：
- **控制结构**：条件语句（if-else）、循环语句（for、while）
- **数据类型**：列表、字典、元组等数据结构
- **函数定义**：封装重复代码，提高代码复用性
- **文件操作**：读写文件，持久化存储数据

---

**记住**：编程是一个实践的过程，多写代码、多调试、多思考，才能熟练掌握。你已经掌握了 Python 输入输出的核心技能，这是迈向更高层次编程的第一步。继续加油，保持学习的热情，你一定能够成为优秀的 Python 开发者！💪✨

---

**厦门工学院人工智能创作坊 -- 郑恩赐**  
**2025 年 11 月 02 日**

