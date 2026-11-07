---
name: publish-csdn
description: CSDN 平台发布子 skill。用于将最新技术文档发布到 CSDN（csdn.net）。当用户说「发布最新文档到CSDN / 发布到CSDN / 发CSDN / csdn」时触发；也可由 publish-latest-doc command 在用户选择「CSDN」时引用。负责 CSDN 的通道选择、发布步骤、CSDN 平台问题库，并内联三平台共用前置流程。
---

# 发布到 CSDN（publish-csdn）

> 👉 **触发方式**：可由用户说「发布最新文档到CSDN / 发布到CSDN / 发CSDN / csdn」等关键词**独立触发**；也可由 `publish-latest-doc` command 第 0️⃣ 步用户选定「CSDN」时，由 command 引导读取本 skill。两种方式都会执行本 skill。

## 📌 通道铁律（强制）

| 项 | 要求 |
|---|---|
| **必须使用通道** | **TRAE 内置沙盒浏览器**（= TRAE Browser Control / chrome 插件通道，`browser_tabs` / `browser_navigate` / `browser_evaluate` / `browser_upload_file` / `browser_snapshot`） |
| **禁止通道** | **chrome-devtools MCP**（`chrome-devtools_*` 系列） |
| **原因** | CSDN 编辑器对**未登录的隔离 profile**（chrome-devtools MCP）必触发**图形验证码 / 风控**——进编辑器即拖拽验证、或提示「操作过于频繁」（见问题库 #34）。必须用本机已登录的 TRAE Browser Control 通道，复用已登录 cookie 继续发布。两套通道互斥，严禁混用。 |

> 🏷️ **通道术语对照**：用户口中的「TRAE 内置沙盒浏览器」= TRAE Browser Control / chrome 插件通道（`browser_tabs` 系列）。它与 chrome-devtools MCP（另一个隔离 profile 的调试通道）是**两套互斥通道**。CSDN 走前者，抖音 / 掘金走后者。

> ⚠️ **不要在同一通道反复重试**：一条通道一次到位。若用 chrome-devtools MCP 打开编辑器触发风控，立即切换到本机已登录的 chrome 插件通道。

## 🧩 共用前置流程（先执行，再进发布）

以下为三平台共用步骤，CSDN skill **各自内联**一份，执行时按序走完。

### P1 定位最新文章组（Document Group）

在项目根目录执行（Git Bash）：

```bash
find . -name "*.md" \
  -not -path "./.trae/*" \
  -not -path "./.git/*" \
  -not -path "*/resources/*" \
  -not -name "README.md" \
  -not -name "*url链接目录*" \
  -not -name "*目录.md" \
  -not -name "*-知乎.md" \
  -not -name "*-腾讯云.md" \
  -not -name "*-小红书.md" \
  -not -name "*-抖音.md" \
  -printf "%T@ %TY-%Tm-%Td %TH:%TM %p\n" \
  | sort -rn | head -n 5
```

- 🥇 取**母稿 mtime 最新**的一篇作为本轮发布对象，输出前 5 名候选及时间，报告最终选中项及理由。
- ⚠️ **秒级排序精度不足**：`%T@` 是秒级时间戳，批量产出时多篇同秒落盘。**必须在秒级之上做毫秒级二次判定**：对秒级结果中 mtime 相邻（同秒或差 <1s）的候选，用毫秒级 mtime（`find -printf "%T@ %TY-%Tm-%Td %TH:%TM:%TS"` 或 `stat -c %y` / `Get-Date` / `LastWriteTime`）精确比对，取**毫秒级最新**为一篇为母稿，其余同秒候选不作并列。报告附候选毫秒级时间。
- 🎯 **「最新且未发布」判据（强制）**：`find` 只按 mtime 倒序，不判断是否已发布。拿到前 5 名后须叠加「未发布」过滤——逐篇检查对应专栏 `00-*链接目录.md`，若该篇标题已在链接目录出现（掘金 / CSDN / 抖音任一平台记录）即视为已发布，跳过并标注。取 mtime 最新且未发布的一篇；前 5 名全已发布则顺延到前 10 名再判。⚠️ 过滤依据是**标题**匹配链接目录，不是文件序号。
- 🧩 由母稿路径推导整组 2 个文件，缺项直接标「未生成」：

| 产出 | 路径规则 | 发布平台 |
|---|---|---|
| 母稿 | 定位结果 | 掘金 + CSDN |
| 变体 | `{母稿去扩展名}-抖音.md` | 抖音 |

- 🚫 排除项：`.trae/`、`resources/`、`README.md`、各类 `url链接目录`、临时草稿与 `.rendered.html`。
- 🗂️ `*-知乎.md`、`*-小红书.md`、`*-腾讯云.md` 为历史遗留变体，已停止生成与发布，保留在 `find` 排除列表防止被误当母稿。
- ⚠️ **绝不允许**把变体文件当母稿发到 CSDN：变体按平台分发，母稿只走长文双平台。

### P2 解析标题、专栏与 front-matter

