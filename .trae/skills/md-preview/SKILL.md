---
name: md-preview
description: 用 render-md.py 把当前 md 文件嵌入 HTML 模板并在浏览器渲染预览。Use when the user asks to preview or render a markdown file 预览渲染. Do not use for generating documents.
---

# md 渲染预览（md-preview）

> 📄 **完整规范参考**：本 skill 的执行命令以 [md-preview.md](../../commands/md-preview.md)（本仓库 command 文件）为准。本文件作为入口，执行时先读该 command 文件。

## 目标

用 `render-md.py` 把当前 Markdown 文件嵌入 HTML 模板，在浏览器中渲染出预览效果。

## 前置条件

1. 读 `md-preview.md` command 文件全文。
2. 确认当前要预览的 `.md` 相对路径。

## 执行主流程

- **① 定位当前 md**：确认要预览的 Markdown 文件相对路径。
- **② 执行渲染**：运行 `python render-md.py <当前md相对路径>`。
- **③ 浏览器查看**：脚本渲染后自动在浏览器打开预览。

## 关键铁律（不可省略）

- 🔒 用 `python render-md.py <相对路径>` 即可，参数为当前 md 的相对路径。
- 🚫 不要修改 md 源文件，仅渲染预览。

## 交付汇报

报告预览已打开，或贴出渲染报错以便排查。
