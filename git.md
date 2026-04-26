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

### 4.1 仓库初始化

> **创建新仓库**：
> 
> ```bash
> # 在当前目录初始化 Git 仓库
> git init
> 
> # 创建新目录并初始化
> git init my-project
> ```
> 
> 执行后会在目录下生成 `.git` 隐藏文件夹，这就是 Git 的版本库。

> **克隆远程仓库**：
> 
> ```bash
> # 克隆 Gitee 上的项目到本地
> git clone https://gitee.com/username/repo.git
> 
> # 克隆时指定本地文件夹名
> git clone https://gitee.com/username/repo.git my-folder
> ```
> 
> 💡 **推荐新手尝试的知名项目**：
> 
> | 项目 | 地址 | 特点 |
> |:-----|:-----|:-----|
> | **Web-Development 迷你项目** | `https://gitcode.com/gh_mirrors/webde/Web-Development` | HTML/CSS 实战教程，克隆即用 |
> | **樱花个人引导页** | `https://gitee.com/suinian_Nian/Personal_Sakura_Guide_Page` | 纯前端，双击 `index.html` 即可运行 |
> 
> 这些项目都是**纯前端项目**，克隆后双击 HTML 文件就能在浏览器打开，非常适合新手练习！

### 4.2 基本工作流程（add/commit）

> Git 工作区有三个概念：
> 
> | 区域 | 说明 | 对应命令 |
> |:-----|:-----|:---------|
> | **工作区** | 你看到的实际文件 | 直接编辑文件 |
> | **暂存区** | 准备提交的修改 | `git add` |
> | **本地仓库** | 提交后的版本历史 | `git commit` |

> **添加文件到暂存区**：
> 
> ```bash
> # 添加单个文件
> git add filename.txt
> 
> # 添加所有修改
> git add .
> 
> # 添加所有 .py 文件
> git add *.py
> ```

> **提交到本地仓库**：
> 
> ```bash
> # 提交并写说明（必须加 -m）
> git commit -m "完成了登录功能"
> 
> # 添加并提交（合并 add 和 commit）
> git commit -am "修复了样式bug"
> ```

### 4.3 查看状态与历史

> **查看当前状态**：
> 
> ```bash
> # 查看哪些文件被修改、哪些在暂存区
> git status
> ```

> **查看提交历史**：
> 
> ```bash
> # 查看完整历史
> git log
> 
> # 简洁显示（一行一个提交）
> git log --oneline
> 
> # 查看最近3条
> git log -3
> 
> # 图形化显示分支
> git log --oneline --graph
> ```

> **查看文件差异**：
> 
> ```bash
> # 查看工作区与暂存区的差异
> git diff
> 
> # 查看暂存区与上次提交的差异
> git diff --cached
> ```

### 4.4 撤销与回退

> **撤销工作区的修改**（未 add）：
> 
> ```bash
> # 撤销单个文件的修改
> git checkout -- filename.txt
> 
> # 撤销所有修改
> git checkout -- .
> ```

> **撤销暂存区的文件**（已 add 未 commit）：
> 
> ```bash
> # 把文件从暂存区移回工作区
> git reset HEAD filename.txt
> ```

> **回退到历史版本**：
> 
> ```bash
> # 查看提交历史，找到 commit id
> git log --oneline
> 
> # 软回退（保留修改，回到暂存区）
> git reset --soft HEAD~1
> 
> # 硬回退（丢弃修改，彻底回到上一版本）
> git reset --hard HEAD~1
> 
> # 回退到指定版本
> git reset --hard abc1234
> ```

> ⚠️ **注意**：`--hard` 会永久删除未提交的修改，使用前请确认！

Git 基础操作参考资料：
- [Git 从入门到封神--CSDN](https://blog.csdn.net/2301_81028896/article/details/157034702)
- [Git教程(入门)--腾讯云](https://developer.cloud.tencent.com/article/2622894)
- [Revert and undo changes--GitLab Docs](https://docs.gitlab.com/ee/topics/git/undo.html)

---

## 4. 分支管理 🌿

### 4.1 分支基础

### 4.2 分支合并

### 4.3 分支策略

### 4.4 冲突解决

---

## 5. 远程仓库 🌐

### 5.1 远程仓库配置

### 5.2 推送与拉取

### 5.3 分支同步

### 5.4 多人协作

---

## 6. 代码托管平台详解 📦

### 6.1 GitHub

### 6.2 Gitee（码云）

### 6.3 GitCode

### 6.4 GitLab

---

## 7. 高级特性 🚀

### 7.1 标签管理

### 7.2 储藏与清理

### 7.3 变基操作

### 7.4 子模块

---

## 8. Git 工作流 🔄

### 8.1 集中式工作流

### 8.2 功能分支工作流

### 8.3 Git Flow 工作流

### 8.4 Forking 工作流

---

## 9. 常见问题与技巧 💡

### 9.1 常见错误处理

### 9.2 实用技巧

### 9.3 最佳实践

---

**最后更新时间：2026-04-25**
