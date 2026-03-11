# P1F-Python控制结构详解-条件与循环

## 📋 目录

- [1. 概述](#1-概述)
- [2. 条件语句](#2-条件语句)
- [3. 循环语句](#3-循环语句)
- [4. 循环控制](#4-循环控制)
- [5. 实际应用](#5-实际应用)

## 1. 概述

控制结构是编程的核心，它决定了程序的执行流程。Python提供了条件语句和循环语句来控制程序的执行路径。

💡 **学习目标：**

- 掌握if-elif-else条件语句的使用
- 理解for循环和while循环的区别
- 学会使用break、continue、pass控制循环
- 能够编写实用的控制结构程序

## 2. 条件语句

### 2.1 基本if语句

```python
# 基本if语句
age = 18
if age >= 18:
    print("成年人")
else:
    print("未成年人")

# 输出: 成年人
```

### 2.2 多条件判断

```python
# 成绩等级判断
score = 85
if score >= 90:
    grade = "优秀"
elif score >= 80:
    grade = "良好"
elif score >= 70:
    grade = "中等"
elif score >= 60:
    grade = "及格"
else:
    grade = "不及格"

print(f"成绩: {score}, 等级: {grade}")
# 输出: 成绩: 85, 等级: 良好
```

### 2.3 逻辑运算符

```python
# 逻辑运算符使用
username = "admin"
password = "123456"
is_logged_in = True

# and: 两个条件都为True
if username == "admin" and password == "123456":
    print("登录成功")

# or: 至少一个条件为True
if is_logged_in or username == "admin":
    print("有权限访问")

# not: 条件取反
if not is_logged_in:
    print("请先登录")
```

### 2.4 三元运算符

```python
# 三元运算符: 值1 if 条件 else 值2
age = 20
status = "成年人" if age >= 18 else "未成年人"
print(status)  # 输出: 成年人

# 比较两个数的大小
a, b = 10, 20
max_value = a if a > b else b
print(f"较大的数是: {max_value}")  # 输出: 较大的数是: 20
```

## 3. 循环语句

### 3.1 for循环

```python
# 遍历列表
fruits = ["苹果", "香蕉", "橙子"]
for fruit in fruits:
    print(f"我喜欢{fruit}")

# 输出:
# 我喜欢苹果
# 我喜欢香蕉
# 我喜欢橙子

# 使用range()生成数字序列
for i in range(5):
    print(f"数字: {i}")

# 输出: 0, 1, 2, 3, 4
```

### 3.2 while循环

```python
# 计数器循环
count = 0
while count < 3:
    print(f"计数: {count}")
    count += 1

# 输出:
# 计数: 0
# 计数: 1
# 计数: 2

# 用户输入循环
# number = int(input("请输入一个数字: "))
# while number != 0:
#     print(f"你输入了: {number}")
#     number = int(input("请输入一个数字 (输入0退出): "))
```

### 3.3 嵌套循环

```python
# 打印乘法表
for i in range(1, 4):  # 1, 2, 3
    for j in range(1, 4):  # 1, 2, 3
        print(f"{i} × {j} = {i * j}", end="  ")
    print()  # 换行

# 输出:
# 1 × 1 = 1  1 × 2 = 2  1 × 3 = 3
# 2 × 1 = 2  2 × 2 = 4  2 × 3 = 6
# 3 × 1 = 3  3 × 2 = 6  3 × 3 = 9
```

### 3.4 循环与else

```python
# for-else: 循环正常结束时执行else
numbers = [1, 2, 3, 4, 5]
for num in numbers:
    if num == 3:
        print(f"找到数字: {num}")
        break
else:
    print("没有找到数字3")

# while-else: 条件为False时执行else
count = 0
while count < 3:
    print(f"计数: {count}")
    count += 1
else:
    print("循环结束")
```

## 4. 循环控制

### 4.1 break语句

```python
# 找到第一个偶数就停止
numbers = [1, 3, 5, 8, 9, 10]
for num in numbers:
    if num % 2 == 0:
        print(f"找到第一个偶数: {num}")
        break
    print(f"{num} 是奇数")

# 输出:
# 1 是奇数
# 3 是奇数
# 5 是奇数
# 找到第一个偶数: 8
```

### 4.2 continue语句

```python
# 只打印奇数
for i in range(1, 6):
    if i % 2 == 0:
        continue  # 跳过偶数
    print(f"奇数: {i}")

# 输出:
# 奇数: 1
# 奇数: 3
# 奇数: 5
```

### 4.3 pass语句

```python
# pass作为占位符，什么都不做
for i in range(3):
    if i == 1:
        pass  # 什么都不做，但语法需要
    else:
        print(f"数字: {i}")

# 输出:
# 数字: 0
# 数字: 2

# 在函数中使用pass
def future_function():
    pass  # 暂时不实现，避免语法错误
```

## 5. 实际应用

### 5.1 猜数字游戏

```python
import random

# 猜数字游戏
def guess_number():
    target = random.randint(1, 100)
    attempts = 0
    max_attempts = 7
    
    print("欢迎来到猜数字游戏！")
    print("我想了一个1到100之间的数字，你能猜出来吗？")
    
    while attempts < max_attempts:
        try:
            guess = int(input(f"第{attempts + 1}次猜测，请输入数字: "))
            attempts += 1
            
            if guess == target:
                print(f"🎉 恭喜你！猜对了！用了{attempts}次")
                break
            elif guess < target:
                print("太小了，再试试！")
            else:
                print("太大了，再试试！")
                
        except ValueError:
            print("请输入有效的数字！")
            attempts -= 1  # 不计入尝试次数
    else:
        print(f"游戏结束！正确答案是: {target}")

# 运行游戏
# guess_number()
```

### 5.2 数据统计

```python
# 学生成绩统计
scores = [85, 92, 78, 96, 88, 76, 91, 83, 89, 94]

# 计算平均分
total = 0
for score in scores:
    total += score
average = total / len(scores)

# 统计等级分布
excellent = good = medium = pass_grade = fail = 0

for score in scores:
    if score >= 90:
        excellent += 1
    elif score >= 80:
        good += 1
    elif score >= 70:
        medium += 1
    elif score >= 60:
        pass_grade += 1
    else:
        fail += 1

print(f"平均分: {average:.2f}")
print(f"优秀(90+): {excellent}人")
print(f"良好(80-89): {good}人")
print(f"中等(70-79): {medium}人")
print(f"及格(60-69): {pass_grade}人")
print(f"不及格(60-): {fail}人")
```

### 5.3 查找算法

```python
# 线性查找函数
def linear_search(numbers, target):
    for i, num in enumerate(numbers):
        if num == target:
            return i  # 返回索引
    return -1  # 未找到

# 测试查找
data = [10, 25, 30, 45, 50, 60, 75, 80]
search_value = 45

index = linear_search(data, search_value)
if index != -1:
    print(f"找到数字 {search_value}，位置在索引 {index}")
else:
    print(f"数字 {search_value} 不存在")
```

## 学习要点总结

🎯 **学习要点总结：**

- **条件语句**：if-elif-else实现分支逻辑，三元运算符简化条件赋值
- **循环语句**：for循环遍历序列，while循环基于条件重复执行
- **循环控制**：break跳出循环，continue跳过当前迭代，pass占位符
- **实际应用**：结合具体问题练习控制结构的综合使用

## 练习建议

📚 **练习建议：**

1. 编写一个简单的计算器程序
2. 实现一个简单的文本菜单系统
3. 创建一个数字序列生成器
4. 编写一个简单的数据验证程序

---

**厦门工学院人工智能创作坊 --郑恩赐**
