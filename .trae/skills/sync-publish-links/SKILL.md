---
name: sync-publish-links
description: 同步最近24小时内修改过的业务文档到各专栏 URL 目录，抓取审核通过链接并去重。Use when the user asks to sync publish links or 同步发布链接. Do not use for generating new docs.
---

# 同步发布链接（sync-publish-links）

> 📄 **完整规范参考**：本 skill 的定位、去重、抓取、写入、失败处理、汇报全部以 [sync-publish-links.md](../../commands/sync-publish-links.md)（本仓库 command 文件）为准。本文件作为入口与铁律兜底，执行时先读该 command 文件。

## 目标

找出**当前时间往前推 24 小时内修改过的业务文档**，对尚未记录在专栏 URL 目录里的，从掘金/CSDN 抓取「审核通过」的真实链接并写入对应 `*url链接目录*.md`。

## 前置条件

1. 读 `sync-publish-links.md` command 文件全文。
2. 用 `find` 按 `-mtime -1` 找到 24 小时窗口内修改的文档（不限一篇）。
3. 确认各专栏的 URL 目录文件名（`*url链接目录*.md`）。

## 执行主流程

- **① 定位候选**：`find` `-mtime -1` 列出 24 小时内修改的文档。
- **② 剔除已记录**：对每个候选，查对应 `*url链接目录*.md` 是否已有该文档链接；已记录的**跳过**。
- **③ 逐篇解析**：读文档标题/专栏/front-matter，确定落哪个专栏目录。
- **④ 抓取链接**：用内置浏览器在掘金/CSDN 搜索该文档标题，取「审核通过/已发布」的真实链接。
- **⑤ 写入目录**：只在对应 URL 目录**追加**一行，不修改原文档。
- **⑥ 汇报**：输出汇总表 `候选 N / 已记录 M / 待抓取 K / 写入 W`；全部已记录时报告「无需新增」。

## 关键铁律（不可省略）

- 🔒 **只用内置浏览器**，不调用平台 API。
- ⚠️ **CSDN 必须走 TRAE 内置沙盒浏览器（强制）**：CSDN 内容管理后台（`mp.csdn.net`）对**未登录的隔离 profile**（chrome-devtools MCP）会触发图形验证码/风控（见发布指令问题库第 34 条），因此 CSDN 一律走本机**已登录的 TRAE Browser Control（chrome 插件）通道**（`browser_tabs` / `browser_navigate` / `browser_evaluate` 等），**禁止使用 chrome-devtools MCP**。
- ⚠️ **掘金必须使用 chrome-devtools MCP 通道（与 CSDN 相反）**：掘金内容管理页的读取与注入依赖 `evaluate_script` 与隔离 profile，**必须使用 chrome-devtools MCP 通道**（`chrome-devtools_navigate_page` / `chrome-devtools_evaluate_script` 等），**禁止使用 TRAE Browser Control（chrome 插件）通道**。**两套通道互斥，同一轮严禁混用**。
- 🚫 **审核未通过一律不写**：掘金未过审不写；CSDN 仅「已发布」算通过；`/spost/` 链接不得写。
- 🚫 **不编造**：链接、状态、专栏名一律以实际抓取为准，取不到记录 ID 与时间，不伪造 URL。
- 🔒 **仅追加不改原文**：只往目录追加新行，不动原文档内容。
- 🔒 **自动 git 提交**：写入完成后 add/commit（英文 message），禁止 push。

## 交付汇报

输出汇总总表与逐篇 3 行详情，并说明是否有跳过/失败原因。
