# P3H0-Python-os模块完全指南-操作系统接口与文件路径处理利器

> 📌 **学习建议**：本文档旨在帮助您了解 Python `os` 模块的功能和使用方法。需要注意的是，在实际开发中，并非所有场景都需要使用 `os` 模块。因此，建议您：
> - **了解为主**：对 `os` 模块的功能有一个大致的认识即可，无需深入掌握每个细节
> - **按需学习**：在实际开发中遇到需要使用 `os` 模块的场景时，再学习相应的函数和用法
> - **灵活选择**：根据具体需求选择合适的工具，不必拘泥于使用 `os` 模块
> 
> 当您需要处理文件路径、环境变量、系统调用等场景时，可以查找相应的解决方案和示例代码。

## 📝 摘要

Python `os` 模块是标准库中的核心模块，提供与操作系统交互的接口。本文档全面介绍了 os 模块的八大核心功能，涵盖环境变量操作、文件和目录管理、路径处理、文件权限控制、进程管理、系统信息获取、文件描述符操作以及用户与权限管理。通过丰富的示例代码，帮助开发者掌握跨平台系统编程技能。

## 🎯 前置知识点

在学习 Python `os` 模块之前，建议您掌握以下基础知识，这将有助于更好地理解和应用 `os` 模块的功能。

### 前置知识点思维导图

```mermaid
mindmap
  root)前置知识点(
    Python 基础语法
      变量和数据类型
      控制结构
        条件语句
        循环语句
      函数定义和调用
      模块导入
        import 语句
        from import
    文件系统基础
      路径概念
        绝对路径
        相对路径
      路径分隔符
        Windows 反斜杠
        Linux macOS 正斜杠
      目录结构
        根目录
        当前目录
        上级目录
    环境变量
      概念和作用
      常见环境变量
        PATH
        HOME USERPROFILE
        USER USERNAME
      获取和设置
    异常处理
      try except 语句
      常见异常类型
        FileNotFoundError
        PermissionError
        OSError
    文件权限
      权限概念
        读权限
        写权限
        执行权限
      权限表示
        八进制数
        符号表示
    进程基础
      进程概念
      进程 ID PID
      父进程和子进程
    跨平台编程
      操作系统差异
        Windows
        Linux
        macOS
      路径处理
      命令差异
```

### 1. Python 基础语法

在使用 `os` 模块之前，您需要掌握 Python 的基础语法：

- **变量和数据类型**：了解字符串、整数、列表等基本数据类型
- **控制结构**：掌握 `if-else` 条件语句和 `for`、`while` 循环语句
- **函数定义和调用**：理解如何定义函数、传递参数和返回值
- **模块导入**：熟悉 `import os` 和 `from os import xxx` 等导入方式

**示例**：

```python
# 导入 os 模块
import os

# 使用 os 模块的函数
current_dir = os.getcwd()
print(f"当前目录: {current_dir}")
```

### 2. 文件系统基础

理解文件系统的基本概念对于使用 `os` 模块至关重要：

- **路径概念**：
  - **绝对路径**：从文件系统根目录开始的完整路径（如 `C:\Users\admin\file.txt` 或 `/home/user/file.txt`）
  - **相对路径**：相对于当前工作目录的路径（如 `./file.txt` 或 `../parent/file.txt`）
- **路径分隔符**：
  - Windows 使用反斜杠 `\`
  - Linux/macOS 使用正斜杠 `/`
- **目录结构**：理解根目录、当前目录（`.`）、上级目录（`..`）等概念

### 3. 环境变量

环境变量是操作系统层面的配置信息：

- **概念**：环境变量是键值对，用于存储系统配置、路径等信息
- **常见环境变量**：
  - `PATH`：可执行文件的搜索路径
  - `HOME`（Linux/macOS）或 `USERPROFILE`（Windows）：用户主目录
  - `USER`（Linux/macOS）或 `USERNAME`（Windows）：当前用户名
- **作用**：环境变量可以让程序在不同环境中使用不同的配置，无需修改代码

### 4. 异常处理

使用 `os` 模块进行文件操作时，可能会遇到各种异常：

- **try-except 语句**：用于捕获和处理异常
- **常见异常类型**：
  - `FileNotFoundError`：文件或目录不存在
  - `PermissionError`：权限不足
  - `OSError`：操作系统相关的错误

**示例**：

```python
import os

try:
    os.remove("nonexistent_file.txt")
except FileNotFoundError:
    print("文件不存在")
except PermissionError:
    print("权限不足")
```

### 5. 文件权限基础

理解文件权限有助于使用 `os.chmod()` 等函数：

- **权限概念**：
  - **读权限（r）**：可以读取文件内容或列出目录内容
  - **写权限（w）**：可以修改文件内容或在目录中创建文件
  - **执行权限（x）**：可以执行文件或进入目录
- **权限表示**：
  - **八进制数**：如 `0o755` 表示所有者有全部权限，其他用户有读和执行权限
  - **符号表示**：如 `rwxr-xr-x` 表示相同的权限

> 💡 **提示**：文件权限主要在类 Unix 系统（Linux、macOS）上使用，Windows 的权限系统有所不同。

### 6. 进程基础

了解进程概念有助于理解 `os` 模块的进程管理功能：

- **进程概念**：进程是正在运行的程序实例
- **进程 ID（PID）**：操作系统为每个进程分配的唯一标识符
- **父进程和子进程**：进程可以创建子进程，形成进程树结构

### 7. 模块导入

掌握 Python 的模块导入机制：

- **import 语句**：`import os` 导入整个模块
- **from...import**：`from os import getcwd` 导入特定函数
- **模块路径**：理解 Python 如何查找和导入模块

**示例**：

```python
# 方式一：导入整个模块
import os
current_dir = os.getcwd()

