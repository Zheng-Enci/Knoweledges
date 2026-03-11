# J1C-为什么99%的人选错IDE？大厂Java开发者的IDE选择与使用完全指南

> **摘要**：**99% 的 Java 新手选错 IDE**，用记事本写代码、用 Eclipse 卡顿。而**大厂开发者首选 IntelliJ IDEA**，效率提升 5 倍。本文档提供完整指南，助你快速上手。

## 📚 目录

- [前置知识点](#前置知识点) - 判断是否需要先学习基础知识
- [问题描述](#问题描述) - 为什么99%的人选错IDE？
- [1. IDE 选择：IntelliJ IDEA vs Eclipse](#1-ide-选择intellij-idea-vs-eclipse)
- [2. IntelliJ IDEA 下载与安装](#2-intellij-idea-下载与安装)
- [3. IntelliJ IDEA 基本配置](#3-intellij-idea-基本配置)
- [4. 创建第一个 Java 项目](#4-创建第一个-java-项目)
- [5. 常用功能与快捷键](#5-常用功能与快捷键)
- [6. 常见问题与解决方案](#6-常见问题与解决方案)
- [7. 最佳实践](#7-最佳实践)
- [参考资料](#参考资料)

---

## 🎯 前置知识点

在学习本文档之前，你需要掌握以下基础知识：

### 基础知识点（必须掌握）

- **JDK 安装与环境配置** 📖 [J1B - JDK 安装与环境配置完全指南](./J1B-为什么99%的人配置Java环境失败？大厂开发者5分钟搞定的JDK安装与环境配置完全指南.md)
  - 已完成 JDK（Java Development Kit，Java 开发工具包）的下载和安装
  - 已正确配置 `JAVA_HOME`、`PATH`、`CLASSPATH` 三个环境变量
  - 已通过命令行验证环境配置成功（`javac -version` 能正常输出版本号）

- **Windows 操作系统基础**
  - 了解 Windows 10/11 系统的基本操作
  - 能够使用文件资源管理器浏览文件夹
  - 理解软件安装的基本流程

### 📖 学习建议

- **零基础小白**：建议先学习 J1B（JDK 安装与环境配置）文档，确保 Java 环境配置成功，再学习本文档的 IDE 安装和配置部分
- **有基础读者**：如果已经完成 JDK 环境配置，可以直接学习本文档的 IDE 选择和使用部分
- **中级开发者**：重点关注本文档中的 IDE 对比分析、常用功能与快捷键、最佳实践部分

---

## 问题描述：为什么99%的人选错IDE？

### 新手常见错误场景

**错误做法**：
- ❌ 用记事本写 Java 代码，手动编译运行，效率极低
- ❌ 选择 Eclipse（性能较差，界面老旧），学习曲线陡峭，插件配置复杂
- ❌ 不知道如何配置 IDE（Integrated Development Environment，集成开发环境），导致 IDE 识别不到 JDK（Java Development Kit，Java 开发工具包）
- ❌ 不知道如何创建 Java 项目，用 IDE 写代码仍然手动编译运行
- ❌ 不熟悉 IDE 的快捷键和常用功能，效率低下
- ❌ 不知道如何安装和配置插件，缺少必要的开发工具

**结果**：开发效率极低，代码质量差，学习进度缓慢，无法享受现代 IDE（Integrated Development Environment，集成开发环境）带来的便利。😭

### 大厂开发者的做法

**正确做法**：
- ✅ 首选 **IntelliJ IDEA**（简称 IDEA），业界最流行的 Java IDE（Integrated Development Environment，集成开发环境），功能强大、性能优秀
- ✅ 下载 **IntelliJ IDEA Community Edition（社区版）**（免费、开源），足够学习和中小型项目开发
- ✅ 正确配置 JDK（Java Development Kit，Java 开发工具包）路径，确保 IDE（Integrated Development Environment，集成开发环境）能识别 Java 开发环境
- ✅ 熟练使用 IDE（Integrated Development Environment，集成开发环境）创建项目、编写代码、运行调试，告别手动编译
- ✅ 掌握常用快捷键和功能，大幅提升开发效率
- ✅ 安装必要的插件（如 Lombok、Maven Helper），提升开发体验

**结果**：开发效率提升 5 倍，代码质量更高，学习进度更快，享受现代 IDE（Integrated Development Environment，集成开发环境）带来的便利！🚀

---

## 1. IDE 选择：IntelliJ IDEA vs Eclipse

📖 [IntelliJ IDEA 官方文档](https://www.jetbrains.com/help/idea/) 📚 [Eclipse 官方文档](https://www.eclipse.org/documentation/) 💡 [IDE 对比分析 - 菜鸟教程](https://www.runoob.com/java/java-ide.html)

### 1.1 什么是 IDE？

**IDE（Integrated Development Environment，集成开发环境）** 是一种集成了代码编辑、编译、调试、运行等功能的软件开发工具，可以大幅提升开发效率。

**生活化比喻**：
- **记事本写代码** = 用笔和纸写作文，需要手动检查语法、手动排版
- **IDE（Integrated Development Environment，集成开发环境）** = 用专业的写作软件，自动检查语法、自动排版、自动提示、一键运行

### 1.2 IntelliJ IDEA vs Eclipse 对比

| 对比项 | IntelliJ IDEA | Eclipse |
|--------|--------------|---------|
| **性能** | ⭐⭐⭐⭐⭐ 启动快、运行流畅 | ⭐⭐⭐ 启动慢、卡顿明显 |
| **代码提示** | ⭐⭐⭐⭐⭐ 智能提示、自动补全 | ⭐⭐⭐ 基础提示 |
| **界面** | ⭐⭐⭐⭐⭐ 现代化、美观 | ⭐⭐⭐ 界面老旧 |
| **学习曲线** | ⭐⭐⭐⭐ 易于上手 | ⭐⭐⭐ 学习曲线陡峭 |
| **插件生态** | ⭐⭐⭐⭐⭐ 插件丰富、质量高 | ⭐⭐⭐⭐ 插件多但质量参差不齐 |
| **价格** | Community Edition（社区版）免费，Ultimate（旗舰版）收费 | 完全免费 |
| **市场占有率** | ⭐⭐⭐⭐⭐ 大厂首选，市场占有率最高 | ⭐⭐⭐ 仍有一定用户群体 |
| **推荐度** | ✅ **强烈推荐** | ⚠️ 不推荐（除非有特殊需求） |

### 1.3 为什么选择 IntelliJ IDEA？

**核心优势**：
1. **性能优秀**：启动快、运行流畅，不会像 Eclipse 那样卡顿
2. **智能提示**：代码自动补全、智能提示，大幅提升编码效率
3. **界面美观**：现代化界面，使用体验更好
4. **插件丰富**：插件生态完善，质量高，满足各种开发需求
5. **大厂首选**：绝大多数大厂和企业级项目都使用 IntelliJ IDEA，学习 IDEA 更有利于就业

**推荐版本**：
- **Community Edition（社区版）**：免费、开源，足够学习和中小型项目开发
- **Ultimate（旗舰版）**：收费，功能更强大，适合大型项目和企业开发

> **💡 建议**：初学者和中小型项目选择 **Community Edition（社区版）**即可，功能完全够用。

---

## 2. IntelliJ IDEA 下载与安装 <span style="background-color: #d4edda; color: #155724; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">Must</span>

📖 [IntelliJ IDEA 官方下载](https://www.jetbrains.com/idea/download/) 📚 [IntelliJ IDEA 下载与安装教程 - 菜鸟教程](https://www.runoob.com/java/java-ide.html) 💡 [IDEA 安装步骤详解 - CSDN](https://blog.csdn.net/qq_41684621/article/details/112257176)

### 2.1 下载 IntelliJ IDEA Community Edition（社区版）

1. **访问官网**：
   - 官网地址：[jetbrains.com/idea/download/](https://www.jetbrains.com/idea/download/?section=windows)
   - 选择操作系统：**Windows（操作系统）**

2. **选择版本**：
   - **推荐**：**Community Edition（社区版）**（免费、开源，足够学习和中小型项目开发）
   - 下载格式：**.exe**（图形化安装，推荐）或 **.zip**（便携版）

### 2.2 安装步骤 <span style="background-color: #d4edda; color: #155724; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">Must</span>

📚 [IntelliJ IDEA 安装步骤详解 - 菜鸟教程](https://www.runoob.com/java/java-ide.html) 💡 [IDEA 安装详细步骤 - CSDN](https://blog.csdn.net/qq_41684621/article/details/112257176)

1. **运行安装包**：
   - 双击下载的 `ideaIC-2024.1.exe`，点击「Next」

2. **选择安装路径**：
   - 默认路径：`C:\Program Files\JetBrains\IntelliJ IDEA Community Edition 2024.1`
   - **推荐保持默认路径**（避免中文、空格或特殊字符）
   - 点击「Next」

3. **安装选项**：
   - 勾选以下选项（推荐）：
     - ✅ **Create Desktop Shortcut**（创建桌面快捷方式）
     - ✅ **Add "Open Folder as Project"**（支持右键打开文件夹为项目）
     - ✅ **Associate .java files**（关联 .java 文件，双击用 IDEA 打开）
     - ✅ **Add to PATH**（可选，方便命令行启动）
   - 点击「Next」→ 「Install」→ 等待安装完成（约 1-2 分钟）→ 点击「Finish」

> **⚠️ 安装注意事项**
> - 禁止将 IDEA 安装到含中文的路径（如「C:\Java开发\idea」）
> - 禁止路径包含空格（如「C:\My IDE\idea」）
> - 首次启动会提示导入设置，选择「Do not import settings」即可

### 2.3 安装验证（初步检查） <span style="background-color: #d4edda; color: #155724; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">Must</span>

📚 [IntelliJ IDEA 安装验证方法 - 菜鸟教程](https://www.runoob.com/java/java-ide.html)

1. **启动 IDEA**：
   - 双击桌面快捷方式，或从开始菜单启动 IntelliJ IDEA
   - 首次启动会提示「Import IntelliJ IDEA Settings」，选择「Do not import settings」→ 「OK」

2. **选择主题**：
   - 选择 UI（User Interface，用户界面）主题（Light/Dark，根据喜好选择）
   - 点击「Next: Featured plugins」

3. **跳过插件安装**：
   - 初学者无需安装额外插件，直接点击「Next: Start using IntelliJ IDEA」

> **✅ 安装成功标志**：IDEA 主界面正常显示，无任何错误提示。

---

## 3. IntelliJ IDEA 基本配置 <span style="background-color: #d4edda; color: #155724; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">Must</span>

📖 [IntelliJ IDEA 配置 JDK 官方指南](https://www.jetbrains.com/help/idea/sdk.html) 📚 [IDEA 配置 JDK 教程 - 菜鸟教程](https://www.runoob.com/java/java-ide.html) 💡 [IDEA JDK 配置实战 - CSDN](https://blog.csdn.net/qq_41684621/article/details/112257176)

### 3.1 配置 JDK（关键） <span style="background-color: #d4edda; color: #155724; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">Must</span>

📖 [IntelliJ IDEA 配置 JDK 官方指南](https://www.jetbrains.com/help/idea/sdk.html) 📚 [IDEA 配置 JDK 教程 - 菜鸟教程](https://www.runoob.com/java/java-ide.html) 💡 [IDEA JDK 配置实战 - CSDN](https://blog.csdn.net/qq_41684621/article/details/112257176)

首次使用 IDEA 时，需要配置 JDK（Java Development Kit，Java 开发工具包），确保 IDE（Integrated Development Environment，集成开发环境）能识别 Java 开发环境。

**方法一：在创建新项目时配置**（推荐）

1. **点击「New Project」**：
   - 在 IDEA 主界面点击「New Project」

2. **选择 JDK**：
   - 在「New Project」界面中，点击「Project SDK」下拉框
   - 若未显示 JDK 17，点击「Add SDK」→ 「JDK」
   - 在弹出的窗口中，选择 JDK 安装路径（即 `JAVA_HOME` 路径，如 `C:\Program Files\Eclipse Adoptium\jdk-17.0.10.7-hotspot`）
   - 点击「OK」→ 此时「Project SDK」会显示「17 (Eclipse Adoptium)」

**方法二：在全局设置中配置**

1. **打开设置**：
   - 点击「File」→ 「Settings」（或使用快捷键 `Ctrl+Alt+S`）

2. **配置 SDK**：
   - 左侧导航栏选择「Build, Execution, Deployment」→ 「Build Tools」→ 「Project Settings」→ 「Project」
   - 在「Project SDK」下拉框中选择已安装的 JDK（Java Development Kit，Java 开发工具包），或点击「New」添加新的 JDK（Java Development Kit，Java 开发工具包）
   - 点击「OK」保存

> **💡 后续项目 JDK 配置**：若已创建项目，可通过「File → Project Structure → Project Settings → Project → Project SDK」重新选择或添加 JDK（Java Development Kit，Java 开发工具包）。

### 3.2 配置编码（重要） <span style="background-color: #fff3cd; color: #856404; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">Should</span>

📚 [IDEA 编码配置教程 - 菜鸟教程](https://www.runoob.com/java/java-ide.html)

为避免中文乱码问题，建议统一设置编码为 **UTF-8（Unicode Transformation Format-8，统一字符编码转换格式-8）**：

1. **打开设置**：
   - 点击「File」→ 「Settings」（或使用快捷键 `Ctrl+Alt+S`）

2. **设置编码**：
   - 左侧导航栏选择「Editor」→ 「File Encodings」
   - 设置以下选项为 **UTF-8（Unicode Transformation Format-8，统一字符编码转换格式-8）**：
     - **Global Encoding**：UTF-8（Unicode Transformation Format-8，统一字符编码转换格式-8）
     - **Project Encoding**：UTF-8（Unicode Transformation Format-8，统一字符编码转换格式-8）
     - **Default encoding for properties files**：UTF-8（Unicode Transformation Format-8，统一字符编码转换格式-8）
   - 勾选「Transparent native-to-ascii conversion」
   - 点击「OK」保存

### 3.3 配置字体和主题（可选） <span style="background-color: #cce5ff; color: #004085; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">Could</span>

📚 [IDEA 字体和主题配置教程 - 菜鸟教程](https://www.runoob.com/java/java-ide.html)

1. **配置字体**：
   - 「File」→ 「Settings」→ 「Editor」→ 「Font」
   - 推荐字体：**JetBrains Mono**（IDEA 自带，等宽字体，代码显示清晰）
   - 推荐字号：**14-16**

2. **配置主题**：
   - 「File」→ 「Settings」→ 「Appearance & Behavior」→ 「Appearance」
   - 选择主题：**Light**（浅色）或 **Dark**（深色）
   - 推荐：**IntelliJ Light**（浅色）或 **Darcula**（深色）

---

## 4. 创建第一个 Java 项目 <span style="background-color: #d4edda; color: #155724; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">Must</span>

📖 [IntelliJ IDEA 创建项目官方指南](https://www.jetbrains.com/help/idea/creating-and-running-your-first-java-application.html) 📚 [IDEA 创建项目教程 - 菜鸟教程](https://www.runoob.com/java/java-ide.html) 💡 [HelloWorld 项目实战 - 菜鸟教程在线运行](https://www.runoob.com/try/runcode.php?filename=HelloWorld&type=java)

### 4.1 创建新项目 <span style="background-color: #d4edda; color: #155724; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">Must</span>

📖 [IntelliJ IDEA 创建项目官方指南](https://www.jetbrains.com/help/idea/creating-and-running-your-first-java-application.html) 📚 [IDEA 创建项目教程 - 菜鸟教程](https://www.runoob.com/java/java-ide.html)

1. **新建 Java 项目**：
   - IDEA 主界面点击「New Project」
   - 确认「Project SDK」为 JDK 17（若未显示，参考本文档第 3.1 节配置）
   - 「Name」：输入项目名（如 `HelloWorld`）
   - 「Location」：选择项目保存路径（如 `D:\JavaProjects\HelloWorld`）
   - 取消勾选「Create Git repository」（初学者无需版本控制）
   - 点击「Create」

2. **等待项目创建**：
   - IDEA 会自动创建项目结构，等待几秒即可

### 4.2 创建 Java 类 <span style="background-color: #d4edda; color: #155724; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">Must</span>

📚 [IDEA 创建 Java 类教程 - 菜鸟教程](https://www.runoob.com/java/java-ide.html)

1. **创建 Java 类**：
   - 在左侧「Project」面板中，右键点击「src」→ 「New」→ 「Java Class」
   - 「Name」：输入 `HelloWorld`（Java 类名必须与文件名一致，首字母大写）
   - 点击「Enter」，自动生成类文件

2. **编写 HelloWorld 代码**：
```java
public class HelloWorld {
    // 主方法（程序入口）
    public static void main(String[] args) {
        // 输出内容到控制台
        System.out.println("Hello, Java! IDE 配置成功！");
    }
}
```

### 4.3 运行项目与验证 <span style="background-color: #d4edda; color: #155724; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">Must</span>

📚 [Java 程序运行教程 - 菜鸟教程](https://www.runoob.com/java/java-examples.html) 💡 [Java 程序运行实战 - 菜鸟教程在线运行](https://www.runoob.com/try/runcode.php?filename=HelloWorld&type=java)

1. **运行程序**（三种方法）：
   - **方法 1**：在代码编辑区右键 → 「Run 'HelloWorld.main()'」
   - **方法 2**：点击代码编辑区左侧的绿色三角图标 → 「Run 'HelloWorld'」
   - **方法 3**：使用快捷键「Ctrl+Shift+F10」

2. **查看运行结果**：
   - 底部「Run」面板会显示输出：`Hello, Java! IDE 配置成功！`
   - 无任何错误提示（如「Error: Could not find or load main class（主类）」）

> **✅ 项目创建成功标志**：能够正常创建项目、编写代码、运行程序，输出预期内容，无任何编译或运行错误。

---

## 5. 常用功能与快捷键 <span style="background-color: #fff3cd; color: #856404; padding: 2px 8px; border-radius: 12px; font-size: 12px; font-weight: bold;">Should</span>

📖 [IntelliJ IDEA 快捷键官方文档](https://www.jetbrains.com/help/idea/mastering-keyboard-shortcuts.html) 📚 [IDEA 常用快捷键教程 - 菜鸟教程](https://www.runoob.com/java/java-ide.html) 💡 [IDEA 快捷键大全 - CSDN](https://blog.csdn.net/qq_41684621/article/details/112257176)

### 5.1 常用快捷键

**代码编辑**：
- **`Ctrl + Space`**：代码自动补全（最常用）
- **`Ctrl + Shift + Space`**：智能代码补全
- **`Ctrl + Alt + L`**：格式化代码
- **`Ctrl + D`**：复制当前行
- **`Ctrl + Y`**：删除当前行
- **`Ctrl + /`**：注释/取消注释（单行）
- **`Ctrl + Shift + /`**：注释/取消注释（多行）

**代码导航**：
- **`Ctrl + N`**：快速查找类
- **`Ctrl + Shift + N`**：快速查找文件
- **`Ctrl + B`**：跳转到定义
- **`Ctrl + Alt + B`**：跳转到实现
- **`Alt + ←/→`**：切换编辑标签页

**代码重构**：
- **`Shift + F6`**：重命名（变量、方法、类）
- **`Ctrl + Alt + M`**：提取方法
- **`Ctrl + Alt + V`**：提取变量

**运行和调试**：
- **`Shift + F10`**：运行程序
- **`Shift + F9`**：调试程序
- **`Ctrl + F9`**：编译项目

### 5.2 常用功能

**代码提示**：
- IDEA 会自动提示代码，输入部分代码后按 `Ctrl + Space` 即可自动补全

**代码格式化**：
- 使用 `Ctrl + Alt + L` 可以快速格式化代码，统一代码风格

**快速修复**：
- 当代码有错误时，IDEA 会显示红色波浪线，按 `Alt + Enter` 可以快速修复

**代码搜索**：
- 使用 `Ctrl + F` 在当前文件中搜索
- 使用 `Ctrl + Shift + F` 在整个项目中搜索

**快速生成代码**：
- 输入 `psvm` 后按 `Tab` 键，自动生成 `main` 方法
- 输入 `sout` 后按 `Tab` 键，自动生成 `System.out.println()`

---

## 6. 常见问题与解决方案

📚 [Java 环境配置常见问题 - 菜鸟教程](https://www.runoob.com/java/java-environment-setup.html)

### 6.1 问题 1：IDEA 找不到 JDK

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
   - 若路径正确但仍无法识别，卸载 JDK 后重新安装（参考 J1B 文档）
```

### 6.2 问题 2：运行程序提示找不到主类

**现象**：执行 `Run` 时提示「Error: Could not find or load main class（主类） HelloWorld」

**解决方案**：
```cmd
# 解决方案：
1. 检查类名与文件名是否一致：
   - Java 类名必须与文件名完全一致（包括大小写）
   - 如类名 HelloWorld，文件名必须是 HelloWorld.java

2. 检查 main 方法是否正确定义：
   - main 方法必须是 public static void main(String[] args)

3. 检查项目结构：
   - 确认 .java 文件在 src 目录下
   - 右键点击项目 → 「Reload from Disk」刷新项目
```

### 6.3 问题 3：中文乱码

**现象**：程序输出中文时显示乱码（如「Hello, 涓枃!」）

**解决方案**：
```cmd
# 解决方案：
1. 配置 IDE 编码（参考本文档第 3.2 节）：
   - File → Settings → Editor → File Encodings
   - 所有编码设置为 UTF-8
   - 勾选「Transparent native-to-ascii conversion」

2. 重新编译运行：
   - 修改编码后，重新编译运行程序
```

### 6.4 问题 4：IDEA 运行缓慢

**现象**：IDEA 启动慢、运行卡顿

**解决方案**：
```cmd
# 解决方案：
1. 增加内存分配：
   - Help → Edit Custom VM Options
   - 修改 -Xmx（最大内存）和 -Xms（初始内存）参数
   - 推荐：-Xms512m -Xmx2048m（根据电脑配置调整）

2. 关闭不必要的插件：
   - File → Settings → Plugins
   - 禁用不需要的插件

3. 清理缓存：
   - File → Invalidate Caches / Restart
   - 选择「Invalidate and Restart」
```

---

## 7. 最佳实践

📚 [Java 开发最佳实践 - 菜鸟教程](https://www.runoob.com/java/java-tutorial.html)

### 7.1 IDE 选择建议

- **首选 IntelliJ IDEA Community Edition（社区版）**：免费、功能强大、性能优秀，适合绝大多数开发者
- **不建议使用 Eclipse**：性能较差、界面老旧，除非有特殊需求
- **不建议用记事本写代码**：效率极低，无法享受现代 IDE 的便利

### 7.2 项目结构规范

```cmd
# 推荐的项目结构：
HelloWorld/          # 项目根目录
├── src/             # 源代码目录
│   └── com/         # 包名（反向域名，如公司域名com.example）
│       └── demo/
│           └── HelloWorld.java  # 业务代码
├── out/             # 编译输出目录（IDEA自动生成）
└── README.md        # 项目说明文档
```

### 7.3 开发规范

- **使用快捷键**：熟练掌握常用快捷键，大幅提升开发效率
- **代码格式化**：编写代码后及时格式化（`Ctrl + Alt + L`），保持代码风格统一
- **代码注释**：关键代码添加注释，提高代码可读性
- **及时保存**：IDEA 会自动保存，但建议养成 `Ctrl + S` 保存的习惯

### 7.4 插件推荐（可选）

📚 [IDEA 插件推荐 - 菜鸟教程](https://www.runoob.com/java/java-ide.html)

**初学者推荐插件**：
- **Lombok**：简化 Java 代码，减少样板代码
- **Maven Helper**：Maven 依赖管理（如果使用 Maven）
- **Rainbow Brackets**：彩色括号，提高代码可读性

**安装方法**：
- 「File」→ 「Settings」→ 「Plugins」
- 搜索插件名称 → 点击「Install」→ 重启 IDEA

---

## 参考资料

### 官方文档

📖 [IntelliJ IDEA 官方文档](https://www.jetbrains.com/help/idea/)  
📖 [Eclipse 官方文档](https://www.eclipse.org/documentation/)

### 教程资源

📚 [IntelliJ IDEA 使用教程 - 菜鸟教程](https://www.runoob.com/java/java-ide.html)  
📚 [IDEA 创建项目教程 - 菜鸟教程](https://www.runoob.com/java/java-ide.html)  
💡 [IntelliJ IDEA 安装配置完整指南 - CSDN](https://blog.csdn.net/qq_41684621/article/details/112257176)  
💡 [IDEA 快捷键大全 - CSDN](https://blog.csdn.net/qq_41684621/article/details/112257176)

### 实践工具

💡 [Java 在线编译器](https://www.runoob.com/try/runcode.php?filename=HelloWorld&type=java)  
💡 [IntelliJ IDEA 下载地址](https://www.jetbrains.com/idea/download/)

---

## 结语：掌握 Java IDE 选择的精髓

通过本文档的详细步骤，你已经掌握了如何选择并快速上手 Java 开发利器。记住，**IDE 选择不是随意的，而是影响开发效率的关键**：

1. **选择正确的 IDE**：首选 IntelliJ IDEA Community Edition（社区版），功能强大、性能优秀
2. **正确配置环境**：确保 JDK 路径配置正确，IDE 能识别 Java 开发环境
3. **掌握常用功能**：熟练使用快捷键和常用功能，大幅提升开发效率
4. **遵循最佳实践**：规范项目结构，养成良好的开发习惯

**IDE 是 Java 开发者的利器**。选择了正确的 IDE，掌握了正确的使用方法，你就能避免 99% 的 IDE 选择问题，快速进入高效开发的世界，成为一名优秀的 Java 开发者！💪

---

**作者**：郑恩赐  
**机构**：厦门工学院人工智能创作坊  
**日期**：2025 年 11 月 06 日

