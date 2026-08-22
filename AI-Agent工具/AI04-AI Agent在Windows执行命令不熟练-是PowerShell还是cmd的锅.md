# AI Agent 在 Windows 执行命令不熟练：是 PowerShell 还是 cmd 的锅？

> 本文剖析 Trae、Qoder、Cursor、Claude Code、Codex 等 AI Agent 在 Windows 上执行命令行频繁失败的现象，从训练数据 bias、shell 语法差异、shell 检测 bug 三个维度定位根因，并给出 Git Bash、WSL2、PowerShell 7+、cmd 的选择建议与实战配置

---

## 全文摘要

AI Agent 在 Windows 上执行命令不如 Linux 熟练，根因是训练数据 bias（bash 占绝对多数）叠加 shell 语法差异与 IDE 检测 bug，而非 PowerShell 或 cmd 本身更差。推荐给 AI 用 Git Bash 或 WSL2，PowerShell 7+ 次之，cmd 仅兜底。

---

## 1. 现象：AI Agent 在 Windows 上"不会"用命令行（Phenomenon）

同样的 AI Agent（Trae、Qoder、Cursor、Claude Code、Codex CLI），在 Linux 或 macOS 上执行命令行云流水——写脚本、跑构建、handle error 都很流畅；一旦切换到 Windows，就开始"抽风"：命令报错、路径找不到、命令卡死重试，甚至反复 oscillation（反复试探）。

**典型失败表现** 🔍：

1. **Linux 命令语法泄漏到 PowerShell**：AI 生成 `ls`、`rm -rf`、`$VAR`、heredoc、`&&` 等 bash 风格命令，PowerShell 要么不识别，要么行为完全不一致。例如 PowerShell 里 `&&` 在 7.0 之前根本不是合法运算符，`rm -rf` 会被解析成别的含义 🧨

2. **路径分隔符被"吃掉"**：AI 写出 Windows 自然路径 `C:\Users\vzssyd`，在 Git Bash 中 `\U`、`\v` 被当作 escape sequence 解释，路径被静默破坏；在 cmd 中反斜杠则可能被直接吞掉（`C:\Users\name` → `C:Usersname`），文件被创建到错误目录 🗂️

3. **命令"卡住"或假成功**：Cursor 论坛大量报告 Agent 执行后停留在 running 状态、`sleep` 命令在 cmd 中不生效（PowerShell 才有 `sleep`），以及 PowerShell 阻塞 `.ps1` 脚本（npm 的 `npm.ps1` wrapper 被 execution policy 拦截）⏳

4. **shell 检测 bug**：用户明明在 IDE 中设置了 Git Bash 或 cmd 为默认终端，Agent 却仍然用 PowerShell 执行，或错误地切到 WSL——Cursor 官方确认这是已知 bug，Agent 的 shell 检测不遵循 `terminal.integrated.defaultProfile.windows` 🐛

> 💡 **直观类比** 🎨：就像让一个只学过英语的人去写法语——不是人笨，而是训练素材里 90% 是英语。AI 在 Linux 上"如鱼得水"，是因为它训练时看的大多数命令示例都是 bash 写的。

**参考资料：**

