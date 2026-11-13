# Trae 的 .trae 目录到底怎么用：rules、commands、skills 三层机制与一棵典型目录树的落地拆解

> **核心结论**：`.trae` 不是「把一堆 md 扔进去就会生效」的杂物箱，它只有三层真正干活的东西。**rules 决定 AI 每次都要遵守什么**，按 `alwaysApply` 常驻或按需；**commands 决定你用什么入口触发**，只做调度；**skills 决定具体怎么做**，触发时才加载全文。下文这棵示例树：3 份 rules 里 1 份常驻、2 份按需；3 个 command；4 个 skill 目录里 3 个带 `SKILL.md`、1 个只放脚本。分层清楚，规则才不会互相挤占上下文。

---

## 目录

- 1. 三层分工：谁是常驻、谁按需加载
- 2. 一棵典型的 .trae 目录树
- 3. Rules 层：alwaysApply 决定注入方式
- 4. Commands 层：斜杠命令只是入口
- 5. Skills 层：渐进式披露与脚本资源目录
- 6. specs、sessions、handover：三种记忆别混用
- 7. mcp.json：外部能力的接线板
- 8. 对照表：症状 → 原因 → 解法
- 9. 该用 / 不该用的判据

---

## 1. 三层分工：谁是常驻、谁按需加载（Three-Layer Split）

先建立一个直觉 🎭：`.trae` 就像一家店的三种印刷品。**rules 是贴在墙上的店规**，进门就看得到，谁都得遵守；**commands 是菜单上的套餐按钮**，你点哪个出哪个；**skills 是后厨的操作手册**，只有点了那道菜，厨师才去翻对应那页。把后厨手册也贴到墙上，墙就废了——这正是很多人 `.trae` 不好用的原因。

| 层 | 文件位置 | 何时进上下文 | 你往里写什么 |
|---|---|---|---|
| rules（规则） | `.trae/rules/*.md` | 由 `alwaysApply` 决定：常驻或按需 | 约束、铁律、禁止项、风格约定 |
| commands（命令） | `.trae/commands/*.md` | 你打 `/命令` 时 | 触发入口 + 流程骨架 |
| skills（技能） | `.trae/skills/*/SKILL.md` | 任务自动匹配，或被 command 显式引用 | 完整 SOP、问题库、可执行脚本 |

三层的差别不在「文件放哪」，而在**上下文成本**：rules 常驻意味着每一轮对话都为它付费；skill 按需意味着平时只付一行摘要的钱。所以判断一条内容放哪层，只看一句话——**它是不是每次对话都必须在场**。

---

## 2. 一棵典型的 .trae 目录树（Directory Tree）

下面这棵树是一个典型项目的 `.trae` 结构，文件名与数量都可以按你的项目替换：

```text
.trae/
├── rules/                                # 3 个：约束注入层
│   ├── project-conventions.md            # alwaysApply: true   编码与目录约定，常驻
│   ├── api-design.md                     # alwaysApply: false  改接口时才读
│   └── release-checklist.md              # alwaysApply: false  发版时才读
├── commands/                             # 3 个：斜杠入口，只做调度
│   ├── new-feature.md                    # /new-feature   开新功能的流程骨架
│   ├── code-review.md                    # /code-review   派发给三个检查 skill
│   └── release.md                        # /release       构建、变更日志、上线
├── skills/                               # 4 个目录：能力层
│   ├── security-scan/SKILL.md            # 依赖漏洞与密钥泄露检查
│   ├── test-coverage/SKILL.md            # 覆盖率缺口定位
│   ├── docs-check/SKILL.md               # 代码与文档一致性校对
│   └── card-renderer/                    # 无 SKILL.md，只放 render_card.py
├── specs/add-export-api/                 # spec.md + checklist.md + tasks.md
├── sessions/                             # 会话日志，文件名精确到分钟
├── mcp.json                              # MCP server 配置
└── handover.md                           # 跨会话交接单
```

一个容易忽略的细节：`skills/card-renderer/` 里没有 `SKILL.md`，只有一个 `render_card.py`。这说明 skill 目录不一定非得是「一份说明书」，它也可以是**某个流程专用的脚本仓库**，由真正执行渲染的 skill 在正文里引用——AI 平时看不到这个脚本，只有执行到渲染那一步才去取。

---

## 3. Rules 层：alwaysApply 决定注入方式（Rule Injection）

规则文件顶部的 front-matter 就是一个开关：

