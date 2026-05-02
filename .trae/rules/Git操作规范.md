---
alwaysApply: true
---
# Git 操作规范

## 基本原则

当对仓库中的文件进行以下操作时，必须自动执行 git add 和 git commit：

- 创建新文件
- 移动/重命名文件
- 删除文件
- 修改文件内容

## 操作流程

1. 执行 `git add <文件>` 将改动添加到暂存区
2. 执行 `git commit -m "<提交信息>"` 提交改动

## 重要规则

### 禁止操作
- **严禁执行 git push 命令**
- 禁止强制推送（git push --force）

### 提交信息要求
- 必须使用中文编写 commit 信息
- 信息应简洁描述本次改动内容

### 示例
```bash
git add <改动文件>
git commit -m "更新文档内容"
```

---

**注意**：所有文件操作后都应自动触发 git add 和 commit，无需用户额外指示。