| 字段 | 母稿 | 变体 |
|------|------|------|
| **文章标题** | 文件名去扩展名 + 去编号前缀 | front-matter `title` |
| **摘要** | 按 P5 重写 | front-matter `summary`，仅按平台上限压缩 |
| **标签** | 正文 + 文件夹名提取 | front-matter `tags` |
| **专栏名** | 文档所在**文件夹名**（原样保留） | 同上（抖音无专栏，落成话题） |

- 🔢 编号前缀正则：`^[A-Za-z]{0,4}[0-9]+[A-Za-z0-9]{0,6}[-_ ]+`
- 🧪 对照示例：
  - `A04-AI时代什么样的程序员不会被淘汰-抖音.md` → 标题取 `title` 字段，文件名编号不进平台标题
  - `J1C-IDE选择与使用-...` → `IDE选择与使用-...`
  - `09aaa-LayerNorm是什么？` → `LayerNorm是什么？`
  - `@Bean注解基础入门-...` → 无编号，保持不变
- 🔗 **串台校验**：变体 front-matter 的 `source` 必须等于本组母稿完整文件名；不一致即视为串台，停止发布并在汇报里标注。
- 🏷️ 标签建议：CSDN **最多 5 个**（以页面提示剩余数量为准）。CSDN 允许 **Enter 键入自定义标签**，优先用正文里已写明的标签；账号等级不足时**不建自定义标签**，只从标签库选满 5 个（见问题库 #24）。
- 🎯 分类按正文技术栈选择（Java/Spring 类选「后端」，纯数据库选「后端」，前端框架选「前端」）。
- 🎯 专栏优先复用**已存在的同系列专栏**；确实不存在时才新建，名称取文件夹名。

### P3 生成封面图（两种比例）

刷信息流时用户只能看到三样东西：**标题、摘要、封面图**。两种比例各自独立生成，不能一张横图裁两个平台。

| 用途 | 尺寸 | 落盘路径 | 适用平台 |
|---|---|---|---|
| 横版 | `2560x1440`（16:9） | `Temp/<语义化主题>_2560x1440.png` | 掘金、CSDN |
| 竖版 3:4 | `1080x1440` | `Temp/<语义化主题>_1080x1440.png` | 抖音图文卡片（`P01` 兼封面） |

> ⚠️ **横版是「缩略图工程」**：CSDN 列表卡片里这张 16:9 图的实际展示宽度只有 **200–350 px**，字号按 `2560` 画布设计时很容易写成「只有原图看得清」。横版一切设计以「缩到 350 px 还读得出来」为唯一标准。

**做法**：调用全局 `/生成图片` 指令（绝对路径 `C:\Users\zheng\.trae-cn\commands\生成图片.md`，不在本项目内）分别生成 2 张，默认不加水印；发布时用 `upload_file` 上传到各平台封面框。

> ⏩ **提速：封面并发生成**（必做）：横版 `2560x1440` 与竖版 `1080x1440` 是 2 张独立图，用 `min(2,3)` 多线程并发生成，不要串行等两张。

**🖥️ 本机 Python 环境（需要代码绘制图片时用）** 🔒：

| 项 | 值 |
|---|---|
| 解释器 | `C:\Users\zheng\OneDrive\Desktop\CodeEnvironment\miniconda3\python.exe` |
| 版本 | Python 3.14.7（Anaconda 打包版） |
| 已装库 | Pillow 13.0.0 |
| 字体 | `C:\Windows\Fonts\msyh.ttc`（微软雅黑）、`consola.ttf`（等宽） |
| 调用方式 | **必须写全路径**：`python`、`py`、`python3` 都不在 `PATH` 上，直接调用会返回 `Python was not found` |
| 相邻工具 | `CodeEnvironment\ms-playwright`（需要 HTML 截图时可用）、`CodeEnvironment\ffmpeg-*` |

> ⚠️ 按 `Python命令行绘图规范.md`：一律用 `python -c` 内联执行，或在 `Temp/` 下写临时脚本、用完即删，**不得在项目目录留 `.py` 文件**。

**吸引力公式（按优先级）** 🔥：

1. **夸张情绪的主体**：一张脸或一个拟人化主体占画布 **15% 以上**，表情夸张的惊讶、崩溃或得意——缩到 200px 时只有极端表情还看得清。带人脸的封面实测点击率高出约 38%。
2. **眼神引流**：主体视线指向标题文字或画面冲突点。
3. **高对比撞色**：主体与背景用互补色，优先 **黄+黑**、红+白；整体「背景 80% 收敛、主体 20% 高饱和」。
4. **给结果、藏方法（悬念）**：画面只呈现冲突的结果，不给出解法。
5. **文字要大，字少字大**：横版主标题 **5–7 个字、字号 ≥ 画布宽的 1/10**；副标题／数字 **字号 ≥ 画布宽的 1/18**；全图文字总量 ≤ 20 字。竖版最多 5 个字，字号 ≥ 画布宽的 1/8。粗黑体，且不与文章标题重复。
6. **三元素上限**：主体 + 一个对比物 + 一行字，再多就糊成一团。

**必须贴合文档** 🎯：视觉隐喻直接取自本文核心冲突；图上文字只能来自标题或其同义改写，禁止出现文档里没有的数字、百分比、性能指标；禁止真实人物肖像、平台 logo、二维码、水印。

**落地检查** ✅：

