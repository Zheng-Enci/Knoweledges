# 为什么苹果的圆角更高级：连续曲率圆角 Squircle 从超椭圆到 CSS 实现的完全讲解

> **核心结论**：你让 AI 做卡片、把圆角数值调到和苹果一致，看着却还是「更硬」，毛病出在**直线拐进圆弧的那个接口**——普通圆角是「直线直接接上 1/4 圆弧」，在接口处曲率从 0 瞬间跳到最大，像开车进弯时方向盘一下打死；而苹果用的是**连续曲率圆角（squircle）**，从直线开始一点点弯进去、过弯心再慢慢回正，全程曲率平滑过渡，视觉上柔和得多。这个形状的数学本质是**超椭圆（superellipse）**，公式 $|x/a|^n + |y/b|^n = 1$，其中 $n=4$ 的等轴情形就是 squircle。2013 年 iOS 7 把图标换成这种形状，2018 年 Figma 工程师专门写了长文研究怎么还原它——如今网页有了新写法 `corner-shape: squircle`，Chrome 已经能用，让 AI 做界面时**直接点名「圆角要用连续曲率」**，别只说「圆角大一点」。

## 目录

- 1. 一句话结论
- 2. 毛病出在哪：直线接圆弧的接口
- 3. 曲率突变（Curvature Discontinuity）：为什么普通圆角「硬」
- 4. 连续曲率（Continuous Curvature）：苹果圆角「柔」的真相
- 5. 数学本质：超椭圆 Superellipse
- 6. 历史脉络：从 iOS 7 到 Figma 的还原
- 7. 让 AI 做对：别只说「圆角大一点」
- 8. 网页实现：corner-shape 新写法
- 9. 完整可运行代码（CSS + SVG 演示）
- 10. 对照表：症状 → 原因 → 解法
- 11. 判断收尾

## 1. 一句话结论

先建立一个直觉 🎭：**普通圆角像「开车到路口突然把方向盘打死」**，乘客会被甩一下；**连续曲率圆角像「老司机提前减速、慢慢打方向、过了弯心再回正」**，全程平稳。这个「甩不甩一下」的差别，就是苹果圆角看起来更高级的全部秘密。

所以记住三件事：

- **病根**：普通圆角在「直线 ↔ 圆弧」的接口处，曲率从 0 瞬间跳到最大，视觉上「硬」。
- **解药**：连续曲率圆角让曲率平滑过渡，视觉上「柔」，数学上叫超椭圆（superellipse）。
- **落地**：网页用 `corner-shape: squircle`，给 AI 下指令时直接说「连续曲率圆角」。

一句话：**圆角好不好看，不只看半径大小，更看曲率怎么变**——这就是苹果和「普通 AI 卡片」的分水岭。

## 2. 毛病出在哪：直线接圆弧的接口

先看普通圆角是怎么画出来的：

- 一个普通圆角，就是**一条直线直接接上 1/4 个圆弧**，半径多大，圆弧就多圆。
- 数学上，**直线的曲率是 0**（它不弯），**圆弧从第一个点起曲率就是最大**（它恒定地弯）。
- 于是在「直线 ↔ 圆弧」的这个接口点，**曲率一下从 0 跳到了最大值**——这就是「硬」的根源。

你让 AI 把卡片圆角调大、调高级，它只会把半径改大——但**接口那一下突变还在**，所以数值一样、看着还是比苹果硬。

用类比 🎭：**普通圆角像「笔直的马路突然接一个直角弯」**，无论弯道画多圆，进弯那一刻方向都是猛地一转；你觉得它不顺，不是弯不够圆，是**从直变弯的那一下太突然**。

> ⚠️ 关键认知：**圆角半径只决定「弯多大」，不决定「弯得多平滑」。** 半径再大，只要接口处曲率突变，视觉上就是「硬」。

## 3. 曲率突变（Curvature Discontinuity）：为什么普通圆角「硬」

这一节讲清楚「硬」的数学机制，不用怕，很直观。

**曲率（curvature）** 衡量一条线「弯得有多厉害」：直线曲率是 0，圆弧曲率是常数（等于半径的倒数 $1/r$）。

