# J1B-为什么99%的人配置Java环境失败？大厂开发者5分钟搞定的JDK安装与环境配置完全指南

> **摘要**：**99% 的 Java 新手配置环境时踩坑**，`javac` 找不到、环境变量配错。而**大厂开发者 5 分钟搞定**，一次配置终身使用。本文档提供完整指南，助你快速搭建 Java 开发环境。

## 📚 目录

- [前置知识点](#前置知识点) - 判断是否需要先学习基础知识
- [问题描述](#问题描述) - 为什么99%的人配置Java环境会失败？
- [1. JDK 下载与安装](#1-jdk-下载与安装)
- [2. 环境变量配置（核心步骤）](#2-环境变量配置核心步骤)
- [3. IDE 配置（IntelliJ IDEA）](#3-ide-配置intellij-idea)
- [4. 项目创建与环境验证](#4-项目创建与环境验证)
- [5. 常见问题与解决方案](#5-常见问题与解决方案)
- [6. 最佳实践](#6-最佳实践)
- [参考资料](#参考资料)

---

## 🎯 前置知识点

在学习本文档之前，你需要掌握以下基础知识：

### 基础知识点（必须掌握）

- **Java 版本选择基础** 📖 [J1A - Java 版本选择踩坑指南 - 掘金](https://juejin.cn/post/7568505252820369454)
  - 了解 JDK（Java Development Kit，Java 开发工具包）版本选择的重要性
  - 理解 LTS（Long Term Support，长期支持）版本和非 LTS 版本的区别
  - 掌握 JDK 版本选择的基本原则

- **Windows 操作系统基础**
  - 了解 Windows 10/11 系统的基本操作
  - 理解文件路径的概念（绝对路径、相对路径）
  - 能够使用文件资源管理器浏览文件夹

### 📖 学习建议

- **零基础小白**：建议先学习 J1A（Java 版本选择）文档 📖 [J1A - Java 版本选择踩坑指南 - 掘金](https://juejin.cn/post/7568505252820369454)，了解 JDK 版本选择的重要性，再学习本文档
- **有基础读者**：如果已经了解 Java 版本选择，可以直接学习本文档的环境配置部分
- **中级开发者**：重点关注本文档中的环境变量配置规范和最佳实践部分

---

## 问题描述：为什么99%的人配置Java环境会失败？

### 新手常见错误场景

**错误做法**：
- ❌ 下载了 JRE（Java Runtime Environment，Java 运行时环境）而不是 JDK（Java Development Kit，Java 开发工具包），导致无法编译 Java 代码
- ❌ 环境变量配置错误，`javac` 命令找不到，提示「不是内部或外部命令」
- ❌ 将 JDK 安装到中文路径（如 `C:\Java开发\jdk17`），导致环境变量配置失败
- ❌ 配置环境变量后没有重启命令提示符，导致配置不生效
- ❌ 不知道如何配置 IDE（Integrated Development Environment，集成开发环境），导致 IDE 识别不到 JDK
- ❌ 多个 JDK 版本冲突，系统使用了错误的 JDK 版本

**结果**：环境配置失败，无法编译运行 Java 程序，学习进度受阻。😭

### 大厂开发者的做法

**正确做法**：
- ✅ 选择 JDK LTS（Long Term Support，长期支持）版本（如 JDK 17），下载正确的 JDK 安装包
- ✅ 将 JDK 安装到默认路径（无中文、无空格），避免路径问题
- ✅ 正确配置 `JAVA_HOME`、`PATH`、`CLASSPATH` 三个环境变量，使用 `%JAVA_HOME%` 引用避免硬编码
- ✅ 配置完成后重启命令提示符和 IDE，验证环境变量生效
- ✅ 在 IDE 中正确配置 JDK 路径，确保 IDE 能识别 Java 开发环境
- ✅ 统一团队 JDK 版本，避免版本冲突问题

**结果**：环境配置成功，5 分钟搞定，一次配置终身使用！🚀

---

## 1. JDK 下载与安装 <span style="background-color: #d4edda; color: #155724; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">Must</span>

📖 [Oracle Java 官方下载](https://www.oracle.com/java/technologies/downloads/) 📚 [JDK 下载与安装教程 - 菜鸟教程](https://www.runoob.com/java/java-environment-setup.html) 💡 [JDK 安装步骤详解 - CSDN](https://blog.csdn.net/EmeraldTiger56/article/details/154012693)

### 1.1 核心概念区分

在开始安装之前，需要理解 JDK（Java Development Kit，Java 开发工具包）、JRE（Java Runtime Environment，Java 运行时环境）和 JVM（Java Virtual Machine，Java 虚拟机）的区别：

| 组件 | 作用 | 是否需要安装 |
|------|------|-------------|
| JDK（Java Development Kit） | 包含编译器（javac）、调试工具、文档等，用于 Java 开发 | ✅ 开发必须安装 |
| JRE（Java Runtime Environment） | 包含 JVM（Java 虚拟机），用于运行 Java 程序 | ❌ JDK 11+ 已内置，无需单独安装 |
| JVM（Java Virtual Machine） | 实现 Java 跨平台的核心，负责执行字节码 | ❌ 包含在 JRE/JDK 中，无需单独安装 |

### 1.2 为什么必须配置 Java 环境？

📚 [Java 环境变量配置原理 - 菜鸟教程](https://www.runoob.com/java/java-environment-setup.html)

- **编译需求**：Java 源代码（.java）需通过 JDK 的 `javac`（Java 编译器）命令编译为字节码（.class）
- **运行需求**：系统需通过环境变量找到 JVM（Java Virtual Machine，Java 虚拟机）和执行工具
- **IDE（Integrated Development Environment，集成开发环境）依赖**：开发工具（如 IDEA）需通过环境变量定位 JDK 位置
- **跨平台保障**：统一的环境配置确保程序在不同 Windows 设备上正常运行

> **💡 版本推荐**：优先选择 **LTS（Long Term Support，长期支持）版本**，如 JDK 8、JDK 11、JDK 17（当前主流）。LTS 版本提供 5-8 年官方支持，稳定性更高，适合生产环境和学习使用。关于版本选择的详细说明，请参考本文档的前置知识点部分。

### 1.3 下载渠道选择

Java 官方提供两种主流下载渠道，推荐选择开源免费的 Adoptium（避免 Oracle（甲骨文公司）的商业授权问题）：

#### 1. 推荐渠道：Adoptium（开源免费）

- 访问官网：[adoptium.net](https://adoptium.net/)
- 选择版本：**OpenJDK 17 LTS（Long Term Support，长期支持）**（兼容性最好，支持最广）
- 选择操作系统：**Windows（操作系统）** → 架构：**x64**（主流电脑均为 64 位）
- 下载安装包：选择 **.msi** 格式（图形化安装，更简单）或 **.zip** 格式（解压即用）

#### 2. 备选渠道：Oracle（甲骨文公司）JDK（需注意授权）

- 访问官网：[oracle.com/java/technologies/downloads/](https://www.oracle.com/java/technologies/downloads/)
- 注意：Oracle（甲骨文公司）JDK 用于商业用途需购买授权，个人学习可免费使用
- 需注册 Oracle（甲骨文公司）账号才能下载，步骤较繁琐

### 1.4 安装步骤（以 Adoptium .msi 为例） <span style="background-color: #d4edda; color: #155724; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">Must</span>

📚 [JDK 安装步骤详解 - 菜鸟教程](https://www.runoob.com/java/java-environment-setup.html) 💡 [JDK 安装详细步骤 - CSDN](https://blog.csdn.net/EmeraldTiger56/article/details/154012693)

1. **运行安装包**：双击下载的 `OpenJDK17U-jdk_x64_windows_hotspot_17.0.10_7.msi`，点击「Next」

2. **接受协议**：勾选「I accept the terms in the License Agreement」，点击「Next」

3. **选择安装路径（关键）**
   - 默认路径：`C:\Program Files\Eclipse Adoptium\jdk-17.0.10.7-hotspot`
   - **推荐保持默认路径**（避免中文、空格或特殊字符，减少环境变量配置错误）
   - 记住此路径！后续配置环境变量需用到（可复制路径备用）
   - 点击「Next」

4. **开始安装**：点击「Install」，等待安装完成（约 1-2 分钟），最后点击「Finish」

> **⚠️ 安装注意事项**
> - 禁止将 JDK 安装到含中文的路径（如「C:\Java开发\jdk17」）
> - 禁止路径包含空格（如「C:\My JDK\jdk17」）
> - 无需勾选「安装 JRE（Java Runtime Environment，Java 运行时环境）」（JDK 17 已内置 JRE，路径为 `jdk-17.0.10.7-hotspot\jre`）

### 1.5 安装验证（初步检查）

📚 [JDK 安装验证方法 - 菜鸟教程](https://www.runoob.com/java/java-environment-setup.html)

```cmd
# 1. 打开「命令提示符」（Win+R → 输入cmd → 回车）
# 2. 进入 JDK 的 bin 目录（替换为你的安装路径）
cd "C:\Program Files\Eclipse Adoptium\jdk-17.0.10.7-hotspot\bin"

# 3. 检查 JDK 版本
javac -version  # 应输出：javac 17.0.10
java -version   # 应输出：java version "17.0.10"
```

> **✅ 初步安装成功标志**：执行 `javac -version` 和 `java -version` 均能显示 JDK 17 版本号（若提示「不是内部或外部命令」，需继续配置环境变量）。

## 2. 环境变量配置（核心步骤） <span style="background-color: #d4edda; color: #155724; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">Must</span>

📖 [Oracle Java 环境变量配置官方文档](https://docs.oracle.com/javase/tutorial/essential/environment/paths.html) 📚 [Java 环境变量配置详解 - 菜鸟教程](https://www.runoob.com/java/java-environment-setup.html) 💡 [环境变量配置实战 - CSDN](https://blog.csdn.net/FrostfirePanther89/article/details/154063106)

Java 开发必须配置 3 个核心环境变量：`JAVA_HOME`、`PATH`、`CLASSPATH`。以下以 Windows 10/11 系统为例，步骤通用。

### 2.1 打开环境变量配置界面

1. **快速打开方式**：
   - Win+R → 输入`sysdm.cpl` → 回车
   - 点击「高级」选项卡 → 点击「环境变量」按钮

2. **区分「用户变量」和「系统变量」**：
   - **系统变量**：所有用户均可使用，**推荐配置此处**
   - 用户变量：仅当前登录用户可用，多人共用电脑时建议用系统变量

### 2.2 配置 JAVA_HOME（关键） <span style="background-color: #d4edda; color: #155724; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">Must</span>

📚 [JAVA_HOME 环境变量详解 - 菜鸟教程](https://www.runoob.com/java/java-environment-setup.html) 💡 [JAVA_HOME 配置实战 - CSDN](https://blog.csdn.net/FrostfirePanther89/article/details/154063106)

`JAVA_HOME` 用于告诉系统和 IDE（Integrated Development Environment，集成开发环境）「JDK 安装在哪里」，是其他变量的基础。

1. **新建系统变量**：
   - 在「系统变量」区域点击「新建」
   - 变量名：`JAVA_HOME`（必须大写，不能错）
   - 变量值：粘贴 JDK 安装路径（如 `C:\Program Files\Eclipse Adoptium\jdk-17.0.10.7-hotspot`）
   - 点击「确定」

### 2.3 配置 PATH（执行命令必备） <span style="background-color: #d4edda; color: #155724; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">Must</span>

📚 [PATH 环境变量详解 - 菜鸟教程](https://www.runoob.com/java/java-environment-setup.html) 💡 [PATH 配置实战 - CSDN](https://blog.csdn.net/FrostfirePanther89/article/details/154063106)

`PATH` 用于告诉系统「去哪里找 Java 的执行命令（如 `javac`（Java 编译器）、`java`（Java 运行器））」，无需每次进入 `bin` 目录执行命令。

1. **编辑系统变量 PATH**：
   - 在「系统变量」区域找到`PATH` → 点击「编辑」
   - 点击「新建」→ 输入 `%JAVA_HOME%\bin`（引用 JAVA_HOME，避免路径硬编码）
   - （可选）再点击「新建」→ 输入 `%JAVA_HOME%\jre\bin`（JDK 17 内置 JRE，部分旧工具需要）
   - 点击「上移」，将上述两个路径移到最顶部（避免与其他 Java 版本冲突）
   - 点击「确定」保存

### 2.4 配置 CLASSPATH（可选，旧项目需用） <span style="background-color: #cce5ff; color: #004085; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">Could</span>

📚 [CLASSPATH 环境变量详解 - 菜鸟教程](https://www.runoob.com/java/java-environment-setup.html)

`CLASSPATH` 用于告诉 JVM（Java Virtual Machine，Java 虚拟机）「去哪里找编译后的字节码文件（.class）」，JDK 1.5+ 后可省略，但部分旧项目或工具需要配置。

1. **新建系统变量 CLASSPATH**：
   - 在「系统变量」区域点击「新建」
   - 变量名：`CLASSPATH`（必须大写）
   - 变量值：`.;%JAVA_HOME%\lib\dt.jar;%JAVA_HOME%\lib\tools.jar`（开头的「.」表示当前目录，必须加）
   - 点击「确定」

### 2.5 环境变量验证（最终检查） <span style="background-color: #d4edda; color: #155724; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">Must</span>

📚 [环境变量验证方法 - 菜鸟教程](https://www.runoob.com/java/java-environment-setup.html) 💡 [环境变量验证实战 - CSDN](https://blog.csdn.net/FrostfirePanther89/article/details/154063106)

> **⚠️ 重要提醒**：配置完成后，**必须关闭所有已打开的命令提示符/IDE**，重新打开新窗口才能使环境变量生效！

```cmd
# 1. 打开新的「命令提示符」（Win+R → cmd → 回车）
# 2. 执行以下命令，均需正常输出版本号
java -version   # 验证 Java 运行环境
javac -version  # 验证 Java 编译器（关键，必须成功）

# 3. 验证 JAVA_HOME 配置
echo %JAVA_HOME%  # 应输出 JDK 安装路径，如 C:\Program Files\Eclipse Adoptium\jdk-17.0.10.7-hotspot

# 4. 验证 PATH 配置
where java       # 应输出 %JAVA_HOME%\bin\java.exe 路径
where javac      # 应输出 %JAVA_HOME%\bin\javac.exe 路径
```

> **✅ 环境变量配置成功标志**：在任意目录下执行 `javac -version` 均能显示 JDK 版本号，且 `echo %JAVA_HOME%` 能正确输出安装路径。

## 3. IDE 配置（IntelliJ IDEA） <span style="background-color: #fff3cd; color: #856404; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">Should</span>

📖 [IntelliJ IDEA 官方指南](https://www.jetbrains.com/help/idea/getting-started.html) 📚 [IntelliJ IDEA 使用教程 - 菜鸟教程](https://www.runoob.com/java/java-ide.html) 💡 [IDEA 配置 JDK 实战 - CSDN](https://blog.csdn.net/EmeraldTiger56/article/details/154012693)

Java 开发推荐使用 **IntelliJ IDEA**（简称 IDEA），它是目前最流行、功能最强大的 Java IDE（Integrated Development Environment，集成开发环境），提供免费的 Community Edition（社区版）（足够学习和中小型项目开发）。

### 3.1 IDEA 下载与安装

📚 [IDEA 下载与安装教程 - 菜鸟教程](https://www.runoob.com/java/java-ide.html)

1. **下载 IDEA Community Edition（社区版）**：
   - 访问官网：[jetbrains.com/idea/download/](https://www.jetbrains.com/idea/download/?section=windows)
   - 选择版本：**Community Edition（社区版）**（免费，开源）
   - 下载格式：**.exe**（图形化安装）

2. **安装步骤**：
   - 双击安装包，点击「Next」
   - 选择安装路径（如 `C:\Program Files\JetBrains\IntelliJ IDEA Community Edition 2024.1`）
   - 勾选附加任务（推荐）：
     - Create Desktop Shortcut（创建桌面快捷方式）
     - Add "Open Folder as Project"（支持右键打开文件夹为项目）
     - Associate .java files（关联 .java 文件，双击用 IDEA 打开）
     - Add to PATH（可选，方便命令行启动）
   - 点击「Next」→ 「Install」→ 安装完成后点击「Finish」

### 3.2 IDEA 配置 JDK（关键） <span style="background-color: #fff3cd; color: #856404; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">Should</span>

📖 [IntelliJ IDEA 配置 JDK 官方指南](https://www.jetbrains.com/help/idea/sdk.html) 📚 [IDEA 配置 JDK 教程 - 菜鸟教程](https://www.runoob.com/java/java-ide.html) 💡 [IDEA JDK 配置实战 - CSDN](https://blog.csdn.net/EmeraldTiger56/article/details/154012693)

首次打开 IDEA 时，需关联已安装的 JDK（Java Development Kit，Java 开发工具包），确保 IDE（Integrated Development Environment，集成开发环境）能识别 Java 开发环境。

1. **首次打开 IDEA**：
   - 首次启动会提示「Import IntelliJ IDEA Settings」，选择「Do not import settings」→ 「OK」
   - 选择 UI（User Interface，用户界面）主题（Light/Dark，根据喜好选择）→ 「Next: Featured plugins」
   - 无需安装额外插件，直接点击「Next: Start using IntelliJ IDEA」

2. **配置项目 SDK（Software Development Kit，软件开发工具包）（即 JDK）**：
   - 点击「New Project」→ 在「New Project」界面中，点击「Project SDK」下拉框
   - 若未显示 JDK 17，点击「Add SDK」→ 「JDK」
   - 在弹出的窗口中，选择 JDK 安装路径（即 `JAVA_HOME` 路径，如 `C:\Program Files\Eclipse Adoptium\jdk-17.0.10.7-hotspot`）
   - 点击「OK」→ 此时「Project SDK」会显示「17 (Eclipse Adoptium)」

> **💡 后续项目 JDK 配置**：若已创建项目，可通过「File → Project Structure → Project Settings → Project → Project SDK」重新选择或添加 JDK。

## 4. 项目创建与环境验证 <span style="background-color: #d4edda; color: #155724; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">Must</span>

📖 [Oracle Java 教程 - 你的第一个程序](https://docs.oracle.com/javase/tutorial/getStarted/cupojava/index.html) 📚 [Java 项目创建教程 - 菜鸟教程](https://www.runoob.com/java/java-examples.html) 💡 [HelloWorld 项目实战 - 菜鸟教程在线运行](https://www.runoob.com/try/runcode.php?filename=HelloWorld&type=java)

通过创建一个简单的「HelloWorld」项目，验证 Java 环境是否完全可用。

### 4.1 用 IDEA 创建 HelloWorld 项目 <span style="background-color: #d4edda; color: #155724; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">Must</span>

📖 [IntelliJ IDEA 创建项目官方指南](https://www.jetbrains.com/help/idea/creating-and-running-your-first-java-application.html) 📚 [IDEA 创建项目教程 - 菜鸟教程](https://www.runoob.com/java/java-ide.html)

1. **新建 Java 项目**：
   - IDEA 主界面点击「New Project」→ 确认「Project SDK」为 JDK 17
   - 「Name」：输入项目名（如 `HelloWorld`）
   - 「Location」：选择项目保存路径（如 `D:\JavaProjects\HelloWorld`）
   - 取消勾选「Create Git repository」（初学者无需版本控制）
   - 点击「Create」

2. **创建 Java 类**：
   - 在左侧「Project」面板中，右键点击「src」→ 「New」→ 「Java Class」
   - 「Name」：输入 `HelloWorld`（Java 类名必须与文件名一致，首字母大写）
   - 点击「Enter」，自动生成类文件

3. **编写 HelloWorld 代码**：
```java
public class HelloWorld {
    // 主方法（程序入口）
    public static void main(String[] args) {
        // 输出内容到控制台
        System.out.println("Hello, Java! 环境配置成功！");
    }
}
```

### 4.2 运行项目与验证 <span style="background-color: #d4edda; color: #155724; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">Must</span>

📚 [Java 程序运行教程 - 菜鸟教程](https://www.runoob.com/java/java-examples.html) 💡 [Java 程序运行实战 - 菜鸟教程在线运行](https://www.runoob.com/try/runcode.php?filename=HelloWorld&type=java)

1. **运行程序**：
   - 方法1：在代码编辑区右键 → 「Run 'HelloWorld.main()'」
   - 方法2：点击代码编辑区左侧的绿色三角图标 → 「Run 'HelloWorld'」
   - 方法3：使用快捷键「Ctrl+Shift+F10」

2. **查看运行结果**：
   - 底部「Run」面板会显示输出：`Hello, Java! 环境配置成功！`
   - 无任何错误提示（如「Error: Could not find or load main class（主类）」）

### 4.3 命令行验证（备选） <span style="background-color: #cce5ff; color: #004085; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">Could</span>

📚 [Java 命令行编译运行 - 菜鸟教程](https://www.runoob.com/java/java-environment-setup.html)

若需确认命令行环境是否正常，可通过手动编译运行验证：

```cmd
# 1. 打开命令提示符，进入项目src目录（替换为你的路径）
cd D:\JavaProjects\HelloWorld\src

# 2. 编译 Java 源代码（生成 HelloWorld.class）
javac HelloWorld.java

# 3. 运行字节码文件
java HelloWorld

# 4. 预期输出
Hello, Java! 环境配置成功！
```

> **✅ 完整环境验证成功标志**：IDEA 或命令行均能正常运行 HelloWorld 程序，输出预期内容，无任何编译或运行错误。

## 5. 常见问题与解决方案

📚 [Java 环境配置常见问题 - 菜鸟教程](https://www.runoob.com/java/java-environment-setup.html)

### 5.1 问题 1：javac 不是内部或外部命令

**现象**：命令行输入 `javac -version` 提示「'javac' 不是内部或外部命令，也不是可运行的程序或批处理文件。」

**解决方案**：
```cmd
# 解决方案：
1. 检查环境变量 PATH 是否配置正确：
   - 确认 PATH 中包含「%JAVA_HOME%\bin」
   - 确认 %JAVA_HOME% 指向正确的 JDK 路径（无中文、空格）

2. 检查 JAVA_HOME 配置：
   - 执行 echo %JAVA_HOME%，确认路径正确（如 C:\Program Files\Eclipse Adoptium\jdk-17.0.10.7-hotspot）

3. 重启命令提示符：
   - 环境变量修改后必须关闭所有旧窗口，重新打开新窗口

4. 手动验证：
   - 进入 JDK 的 bin 目录（cd %JAVA_HOME%\bin）
   - 执行 javac -version，若成功则说明 PATH 配置问题
```

### 5.2 问题 2：IDEA 找不到 JDK

**现象**：IDEA 新建项目时，「Project SDK」下拉框为空，提示「No SDK specified」

**解决方案**：
```cmd
# 解决方案：
1. 手动添加 JDK：
   - 点击「Add SDK」→ 「JDK」
   - 浏览并选择 JDK 安装路径（即 JAVA_HOME 路径）
   - 确认路径中无中文、空格

2. 检查 JDK 是否真的安装成功：
   - 命令行执行 javac -version，确认 JDK 正常

3. 重新安装 JDK：
   - 若路径正确但仍无法识别，卸载 JDK 后重新安装（选择 .msi 格式）
```

### 5.3 问题 3：运行程序提示找不到主类

**现象**：执行 `java HelloWorld` 提示「Error: Could not find or load main class（主类） HelloWorld」

**解决方案**：
```cmd
# 解决方案：
1. 检查类名与文件名是否一致：
   - Java 类名必须与文件名完全一致（包括大小写）
   - 如类名 HelloWorld，文件名必须是 HelloWorld.java

2. 检查编译是否成功：
   - 确认 `src` 目录下生成了 `HelloWorld.class` 文件（`javac`（Java 编译器）编译成功的标志）
   - 若没有 `.class` 文件，重新执行 `javac HelloWorld.java`

3. 检查运行目录：
   - 必须在 `.class` 文件所在目录运行 `java`（Java 运行器）命令
   - 如 `.class` 在 `src` 目录，需 `cd` 到 `src` 目录后执行 `java HelloWorld`
```

### 5.4 问题 4：中文乱码

**现象**：程序输出中文时显示乱码（如「Hello, 涓枃!」）

**解决方案**：
```cmd
# 解决方案：
1. 命令行编译时指定编码：
   javac -encoding UTF-8 HelloWorld.java  # 使用 UTF-8（Unicode Transformation Format-8，统一字符编码转换格式-8）编码编译
   java HelloWorld

2. IDEA 中配置编码（永久解决）：
   - File → Settings → Editor → File Encodings
   - 所有编码设置为「UTF-8（Unicode Transformation Format-8，统一字符编码转换格式-8）」（Global Encoding、Project Encoding、Default encoding for properties files）
   - 勾选「Transparent native-to-ascii conversion」
   - 点击「OK」，重新编译运行
```

### 5.5 问题 5：多个 JDK 版本冲突

**现象**：执行 `java -version` 显示的版本与安装的 JDK 17 不一致

**解决方案**：
```cmd
# 解决方案：
1. 检查 PATH 环境变量顺序：
   - 确保「%JAVA_HOME%\bin」在 PATH 的最顶部
   - 移除其他 JDK 的路径（如旧版本 JDK 的 bin 目录）

2. 检查 JAVA_HOME 指向：
   - 执行 echo %JAVA_HOME%，确认指向 JDK 17 路径
   - 若指向旧版本，修改 JAVA_HOME 为新路径

3. 检查是否有残留的旧 JDK：
   - 控制面板 → 卸载程序 → 卸载旧版本 JDK
   - 重启电脑后重新验证
```

## 6. 最佳实践

📚 [Java 开发最佳实践 - 菜鸟教程](https://www.runoob.com/java/java-tutorial.html)

### 6.1 版本选择与管理

- **优先使用 LTS（Long Term Support，长期支持）版本**：JDK 8、11、17（企业级项目主流，稳定性高，支持周期长）
- **统一团队版本**：多人协作时确保所有成员使用相同 JDK 版本，避免兼容性问题
- **避免频繁更新**：项目开发过程中不随意更新 JDK 版本，如需更新需全面测试

### 6.2 环境变量配置规范

- **使用系统变量**：所有用户均可使用，避免重复配置
- **引用 JAVA_HOME**：PATH 中使用 `%JAVA_HOME%\bin`，而非硬编码路径（如 `C:\Program Files\Java\jdk17\bin`），便于后续 JDK 升级
- **记录配置信息**：将 JDK 版本、安装路径、环境变量配置记录到项目文档中，便于新人快速上手

### 6.3 项目开发规范

```cmd
# 1. 项目结构规范（推荐）
HelloWorld/          # 项目根目录
├── src/             # 源代码目录
│   └── com/         # 包名（反向域名，如公司域名com.example）
│       └── demo/
│           └── HelloWorld.java  # 业务代码
├── out/             # 编译输出目录（IDEA自动生成）
└── README.md        # 项目说明文档

# 2. 使用构建工具（推荐）
# 中小型项目：Maven（管理依赖，自动构建）
# 大型项目：Gradle（更灵活，支持多模块）

# 3. 代码规范
# 安装 Checkstyle 插件（IDEA 中搜索 Checkstyle）
# 遵循阿里巴巴 Java 开发手册（主流规范）
```

### 6.4 环境备份与迁移

- **备份环境变量**：在「环境变量」界面点击「导出」，保存为 `.reg` 文件，重装系统后可双击导入
- **JDK 绿色安装**：若需频繁迁移，选择 `.zip` 格式的 JDK（解压即用），无需重新安装，只需配置环境变量
- **IDE 配置导出**：IDEA 中通过「File → Manage IDE Settings → Export Settings」导出配置，新设备导入即可复用

## 参考资料

### 官方文档

📖 [Oracle Java 官方文档](https://docs.oracle.com/en/java/)  
📖 [IntelliJ IDEA 官方指南](https://www.jetbrains.com/help/idea/)

### 教程资源

📚 [Java 环境配置教程 - 菜鸟教程](https://www.runoob.com/java/java-environment-setup.html)  
📚 [Java IDE 使用教程 - 菜鸟教程](https://www.runoob.com/java/java-ide.html)  
💡 [Java 开发环境搭建完整指南 - CSDN](https://blog.csdn.net/EmeraldTiger56/article/details/154012693)  
💡 [JDK 环境配置全流程指南 - CSDN](https://blog.csdn.net/FrostfirePanther89/article/details/154063106)

### 实践工具

💡 [Java 在线编译器](https://www.runoob.com/try/runcode.php?filename=HelloWorld&type=java)  
💡 [JDK 下载地址 - Adoptium](https://adoptium.net/)

---

## 结语：掌握 Java 环境配置的精髓

通过本文档的详细步骤，你已经掌握了如何从零开始搭建 Java 开发环境。记住，**环境配置不是一次性任务，而是开发的基础**：

1. **选择正确的版本**：优先选择 JDK LTS 版本，确保稳定性和长期支持
2. **规范配置环境变量**：使用 `JAVA_HOME` 引用，避免硬编码路径
3. **验证配置结果**：配置完成后务必验证，确保环境可用
4. **遵循最佳实践**：统一团队版本，规范项目结构，提高开发效率

**环境配置是 Java 开发的第一步，也是最重要的一步**。掌握了正确的配置方法，你就能避免 99% 的配置问题，快速进入 Java 开发的世界，成为一名优秀的 Java 开发者！💪

---

**作者**：郑恩赐  
**机构**：厦门工学院人工智能创作坊  
**日期**：2025 年 11 月 06 日