- **横版按 350 px 宽自查**：主标题折合字高 ≥ `35 px`、副标题 ≥ `19 px`；看不清就放大字号或砍字后重出图。
- **🖼️ 文字测宽铁律（生成封面脚本必守）** 🔒：
  - **禁止固定 x 坐标 + 固定字号放文字**：必须先测量文字实际渲染宽度再决定字号与起点。
  - **必须用 `textlength` / `textbbox` 动态测量**：用 `fit_font(text, max_w, start_size, max_size)` 递归缩放字号直到宽度 ≤ `max_w`；起点 `x` 由「区域起点」而非「固定像素」决定。
  - **主标题字号有上限也要自动收缩**：即使写 `max_size=300`，测宽超 `right_max_w` 也要降字号回退（步长 4px），保证任何文本不超出画布右缘。`right_x` 取「左侧主视觉右缘 + 安全间距」，并反算 `right_max_w = 画布宽 - right_x - 右侧安全边距`。

### P4 生成发布稿（不改原文档）

在临时目录为**每个待发布产出各生成一份发布副本**，原文档**只读不写** 🔒

1. **🧾 剥离 front-matter**：变体首部 `---` 包裹的整段 YAML 必须删除（母稿无 front-matter，本步跳过）。
2. **✂️ 去掉正文首个一级标题**：若正文首行是 `# 与标题相同/相近的 H1`，删除该行。
3. **🖼️ 本地图片转 GitCode Raw URL**：按 `.trae/rules/GitCode图片URL转换规范.md` 转换
   - 基础地址：`https://raw.gitcode.com/ZhengEnCi/knoweledges/raw/master/`
   - `resources/P2L/photo/xx.png` → `https://raw.gitcode.com/ZhengEnCi/knoweledges/raw/master/Python-基础技术/resources/P2L/photo/xx.png`
   - 路径统一正斜杠 `/`，中文与空格做完整 URL 编码 ⚠️
4. **🧾 其余内容原样保留**：不润色、不删改段落、不调整结构 🚫
5. **📵 抖音额外做纯文本化**（仅抖音适用，CSDN 保留 Markdown）：见 publish-douyin skill。

### P5 平台摘要撰写（必做，禁止用平台自动提取）

发布面板里的「文章摘要」（CSDN，≤256 字）**必须手动重写**，不能保留平台自动提取的内容。

**分工** 🔀：

- **母稿**：掘金与 CSDN 各写一版，两版不得完全相同 ✅
- **变体**：直接用 front-matter `summary`（已是按平台改写的手写稿），只需按平台上限压缩，不得替换成平台自动提取内容

**写作规则** 🔥：

1. **开头 15 字内抛痛点或反常识结论**：不用「本文介绍了」「随着……的发展」这类开场
2. **中段给具体交付物**：几张表、哪几条约束、能解决什么答辩问题；用名词和数字，不喊口号
3. **结尾留一个具体钩子**：老师最爱追问什么、哪一步最容易翻车
4. **自然嵌入 1-2 个搜索关键词**（如「代码组织」「改动成本」），保证长尾搜索命中
5. **禁止**：编造数据、夸大承诺、「史上最全」「干货满满」「包过」「一键搞定」
6. **禁止直接复制正文首段**：摘要要能脱离正文独立阅读

**模板** 🧩：

```
{痛点或反常识结论}：{具体做法 + 关键数字}。{读者能拿走什么}，{留一个钩子}。
```

**落地检查** ✅：填完后读取输入框 `value`，确认字数未超限（≤256 字）、无残留的自动摘要。CSDN 摘要框默认是 AI 自动提取的内容，需**全选覆盖**。

### P6 图片渲染兜底（重点）⚠️

GitCode Raw 图片首次访问可能空白或返回占位图，必须验证后再发布：

1. 在浏览器**新标签页逐个打开**发布稿中的 GitCode 图片 URL
2. 等待图片真正加载完成（必要时**手动点击/刷新一次**触发 GitCode 渲染）
3. 回到编辑器，刷新预览或重新粘贴该图片，确认编辑器内**图片可见**
4. 若多次仍无法渲染：改为在编辑器中**直接上传本地图片**，替换该处外链
5. ✅ 所有图片确认可见后，才允许进入发布提交

### P7 配套资源链接预热（重点）⚠️

正文里的「📦 配套资源」直链（`.py` / `.java` / `.sql` / `.zip` / `.json` 等**非图片**文件）指向 `raw.gitcode.com`。该域名是 CDN，仓库文件首次被访问时可能返回 404、空白或占位内容——只有先在浏览器里真实走到该文件、触发一次回源，raw URL 才会稳定可下载。

**触发条件**：发布稿中存在 `https://raw.gitcode.com/...` 且后缀不是图片的链接，或正文出现 `> 📦 配套资源：` 行。命中即必须执行。母稿命中即视为全组命中，只需预热一次。

**做法** 🔧：

