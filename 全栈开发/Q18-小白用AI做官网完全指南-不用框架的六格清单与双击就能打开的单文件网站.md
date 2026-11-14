# 小白用 AI 做官网完全指南：不用任何框架，一张六格清单 + 双击就能打开的单文件网站

> **核心结论**：小白用 AI 做官网，翻车点从来不是代码，而是三件事没交代清楚——**页面有哪几块**、**什么样算好看**、**交付成什么形态**。只丢一句「帮我做个公司官网」，AI 只能按模板套；把需求写成一张 **6 格清单**（谁看 / 有哪几块 / 什么风格 / 什么尺寸 / 怎么交付 / 怎么验收），再让它**先联网搜参考站、后写代码**，最后统一按「单文件 + 相对路径 + 零外链」交付，双击就能打开。本文给一张可直接抄的提示词、一段 13.6 KB 的完整可运行代码，以及桌面双击打开时 5 种打不开的排查路径。

📦 配套资源：[可直接双击运行的单文件官网模板（带逐行注释）](https://gitcode.com/ZhengEnCi/knoweledges/blob/master/resources/Q18/index.html)

## 目录

- 1. 一句话结论
- 2. 一个官网其实只需要 6 块
- 3. 制作方法：四步走到能打开
- 4. 提示词该写什么：六格清单
- 5. 一条可直接复制的完整提示词
- 6. 让 AI 自己联网学 UI 的三步法
- 7. 完整可运行代码（单文件官网）
- 8. 桌面上怎么双击打开
- 9. 对照表：症状 → 原因 → 解法
- 10. 发布前验收清单

## 1. 一句话结论（Conclusion）

先看一个画面 🏠：你请施工队装修，只说「我家 90 平，你看着办」——他只能按自己熟悉的样板间做，做完你说「太像出租屋」。官网是同一回事：**AI 不是不会写 HTML（超文本标记语言），是你没给它户型图、材料清单和验收标准。**

三条判断，记住就能少走 90% 的弯路：

- **结构先于样式**：先定「有哪 6 块」，再谈配色。没结构，AI 只能堆一堆居中的大标题。
- **风格必须可判定**：说「大气一点」它听不懂；说「主色只有一个、标题不超过 2 种字号、区块间距 88px」它立刻能执行。
- **交付形态决定成败**：单文件、内联样式、零外部链接，双击就能开；拆成三个文件还引 CDN（内容分发网络）字体，小白第一步就卡住。

这和我在[12 种高级 UI 交互效果及对应 AI 提示词](https://juejin.cn/post/7704947965462315035)里讲的是同一条规律：**AI 只认具体、可判定的规格**。你说「加个动效」它给最普通的缩放，说「松手先弹到 1.05 再落回 1.0」它才照做。

## 2. 一个官网其实只需要 6 块（Page Structure）

别让 AI 自由发挥，直接给它区块清单。一家小公司、一个工作室、一款产品，首页都是这 6 块：

| # | 区块 | 一句话该写什么 | 缺了会怎样 |
|---|---|---|---|
| 1 | 导航栏（nav） | logo + 3–4 个锚点 + 一个主按钮 | 访客不知道还能往下看什么 |
| 2 | 首屏（hero） | 一句主标题 + 一句副标题 + 两个按钮 + 一块视觉 | 三秒内说不出你是干什么的 |
| 3 | 服务或产品 | 3 张卡，每张一句话 | 访客只能猜你能提供什么 |
| 4 | 证明 | 3 个数字、客户 logo 或一句评价 | 全是自夸，没有可信度 |
| 5 | 联系入口 | 邮箱、电话或表单，整页只有这一个主按钮 | 想咨询的人找不到出口 |
| 6 | 页脚（footer） | 版权 + 联系方式 + 年份 | 页面像没做完 |

为什么是 6 块？因为**小白最容易犯的错是「什么都想放」**——简介四段、团队九人、新闻十条。访客只会做一次判断：**这家能不能解决我的问题**。6 块刚好答完，多一块都是干扰。

一个比喻 🍱：官网像一份便当，不是自助餐。米饭、主菜、两样配菜、一个汤位，摆满就够；硬塞十二格，每格都只剩一口。

## 3. 制作方法：四步走到能打开（Workflow）

**第 1 步：建文件夹，不写代码。** 桌面右键 → 新建文件夹，命名 `website`，路径不带中文、不放系统目录。**所有东西以后都在一个盒子里**，换电脑、发给别人都不丢图。

**第 2 步：先要结构，不要代码。** 发第 4 节的六格清单，末尾加一句：**「先只输出区块大纲和每块文案，我确认后再写代码。」** 结构错了，改样式是白改。

**第 3 步：分段生成。** 一次要 600 行，它会在后半段丢上下文：导航两套、圆角三种。拆成「骨架 → 首屏 → 手机端」三段，每段单独能跑、单独能预览。

**第 4 步：保存、双击、三处验收。** 只看**有没有横向滚动条**、**首屏有没有一个主按钮**、**拖窄到手机宽度有没有挤乱**。三条都过，就能拿去给人看。

## 4. 提示词该写什么：六格清单（Prompt Checklist）

公司信息只是第 0 格。真正决定成品质量的，是后面六格：

**① 谁看（Who）。** 「给本地餐饮老板看的 B 端（企业端）服务页」和「给学生看的社团招新页」，结构完全不同。写清访客身份、他此刻的疑问、你希望他做什么动作。

**② 有哪几块（Sections）。** 直接抄第 2 节的 6 块，每块配一句真实文案。**先给文案，再要代码**——AI 会按文案长度排布局，比它自己编占位文字准得多。

**③ 什么风格（Style）。** 三个形容词 + 一个参考站 + 一个主色 + 一个禁用项。例如「干净、克制、偏科技感；参考 stripe.com 的信息密度；主色 `#4f7cff`；不要紫色渐变球、不要发光边框」。形容词给方向，禁用项负责止损。

**④ 什么尺寸（Responsive）。** 写死断点：「桌面按 1440px 设计，内容区最大 1120px 居中；900px 以下塌成单列；导航在手机上隐藏」。不写断点，AI 默认不做手机端。

**⑤ 怎么交付（Deliverable）。** 小白最容易漏、也最致命的一格：**「只要一个 `index.html`，CSS 和 JS 全部内联，不引用任何外部 CDN、外部字体、外部图片；视觉元素用 CSS 渐变或内联 SVG 画。」** 单文件意味着能双击打开、能微信发给别人、能丢到任何服务器上。

**⑥ 怎么验收（Acceptance）。** 写成能数出来的：「全站 1 个主色 + 1 个辅色；字阶不超过 4 级；区块间距 88px；任何宽度下不出现横向滚动条；每屏最多 1 个主按钮。」**能被数出来的规则，AI 才会真的执行。**

### 4.1 风格词怎么写才不白写

「大气」「高级」「有质感」是三个最常被写、也最没用的词。把它们翻译成可执行参数：

| 你想要的 | 别这么写 | 这么写 |
|---|---|---|
| 大气 | 页面要大气 | 内容区 1120px 居中，区块间距 88–96px，标题字号 40–56px |
| 高级 | 高级一点 | 只用 1 个强调色，其余为黑灰白；不用阴影叠阴影；圆角统一 12px |
| 有呼吸感 | 留白多一点 | 标题与正文间距 18px，卡片内边距 26px，任意两区块之间不小于 80px |
| 现代 | 现代风格 | 无衬线字体，标题字重 700，正文 400，渐变仅用于 1 个按钮 |

## 5. 一条可直接复制的完整提示词（Copy-Ready Prompt）

把下面这段整块复制，替换方括号里的内容即可：

```markdown
你是资深前端工程师兼 UI 设计师。请为 [公司名] 做一个官网首页。

【公司信息】
- 业务：[一句话说清卖什么]
- 客户：[谁会来看这个页面]
- 希望访客做的动作：[留邮箱 / 打电话 / 加微信]
- 现有素材：[只有公司名和电话 / 有 logo 和 3 张产品图]

【页面结构】严格按这 6 块，顺序不可增删：
1. 导航：logo + 服务/案例/联系 3 个锚点 + 1 个主按钮
2. 首屏：主标题（≤18 字）+ 副标题（≤40 字）+ 主次按钮 + 一块视觉区
3. 服务：3 张卡片，每张含编号、标题、一句 ≤30 字的说明
4. 证明：3 个数字指标
5. 联系：一个居中区块，只留 1 个主按钮
6. 页脚：版权 + 联系方式 + 自动年份

【风格】
干净、克制、偏科技感。主色 #4f7cff，辅色 #7c5cff，其余为黑灰白。
禁用：紫色发光球、重叠阴影、超过 2 种字体、超过 4 级字号。

【尺寸】
桌面按 1440px 设计，内容区最大 1120px 居中，左右留 24px。
900px 以下全部塌成单列，导航菜单隐藏。
任何宽度下不允许出现横向滚动条。

【交付】
只输出一个 index.html。CSS 与 JS 全部内联在文件内。
禁止引用任何外部 CDN、外部字体、外部图片、外部图标库；
视觉区用 CSS 渐变或内联 SVG 实现。

【流程】先只输出区块大纲与每块文案，我确认后再输出完整代码；代码输出后按【验收】逐条自查。

【验收】
1. 全站只用 1 个主色 + 1 个辅色
2. 字阶不超过 4 级
3. 区块垂直间距 88px
4. 桌面与手机宽度下均无横向滚动
5. 每个区块最多 1 个主按钮
```

注意最后那段「先结构、后代码、再自查」。**这三步是整条提示词里最值钱的部分**，因为它把一次性的赌博式生成，换成了三次可检查的交付。

## 6. 让 AI 自己联网学 UI 的三步法（AI Research）

你不懂 UI 没关系，但你要会让 AI 去学。这里有个关键认知：**AI 联网读到的多半是网页源码和文字描述，不是「审美判断」**。所以别问它「哪个好看」，要让它输出**能被写进代码的规格**。

**第一步：给它搜索目标，不给「好看」这个词。** 搜索词要带行业和页面类型，而不是泛泛的「好看的网站」。设计社区的经验是：搜 `onboarding` 只会得到通用的引导页，搜 `banking app onboarding` 才会出现 KYC（实名认证）、合规声明这类真实结构。做官网同理，搜「律所官网 首页」比搜「企业官网模板」有用得多。

**第二步：让它输出去重后的拆解表，不输出方案。** 提示词：

```markdown
请联网搜索 3 个 [行业] 的官网首页（优先 awwwards.com、dribbble.com、siteinspire.com 上的案例），
然后只输出一张拆解表，列：首屏栏数 / 标题字号 / 正文行高 / 区块间距 / 配色数量 / 有无大图 / 有无动效。
不要给我设计建议，也不要写代码。
```

**第三步：你挑一行，让它把那一行翻译成 CSS 规格再写码。** 例如你选了「首屏两栏、标题 48–56px、配色 2 种、无大图」——这三个数字就是第 5 节提示词里「风格」和「尺寸」两格的答案。这时再让它写代码，出来的东西就有据可依。

两个必须提醒的坑：

- **获奖站是视觉参考，不是可用性参考。** Awwwards 上的站为了视觉冲击常把导航藏起来、对比度压低。让 AI 学它的**版式节奏**，别学它的**交互复杂度**。
- **写明「只学结构，不抄文案和配色」。** 否则你会得到一个四不像：别人的文案、别人的主色，唯独不像你自己。

兜底一条：AI 工具没有联网能力，就把 2 个你喜欢的官网链接贴给它，让它先拆解结构再写。**「先拆再写」比「直接写」稳定一个量级。**

AI 研究 UI 参考资料：

- [Awwwards 获奖网站集合 -- Awwwards](https://www.awwwards.com/) ⭐值得阅读
- [Dribbble 设计作品与搜索 -- Dribbble](https://dribbble.com/) ⭐值得阅读
- [SiteInspire 网页设计灵感库 -- SiteInspire](https://www.siteinspire.com/)

## 7. 完整可运行代码（Runnable Demo）

下面这段是完整可运行版（精简掉了注释与部分 hover 细节，视觉与开头资源里的完整版一致）。复制 → 记事本 → 另存为 `index.html`（编码选 UTF-8）→ 双击，就能看到整页。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width,initial-scale=1">
<title>云图设计 | 让品牌被看见</title>
<style>
  :root{--ink:#0b1020;--body:#4a5468;--line:#e6eaf2;--bg:#f6f8fc;--brand:#4f7cff;--brand2:#7c5cff}  /* 6 个色值即整套皮肤 */
  *{box-sizing:border-box;margin:0;padding:0}                                                       /* 统一盒模型，宽度含内边距 */
  body{font-family:-apple-system,"Segoe UI","PingFang SC","Microsoft YaHei",sans-serif;color:var(--ink);line-height:1.65}
  a{color:inherit;text-decoration:none}                                                              /* 链接继承颜色、去下划线 */
  .wrap{max-width:1120px;margin:0 auto;padding:0 24px}                                               /* 全站共用内容容器 */
  header{position:sticky;top:0;background:rgba(255,255,255,.85);backdrop-filter:blur(12px);border-bottom:1px solid var(--line)}
  .nav{display:flex;align-items:center;justify-content:space-between;height:68px}
  .logo{display:flex;align-items:center;gap:10px;font-weight:700}
  .logo i{width:26px;height:26px;border-radius:8px;background:linear-gradient(135deg,var(--brand),var(--brand2))}
  nav ul{display:flex;gap:28px;list-style:none;font-size:15px;color:var(--body)}
  .btn{display:inline-flex;align-items:center;height:46px;padding:0 24px;border-radius:10px;font-size:15px;font-weight:600}
  .btn-main{background:linear-gradient(135deg,var(--brand),var(--brand2));color:#fff}
  .btn-line{border:1px solid var(--line)}
  .hero{padding:84px 0 96px}
  .hero .wrap{display:grid;grid-template-columns:1.05fr .95fr;gap:56px;align-items:center}           /* 首屏两栏 */
  .tag{display:inline-block;padding:6px 14px;border-radius:999px;background:rgba(79,124,255,.1);color:var(--brand);font-size:13px;font-weight:600}
  h1{font-size:clamp(34px,4.6vw,56px);line-height:1.15;letter-spacing:-1px;margin:20px 0 18px}        /* clamp：字号随屏幕自适应 */
  h1 em{font-style:normal;background:linear-gradient(120deg,var(--brand),var(--brand2));-webkit-background-clip:text;background-clip:text;color:transparent}
  .hero p{font-size:17px;color:var(--body);max-width:460px}
  .actions{display:flex;gap:12px;margin-top:30px}
  .visual{position:relative;height:340px;border-radius:24px;background:linear-gradient(150deg,#dfe8ff,#efe6ff 60%,#fff);overflow:hidden}
  .glass{position:absolute;left:34px;right:34px;top:48px;padding:20px;border-radius:16px;background:rgba(255,255,255,.75);border:1px solid #fff;box-shadow:0 18px 40px rgba(30,50,120,.14)}
  .bar{height:8px;border-radius:4px;background:#e8ecf7;margin:9px 0}                                  /* 占位条：代替真实截图 */
  .bar.s{width:62%}
  .section{padding:88px 0}
  .alt{background:var(--bg)}                                                                          /* 交替底色，区块自带分隔 */
  .head{max-width:620px;margin-bottom:44px}
  h2{font-size:clamp(26px,3vw,34px);letter-spacing:-.6px;margin-bottom:12px}
  .head p{color:var(--body)}
  .grid3{display:grid;grid-template-columns:repeat(3,1fr);gap:22px}                                   /* 三卡等宽 */
  .card{background:#fff;border:1px solid var(--line);border-radius:16px;padding:26px}
  .num{font-size:13px;font-weight:700;color:var(--brand);letter-spacing:1px}
  .card h3{font-size:19px;margin:14px 0 8px}
  .card p{font-size:14.5px;color:var(--body)}
  .stats{background:var(--ink);color:#fff;padding:56px 0}                                              /* 深色横带：放证明 */
  .stats .wrap{display:grid;grid-template-columns:repeat(3,1fr);gap:24px;text-align:center}
  .stats b{display:block;font-size:clamp(28px,3.4vw,40px);letter-spacing:-1px}
  .stats span{font-size:14px;color:rgba(255,255,255,.62)}
  .cta-box{margin:88px auto;max-width:1120px;border-radius:24px;padding:60px 32px;text-align:center;background:linear-gradient(135deg,var(--brand),var(--brand2));color:#fff}
  .cta-box p{color:rgba(255,255,255,.86);margin:12px 0 26px}
  .cta-box .btn{background:#fff;color:var(--brand)}                                                    /* 渐变底上用反色按钮 */
  footer{padding:40px 0;border-top:1px solid var(--line);font-size:14px;color:var(--body)}
  footer .wrap{display:flex;justify-content:space-between;flex-wrap:wrap;gap:12px}
  @media(max-width:900px){                                                                             /* 手机断点：全部塌单列 */
    .hero .wrap,.grid3,.stats .wrap{grid-template-columns:1fr}
    nav ul{display:none}
    .hero{padding:48px 0 64px}
    .visual{height:280px}
    .section{padding:60px 0}
    .cta-box{margin:56px 20px}
  }
</style>
</head>
<body>
<header><div class="wrap nav">
  <a class="logo" href="#top"><i></i>云图设计</a>
  <nav><ul><li><a href="#service">服务</a></li><li><a href="#proof">案例</a></li><li><a href="#contact">联系</a></li></ul></nav>
  <a class="btn btn-main" href="#contact">预约咨询</a>
</div></header>

<section class="hero" id="top"><div class="wrap">
  <div>
    <span class="tag">品牌视觉 · 官网设计</span>
    <h1>让中小品牌的<em>第一眼</em>，就有专业感</h1>
    <p>把一款产品、一家门店、一个工作室，做成一张能自己说话的网页。</p>
    <div class="actions"><a class="btn btn-main" href="#contact">免费看方案</a><a class="btn btn-line" href="#service">看看怎么做的</a></div>
  </div>
  <div class="visual"><div class="glass"><b>首页结构预览</b><div class="bar"></div><div class="bar s"></div><div class="bar s"></div></div></div>
</div></section>

<section class="section alt" id="service"><div class="wrap">
  <div class="head"><h2>三件事，做到位就够了</h2><p>不堆功能，不加花活：首屏、结构、入口，三块把话说清楚。</p></div>
  <div class="grid3">
    <div class="card"><div class="num">01</div><h3>首屏定调</h3><p>一句主标题、一句副标题、一个按钮，三秒说清你是做什么的。</p></div>
    <div class="card"><div class="num">02</div><h3>结构讲清</h3><p>服务、案例、价格按顺序排，访客自己往下读，不用猜。</p></div>
    <div class="card"><div class="num">03</div><h3>入口收口</h3><p>每个区块后面留一个联系入口，想咨询的人随时能找到你。</p></div>
  </div>
</div></section>

<section class="stats" id="proof"><div class="wrap">
  <div><b>120+</b><span>已交付的官网</span></div>
  <div><b>7 天</b><span>从需求到上线</span></div>
  <div><b>98%</b><span>客户复购或转介绍</span></div>
</div></section>

<section id="contact"><div class="cta-box">
  <h2>先把你的想法说给我们听</h2>
  <p>留个邮箱，48 小时内给你一页结构草案，不收费。</p>
  <a class="btn" href="mailto:hello@example.com">hello@example.com</a>
</div></section>

<footer><div class="wrap">
  <span>© <span id="year">2026</span> 云图设计 · 保留所有权利</span>
  <span>hello@example.com · 周一至周五 10:00–19:00</span>
</div></footer>

<script>
  const header = document.querySelector('header');                                  // 取导航条
  addEventListener('scroll', () => {                                                // 监听页面滚动
    header.style.background = scrollY > 8 ? 'rgba(255,255,255,.95)' : 'rgba(255,255,255,.85)';  // 滚动后底色变实
  });
  document.getElementById('year').textContent = new Date().getFullYear();            // 页脚年份自动更新
</script>
</body>
</html>
```

这段代码实测的几个数字（你可以自己复算）：文件 **13.6 KB**、**6 个语义区块**、**0 个外部请求**（无 CDN、无外链图片、无外部字体）、控制台 **0 条报错**；1440px 与 390px 两种宽度下 `scrollWidth` 均等于 `clientWidth`，即**没有任何横向滚动条**。视觉区的圆球、渐变卡、占位条全部由 CSS 画出，所以断网也能完整显示。

## 8. 桌面上怎么双击打开（Open Locally）

**① 先把扩展名显示出来。** Windows 默认隐藏已知扩展名，这是「我明明存成 html 却变成 txt」的头号原因。打开任意文件夹 → 顶部「查看」→ 勾选「文件扩展名」（Win11 在「查看 → 显示 → 文件扩展名」）。

**② 新建文件夹 `website`。** 建议放桌面。所有图片以后都放这个文件夹里的 `images` 子文件夹，整个文件夹就是一个网站。

**③ 用记事本保存。** 代码粘贴进记事本 → 文件 → 另存为 → **文件名填 `index.html`**（带引号更保险）→ **保存类型选「所有文件」** → **编码选 UTF-8** → 保存。文件名必须是 `index.html`，因为浏览器打开文件夹时默认找它。

**④ 双击。** 图标变成浏览器图标后双击，就能在默认浏览器里打开。想换浏览器：右键 → 打开方式 → 选 Chrome 或 Edge → 勾「始终使用此应用」。

**⑤ 打不开 / 白屏，只查这 5 条。** 下面这张表覆盖了几乎所有情况：

| 现象 | 原因 | 解法 |
|---|---|---|
| 文件名显示成 `index.html.txt` | 系统隐藏了扩展名，你多打了一次 | 先开「文件扩展名」，再重命名为 `index.html` |
| 双击后用记事本打开了 | `.html` 的默认程序被设成了记事本 | 右键 → 打开方式 → Chrome/Edge → 始终使用 |
| 页面一片白 | 文件是空的，或编码选错中文全乱 | 打开文件确认有代码；另存为时选 UTF-8 |
| 排版全乱、像纯文本 | `style` 标签没闭合，或复制时被截断 | 检查 `</style>` 与 `</html>` 是否在文件末尾 |
| 图片全是裂图 | AI 给了 `C:\...` 绝对路径或 `https://` 外链 | 图片放 `images/`，路径改成 `images/a.jpg` |
| 浏览器控制台报 CORS 错误 | 代码里用了 `fetch()` 读本地文件 | 让 AI 把数据直接写成 JS 数组，删掉 `fetch` |

最后一条值得单独说：本地双击打开走的是 `file://` 协议，浏览器出于安全限制，**不允许它用 `fetch()` 去读同目录的文件**，控制台会报 `CORS request not HTTP`（详见 [MDN 的说明](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Guides/CORS/Errors/CORSRequestNotHttp)）。小白阶段最简单的处理就是：**别让 AI 用 `fetch`**，需要展示的数据直接写进 JS 数组里。

**⑥ 想发给别人。** 右键 `website` 文件夹 → 发送到 → 压缩文件夹，把 zip 发过去。对方解压后双击同一个 `index.html` 即可。这一步能成立的前提，正是第 4 节第 ⑤ 格要求的「单文件 + 零外链」。

本地打开与 CORS 参考资料：

- [CORS request not HTTP（本地文件跨域报错说明） -- MDN](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Guides/CORS/Errors/CORSRequestNotHttp) ⭐值得阅读
- [跨源资源共享（CORS）总览 -- MDN](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/CORS)

## 9. 对照表：症状 → 原因 → 解法（Troubleshooting）

| 症状 | 原因 | 解法 |
|---|---|---|
| AI 生成的页面像十年前的模板 | 提示词只有公司简介，没有结构与风格 | 补第 4 节的六格清单，先给区块和文案 |
| 页面越改越乱、颜色越来越多 | 一次性要整站，后半段丢失上下文 | 分三段生成：骨架 → 首屏 → 手机端 |
| 说「大气一点」毫无变化 | 风格词不可判定 | 换成数字：内容区 1120px、间距 88px、主色 1 个 |
| 手机上文字挤成一列 | 没写断点，AI 默认不做响应式 | 提示词加「900px 以下塌成单列」 |
| 双击打开是白屏 | 扩展名多了一层 `.txt` | 显示扩展名后重命名为 `index.html` |
| 换台电脑图片全丢 | 用了绝对路径或远程图片链接 | 图片进 `images/`，路径写相对路径 |
| 发给别人打开是源码 | 对方没有默认浏览器关联 | 让对方右键 → 打开方式 → 选浏览器 |

**三个最常见的踩坑**，都跟技术无关：

1. **一次让它写完整个网站。** 800 行输出到后半段，它开始自由发挥：导航两套、按钮三种圆角。分段生成是给每段留一个可检查的边界。
2. **只说「参考 XX 网站」不说边界。** 结果连文案和配色一起搬，做出来像盗版。正确说法是「只参考版式结构和信息密度，文案、配色、图标全部重做」。
3. **用 AI 给的远程图片链接。** 那些 `https://images.unsplash.com/...` 一断链、或对方断网，页面立刻一片裂图。**能不用图就不用图**，渐变、色块、内联 SVG 够撑起一个首页。

## 10. 发布前验收清单（Checklist）

把下面 6 条抄给 AI，让它逐条回答「是 / 否」，你只核对结果：

- [ ] 只输出一个 `index.html`，CSS 与 JS 全部内联
- [ ] 没有任何 `http://` 或 `https://` 的资源引用（链接跳转除外）
- [ ] 1440px 与 390px 下都没有横向滚动条
- [ ] 全站 1 个主色 + 1 个辅色，字阶不超过 4 级
- [ ] 整页主按钮不超过 3 个，每屏最多 1 个
- [ ] 断网状态下刷新，页面依然完整（证明零外链）

有品牌文案、有产品图，就走「首屏两栏 + 满屏视觉」；只有公司名和一个电话，就把六块压到四块，用留白和字号层级撑住第一屏。**官网好不好看，从来不是素材多少决定的，是结构清不清楚决定的。**
