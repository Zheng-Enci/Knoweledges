# Tasks

- [x] Task 1: 新增指令文件 `.trae/commands/sync-publish-links.md`，写清完整执行流程
  - [x] SubTask 1.1: 写入 front-matter（name / description）与适用场景
  - [x] SubTask 1.2: 写入「定位最新文档」规则，复用 mtime 排序、排除项、去编号正则与专栏名规则
  - [x] SubTask 1.3: 写入掘金 / CSDN 的链接抓取步骤与审核状态判定规则
  - [x] SubTask 1.4: 写入链接目录定位、格式识别、追加、去重与新建模板规则
  - [x] SubTask 1.5: 写入失败处理（审核中 / 未通过 / 未找到 / 专栏无法映射）与结果汇报表格
- [x] Task 2: 核对指令规则与现有链接目录格式兼容
  - [x] SubTask 2.1: 核对表格型目录（`LLM-大模型技术专栏/LLM00-url链接目录.md`）
  - [x] SubTask 2.2: 核对列表型目录（`AI-Agent工具/AI00-url链接目录.md`）
  - [x] SubTask 2.3: 在指令中补全两种格式的写入示例
- [x] Task 3: 按项目 Git 规范提交新增指令文件
  - [x] SubTask 3.1: 经用户确认后执行 `git add` + `git commit`（英文 commit message）
  - [x] SubTask 3.2: 不执行 `git push`

# Task Dependencies
- Task 2 depends on Task 1
- Task 3 depends on Task 1 and Task 2