1. **列出清单**：从发布稿中抽出全部资源 URL，逐个 URL decode 得到仓库相对路径，整理成「URL → 相对路径」对照表
2. **进仓库首页**：`browser_navigate` 打开 `https://gitcode.com/ZhengEnCi/knoweledges`，`browser_snapshot` 确认页面正常渲染（不是 404、不是登录墙）
3. **模拟人工点击**：在文件树里**逐级点击**目录，最后点击目标文件名进入 blob 页面（必须真的点开每一级目录和文件，不能只改地址栏直达）
4. **确认文件内容**：blob 页面渲染出真实源码（能看到首行代码），而不是「文件不存在」提示
5. **再点 Raw**：点击「原始数据 / Raw」按钮打开 raw 页面，确认返回的是**纯文本源码**
6. **刷新校验**：在该 raw 标签页 `browser_navigate` 重新加载一次，仍能拿到内容，才算预热成功
7. **逐个复测**：对清单里每个资源 URL 重复第 2–6 步，全部通过后才允许进入发布
8. **兜底替换**：若某条 raw 链接重试 2 次仍 404 或空白，改用仓库 blob 页面 URL 替换正文该处链接，并在汇报里注明
9. **回写发布稿**：预热过程只允许调整链接形式，**不得改写资源名称、说明文字、所在段落** 🚫

## 6️⃣ 发布到 CSDN（母稿）

> ⚠️ **浏览器通道（强制，勿用 chrome-devtools MCP）**：CSDN 编辑器对**未登录的隔离 profile**（chrome-devtools MCP）必触发**图形验证码 / 风控**（进编辑器即拖拽验证、或提示「操作过于频繁」）。因此 CSDN **必须直接用 TRAE 内置沙盒浏览器（本机已登录的 TRAE Browser Control / chrome 插件通道）**：用 `browser_tabs` 列出本机浏览器 tab，`browser_navigate` 打开 `https://editor.csdn.net/md/`，复用已登录 cookie 继续发布。**不要用 chrome-devtools MCP 打开编辑器**，更**不要在同一通道反复重试**，一条通道一次到位。

1. 打开 `https://editor.csdn.net/md/`
2. 填入**文章标题**（已去编号）、**正文**（Markdown 模式粘贴）
   - 正文区域是 `pre.editor__inner`（contenteditable），聚焦后 `Control+V` 粘贴
   - ⚠️ **标题框防「【无标题】」**：发布前先读 `input.article-bar__title` 的 `value`，若为「【无标题】」或为空则用原生 value setter 填入真实标题 + 派发 `input`/`change` 事件（问题库 #30）
3. 点击「发布文章」打开面板 → 勾选**原创**，填写标签（最多 5 个，Enter 可添加自定义标签），上传**横版封面图**
   - ⚠️ **封面必须上传到服务端**：判据是出现 `https://i-blog.csdnimg.cn/direct/<hash>.png` 直链；`data:image/png;base64` 是本地预览，须再点一次「确认上传」才落库（问题库 #28、#29）
4. 选择**分类专栏**：优先复用已存在的同系列专栏（例如文件夹叫 `SQL-数据库技术专栏`，平台已有 `SQL-数据库查询技术专栏` 时直接复用，避免创建近似重名专栏）
   - 确实不存在才新建：`https://mp.csdn.net/mp_blog/manage/column` → 新建专栏 ✅
5. **填写摘要**：按 P5 撰写（≤256 字），不得留空、不得直接提交「AI 提取摘要」的原样结果
6. 按 P6 完成图片检查 → 直接点击「发布文章」（**无需再向用户确认**）
   - 「发布文章」按钮可能超出视口/命中失败：先定位发布面板 dialog（`textContent` 含「发布文章」+「添加文章标签」），在 dialog 内找 `textContent==='发布文章'` 的 button 直接 `.click()`（问题库 #25）
7. 发布成功后 URL 形如 `https://blog.csdn.net/{user}/article/details/{articleId}`，以 `creation/success/{id}` 页面出现为准
8. 发布后抽查：Mermaid 是否渲染为 SVG（正文不应残留 `erDiagram` 源码）、标签与专栏是否落库（查 `meta[name=keywords]`）、摘要是否是改写后的版本
9. **发布即评论**：点完「发布」立刻进入刚发布的文章，用作者账号发布一条钩子疑问句（见 7.2.1 钩子评论规范）🔒（CSDN 走 chrome 插件通道，确认评论落库）

## 7.2.1 钩子评论规范（全平台统一，发布即评）💬

**发布即评论** 🔒：对**掘金、CSDN、抖音**三个平台统一适用，落在**发布动作完成的下一瞬间**走——不等文章审核通过，点完「发布」立刻进入刚发布的文章/作品，用作者账号发一条钩子评论。

> 🤖 **全自动执行**：发布钩子评论是发布流程的**固定收尾步骤**，AI 自行进入作品详情页、发布钩子评论，**不需要向用户询问是否同意**。默认用户已授权。仅当出现平台验证（扫码/短信/滑块拼图）等必须人工介入的环节时，才停下来请用户协助。

**内容要求**（在「互动钩子」5 点基础上，补充一个**新角度**）：

| 要点 | 要求 | 示例 |
|---|---|---|
| 补一个新角度 | 给正文没展开的一个新判断或新数据 | 「我审 AI 代码最怕的不是语法错，是逻辑很『对』但根本不是业务要的」 |
| A/B 选项 | 给出两个明确可选答案 | 「A 遇到过 B 没踩过」 |
| 一句引导 | 用一句话鼓动回复 | 「你遇到过吗？评论区聊聊」 |
| 呼应正文 | 钩子要与文章核心判断一致 | 与标题/末页钩子口径对得上 |