```yaml
---
alwaysApply: true
description: 项目编码与目录约定，规定命名、分层与提交信息格式
---
```

- `alwaysApply: true` → **全文注入**。本轮对话里，这类规则的完整正文会直接出现在模型上下文中。
- `alwaysApply: false` → **只挂一行 `description`**。AI 知道「有这么一份规范」，需要时再自己读取全文。

把注入方式算成数字就很直观。假设你的规则目录和示例一样是 3 份：`project-conventions.md` 12000 字符、`api-design.md` 4500 字符、`release-checklist.md` 3500 字符。三份全设 `true`，合计 **20000 字符**全文进上下文；只把第一份设 `true`，常驻降到 12000 字符，另两份只在清单里出现名字和描述，正文一个字都没进来。

自己量一遍（在仓库根目录执行）：

```bash
wc -m .trae/rules/*.md
```

输出里每个数字就是该文件的字符数，加总即本轮固定成本。

这个数字值得警惕 ⚠️：上万字符的常驻内容，意味着**每一轮对话都要先为它付一次费用**。如果你把 `release-checklist.md` 里那二十条发版检查塞进 `project-conventions.md`，那它每一轮都在白占位置。判断标准很简单——**去掉它会不会导致 AI 本轮做错事**，会才给 `true`。

---

## 4. Commands 层：斜杠命令只是入口（Command as Entry）

command 文件的 front-matter 只有两个字段，但两个都不能少：

```yaml
---
name: "code-review"
description: "提交前自查：安全、测试覆盖率、文档一致性三项检查"
---
```

`name` 是你在命令面板里看到的名字，`description` 决定 AI 什么场景该用它。正文才是流程骨架。

示例里的 `code-review.md` 就是个好样板：它开头就写明「**本 command 只做调度**，不内联任何检查规则」，然后把安全、覆盖率、文档三块细节全部指向对应 skill：

| 检查项 | 对应子 skill | 路径 |
|---|---|---|
| 安全扫描 | `security-scan` | `.trae/skills/security-scan/SKILL.md` |
| 测试覆盖率 | `test-coverage` | `.trae/skills/test-coverage/SKILL.md` |
| 文档一致性 | `docs-check` | `.trae/skills/docs-check/SKILL.md` |

这样做的好处很实在：命令本身的常驻成本极低（只有几行调度逻辑），三块检查的几百行细节全部沉到 skill 里，**跑哪一项才读哪一份**。代价是多一次文件读取——但这次读取只在真正执行时才发生，比每轮都背着三份检查手册便宜得多。

反过来说，如果一个 command 里内联了所有分支流程，它就退化成一份「巨型规则」：你以为它只是入口，实际上它每轮都在烧上下文。

---

## 5. Skills 层：渐进式披露与脚本资源目录（Progressive Disclosure）

skill 的加载分两级，这是它便宜的根本原因：

| 层级 | 何时加载 | 成本量级 | 内容 |
|---|---|---|---|
| 一级：元数据 | 会话启动即加载 | 约 100 token / 个 | `name` + `description` |
| 二级：正文 | 技能被触发时 | 数千 token | `SKILL.md` 全文 |
| 附：资源 | 执行需要时 | 不设限 | 同目录脚本、模板、数据 |

所以写 `description` 是 skill 里**性价比最高的一件事**：它是唯一常驻的部分，必须写清「**什么时候该用我**」，而不是「我是什么」。示例里 `docs-check` 的描述就是触发式写法——「当用户说『检查文档 / 校对文档 / 交付前过一遍 / docs check』时触发」，把口语变体全列进去，命中率自然高。

还有一条硬规则容易被忽略：**`name` 必须等于目录名**。这是「写了但没接上」的典型——名字对不上时，skill 列表里显示的名字和磁盘目录两套叫法，后续引用就会指向不存在的路径。

---

## 6. specs、sessions、handover：三种记忆别混用（Three Kinds of Memory）

这三样东西长得都像「文档」，但记录的内容完全不同：

| 位置 | 记什么 | 生命周期 |
|---|---|---|
| `specs/<feature>/` | 一次功能改造的 why / what / 场景 / 任务清单 | 改造完成即冻结，不参与运行时 |
| `sessions/YYYY-MM-DD-HHmm.md` | 本轮做了什么、跑了哪些命令、改了哪些文件、踩了什么坑 | 按分钟追加，只增不改 |
| `handover.md` | 跨会话交接：当前进展、卡在哪、下一步干什么 | 单文件滚动覆盖 |

