# Checklist

- [x] 指令文件位于 `.trae/commands/sync-publish-links.md`，front-matter 含 `name` 与 `description`
- [x] 最新文档定位规则与 `publish-latest-doc` 一致：mtime 倒序 + 相同排除项 + 前 5 名候选展示
- [x] 标题去编号正则与 `publish-latest-doc` 一致，专栏名取父文件夹名
- [x] 掘金与 CSDN 两个平台均包含链接抓取步骤
- [x] 仅「审核通过」的链接允许写入链接目录
- [x] 「审核中」「未通过」等状态会明确告知用户且不写入
- [x] 链接目录写入兼容表格型与列表型两种现有格式
- [x] 同一平台同一 URL 已存在时不重复追加
- [x] 链接目录不存在时按编号前缀新建，专栏无法映射时停止并询问用户
- [x] 结束时输出「平台 / 标题 / 审核状态 / 是否写入 / 链接」汇报表格
- [x] 指令明确不修改原文档、不自动 `git push`