**默认策略（无需手写）** 🤖：钩子疑问句由 AI **从正文核心冲突自动生成**——抓取全文最具争议的二元对立点，写成一句「具体经历 + A/B 选项 + 一句能回」的开放疑问。生成后无需用户确认，直接作为发布即评的钩子文案；若正文末页已有强烈钩子，可围绕它换一个角度改写。

**发布评论流程**：
1. 进入刚发布的作品详情页，点「评论」
2. 编辑评论，粘贴准备好的钩子文案（含一个新角度 + A/B 选项）
3. 提交，校验钩子评论成功上墙（评论区出现该评论、带作者标识）
4. 若平台支持且入口可用，可顺手置顶；不支持则不强制
5. ⚠️ **CSDN 评论可能触发滑块拼图风控**：点「评论」提交后弹出「请拖动滑块完成拼图」安全验证弹窗（`#layui-layer-shade1`）时，调用 `browser_waiting_for_user_interaction` 交用户人工完成拼图；验证通过后复核计数变 `1 评论` 即成功（问题库 #50）

**发布后 24 小时跟进**：有新评论就**及时回复**，避免评论冷场拖累互动率；回复尽量给判断而非敷衍。

## 🧠 CSDN 平台问题库（每次执行必读，解决后必更）

> ✍️ 写入规则：①解决后立刻写，同一「平台 + 症状」只保留一条；②四要素齐全：平台 / 症状 / 原因（可复现判断）/ 处理办法；③变体问题标后缀；④旧解法失效就改不新增；⑤不写敏感信息。