- [The hidden variables in your agent eval -- Microsoft for Developers](https://developer.microsoft.com/blog/the-hidden-variables-in-your-agent-eval/) ⭐值得阅读
- [AI Agent (Claude 4) runs commands in PowerShell even when default terminal is Git Bash -- Cursor Forum](https://forum.cursor.com/t/ai-agent-claude-4-runs-commands-in-powershell-even-when-default-terminal-is-git-bash/137164)
- [Cursor AI Agent Shell Tool Hangs on All Commands (Windows) -- Cursor Forum](https://forum.cursor.com/t/cursor-ai-agent-shell-tool-hangs-on-all-commands-windows/162350)
- [Bash tool on Windows: silent command corruption -- GitHub opencode Issue](https://github.com/anomalyco/opencode/issues/15810)
- [windows-claude-code-doctor -- GitHub](https://github.com/iliamalkin/windows-claude-code-doctor) ⭐值得阅读

---

## 2. 根因分析：不是 PowerShell 的锅（Root Cause Analysis）

要回答"是 PowerShell 的原因还是 cmd 的原因"，先要拆清楚问题的本质。我把根因归结为四个层面，**没有任何一层是"某个 shell 本身做错了"**。

### 2.1 根因一：训练数据 bias（Training Data Bias）

这是最核心的根因。**大模型训练时接触的 shell 命令示例中，bash/Linux 占据了绝对多数**。Microsoft 官方博客直接点明：*"Models are trained on far more bash than PowerShell, and it shows——they write more fluent shell scripts, recover from errors more reliably, and chain commands more naturally when they believe they're in a Unix environment."*

也就是说：模型不是"不会"执行命令，而是"更擅长"它见过的语言。给它 PowerShell，就像让英语母语者用法语写代码——能写，但错误率高、语感差 🎯

### 2.2 根因二：语法差异巨大（Syntax Divergence）

bash / PowerShell / cmd 三者虽然都叫"命令行"，但语法体系几乎不互通：

| 语法项 | bash | PowerShell | cmd |
|--------|------|-----------|-----|
| 路径分隔符 | `/` | `\`（兼容 `/`） | `\` |
| 环境变量 | `$VAR` | `$env:VAR` | `%VAR%` |
| 命令拼接 | `&&`、`;` | `;`（7.0 起支持 `&&`） | `&&` |
| 管道 | 文本流 | 对象流 | 文本流 |
| 多行命令 | 支持 | 支持 | ❌ 第二行被吞 |
| 单引号 | 合法 | 合法 | ❌ 字面量 |
| 常用命令 | `ls` `rm` `cat` | `Get-ChildItem` `Remove-Item` | `dir` `del` `type` |

AI 生成的命令按 bash 思维编写，落到 PowerShell 或 cmd 上，会经历一次"translation cost"——每次执行都要现场翻译，翻译错了就报错重试。而 **cmd 由于功能最弱（无对象管道、无多行、无 `$VAR`），是三者中容错空间最小的**；PowerShell 至少语法表达能力强，只是与 bash 不兼容 🔄

### 2.3 根因三：shell 检测 bug（Shell Detection Bug）

即使你正确配置了默认终端，**IDE 的 Agent 执行路径仍可能绕过你的配置**：

- Cursor 的 `detectShellType()` 在 Windows 上有个著名的"死代码"问题——无论用户配置了什么，只要系统装了 PowerShell，就永远返回 `ShellType.PowerShell`
- Cursor Agent 不遵循 `terminal.integrated.defaultProfile.windows`，官方确认为已知 bug
- 部分场景下 Agent 还会错误地切到 WSL（`C:\Windows\System32\bash.exe` 是 WSL launcher，优先级高于 Git Bash）

这意味着：**你用的 shell 是谁，有时不由你决定，而由 IDE 的 bug 决定** 😤

### 2.4 根因四：PowerShell 5.1 与执行策略（Legacy PS 5.1 & Execution Policy）

Windows 自带的 **Windows PowerShell 5.1**（`powershell.exe`）相比 PowerShell 7+（`pwsh`）更老旧，且默认 execution policy 为 `Restricted`，会直接拦截 `.ps1` 脚本——npm 安装的 `npm.ps1` wrapper 就经常被拦，导致 `npm` 命令在 agent 环境里失效 ⛔

> 💡 **结论**：与其问"是 PowerShell 还是 cmd 的锅"，不如说——**是 shell 生态差异 + 训练数据 bias + IDE bug 的共同结果**。PowerShell 与 cmd 都是"受害者"，只是 cmd 能力太弱，在 AI 场景下"受害"更深。

**参考资料：**

- [The hidden variables in your agent eval -- Microsoft for Developers](https://developer.microsoft.com/blog/the-hidden-variables-in-your-agent-eval/) ⭐值得阅读
- [Windows Powershell's hardcoded Linux action Aliases are the sole reason for Agentic AI errors -- GitHub PowerShell Issue #26749](https://github.com/powershell/powershell/issues/26749)
- [Claude defaults to bash/Unix syntax on Windows instead of PowerShell -- GitHub Claude Code Issue #45831](https://github.com/anthropics/claude-code/issues/45831)
- [IDE Agent ignores terminal.integrated.defaultProfile.windows, always uses PowerShell -- Cursor Forum](https://forum.cursor.com/t/ide-agent-ignores-terminal-integrated-defaultprofile-windows-always-uses-powershell-even-with-nushell-bash-configured/151859)
- [Difference Between CMD vs PowerShell vs Bash -- AttuneOps](https://attuneops.io/difference-between-cmd-vs-powershell-vs-bash/)
- [CMD vs. PowerShell vs. Unix Shell：核心差异与哲学对比 -- CSDN](https://blog.csdn.net/YuYe_1990/article/details/154881124)

---

## 3. PowerShell vs cmd 深度对比（PowerShell vs cmd Comparison）

抛开 AI 场景，**PowerShell 与 cmd 根本不是一个时代的产物**：cmd 诞生于 1987 年，本质是 DOS 命令的延续，定位"能跑就行"；PowerShell 诞生于 2006 年，是一个完整的对象化脚本语言，定位"自动化一切"。

| 对比维度 | cmd | PowerShell | 说明 |
|---------|-----|-----------|------|
| 输出模型 | 纯文本 | **对象流** | PowerShell 管道传递对象，`ls \| Where-Object` 可精确过滤 |
| 脚本能力 | 极弱（批处理） | **完整脚本语言** | 支持函数、类、异常处理、模块 |
| 命令生态 | 少量内置 + 外部 exe | **数千 cmdlet** | `Get-Process`、`Get-Service` 等开箱即用 |
| 变量 | `%VAR%` | `$var` + 强类型 | cmd 变量是字符串替换，PowerShell 是真实变量 |
| 错误处理 | ❌ 无 | `try/catch` | AI 生成 PowerShell 代码可依赖结构化错误 |
| 启动速度 | 快 ⚡ | 慢（约 1-2s） | cmd 轻量是它唯一显著优势 |
| AI 友好度 | 低 | **中** | 语法能力强但"翻译成本"仍在 |

**为什么说 PowerShell 远强于 cmd？** 🤔

1. **对象管道 vs 文本管道**：cmd 的 `dir | find "xxx"` 只能做文本匹配；PowerShell 的 `Get-ChildItem | Where-Object { $_.Length -gt 1MB }` 直接按属性过滤。对 AI Agent 而言，对象化输出更可预测、更少歧义 🎯

2. **脚本是"代码"**：PowerShell 支持函数、循环、异常处理，AI 可以像写 Python 一样写 `.ps1` 脚本；cmd 批处理只能逐行堆命令，AI 生成复杂逻辑时几乎必然出错 📜

3. **与 bash 的兼容面更大**：PowerShell 7+ 内置 `&&`、支持 `/` 路径、别名了 `ls`、`cat` 等常见命令（虽然行为不完全一致），容错空间比 cmd 大得多——cmd 连单引号都当成字面量，多行命令第二行直接消失，AI 生成的命令在这里几乎"寸步难行" 🧩

**那 cmd 什么时候有用？** ✅

- 需要极快启动的轻量脚本、旧批处理兼容
- 作为"最坏情况兜底"——如果 agent 在 PowerShell 上反复失败，切到 cmd 有时能绕过 PowerShell 的 execution policy 与 `.ps1` 阻塞问题（Cursor 官方就建议过这种 workaround）

> 💡 **核心结论**：PowerShell 是"现代但不同语言"，cmd 是"古老且简陋"。**两者都是 bash 的"异乡人"，只是 PowerShell 更像"通晓两种语言的移民"，cmd 更像"只会方言的老人"** 🌍

**参考资料：**

- [PowerShell vs CMD: Key Differences, Use Cases -- Netwrix](https://netwrix.com/en/resources/blog/powershell-vs-cmd/)
- [Difference Between CMD vs PowerShell vs Bash -- AttuneOps](https://attuneops.io/difference-between-cmd-vs-powershell-vs-bash/)
- [What is the difference between Cmd, PowerShell, and Bash? -- YouTube](https://www.youtube.com/watch?v=nahtw_csB5w)
- [CMD、PowerShell和Shell三种命令行比较 -- 知乎](https://zhuanlan.zhihu.com/p/692057908)

---

## 4. 推荐方案：到底选哪个（Recommendation）

基于上面的根因分析，结论很清晰：**给 AI Agent 一个 bash 兼容环境，比纠结 PowerShell 还是 cmd 更重要**。因为 AI 的"母语"是 bash，让它说母语，错误率自然下降 🗣️

> 💡 **我最推荐的方案**：Windows 本地项目场景下，**我最推荐 Git Bash**——它同时满足「bash 语法」与「Windows 工具链可用」两个条件，是绝大多数 Windows 开发者的最佳起点。如果你重度依赖 Linux 工具链（Docker、gcc、apt），则我最推荐 WSL2。

### 4.1 首选：Git Bash（Git for Windows）

**适用场景**：项目在 Windows 本地、依赖 Windows 工具链（`mvn`、`node`、`java` 装在 Windows）、不想引入 WSL 的复杂度。

- 提供完整的 bash 语法，AI 生成的命令几乎零翻译成本
- **Cursor、Qoder 官方明确支持**；Claude Code 官方推荐安装（无 Git Bash 时才退回 PowerShell tool）
- 安装即用：安装 [Git for Windows](https://git-scm.com/downloads/win) 后自带 Git Bash

### 4.2 进阶：WSL2（Windows Subsystem for Linux）

**适用场景**：项目依赖 Linux 工具链（`apt`、`gcc`、Docker）、或追求与 macOS/Linux 开发体验完全一致。

- 真正的 Linux 内核环境，Claude Code 官方视其为 **Windows 上最安全的运行方式**，社区资源最丰富
- 命令在 WSL 内执行，AI 完全按照 Linux 思维工作
- 注意：Windows 与 WSL 之间跨文件系统 I/O 较慢，项目应放在 WSL 文件系统内（`~/`），避免 `/mnt/c/` 目录

### 4.3 次选：PowerShell 7+（pwsh）

**适用场景**：必须使用 PowerShell 的场景（公司策略、Windows 管理自动化、依赖 PowerShell cmdlet）。

- **务必升级到 PowerShell 7+（pwsh）**，不要用自带的 Windows PowerShell 5.1——7+ 支持 `&&`、`/` 路径、兼容性更好
- Qoder 官方要求 Windows 下使用 PowerShell 时必须为 7 或更高版本
- 可以设置 `Set-ExecutionPolicy RemoteSigned -Scope CurrentUser` 解除 `.ps1` 拦截
- Claude Code 也提供了 `CLAUDE_CODE_USE_POWERSHELL_TOOL=1` 让命令走 PowerShell 通道（解决 Git Bash 路径/引号问题）

### 4.4 尽量避免：cmd

**cmd 是三者中容错空间最小的**：无对象管道、无 `$VAR`、单引号字面量、多行命令被截断。只有当 agent 在 PowerShell 上反复失败、需要绕过 execution policy 时才临时切到 cmd 兜底。

### 4.5 决策表（Decision Matrix）

| 你的场景 | 推荐 shell | 原因 |
|---------|-----------|------|
| Windows 本地项目 + Windows 工具链 | **Git Bash** | bash 语法 + Windows PATH 可用，Cursor/Qoder 官方支持 |
| Linux 工具链 / Docker / 追求一致体验 | **WSL2** | 完整 Linux 环境，AI 零翻译成本 |
| 必须用 PowerShell（公司策略等） | **PowerShell 7+** | 语法能力强，7+ 修复大量兼容问题 |
| 老脚本兼容 / 极轻量任务 | cmd | 快速启动，仅兜底 |
| 日常开发（人用） | PowerShell 7+ | 比 cmd 强大太多，人操作无翻译成本 |

> 💡 **一句话总结**：**人用 PowerShell，AI 用 bash（Git Bash 或 WSL）** —— 人和 AI 各说各的母语，冲突最少 🏆

> 🏅 **我的最终推荐**：如果只能选一个，**我最推荐 Git Bash**——安装成本低、与 Windows 工具链兼容性好，是让 AI Agent 在 Windows 上执行命令最省心的方案。

**参考资料：**

- [Complete Guide to Setting Up Claude Code on Windows and Avoiding Common Pitfalls -- AI Dev Tools Blog](https://devtools.shingoirie.com/blog/en/claude-code-windows-setup-guide/) ⭐值得阅读
- [Getting started with Claude Code -- Claude Code Docs](https://code.claude.com/docs/en/getting-started)
- [Terminal Execution Exceptions -- Qoder Docs](https://docs.qoder.com/troubleshooting/terminal-execution-exceptions)
- [How to Set Up Claude Code on Windows Using WSL -- lowtouch.ai](https://www.lowtouch.ai/claude-code-windows-wsl-setup-guide/)
- [Troubleshoot installation and login -- Claude Code Docs](https://code.claude.com/docs/en/troubleshoot-install)

---

## 5. 实战配置：让 AI Agent 更听话（Practical Configuration）

选定方案后，还需要四步配置才能真正生效。⚠️ 注意：**Agent 的执行 shell 可能不遵循 IDE 的终端默认配置**（前面提到的 shell 检测 bug），所以要多管齐下。

### 5.1 设置 IDE 默认终端为 Git Bash（VS Code / Cursor）

打开 `settings.json`，将默认 profile 指向 Git Bash，并禁用 WSL profile 自动检测（防止 Agent 错误地切到 WSL）：

```json
{
  "terminal.integrated.useWslProfiles": false,
  "terminal.integrated.defaultProfile.windows": "Git Bash",
  "terminal.integrated.profiles.windows": {
    "Git Bash": {
      "path": "C:\\Program Files\\Git\\bin\\bash.exe",
      "args": []
    },
    "PowerShell": null,
    "Command Prompt": null,
    "Ubuntu (WSL)": null
  }
}
```

修改后**完全重启 IDE**（quit 而不是 Reload Window）。验证方法：在终端执行 `echo $SHELL`，返回 `/usr/bin/bash` 或 `MINGW64` 说明生效。

### 5.2 用提示词规则约束 Agent 的 shell 语法（AGENTS.md / .cursor/rules）

IDE 的 shell 检测 bug 可能让配置失效，这时可以在项目的 `AGENTS.md`、`CLAUDE.md` 或 `.cursor/rules` 中强制注入 shell 规则，**让 Agent 按规则说话而不是按直觉说话**：

```markdown
## Shell Execution Rules (Windows)

1. 路径一律使用正斜杠：`C:/Users/name/project`，禁止反斜杠
2. 路径含空格时必须加引号：`ls "C:/Program Files/"`
3. 涉及文件操作优先使用 IDE 内置工具（Read/Write/Edit/Glob/Grep），绕过 shell
```

> 原理：Agent 在会话开始时读取环境平台信息并应用规则，可以绕过 `detectShellType()` 的死代码问题（Cursor 官方推荐的临时 workaround 就是 `.cursor/rules`）。

### 5.3 为 Agent 工具指定 bash 路径（Claude Code / Qoder）

- **Claude Code**：官方推荐安装 Git for Windows；若找不到 Git Bash，可在 `settings.json` 显式指定：

```json
{
  "env": {
    "CLAUDE_CODE_GIT_BASH_PATH": "C:\\Program Files\\Git\\bin\\bash.exe"
  }
}
```

- **Qoder**：官方文档明确 Windows 支持 `Git Bash` 和 `pwsh`，且 PowerShell 必须为 7+。在 Qoder 设置中选择支持的 shell 即可。

### 5.4 解除 PowerShell 执行策略（若必须用 PowerShell）

```powershell
# 允许本地 .ps1 脚本运行（当前用户级），解决 npm.ps1 被拦问题
Set-ExecutionPolicy RemoteSigned -Scope CurrentUser
```

**参考资料：**

- [Agent command execution uses WSL instead of the Windows default integrated terminal -- Cursor Forum](https://forum.cursor.com/t/agent-command-execution-uses-wsl-instead-of-the-windows-default-integrated-terminal-git-bash/160196) ⭐值得阅读
- [Bash tool on Windows: silent command corruption（Prompt-Level Shell Rules 部分）-- GitHub opencode Issue](https://github.com/anomalyco/opencode/issues/15810)
- [Terminal Execution Exceptions -- Qoder Docs](https://docs.qoder.com/troubleshooting/terminal-execution-exceptions)
- [Terminal Profiles -- VS Code Docs](https://code.visualstudio.com/docs/terminal/profiles)
- [Getting started with Claude Code -- Claude Code Docs](https://code.claude.com/docs/en/getting-started)

---

## 6. Git Bash 安装与配置全指南（Git Bash Installation & Configuration）

前几章给了结论，这一章落地：怎么把 Git Bash 装好、让 AI Agent 真正调用它、以及提示词里到底要不要写 shell 规则。

### 6.1 安装 Git for Windows（Git Bash 随附）

推荐用 winget 一行命令安装（已安装则跳过）：

```powershell
# 用 Windows 包管理器安装 Git for Windows（自带 Git Bash）
winget install --id Git.Git -e --source winget
```

也可以访问 [git-scm.com/downloads/win](https://git-scm.com/downloads/win) 下载安装器。安装过程中的三个关键选项：

| 安装选项 | 推荐选择 | 原因 |
|---------|---------|------|
| PATH 配置 | **Git from the command line and also from 3rd-party software** | 让 Claude Code 等第三方程序能自动找到 git 与 bash |
| 默认编辑器 | VS Code | `git commit` 时打开熟悉的编辑器 |
| 换行符处理 | 默认（Checkout Windows-style, commit Unix-style） | 团队协作兼容性最好 |

安装后验证：

```bash
bash --version      # 应输出 GNU bash, version 5.x（x86_64-pc-msys）
where.exe bash      # 应指向 C:\Program Files\Git\bin\bash.exe
```

### 6.2 两个 bash.exe，别搞混

Git for Windows 装了**两个** bash 入口，用途完全不同：

| 可执行文件 | 位置 | 用途 |
|-----------|------|------|
| `bash.exe` | `C:\Program Files\Git\bin\bash.exe` | 纯 shell，**AI Agent 调用它** |
| `git-bash.exe` | `C:\Program Files\Git\git-bash.exe` | 终端模拟器 wrapper，**人打开窗口用** |

配置 AI Agent 时，一律指向 `bash.exe`（VS Code profile、Claude Code 的 `CLAUDE_CODE_GIT_BASH_PATH`、各 agent 的 shellPath 都认它）；`git-bash.exe` 只是给人类双击打开用的，AI 不认。

> ⚠️ 注意：`C:\Windows\System32\bash.exe` 是 **WSL launcher**，不是 Git Bash。若 IDE 误用了它，Agent 会跑进 WSL——所以 5.1 里要 `useWslProfiles: false`。

### 6.3 各工具接入 Git Bash 速查表

| 工具 | 配置方式 | 关键配置 |
|------|---------|---------|
| VS Code / Cursor / **Trae** | settings.json 默认 profile（详见 5.1） | `terminal.integrated.defaultProfile.windows: "Git Bash"` |
| Claude Code | 自动检测，失败时显式指定（详见 5.3） | `CLAUDE_CODE_GIT_BASH_PATH=C:\Program Files\Git\bin\bash.exe` |
| Qoder | 设置中选择 Git Bash | 官方支持 Git Bash 与 pwsh |
| Pi 等 CLI agent | 全局 settings.json 的 `shellPath` | `"shellPath": "C:\\Program Files\\Git\\bin\\bash.exe"` |

Trae 与 VS Code 同内核，配置路径完全一致：`设置 → 搜索 terminal.integrated.defaultProfile.windows → 选择 Git Bash`，或直接编辑 settings.json。

### 6.4 提示词里要不要写 shell 规则？——要写

答案是 **要写**。原因很直接：IDE 的 shell 检测 bug 无法靠设置彻底消除（见 2.3），而提示词规则是 Agent 每次会话开始必读的"环境说明书"，是唯一绕不过的通道（5.2 讲了机制，这里讲选型与写法）。

2026 年主流的规则文件有三种，**互不冲突，推荐组合使用**：

| 文件 | 谁读 | 定位 |
|------|------|------|
| `AGENTS.md`（项目根目录） | Codex、Cursor、Copilot、Gemini CLI、Aider、Zed 等 20+ 工具 | **open standard**，2026 年事实标准，首选 |
| `CLAUDE.md`（项目根目录） | Claude Code 专用 | 三层 memory 模型，仅 Claude 认 |
| `.cursor/rules/*.mdc` | Cursor 专用 | YAML frontmatter + globs 按文件生效 |

**推荐策略**：根目录放一份 `AGENTS.md` 作为唯一事实源（所有工具都读），Claude Code 用户再放一份精简的 `CLAUDE.md` 指向它；不要让多个文件各自为政。

**shell 规则的具体写法**——要明确告诉 Agent 三件事：① 你运行在 Windows 的 Git Bash 环境；② 用 bash 语法写命令；③ 路径与引号的约定。示例：

```markdown
# AGENTS.md（节选）

## Shell & Command Rules (Windows)

IMPORTANT: You are running on Windows with Git Bash as the shell.

1. YOU MUST write shell commands in bash syntax, NOT PowerShell syntax.
   - ❌ `$env:VAR`        →  ✅ `$VAR`
   - ❌ `Get-ChildItem`   →  ✅ `ls`
   - ❌ `;` 拼接命令       →  ✅ `&&` 拼接
2. ALWAYS use forward slashes in paths: `C:/Users/name/project`.
3. Quote paths containing spaces: `ls "C:/Program Files/"`.
4. NEVER use backslashes in shell commands (escape sequences break paths).
5. Prefer IDE built-in file tools (Read/Write/Edit) over shell for file operations.
6. When a command fails, read the error and adjust syntax to bash, do NOT blindly retry.
```

写作要点（Claude 官方建议）：**直接命令式（direct imperative）+ 强调标记**——`IMPORTANT`、`YOU MUST`、`NEVER` 能显著提高遵守率；每条规则一行、正反例对照；文件控制在 200 行以内，超出就拆子文件。

**参考资料：**

- [AGENTS.md 规范 -- agents.md](https://agents.md/) ⭐值得阅读
- [AGENTS.md vs CLAUDE.md vs Cursor Rules: 2026 Guide -- Codersera](https://codersera.com/blog/agents-md-vs-claude-md-vs-cursor-rules-comparison-2026/) ⭐值得阅读
- [Set up on Windows -- Claude Code Docs](https://code.claude.com/docs/en/setup)
- [Environment variables -- Claude Code Docs](https://code.claude.com/docs/en/env-vars)
- [Claude Code Installation Guide for Windows -- dev.to](https://dev.to/xujfcn/claude-code-installation-guide-for-windows-git-path-environment-variables-powershell-wsl-and-1lag)
- [Windows Setup -- Pi Docs（GitHub）](https://github.com/earendil-works/pi/blob/main/packages/coding-agent/docs/windows.md)
- [Windows Setup Guide -- PairCoder Docs](https://paircoder.ai/docs/guides/windows-setup/)
- [Terminal Profiles -- VS Code Docs](https://code.visualstudio.com/docs/terminal/profiles)

---

## 7. 总结（Summary）

回到最初的问题：**"大模型在 Windows 上不能像 Linux 那样熟练使用命令行，是 PowerShell 的原因还是 cmd 的原因？"** —— 答案是：**都不是，也都有份**。根因在于 bash 生态的绝对主导 + 训练数据 bias + IDE shell 检测 bug，PowerShell 与 cmd 只是"替罪羊"。

**核心要点回顾** 🎯：

| 问题 | 答案 |
|------|------|
| 为什么 AI 在 Linux 上更熟练？ | 训练数据中 bash 占绝对多数，模型"母语"是 bash |
| 是 PowerShell 还是 cmd 的锅？ | 都不是根因；cmd 能力最弱，PowerShell 是"不同语言"而非"更差" |
| PowerShell vs cmd 怎么选？ | 人用选 **PowerShell 7+**；cmd 仅兜底 |
| 给 AI Agent 用什么 shell？ | 首选 **Git Bash**（本地项目）或 **WSL2**（Linux 工具链） |
| 配置了还不生效？ | 是 shell 检测 bug，用 AGENTS.md / .cursor/rules 注入 shell 规则绕过 |

🔴 **关键理解**：

- 💡 **训练数据 bias 是根因**——这不是任何 shell 的"错"，而是模型能力分布的现实
- ⚡ **bash 兼容环境 > 纠结 PowerShell/cmd**——让 AI 说母语，错误率自然下降
- 🛠️ **多管齐下配置**——IDE 默认终端 + 提示词规则 + 显式 bash 路径，才能对抗 shell 检测 bug

---

**最后更新时间**：2026-08-07