# 方式二：导入特定函数
from os import getcwd
current_dir = getcwd()
```

### 8. 跨平台编程注意事项

编写跨平台代码时需要注意：

- **操作系统差异**：
  - Windows、Linux、macOS 在路径表示、命令执行等方面存在差异
  - `os` 模块自动处理大部分差异，但某些功能可能在不同平台上行为不同
- **路径处理**：使用 `os.path.join()` 等函数可以自动处理不同系统的路径分隔符
- **命令差异**：不同操作系统的系统命令可能不同，需要根据平台选择

> 💡 **学习建议**：如果您是初学者，可以先掌握 Python 基础语法和文件系统基础，然后在学习 `os` 模块的过程中逐步了解其他知识点。不必等到完全掌握所有前置知识再开始学习 `os` 模块。

---

## 00. 什么是 os 模块

### 00.1 🔍 os 模块的定义

**os 模块（Operating System Interface，操作系统接口模块）** 是 Python 标准库中的一个核心模块，提供了与操作系统交互的接口。通过 os 模块，开发者可以实现文件和目录操作、环境变量管理、进程管理、系统信息获取等功能，从而编写出跨平台的系统级程序。

**生活化比喻**：
- **os 模块**：就像电脑的"遥控器"，可以控制文件、文件夹、环境变量等系统资源
- **os.path 子模块**：就像"路径导航器"，可以拆分、组合、检查路径，自动处理不同操作系统的路径差异

### 00.2 💡 os 模块的特点和重要性

os 模块具有以下特点和重要性：

1. **跨平台兼容**：os 模块自动处理不同操作系统（Windows、Linux、macOS）的差异，让代码可以在多个平台上运行
2. **系统级操作**：提供了直接与操作系统交互的能力，可以执行文件操作、进程管理等系统级任务
3. **无需安装**：os 模块是 Python 标准库的一部分，无需额外安装即可使用
4. **功能丰富**：涵盖了文件系统操作、环境变量管理、进程控制、系统信息获取等多个方面
5. **底层接口**：提供了操作系统底层的接口，是许多高级模块（如 shutil、pathlib）的基础

### 00.3 📊 os 模块的主要功能分类

os 模块的功能可以分为以下几大类：

```mermaid
mindmap
  root)os 模块功能分类(
    环境变量操作
      获取环境变量
      设置环境变量
      删除环境变量
    文件和目录操作
      创建目录
      删除目录
      重命名文件或目录
      列出目录内容
    路径操作 os.path
      路径拼接
      路径拆分
      路径规范化
      类型判断
    文件权限和属性
      修改文件权限
      获取文件状态信息
    进程管理
      获取进程 ID
      执行系统命令
      创建子进程
    系统信息获取
      获取操作系统名称
      获取系统配置参数
    文件描述符操作
      底层文件 I/O 操作
    用户与权限管理
      获取用户信息
      获取用户组信息
```

### 00.4 为什么需要 os 模块？

在 Python 编程中，我们经常需要与操作系统进行交互，比如获取当前工作目录、创建文件夹、读取环境变量、执行系统命令等。如果没有 os 模块，开发者将面临诸多挑战。

**没有 os 模块会遇到的问题**：

- **代码复杂且冗长**：需要手动编写大量底层代码来实现基本的系统操作，比如获取当前目录需要根据操作系统类型选择不同的命令（Windows 用 `cd`，Linux/Mac 用 `pwd`），并手动处理子进程的创建和输出捕获，导致代码冗长且难以维护。

- **跨平台兼容性差**：不同操作系统的系统调用和路径表示方式各不相同（Windows 使用反斜杠 `\`，Linux/Mac 使用正斜杠 `/`），手动处理这些差异需要大量的条件判断，代码在不同平台上可能无法正常运行。

- **错误风险高**：直接调用底层系统 API 或执行系统命令容易引入各种错误，如命令执行失败、输出格式不一致、权限问题等，增加了调试和维护的难度。

- **性能问题**：手动实现的系统操作通常需要创建子进程或调用外部命令，这比直接调用系统 API 效率低得多，影响程序的整体性能。

**有了 os 模块后的便利**：

- **代码简洁高效**：一行代码就能完成复杂的系统操作，比如 `os.getcwd()` 获取当前目录，`os.makedirs()` 创建目录，无需编写大量底层代码。

- **自动跨平台兼容**：os 模块自动处理不同操作系统的差异，使用 `os.path.join()` 可以自动适配不同系统的路径分隔符，编写的代码可以在 Windows、Linux、macOS 等多个平台上无缝运行。

- **稳定可靠**：os 模块是 Python 标准库的一部分，经过充分测试和优化，直接调用系统 API，避免了命令执行的各种异常情况，大大降低了出错风险。

- **性能优秀**：os 模块的函数直接调用系统 API，无需创建子进程，执行效率高，性能优于手动实现的方式。

因此，os 模块是 Python 系统编程不可或缺的工具，它让开发者能够以简洁、高效、可靠的方式与操作系统交互，大大提升了开发效率和代码质量。

---

## 01. 环境变量操作

环境变量（Environment Variables）是操作系统层面的键值对，通常用来存放路径、配置、凭证等关键信息。`os` 模块提供了两套 API：类字典对象 `os.environ`（实时映射当前进程的环境变量）以及函数 `os.getenv()` / `os.putenv()` 等，帮助我们安全地读取和修改这些配置。

### 01.1 获取环境变量

#### 方式一：`os.getenv()` —— 安全读取

```python
import os

db_host = os.getenv("DB_HOST")           # 不存在时默认返回 None
user_profile = os.getenv("USERPROFILE", "C:/Users/Public")  # USERPROFILE 是 Windows 默认存在的环境变量，可指定默认值

print(f"DB_HOST -> {db_host}")
print(f"USERPROFILE -> {user_profile}")
```

**终端示例输出：**

```
DB_HOST -> None
USERPROFILE -> C:\Users\YourName
```

- **优势**：读取不到时不会抛异常，可设定默认值，适合通用配置。
- **典型场景**：读取数据库连接、API Token 等。

#### 方式二：`os.environ` —— 直接访问底层字典

```python
import os

path_value = os.environ.get("PATH")  # 推荐使用 get，避免 KeyError
all_envs = dict(os.environ)          # 获取当前进程的所有环境变量快照

print(f"PATH -> {path_value[:60]}...")      # 只展示前 60 个字符，避免输出过长
print(f"envs 总数 -> {len(all_envs)}")
```

**终端示例输出：**

```
PATH -> C:\Program Files\Python313\Scripts\;C:\Program Files\Py...
envs 总数 -> 48
```

- **优势**：能一次性遍历环境变量，方便调试或构建配置映射。
- **注意**：若使用 `os.environ["VAR"]` 访问不存在的变量会抛出 `KeyError`。

### 01.2 设置环境变量

使用 `os.environ` 赋值即可修改当前进程（及其子进程）看到的环境变量：

```python
import os

os.environ["UPLOAD_DIR"] = "D:/uploads"
print(os.getenv("UPLOAD_DIR"))  # D:/uploads
```

**终端示例输出：**

```
D:/uploads
```

> ⚠️ **提示**：这种修改仅对当前 Python 进程及其子进程生效，关闭程序后即失效；不影响系统全局配置。

#### 设置默认值的最佳实践

```python
import os

log_level = os.environ.setdefault("LOG_LEVEL", "INFO")
print(f"LOG_LEVEL -> {log_level}")
```

**终端示例输出：**

```
LOG_LEVEL -> INFO
```

`setdefault` 只在变量不存在时才设置，适合提供兜底配置。

### 01.3 删除环境变量

在敏感信息用完后，可以显式删除，降低泄露风险：

```python
import os

removed = os.environ.pop("UPLOAD_DIR", None)  # 若不存在返回 None，不抛异常
print(f"UPLOAD_DIR 已删除 -> {removed is not None}")
```

**终端示例输出：**

```
UPLOAD_DIR 已删除 -> True
```

> ✅ 建议在读取完密钥（如临时访问凭证）后立即 `pop` 掉，减少后续代码误用。

### 01.4 遍历所有环境变量

当需要调试或批量导出配置时，可遍历 `os.environ.items()`：

```python
import os

for key, value in os.environ.items():
    print(f"{key} = {value}")
```

**终端示例输出（截取前 3 行）：**

```
ALLUSERSPROFILE = C:\ProgramData
APPDATA = C:\Users\YourName\AppData\Roaming
COMMONPROGRAMFILES = C:\Program Files\Common Files
...
```

> 👀 **隐私提醒**：遍历环境变量可能输出敏感信息（如 `TOKEN`、`PASSWORD`），在日志或终端打印前务必确认安全性。

---

### 01.5 我的环境变量操作建议

- **命名统一清晰**：尽量使用全大写 + 下划线的方式（如 `MY_APP_HOME`），便于团队快速识别变量用途。
- **敏感信息慎存慎打**：密码、Token 如必须写入环境变量，应避免在日志或异常中泄露，并限制可访问的用户与进程。
- **关键变量有兜底值**：在代码中通过 `os.getenv("VAR", "default")` 或 `setdefault` 提供合理默认，减少部署遗漏造成的启动故障。
- **定期审计清理**：长期项目要清点不再使用的变量，防止陈旧配置干扰新版本。
- **修改系统变量要追加**：如需改写 `PATH`，务必在原值前/后拼接，避免替换掉系统命令路径。
- **善用管理工具**：在多环境/多人协作项目中，可借助 `direnv`、`.env` 管理插件等工具集中维护变量。

## 02. 文件和目录操作

os 模块提供了丰富的文件和目录操作函数，让我们可以方便地管理文件系统中的文件和文件夹。

### 02.1 路径查找机制：相对路径 vs 绝对路径

在理解文件和目录操作之前，我们需要先了解 Python 是如何查找路径的。

#### 相对路径（Relative Path）

**相对路径**是相对于当前工作目录（Current Working Directory）的路径。当前工作目录可以通过 `os.getcwd()` 获取，通常是运行 Python 脚本时所在的目录。

- **示例**：`"config.ini"`、`"./data/file.txt"`、`"../parent_dir"`
- **特点**：路径不以盘符（Windows）或 `/`（Linux/macOS）开头
- **查找方式**：Python 会在当前工作目录下查找该路径

```python
import os

# 假设当前工作目录是 E:\Projects\MyApp
# 相对路径 "config.ini" 会被解析为 E:\Projects\MyApp\config.ini
file_path = "config.ini"  # 相对路径
```

#### 绝对路径（Absolute Path）

**绝对路径**是从文件系统根目录开始的完整路径，不依赖于当前工作目录。

- **示例**：`"E:\Projects\MyApp\config.ini"`（Windows）、`"/home/user/project/config.ini"`（Linux/macOS）
- **特点**：路径包含完整的目录结构，从根目录开始
- **查找方式**：Python 直接根据完整路径查找，不受工作目录影响

```python
import os

# 绝对路径，无论当前工作目录在哪里，都指向同一个文件
file_path = "E:\\Projects\\MyApp\\config.ini"  # Windows 绝对路径
# 或
file_path = "/home/user/project/config.ini"  # Linux/macOS 绝对路径
```

#### Python是如何判断用户输入的路径是绝对还是相对的？

当用户输入一个路径字符串时，Python 需要判断这个路径是绝对路径还是相对路径。Python 的判断依据是基于路径字符串的**格式特征**，而不是路径是否真实存在。

**Python 的判断机制**：

Python 通过 `os.path.isabs()` 函数来判断路径类型，该函数会根据当前运行的操作系统，检查路径字符串是否符合绝对路径的格式特征：

1. **Windows 系统的判断依据**：
   - **盘符路径**：如果路径以单个字母（A-Z）加冒号和反斜杠开头（如 `C:\`、`D:\`），则判断为绝对路径
   - **UNC 路径**：如果路径以两个反斜杠开头（如 `\\server\share`），则判断为绝对路径（网络共享路径）
   - **其他情况**：不符合上述特征的路径，均判断为相对路径

2. **Linux/macOS 系统的判断依据**：
   - **根路径**：如果路径以单个正斜杠 `/` 开头，则判断为绝对路径（从文件系统根目录开始）
   - **其他情况**：不以 `/` 开头的路径，均判断为相对路径

**重要特点**：
- Python 只检查路径字符串的**格式**，不验证路径是否真实存在
- 即使路径不存在，只要格式符合绝对路径特征，也会返回 `True`
- 判断结果依赖于运行 Python 的操作系统类型

```python
import os

# Windows 系统示例
print(os.path.isabs("C:\\Users\\admin\\file.txt"))  # True - 符合盘符路径格式
print(os.path.isabs("\\server\\share\\file.txt"))   # True - 符合 UNC 路径格式
print(os.path.isabs("file.txt"))                    # False - 不符合绝对路径格式
print(os.path.isabs("data\\file.txt"))              # False - 不符合绝对路径格式

# Linux/macOS 系统示例
print(os.path.isabs("/home/user/file.txt"))         # True - 以 / 开头，符合绝对路径格式
print(os.path.isabs("file.txt"))                    # False - 不以 / 开头
print(os.path.isabs("data/file.txt"))               # False - 不以 / 开头
```

**终端示例输出（Windows 系统）：**

```
True
True
False
False
```

> 💡 **核心要点**：Python 的判断依据是路径字符串的**格式特征**，而不是路径的实际存在性。这种设计使得程序可以在文件创建之前就判断路径类型，便于进行路径处理和错误检查。

### 02.2 获取当前工作目录

使用 `os.getcwd()` 可以获取当前 Python 进程的工作目录（Current Working Directory）：

```python
import os

current_dir = os.getcwd()
print(f"当前工作目录: {current_dir}")
```

**假设场景**：假设你的 Python 脚本文件位于 `E:\Projects\MyApp\main.py`，在 `E:\Projects\MyApp` 目录下运行该脚本时：

**终端示例输出：**

```
当前工作目录: E:\Projects\MyApp
```

> 💡 **说明**：工作目录通常是运行 Python 脚本时所在的目录，而不是脚本文件本身所在的目录。

> 💡 **提示**：工作目录是程序执行文件操作时的默认路径，相对路径会基于此目录进行解析。

### 02.3 更改工作目录

使用 `os.chdir(path)` 可以切换到指定的目录：

```python
import os

print(f"切换前: {os.getcwd()}")
os.chdir("..")  # 切换到上一级目录
print(f"切换后: {os.getcwd()}")
```

**终端示例输出：**

```
切换前: E:\Projects\MyApp\src
切换后: E:\Projects\MyApp
```

> ⚠️ **注意**：如果目标目录不存在，`os.chdir()` 会抛出 `FileNotFoundError` 异常。

### 02.4 创建目录

#### 创建单个目录：`os.mkdir()`

`os.mkdir(path)` 用于创建单个目录，如果目录已存在会抛出 `FileExistsError`：

```python
import os

os.mkdir("test_dir")
print("目录创建成功")
```

**终端示例输出：**

```
目录创建成功
```

#### 创建多级目录：`os.makedirs()`

`os.makedirs(path, exist_ok=False)` 可以递归创建多级目录，相当于 `mkdir -p`：

```python
import os

# 创建多级目录
os.makedirs("parent/child/grandchild", exist_ok=True)
print("多级目录创建成功")

# exist_ok=True 时，目录已存在也不会报错
os.makedirs("parent/child/grandchild", exist_ok=True)
print("再次创建（已存在）不会报错")
```

**终端示例输出：**

```
多级目录创建成功
再次创建（已存在）不会报错
```

> 💡 **最佳实践**：使用 `exist_ok=True` 可以避免目录已存在时的异常，适合在不确定目录是否存在时使用。

### 02.5 删除目录

#### 删除空目录：`os.rmdir()`

`os.rmdir(path)` 只能删除空目录，如果目录不为空会抛出 `OSError`：

```python
import os

os.mkdir("empty_dir")
os.rmdir("empty_dir")
print("空目录删除成功")
```

#### 删除多级目录：`os.removedirs()`

`os.removedirs(path)` 递归删除空目录，会从最深层开始删除，直到遇到非空目录：

```python
import os

os.makedirs("a/b/c", exist_ok=True)
os.removedirs("a/b/c")  # 会删除 a、b、c 三个空目录
print("多级空目录删除成功")
```

> ⚠️ **注意**：`os.removedirs()` 只能删除空目录，如果目录中有文件或其他目录，删除会失败。

### 02.6 列出目录内容

使用 `os.listdir(path)` 可以列出指定目录下的所有文件和子目录名称：

```python
import os

# 列出当前目录内容
# os.listdir(path) -> 返回目录中所有文件和子目录名称的列表
items = os.listdir(".")  # 传入目录路径（"." 表示当前目录），返回文件名列表
print("当前目录内容:")
for item in items:
    print(f"  - {item}")

# 列出指定目录内容
# os.path.exists(path) -> 检查路径是否存在，返回 True 或 False
if os.path.exists("parent"):  # 传入路径字符串，返回布尔值
    items = os.listdir("parent")  # 传入目录路径，返回文件名列表
    print(f"\nparent 目录内容: {items}")
```

**终端示例输出：**

```
当前目录内容:
  - main.py
  - config.ini
  - README.md
  - utils.py
  - ...
parent 目录内容: ['child']
```

> 💡 **提示**：`os.listdir()` 返回的是文件名列表，不包含子目录中的内容。如果需要递归列出所有文件，可以使用 `os.walk()`。

### 02.7 检查文件或目录存在性

使用 `os.path.exists(path)` 可以检查文件或目录是否存在：

```python
import os

# 检查文件是否存在
file_exists = os.path.exists("config.ini")
print(f"文件存在: {file_exists}")

# 检查目录是否存在
dir_exists = os.path.exists("test_dir")
print(f"目录存在: {dir_exists}")

# 检查不存在的路径
not_exists = os.path.exists("non_existent_file.txt")
print(f"不存在的路径: {not_exists}")
```

**终端示例输出：**

```
文件存在: True
目录存在: False
不存在的路径: False
```

> 💡 **相关函数**：
> - `os.path.isfile(path)`：检查是否为文件
> - `os.path.isdir(path)`：检查是否为目录
> - `os.path.islink(path)`：检查是否为符号链接
>
> **符号链接（Symbolic Link）简介**：
> 符号链接（也称为软链接）是一种特殊类型的文件，它存储的是指向另一个文件或目录的路径引用，而不是实际的数据内容。符号链接类似于 Windows 系统中的"快捷方式"或 Linux 系统中的"软链接"。与硬链接不同，符号链接可以跨文件系统或分区指向目标，甚至可以指向不存在的路径。当访问符号链接时，系统会自动跳转到它指向的实际文件或目录。

### 02.8 删除文件

使用 `os.remove(path)` 可以删除文件（不能删除目录）：

```python
import os

# 创建一个临时文件
with open("temp_file.txt", "w") as f:
    f.write("临时文件内容")

# 检查文件是否存在
if os.path.exists("temp_file.txt"):
    print("文件存在，准备删除")
    os.remove("temp_file.txt")
    print("文件删除成功")
    
    # 再次检查
    if not os.path.exists("temp_file.txt"):
        print("确认文件已删除")
```

**终端示例输出：**

```
文件存在，准备删除
文件删除成功
确认文件已删除
```

> ⚠️ **注意**：
> - `os.remove()` 只能删除文件，不能删除目录
> - 如果文件不存在，会抛出 `FileNotFoundError`
> - 如果文件被占用（如正在被其他程序打开），删除会失败

### 02.9 重命名文件或目录

使用 `os.rename(src, dst)` 可以重命名文件或目录，也可以用于移动文件：

```python
import os

# 创建一个测试文件
with open("old_name.txt", "w") as f:
    f.write("测试内容")

# 重命名文件
os.rename("old_name.txt", "new_name.txt")
print("文件重命名成功")

# 检查新文件名是否存在
if os.path.exists("new_name.txt"):
    print("新文件存在")

# 重命名目录
os.mkdir("old_dir")
os.rename("old_dir", "new_dir")
print("目录重命名成功")

# 清理
os.remove("new_name.txt")
os.rmdir("new_dir")
```

**终端示例输出：**

```
文件重命名成功
新文件存在
目录重命名成功
```

> 💡 **提示**：`os.rename()` 也可以用于移动文件到不同目录，只要目标路径与源路径在同一文件系统上。

### 02.10 遍历目录树

`os.walk(top)` 是 Python 中用于递归遍历目录树的强大工具，它通过生成器的方式，逐层返回目录路径、子目录列表和文件列表，方便开发者对文件系统进行操作。

#### os.walk() 的工作原理

`os.walk()` 接受一个目录路径作为参数，默认以自顶向下的方式（`topdown=True`）遍历该目录及其所有子目录。在遍历过程中，每次迭代都会返回一个包含三个元素的元组：

1. **`dirpath`**：当前遍历到的目录的完整路径（字符串）
2. **`dirnames`**：当前目录下的所有子目录名称列表（列表，可修改）
3. **`filenames`**：当前目录下的所有文件名列表（列表）

**遍历顺序**：
- 当 `topdown=True`（默认）时：先访问父目录，再访问子目录（自顶向下）
- 当 `topdown=False` 时：先访问子目录，再访问父目录（自底向上）

#### 重要特性

1. **生成器模式**：`os.walk()` 返回一个生成器，不会一次性加载所有目录信息到内存，适合处理大型目录树
2. **可控制遍历**：在 `topdown=True` 时，可以通过修改 `dirnames` 列表来控制遍历哪些子目录（删除列表中的目录名可以跳过该目录）
3. **符号链接处理**：默认不跟随符号链接（`followlinks=False`），避免可能的无限循环
4. **错误处理**：可以通过 `onerror` 参数指定错误处理函数，处理权限错误等异常情况

使用 `os.walk(top)` 可以递归遍历目录树，返回三元组 `(dirpath, dirnames, filenames)`：

**`os.walk()` 参数说明**：
- `top`：要遍历的根目录路径（字符串）
- `topdown=True`：遍历方向，`True` 时从上到下遍历（先访问父目录再访问子目录），`False` 时从下到上遍历（先访问子目录再访问父目录）
- `onerror=None`：错误处理函数，当遍历过程中遇到错误时调用，默认为 `None`（忽略错误）
- `followlinks=False`：是否跟随符号链接，`True` 时会进入符号链接指向的目录，`False` 时跳过符号链接

**返回值**（每次迭代返回一个三元组）：
- `dirpath`：当前正在访问的目录路径（字符串）
- `dirnames`：当前目录下的所有子目录名称列表（列表）
- `filenames`：当前目录下的所有文件名列表（列表）

```python
import os

# os.walk() 返回一个生成器，每次迭代返回 (当前目录路径, 子目录列表, 文件列表)
# 假设存在一个 project 目录，目录结构如下：
# project/
#   main.py
#   src/
#     utils/
#       helper.py
#   tests/
#     test_main.py
for root, dirs, files in os.walk("project"):
    print(f"当前目录: {root}")
    print(f"子目录: {dirs}")
    print(f"文件: {files}")
    print("-" * 40)
```

**终端示例输出：**

```
当前目录: project
子目录: ['src', 'tests']
文件: ['main.py']
----------------------------------------
当前目录: project\src
子目录: ['utils']
文件: []
----------------------------------------
当前目录: project\src\utils
子目录: []
文件: ['helper.py']
----------------------------------------
当前目录: project\tests
子目录: []
文件: ['test_main.py']
----------------------------------------
```

### 02.11 文件和目录操作最佳实践

- **路径使用 `os.path.join()`**：使用 `os.path.join()` 拼接路径，自动处理不同操作系统的路径分隔符差异（本函数详细解释可以查看 [03.1 路径拼接](#031-路径拼接) 章节）
- **操作前先检查**：删除、重命名等操作前，先用 `os.path.exists()` 检查路径是否存在，避免异常
- **异常处理**：文件操作可能因权限、文件占用等原因失败，应使用 `try-except` 捕获异常
- **批量操作用 `os.walk()`**：需要递归处理目录时，使用 `os.walk()` 比手动递归更高效
- **清理临时文件**：程序创建的临时文件和目录，应在使用完毕后及时清理

## 03. 路径操作（os.path）

`os.path` 模块是 Python 标准库中用于处理文件路径的核心模块，它提供了跨平台的路径操作函数，能够自动处理不同操作系统之间的路径差异。

### 不同操作系统的路径差异

不同操作系统之间在路径表示方式上存在显著差异，了解这些差异对于理解路径处理非常重要。

#### 1. 路径分隔符差异

**Windows 系统**：
- 使用反斜杠 `\` 作为路径分隔符
- 示例：`C:\Users\admin\Documents\file.txt`

**Linux/macOS 系统**：
- 使用正斜杠 `/` 作为路径分隔符
- 示例：`/home/user/documents/file.txt`

**影响**：如果手动拼接路径，在不同系统上会出现兼容性问题。需要根据操作系统选择正确的分隔符。

#### 2. 绝对路径格式差异

**Windows 系统**：
- 绝对路径以盘符开头（如 `C:\`、`D:\`）
- 支持 UNC 路径（网络共享路径），格式为 `\\server\share\path`
- 示例：`C:\Users\admin\file.txt`、`\\server\share\file.txt`

**Linux/macOS 系统**：
- 绝对路径以根目录 `/` 开头
- 示例：`/home/user/file.txt`、`/usr/bin/python`

**影响**：判断绝对路径的方式不同，需要根据操作系统采用不同的判断规则。

#### 3. 路径大小写敏感性差异

**Windows 系统**：
- 路径不区分大小写（默认情况下）
- `C:\Users\Admin\file.txt` 和 `C:\users\admin\file.txt` 指向同一个文件

**Linux/macOS 系统**：
- 路径区分大小写
- `/home/User/file.txt` 和 `/home/user/file.txt` 是不同的路径

**影响**：在跨平台代码中，应统一使用大小写一致的路径，避免因大小写导致的错误。

#### 4. 路径长度限制差异

**Windows 系统**：
- 传统路径长度限制为 260 个字符（MAX_PATH）
- Windows 10 及更高版本支持长路径（需要启用）

**Linux/macOS 系统**：
- 路径长度限制通常为 4096 个字符（PATH_MAX）
- 实际限制可能因文件系统而异

**影响**：在 Windows 上处理超长路径时需要注意，可能需要使用特殊的前缀或启用长路径支持。

#### 5. 路径保留字符差异

**Windows 系统**：
- 保留字符：`< > : " | ? *`
- 不能用于文件名或路径中

**Linux/macOS 系统**：
- 保留字符：`/`（路径分隔符）和 `\0`（空字符）
- 其他字符通常可以使用，但某些字符（如空格）可能需要转义

**影响**：在创建文件或目录时，需要避免使用保留字符。

#### 6. 路径格式结构差异

**Windows 系统**：
- 使用盘符系统（C:、D: 等）
- 每个盘符代表一个独立的文件系统
- 路径结构：`盘符:\目录\子目录\文件`

**Linux/macOS 系统**：
- 使用统一的根目录系统
- 所有路径都从根目录 `/` 开始
- 路径结构：`/目录/子目录/文件`

**影响**：Windows 的盘符系统使得路径处理更加复杂，需要特殊处理。

#### 7. 当前目录和上级目录符号

**所有系统通用**：
- `.` 表示当前目录
- `..` 表示上级目录

**示例**：
- Windows：`.\file.txt`、`..\parent\file.txt`
- Linux/macOS：`./file.txt`、`../parent/file.txt`

**影响**：这些符号在所有系统中都通用，用于表示相对路径中的当前目录和上级目录。

### 03.1 路径拼接

`os.path.join()` 函数用于跨平台地拼接路径组件，自动处理不同操作系统的路径分隔符差异，确保生成的路径在各平台上都能正确使用。

#### 函数语法

```python
os.path.join(path1, path2, *paths)
```

- **`path1, path2, ...`**：要拼接的路径组件（字符串），可以传入多个路径参数
- **返回值**：返回一个字符串，表示拼接后的路径

#### 核心特性

1. **自动处理路径分隔符**：
   - Windows 系统：自动使用反斜杠 `\` 作为路径分隔符
   - Linux/macOS 系统：自动使用正斜杠 `/` 作为路径分隔符

2. **绝对路径处理**：
   - 如果任一参数是绝对路径，则在它之前的所有参数都会被忽略
   - 从绝对路径开始重新拼接

3. **空字符串处理**：
   - 空字符串会被忽略，不会影响路径拼接

#### 使用示例

```python
import os

# 拼接相对路径
relative_path = os.path.join('folder', 'subfolder', 'file.txt')
print(relative_path)
# Windows 输出: folder\subfolder\file.txt
# Linux/macOS 输出: folder/subfolder/file.txt

# 拼接绝对路径
absolute_path = os.path.join('/home/user', 'documents', 'file.txt')
print(absolute_path)
# Linux/macOS 输出: /home/user/documents/file.txt

# Windows 绝对路径
windows_path = os.path.join('C:\\', 'Users', 'admin', 'file.txt')
print(windows_path)
# Windows 输出: C:\Users\admin\file.txt

# 绝对路径会忽略前面的参数
mixed_path = os.path.join('folder', '/absolute', 'path', 'file.txt')
print(mixed_path)
# 输出: /absolute/path/file.txt（前面的 'folder' 被忽略）

# 空字符串处理
path_with_empty = os.path.join('folder', '', 'file.txt')
print(path_with_empty)
# 输出: folder/file.txt（空字符串被忽略）
```

#### 与手动拼接的对比

**不推荐的手动拼接方式**：

```python
# ❌ 不推荐：手动拼接路径
path = 'folder' + '\\' + 'subfolder' + '\\' + 'file.txt'  # Windows
path = 'folder' + '/' + 'subfolder' + '/' + 'file.txt'     # Linux/macOS
```

**推荐的 os.path.join() 方式**：

```python
# ✅ 推荐：使用 os.path.join()
path = os.path.join('folder', 'subfolder', 'file.txt')  # 跨平台兼容
```

> 💡 **最佳实践**：
> - 始终使用 `os.path.join()` 拼接路径，而不是手动使用字符串拼接或硬编码路径分隔符
> - 这样可以确保代码在不同操作系统上都能正确运行，提高代码的可移植性
> - 即使只在一个平台上开发，也应该养成使用 `os.path.join()` 的习惯

### 03.2 路径拆分

`os.path` 模块提供了多个函数用于拆分路径，可以分别获取路径的目录部分和文件名部分。

#### os.path.split() - 拆分路径为目录和文件名

`os.path.split(path)` 将路径拆分为目录部分和文件名部分，返回一个元组 `(目录路径, 文件名)`。

**函数语法**：

```python
os.path.split(path)
```

- **`path`**：要拆分的路径字符串
- **返回值**：返回一个元组 `(head, tail)`，其中 `head` 是目录部分，`tail` 是路径的最后一部分（文件名或目录名）
  - **重要**：如果路径以斜杠（`/` 或 `\`）结尾，`tail` 返回空字符串；否则返回最后一部分的名称（可能是文件名或目录名）

**使用示例**：

```python
import os

# 拆分文件路径
path = '/home/user/documents/file.txt'
head, tail = os.path.split(path)
print(f"目录部分: {head}")    # 输出: /home/user/documents
print(f"文件名部分: {tail}")  # 输出: file.txt

# Windows 路径拆分
windows_path = 'C:\\Users\\admin\\file.txt'
head, tail = os.path.split(windows_path)
print(f"目录部分: {head}")    # 输出: C:\Users\admin
print(f"文件名部分: {tail}")  # 输出: file.txt

# 只有文件名的情况
filename_only = 'file.txt'
head, tail = os.path.split(filename_only)
print(f"目录部分: {head}")    # 输出: （空字符串）
print(f"文件名部分: {tail}")  # 输出: file.txt

# 路径以斜杠结尾的情况（目录路径）
dir_with_slash = '/home/user/documents/'
head, tail = os.path.split(dir_with_slash)
print(f"目录部分: {head}")    # 输出: /home/user/documents
print(f"文件名部分: {tail}")  # 输出: （空字符串）

# 路径不以斜杠结尾的情况（也是目录路径）
dir_without_slash = '/home/user/documents'
head, tail = os.path.split(dir_without_slash)
print(f"目录部分: {head}")    # 输出: /home/user
print(f"文件名部分: {tail}")  # 输出: documents（注意：这里返回的是目录名，不是空字符串）
```

#### os.path.dirname() - 获取目录部分

`os.path.dirname(path)` 返回路径的目录部分，等价于 `os.path.split(path)[0]`。

**函数语法**：

```python
os.path.dirname(path)
```

- **`path`**：要获取目录的路径字符串
- **返回值**：返回路径的目录部分（字符串）

**使用示例**：

```python
import os

path = '/home/user/documents/file.txt'
directory = os.path.dirname(path)
print(directory)  # 输出: /home/user/documents

# 相对路径
relative_path = 'folder/subfolder/file.txt'
directory = os.path.dirname(relative_path)
print(directory)  # 输出: folder/subfolder
```

#### os.path.basename() - 获取路径的最后一部分

`os.path.basename(path)` 返回路径的最后一部分（文件名或目录名），等价于 `os.path.split(path)[1]`。

**函数语法**：

```python
os.path.basename(path)
```

- **`path`**：要获取最后部分的路径字符串
- **返回值**：返回路径的最后一部分（字符串）。如果路径以斜杠（`/` 或 `\`）结尾，返回空字符串

**使用示例**：

```python
import os

# 文件路径
path = '/home/user/documents/file.txt'
filename = os.path.basename(path)
print(filename)  # 输出: file.txt

# 目录路径（末尾有斜杠）- 返回空字符串
dir_path = '/home/user/documents/'
basename = os.path.basename(dir_path)
print(basename)  # 输出: （空字符串）

# 目录路径（末尾没有斜杠）- 返回目录名
dir_path_no_slash = '/home/user/documents'
basename = os.path.basename(dir_path_no_slash)
print(basename)  # 输出: documents

# 只有文件名
filename_only = 'file.txt'
basename = os.path.basename(filename_only)
print(basename)  # 输出: file.txt
```

#### 综合示例

```python
import os

# 完整路径拆分示例
full_path = '/home/user/documents/report.pdf'

# 方法一：使用 split()
directory, filename = os.path.split(full_path)
print(f"目录: {directory}")      # 输出: /home/user/documents
print(f"文件名: {filename}")      # 输出: report.pdf

# 方法二：分别使用 dirname() 和 basename()
directory = os.path.dirname(full_path)
filename = os.path.basename(full_path)
print(f"目录: {directory}")      # 输出: /home/user/documents
print(f"文件名: {filename}")      # 输出: report.pdf
```

> 💡 **提示**：
> - `os.path.split()` 返回元组，可以一次性获取目录和文件名
> - `os.path.dirname()` 获取目录部分，`os.path.basename()` 获取路径的最后一部分（可能是文件名或目录名）
> - 这些函数只对路径字符串进行操作，不会检查路径是否真实存在
> - **重要**：如果路径以斜杠（`/` 或 `\`）结尾，`os.path.basename()` 会返回空字符串，而不是目录名
> - 对于空字符串或根目录，`dirname()` 可能返回空字符串或 `.`，`basename()` 可能返回空字符串

### 03.3 获取文件名和扩展名

`os.path.splitext()` 函数用于将路径拆分为文件名部分和扩展名部分，常用于获取文件扩展名或修改文件扩展名。

#### os.path.splitext() - 分离文件名和扩展名

`os.path.splitext(path)` 将路径拆分为文件名（不含扩展名）和扩展名两部分，返回一个元组 `(文件名, 扩展名)`。

**函数语法**：

```python
os.path.splitext(path)
```

- **`path`**：要拆分的路径字符串
- **返回值**：返回一个元组 `(root, ext)`，其中 `root` 是文件名（不含扩展名）和路径部分，`ext` 是扩展名（包含点号）

**使用示例**：

```python
import os

# 基本用法：分离文件名和扩展名
path = '/home/user/documents/report.pdf'
root, ext = os.path.splitext(path)
print(f"文件名部分: {root}")    # 输出: /home/user/documents/report
print(f"扩展名部分: {ext}")     # 输出: .pdf

# 多个扩展名的情况
path2 = '/home/user/file.tar.gz'
root, ext = os.path.splitext(path2)
print(f"文件名部分: {root}")    # 输出: /home/user/file.tar
print(f"扩展名部分: {ext}")     # 输出: .gz（注意：只分离最后一个扩展名）

# 没有扩展名的文件
path3 = '/home/user/README'
root, ext = os.path.splitext(path3)
print(f"文件名部分: {root}")    # 输出: /home/user/README
print(f"扩展名部分: {ext}")     # 输出: （空字符串）

# 只有扩展名的情况（以点开头）
path4 = '/home/user/.hidden'
root, ext = os.path.splitext(path4)
print(f"文件名部分: {root}")    # 输出: /home/user/.hidden
print(f"扩展名部分: {ext}")     # 输出: （空字符串，因为点号在开头）

# 相对路径
relative_path = 'data/config.yaml'
root, ext = os.path.splitext(relative_path)
print(f"文件名部分: {root}")    # 输出: data/config
print(f"扩展名部分: {ext}")     # 输出: .yaml
```

#### 重要注意事项

1. **扩展名包含点号**：`splitext()` 返回的扩展名包含点号（如 `.pdf`），如果需要去掉点号，可以使用 `ext[1:]`

2. **只分离最后一个扩展名**：对于 `file.tar.gz` 这样的文件，`splitext()` 只会分离 `.gz`，而不是 `.tar.gz`

3. **隐藏文件处理**：以点号开头的文件（如 `.hidden`）不会被识别为扩展名，`ext` 返回空字符串

4. **路径部分保留**：`root` 部分包含完整的路径和文件名（不含扩展名），不仅仅是文件名

> 💡 **提示**：
> - `os.path.splitext()` 只对路径字符串进行操作，不检查文件是否真实存在
> - 如果需要获取纯文件名（不含路径），可以结合使用 `os.path.basename()` 和 `os.path.splitext()`
> - 示例：`os.path.splitext(os.path.basename('/path/to/file.txt'))` 返回 `('file', '.txt')`

### 03.4 获取绝对路径

`os.path.abspath()` 函数用于将给定的路径转换为规范化的绝对路径。如果提供的路径是相对路径，该函数会将其转换为基于当前工作目录的绝对路径；如果提供的是绝对路径，则返回该路径的规范化形式。

#### os.path.abspath() - 获取绝对路径

**函数语法**：

```python
os.path.abspath(path)
```

- **`path`**：要转换的路径字符串，可以是相对路径或绝对路径
- **返回值**：返回 `path` 的绝对路径字符串（规范化后的）

#### 工作原理

`os.path.abspath(path)` 在大多数平台上等价于：

```python
os.path.normpath(os.path.join(os.getcwd(), path))
```

即：将当前工作目录与提供的路径拼接后，进行路径规范化处理。

> 💡 **提示**：关于 `os.path.normpath()` 函数的详细说明，请查看 [03.5 规范化路径](#035-规范化路径) 章节。

#### 使用示例

**假设场景**：假设你的 Python 脚本在 `/home/user/project` 目录下运行，当前工作目录为 `/home/user/project`。

```python
import os

# 获取当前工作目录的绝对路径
current_dir = os.path.abspath('.')
print(f"当前目录的绝对路径: {current_dir}")
# 输出: 当前目录的绝对路径: /home/user/project

# 获取上级目录的绝对路径
parent_dir = os.path.abspath('..')
print(f"上级目录的绝对路径: {parent_dir}")
# 输出: 上级目录的绝对路径: /home/user

# 将相对路径转换为绝对路径
relative_path = 'subdir/file.txt'
absolute_path = os.path.abspath(relative_path)
print(f"相对路径 '{relative_path}' 的绝对路径: {absolute_path}")
# 输出: 相对路径 'subdir/file.txt' 的绝对路径: /home/user/project/subdir/file.txt

# 处理包含上级目录的相对路径
relative_path_with_parent = '../config/settings.yaml'
absolute_path_with_parent = os.path.abspath(relative_path_with_parent)
print(f"相对路径 '{relative_path_with_parent}' 的绝对路径: {absolute_path_with_parent}")
# 输出: 相对路径 '../config/settings.yaml' 的绝对路径: /home/user/config/settings.yaml

# 如果已经是绝对路径，则返回规范化后的绝对路径
absolute_input = '/home/user/../documents/file.txt'
normalized = os.path.abspath(absolute_input)
print(f"规范化后的绝对路径: {normalized}")
# 输出: 规范化后的绝对路径: /home/documents/file.txt

# Windows 路径示例
# 假设场景：在 Windows 系统上，当前工作目录为 E:\Projects\MyApp
windows_relative = 'data\\config.ini'
windows_absolute = os.path.abspath(windows_relative)
print(f"Windows 相对路径的绝对路径: {windows_absolute}")
# 输出: Windows 相对路径的绝对路径: E:\Projects\MyApp\data\config.ini
```

#### 重要特性

1. **不检查路径是否存在**：`os.path.abspath()` 仅对路径字符串进行处理，不会验证路径或文件是否实际存在

2. **依赖当前工作目录**：对于相对路径，`os.path.abspath()` 的结果依赖于当前的工作目录。如果在不同的工作目录下运行相同的代码，返回的绝对路径也会有所不同

3. **自动路径规范化**：函数会自动处理路径中的 `.` 和 `..`，返回规范化的绝对路径

4. **跨平台兼容**：`os.path` 模块会根据操作系统自动处理路径分隔符的差异（Windows 使用 `\`，Linux/macOS 使用 `/`）

5. **不解析符号链接**：`os.path.abspath()` 不会解析路径中的符号链接（symlinks）。如果需要获取路径的真实绝对路径（解析符号链接），可以使用 `os.path.realpath()` 函数

#### 与 os.path.realpath() 的区别

- **`os.path.abspath(path)`**：将给定路径转换为绝对路径，但不解析符号链接
- **`os.path.realpath(path)`**：将给定路径转换为绝对路径，并解析路径中的所有符号链接，返回最终的目标路径

**示例对比**：

```python
import os

# 假设存在符号链接 /home/user/shortcut.txt 指向 /home/user/documents/report.txt
symlink_path = '/home/user/shortcut.txt'

# 使用 abspath() - 不解析符号链接
absolute_path = os.path.abspath(symlink_path)
print(f"绝对路径: {absolute_path}")  # 输出: /home/user/shortcut.txt

# 使用 realpath() - 解析符号链接
real_path = os.path.realpath(symlink_path)
print(f"真实路径: {real_path}")  # 输出: /home/user/documents/report.txt
```

#### 注意事项

1. **工作目录的影响**：由于 `os.path.abspath()` 依赖当前工作目录，在调用前应确保工作目录是正确的，或者使用绝对路径作为输入

2. **路径不存在的情况**：即使路径不存在，`os.path.abspath()` 也会返回一个绝对路径，不会抛出异常

3. **符号链接处理**：如果需要处理符号链接，应使用 `os.path.realpath()` 而不是 `os.path.abspath()`

4. **性能考虑**：`os.path.abspath()` 只进行字符串操作，性能开销很小；而 `os.path.realpath()` 需要访问文件系统来解析符号链接，性能开销相对较大

> 💡 **最佳实践**：
> - 在处理文件路径时，使用 `os.path.abspath()` 可以确保路径的一致性和准确性
> - 特别是在需要将相对路径转换为绝对路径的情况下，使用 `os.path.abspath()` 可以避免因相对路径导致的潜在问题
> - 如果需要获取符号链接的真实路径，应使用 `os.path.realpath()` 而不是 `os.path.abspath()`

### 03.5 规范化路径

`os.path.normpath()` 函数用于规范化路径名，消除路径中的冗余部分，如多余的斜杠、当前目录符号（`.`）和上级目录符号（`..`），从而生成一个标准化的路径表示。

#### os.path.normpath() - 规范化路径

**函数语法**：

```python
os.path.normpath(path)
```

- **`path`**：要规范化的路径字符串
- **返回值**：返回规范化后的路径字符串

#### 核心功能

`os.path.normpath()` 会执行以下规范化操作：

1. **消除冗余分隔符**：将多个连续的斜杠或反斜杠合并为一个
2. **解析当前目录符号**：处理路径中的 `.`（当前目录），简化路径
3. **解析上级目录符号**：处理路径中的 `..`（上级目录），向上导航并简化路径
4. **跨平台处理**：在 Windows 上将正斜杠转换为反斜杠，在 Linux/macOS 上保持正斜杠

#### 使用示例

```python
import os

# 示例 1：处理多余的斜杠和 . 符号
path1 = '/home//user/./Documents/../Downloads'
normalized1 = os.path.normpath(path1)
print(f"原始路径: {path1}")
print(f"规范化后: {normalized1}")
# 输出: 原始路径: /home//user/./Documents/../Downloads
# 输出: 规范化后: /home/user/Downloads（Linux/macOS）或 \home\user\Downloads（Windows）

# 示例 2：处理 .. 符号
path2 = '/home/user/../user/documents/../../Downloads'
normalized2 = os.path.normpath(path2)
print(f"原始路径: {path2}")
print(f"规范化后: {normalized2}")
# 输出: 原始路径: /home/user/../user/documents/../../Downloads
# 输出: 规范化后: /Downloads（Linux/macOS）或 \home\Downloads（Windows）

# 示例 3：Windows 路径规范化
windows_path = 'C:\\Users\\..\\Users\\admin\\Documents'
normalized3 = os.path.normpath(windows_path)
print(f"原始路径: {windows_path}")
print(f"规范化后: {normalized3}")
# 输出: 原始路径: C:\Users\..\Users\admin\Documents
# 输出: 规范化后: C:\Users\admin\Documents

# 示例 4：处理混合分隔符（Windows）
mixed_path = 'C:/Users/admin/Documents'
normalized4 = os.path.normpath(mixed_path)
print(f"原始路径: {mixed_path}")
print(f"规范化后: {normalized4}")
# 输出: 原始路径: C:/Users/admin/Documents
# 输出: 规范化后: C:\Users\admin\Documents

# 示例 5：相对路径规范化
relative_path = '../config/./settings.yaml'
normalized5 = os.path.normpath(relative_path)
print(f"原始路径: {relative_path}")
print(f"规范化后: {normalized5}")
# 输出: 原始路径: ../config/./settings.yaml
# 输出: 规范化后: ..\config\settings.yaml（Windows）或 ../config/settings.yaml（Linux/macOS）

# 示例 6：处理末尾斜杠
path_with_trailing = '/home/user/documents/'
normalized6 = os.path.normpath(path_with_trailing)
print(f"原始路径: {path_with_trailing}")
print(f"规范化后: {normalized6}")
# 输出: 原始路径: /home/user/documents/
# 输出: 规范化后: /home/user/documents（Linux/macOS）或 \home\user\documents（Windows）
```

#### 重要特性

1. **仅字符串操作**：`os.path.normpath()` 只对路径字符串进行处理，不会检查路径是否真实存在于文件系统中

2. **不解析符号链接**：函数不会解析路径中的符号链接（symlinks），只进行字符串级别的规范化

3. **不转换为绝对路径**：`os.path.normpath()` 不会将相对路径转换为绝对路径，它只规范化路径的格式

4. **跨平台兼容**：函数会根据运行的操作系统自动处理路径分隔符的差异

5. **保留路径类型**：规范化后的路径类型（绝对路径或相对路径）与输入路径保持一致

#### 注意事项

1. **路径不存在的情况**：即使路径不存在，`os.path.normpath()` 也会返回规范化后的路径，不会抛出异常

2. **符号链接处理**：如果需要解析符号链接，应使用 `os.path.realpath()` 而不是 `os.path.normpath()`

3. **路径安全性**：规范化后的路径可能改变包含符号链接的路径的含义，在处理用户输入时应谨慎使用

4. **Windows 特殊处理**：在 Windows 上，`os.path.normpath()` 会将正斜杠转换为反斜杠，并处理盘符路径

> 💡 **提示**：
> - `os.path.normpath()` 常用于清理用户输入的路径或处理拼接后的路径
> - 如果需要获取绝对路径，应使用 `os.path.abspath()` 而不是 `os.path.normpath()`
> - 规范化路径可以提高路径的可读性和一致性，便于路径比较和处理

### 03.6 路径存在性检查

> 📝 **说明**：写到这里才发现，前面章节的内容过于详细了，其实没必要写那么啰嗦。从本章节开始，我将采用更简洁的表述方式，重点突出核心功能和用法即可。

`os.path.exists(path)` 函数用于检查指定的路径（文件或目录）是否真实存在于文件系统中。

**函数语法**：

```python
os.path.exists(path)
```

- **`path`**：要检查的路径字符串，可以是文件路径或目录路径，可以是绝对路径或相对路径
- **返回值**：如果路径存在返回 `True`，不存在返回 `False`（布尔值）

**核心特性**：
- 可以检查文件或目录是否存在，不区分类型
- 如果路径是符号链接，会检查符号链接指向的目标是否存在
- 如果路径存在但当前用户没有访问权限，可能返回 `False`

**使用示例**：

```python
import os

# 检查文件是否存在
file_exists = os.path.exists("config.ini")
print(f"文件存在: {file_exists}")
# 输出: 文件存在: True（如果文件存在）或 False（如果文件不存在）

# 检查目录是否存在
dir_exists = os.path.exists("data")
print(f"目录存在: {dir_exists}")
# 输出: 目录存在: True（如果目录存在）或 False（如果目录不存在）

# 检查不存在的路径
not_exists = os.path.exists("non_existent_file.txt")
print(f"路径存在: {not_exists}")
# 输出: 路径存在: False

# 在文件操作前检查
target_file = "important_data.txt"
if os.path.exists(target_file):
    print("文件存在，可以继续操作")
else:
    print("文件不存在，需要先创建")
# 输出: 文件存在，可以继续操作（如果存在）
# 或: 文件不存在，需要先创建（如果不存在）
```

**与相关函数的区别**：
- **`os.path.exists(path)`**：检查路径是否存在（不区分是文件还是目录）
- **`os.path.isfile(path)`**：检查路径是否存在且是文件
- **`os.path.isdir(path)`**：检查路径是否存在且是目录

> 💡 **提示**：如果需要区分文件和目录，应使用 `os.path.isfile()` 或 `os.path.isdir()` 而不是仅使用 `os.path.exists()`。

### 03.7 路径类型判断

`os.path` 模块提供了多个函数用于判断路径的类型，可以区分文件、目录和符号链接。

#### os.path.isfile() - 检查是否为文件

**函数语法**：

```python
os.path.isfile(path)
```

- **`path`**：要检查的路径字符串
- **返回值**：如果路径存在且是文件返回 `True`，否则返回 `False`

**使用示例**：

```python
import os

# 检查是否为文件
is_file = os.path.isfile("config.ini")
print(f"是文件: {is_file}")
# 输出: 是文件: True（如果是文件）或 False（如果不是文件或不存在）

# 检查目录（不是文件）
is_file = os.path.isfile("data")
print(f"是文件: {is_file}")
# 输出: 是文件: False
```

#### os.path.isdir() - 检查是否为目录

**函数语法**：

```python
os.path.isdir(path)
```

- **`path`**：要检查的路径字符串
- **返回值**：如果路径存在且是目录返回 `True`，否则返回 `False`

**使用示例**：

```python
import os

# 检查是否为目录
is_dir = os.path.isdir("data")
print(f"是目录: {is_dir}")
# 输出: 是目录: True（如果是目录）或 False（如果不是目录或不存在）

# 检查文件（不是目录）
is_dir = os.path.isdir("config.ini")
print(f"是目录: {is_dir}")
# 输出: 是目录: False
```

#### os.path.islink() - 检查是否为符号链接

**函数语法**：

```python
os.path.islink(path)
```

- **`path`**：要检查的路径字符串
- **返回值**：如果路径是符号链接返回 `True`，否则返回 `False`

**使用示例**：

```python
import os

# 检查是否为符号链接
is_link = os.path.islink("symlink_file")
print(f"是符号链接: {is_link}")
# 输出: 是符号链接: True（如果是符号链接）或 False（如果不是符号链接或不存在）
```

**综合示例**：

```python
import os

def check_path_type(path):
    """检查路径类型"""
    if os.path.isfile(path):
        return "文件"
    elif os.path.isdir(path):
        return "目录"
    elif os.path.islink(path):
        return "符号链接"
    else:
        return "不存在"

# 使用示例
print(check_path_type("config.ini"))  # 输出: 文件（如果存在）
print(check_path_type("data"))         # 输出: 目录（如果存在）
print(check_path_type("nonexistent"))  # 输出: 不存在
```

> 💡 **提示**：
> - `os.path.isfile()` 和 `os.path.isdir()` 会检查路径是否存在，如果路径不存在，两者都返回 `False`
> - `os.path.islink()` 只检查路径本身是否为符号链接，不检查符号链接指向的目标是否存在
> - **重要**：`os.path.isfile()` 和 `os.path.isdir()` 会**跟踪符号链接**（follow symlinks），检查符号链接指向的目标类型。因此，对于同一个符号链接路径，`os.path.islink()` 和 `os.path.isfile()`（或 `os.path.isdir()`）可能同时返回 `True`

### 03.8 获取文件信息

`os.path` 模块提供了多个函数用于获取文件的基本信息，如文件大小、修改时间、创建时间和访问时间。

#### os.path.getsize() - 获取文件大小

**函数语法**：

```python
os.path.getsize(path)
```

- **`path`**：文件路径字符串
- **返回值**：文件大小（以字节为单位，整数）

**使用示例**：

```python
import os

# 获取文件大小
file_size = os.path.getsize("config.ini")
print(f"文件大小: {file_size} 字节")
# 输出: 文件大小: 1024 字节（示例）

# 转换为更易读的格式
def format_size(size_bytes):
    """格式化文件大小"""
    for unit in ['B', 'KB', 'MB', 'GB']:
        if size_bytes < 1024.0:
            return f"{size_bytes:.2f} {unit}"
        size_bytes /= 1024.0
    return f"{size_bytes:.2f} TB"

size = os.path.getsize("config.ini")
print(f"文件大小: {format_size(size)}")
# 输出: 文件大小: 1.00 KB（示例）
```

#### os.path.getmtime() - 获取修改时间

**函数语法**：

```python
os.path.getmtime(path)
```

- **`path`**：文件路径字符串
- **返回值**：文件最后修改时间（时间戳，浮点数）

**使用示例**：

```python
import os
from datetime import datetime

# 获取修改时间（时间戳）
mtime = os.path.getmtime("config.ini")
print(f"修改时间戳: {mtime}")
# 输出: 修改时间戳: 1704067200.0（示例）

# 转换为可读格式
mtime_readable = datetime.fromtimestamp(mtime)
print(f"修改时间: {mtime_readable}")
# 输出: 修改时间: 2024-01-01 12:00:00（示例）
```

#### os.path.getctime() - 获取创建时间

**函数语法**：

```python
os.path.getctime(path)
```

- **`path`**：文件路径字符串
- **返回值**：文件创建时间（时间戳，浮点数）

**使用示例**：

```python
import os
from datetime import datetime

# 获取创建时间（时间戳）
ctime = os.path.getctime("config.ini")
print(f"创建时间戳: {ctime}")
# 输出: 创建时间戳: 1704067200.0（示例）

# 转换为可读格式
ctime_readable = datetime.fromtimestamp(ctime)
print(f"创建时间: {ctime_readable}")
# 输出: 创建时间: 2024-01-01 12:00:00（示例）
```

> 💡 **注意**：在 Windows 上，`getctime()` 返回创建时间；在 Linux/macOS 上，返回的是元数据最后修改时间（可能不是真正的创建时间）。
> 
> **什么是元数据？** 元数据（Metadata）是关于数据的数据，用于描述文件的属性和信息。在文件系统中，元数据包括文件名、大小、创建时间、修改时间、访问时间、权限、所有者等。在 Linux/Unix 系统中，元数据存储在 inode（索引节点）结构中；在 Windows 系统中，元数据存储在文件的属性中。当文件的元数据（如权限、所有者）被修改时，元数据修改时间会更新，但文件内容可能并未改变。

#### os.path.getatime() - 获取访问时间

**函数语法**：

```python
os.path.getatime(path)
```

- **`path`**：文件路径字符串
- **返回值**：文件最后访问时间（时间戳，浮点数）

**使用示例**：

```python
import os
from datetime import datetime

# 获取访问时间（时间戳）
atime = os.path.getatime("config.ini")
print(f"访问时间戳: {atime}")
# 输出: 访问时间戳: 1704067200.0（示例）

# 转换为可读格式
atime_readable = datetime.fromtimestamp(atime)
print(f"访问时间: {atime_readable}")
# 输出: 访问时间: 2024-01-01 12:00:00（示例）
```

**综合示例**：

```python
import os
from datetime import datetime

def get_file_info(filepath):
    """获取文件的完整信息"""
    if not os.path.exists(filepath):
        return "文件不存在"
    
    info = {
        "大小": f"{os.path.getsize(filepath)} 字节",
        "修改时间": datetime.fromtimestamp(os.path.getmtime(filepath)),
        "创建时间": datetime.fromtimestamp(os.path.getctime(filepath)),
        "访问时间": datetime.fromtimestamp(os.path.getatime(filepath))
    }
    return info

# 使用示例
file_info = get_file_info("config.ini")
for key, value in file_info.items():
    print(f"{key}: {value}")
# 输出示例:
# 大小: 1024 字节
# 修改时间: 2024-01-01 12:00:00
# 创建时间: 2024-01-01 10:00:00
# 访问时间: 2024-01-01 15:00:00
```

> 💡 **提示**：
> - 所有时间函数返回的都是时间戳（自1970年1月1日以来的秒数，浮点数）
> - 使用 `datetime.fromtimestamp()` 可以将时间戳转换为可读的日期时间格式
> - `os.path.getsize()` 对于目录可能返回不一致的结果，建议先使用 `os.path.isdir()` 判断
>   - **为什么目录返回不一致？** `os.path.getsize()` 主要设计用于文件，对目录的行为取决于操作系统和文件系统：
>     - **目录大小的定义不一致**：目录本身占用的空间可能仅包含元数据（如目录项列表），而不包括其包含的文件和子目录的大小
>     - **操作系统差异**：在某些系统上可能返回目录的元数据大小，在某些系统上可能返回 0 或固定字节数，甚至可能引发异常
>     - **文件系统实现差异**：不同文件系统对目录大小的计算方式不同，有些可能固定为一个块的大小，有些可能根据目录项数量动态变化
>     - **目录被视为特殊文件**：在某些系统中，目录被视为包含文件列表的特殊文件，其大小仅反映该列表所占的空间，而非目录内所有文件的总和
>   - **正确做法**：如果需要获取目录的总大小，应使用 `os.walk()` 递归遍历目录，累加其中所有文件的大小
> - 如果文件不存在，这些函数会抛出 `OSError` 异常，建议先使用 `os.path.exists()` 检查

## 04. 文件权限和属性

### 04.1 修改文件权限

`os.chmod()` 函数用于修改文件或目录的权限。

**函数语法**：

```python
os.chmod(path, mode)
```

- **`path`**：要修改权限的文件或目录路径字符串
- **`mode`**：权限模式，可以是八进制数（如 `0o755`）或使用 `stat` 模块的权限常量组合
- **返回值**：无返回值，修改成功不返回任何内容；失败时抛出 `OSError` 异常

**权限模式说明**：

权限模式由三组权限位组成，分别对应所有者（user）、用户组（group）和其他用户（other）：
- **读权限（r）**：值为 4
- **写权限（w）**：值为 2
- **执行权限（x）**：值为 1

**使用示例**：

```python
import os
import stat

# 使用八进制数设置权限
os.chmod("script.sh", 0o755)  # 所有者：读写执行(7)，用户组和其他：读执行(5)
print("权限修改成功")

# 使用 stat 模块的常量组合权限
os.chmod("config.ini", stat.S_IRUSR | stat.S_IWUSR)  # 所有者：读写权限
print("权限修改成功")

# 设置目录权限
os.chmod("data", 0o755)
print("目录权限修改成功")
```

**常用权限模式**：
- `0o777`：所有用户都有读、写、执行权限
- `0o755`：所有者有全部权限，用户组和其他用户有读和执行权限（常用于可执行文件）
- `0o644`：所有者有读写权限，用户组和其他用户只有读权限（常用于普通文件）
- `0o600`：只有所有者有读写权限（常用于敏感文件）

> 💡 **提示**：
> - `os.chmod()` 在 Windows 上的行为与 Linux/macOS 不同，Windows 主要支持只读属性的修改
> - 对于符号链接，`os.chmod()` 会修改符号链接指向的目标文件的权限
> - 如果没有足够的权限修改文件，会抛出 `PermissionError` 异常
> - 建议在修改权限前先检查文件是否存在，使用 `os.path.exists()` 或 `os.path.isfile()`

### 04.2 修改文件所有者

`os.chown()` 函数用于修改文件或目录的所有者和组 ID。

**函数语法**：

```python
os.chown(path, uid, gid)
```

- **`path`**：要修改所有者的文件或目录路径字符串
- **`uid`**：新的所有者用户 ID（整数），设置为 `-1` 表示不修改所有者
- **`gid`**：新的组 ID（整数），设置为 `-1` 表示不修改组
- **返回值**：无返回值，修改成功不返回任何内容；失败时抛出 `OSError` 异常

**使用示例**：

```python
import os

# 修改文件的所有者和组
os.chown("script.sh", 1000, 1000)  # 将所有者改为 UID 1000，组改为 GID 1000
print("所有者修改成功")

# 只修改所有者，不修改组（使用 -1 保持组不变）
os.chown("config.ini", 1000, -1)
print("所有者修改成功")

# 只修改组，不修改所有者
os.chown("data.txt", -1, 1000)
print("组修改成功")

# 修改目录的所有者
os.chown("data", 1000, 1000)
print("目录所有者修改成功")
```

**获取用户 ID 和组 ID**：

```python
import os
import pwd
import grp

# 通过用户名获取用户 ID
username = "admin"
uid = pwd.getpwnam(username).pw_uid

# 通过组名获取组 ID
groupname = "users"
gid = grp.getgrnam(groupname).gr_gid

# 修改文件所有者
os.chown("file.txt", uid, gid)
```

> 💡 **提示**：
> - `os.chown()` 仅在类 Unix 系统（Linux、macOS）上可用，在 Windows 上不可用
> - 修改文件所有者通常需要超级用户权限（root），否则会抛出 `PermissionError` 异常
> - 对于符号链接，`os.chown()` 会修改符号链接指向的目标文件的所有者；如需修改符号链接本身，可使用 `os.lchown()`
> - 使用 `-1` 作为 `uid` 或 `gid` 参数可以保持对应的值不变
> - 建议在修改前先检查文件是否存在，使用 `os.path.exists()` 或 `os.path.isfile()`

### 04.3 获取文件状态信息

`os.stat()` 函数用于获取文件或目录的详细状态信息。

**函数语法**：

```python
os.stat(path, *, follow_symlinks=True)
```

- **`path`**：要获取状态信息的文件或目录路径字符串
- **`follow_symlinks`**：是否跟随符号链接，默认为 `True`（跟随符号链接获取目标文件信息）
- **返回值**：返回一个 `os.stat_result` 对象，包含文件的详细信息

**stat_result 对象常用属性**：

- **`st_size`**：文件大小（字节）
- **`st_mtime`**：最后修改时间（时间戳）
- **`st_ctime`**：创建时间或元数据修改时间（时间戳）
- **`st_atime`**：最后访问时间（时间戳）
- **`st_mode`**：文件类型和权限模式
- **`st_uid`**：所有者用户 ID（Unix）
- **`st_gid`**：所有者组 ID（Unix）

**使用示例**：

```python
import os
from datetime import datetime

# 获取文件状态信息
file_stat = os.stat("config.ini")

# 获取文件大小
file_size = file_stat.st_size
print(f"文件大小: {file_size} 字节")

# 获取修改时间
mtime = datetime.fromtimestamp(file_stat.st_mtime)
print(f"修改时间: {mtime}")

# 获取创建时间
ctime = datetime.fromtimestamp(file_stat.st_ctime)
print(f"创建时间: {ctime}")

# 获取访问时间
atime = datetime.fromtimestamp(file_stat.st_atime)
print(f"访问时间: {atime}")
```

**相关函数**：

- **`os.lstat(path)`**：类似 `os.stat()`，但不跟随符号链接，返回符号链接本身的信息
- **`os.fstat(fd)`**：通过文件描述符获取文件状态信息

**使用示例**：

```python
import os

# 获取符号链接本身的信息（不跟随链接）
link_stat = os.lstat("symlink_file")
print(f"符号链接大小: {link_stat.st_size}")

# 通过文件描述符获取文件信息
with open("file.txt", "r") as f:
    file_stat = os.fstat(f.fileno())
    print(f"文件大小: {file_stat.st_size} 字节")
```

> 💡 **提示**：
> - `os.stat()` 会跟随符号链接获取目标文件的信息；如需获取符号链接本身的信息，使用 `os.lstat()`
> - 如果文件不存在，会抛出 `FileNotFoundError` 异常
> - 如果没有权限访问文件，会抛出 `PermissionError` 异常
> - 在 Windows 上，`st_ctime` 表示创建时间；在 Linux/macOS 上，表示元数据修改时间
> - 使用 `stat` 模块可以解析 `st_mode` 属性，获取文件类型和权限信息

## 05. 进程管理

### 05.1 获取进程 ID

`os.getpid()` 和 `os.getppid()` 函数用于获取进程 ID 信息。

#### os.getpid() - 获取当前进程 ID

**函数语法**：

```python
os.getpid()
```

- **参数**：无参数
- **返回值**：返回当前进程的进程 ID（PID，整数）

**使用示例**：

```python
import os

# 获取当前进程 ID
pid = os.getpid()
print(f"当前进程 ID: {pid}")
# 输出: 当前进程 ID: 12345（示例）
```

#### os.getppid() - 获取父进程 ID

**函数语法**：

```python
os.getppid()
```

- **参数**：无参数
- **返回值**：返回当前进程的父进程 ID（PPID，整数）

**使用示例**：

```python
import os

# 获取当前进程 ID
pid = os.getpid()
print(f"当前进程 ID: {pid}")

# 获取父进程 ID
ppid = os.getppid()
print(f"父进程 ID: {ppid}")
# 输出示例:
# 当前进程 ID: 12345
# 父进程 ID: 12340
```

**综合示例**：

```python
import os

def show_process_info():
    """显示进程信息"""
    pid = os.getpid()
    ppid = os.getppid()
    print(f"当前进程 ID: {pid}")
    print(f"父进程 ID: {ppid}")

show_process_info()
```

> 💡 **提示**：
> - 进程 ID（PID）是操作系统分配给每个进程的唯一标识符
> - 父进程 ID（PPID）是创建当前进程的进程的 ID
> - 这两个函数在所有平台上都可用，返回值是整数
> - 进程 ID 在进程生命周期内保持不变，进程结束后该 ID 可能被其他进程重用
> - 在多进程编程中，进程 ID 常用于进程间通信和进程管理

### 05.2 执行系统命令

`os.system()` 函数用于在子 shell 中执行系统命令。

**函数语法**：

```python
os.system(command)
```

- **`command`**：要执行的系统命令字符串
- **返回值**：返回命令的退出状态码（整数），0 表示成功，非 0 表示失败

**使用示例**：

```python
import os

# 在 Windows 上执行命令
exit_code = os.system("dir")
print(f"命令退出状态码: {exit_code}")
# 输出: 命令退出状态码: 0（如果成功）

# 在 Linux/macOS 上执行命令
exit_code = os.system("ls -l")
print(f"命令退出状态码: {exit_code}")

# 执行带参数的命令
exit_code = os.system("echo Hello World")
print(f"命令退出状态码: {exit_code}")
```

**检查命令执行结果**：

```python
import os

# 执行命令并检查结果
exit_code = os.system("python --version")
if exit_code == 0:
    print("命令执行成功")
else:
    print(f"命令执行失败，退出状态码: {exit_code}")
```

**跨平台示例**：

```python
import os
import sys

def list_files():
    """跨平台列出文件"""
    if sys.platform == "win32":
        os.system("dir")
    else:
        os.system("ls -l")

list_files()
```

> 💡 **提示**：
> - `os.system()` 会阻塞当前进程，直到命令执行完成
> - 返回值是命令的退出状态码，0 通常表示成功，非 0 表示失败
> - 无法直接获取命令的输出，命令的输出会直接显示在终端
> - 不同操作系统的命令可能不同，需要注意跨平台兼容性
> - **安全提示**：`os.system()` 存在安全风险，如果命令字符串来自用户输入，可能导致命令注入攻击
> - **推荐替代**：对于需要获取命令输出或更复杂的控制，建议使用 `subprocess` 模块（如 `subprocess.run()`、`subprocess.Popen()`）

### 05.3 创建子进程

`os.fork()` 函数用于在类 Unix 系统上创建子进程。

**函数语法**：

```python
os.fork()
```

- **参数**：无参数
- **返回值**：返回两次
  - 在父进程中：返回子进程的进程 ID（PID，整数）
  - 在子进程中：返回 0

**子进程执行的内容**：

`os.fork()` 会复制父进程的整个内存空间（包括代码、数据、变量等），创建子进程。子进程从 `os.fork()` 调用后的下一行代码开始执行，默认会执行与父进程相同的代码。

由于子进程是父进程的完整复制，它继承了：
- 父进程的所有代码
- 父进程的所有变量和数据
- 父进程的文件描述符
- 父进程的环境变量

为了让子进程执行不同的任务，需要通过判断 `os.fork()` 的返回值来区分父进程和子进程，并在各自的代码分支中执行不同的逻辑。

**使用示例**：

```python
import os

# 创建子进程
pid = os.fork()

if pid == 0:
    # 子进程代码
    print(f"子进程：PID 为 {os.getpid()}, 父进程 PID 为 {os.getppid()}")
else:
    # 父进程代码
    print(f"父进程：PID 为 {os.getpid()}, 子进程 PID 为 {pid}")
```

**等待子进程完成**：

```python
import os

pid = os.fork()

if pid == 0:
    # 子进程执行任务
    print("子进程正在执行任务...")
    os._exit(0)  # 子进程退出
else:
    # 父进程等待子进程完成
    child_pid, status = os.wait()
    print(f"子进程 {child_pid} 已完成，退出状态码: {status}")
```

**注意事项**：

- `os.fork()` 会复制当前进程的内存空间，创建完全独立的子进程
- 子进程从 `os.fork()` 返回后开始执行，与父进程并发运行
- 子进程需要使用 `os._exit()` 退出，而不是 `sys.exit()`，以避免影响父进程

> 💡 **提示**：
> - `os.fork()` 仅在类 Unix 系统（Linux、macOS）上可用，在 Windows 上不可用
> - 创建子进程后，父进程和子进程会并发执行，需要根据返回值区分执行不同的代码
> - 父进程应使用 `os.wait()` 或 `os.waitpid()` 等待子进程完成，避免产生僵尸进程
> - **跨平台推荐**：对于需要跨平台的多进程编程，建议使用 `multiprocessing` 模块，它提供了更高级的接口和更好的跨平台支持
> - `os.fork()` 会复制整个进程的内存空间，对于大型程序可能消耗较多资源

## 06. 系统信息获取

### 06.1 获取操作系统名称

`os.name` 属性用于获取当前操作系统的名称。

**属性说明**：

```python
os.name
```

- **类型**：字符串属性（不是函数，无需调用）
- **返回值**：操作系统名称字符串
  - `'posix'`：类 Unix 系统（Linux、macOS、Unix 等）
  - `'nt'`：Windows 系统
  - `'java'`：Java 虚拟机（Jython）

**使用示例**：

```python
import os

# 获取操作系统名称
os_type = os.name
print(f"操作系统类型: {os_type}")
# 输出: 操作系统类型: posix（Linux/macOS）或 nt（Windows）

# 根据操作系统类型执行不同操作
if os.name == 'nt':
    print("当前运行在 Windows 系统上")
elif os.name == 'posix':
    print("当前运行在类 Unix 系统上（Linux/macOS）")
else:
    print(f"当前运行在 {os.name} 系统上")
```

**跨平台条件判断示例**：

```python
import os

# 根据操作系统选择不同的命令
if os.name == 'nt':
    command = "dir"
else:
    command = "ls -l"

os.system(command)
```

> 💡 **提示**：
> - `os.name` 是一个属性，不是函数，使用时不需要加括号
> - `os.name` 只能区分大类操作系统（Windows、Unix），无法区分具体的操作系统版本
> - **更精确的检测**：如果需要更详细的操作系统信息，建议使用 `sys.platform`（如 `'win32'`、`'linux'`、`'darwin'`）或 `platform` 模块
> - `os.name` 主要用于简单的跨平台判断，对于复杂的平台检测，建议使用 `platform` 模块

### 06.2 获取系统配置参数

`os` 模块提供了多个函数用于获取系统配置参数。

#### os.cpu_count() - 获取 CPU 核心数

**函数语法**：

```python
os.cpu_count()
```

- **参数**：无参数
- **返回值**：返回 CPU 的核心数（整数），如果无法确定则返回 `None`

**使用示例**：

```python
import os

# 获取 CPU 核心数
cpu_count = os.cpu_count()
print(f"CPU 核心数: {cpu_count}")
# 输出: CPU 核心数: 8（示例）
```

#### os.uname() - 获取系统信息（Unix/Linux）

**函数语法**：

```python
os.uname()
```

- **参数**：无参数
- **返回值**：返回一个包含系统信息的元组 `(sysname, nodename, release, version, machine)`
  - `sysname`：操作系统名称
  - `nodename`：主机名
  - `release`：操作系统版本
  - `version`：系统版本详细信息
  - `machine`：硬件架构

**使用示例**：

```python
import os

# 获取系统信息（仅在 Unix/Linux 上可用）
if hasattr(os, 'uname'):
    sys_info = os.uname()
    print(f"操作系统: {sys_info.sysname}")
    print(f"主机名: {sys_info.nodename}")
    print(f"版本: {sys_info.release}")
    print(f"架构: {sys_info.machine}")
```

#### os.get_terminal_size() - 获取终端大小

**函数语法**：

```python
os.get_terminal_size(fd=None)
```

- **`fd`**：文件描述符，默认为 `None`（使用标准输出）
- **返回值**：返回一个 `os.terminal_size` 对象，包含 `columns`（列数）和 `lines`（行数）属性

**使用示例**：

```python
import os

# 获取终端大小
size = os.get_terminal_size()
print(f"终端大小: {size.columns} 列 x {size.lines} 行")
# 输出: 终端大小: 80 列 x 24 行（示例）
```

> 💡 **提示**：
> - `os.cpu_count()` 在所有平台上都可用，常用于多进程编程时确定工作进程数量
> - `os.uname()` 仅在类 Unix 系统（Linux、macOS）上可用，在 Windows 上不可用
> - `os.get_terminal_size()` 在所有平台上都可用，但如果没有连接到终端可能引发异常
> - 对于更详细的系统信息，建议使用 `platform` 模块，它提供了更丰富的跨平台系统信息获取功能

## 07. 文件描述符操作

### 07.1 打开文件描述符

`os.open()` 函数用于打开文件并返回文件描述符（底层接口）。

**函数语法**：

```python
os.open(path, flags, mode=0o777)
```

- **`path`**：要打开的文件路径字符串
- **`flags`**：文件打开标志位（整数），使用 `os` 模块的常量组合
- **`mode`**：文件权限模式（八进制数），仅在创建文件时有效，默认为 `0o777`
- **返回值**：返回文件描述符（整数），用于后续的文件操作

**常用标志位**：

- **`os.O_RDONLY`**：只读模式
- **`os.O_WRONLY`**：只写模式
- **`os.O_RDWR`**：读写模式
- **`os.O_CREAT`**：如果文件不存在则创建
- **`os.O_TRUNC`**：如果文件存在则清空
- **`os.O_APPEND`**：追加模式

**使用示例**：

```python
import os

# 以只读模式打开文件
fd = os.open("file.txt", os.O_RDONLY)
print(f"文件描述符: {fd}")
os.close(fd)  # 关闭文件描述符

# 创建并写入文件
fd = os.open("new_file.txt", os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
os.write(fd, b"Hello World")
os.close(fd)

# 以追加模式打开文件
fd = os.open("log.txt", os.O_WRONLY | os.O_APPEND)
os.write(fd, b"\nNew log entry")
os.close(fd)
```

**与内置 `open()` 函数的区别**：

- **`os.open()`**：返回文件描述符（整数），是底层接口，需要手动管理文件描述符
- **`open()`**：返回文件对象，是高级接口，支持上下文管理器（`with` 语句），更易用

**使用示例对比**：

```python
import os

# 使用 os.open()（底层接口）
fd = os.open("file.txt", os.O_RDONLY)
data = os.read(fd, 1024)
os.close(fd)

# 使用 open()（高级接口，推荐）
with open("file.txt", "r") as f:
    data = f.read()
```

> 💡 **提示**：
> - `os.open()` 是底层接口，通常用于需要精确控制文件打开方式的场景
> - 标志位可以使用按位或（`|`）运算符组合多个选项
> - 使用 `os.open()` 后必须调用 `os.close()` 关闭文件描述符，否则会造成资源泄漏
> - **推荐**：对于大多数场景，建议使用内置的 `open()` 函数，它更易用且支持上下文管理器
> - 文件描述符是系统资源，使用完毕后应及时关闭

### 07.2 读写文件描述符

`os.read()` 和 `os.write()` 函数用于读写文件描述符。

#### os.read() - 读取文件描述符

**函数语法**：

```python
os.read(fd, n)
```

- **`fd`**：文件描述符（整数）
- **`n`**：要读取的字节数（整数）
- **返回值**：返回读取的字节数据（`bytes` 对象），如果到达文件末尾则返回空字节串

**使用示例**：

```python
import os

# 打开文件
fd = os.open("file.txt", os.O_RDONLY)

# 读取 1024 字节
data = os.read(fd, 1024)
print(f"读取的数据: {data}")

# 关闭文件描述符
os.close(fd)
```

#### os.write() - 写入文件描述符

**函数语法**：

```python
os.write(fd, data)
```

- **`fd`**：文件描述符（整数）
- **`data`**：要写入的字节数据（`bytes` 对象）
- **返回值**：返回实际写入的字节数（整数）

**使用示例**：

```python
import os

# 打开文件（创建模式）
fd = os.open("output.txt", os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)

# 写入数据
data = b"Hello World"
bytes_written = os.write(fd, data)
print(f"写入字节数: {bytes_written}")

# 关闭文件描述符
os.close(fd)
```

**综合示例**：

```python
import os

# 创建并写入文件
fd = os.open("test.txt", os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o644)
os.write(fd, b"Hello World\n")
os.write(fd, b"Python os module")
os.close(fd)

# 读取文件
fd = os.open("test.txt", os.O_RDONLY)
data = os.read(fd, 1024)
print(f"文件内容: {data.decode()}")
os.close(fd)
```

> 💡 **提示**：
> - `os.read()` 和 `os.write()` 是底层接口，操作的是字节数据（`bytes`），不是字符串
> - `os.read()` 可能返回的字节数少于请求的字节数，需要循环读取直到返回空字节串
> - `os.write()` 返回实际写入的字节数，可能少于请求写入的字节数
> - **推荐**：对于大多数场景，建议使用内置的 `open()` 函数，它返回的文件对象提供了更易用的 `read()` 和 `write()` 方法
> - 使用文件描述符进行 I/O 操作时，需要手动处理字节编码/解码

### 07.3 关闭文件描述符

`os.close()` 函数用于关闭文件描述符，释放系统资源。

**函数语法**：

```python
os.close(fd)
```

- **`fd`**：要关闭的文件描述符（整数）
- **返回值**：无返回值，关闭成功不返回任何内容；失败时抛出 `OSError` 异常

**使用示例**：

```python
import os

# 打开文件
fd = os.open("file.txt", os.O_RDONLY)

# 读取文件
data = os.read(fd, 1024)

# 关闭文件描述符
os.close(fd)
```

**异常处理示例**：

```python
import os

fd = None
try:
    fd = os.open("file.txt", os.O_RDONLY)
    data = os.read(fd, 1024)
except OSError as e:
    print(f"操作失败: {e}")
finally:
    # 确保文件描述符被关闭
    if fd is not None:
        os.close(fd)
```

**重要提示**：

- 文件描述符是系统资源，每个进程可打开的文件描述符数量有限
- 使用 `os.open()` 打开的文件描述符必须使用 `os.close()` 关闭
- 未关闭的文件描述符会导致资源泄漏，可能耗尽系统资源
- 多次关闭同一个文件描述符会抛出 `OSError` 异常

> 💡 **提示**：
> - 使用 `os.open()` 后必须调用 `os.close()` 关闭文件描述符，否则会造成资源泄漏
> - 建议使用 `try-finally` 或上下文管理器确保文件描述符被正确关闭
> - 如果文件描述符无效或已关闭，`os.close()` 会抛出 `OSError` 异常
> - **推荐**：对于大多数场景，建议使用内置的 `open()` 函数，它支持上下文管理器（`with` 语句），可以自动关闭文件
> - 文件描述符泄漏会导致进程无法打开新文件，影响程序正常运行

## 08. 用户与权限管理

### 08.1 获取当前用户信息

`os` 模块提供了多个函数用于获取当前用户的信息。

#### os.getlogin() - 获取当前登录用户名

**函数语法**：

```python
os.getlogin()
```

- **参数**：无参数
- **返回值**：返回当前登录用户的用户名（字符串）

**使用示例**：

```python
import os

# 获取当前登录用户名
username = os.getlogin()
print(f"当前用户名: {username}")
# 输出: 当前用户名: admin（示例）
```

#### os.getuid() / os.getgid() - 获取用户 ID 和组 ID（Unix/Linux）

**函数语法**：

```python
os.getuid()  # 获取当前进程的用户 ID
os.getgid()  # 获取当前进程的组 ID
```

- **参数**：无参数
- **返回值**：返回用户 ID 或组 ID（整数）

**使用示例**：

```python
import os

# 获取用户 ID 和组 ID（仅在 Unix/Linux 上可用）
if hasattr(os, 'getuid'):
    uid = os.getuid()
    gid = os.getgid()
    print(f"用户 ID: {uid}, 组 ID: {gid}")
    # 输出: 用户 ID: 1000, 组 ID: 1000（示例）
```

#### os.geteuid() / os.getegid() - 获取有效用户 ID 和有效组 ID（Unix/Linux）

**函数语法**：

```python
os.geteuid()  # 获取当前进程的有效用户 ID
os.getegid()  # 获取当前进程的有效组 ID
```

- **参数**：无参数
- **返回值**：返回有效用户 ID 或有效组 ID（整数）

**使用示例**：

```python
import os

# 获取有效用户 ID 和有效组 ID（仅在 Unix/Linux 上可用）
if hasattr(os, 'geteuid'):
    euid = os.geteuid()
    egid = os.getegid()
    print(f"有效用户 ID: {euid}, 有效组 ID: {egid}")
```

**综合示例**：

```python
import os

def get_user_info():
    """获取当前用户信息"""
    info = {}
    
    # 获取用户名
    try:
        info['username'] = os.getlogin()
    except OSError:
        info['username'] = os.getenv('USER') or os.getenv('USERNAME')
    
    # 获取用户 ID 和组 ID（Unix/Linux）
    if hasattr(os, 'getuid'):
        info['uid'] = os.getuid()
        info['gid'] = os.getgid()
        info['euid'] = os.geteuid()
        info['egid'] = os.getegid()
    
    return info

user_info = get_user_info()
print(f"用户信息: {user_info}")
```

> 💡 **提示**：
> - `os.getlogin()` 在所有平台上都可用，但可能在某些环境下（如无终端环境）抛出 `OSError` 异常
> - `os.getuid()`、`os.getgid()`、`os.geteuid()`、`os.getegid()` 仅在类 Unix 系统（Linux、macOS）上可用，在 Windows 上不可用
> - 如果 `os.getlogin()` 失败，可以尝试使用环境变量 `USER`（Unix）或 `USERNAME`（Windows）作为替代
> - 有效用户 ID（euid）和有效组 ID（egid）用于权限检查，可能与实际用户 ID 不同（如使用 setuid 程序时）

### 08.2 获取用户组信息

`os` 模块和 `grp` 模块提供了多个函数用于获取用户组信息。

#### os.getgroups() - 获取所有补充组 ID

**函数语法**：

```python
os.getgroups()
```

- **参数**：无参数
- **返回值**：返回当前进程所属的所有补充组 ID 列表（整数列表）

**使用示例**：

```python
import os

# 获取所有补充组 ID（仅在 Unix/Linux 上可用）
if hasattr(os, 'getgroups'):
    groups = os.getgroups()
    print(f"补充组 ID: {groups}")
    # 输出: 补充组 ID: [1000, 1001, 1002]（示例）
```

> 💡 **提示**：`os.getgroups()` 返回的是补充组（supplementary groups）ID 列表，不包括主组 ID。主组 ID 可以通过 `os.getgid()` 获取。

#### grp.getgrgid() - 通过组 ID 获取组信息

**函数语法**：

```python
grp.getgrgid(gid)
```

- **`gid`**：组 ID（整数）
- **返回值**：返回一个 `grp.struct_group` 对象，包含组信息

**struct_group 对象属性**：
- **`gr_name`**：组名（字符串）
- **`gr_passwd`**：组密码（通常为 `'x'` 或 `'*'`，字符串）
- **`gr_gid`**：组 ID（整数）
- **`gr_mem`**：组成员用户名列表（列表）

**使用示例**：

```python
import os
import grp

# 获取主组信息
if hasattr(os, 'getgid'):
    gid = os.getgid()
    group_info = grp.getgrgid(gid)
    print(f"主组名: {group_info.gr_name}")
    print(f"主组 ID: {group_info.gr_gid}")
    print(f"组成员: {group_info.gr_mem}")
    # 输出示例:
    # 主组名: users
    # 主组 ID: 1000
    # 组成员: ['user1', 'user2']
```

#### grp.getgrnam() - 通过组名获取组信息

**函数语法**：

```python
grp.getgrnam(name)
```

- **`name`**：组名（字符串）
- **返回值**：返回一个 `grp.struct_group` 对象，包含组信息

**使用示例**：

```python
import grp

# 通过组名获取组信息
try:
    group_info = grp.getgrnam("users")
    print(f"组名: {group_info.gr_name}")
    print(f"组 ID: {group_info.gr_gid}")
    print(f"组成员: {group_info.gr_mem}")
except KeyError:
    print("组不存在")
```

#### grp.getgrall() - 获取所有组信息

**函数语法**：

```python
grp.getgrall()
```

- **参数**：无参数
- **返回值**：返回所有组的 `grp.struct_group` 对象列表

**使用示例**：

```python
import grp

# 获取所有组信息
all_groups = grp.getgrall()
print(f"系统中共有 {len(all_groups)} 个组")

# 列出前 5 个组
for group in all_groups[:5]:
    print(f"{group.gr_name} (GID: {group.gr_gid})")
```

**综合示例**：

```python
import os
import grp

def get_group_info():
    """获取当前用户的所有组信息"""
    if not hasattr(os, 'getgid'):
        return "此功能仅在 Unix/Linux 系统上可用"
    
    info = {}
    
    # 获取主组信息
    primary_gid = os.getgid()
    primary_group = grp.getgrgid(primary_gid)
    info['主组'] = {
        '名称': primary_group.gr_name,
        'ID': primary_group.gr_gid
    }
    
    # 获取所有补充组信息
    supplementary_gids = os.getgroups()
    supplementary_groups = []
    for gid in supplementary_gids:
        try:
            group = grp.getgrgid(gid)
            supplementary_groups.append({
                '名称': group.gr_name,
                'ID': group.gr_gid
            })
        except KeyError:
            supplementary_groups.append({'名称': '未知', 'ID': gid})
    
    info['补充组'] = supplementary_groups
    
    return info

group_info = get_group_info()
print(f"组信息: {group_info}")
```

> 💡 **提示**：
> - `os.getgroups()` 和 `grp` 模块仅在类 Unix 系统（Linux、macOS）上可用，在 Windows 上不可用
> - `grp.getgrgid()` 和 `grp.getgrnam()` 在组不存在时会抛出 `KeyError` 异常，建议使用 `try-except` 处理
> - 主组（primary group）通过 `os.getgid()` 获取，补充组（supplementary groups）通过 `os.getgroups()` 获取
> - `grp` 模块需要单独导入：`import grp`