| # | 平台 | 症状 | 原因 | 处理办法 | 更新日期 |
|---|---|---|---|---|---|
| 1 | 掘金 / CSDN | 发出去的其实是抖音短文：标题 21 字、正文末尾带 `#话题` | 选文按 mtime 取最新 `.md`，`-抖音.md` 永远是最新的那个 | `find` 里加 4 条 `-not -name "*-平台名.md"` 排除；发布前校验变体 front-matter `source` 等于母稿完整文件名 | 2026-10-27 |
| 2 | 掘金 / CSDN | 正文顶部多出 `platform:` `title:` `summary:` 等 YAML 行 | 变体首部 front-matter 没剥离就整篇粘贴 | 生成发布稿第 1 步先删 `---` 包裹的整段 YAML，母稿跳过本步 | 2026-10-27 |
| 24 | CSDN | 标签区读出的全是左栏分类（`python,大数据,开发语言…`），点已选标签反而少了一个 | 已选 chip 是 `.mark_selection_box_el_tag`，候选项是 `.mark_selection_box li`；左侧分类项同为 `li`，误点会切走列表；chip 内 `.el-icon-close` 是删除按钮 | 读 chip 只用 `.mark_selection_box_el_tag`；候选用 `children.length===0 && textContent.trim()===关键词` 过滤后再 `.click()`；搜索框 `input[placeholder*="自定义标签"]` 用原生 value setter + `input` 事件；账号等级不足时不建自定义标签，只从标签库选满 5 个；**自定义标签添加时序**：`browser_type` 输入 → 等 ≥800ms 候选渲染 → 直接 Enter（`browser_type` 与 `Enter` 之间**不要插入 evaluate 查询脚本**，会干扰添加） | 2026-11-03 |
| 25 | CSDN | 「发布文章」按钮点不动（`browser_click` 报不可见 / 命中失败） | 该按钮不在 `.modal__content` 内，且 `y≈909` 超出视口；发布面板内按钮 class 已由 `btn-b-red` 改为 `btn btn-publish`；面板挂载过「定时发布」子 dialog 后 evaluate `.click()` 会静默失效 | 先定位「发布文章」面板 dialog（`textContent` 同时含「发布文章」与「添加文章标签」），**优先 snapshot 拿 `button "发布文章"` 的 ref 用 `browser_click` 真实点击**；evaluate `.click()` 无效（页面停留编辑器、dialog 仍开）时立刻切 browser_click；跳转 `mp.csdn.net/mp_blog/creation/success/<id>` 即成功 | 2026-11-06 |
| 28 | CSDN | 发布弹窗封面区已显示图片，发布后列表卡片与博客首页都没有封面 | 弹窗里显示的是 `data:image/png;base64` 本地预览，图片没上传到服务端；`vue-image-crop-upload` 裁切器必须再点一次「确认上传」才真正落库 | 唯一通过判据是出现 `https://i-blog.csdnimg.cn/direct/<hash>.png`：发布前读 `.preview-box.hasImg img` 的 `src`，以 `i-blog.csdnimg.cn` 开头才算完成，`base64` 一律视为未上传；发布后用 `mp.csdn.net/mp_blog/manage/article` 卡片 `.list-item-mp-left` 的 `background-image` 复核 | 2026-10-28 |
| 29 | CSDN | 封面 file input 是 `display:none`，`browser_snapshot` 取不到 ref；给按钮 ref 调 `browser_upload_file` 报 `could not accept the file directly, and clicking it did not trigger a file chooser` | 隐藏元素的 AX 节点不进快照；裁切器「确认上传」是 `div.vicp-operate-btn`，无 button 语义，同样取不到 ref | ①`browser_evaluate` 把 `.cover-upload-box input.el-upload__input` 改成 `display:block;position:fixed;left:8px;top:8px;width:48px;height:48px;opacity:0.02` ②重新 snapshot 得到 `textbox` ref ③`browser_upload_file` 直传绝对路径（不走 `fetch`，避开 CORS）④给 `.vicp-operate-btn` 补 `role=button` + `aria-label` 再 snapshot 取 ref 并 click ⑤校验 `i-blog.csdnimg.cn` 直链 | 2026-10-28 |
| 30 | CSDN | 发布后审核提示「违规-不符合定位」，文章标题显示「【无标题】」，后台「审核中/未通过」里有该文 | 发布时标题框 `input.article-bar__title` 被填成了占位符「【无标题】」（CSDN 在标题为空时自动填充并当作实际标题提交，命中《CSDN 社区内容创作规范》7.3.6 文章无标题），导致审核判「不符合定位」 | ①发布前先读 `input.article-bar__title` 的 `value`，若为「【无标题】」或为空则用原生 value setter 填入真实标题 + 派发 `input`/`change` 事件 ②发布成功后到 `mp.csdn.net/mp_blog/manage/article` 复核状态，应从「审核未通过」变为「待审核」 ③标题按「5~100 字」落位，不依赖平台自动提取 | 2026-10-29 |
| 34 | CSDN | 进 `editor.csdn.net/md/` 就反复触发图形验证码（拖拽滑块 / 操作过于频繁），浏览器通道反复验证不过 | chrome-devtools MCP 用**隔离 profile**（无登录 cookie），CSDN 对未登录 editor 必触发风控 | **立即切换到本机已登录的 TRAE Browser Control（chrome 插件）通道**：`browser_tabs` 列本机 tab（参数 `{action:'list'}`）→ `browser_navigate` 打开编辑器 → 直接复用已登录 cookie 发布；**不要在同一通道反复重试** | 2026-10-30 |
| 50 | CSDN | 钩子评论找不到可见的「评论」提交按钮（`.btn-submit` 尺寸 `0x0`、页面上无文本为「评论」的可见按钮），JS `.click()` 与 evaluate 派发事件均无反应；吐槽滑块验证弹窗（`#layui-layer-shade1`）出现时无法自动完成 | 评论框在侧边抽屉 `.comment-box-new2` 内，提交控件不可见/被模板遮挡；评论提交还另触发滑块拼图风控 | ✅ **最稳路径（2026-11-07 验证）**：①`document.querySelector('.go-side-comment').click()` 展开抽屉；②用原生 setter 把文案写入 `textarea#comment_content` 并派发 `input`；③`ta.focus()` 后 `browser_press_key({key:'Control+Enter'})` **直接提交**（textarea 清空即已提交）；④校验不能只看 `document.body.innerText`——评论落在 `.new-comment` 节点里，用 `document.querySelectorAll('.new-comment').length` 与首条文本确认；⑤若弹滑块再 `browser_waiting_for_user_interaction` 交用户 | 2026-11-07 |
| 51 | CSDN | 封面 PNG 上传后裁切器无图或「确认上传」后封面区仍为空、不落库 | 封面文件 >5MB（实测 5.78MB 上传失败）；裁切器「确认上传」用 evaluate `.click()` 不触发 Vue handler | 上传前用 Pillow 压缩封面：`resize` 到 1920x1080 + `optimize=True`，目标 <4MB（实测 3.1MB 成功）；裁切器内「确认上传」必须**补 `role=button`/`aria-label` 后 snapshot 拿 ref 用 `browser_click`**（真实点击），不能 evaluate `.click()`；落库判据仍为 `i-blog.csdnimg.cn` 直链 | 2026-11-03 |
| 52 | CSDN | 发布面板内 `browser_click` 报「Element is not visible」、`browser_evaluate` 检测元素可见但点击无效，浏览器 viewport 为 `0x0` | TRAE 浏览器窗口被最小化/隐藏（`window.innerWidth/Height` 均为 0），CDP 无法命中可见元素 | **首选免打扰方案**：`browser_tabs({action:'close'})` 关掉旧 tab → `browser_navigate({url, newTab:true})` 重开新 tab，viewport 即恢复（实测 1814x1191 / 598x830，无需用户接管）；若重开仍 0x0 再调 `browser_waiting_for_user_interaction` 请用户最大化窗口；恢复后 `browser_click` 正常；期间封面上传若 evaluate 点击看似失败，重开流程后先查 `.container-coverimage-box img` 的 `i-blog.csdnimg.cn` 直链，可能已实际落库 | 2026-11-06 |
| 53 | CSDN | 发布面板「新建分类专栏」点击无响应（evaluate `.click()` 与 `browser_click` 均不弹出新建输入框），panel 无新 dialog | 新建专栏入口依赖跳转 `mp.csdn.net/mp_blog/manage/column` 或弹窗被环境限制拦截 | 不为新建专栏阻塞发布：**按内容主体复用最贴近的既有专栏**（如 CV 视觉定位 SOTA 评测复用「LLM-大模型技术专栏」），并在汇报中注明复用理由；确有必要时再单独去专栏管理页新建，下一轮发布即可勾选 | 2026-11-06 |
| 54 | CSDN | 直接调用工具列表里**看不到** `browser_tabs` / `browser_navigate` / `browser_evaluate`（TRAE Browser Control），只有 `chrome-devtools_*`；而 chrome-devtools 打开 `editor.csdn.net/md/` 被重定向到 `passport.csdn.net/login`，窗口坐标还在屏幕外（`screenX≈2560, screenY≈-532`） | 内置浏览器工具**未直接暴露在工具面板**，但在 code_mode 运行时里注册着——`Exec` 内 `Object.keys(tools)` 能看到完整 `browser_*` 系列 | ✅ **正确解法**：在 `Exec` 里 `await tools.browser_navigate({url, newTab:true})` 调内置浏览器；首次导航后 `innerWidth` 可能为 `0x0`，**再 `browser_take_screenshot()` 或做一次交互即可恢复**（实测 960 宽）。全部步骤都能在 Exec 内完成：`browser_evaluate` 注入正文/设值、`browser_snapshot` 取 ref、`browser_click`/`browser_type`/`browser_press_key` 真实交互、`browser_upload_file` 传图；evaluate 脚本**禁止出现 `return`**（含 `function(x){return ...}`），否则整段返回 `undefined`。| 2026-11-07 |

