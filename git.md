# Git 完整指南

### 1.1 什么是 Git 📚

> **一句话定义**：Git 是一个开源的分布式版本控制系统，用于高效管理项目代码的版本和历史。

> **通俗理解**：
> 
> 想象你在写一篇论文，每次修改都怕把之前的版本搞丢了。Git 就像一个"时光机"，可以：
> - 保存每次修改的"快照"
> - 随时回退到任意历史版本
> - **多人协作不冲突**（每个人在独立分支工作，最后合并）
> - 离线也能工作

> **核心特点**：
> 
> | 特点 | 说明 |
> |:-----|:-----|
> | **分布式** | 每个开发者都有完整的代码仓库 |
> | **离线工作** | 不需要联网也能提交代码 |
> | **分支管理** | 轻松创建、切换、合并分支 |
> | **速度快** | 本地操作，秒级响应 |

Git 简介参考资料：
- [Git 是什么--Microsoft Learn](https://docs.microsoft.com/zh-cn/devops/develop/git/what-is-git)
- [Git版本控制系统详解--CSDN](https://blog.csdn.net/xingzhemengyou1/article/details/159800029)

---

### 1.2 什么是代码托管平台 🌐

> **一句话定义**：代码托管平台是基于 Git 的**远程代码存储服务**，让你可以把本地代码上传到云端，实现备份、分享和多人协作。

> **通俗理解**：
> 
> 如果把 Git 比作"邮件客户端"，那代码托管平台就是"邮箱服务商"：
> - Git 负责在本地管理代码版本
> - 代码托管平台负责在云端存储代码
> - 两者配合，实现本地↔云端的双向同步

> **主流平台对比**：
> 
> | 平台 | 特点 | 适用场景 |
> |:-----|:-----|:---------|
> | **GitHub** | 全球最大开源社区，生态丰富 | 开源项目、国际协作 |
> | **Gitee（码云）** | 国内访问快，本土化服务好 | 国内项目、中文文档 |
> | **GitCode** | 华为云+CSDN联合打造，大文件托管能力强 | 大文件项目、内置CI/CD需求 |
> | **GitLab** | 支持私有化部署 | 企业内部、安全要求高 |

> **核心功能**：
> - 📦 **代码托管**：安全存储代码历史版本
> - 🤝 **协作开发**：多人共同维护项目
> - 🔄 **CI/CD**：自动化构建、测试、部署
> - 📊 **项目管理**：Issue、PR、Wiki 等工具

代码托管平台参考资料：
- [同样是代码托管，GitLab、GitHub、Gitee、GitCode之间有什么区别--CSDN](https://blog.csdn.net/BradenHan/article/details/136673828)
- [2025 Gitee 与 GitHub 全面对比--掘金](https://juejin.cn/post/7570984341414887439)

---

### 1.3 Git 与代码托管平台的关系 🔗

> **一句话总结**：Git 是**工具**，代码托管平台是**服务**；Git 先诞生（2005年），GitHub 后出现（2008年）。

> **历史时间线**：
> 
> | 时间 | 事件 | 意义 |
> |:-----|:-----|:-----|
> | **2005年4月** | Linus Torvalds 创建 Git | 解决 Linux 内核版本管理问题 |
> | **2008年4月** | GitHub 正式上线 | 首创 Fork+PR 协作模式，开启代码社交时代 |
> | **2018年6月** | 微软收购 GitHub | 加速 DevOps 与 AI 生态整合 |

> **两者关系**：
> 
> 可以把它们比作**笔和纸**：
> - **Git = 笔**：负责在本地"写字"（管理代码版本）
> - **代码托管平台 = 纸**：提供"纸张"让你存放和分享作品
> - 没有笔，纸无法书写；没有纸，笔只能本地使用

> **核心区别**：
> 
> | 对比项 | Git | 代码托管平台（如 GitHub） |
> |:-------|:----|:------------------------|
> | **本质** | 本地版本控制工具 | 云端代码托管服务 |
> | **是否需要网络** | 不需要，可离线使用 | 需要网络访问远程仓库 |
> | **功能** | 提交、分支、合并等 | 仓库托管、协作、CI/CD、项目管理 |
> | **关系** | 独立存在 | 基于 Git 构建，依赖 Git 实现版本控制 |

Git 与 GitHub 关系参考资料：
- [【编程史】Git是啥?它和GitHub关系是?--掘金](https://juejin.cn/post/7515461483893145610)
- [Git 和 GitHub 入门教程--CSDN](https://blog.csdn.net/hhw_hhw/article/details/148510950)

---

## 2. Git 安装与配置 ⚙️

> 💡 **说明**：由于大部分开发者使用 Windows 系统进行开发，本章主要讲解 **Windows 环境下的 Git 安装与配置**。macOS 和 Linux 用户可参考官方文档进行安装。

### 2.1 Windows 安装

> **安装步骤**：
> 
> 1. 访问官方下载页面：[https://git-scm.com/install/windows](https://git-scm.com/install/windows)
> 
> 2. 点击 **"Click here to download"** 下载最新版本（例如 x64 版本）
> 
> 3. 或者选择 **"Other Git for Windows downloads"** 中的特定版本：
> 
>    | 版本类型 | 具体选项 | 说明 |
>    |:---------|:---------|:-----|
>    | **Standalone Installer** | Git for Windows/x64 Setup | 标准安装版（64位），适合大多数电脑 |
>    | | Git for Windows/ARM64 Setup | 标准安装版（ARM架构），适合ARM设备 |
>    | **Portable** | Git for Windows/x64 Portable | 便携版，双击解压出文件夹，无需安装，适合U盘携带 |
>    | | Git for Windows/ARM64 Portable | ARM便携版，解压即用，不修改系统环境 |
>    | **Using winget** | `winget install --id Git.Git -e --source winget` | 命令行一键安装 |
> 
>    💡 **如何选择**：普通电脑选 **x64 Setup**；需要U盘携带选 **Portable**；ARM设备选 **ARM64** 版本
> 
> 4. **验证安装**：
>    - **Setup 版本**：直接在命令行输入 `git --version`
>    - **Portable 版本**：进入解压后的 `bin` 目录，使用完整路径运行，如 `D:\Git\bin\git.exe --version`
> 
>    > 💡 **可以给 Portable 配置环境变量，但不推荐**
>    > 
>    > 如果配置了环境变量，拔出 U 盘后：
>    > - 环境变量里还残留着 U 盘路径（如 `D:\Git\bin`）
>    > - 下次输入 `git` 命令会报错"找不到命令"
>    > - 污染系统环境，影响其他依赖 git 的软件
>    > 
>    > Portable 的设计初衷就是**即插即用、零残留**，用完整路径运行最符合这个理念
> 
> **关于 winget 命令安装**：
> 
> > 💡 **什么是 winget？**
> > 
> > winget 是**微软官方推出的 Windows 包管理器**（Windows Package Manager），对标 Linux 的 `apt` / `yum`、macOS 的 `Homebrew`。它是 Windows 10/11 系统自带的命令行工具，让你用一行命令就能搜索、安装、更新、卸载软件。
> 
> winget 其实是**自动化下载安装器**，它会自动从 GitHub 下载 `Git-2.54.0-64-bit.exe` 并执行安装，本质上和手动下载是一样的：
> 
> ```
> C:\Users\zheng>winget install --id Git.Git -e --source winget
> Found Git [Git.Git] Version 2.54.0
> Downloading https://github.com/git-for-windows/git/releases/download/...
> Successfully installed
> ```
> 
> ✅ **winget 的优势**：
> - ⚡ **更快**：命令行下载速度通常比浏览器快
> - 🖱️ **省事**：一键完成下载+安装，无需手动点击
> - 🔄 **易更新**：`winget upgrade Git.Git` 一键更新到最新版
> - 📋 **好管理**：`winget list` 查看所有已安装软件

### 2.2 基础配置

> 💡 **配置的第一步：设置用户名和邮箱**
> 
> 就像使用软件需要先登录一样，Git 也需要知道"你是谁"。**用户名和邮箱是 Git 配置的必选项**，每次提交代码时都会记录这些信息。

> **为什么需要配置用户名和邮箱？**
> 
> Git 是分布式版本控制系统，每次提交代码时都需要记录"是谁提交的"。**如果不配置，会导致提交失败**，报错信息如下：
> 
> ```
> *** Please tell me who you are.
> 
> Run
>   git config --global user.name "Your Name"
>   git config --global user.email "you@example.com"
> ```
> 
> 配置后可以避免：
> - 提交记录显示为 unknown 或系统默认用户名
> - 无法与 GitHub/Gitee 等平台账号正确关联
> - 团队协作时难以追溯代码来源

> **全局配置（推荐）**：
> 
> 使用 `--global` 参数配置，适用于当前用户在本机上的所有 Git 仓库：
> 
> ```bash
> # 设置用户名（建议使用真实姓名或常用昵称）
> git config --global user.name "Your Name"
> 
> # 设置邮箱（建议使用 GitHub/Gitee 绑定的邮箱）
> git config --global user.email "your.email@example.com"
> ```
> 
> 💡 **建议**：首次安装 Git 后，第一时间执行这两个命令！

> **验证配置**：
> 
> ```bash
> # 查看用户名
> git config --global user.name
> 
> # 查看邮箱
> git config --global user.email
> 
> # 查看所有配置
> git config --list
> ```

> **Git 配置的三个级别**：
> 
> Git 支持三个级别的配置，优先级从高到低：**Local > Global > System**
> 
> | 级别 | 参数 | 作用范围 | 配置文件位置 |
> |:-----|:-----|:---------|:-------------|
> | **Local（本地）** | `--local` | 当前仓库 | `.git/config` |
> | **Global（全局）** | `--global` | 当前用户所有仓库 | `~/.gitconfig` |
> | **System（系统）** | `--system` | 系统所有用户 | `/etc/gitconfig` |
> 
> 💡 **使用建议**：
> - 个人开发：用 `--global` 设置默认身份
> - 多身份场景：工作项目用 `--local` 单独配置公司邮箱
> - System 级别：企业统一配置时使用（需管理员权限）

> **本地配置示例（工作/个人分离）**：
> 
> ```bash
> # 进入工作项目目录
> cd /path/to/work-project
> 
> # 单独配置工作身份（不加 --global，默认就是 --local）
> git config user.name "Work Name"
> git config user.email "work@company.com"
> ```
> 
> 这样工作项目用公司邮箱，其他项目用个人邮箱，互不干扰。

Git 基础配置参考资料：
- [Git 用户名与邮箱配置指南--CSDN](https://blog.csdn.net/wenxuankeji/article/details/153337947)
- [Git 提交时为什么必须设置用户名和邮箱--CSDN](https://wenku.csdn.net/answer/z3rz3f2macyt)
- [Git配置层级：system、global、local配置的优先级处理--CSDN](https://blog.csdn.net/gitblog_00908/article/details/151811087)

---

## 3. .git 目录是什么？📁

> 💡 **接下来我们要了解一个很重要的东西——.git 文件夹**
> 
> 它是 Git 的核心，理解了它，你就理解了 Git 是如何存储版本历史的。

> `.git` 文件夹是 **Git 的版本库**，包含了项目所有的版本控制信息和历史记录。

> **.git 文件夹在哪里？**
> 
> `.git` 位于**项目根目录下**，是一个隐藏文件夹。
> 
> 例如：
> - 如果你的项目在 `C:\Users\user\my-project`，那么 `.git` 就在 `C:\Users\user\my-project\.git`
> - 如果你的项目在 `/home/user/myproject`，那么 `.git` 就在 `/home/user/myproject/.git`
> 
> 💡 **注意**：`.git` 是隐藏文件夹，Windows 需要在文件资源管理器中开启"显示隐藏文件"才能看到。

> 💡 **Git 命令的本质**
> 
> 你使用的所有 Git 命令，本质上都是在**读取或修改 `.git` 目录中的文件**。比如：
> - 提交代码时，Git 会把代码内容写入 `.git/objects/`
> - 查看历史时，Git 会从 `.git/objects/` 和 `.git/refs/` 中读取记录
> - 切换分支时，Git 会根据 `.git/HEAD` 的指向恢复文件

> **.git 目录的核心文件和文件夹**：
> 
> | 文件/文件夹 | 作用 |
> |:------------|:-----|
> | **HEAD** | 指向当前所在的分支 |
> | **config** | 该仓库的本地配置文件 |
> | **index** | 暂存区（Stage）的信息 |
> | **objects/** | 存储所有文件内容和版本数据 |
> | **refs/** | 存储分支和标签的引用 |
> | **hooks/** | 钩子脚本（如提交前自动检查） |

> 💡 **重要提示**：
> - `.git` 是**隐藏文件夹**，Windows 需要在文件资源管理器中开启"显示隐藏文件"才能看到
> - **不要手动修改** `.git` 目录下的内容，否则可能导致版本库损坏
> - 删除 `.git` 文件夹 = 删除整个版本历史，项目变成普通文件夹

.git 目录参考资料：
- [.git 文件夹解析教程--CSDN](https://blog.csdn.net/Rysxt_/article/details/151074098)
- [仓库创建与配备-.git目录的结构与作用--51CTO](https://blog.51cto.com/u_15469972/14471718)

---

## 4. Git 基础操作 📝

> 💡 **如何开始使用 Git？**
> 
> 一个新项目创建时是**没有** `.git` 文件夹的，它只是一个普通文件夹。你需要在项目根目录下运行 `git init` 命令，Git 才会创建 `.git` 目录，把这个项目变成 Git 仓库。
> 
> **三种获取 Git 仓库的方式**：
> 
> | 方式 | 命令 | 说明 |
> |:-----|:-----|:-----|
> | **本地初始化** | `git init` | 在现有项目目录创建 `.git` |
> | **创建新项目** | `git init my-project` | 先创建文件夹，再在里面创建 `.git` |
> | **克隆远程仓库** | `git clone <url>` | 下载的项目**已经包含** `.git` 和历史记录，如 Gitee 或 GitCode 上的项目 |

### 4.1 仓库操作命令

#### git init - 初始化仓库

**作用**：在当前目录创建 `.git` 文件夹，把普通目录变成 Git 仓库。

**使用场景**：
- 创建新项目时
- 把已有项目纳入 Git 管理

**示例**：
```bash
# 在当前目录初始化
$ git init
Initialized empty Git repository in F:/my-project/.git/

# 创建新目录并初始化
$ git init my-project
```

---

#### git clone - 克隆远程仓库

**作用**：从远程仓库下载完整项目（包括所有历史记录），自动创建本地仓库。

**使用场景**：
- 加入已有项目
- 学习开源项目

**示例**：
```bash
# 克隆 Gitee 上的项目
$ git clone https://gitee.com/username/repo.git

# 克隆时指定本地文件夹名
$ git clone https://gitee.com/username/repo.git my-folder

# 只克隆最新版本（节省时间和空间）
$ git clone --depth 1 https://gitee.com/username/repo.git
```

💡 可以试试克隆这个项目：

```bash
git clone https://gitcode.com/ZhengEnCi/ai-workshop-student-management-system-front-end.git
```

---

### 4.2 日常开发命令

#### git add - 添加到暂存区

**作用**：把工作区的修改放入暂存区，准备提交。

**使用场景**：
- 完成一部分代码，准备提交
- 选择性地提交部分文件

**示例**：
```bash
# 添加单个文件
$ git add filename.txt

# 添加所有修改（最常用）
$ git add .

# 添加所有 .py 文件
$ git add *.py

# 交互式选择（按代码块选择）
$ git add -p
```

💡 **暂存区是什么？**

暂存区是**工作区和本地仓库之间的"中转站"**（对应 `.git/index` 文件）。

它的作用是让你**选择性提交**：
- 可以只提交部分修改，而不是全部
- 可以多次 `git add`，逐步构建一次提交
- 提交前可以预览确认，避免误提交

简单理解：就像**机场安检台**——把要托运的行李放上去检查，确认无误后再打包上飞机。

---

#### git commit - 提交到本地仓库

**作用**：把暂存区的内容保存到本地仓库，生成一个新的版本记录。

**使用场景**：
- 完成一个功能或修复
- 保存代码的重要节点

**示例**：
```bash
# 基本提交（必须加 -m 写说明）
$ git commit -m "完成了登录功能"

# 添加并提交（跳过 git add）
$ git commit -am "修复了样式bug"
```

⚠️ **注意**：`-am` 只处理**已跟踪的文件**（之前提交过的文件），**新文件不会被包含**！新文件仍需先用 `git add` 添加。

💡 **写好提交信息的原则**：
- 第一行简要说明（50字以内）
- 空一行后详细描述（可选）
- 使用现在时态，如"添加功能"而非"添加了功能"

---

#### git status - 查看状态

**作用**：查看工作区和暂存区的文件状态。

**使用场景**：
- 随时了解哪些文件被修改
- 确认哪些文件已准备好提交

**示例**：
```bash
$ git status
On branch master
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
        modified:   index.html

Untracked files:
  (use "git add <file>..." to include in what will be committed)
        newfile.js
```

**输出解读**：
- `modified`：已修改但未暂存
- `staged`：已暂存，等待提交
- `untracked`：新文件，Git 未跟踪

---

#### git diff - 查看差异

**作用**：比较不同区域之间的代码差异。

**使用场景**：
- 提交前检查改了什么
- 对比不同版本之间的变化

**示例**：
```bash
# 查看工作区 vs 暂存区的差异
$ git diff

# 查看暂存区 vs 上次提交的差异
$ git diff --cached

# 查看某个文件的差异
$ git diff filename.txt
```

---

### 4.3 历史查看命令

#### git log - 查看提交历史

**作用**：查看项目的提交记录，包括作者、时间、提交信息。

**使用场景**：
- 回顾项目发展历程
- 查找某个功能的提交

**示例**：
```bash
# 完整显示
$ git log

# 简洁显示（推荐）
$ git log --oneline

# 显示最近3条
$ git log -3

# 图形化显示分支合并
$ git log --oneline --graph --all

# 显示每次提交的详细修改
$ git log -p
```

**输出示例**：
```
commit a1b2c3d (HEAD -> master)
Author: 张三 <zhangsan@example.com>
Date:   Mon Jan 1 10:00:00 2025

    添加了用户登录功能
```

---

### 4.4 撤销与回退命令

#### git checkout -- - 撤销工作区修改

**作用**：丢弃工作区的修改，恢复为上次提交的状态。

**使用场景**：
- 改错了代码，想恢复到之前的状态
- 实验性修改后决定放弃

**示例**：
```bash
# 撤销单个文件
$ git checkout -- filename.txt

# 撤销所有修改（⚠️ 危险操作）
$ git checkout -- .
```

⚠️ **警告**：此操作会**永久丢失**未提交的修改，无法恢复！

---

#### git reset HEAD - 撤销暂存

**作用**：把文件从暂存区移回工作区（取消 add）。

**使用场景**：
- 不小心 add 了不该提交的文件
- 想重新选择要提交的文件

**示例**：
```bash
# 把文件从暂存区移回工作区
$ git reset HEAD filename.txt

# 撤销所有暂存
$ git reset HEAD .
```

💡 **注意**：文件内容不会丢失，只是回到未 add 的状态。

---

#### git reset - 版本回退

**作用**：回退到之前的某个版本。

**使用场景**：
- 代码出现严重问题，需要回滚
- 提交了错误的代码

**示例**：
```bash
# 查看历史，找到 commit id
$ git log --oneline

# 软回退（保留修改，回到暂存区）
$ git reset --soft HEAD~1

# 混合回退（保留修改，回到工作区，默认）
$ git reset --mixed HEAD~1

# 硬回退（⚠️ 彻底丢弃修改）
$ git reset --hard HEAD~1

# 回退到指定版本
$ git reset --hard abc1234
```

**三种模式对比**：

| 模式 | 工作区 | 暂存区 | 说明 |
|:-----|:-------|:-------|:-----|
| `--soft` | 保留 | 保留 | 只移动 HEAD，适合重新提交 |
| `--mixed` | 保留 | 清空 | 默认模式，修改回到工作区 |
| `--hard` | 清空 | 清空 | ⚠️ 彻底回退，数据丢失！|

⚠️ **警告**：`--hard` 会永久删除未提交的修改，使用前请确认！

---

### 4.5 综合实践

> 通过一个完整的练习，巩固本章学到的 Git 基础命令。

#### 第一步：克隆仓库

**目标**：将远程仓库下载到本地。

**操作**：

> 💡 **克隆位置说明**：在哪个目录执行 `git clone`，项目就会下载到哪个目录下。
> 
> 例如：在桌面执行，项目就会下载到 `C:\Users\你的用户名\Desktop\ai-workshop-student-management-system-front-end`

```bash
# 先进入桌面（示例）
$ cd C:\Users\zheng\Desktop

# 克隆 AI Workshop 学生管理系统前端项目
$ git clone https://gitcode.com/ZhengEnCi/ai-workshop-student-management-system-front-end.git
```

**验证**：

> 克隆完成后，在桌面打开 `ai-workshop-student-management-system-front-end` 文件夹，查看以下内容：
> 
> - **项目文件**（如 `index.html`、`css`、`js` 等）
> - **`README.md` 文件**（项目的"说明书"，介绍项目是什么、怎么用）
> - **隐藏的 `.git` 文件夹**（Git 仓库的标志，需要在文件资源管理器中开启"显示隐藏的项目"）
> 
> 💡 **关于 README.md**：
> 
> 一个规范的开源项目通常都会有 `README.md` 文件，它是项目的**入口和名片**，用来告诉访问者：
> - 这个项目是做什么的
> - 如何安装和使用
> - 项目的功能特点

---

#### 第二步：查看仓库状态（练习 `git status`）

**目标**：使用 `git status` 查看当前仓库的状态。

**操作**：
```bash
# 确保你在项目目录下
$ cd ai-workshop-student-management-system-front-end

# 查看仓库状态
$ git status
```

**预期输出**：
```
git status
Refresh index: 100% (410/410), done.
On branch master
Your branch is up to date with 'origin/master'.

nothing to commit, working tree clean
```

**说明**：
- `On branch master`：当前在 master 分支上（分支相关内容在后面详细讲解）
- `nothing to commit`：没有需要提交的修改
- `working tree clean`：工作区很干净

---

#### 第三步：查看提交历史（练习 `git log`）

**目标**：使用 `git log` 查看项目的提交历史。

**操作**：
```bash
# 查看完整提交历史
$ git log

# 查看简洁版（推荐）
$ git log --oneline

# 查看最近3条提交
$ git log -3
```

**`git log` 预期输出**（部分）：
```
git log
commit 0c09fcf104bcc80ce028d872c2f41b4ca4101737 (HEAD -> master, origin/master, origin/HEAD)
Author: 王乐宸 <1954326264@qq.com>
Date:   Sat Apr 25 17:12:04 2026 +0800

    添加开发成员王乐宸

commit 338b28ae59cda617c5f1faeed6198238643e2f54
Author: ZhengEnCi <zheng_enci@qq.com>
Date:   Thu Apr 23 21:18:02 2026 +0800

    docs: 将README中相对路径链接改为GitCode完整URL
:...skipping...
```

**说明**：
- 显示完整的 commit ID、作者、日期和提交信息
- `:...skipping...` 表示还有更多内容，按 `q` 退出查看

---

**`git log --oneline` 预期输出**（部分）：
```
git log --oneline
0c09fcf1 (HEAD -> master, origin/master, origin/HEAD) 添加开发成员王乐宸
338b28ae docs: 将README中相对路径链接改为GitCode完整URL
4f890576 docs: 修正README中English Version链接的分支名为master
c9663890 docs: 将README中English Version链接改为GitCode完整URL
bcd6303c docs: 重命名README_CN.md为README_EN.md
3f8e25c7 docs: 将README_CN.md翻译为英文版
5bb92d32 docs: 修复README.md中Logo路径
455c85ba docs: 在README.md标题区域添加项目Logo
6cc9a2e5 docs: 将'开发团队'改为'我'
656dcd3c docs: 润色设计原则表述
a4e75d22 docs: 润色JS/TS混用说明的表述
...
```

**说明**：
- 每条记录只显示一行，更简洁
- 显示简短的 commit ID 和提交信息

---

**`git log -3` 预期输出**：
```
git log -3
commit 0c09fcf104bcc80ce028d872c2f41b4ca4101737 (HEAD -> master, origin/master, origin/HEAD)
Author: 王乐宸 <1954326264@qq.com>
Date:   Sat Apr 25 17:12:04 2026 +0800

    添加开发成员王乐宸

commit 338b28ae59cda617c5f1faeed6198238643e2f54
Author: ZhengEnCi <zheng_enci@qq.com>
Date:   Thu Apr 23 21:18:02 2026 +0800

    docs: 将README中相对路径链接改为GitCode完整URL

commit 4f89057690c87a1d2ed2990bca0ca6f27c9ed6cd
Author: ZhengEnCi <zheng_enci@qq.com>
Date:   Thu Apr 23 21:16:36 2026 +0800

    docs: 修正README中English Version链接的分支名为master
```

**说明**：
- `-3` 表示只显示最近3条提交
- 适合快速查看最新提交历史

---

#### 第四步：修改文件并查看差异（练习 `git diff`）

**目标**：修改文件后，使用 `git diff` 查看修改内容。

**操作**：
```bash
# 1. 先执行 git diff，确认当前没有修改
$ git diff

# 2. 用文本编辑器打开 README.md，在最后一行添加 "Hello git"，然后保存

# 3. 再次执行 git diff，查看工作区的修改
$ git diff

# 4. 查看仓库状态
$ git status
```

**第1步预期输出**（修改前）：
```
git diff
# 没有任何输出，表示工作区没有修改
```

**第3步预期输出**（修改后）：
```
git diff
diff --git a/README.md b/README.md
index 686311c9..779455c8 100644
--- a/README.md
+++ b/README.md
@@ -552,3 +552,4 @@ API 接口定义在 `src/api/` 目录：
 Made with ❤ by 郑恩赐
 
 </div>
+Hello git
\ No newline at end of file
```

**说明**：
- `diff --git a/README.md b/README.md`：表示比较 a/README.md（修改前）和 b/README.md（修改后）
- `index 686311c9..779455c8 100644`：显示文件的哈希值索引，100644 是文件权限
- `--- a/README.md`：表示原文件内容（a 代表修改前）
- `+++ b/README.md`：表示修改后的内容（b 代表修改后）
- `@@ -552,3 +552,4 @@`：表示变更的位置（-552,3 表示原文件第552行开始的3行；+552,4 表示修改后第552行开始的4行）
- `+` 开头的行表示新增的内容
- `-` 开头的行表示删除的内容
- `\ No newline at end of file`：表示文件末尾没有换行符

**第4步预期输出**：
```
git status
On branch master
Your branch is up to date with 'origin/master'.

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   README.md

no changes added to commit (use "git add" and/or "git commit -a")
```

**说明**：
- `On branch master`：当前在 master 分支上
- `Your branch is up to date with 'origin/master'`：本地分支与远程分支同步
- `Changes not staged for commit`：有修改但未添加到暂存区
- `modified: README.md`：README.md 文件被修改了
- `use "git add <file>..."`：提示可以使用 `git add` 添加文件到暂存区
- `use "git restore <file>..."`：提示可以使用 `git restore` 撤销修改

---

#### 第五步：添加到暂存区（练习 `git add`）

**目标**：使用 `git add` 将修改添加到暂存区。

**操作**：
```bash
# 将修改后的 README.md 添加到暂存区
$ git add README.md

# 或者添加所有修改
$ git add .

# 查看状态，确认已暂存
$ git status
```

**预期输出**：
```
git status
On branch master
Your branch is up to date with 'origin/master'.

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   README.md
```

**说明**：
- `Changes to be committed`：修改已添加到暂存区，等待提交
- `use "git restore --staged <file>..."`：提示可以使用 `git restore --staged` 撤销暂存
- 与 `Changes not staged` 不同，现在文件已经在暂存区了

---

#### 第六步：提交修改（练习 `git commit`）

**目标**：使用 `git commit` 将暂存区的修改提交到本地仓库。

**操作**：
```bash
# 提交修改，并写提交信息
$ git commit -m "在 README.md 文件末尾增加了一行 Hello git"

# 查看提交后的状态
$ git status

# 查看最新的提交历史
$ git log --oneline -3
```

**`git commit` 预期输出**：
```
git commit -m "在 README.md 文件末尾增加了一行 Hello git"
[master b2d2322f] 在 README.md 文件末尾增加了一行 Hello git
 1 file changed, 1 insertion(+)
```

**说明**：
- `[master b2d2322f]`：表示在 master 分支上创建了新提交，commit ID 是 b2d2322f
- `1 file changed, 1 insertion(+)`：1个文件被修改，增加了1行

**`git status` 预期输出**：
```
git status
On branch master
Your branch is ahead of 'origin/master' by 1 commit.
  (use "git push" to publish your local commits)

nothing to commit, working tree clean
```

**说明**：
- `Your branch is ahead of 'origin/master' by 1 commit`：本地分支比远程分支领先1个提交
- `use "git push" to publish your local commits`：提示可以使用 `git push` 推送提交到远程
- `nothing to commit, working tree clean`：工作区干净，没有未提交的修改

**`git log --oneline -3` 预期输出**：
```
git log --oneline -3
b2d2322f (HEAD -> master) 在 README.md 文件末尾增加了一行 Hello git
0c09fcf1 (origin/master, origin/HEAD) 添加开发成员王乐宸
338b28ae docs: 将README中相对路径链接改为GitCode完整URL
```

**说明**：
- 最新的提交显示在最上面
- `(HEAD -> master)` 表示当前 HEAD 指向 master 分支的最新提交
- `(origin/master, origin/HEAD)` 表示远程仓库的最新提交位置

---

#### 第七步：撤销暂存（练习 `git reset HEAD`）

**目标**：练习将文件从暂存区移回工作区。

**操作**：
```bash
# 1. 删除刚才添加的 "Hello git" 这一行

# 2. 添加到暂存区
$ git add README.md

# 3. 查看状态，确认已暂存
$ git status

# 4. 撤销暂存（从暂存区移回工作区）
$ git reset HEAD README.md

# 5. 查看状态，确认已回到工作区
$ git status
```

**第3步预期输出**（暂存状态）：
```
git status
On branch master
Your branch is ahead of 'origin/master' by 1 commit.
  (use "git push" to publish your local commits)

Changes to be committed:
  (use "git restore --staged <file>..." to unstage)
        modified:   README.md
```

**第4步预期输出**：
```
git reset HEAD README.md
Unstaged changes after reset:
M       README.md
```

**说明**：
- `Unstaged changes after reset`：表示已成功撤销暂存
- `M       README.md`：M 表示文件被修改（Modified）

**第5步预期输出**（撤销暂存后）：
```
git status
On branch master
Your branch is ahead of 'origin/master' by 1 commit.
  (use "git push" to publish your local commits)

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   README.md

no changes added to commit (use "git add" and/or "git commit -a")
```

**说明**：
- `Changes not staged for commit`：文件已回到工作区，不在暂存区
- `git reset HEAD` 不会丢失文件内容，只是取消暂存
- 文件修改仍然保留在工作区

---

#### 第八步：撤销工作区修改（练习 `git checkout --`）

**目标**：练习撤销工作区的修改，恢复到最后一次提交的状态。

**操作**：
```bash
# 1. 确认 README.md 在工作区有修改（未 add）
$ git status

# 2. 查看具体修改了什么
$ git diff README.md

# 3. 撤销工作区的修改（⚠️ 会丢失修改！）
$ git checkout -- README.md

# 4. 查看状态，确认已恢复
$ git status

# 5. 打开 README.md 文件确认内容已恢复
# 可以看到 "Hello git" 这一行又回来了，因为我们撤销了删除操作
```

**第1步预期输出**：
```
git status
On branch master
Your branch is ahead of 'origin/master' by 1 commit.
  (use "git push" to publish your local commits)

Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   README.md

no changes added to commit (use "git add" and/or "git commit -a")
```

**第2步预期输出**：
```
git diff README.md
diff --git a/README.md b/README.md
index 779455c8..d8b93b7a 100644
--- a/README.md
+++ b/README.md
@@ -551,5 +551,4 @@ API 接口定义在 `src/api/` 目录：
 
 Made with ❤ by 郑恩赐
 
-</div>
-Hello git
\ No newline at end of file
+</div>
\ No newline at end of file
```

**说明**：
- `-</div>` 和 `-Hello git`：表示这两行被删除了
- `+</div>`：表示修改后只剩下这一行

**第3步预期输出**：
```
git checkout -- README.md
# 没有任何输出，表示执行成功
```

**第4步预期输出**：
```
git status
On branch master
Your branch is ahead of 'origin/master' by 1 commit.
  (use "git push" to publish your local commits)

nothing to commit, working tree clean
```

**说明**：
- `nothing to commit, working tree clean`：工作区已恢复干净，修改已被丢弃
- 文件内容已恢复到**最近一次提交（HEAD）**时的状态

💡 **`git checkout --` 原理**：
- 用**暂存区**的内容覆盖工作区的文件
- 如果文件**没有被 add** 到暂存区，则用 **最近一次提交（HEAD）** 的内容覆盖
- 这会**永久丢弃**工作区中未提交的修改

⚠️ **警告**：`git checkout --` 会永久丢失未提交的修改，请谨慎使用！

---

#### 第九步：版本回退（练习 `git reset --hard`）

**目标**：练习回退到之前的版本。

**操作**：
```bash
# 1. 查看最近5次提交历史
$ git log --oneline -5

# 2. 回退到上一个版本（保留修改）
$ git reset --soft HEAD~1

# 或者回退到上一个版本（丢弃修改）
$ git reset --hard HEAD~1

# 3. 回退到指定版本（使用 commit ID）
$ git reset --hard abc1234

# 4. 查看提交历史确认
$ git log --oneline
```

**三种模式对比**：

| 模式 | HEAD | 暂存区 | 工作区 | 说明 |
|:-----|:-----|:-------|:-------|:-----|
| `--soft` | 回退 | 保留修改 | 保留修改 | **保留修改**：回退后，修改还在暂存区，可以直接重新提交 |
| `--mixed`（默认） | 回退 | 清空 | 保留修改 | 修改回到工作区，需要重新 add |
| `--hard` | 回退 | 清空 | 清空 | **丢弃修改**：回退后，修改完全丢失，无法恢复 |

**简单理解**：
- `--soft` **保留修改**：就像撤销提交，但修改还在"购物车"里，可以直接再提交
- `--hard` **丢弃修改**：就像彻底删除这次提交和所有修改，回到之前的状态

⚠️ **警告**：`--hard` 会永久删除未提交的修改，使用前请确认！

---

Git 基础操作参考资料：
- [Git 从入门到封神--CSDN](https://blog.csdn.net/2301_81028896/article/details/157034702)
- [Git教程(入门)--腾讯云](https://developer.cloud.tencent.com/article/2622894)
- [Revert and undo changes--GitLab Docs](https://docs.gitlab.com/ee/topics/git/undo.html)

---

## 5. 分支管理 🌿

分支是 Git 最强大的功能之一。你可以把它理解为**平行宇宙**——在同一个项目中，不同的分支可以同时进行不同的开发工作，互不干扰。

### 5.1 分支基础

#### 什么是分支？

分支就像是一条独立的时间线：
- **主分支（master/main）**：项目的稳定版本，随时可以发布
- **开发分支（develop）**：日常开发的主线
- **功能分支（feature）**：开发新功能时使用
- **修复分支（hotfix）**：紧急修复线上问题

💡 **类比**：想象你在写一本小说，主分支是已出版的版本，功能分支是你在写的番外篇，两者互不影响。

#### 查看分支

```bash
# 查看本地所有分支
$ git branch

# 查看所有分支（包括远程）
$ git branch -a

# 查看分支详情（含最后一次提交）
$ git branch -v
```

**预期输出**：
```
git branch
* master
  dev
  feature-login
```

**说明**：
- `*` 表示当前所在的分支
- `master` 是主分支
- `dev` 和 `feature-login` 是其他分支

#### 创建分支

```bash
# 方式1：仅创建分支（不切换）
$ git branch <分支名>

# 示例：创建 feature-login 分支
$ git branch feature-login
```

#### 切换分支

```bash
# 切换到指定分支
$ git checkout <分支名>

# 示例：切换到 feature-login 分支
$ git checkout feature-login
```

**预期输出**：
```
git checkout feature-login
Switched to branch 'feature-login'
```

#### 创建并切换分支（推荐）

```bash
# 一步完成创建和切换
$ git checkout -b <分支名>

# 示例：创建并切换到 dev 分支
$ git checkout -b dev
```

**预期输出**：
```
git checkout -b dev
Switched to a new branch 'dev'
```

💡 **建议**：日常开发中推荐使用 `git checkout -b`，一步到位！

#### 删除分支

```bash
# 删除已合并的分支
$ git branch -d <分支名>

# 强制删除未合并的分支
$ git branch -D <分支名>
```

⚠️ **注意**：不能删除当前所在的分支，需要先切换到其他分支。

---

### 5.2 分支合并

当功能开发完成后，需要将分支合并回主分支。

#### 合并分支

```bash
# 1. 先切换到目标分支（如 master）
$ git checkout master

# 2. 合并指定分支到当前分支
$ git merge <分支名>

# 示例：将 dev 分支合并到 master
$ git checkout master
$ git merge dev
```

**预期输出**（无冲突）：
```
git merge dev
Updating abc1234..def5678
Fast-forward
 src/login.js | 10 ++++++++++
 1 file changed, 10 insertions(+)
```

**说明**：
- `Fast-forward`：表示快速合并，没有冲突
- 列出了修改的文件和变更统计

#### 合并模式

| 模式 | 说明 | 使用场景 |
|:-----|:-----|:---------|
| **Fast-forward** | 快速合并，直接移动指针 | 目标分支没有新提交 |
| **Three-way merge** | 三方合并，创建新的合并提交 | 两个分支都有新提交 |
| **Squash merge** | 压缩合并，将多个提交合并为一个 | 保持主分支历史简洁 |

#### 查看合并历史

```bash
# 查看分支合并图
$ git log --oneline --graph --all
```

**预期输出**：
```
git log --oneline --graph --all
*   def5678 (HEAD -> master) Merge branch 'dev'
|\
| * abc1234 (dev) 添加用户登录功能
| * 7890abc 添加登录页面
* | 4567def (master) 修复首页样式
|/
* 1234abc 初始提交
```

**说明**：
- `*` 表示提交节点
- `|` 和 `\` 表示分支走向
- 可以清楚地看到分支的创建、开发和合并过程

---

### 5.3 分支策略

好的分支策略能让团队协作更高效。

#### Git Flow 工作流

Git Flow 是一种经典的分支管理模型，包含五类分支：

| 分支类型 | 名称 | 作用 | 生命周期 |
|:---------|:-----|:-----|:---------|
| **主分支** | `master` | 存放稳定、可发布的代码 | 长期存在 |
| **开发分支** | `develop` | 集成所有开发完成的特性 | 长期存在 |
| **功能分支** | `feature/*` | 开发新功能 | 临时，合并后删除 |
| **发布分支** | `release/*` | 准备发布的版本 | 临时，发布后删除 |
| **热修复分支** | `hotfix/*` | 紧急修复生产环境问题 | 临时，修复后删除 |

**工作流程**：
```
1. 从 develop 创建 feature 分支开发新功能
2. 功能完成后合并回 develop
3. 发布时从 develop 创建 release 分支
4. release 完成后合并到 master 和 develop
5. 线上问题从 master 创建 hotfix 分支修复
6. hotfix 完成后合并到 master 和 develop
```

#### GitHub Flow 工作流

GitHub Flow 是一种更简单的分支策略：

1. **master 分支**始终保持可部署状态
2. 从 master 创建功能分支进行开发
3. 完成后提交 Pull Request
4. 代码审查通过后合并到 master
5. 立即部署

💡 **适用场景**：
- Git Flow：大型项目，版本发布周期较长
- GitHub Flow：小型项目，持续部署

#### 分支命名规范

| 分支类型 | 命名示例 | 说明 |
|:---------|:---------|:-----|
| 功能分支 | `feature/login-page` | feature/功能描述 |
| 修复分支 | `fix/header-style` | fix/修复描述 |
| 热修复分支 | `hotfix/payment-bug` | hotfix/修复描述 |
| 发布分支 | `release/v1.2.0` | release/版本号 |

---

### 5.4 冲突解决

当两个分支修改了同一文件的同一位置时，就会产生冲突。

#### 冲突是如何产生的？

```
        A---B---C feature
       /
  D---E---F---G master
```

- 分支 `feature` 修改了某文件
- 分支 `master` 也修改了同一文件的同一位置
- 合并时 Git 无法自动判断该保留哪个版本

#### 解决冲突的步骤

**1. 查看冲突文件**

```bash
$ git status
```

**预期输出**：
```
git status
On branch master
You have unmerged paths.
  (fix conflicts and run "git commit")

Unmerged paths:
  (use "git add <file>..." to mark resolution)
        both modified:   src/login.js
```

**2. 打开冲突文件**

冲突文件会包含特殊标记：
```javascript
<<<<<<< HEAD
// master 分支的内容
function login() {
    return "old login";
}
=======
// feature 分支的内容
function login() {
    return "new login with OAuth";
}
>>>>>>> feature
```

**标记说明**：
- `<<<<<<< HEAD` 到 `=======`：当前分支的内容
- `=======` 到 `>>>>>>> feature`：要合并的分支的内容

**3. 手动编辑解决冲突**

删除冲突标记，保留正确的代码：
```javascript
// 解决后的内容
function login() {
    return "new login with OAuth";
}
```

**4. 标记冲突已解决**

```bash
# 添加已解决的文件
$ git add src/login.js

# 完成合并
$ git commit -m "解决 login.js 合并冲突"
```

#### 使用合并工具

```bash
# 启动图形化合并工具
$ git mergetool
```

常用的合并工具：
- **VS Code**：内置 Git 合并功能
- **Beyond Compare**：专业的文件对比工具
- **KDiff3**：开源的合并工具

#### 取消合并

如果冲突太复杂，可以取消合并：
```bash
# 取消当前合并（保留修改）
$ git merge --abort
```

#### 预防冲突的建议

1. **频繁同步**：经常从主分支拉取最新代码
2. **小步提交**：每次修改尽量小，减少冲突范围
3. **及时合并**：功能完成后尽快合并
4. **沟通协调**：多人协作时提前沟通分工

分支管理参考资料：
- [Git入门--分支管理--CSDN](https://bbs.csdn.net/topics/619739251)
- [Git 分支管理终极指南--CSDN](https://blog.csdn.net/2301_79248256/article/details/155818051)
- [Git分支管理从基础操作到团队协作工作流实践--阿里云](https://developer.aliyun.com/article/1665687)
- [Git 高级合并--Git官方文档](https://git-scm.com/book/zh/v2/Git-%E5%B7%A5%E5%85%B7-%E9%AB%98%E7%BA%A7%E5%90%88%E5%B9%B6.html)

---

### 5.5 综合实践 🎯

> 通过一个完整的练习，巩固本章学到的分支管理命令。

💡 **准备工作**：

由于前面的章节（第四章）主要练习的是基础 Git 命令，还没有涉及分支操作，所以你现在应该还在 master 分支上。但为了确保练习环境干净，建议先执行以下步骤：

```bash
# 1. 进入项目目录
$ cd ai-workshop-student-management-system-front-end

# 2. 拉取最新代码（确保与远程同步）
$ git pull origin master
```

⚠️ **注意**：`git pull` 会将远程仓库的最新代码拉取到本地，确保你从一个干净的状态开始练习。由于该项目只有一个 master 分支，且前面的练习没有创建过其他分支，所以无需额外清理。

---

#### 第一步：查看当前分支（练习 `git branch`）

**目标**：使用 `git branch` 查看当前仓库的所有分支。

**操作**：
```bash
# 查看本地分支
$ git branch

# 查看所有分支（包括远程）
$ git branch -a

# 查看分支详情
$ git branch -v
```

**预期输出**：
```
git branch
* master

git branch -a
* master
  remotes/origin/HEAD -> origin/master
  remotes/origin/master

git branch -v
* master 0c09fcf1 添加开发成员王乐宸
```

**说明**：
- `*` 表示当前在 master 分支上
- `remotes/origin/master` 是远程分支
- 最后一列显示该分支最后一次提交的说明

---

#### 第二步：创建功能分支（练习 `git checkout -b`）

**目标**：创建并切换到一个新的功能分支。

**操作**：
```bash
# 创建并切换到 feature-readme 分支
$ git checkout -b feature-readme
```

**预期输出**：
```
git checkout -b feature-readme
Switched to a new branch 'feature-readme'
```

**验证**：
```bash
# 确认当前分支
$ git branch
```

**预期输出**：
```
git branch
* feature-readme
  master
```

**说明**：
- `*` 现在在 feature-readme 分支上
- master 分支仍然存在

---

#### 第三步：在功能分支上修改文件（练习 `git add` 和 `git commit`）

**目标**：在功能分支上做一些修改并提交。

**操作**：
```bash
# 1. 在 README.md 文件末尾添加一行："Feature: 优化 README 格式"

# 2. 查看状态
$ git status

# 3. 添加到暂存区
$ git add README.md

# 4. 提交修改
$ git commit -m "feat: 优化 README 格式"
```

**预期输出**：
```
git status
On branch feature-readme
Changes not staged for commit:
  (use "git add <file>..." to update what will be committed)
  (use "git restore <file>..." to discard changes in working directory)
        modified:   README.md

no changes added to commit (use "git add" and/or "git commit -a")

git add README.md

git commit -m "feat: 优化 README 格式"
[feature-readme 3d3dc5e6] feat: 优化 README 格式
 1 file changed, 1 insertion(+)
```

---

#### 第四步：切换回主分支（练习 `git checkout`）

**目标**：切换回 master 分支，观察文件变化。

**操作**：
```bash
# 切换回 master 分支
$ git checkout master

# 查看 README.md 文件
# 你会发现刚才添加的那行文字不见了！
```

**预期输出**：
```
git checkout master
Switched to branch 'master'
Your branch is up to date with 'origin/master'.
```

**说明**：
- 切换回 master 后，刚才在 feature-readme 分支上的修改**不可见**
- 这就是分支的隔离性，不同分支互不影响

---

#### 第五步：再次切换并添加更多提交

**目标**：在功能分支上添加更多提交。

**操作**：
```bash
# 1. 切换回 feature-readme 分支
$ git checkout feature-readme

# 2. 再次修改 README.md，添加："Feature: 添加项目介绍"

# 3. 提交
$ git add README.md
$ git commit -m "feat: 添加项目介绍"

# 4. 查看提交历史
$ git log --oneline -3
```

**预期输出**：
```
git checkout feature-readme
Switched to branch 'feature-readme'

git add README.md

git commit -m "feat: 添加项目介绍"
[feature-readme 03c62bf9] feat: 添加项目介绍
 1 file changed, 2 insertions(+), 1 deletion(-)

git log --oneline -3
03c62bf9 (HEAD -> feature-readme) feat: 添加项目介绍
3d3dc5e6 feat: 优化 README 格式
0c09fcf1 (origin/master, origin/HEAD, master) 添加开发成员王乐宸
```

**说明**：
- feature-readme 分支现在比 master 分支多了 2 个提交
- master 分支还停留在 `0c09fcf`

---

#### 第六步：合并分支（练习 `git merge`）

**目标**：将 feature-readme 分支合并到 master 分支。

**操作**：
```bash
# 1. 切换回 master 分支
$ git checkout master

# 2. 合并 feature-readme 分支
$ git merge feature-readme

# 3. 查看提交历史
$ git log --oneline --graph -5
```

**预期输出**（无冲突）：
```
git checkout master
Switched to branch 'master'
Your branch is up to date with 'origin/master'.

git merge feature-readme
Updating 0c09fcf1..03c62bf9
Fast-forward
 README.md | 2 ++
 1 file changed, 2 insertions(+)

git log --oneline --graph -5
* 03c62bf9 (HEAD -> master, feature-readme) feat: 添加项目介绍
* 3d3dc5e6 feat: 优化 README 格式
* 0c09fcf1 (origin/master, origin/HEAD) 添加开发成员王乐宸
* 338b28ae docs: 将README中相对路径链接改为GitCode完整URL
* 4f890576 docs: 修正README中English Version链接的分支名为master
```

**说明**：
- `Fast-forward` 表示快速合并
- master 分支现在包含了 feature-readme 的所有提交
- 打开 README.md，你会看到刚才添加的两行内容都出现了

---

#### 第七步：删除功能分支（练习 `git branch -d`）

**目标**：功能分支的使命完成了，删除它。

**操作**：
```bash
# 删除已合并的功能分支
$ git branch -d feature-readme

# 查看剩余分支
$ git branch
```

**预期输出**：
```
git branch -d feature-readme
Deleted branch feature-readme (was 1234def).

git branch
* master
```

**说明**：
- feature-readme 分支已被删除
- 但合并后的提交仍然保留在 master 分支上
- 现在只剩下 master 分支

---

#### 第八步：创建冲突并解决（练习冲突解决）

**目标**：模拟并解决一个合并冲突。

**操作**：
```bash
# 1. 创建并切换到冲突测试分支
$ git checkout -b conflict-test

# 2. 修改 README.md 的第一行，改为："# AI Workshop 学生管理系统 - 冲突测试分支"

# 3. 提交
$ git add README.md
$ git commit -m "test: 在冲突测试分支修改标题"

# 4. 切换回 master
$ git checkout master

# 5. 在 master 上也修改 README.md 的第一行，改为："# AI Workshop 学生管理系统 - 主分支"

# 6. 提交
$ git add README.md
$ git commit -m "test: 在主分支修改标题"

# 7. 尝试合并（会产生冲突）
$ git merge conflict-test
```

**预期输出**（有冲突）：
```
git merge conflict-test
Auto-merging README.md
CONFLICT (content): Merge conflict in README.md
Automatic merge failed; fix conflicts and then commit the result.
```

**解决冲突**：
```bash
# 1. 查看冲突状态
$ git status

# 2. 打开 README.md，你会看到冲突标记
# <<<<<<< HEAD
# # AI Workshop 学生管理系统 - 主分支
# =======
# # AI Workshop 学生管理系统 - 冲突测试分支
# >>>>>>> conflict-test

# 3. 手动编辑，保留你想要的内容，删除冲突标记
# 例如保留："# AI Workshop 学生管理系统"

# 4. 标记冲突已解决
$ git add README.md

# 5. 完成合并
$ git commit -m "解决合并冲突，统一标题格式"
```

**预期输出**：
```
git add README.md

git commit -m "解决合并冲突，统一标题格式"
[master 5678abc] 解决合并冲突，统一标题格式
```

**查看合并历史**：
```bash
$ git log --oneline --graph -5
```

**预期输出**：
```
git log --oneline --graph -5
*   5678abc (HEAD -> master) 解决合并冲突，统一标题格式
|\
| * 2345def (conflict-test) test: 在冲突测试分支修改标题
* | 3456abc test: 在主分支修改标题
|/
* 1234def feat: 添加项目介绍
```

**说明**：
- `|` 和 `\` 显示了分支的分离和合并过程
- 冲突已解决，两个分支的修改被整合在一起

---

#### 第九步：清理测试分支

**目标**：删除测试用的冲突分支。

**操作**：
```bash
# 删除 conflict-test 分支
$ git branch -d conflict-test

# 查看最终状态
$ git branch
$ git log --oneline --graph -5
```

**预期输出**：
```
git branch -d conflict-test
Deleted branch conflict-test (was 2345def).

git branch
* master

git log --oneline --graph -5
*   5678abc (HEAD -> master) 解决合并冲突，统一标题格式
|\
| * 2345def test: 在冲突测试分支修改标题
* | 3456abc test: 在主分支修改标题
|/
* 1234def feat: 添加项目介绍
```

---

分支管理实践参考资料：
- [Git入门--分支管理--CSDN](https://bbs.csdn.net/topics/619739251)
- [Git 分支管理终极指南--CSDN](https://blog.csdn.net/2301_79248256/article/details/155818051)

---

## 6. 远程仓库 🌐

### 6.1 远程仓库配置

### 6.2 推送与拉取

### 6.3 分支同步

### 6.4 多人协作

---

## 7. 代码托管平台详解 📦

### 7.1 GitHub 使用指南

### 7.2 Gitee 使用指南

### 7.3 GitCode 使用指南

---

## 8. 高级特性 🚀

### 8.1 标签管理

### 8.2 储藏（Stash）

### 8.3 子模块

---

## 9. Git 工作流 🔄

### 9.1 集中式工作流

### 9.2 功能分支工作流

### 9.3 Git Flow

---

## 10. 常见问题与技巧 💡

### 10.1 常见问题

### 10.2 实用技巧

---

**最后更新时间：2026-04-25**
