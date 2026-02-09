# 🏗️ Python类基础详解 - 从入门到精通

## 📋 目录

- [1. 什么是类](#1-什么是类)
- [2. 创建第一个类](#2-创建第一个类)
- [3. 构造函数__init__](#3-构造函数__init__)
- [4. 实例属性和方法](#4-实例属性和方法)
- [5. 类属性和类方法](#5-类属性和类方法)
- [6. 静态方法](#6-静态方法)
- [7. 属性访问控制](#7-属性访问控制)
- [8. 实际应用示例](#8-实际应用示例)
- [9. 最佳实践](#9-最佳实践)

## 1. 什么是类

### 1.1 用最简单的话说

**类就像是一个表格模板。**

比如学生信息表：
```
姓名: _______
年龄: _______
学号: _______
专业: _______
```

**类 = 表格模板**
**对象 = 填好信息的表格**

### 1.2 超级简单的例子

```python
# 第一步：制作学生信息表模板
class Student:
    """学生信息表模板"""
    pass

# 第二步：用模板制作表格
student1 = Student()  # 制作第一张表格
student2 = Student()  # 制作第二张表格

print(student1)  # 显示第一张表格
print(student2)  # 显示第二张表格
```

**运行结果：**
```
<__main__.Student object at 0x...>
<__main__.Student object at 0x...>
```

**解释：**
- `Student` = 学生信息表模板（类）
- `student1` = 用模板制作的第一张表格（对象）
- `student2` = 用模板制作的第二张表格（对象）

就像：
- 学生登记表模板 = 类
- 张三的登记表 = 对象1
- 李四的登记表 = 对象2

## 2. 创建第一个类

### 2.1 先做一个空的表格模板

```python
# 第一步：制作一个空的表格模板
class Student:
    """学生信息表模板"""
    pass

# 第二步：用模板制作表格
student1 = Student()  # 制作第一张表格
student2 = Student()  # 制作第二张表格

print(student1)  # 显示第一张表格
print(student2)  # 显示第二张表格
```

**运行结果：**
```
<__main__.Student object at 0x...>
<__main__.Student object at 0x...>
```

**说明：** 现在表格制作好了，但是还没有填写信息。

### 2.2 给表格添加空白栏

```python
class Student:
    """学生信息表模板"""
    
    def __init__(self):
        """给表格添加空白栏"""
        self.name = "未知"      # 姓名栏
        self.age = 0           # 年龄栏
        self.student_id = "未知"  # 学号栏

# 制作表格
student1 = Student()
student2 = Student()

# 看看表格的内容
print(f"表格1 - 姓名: {student1.name}, 年龄: {student1.age}")
print(f"表格2 - 姓名: {student2.name}, 年龄: {student2.age}")
```

**运行结果：**
```
表格1 - 姓名: 未知, 年龄: 0
表格2 - 姓名: 未知, 年龄: 0
```

**说明：** 现在表格有了空白栏，但都还没有填写具体信息。

## 3. 构造函数__init__

### 3.1 什么是构造函数

**构造函数就是制作表格时自动填写的代码。**

就像制作学生登记表时，会自动在表格上写上"姓名"、"年龄"等栏目。

```python
class Student:
    """学生信息表模板"""
    
    def __init__(self, name, age, student_id):
        """制作表格时自动填写"""
        print(f"正在制作 {name} 的表格")
        self.name = name           # 填写姓名栏
        self.age = age            # 填写年龄栏
        self.student_id = student_id  # 填写学号栏
        self.grades = []          # 准备成绩栏
        print(f"{name} 的表格制作完成")

# 制作表格（会自动运行__init__）
student1 = Student("张三", 20, "2024001")
student2 = Student("李四", 19, "2024002")

# 看看制作好的表格
print(f"表格1: {student1.name}, 年龄: {student1.age}")
print(f"表格2: {student2.name}, 年龄: {student2.age}")
```

**运行结果：**
```
正在制作 张三 的表格
张三 的表格制作完成
正在制作 李四 的表格
李四 的表格制作完成
表格1: 张三, 年龄: 20
表格2: 李四, 年龄: 19
```

**说明：** 每次制作表格时，`__init__`会自动运行，填写表格的基本信息。

### 3.2 给一些栏目设置默认值

有时候我们不想每次都填写所有栏目，可以设置默认值。

```python
class Book:
    """图书信息表模板"""
    
    def __init__(self, title, author, pages=100, price=0.0):
        """制作图书表格时自动填写"""
        self.title = title      # 书名栏（必须填写）
        self.author = author    # 作者栏（必须填写）
        self.pages = pages      # 页数栏（默认100页）
        self.price = price      # 价格栏（默认0元）

# 制作图书表格方式1：只填写书名和作者
book1 = Book("Python编程", "张三")
print(f"《{book1.title}》- {book1.author}, {book1.pages}页, {book1.price}元")

# 制作图书表格方式2：填写所有栏目
book2 = Book("Java编程", "李四", 200, 59.9)
print(f"《{book2.title}》- {book2.author}, {book2.pages}页, {book2.price}元")
```

**运行结果：**
```
《Python编程》- 张三, 100页, 0.0元
《Java编程》- 李四, 200页, 59.9元
```

**说明：** 
- `pages=100` 意思是如果不填写页数栏，默认写100页
- `price=0.0` 意思是如果不填写价格栏，默认写0元

## 4. 实例属性和方法

### 4.1 实例属性

实例属性属于特定的对象实例，每个对象都有自己独立的属性值。

```python
class Car:
    """汽车类 - 演示实例属性"""
    
    def __init__(self, brand, model, color, price):
        """构造函数"""
        self.brand = brand      # 品牌
        self.model = model      # 型号
        self.color = color      # 颜色
        self.price = price      # 价格
        self.mileage = 0        # 里程数
        self.is_running = False # 是否运行中

# 创建汽车对象
car1 = Car("奔驰", "C200", "黑色", 350000)
car2 = Car("宝马", "X3", "白色", 450000)

# 每个对象都有独立的属性
print(f"汽车1: {car1.brand} {car1.model}, 颜色: {car1.color}")
print(f"汽车2: {car2.brand} {car2.model}, 颜色: {car2.color}")

# 修改一个对象的属性不会影响另一个对象
car1.mileage = 10000
print(f"汽车1里程: {car1.mileage}")  # 10000
print(f"汽车2里程: {car2.mileage}")  # 0
```

### 4.2 实例方法

实例方法是定义在类中的函数，可以访问和修改实例属性。

```python
class Car:
    """汽车类 - 演示实例方法"""
    
    def __init__(self, brand, model, color, price):
        """构造函数"""
        self.brand = brand
        self.model = model
        self.color = color
        self.price = price
        self.mileage = 0
        self.is_running = False
    
    def start_engine(self):
        """启动引擎"""
        if not self.is_running:
            self.is_running = True
            print(f"{self.brand} {self.model} 引擎已启动")
        else:
            print(f"{self.brand} {self.model} 引擎已经在运行")
    
    def stop_engine(self):
        """关闭引擎"""
        if self.is_running:
            self.is_running = False
            print(f"{self.brand} {self.model} 引擎已关闭")
        else:
            print(f"{self.brand} {self.model} 引擎已经关闭")
    
    def drive(self, distance):
        """驾驶汽车"""
        if self.is_running:
            self.mileage += distance
            print(f"{self.brand} {self.model} 行驶了{distance}公里")
            print(f"总里程: {self.mileage}公里")
        else:
            print("请先启动引擎")
    
    def get_info(self):
        """获取汽车信息"""
        status = "运行中" if self.is_running else "已关闭"
        return f"{self.brand} {self.model} ({self.color}) - {status} - 里程: {self.mileage}公里"

# 使用实例方法
car = Car("特斯拉", "Model 3", "蓝色", 300000)

print(car.get_info())
car.start_engine()
car.drive(50)
car.drive(30)
car.stop_engine()
print(car.get_info())
```

## 5. 类属性和类方法

### 5.1 类属性

类属性属于类本身，所有实例共享同一个类属性。

```python
class Car:
    """汽车类 - 演示类属性"""
    
    # 类属性 - 所有实例共享
    wheels = 4
    engine_type = "内燃机"
    manufacturer = "未知制造商"
    
    def __init__(self, brand, model, color, price):
        """构造函数"""
        self.brand = brand      # 实例属性
        self.model = model      # 实例属性
        self.color = color      # 实例属性
        self.price = price      # 实例属性
    
    def get_class_info(self):
        """获取类信息"""
        return f"轮子数: {Car.wheels}, 引擎类型: {Car.engine_type}, 制造商: {Car.manufacturer}"

# 创建汽车对象
car1 = Car("奔驰", "C200", "黑色", 350000)
car2 = Car("宝马", "X3", "白色", 450000)

# 访问类属性
print(f"汽车轮子数: {Car.wheels}")
print(f"引擎类型: {Car.engine_type}")

# 通过实例访问类属性
print(car1.get_class_info())
print(car2.get_class_info())

# 修改类属性会影响所有实例
Car.wheels = 6
Car.engine_type = "电动"
print("修改类属性后:")
print(car1.get_class_info())
print(car2.get_class_info())
```

### 5.2 类方法

类方法是使用`@classmethod`装饰器定义的方法，第一个参数是类本身（通常命名为`cls`）。

```python
class Car:
    """汽车类 - 演示类方法"""
    
    wheels = 4
    manufacturer = "未知制造商"
    total_cars = 0  # 总汽车数量
    
    def __init__(self, brand, model, color, price):
        """构造函数"""
        self.brand = brand
        self.model = model
        self.color = color
        self.price = price
        Car.total_cars += 1  # 每创建一个汽车，总数+1
    
    @classmethod
    def set_manufacturer(cls, manufacturer_name):
        """设置制造商 - 类方法"""
        cls.manufacturer = manufacturer_name
        print(f"制造商已设置为: {manufacturer_name}")
    
    @classmethod
    def get_total_cars(cls):
        """获取总汽车数量 - 类方法"""
        return cls.total_cars
    
    @classmethod
    def create_tesla(cls, model, color, price):
        """创建特斯拉汽车 - 类方法"""
        return cls("特斯拉", model, color, price)
    
    def get_info(self):
        """获取汽车信息"""
        return f"{self.brand} {self.model} ({self.color}) - {self.price}元"

# 使用类方法
print(f"总汽车数: {Car.get_total_cars()}")

# 创建汽车
car1 = Car("奔驰", "C200", "黑色", 350000)
car2 = Car("宝马", "X3", "白色", 450000)

print(f"总汽车数: {Car.get_total_cars()}")

# 设置制造商
Car.set_manufacturer("德国汽车集团")

# 使用类方法创建特定品牌的汽车
tesla = Car.create_tesla("Model S", "红色", 500000)
print(tesla.get_info())
```

## 6. 静态方法

静态方法是使用`@staticmethod`装饰器定义的方法，不需要访问类或实例，可以像普通函数一样使用。

```python
class MathUtils:
    """数学工具类 - 演示静态方法"""
    
    @staticmethod
    def add(a, b):
        """加法"""
        return a + b
    
    @staticmethod
    def multiply(a, b):
        """乘法"""
        return a * b
    
    @staticmethod
    def is_even(number):
        """判断是否为偶数"""
        return number % 2 == 0
    
    @staticmethod
    def calculate_circle_area(radius):
        """计算圆的面积"""
        import math
        return math.pi * radius ** 2
    
    @staticmethod
    def calculate_distance(x1, y1, x2, y2):
        """计算两点间距离"""
        import math
        return math.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)

# 使用静态方法
print(f"5 + 3 = {MathUtils.add(5, 3)}")
print(f"4 * 6 = {MathUtils.multiply(4, 6)}")
print(f"8是偶数吗: {MathUtils.is_even(8)}")
print(f"半径为5的圆面积: {MathUtils.calculate_circle_area(5):.2f}")
print(f"两点间距离: {MathUtils.calculate_distance(0, 0, 3, 4):.2f}")

# 也可以通过实例调用静态方法
math_utils = MathUtils()
print(f"通过实例调用: {math_utils.add(10, 20)}")
```

## 7. 属性访问控制

### 7.1 公有属性

默认情况下，Python中的属性都是公有的，可以从外部直接访问。

```python
class BankAccount:
    """银行账户类 - 演示公有属性"""
    
    def __init__(self, account_holder, initial_balance=0):
        """构造函数"""
        self.account_holder = account_holder  # 公有属性
        self.balance = initial_balance        # 公有属性
        self.account_number = "ACC" + str(id(self))  # 公有属性

# 创建账户
account = BankAccount("张三", 1000)

# 可以直接访问和修改公有属性
print(f"账户持有人: {account.account_holder}")
print(f"余额: {account.balance}")
print(f"账户号: {account.account_number}")

# 可以直接修改余额（不安全）
account.balance = 10000  # 危险！直接修改余额
print(f"修改后余额: {account.balance}")
```

### 7.2 受保护属性

使用单下划线`_`前缀表示受保护属性，约定不应该从外部直接访问。

```python
class BankAccount:
    """银行账户类 - 演示受保护属性"""
    
    def __init__(self, account_holder, initial_balance=0):
        """构造函数"""
        self.account_holder = account_holder
        self._balance = initial_balance      # 受保护属性
        self._transaction_count = 0         # 受保护属性
    
    def deposit(self, amount):
        """存款"""
        if amount > 0:
            self._balance += amount
            self._transaction_count += 1
            print(f"存款成功，余额: {self._balance}")
        else:
            print("存款金额必须大于0")
    
    def withdraw(self, amount):
        """取款"""
        if amount > 0:
            if amount <= self._balance:
                self._balance -= amount
                self._transaction_count += 1
                print(f"取款成功，余额: {self._balance}")
            else:
                print("余额不足")
        else:
            print("取款金额必须大于0")
    
    def get_balance(self):
        """获取余额"""
        return self._balance
    
    def get_transaction_count(self):
        """获取交易次数"""
        return self._transaction_count

# 使用受保护属性
account = BankAccount("李四", 2000)

# 推荐通过方法访问
account.deposit(500)
account.withdraw(200)
print(f"余额: {account.get_balance()}")
print(f"交易次数: {account.get_transaction_count()}")

# 仍然可以直接访问（但不推荐）
print(f"直接访问余额: {account._balance}")
```

### 7.3 私有属性

使用双下划线`__`前缀表示私有属性，Python会进行名称修饰，使外部无法直接访问。

```python
class BankAccount:
    """银行账户类 - 演示私有属性"""
    
    def __init__(self, account_holder, initial_balance=0):
        """构造函数"""
        self.account_holder = account_holder
        self.__balance = initial_balance        # 私有属性
        self.__transaction_history = []        # 私有属性
        self.__pin = "1234"                    # 私有属性
    
    def deposit(self, amount):
        """存款"""
        if amount > 0:
            self.__balance += amount
            self.__transaction_history.append(f"存款: +{amount}")
            print(f"存款成功，余额: {self.__balance}")
        else:
            print("存款金额必须大于0")
    
    def withdraw(self, amount, pin):
        """取款"""
        if pin != self.__pin:
            print("密码错误")
            return
        
        if amount > 0:
            if amount <= self.__balance:
                self.__balance -= amount
                self.__transaction_history.append(f"取款: -{amount}")
                print(f"取款成功，余额: {self.__balance}")
            else:
                print("余额不足")
        else:
            print("取款金额必须大于0")
    
    def get_balance(self):
        """获取余额"""
        return self.__balance
    
    def get_transaction_history(self):
        """获取交易历史"""
        return self.__transaction_history.copy()
    
    def change_pin(self, old_pin, new_pin):
        """修改密码"""
        if old_pin == self.__pin:
            self.__pin = new_pin
            print("密码修改成功")
        else:
            print("原密码错误")

# 使用私有属性
account = BankAccount("王五", 3000)

# 正常操作
account.deposit(1000)
account.withdraw(500, "1234")
account.withdraw(100, "0000")  # 密码错误

# 获取信息
print(f"余额: {account.get_balance()}")
print("交易历史:")
for transaction in account.get_transaction_history():
    print(f"  {transaction}")

# 尝试直接访问私有属性（会失败）
try:
    print(account.__balance)  # 会报错
except AttributeError as e:
    print(f"无法访问私有属性: {e}")

# 修改密码
account.change_pin("1234", "5678")
account.withdraw(200, "5678")
```

## 8. 实际应用示例

### 8.1 学生成绩管理系统

```python
class Student:
    """学生类 - 成绩管理系统"""
    
    # 类属性
    school_name = "厦门工学院"
    total_students = 0
    
    def __init__(self, name, student_id, major):
        """构造函数"""
        self.name = name
        self.student_id = student_id
        self.major = major
        self.courses = {}  # 课程成绩字典
        self.gpa = 0.0
        Student.total_students += 1
    
    def add_course(self, course_name, grade):
        """添加课程成绩"""
        if 0 <= grade <= 100:
            self.courses[course_name] = grade
            self._calculate_gpa()
            print(f"{self.name}的{course_name}成绩已添加: {grade}")
        else:
            print("成绩必须在0-100之间")
    
    def remove_course(self, course_name):
        """删除课程"""
        if course_name in self.courses:
            del self.courses[course_name]
            self._calculate_gpa()
            print(f"{self.name}的{course_name}课程已删除")
        else:
            print(f"{self.name}没有选修{course_name}")
    
    def _calculate_gpa(self):
        """计算GPA（私有方法）"""
        if self.courses:
            self.gpa = sum(self.courses.values()) / len(self.courses)
        else:
            self.gpa = 0.0
    
    def get_course_count(self):
        """获取课程数量"""
        return len(self.courses)
    
    def get_best_course(self):
        """获取最高分课程"""
        if self.courses:
            best_course = max(self.courses, key=self.courses.get)
            return best_course, self.courses[best_course]
        return None, 0
    
    def get_worst_course(self):
        """获取最低分课程"""
        if self.courses:
            worst_course = min(self.courses, key=self.courses.get)
            return worst_course, self.courses[worst_course]
        return None, 0
    
    def get_student_info(self):
        """获取学生信息"""
        return f"""
学生信息:
姓名: {self.name}
学号: {self.student_id}
专业: {self.major}
学校: {Student.school_name}
课程数量: {self.get_course_count()}
GPA: {self.gpa:.2f}
        """
    
    @classmethod
    def get_school_info(cls):
        """获取学校信息"""
        return f"学校: {cls.school_name}, 总学生数: {cls.total_students}"
    
    @staticmethod
    def grade_to_letter(grade):
        """成绩转换为等级"""
        if grade >= 90:
            return "A"
        elif grade >= 80:
            return "B"
        elif grade >= 70:
            return "C"
        elif grade >= 60:
            return "D"
        else:
            return "F"

# 使用学生管理系统
print("=== 学生成绩管理系统 ===")

# 创建学生
student1 = Student("张三", "2024001", "计算机科学")
student2 = Student("李四", "2024002", "软件工程")

# 添加课程成绩
student1.add_course("Python编程", 85)
student1.add_course("数据结构", 92)
student1.add_course("算法设计", 78)
student1.add_course("数据库", 88)

student2.add_course("Java编程", 90)
student2.add_course("Web开发", 85)
student2.add_course("软件工程", 82)

# 显示学生信息
print(student1.get_student_info())
print(student2.get_student_info())

# 获取最高分和最低分课程
best_course, best_grade = student1.get_best_course()
worst_course, worst_grade = student1.get_worst_course()
print(f"{student1.name}最高分课程: {best_course} ({best_grade}分)")
print(f"{student1.name}最低分课程: {worst_course} ({worst_grade}分)")

# 成绩等级转换
print(f"85分对应等级: {Student.grade_to_letter(85)}")
print(f"78分对应等级: {Student.grade_to_letter(78)}")

# 学校信息
print(Student.get_school_info())
```

## 9. 最佳实践

### 9.1 命名规范

```python
class UserAccount:
    """用户账户类 - 遵循命名规范"""
    
    # 类属性使用大写
    MAX_LOGIN_ATTEMPTS = 3
    DEFAULT_BALANCE = 0.0
    
    def __init__(self, username, email):
        # 实例属性使用小写
        self.username = username
        self.email = email
        self._balance = UserAccount.DEFAULT_BALANCE  # 受保护属性
        self.__login_attempts = 0  # 私有属性
    
    # 公共方法使用小写
    def deposit(self, amount):
        """存款"""
        pass
    
    # 私有方法使用双下划线
    def __validate_amount(self, amount):
        """验证金额"""
        return amount > 0
    
    # 属性访问器
    @property
    def balance(self):
        """余额属性"""
        return self._balance
    
    @balance.setter
    def balance(self, value):
        """设置余额"""
        if value >= 0:
            self._balance = value
        else:
            raise ValueError("余额不能为负数")
```

### 9.2 文档字符串

```python
class Calculator:
    """计算器类
    
    提供基本的数学运算功能，包括加减乘除等操作。
    
    属性:
        result (float): 当前计算结果
        
    示例:
        >>> calc = Calculator()
        >>> calc.add(5)
        >>> calc.multiply(3)
        >>> print(calc.result)
        15.0
    """
    
    def __init__(self):
        """初始化计算器
        
        将结果初始化为0。
        """
        self.result = 0.0
    
    def add(self, number):
        """加法运算
        
        参数:
            number (float): 要加的数字
            
        返回:
            Calculator: 返回自身，支持链式调用
        """
        self.result += number
        return self
    
    def multiply(self, number):
        """乘法运算
        
        参数:
            number (float): 要乘的数字
            
        返回:
            Calculator: 返回自身，支持链式调用
        """
        self.result *= number
        return self
```

### 9.3 错误处理

```python
class SafeCalculator:
    """安全计算器类 - 演示错误处理"""
    
    def __init__(self):
        self.result = 0.0
        self.history = []
    
    def safe_divide(self, number):
        """安全除法"""
        try:
            if number == 0:
                raise ZeroDivisionError("除数不能为零")
            self.result /= number
            self.history.append(f"除法: ÷{number}")
            return True
        except ZeroDivisionError as e:
            print(f"错误: {e}")
            return False
        except Exception as e:
            print(f"未知错误: {e}")
            return False
    
    def safe_operation(self, operation, *args):
        """安全操作包装器"""
        try:
            result = operation(*args)
            self.history.append(f"操作: {operation.__name__}")
            return result
        except Exception as e:
            print(f"操作失败: {e}")
            return None
```

## 学习要点总结

🎯 **关键要点总结：**

- **类定义**：使用`class`关键字定义类，类名使用大驼峰命名
- **构造函数**：`__init__`方法用于初始化对象属性
- **实例属性**：每个对象都有独立的属性值
- **实例方法**：可以访问和修改实例属性的方法
- **类属性**：所有实例共享的属性
- **类方法**：使用`@classmethod`装饰器，操作类属性
- **静态方法**：使用`@staticmethod`装饰器，不依赖类或实例
- **访问控制**：使用`_`和`__`控制属性访问级别

## 练习建议

📚 **练习建议：**

1. 创建一个`Rectangle`类，计算面积和周长
2. 设计一个`BankAccount`类，实现存款、取款功能
3. 实现一个`Library`类，管理图书借阅
4. 创建一个`Employee`类，计算工资和奖金

---

**厦门工学院人工智能创作坊 --郑恩赐**  
**2025年9月29日**