### 🌐 全平台通用问题库（内联）

| # | 平台 | 症状 | 原因 | 处理办法 | 更新日期 |
|---|---|---|---|---|---|
| 6 | 全平台 | `browser_evaluate` 一律返回 `undefined`，无论脚本多简单 | 脚本里出现 `return` 关键字（含 `function(x){return ...}` 与箭头函数 block body），整个 evaluate 结果被吞 | 只写**单个表达式**：隐式返回箭头或赋值 `window.__x=function(el){...}`（无 return）；需要多语句用逗号表达式 | 2026-10-27 |
| 7 | 全平台 | `SyntaxError: Invalid regular expression: missing /` | 脚本里的 `/\n/g` 被解析成真实换行，正则失去结尾斜杠 | 禁止在 evaluate 里写 `\n` 正则，改用 `String.fromCharCode(10)` 配 `split/join` | 2026-10-27 |
| 8 | 全平台 | 正文注入失败：远程剪贴板（`Set-Clipboard` + `Control+V`）只在本机生效 | 浏览器由扩展远程驱动，剪贴板不通 | 本地起静态服务（`serve.ps1`，`Access-Control-Allow-Origin: *`）→ 页面内 `fetch` 取纯文本写入全局变量 → `new DataTransfer()` + `new ClipboardEvent('paste',{clipboardData:dt,bubbles:true})` 派发到聚焦后的编辑器 | 2026-10-27 |
| 9 | 全平台 | 封面图上传框是隐藏 file input，`upload_file` 与 click 均无响应 | 元素 `display:none` 或已游离 DOM，脚本取到的是被丢弃的实例 | 覆写 `HTMLInputElement.prototype.click` 捕获真实 input，再用 `DataTransfer` 合成 `File` 派发 `dragenter/dragover/drop` 到目标及祖先链；上传后以 `img.naturalWidth` 校验 | 2026-10-27 |
| 10 | 全平台 | 单标签页报 `WebView is not ready yet (timeout after 5s)`，之后该 tab 全部操作失败 | 该 tab 的 renderer 已卡死，无法恢复 | `browser_tabs({action:'close',viewId})` 关掉 → `browser_tabs({action:'new'})` → 显式 `browser_navigate`；工具名为 `browser_tabs`，**不存在** `browser_close_page` | 2026-10-27 |
| 17 | 全平台 | 命令行执行 `python`、`py`、`python3` 全部报 `Python was not found` | 系统未把 Python 加进 `PATH`，环境装在桌面 `CodeEnvironment` 目录 | 用全路径 `C:\Users\zheng\OneDrive\Desktop\CodeEnvironment\miniconda3\python.exe`（3.14.7 + Pillow 13.0.0）；配套 Playwright 在 `CodeEnvironment\ms-playwright` | 2026-10-27 |
| 18 | 全平台 | `list_pages` 报 `The browser is already running for ...\.cache\chrome-devtools-mcp\chrome-profile`，随后该 MCP 全部浏览器调用失败 | chrome-devtools MCP 独占 profile，与本机已开 Chrome 抢锁 | 改用 `integrated_code_mode` 的 `Exec`：`await tools.browser_evaluate/navigate/click/press_key`，输出必须 `text(String(r.content[0].text))`（`text(r)` 只会打印 `[object Object]`） | 2026-10-27 |
| 23 | 全平台 | `browser_evaluate({code:'...'})` 报 `missing field 'script'`；改传 `script` 后 IIFE 与顶层 `await` 一律返回 `undefined` | 该工具只接受 `script` 字符串，执行上下文按 V8 表达式求值：IIFE 没有隐式返回值、顶层 `await` 不被支持、异常被吞 | 参数固定 `{script}`；脚本写成「多条语句 + 最后一条为表达式」；需要等待时在 Exec 层 `await new Promise(r=>setTimeout(r,ms))` | 2026-10-28 |
| 33 | 全平台 | `upload_file` 与 `evaluate_script` 的 `sourcePath` 一律报 `not within any of the configured workspace roots` | chrome-devtools MCP 的 workspace roots 是硬编码白名单，项目路径不在名单内；但 `os.tmpdir()`（`C:\Users\zheng\AppData\Local\Temp`）**始终是允许的 root** | 所有要上传的封面/卡片图先复制到 `C:\Users\zheng\AppData\Local\Temp\`，再 `upload_file` 该绝对路径；`evaluate_script` 的脚本用 `function` 参数内联，或改走 `data:`/`fetch` 方案 | 2026-10-29 |
| 37 | 全平台 | 封面脚本生成的图主标题 / 副标题被**右缘硬裁** | 生成脚本用了**固定 x 坐标 + 固定字号**放文字，从不测量文字实际宽度 | 封面脚本**必须先测文字宽度再定字号与起点**：用 `fit_font(text, max_w, start_size, max_size)` 按 `textlength`/`textbbox` 递归缩放字号直到宽度 ≤ `max_w`；起点 `x` 由「左侧主视觉右缘 + 安全间距」算出 `right_x`，并反算 `right_max_w`。**禁止写死 `(x,y)` 和固定 `size`** | 2026-10-31 |
| 40 | 全平台 | `card_gen.py` 生成的卡片只放到 serve 根目录 `Temp/publish`，**漏掉正式归档** | 只做了前一半；卡片/脚本要一步到位落位到 `resources/` | `card_gen.py` 输出目录**直接指向** `resources/{文档编号}/douyin/photo/`，脚本复制到 `resources/{文档编号}/douyin/code/`，**不经过 `Temp/` 中转**；生成完成后核对归档目录字节数一致 | 2026-11-01 |
| 42 | 全平台 | `card_gen.py` 卡片里序号 `①②③` 直接压住正文文字 | 正文起点写死 `bx = x + 42`，但字号被撑大后序号实际宽度超过 42px，正文起点却没动 | 改为**动态测量序号真实宽度**再定正文起点：`seq_w = d.textbbox((0,0), seq, font=f_body)[2]`，`bx = x + seq_w + 16`。**禁止**写死后续 X 坐标 | 2026-11-01 |
| 43 | 全平台 | 「按修改时间找」一次列出**两篇**都未发布的候选 | `find %T@` 是**秒级**时间戳，批量产出时多篇同秒落盘，排序精度不够 | 秒级排序后**必须做毫秒级二次判定**：对同秒/相邻（<1s）候选，用文件系统毫秒级 mtime 精确比对，取**毫秒级最新**者为母稿；报告附候选毫秒级时间 | 2026-11-01 |
| 46 | 全平台 | `card_gen.py` 里数字 `99.2%`、`9%–18%`、`bf16` 被**字符级断行**拆开 | `wrap_text` 按**单字符**切词断行，遇到含小数/百分号/区间的数字串就把首字符单独成行 | 引入 `tokenize`：用 `re.compile(r'[0-9]+(?:\.[0-9]+)?%?(?:\s*[–—-]\s*[0-9]+(?:\.[0-9]+)?%?)?')` 把数字/百分比/区间当作**原子 token**，`wrap_text` 按 token 断行 | 2026-11-01 |
| 47 | 全平台 | 封面卡把「大标题：」「副标题：」这类**元标签前缀**渲染进卡面 | 卡面字段直接用了 markdown 里的标注，脚本按原样画到图上，未剥离标签前缀 | **标签前缀必须回到文档里删**：`- 大标题：**同一个模型**` → `- **同一个模型**`。发布前用 `browser_evaluate` 检查卡面 `innerText` 不含「大标题」「副标题」「核心数字」字样 | 2026-11-01 |

**变体适配固定检查**（粘贴前先过一遍）：

| 变体 | 粘贴前必查 |
|---|---|
| 母稿 | 无 front-matter、H1 已删、Markdown 语法完整 |
| `-抖音` | 标题 ≤20 字、描述 ≤200 字并已纯文本化、卡片图张数 = 文档页数 N（`P01…PN` 一页一卡）且已上传、文字与文档逐字一致、**背景音乐已选中** |

## ✅ 发布后汇报（CSDN 行）

在 command 第 9️⃣ 节表格中输出 CSDN 行：

| 平台 | 文章标题 | 专栏 / 分类 | 状态 | 链接 |
|------|----------|-------------|------|------|
| CSDN | {母稿去编号标题} | {文件夹名或实际复用专栏} / {分类} | 已发布 / 待审核 / 失败 / 未选 | {URL} |

- 🔁 平台已存在同名文章时，不重复创建，报告已有链接，按「更新」处理（编辑原文后重新发布）。
- 📝 注明实际使用的分类、标签、专栏。
- 🔍 发布后复核：`mp.csdn.net/mp_blog/manage/article` 看状态（待审核 / 审核未通过）；标题「【无标题】」需按问题库 #30 处理。