普通圆角在接口处的变化是：

- 直线段：曲率 = 0（不弯）
- 进入圆弧瞬间：曲率 = $1/r$（立刻弯到最大）

这中间**没有过渡**，曲率从 0 直接跳到 $1/r$，数学上叫**曲率不连续（curvature discontinuity）**，也叫 $G^1$ 连续（只保证切线方向连续，不保证曲率连续）。

- $G^1$ 连续：只保证「方向」平滑（切线方向），但「弯的加速度」会突跳。
- 人眼能分辨这种「加速度突变」——所以普通圆角即使半径大，仍显得生硬。

用开车类比 🎭：**曲率就是「方向盘的角度」**。普通圆角是「方向盘瞬间从 0 打到最大」，乘客被甩一下；这就是为什么它「硬」。

## 4. 连续曲率（Continuous Curvature）：苹果圆角「柔」的真相

苹果的圆角，解决的就是这个「曲率突变」。它是**连续曲率圆角（continuous curvature corner）**，官方也叫 squircle（Square + Circle，方加圆）。

它的画法完全不同：

- **从直线开始一点点弯进去**：接口处曲率从 0 逐渐增大，而不是瞬间跳满。
- **过了弯心再一点点回正**：曲率逐渐归 0，平稳接回直线。
- 全程曲率连续变化，数学上达到 $G^2$ 连续（切线方向 + 曲率都连续）。

这和现实世界的工程做法一模一样：**铁路和高速公路修弯道，都要先接一段「慢慢变弯的过渡曲线」**（如缓和曲线），而不是直接进圆弧——就是为了让乘客不被甩、火车不脱轨。

用类比 🎭：**连续曲率圆角是「老司机进弯」**，提前减速、匀速打方向、出了弯再慢慢回正；全程平稳，乘客根本感觉不到转弯的「卡顿」。

> 💡 所以苹果圆角的「高级感」，本质是**把物理学里的「平滑过渡」原则用在了视觉上**——眼睛和身体一样，讨厌「突然的加速度变化」。

## 5. 数学本质：超椭圆 Superellipse

连续曲率圆角的数学形状，来自**超椭圆（superellipse）**——也叫 Lamé 曲线（由法国数学家加布里埃尔·拉梅提出）。公式：

$$|x/a|^n + |y/b|^n = 1$$

- $a$、$b$ 是水平、垂直半轴长；
- $n$ 是指数，决定了形状：
  - $n = 2$：标准椭圆（$a=b$ 时是圆）
  - $n > 2$：带圆角的正方形 / 矩形（指数越大角越方）
  - $n \to \infty$：退化成纯方形

而 **squircle 是 $a = b$ 且 $n = 4$** 的特殊情形——这就是 iOS 图标、Figma 平滑圆角的数学原型。

为什么 $n=4$ 就能实现「连续曲率」？因为当 $n > 2$ 时，超椭圆在轴交点（$x=\pm a$、$y=0$ 等）处的**曲率精确为 0**，所以它和直线边相接时**天然达到 $G^2$ 连续**，不需要额外构造过渡段——这就是「连续曲率圆角」的数学基础。

用类比 🎭：**超椭圆像「圆的表亲」**，指数 $n$ 就是那个「表亲的圆润度旋钮」——调到 4，就是苹果那种「方中带圆、圆中带方」的舒服形状。

