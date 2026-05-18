---
trigger: always_on
---
# Git 操作规范

## 执行目录

所有 git 命令在本项目**根目录**下执行即可。

## 文件变更提交

每次修改、创建或删除文件后，**必须自动执行** `git add` 和 `git commit`（提交信息使用中文）。

> ⚠️ 注意：禁止自动执行 `git push`

## 用户修改代码后执行 Git

当用户说"修改了代码"或类似表述，要求执行 git 时：
1. 执行 `git status` 查看变更状态
2. 执行 `git diff -- "本项目/src" > "本项目/git_diff.diff"` 将差异输出到 diff 文件
3. 查看 diff 内容了解变更后(必须阅读"本项目/git_diff.diff"了解变更内容)，进行 `git add` 和 `git commit`
4. 提交完成后**FrontEnd/git_diff.diff 文件**不用删除

> ⚠️ 注意：禁止使用 `git diff -p --output`，会造成递归嵌套问题

## Git提交规范

格式：type(scope): subject
类型：feat|fix|docs|style|refactor|perf|test|build|ci|chore|revert|types|wip|release
规则：type小写 | subject非空 | 无句号 | subject最长72 | header最长100


## git_diff.diff 文件管理

- `git_diff.diff` 文件仅用于本地查看变更，**不需要跟踪**
- 该文件**不需要上传到 git**
- 每次生成新的 diff 文件时会自动覆盖旧内容，保持最新变更记录