一句话区分：**specs 写「要做什么」，sessions 写「做了什么」，handover 写「接下来做什么」**。三者混用的典型后果是——你想查「这段逻辑上个月为什么这么改」，结果翻到的全是最新那张交接单，历史早被覆盖了。

示例里的 `specs/add-export-api/` 就是标准三件套：`spec.md` 讲需求与场景，`checklist.md` 做验收打勾，`tasks.md` 拆执行步骤。这套结构适合「改一次就归档」的功能级改造，不适合日常流水账。

---

## 7. mcp.json：外部能力的接线板（MCP Wiring）

`mcp.json` 只有一件事：告诉 IDE 有哪些 MCP server、怎么连。它支持两种典型形态：

```json
{
  "mcpServers": {
    "远程检索": {
      "url": "https://<host>/mcp",
      "headers": { "X-Agent-Plan-Key": "${MCP_PLAN_KEY}" }
    },
    "本地检索": {
      "command": "uvx",
      "args": ["--from", "git+https://github.com/<org>/<repo>#subdirectory=<path>", "<entry>"],
      "env": { "API_KEY": "${MCP_API_KEY}" }
    }
  }
}
```

- `url` 型：连远端 HTTP 服务，通常要带鉴权 header。
- `command` 型：本地拉起进程（示例用 `uvx` 直接从 git 仓库装包），靠 `env` 传 key。

⚠️ 一个必须点明的安全边界：把 key **明文硬编码**在 `mcp.json` 里、再随配置提交进团队仓库，是这类文件最常见的坑。一旦进了公开仓库，key 就等于公开了——正确写法是像上面示例那样用 `${ENV_VAR}` 占位，把真值放进本地环境变量或 `.env`（并确认 `.env` 已在 `.gitignore` 里）。这不是风格问题，是凭据泄露问题。

---

## 8. 对照表：症状 → 原因 → 解法（Symptom Table）

| 症状 | 原因 | 解法 |
|---|---|---|
| 规则写了一大堆，AI 却总漏掉某几条 | 所有规则都设 `alwaysApply: true`，后面的被长上下文稀释 | 只把「每轮都必须遵守」的留 `true`，其余改 `false` + 写清 `description` |
| 自定义命令打了没反应 | command 的 front-matter 缺 `name` 或 `description` | 补齐两个字段，`name` 用中文短名，`description` 写触发场景 |
| skill 明明存在，AI 却想不起来用 | `description` 写成了「我是干什么的」，没写「什么时候用」 | 改写成触发式描述，把用户口语变体列进去 |
| command 引用的 skill 路径失效 | 目录改名后 command 里的路径没同步 | 改名时全局搜索旧名逐处替换，保持「目录名 = `SKILL.md` 里的 `name` = 引用路径」三处一致 |
| 每轮对话都很慢、token 消耗高 | 常驻规则过长（示例里 3 份全设 `true`，常驻就是 20000 字符） | 把流程类内容下沉到 skill，rules 只留判断标准和禁止项 |
| 想回溯「上次为什么这么改」却查不到 | 只有 `handover.md` 滚动覆盖，没有 `sessions/` 留存 | 每次动手后补一份分钟级会话日志，specs 用于功能级改造 |

---

## 9. 该用 / 不该用的判据（Verdict）

**什么时候该用这套三层结构**：出现下面三个信号中的任意一个，就该分层——① `rules/` 里 `alwaysApply: true` 的规则加起来超过 8000 字符，AI 开始漏规则；② 同一段操作要求，你已经向 AI 交代过第三遍；③ 两个任务的规矩开始互相打架，比如一边要求「提交前必须跑全量测试」，另一边要求「提交前直接发版」。约束进 rules、入口进 commands、流程进 skills，三层各管一段上下文。

**什么时候不该用**：项目刚开始、规则不到十条时，直接一份 `rules/project.md` 写完全部约定就够了。过早拆成 commands + skills，只会让你在三个文件夹之间来回找文件，而 AI 依然要靠你手动打命令触发。分层的收益来自「内容多到必须按需加载」，内容不多时，分层只是增加维护成本。

---

本专栏《AI Agent 工具专栏》从工具调用、记忆管理、Skill 路由一路讲到规则治理与目录工程，每篇配一段可直接运行的代码和一张症状对照表，每周更新一篇。想系统看完 Agent 工程这条线，可在专栏页订阅。