参考资料：
- [What is a Squircle? -- Squircle.js](https://squircle.js.org/blog/what-is-a-squircle) ⭐值得阅读
- [The Squircle Formula: Superellipse Math Explained -- Squircle.js](https://squircle.js.org/blog/math-behind-squircles) ⭐值得阅读

## 6. 历史脉络：从 iOS 7 到 Figma 的还原

连续曲率圆角不是新发明，但它近十年在界面设计里掀起过两次高潮：

- **2013 年，iOS 7**：苹果把图标换成了 squircle 形状，设计师很快注意到它和普通圆角不一样——「数值一样，看着就是更顺」。
- **2018 年，Figma 工程师写长文**：专门研究怎么还原苹果的圆角。他们先试了超椭圆公式，发现**对不太上**（苹果用的不是单一超椭圆，而是每个角用一段曲线去贴合）。
- **最后方案**：Figma 用**分段曲线**逐角拟合苹果形状——**这就是你在 Figma 里看到的「圆角平滑滑块」的来源**。

这个历史告诉我们两件事：

1. **苹果的形状是「定制曲线」，不是简单公式**——想完美复刻，要分段拟合。
2. **但「连续曲率」是它的本质特征**——理解了这一点，你用超椭圆近似也能做出 90% 的效果。

> 💡 对普通设计师 / AI 使用者的启示：**不需要精确复刻苹果，只要做到「曲率连续」，视觉上就比普通圆角高级一个档次**。

参考资料：
- [Apple 连续曲率与同心圆角：CSS、SwiftUI、Tailwind 元件实作 -- ZeroOne](https://laplusda.com/posts/apple-continuous-corners-concentric-radius-tailwind/) ⭐值得阅读

## 7. 让 AI 做对：别只说「圆角大一点」

这一点是给「用 AI 做界面」的人最实用的建议。AI 默认做页面时，圆角就是普通圆角——直线接圆弧。

- 你跟 AI 说「圆角大一点」→ 它只会把 `border-radius` 半径调大，**接口那一下突变还在**。
- 你跟 AI 说「圆角高级一点」→ 它仍然只会改半径，因为它不知道「高级」指的是「曲率连续」。
- 正确做法：**直接点名「圆角要用连续曲率」**——这个词足够明确，AI 能理解并去实现。

同样地，做苹果手机 App：

- **苹果开发工具（Xcode / SwiftUI）里就有这个选项**，官方说法就叫**连续曲率圆角（continuous corner radius）**。
- 自己用设计工具时，**把圆角和平滑滑块往上拉**——Figma 的平滑滑块、或对应工具的 continuous corner 选项。
- 网页端则用下面第 8 节的 `corner-shape: squircle`。

用类比 🎭：**给 AI 下指令像「给装修师傅讲需求」**——你说「刷白一点」，他只会多刷几遍白漆；你说「要乳胶漆的哑光质感」，他才懂怎么调。**「连续曲率」就是那个能让 AI 真正听懂的关键词**。

## 8. 网页实现：corner-shape 新写法

网页上实现连续曲率圆角，有个**新 CSS 写法**，名字就叫 **squircle**（方 + 圆）。

- 核心是新增的 **`corner-shape`** 属性，它控制角落的**几何形状**，而 `border-radius` 继续控制**大小**。
- 关键值：`corner-shape: squircle`（squircle 形状）或 `corner-shape: superellipse(...)`（指定超椭圆指数）。
- **浏览器支持**：Chrome 已经能用；Safari（苹果）还在测试版。
- **优雅降级**：不支持的浏览器会自动退回普通圆角，**页面不会坏**——所以可以放心用，只是高级效果只在支持的浏览器里显示。

> ⚠️ 注意：`border-radius` 单独设置时**永远画的是圆弧**（圆或椭圆弧），它没法自己变成 squircle；`corner-shape` 才是改「形状」的关键。如果半径是 0，单独设 `corner-shape` 也没效果。

一个实用细节：**同样的数值，squircle 看着会更「方」一点**，因为超椭圆在角附近的曲率是渐变的、不像圆弧那么「圆鼓鼓」。所以用 squircle 时，**数值可以比普通圆角加大一点**，视觉上才更接近你习惯的圆润度。

参考资料：
- [Squircles in CSS: corner-shape, superellipse() and Browser Support -- Squircle.js](https://squircle.js.org/blog/squircles-in-css) ⭐值得阅读
- [border-radius CSS property -- MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/border-radius)

## 9. 完整可运行代码（Runnable Code）：CSS + SVG 演示

下面是一段**可直接跑的完整代码**，用一个 HTML 页面对比普通圆角与连续曲率圆角（squircle），并附一个手绘的超椭圆 SVG，让你直观看到「曲率突变 vs 曲率连续」的差别。保存为 `squircle.html`，浏览器打开即可。

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
<meta charset="UTF-8">
<title>连续曲率圆角 Squircle 演示</title>
<style>
  body { font-family: sans-serif; display: flex; gap: 40px; padding: 40px; }
  .card { width: 160px; height: 160px; display: flex;
          align-items: center; justify-content: center; color: #fff;
          font-weight: bold; text-align: center; }
  .normal { background: #999; border-radius: 32px; }            /* 普通圆角：直线接圆弧，接口处曲率突变 */
  .sq     { background: #ff4d2e; border-radius: 48px;           /* 连续曲率：数值更大，视觉更"方"，曲率平滑 */
            corner-shape: squircle; }                           /* Chrome 支持；不支持则优雅退回普通圆角 */
</style>
</head>
<body>
  <div>
    <div class="card normal">普通圆角<br>曲率突变</div>
    <p>border-radius: 32px</p>
  </div>
  <div>
    <div class="card sq">Squircle<br>连续曲率</div>
    <p>corner-shape: squircle<br>border-radius: 48px</p>
  </div>
</body>
</html>
```

**怎么读这段代码**：`.normal` 只用 `border-radius`，是普通圆角——接口处曲率从 0 突变到 $1/r$；`.sq` 加了 `corner-shape: squircle`，并为了补偿「squircle 显得更方」把半径从 32 加大到 48。在 Chrome 里打开，你会明显感到右侧的卡片「更顺、更接近苹果」；用不支持的浏览器打开，它只是退回普通圆角，页面不坏——这就是第 8 节讲的「优雅降级」。

## 10. 对照表：症状 → 原因 → 解法

| 症状 | 原因 | 解法 |
|------|------|------|
| 圆角数值调到和苹果一样，看着还是硬 | 普通圆角直线接圆弧，接口处曲率突变 | 换成连续曲率圆角（squircle） |
| 让 AI 做卡片，说「圆角大一点」还是不好看 | AI 只会改半径，接口突变还在 | 直接点名「圆角要用连续曲率」 |
| 网页圆角想做成苹果那种 | border-radius 只能画圆弧 | 用 corner-shape: squircle |
| 用 squircle 后觉得太「方」 | 超椭圆比圆弧更方 | 把 border-radius 数值加大一点 |
| 担心新写法浏览器不支持 | corner-shape 是新技术 | 不支持的自动退回普通圆角，页面不坏 |

## 11. 判断收尾

**什么时候该用连续曲率圆角**：你在做「对视觉质感有要求」的界面——App 图标、卡片、按钮、品牌感强的页面，且你的浏览器 / 环境支持（Chrome）或愿意接受优雅降级。**什么时候不必纠结**：你是做纯功能性后台、数据密集型页面，圆角只起轻微装饰作用——此时普通 `border-radius` 完全够用，不必为这点视觉差异引入新技术。判断标准只有一条：**这个圆角是不是用户视觉注意的焦点**——是，就值得上 squircle；不是，普通圆角即可。

本专栏《全栈开发》覆盖前后端工程、UI 设计与开发工具链，每篇都配可直接运行的代码与实战讲解，持续更新。想在界面与工程细节上少走弯路，可在专栏页订阅。

参考资料（综合）：
- [What is a Squircle? -- Squircle.js](https://squircle.js.org/blog/what-is-a-squircle) ⭐值得阅读
- [The Squircle Formula: Superellipse Math Explained -- Squircle.js](https://squircle.js.org/blog/math-behind-squircles) ⭐值得阅读
- [Squircles in CSS: corner-shape, superellipse() and Browser Support -- Squircle.js](https://squircle.js.org/blog/squircles-in-css) ⭐值得阅读
- [Apple 连续曲率与同心圆角：CSS、SwiftUI、Tailwind 元件实作 -- ZeroOne](https://laplusda.com/posts/apple-continuous-corners-concentric-radius-tailwind/) ⭐值得阅读
- [border-radius CSS property -- MDN](https://developer.mozilla.org/en-US/docs/Web/CSS/Reference/Properties/border-radius)
