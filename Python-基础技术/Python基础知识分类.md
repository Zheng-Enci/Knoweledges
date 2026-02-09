# 🐍 Python基础知识分类 - 完整学习指南

## 📚 学习路径建议

1. 基础语法 → 2. 数据类型 → 3. 控制结构 → 4. 函数 → 5. 面向对象 → 6. 模块包 → 7. 文件操作 → 8. 异常处理 → 9. 高级特性

## 🎯 一、基础语法

### 1.1 语言特性 <span style="background-color: #d4edda; color: #155724; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">入门</span>

- **Python解释器**：了解Python解释器的工作原理，CPython、PyPy等不同实现
- **缩进规则**：Python使用缩进来表示代码块，4个空格或1个Tab
- **注释语法**：单行注释(#)和多行注释("""或''')的使用
- **编码声明**：# -*- coding: utf-8 -*- 等编码声明

### 1.2 变量和赋值 <span style="background-color: #d4edda; color: #155724; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">入门</span>

- **变量命名规则**：字母、数字、下划线，不能以数字开头，区分大小写
- **赋值操作**：=、+=、-=、*=、/=、//=、%=、**= 等赋值运算符
- **多重赋值**：a, b = 1, 2 或 a, b = b, a 交换变量
- **变量作用域**：局部变量、全局变量、LEGB规则

## 📊 二、数据类型

### 2.1 基本数据类型 <span style="background-color: #d4edda; color: #155724; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">入门</span>

- **数字类型**：int(整数)、float(浮点数)、complex(复数)
- **字符串类型**：str，单引号、双引号、三引号的使用
- **布尔类型**：bool，True和False，布尔运算
- **None类型**：None，表示空值或缺失值

### 2.2 容器数据类型 <span style="background-color: #d4edda; color: #155724; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">入门</span>

- **列表(List)**：有序、可变、可重复的序列，用[]表示
- **元组(Tuple)**：有序、不可变、可重复的序列，用()表示
- **字典(Dict)**：键值对映射，无序、可变，用{}表示
- **集合(Set)**：无序、可变、不重复的集合，用{}表示

## 🔄 三、控制结构

### 3.1 条件语句 <span style="background-color: #d4edda; color: #155724; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">入门</span>

- **if语句**：if、elif、else的基本用法
- **条件表达式**：三元运算符：x if condition else y
- **逻辑运算符**：and、or、not的使用
- **比较运算符**：==、!=、<、>、<=、>=、is、in

### 3.2 循环语句 <span style="background-color: #d4edda; color: #155724; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">入门</span>

- **for循环**：遍历序列、range()函数、enumerate()
- **while循环**：条件循环、无限循环、循环控制
- **循环控制**：break、continue、pass语句
- **else子句**：for-else、while-else的使用

## 🔧 四、函数

### 4.1 函数基础 <span style="background-color: #d4edda; color: #155724; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">入门</span>

- **函数定义**：def关键字、函数名、参数、返回值
- **参数传递**：位置参数、关键字参数、默认参数
- **返回值**：return语句、多值返回、None返回值
- **作用域**：局部作用域、全局作用域、nonlocal关键字

### 4.2 高级函数特性 <span style="background-color: #fff3cd; color: #856404; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">中级</span>

- **可变参数**：*args、**kwargs的使用
- **匿名函数**：lambda表达式的定义和使用
- **高阶函数**：map()、filter()、reduce()函数
- **装饰器**：@decorator语法、装饰器原理

## 🏗️ 五、面向对象编程

### 5.1 类和对象 <span style="background-color: #fff3cd; color: #856404; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">中级</span>

- **类定义**：class关键字、类名、类体
- **对象创建**：实例化、__init__方法、self参数
- **属性和方法**：实例属性、类属性、实例方法、类方法、静态方法
- **访问控制**：公有、私有、受保护的属性和方法

### 5.2 继承和多态 <span style="background-color: #fff3cd; color: #856404; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">中级</span>

- **继承**：单继承、多继承、super()函数
- **方法重写**：重写父类方法、调用父类方法
- **多态**：同一接口的不同实现
- **特殊方法**：__str__、__repr__、__len__等魔术方法

## 📦 六、模块和包

### 6.1 模块系统 <span style="background-color: #fff3cd; color: #856404; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">中级</span>

- **模块导入**：import、from...import、as别名
- **标准库模块**：os、sys、math、random、datetime等
- **第三方模块**：pip安装、requirements.txt
- **模块搜索路径**：sys.path、PYTHONPATH环境变量

### 6.2 包管理 <span style="background-color: #fff3cd; color: #856404; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">中级</span>

- **包结构**：__init__.py文件、包目录结构
- **相对导入**：from .module import、from ..package import
- **包初始化**：__init__.py中的代码执行
- **命名空间包**：Python 3.3+的命名空间包

## 📁 七、文件操作

### 7.1 文件读写 <span style="background-color: #d4edda; color: #155724; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">入门</span>

- **文件打开**：open()函数、文件模式(r、w、a、x等)
- **文件读取**：read()、readline()、readlines()方法
- **文件写入**：write()、writelines()方法
- **文件关闭**：close()方法、with语句

### 7.2 文件系统操作 <span style="background-color: #fff3cd; color: #856404; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">中级</span>

- **路径操作**：os.path模块、pathlib模块
- **目录操作**：os.mkdir()、os.rmdir()、os.listdir()
- **文件信息**：os.stat()、文件大小、修改时间等
- **文件遍历**：os.walk()、递归遍历目录

## ⚠️ 八、异常处理

### 8.1 异常基础 <span style="background-color: #d4edda; color: #155724; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">入门</span>

- **异常类型**：ValueError、TypeError、FileNotFoundError等
- **try-except**：捕获异常、处理异常
- **finally子句**：无论是否异常都执行的代码
- **else子句**：没有异常时执行的代码

### 8.2 异常高级 <span style="background-color: #fff3cd; color: #856404; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">中级</span>

- **自定义异常**：继承Exception类、创建自定义异常
- **异常链**：raise...from...语法
- **异常信息**：traceback模块、异常详细信息
- **断言**：assert语句、调试和测试

## 🚀 九、高级特性

### 9.1 生成器和迭代器 <span style="background-color: #f8d7da; color: #721c24; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">高级</span>

- **迭代器协议**：__iter__()、__next__()方法
- **生成器函数**：yield关键字、生成器表达式
- **生成器方法**：send()、throw()、close()方法
- **协程**：async/await语法、异步编程基础

### 9.2 元编程 <span style="background-color: #f8d7da; color: #721c24; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">高级</span>

- **装饰器高级**：带参数的装饰器、类装饰器
- **元类**：type()函数、__metaclass__属性
- **反射**：getattr()、setattr()、hasattr()、delattr()
- **动态导入**：importlib模块、动态加载模块

### 9.3 并发编程 <span style="background-color: #f8d7da; color: #721c24; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">高级</span>

- **多线程**：threading模块、GIL全局解释器锁
- **多进程**：multiprocessing模块、进程间通信
- **异步编程**：asyncio模块、事件循环
- **协程池**：asyncio.gather()、asyncio.create_task()

## 🛠️ 十、常用库和工具

### 10.1 数据处理 <span style="background-color: #fff3cd; color: #856404; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">中级</span>

- **NumPy**：数值计算、数组操作、线性代数
- **Pandas**：数据分析、DataFrame、Series
- **Matplotlib**：数据可视化、图表绘制
- **Seaborn**：统计图表、数据可视化

### 10.2 人工智能与机器学习 <span style="background-color: #f8d7da; color: #721c24; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">高级</span>

- **TensorFlow**：Google开源深度学习框架
- **PyTorch**：Facebook开源深度学习框架
- **Scikit-learn**：机器学习算法库、数据挖掘
- **OpenCV**：计算机视觉、图像处理
- **NLTK**：自然语言处理工具包
- **SpaCy**：现代自然语言处理库

### 10.3 Web开发 <span style="background-color: #fff3cd; color: #856404; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">中级</span>

- **Flask**：轻量级Web框架、路由、模板
- **Django**：全功能Web框架、ORM、管理后台
- **FastAPI**：现代Web框架、自动API文档
- **Requests**：HTTP库、API调用、网络请求

### 10.4 网络爬虫 <span style="background-color: #fff3cd; color: #856404; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">中级</span>

- **Scrapy**：专业爬虫框架、分布式爬取
- **BeautifulSoup**：HTML/XML解析库
- **Selenium**：浏览器自动化、动态网页爬取
- **Playwright**：现代浏览器自动化工具
- **aiohttp**：异步HTTP客户端/服务器

### 10.5 自动化脚本 <span style="background-color: #fff3cd; color: #856404; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">中级</span>

- **pyautogui**：GUI自动化、鼠标键盘控制
- **schedule**：任务调度、定时执行
- **APScheduler**：高级任务调度器
- **watchdog**：文件系统监控、自动响应
- **psutil**：系统和进程监控

### 10.6 数据库操作 <span style="background-color: #fff3cd; color: #856404; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">中级</span>

- **SQLAlchemy**：Python SQL工具包和ORM
- **PyMySQL**：MySQL数据库连接器
- **psycopg2**：PostgreSQL数据库适配器
- **pymongo**：MongoDB数据库驱动
- **redis-py**：Redis数据库客户端

### 10.7 测试框架 <span style="background-color: #fff3cd; color: #856404; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">中级</span>

- **pytest**：现代Python测试框架
- **unittest**：Python标准测试库
- **Selenium**：Web应用自动化测试
- **mock**：模拟对象和函数

### 10.8 系统运维 <span style="background-color: #fff3cd; color: #856404; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">中级</span>

- **Fabric**：远程部署和系统管理
- **Ansible**：自动化运维工具
- **Docker SDK**：Docker容器管理
- **paramiko**：SSH2协议库

## 📚 学习资源推荐

- **官方文档**：Python官方文档是最权威的学习资源
- **在线教程**：菜鸟教程、廖雪峰Python教程
- **实践项目**：GitHub上的开源项目、LeetCode算法题
- **书籍推荐**：《Python编程：从入门到实践》、《流畅的Python》
- **视频教程**：B站、慕课网等平台的Python课程

---

**厦门工学院人工智能创作坊 --郑恩赐**
