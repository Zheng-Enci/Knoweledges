# AI Agent 时代前端项目怎么组织：按页面纵向切块，替代按类型分层目录

> **核心结论**：传统前端的 `components/`、`styles/`、`hooks/`、`utils/` 是按类型横向分层，改一个页面的交互要在四五个目录之间来回跳。AI Agent 时代更合适的做法是**按页面纵向切块（Vertical Slice，纵向切片）**：一个 URL 对应一个页面目录，页面结构、页面 CSS、页面 JS 全放里面，页面之间互不引用；只允许三类内容跨页共享——API 服务层、通用主题样式、全局消息提示。按 20 个页面、每页 5 个文件的仓库估算，一次修改要读的文件从 **8 个降到 3 个**，降幅 **62.5%**。代码量短期会变大，但修改者已经从人换成了 AI，读文件数与上下文占用才是真正的成本。

---

## 目录

- 1. 结论先行：按页面纵向切块
- 2. 横向分层在 AI 手里为什么变慢
- 3. 新结构长什么样
- 4. 共享层只留三类
- 5. 一笔可算的账：8 个文件降到 3 个
- 6. 代码量短期变大，长期为什么变小
- 7. 一份可直接运行的纵向切片
- 8. 症状 → 原因 → 解法对照表
- 9. 五个落地坑
- 10. 判据：该切还是不该切

---

## 1. 结论先行：按页面纵向切块（Vertical Slice）

先说结论，再解释为什么。

**组织轴从「文件类型」换成「业务页面」**。以前是「所有组件放一处、所有样式放一处」，现在是「首页的一切放一处、订单页的一切放一处」。判断标准只有一条：改一个页面，要不要打开别的页面的目录？不该。

**共享层收敛成白名单**。只有三样东西可以跨页：调用后端的 API 服务层、通用主题样式（theme）、全局消息提示（toast）。白名单之外出现第四个共享物，就要问一句「它到底是共享，还是这一页自己的事」。

**修改半径从「仓库」缩到「目录」**。哪里有问题就改哪里，AI 只需要读出现问题的那个目录，外加一到两个共享文件。

这个思路在业界叫 vertical slice architecture（纵向切片架构），也被称为 feature-based（按功能）组织，和 type-based（按类型）组织是两条正交的路。它不是新发明，但在「修改者是 AI」这个前提下，收益结构发生了变化——人改代码看的是**仓库好不好维护**，AI 改代码看的是**一次任务要读多少文件**。两者的最优解不一样。

引入这个思路的参考资料：
- [Architecture Patterns for AI Coding: Why Your File Structure Matters More Than Your Prompts](https://www.rasmuswiding.com/blog/architecture-patterns-for-ai-coding/) ⭐值得阅读
- [The Perfect Folder Structure for Scalable Frontend](https://feature-sliced.design/zh/blog/frontend-folder-structure)
- [Scaling Next.js for Enterprise](https://marabesi.com/web/ecosystems/nextjs/scaling-nextjs-for-enterprise.html)

---

## 2. 横向分层在 AI 手里为什么变慢（Type-based Layering）

横向分层的原始动机是复用：同一个按钮组件，十个页面共用一份，改一次全站生效。在人写代码的年代，这个账算得过来——人改一次按钮，成本是「找到它 + 改它」，而找到它这个动作，人靠记忆和 IDE 的跳转就够了。

问题在于，AI 没有记忆，只有上下文窗口（context window）。它要找的东西不会自动浮现，必须**被读进来**才算知道。这就让「文件散落在哪里」从一个导航问题，变成了一个**成本问题**。

看一个具体场景：订单页上「取消订单」按钮点下去没反应。

按类型分层的仓库里，这条链路横跨五个目录：

1. `routes/orders.tsx` —— 页面结构，按钮挂在哪
2. `components/Button.tsx` —— 按钮组件本身
3. `hooks/useCancelOrder.ts` —— 点击后的逻辑
4. `api/order.ts` —— 真正发请求的地方
5. `styles/orders.css` —— 按钮的禁用态样式

AI 要判断问题在哪，最稳妥的做法是把这五个都读一遍，再外加全局的消息提示和主题变量。这就是 7 到 8 个文件。每个文件都不大，但**它们之间没有信息边界**——你无法从目录结构看出「哪些文件属于订单页」，只能靠文件名猜。

打个比方 🍱：横向分层像一个按材料分类的仓库，所有螺丝在一号货架、所有木板在二号货架、所有油漆在三号货架。你要装一把椅子，得跑遍五个货架；装完之后剩下的边角料，也不知道该退回哪个货架。纵向切块则是**按菜品的备料盒**：一个盒子装一道菜的全部材料，厨师伸手就拿，用完整个盒子扔掉。

---

## 3. 新结构长什么样（Directory Layout）

一棵典型的纵向切片目录树：

```text
src/
├── pages/                        # 页面层：一个 URL 一个目录，彼此不引用
│   ├── home/
│   │   ├── page.js               # 首页的结构 + 逻辑
│   │   ├── page.css              # 首页的样式，只作用于首页
│   │   └── page.test.js          # 首页自己的测试
│   ├── orders/
│   │   ├── page.js               # 订单页的结构 + 逻辑
│   │   ├── page.css              # 订单页的样式
│   │   └── page.test.js
│   └── settings/
│       ├── page.js
│       └── page.css
├── shared/                       # 共享层：白名单，只有三类
│   ├── api/                      # ① 后端接口调用
│   │   ├── order.js
│   │   └── user.js
│   ├── theme.css                 # ② 主题变量与全局重置
│   └── toast.js                  # ③ 全局消息提示
└── router.js                     # 路由表：URL → 页面目录，集中维护
```

三个约束撑起这棵树：

**一页一目录**。`pages/orders/` 里所有文件的职责都是「让订单页跑起来」，不存在一个文件同时服务三个页面。页面之间**禁止互相 import**，需要共用就去共享层，或者干脆各写一份。

**样式就近同置（colocation，同置）**。`page.css` 和 `page.js` 放在同一个目录，改样式的时候不需要猜它在哪个 styles 文件里，也不会误伤别的页面——因为这份 CSS 只被这一页引入。

**路由表独立**。`router.js` 是唯一知道「有哪些页面」的地方。加一个页面 = 加一个目录 + 加一行路由；删一个页面 = 删一个目录 + 删一行路由，不会留下孤儿样式和孤儿 hook。

这个结构下，「取消订单按钮没反应」的排查半径是：`pages/orders/page.js` + `shared/api/order.js`，最多再看一眼 `shared/toast.js`。

---

## 4. 共享层只留三类（Shared Layer Boundary）

纵向切块最容易被搞坏的地方，就是共享层。第一个页面写完后，总会有人说「这个格式化函数三个页面都要用，放 shared 吧」，第二个、第三个接踵而至，半年后 `shared/utils/` 又长成了一个新的 `utils/`。

所以共享层必须是**白名单制**，只有三类：

| 类别 | 放什么 | 为什么必须共享 |
|---|---|---|
| API 服务层 | 请求封装、接口定义、错误码映射 | 后端契约只有一份，各页各写一份必然不一致 |
| 通用主题 | CSS 变量、字体、间距、明暗主题 | 全站视觉要统一，只能有一个事实来源 |
| 全局消息提示 | toast、confirm、loading 遮罩 | 同时只能有一个提示在屏幕上，天然是全局的 |

白名单之外的第四类东西想进共享层，先过三道问号：

1. **它是不是只有两三页在用？** 是的话，宁可复制两份。三份以上再考虑提取。
2. **它会不会因为某一页的需求而改？** 会的话，说明它不是通用能力，是那一页的业务逻辑。
3. **删掉它，需要在几个目录里改代码？** 如果答案是「十几个」，那它已经变成了横向耦合，不是共享。

这条线叫 rule of three（三次法则）：第一次直接写，第二次复制，第三次才抽象。人写代码时这条法则常被当成风格建议，AI 时代它是**成本纪律**——共享层每多一个文件，每个相关页面的一次修改就多读一个文件，而读取是 AI 唯一的开销。

主题样式这一层单独说一句：它会和按页样式共存，顺序必须是**先主题、后页面**，否则页面样式里的变量引用拿不到值。这套分层在[前端项目为什么需要一份统一的 theme.css](https://juejin.cn/post/7656270771610370075) 里有完整实现，本篇只强调边界——主题只放变量和重置，不放任何具体页面的类名。

---

## 5. 一笔可算的账：8 个文件降到 3 个（Context Locality）

「AI 改得更快」这句话如果没有数字，就只是一句口号。下面这笔账可以自己复算。

**假设**（写清楚前提，数字才有意义）：

- 仓库有 20 个页面；
- 每页相关文件 5 个，按类型散在 `routes/`、`components/`、`hooks/`、`api/`、`styles/` 五个目录；
- 共享文件 3 个（主题、提示、一个公共工具）；
- 平均每个文件 120 行、约 1200 token（Token，模型计费与上下文的最小单位）。

**按类型分层**：改一处页面交互，稳妥做法是读 5 个页面相关文件 + 3 个共享文件 = **8 个文件**，约 9600 token。

**纵向切块**：同一个改动，读本页的 `page.js` 和 `page.css`，再读一个相关的 `shared/api/order.js` = **3 个文件**，约 3600 token。

降幅：

$$
\frac{8 - 3}{8} = 62.5\%
$$

token 占用从 9600 降到 3600，省下 6000。这个数字的意义不在于精确，而在于它**可以被质疑和修正**：如果你每页只有 3 个文件，降幅就会变小；如果每页散在 8 个目录里，降幅会更大。真正决定收益的是「一页到底散在几个目录」，这也正是新结构要动的那一刀。

还有一个不体现在公式里的收益：**上下文污染（context pollution，上下文污染）**。8 个文件里必然有其他页面的样式和逻辑，模型读得越多，注意力越分散，越容易把订单页的写法套到设置页上。只读 3 个都属于同一页的文件，跨页串味的概率会明显下降。

---

## 6. 代码量短期变大，长期为什么变小（Code Volume）

这是整个方案里最反直觉的一点，必须给理由 🔍。

**短期确实变大。** 沿用上一节的仓库：按类型分层时，20 个页面共享一套 `Button`、一套 `Table`、一套格式化函数，总量约 9000 行；改成纵向切块后，每个页面自己写自己那份，共用部分被复制，总量会涨到 12000 行上下，涨幅约 30%。

**明知变大还要这么做，理由有三条**（属于「明知有代价仍选择」的取舍，必须说清而不是回避）：

**第一，AI 的成本不看仓库总行数，看单次读入量。** 模型不会因为仓库有 12000 行就更贵，它只为你这一次塞进上下文的那部分付费。仓库从 9000 行涨到 12000 行，单次读取量反而从 9600 token 降到 3600 token。总行数和单次成本，是两条不同的曲线。

**第二，抽象的成本被重新定价了。** 横向共享的本质是「用耦合换重复」。人改代码时耦合便宜——改一处、全站生效很爽；但耦合的代价是**修改半径变成 O(页面数)**：那个被 20 页共用的 `Button` 一旦要加个 `loading` 属性,你可能要回归测试 20 个页面。纵向切块把这份 O(20) 的回归风险，换成了每个页面各写一份的重复。对一个每次改动都要重新读文件的执行者来说，这笔交换是划算的。

**第三，删除是干净的。** 需求下线一个页面时，纵向切块只要删掉一个目录，所有相关代码一起消失；横向分层则会留下没人引用的组件、样式和 hook，它们常年躺在仓库里，每次 AI 搜索都会命中，慢慢变成噪音。**长期变小**指的就是这个：不是代码总量变小，而是**有效代码占比**变高、死代码不再累积。

一句话总结这条取舍：重复的成本是「多写几行」，耦合的成本是「每次改动都要读懂一片」。当写代码的边际成本趋近于零，前者的价格就会跌到几乎可以忽略。

---

## 7. 一份可直接运行的纵向切片（Runnable Slice）

下面这段零依赖、可直接跑。存成 `server.mjs`，执行 `node server.mjs`，打开 `http://localhost:3000` 就能看到两个独立页面切片。首次运行会自动生成示例目录树，不需要手动建文件。

```js
// server.mjs —— 按「页面纵向切块」组织的零依赖服务，node server.mjs 即可运行
import { createServer } from 'node:http'                                        // Node 内置 http，不引入框架
import { readFile, mkdir, writeFile } from 'node:fs/promises'                   // 读写切片与共享层文件
import { existsSync } from 'node:fs'                                            // 判断首次运行要不要生成示例
import { join, dirname } from 'node:path'                                       // 拼跨平台路径
import { fileURLToPath, pathToFileURL } from 'node:url'                         // 动态 import 需要 file URL

const ROOT = dirname(fileURLToPath(import.meta.url))                            // 以本文件所在目录为项目根

// 路由表：URL → 页面目录名，一一对应，看表就知道该改哪一页
const ROUTES = {
  '/': 'home',                                                                  // 首页 → pages/home/
  '/orders': 'orders',                                                          // 订单页 → pages/orders/
}

// 首次运行生成两个页面切片 + 三个共享文件，保证「复制粘贴就能跑」
async function ensureDemo() {
  if (existsSync(join(ROOT, 'pages'))) return                                    // 目录已存在就跳过，不覆盖你的改动
  const files = {
    'shared/theme.css': ':root{--bg:#fff;--fg:#1f2937;--accent:#22c55e}\nbody{background:var(--bg);color:var(--fg);font-family:system-ui}\n', // ② 通用主题
    'shared/api.js': 'export async function listOrders(){return [{id:1,total:99},{id:2,total:120}]}\n',                                      // ① API 服务层
    'shared/toast.js': 'export function toast(t){return `<div class="toast">${t}</div>`}\n',                                                 // ③ 全局消息提示
    'pages/home/page.js': 'export default function page(){return {title:"首页",html:`<h1>首页</h1><p><a href="/orders">去订单页</a></p>`}}\n', // 首页切片
    'pages/home/page.css': 'h1{color:var(--accent)}\n',                                                                                      // 首页样式只作用于首页
    'pages/orders/page.js': 'import { listOrders } from "../../shared/api.js"\nimport { toast } from "../../shared/toast.js"\nexport default async function page(){const rows=await listOrders()\nreturn {title:"订单",html:`<h1>订单</h1><ul>${rows.map(r=>`<li>#${r.id} ¥${r.total}</li>`).join("")}</ul>${toast("已加载 "+rows.length+" 条")}`}}\n', // 订单页切片
    'pages/orders/page.css': 'ul{padding-left:1rem}\n.toast{color:var(--accent)}\n',                                                          // 订单页样式
  }
  for (const [p, body] of Object.entries(files)) {                               // 逐个落盘：路径本身就是约定
    await mkdir(dirname(join(ROOT, p)), { recursive: true })                     // 目录不存在就递归创建
    await writeFile(join(ROOT, p), body)                                         // 写入最小可运行内容
  }
}

// 渲染一个页面：只碰三样东西——本页 page.js、本页 page.css、共享层
async function renderPage(name) {
  const dir = join(ROOT, 'pages', name)                                          // 这一页独占的目录
  const { default: page } = await import(pathToFileURL(join(dir, 'page.js')).href) // 页面逻辑就在自己目录里
  const view = await page()                                                      // 每页自己决定要什么数据
  const pageCss = await readFile(join(dir, 'page.css'), 'utf8')                  // 这一页的样式也在自己目录里
  const themeCss = await readFile(join(ROOT, 'shared', 'theme.css'), 'utf8')     // 主题变量来自唯一共享层
  return `<!doctype html><html><head><meta charset="utf-8"><title>${view.title}</title>
<style>${themeCss}\n${pageCss}</style></head><body>${view.html}</body></html>`   // 主题在前、页面样式在后
}

const server = createServer(async (req, res) => {                               // 一个 URL 进来，只找它自己的目录
  const name = ROUTES[req.url.split('?')[0]]                                    // 用路由表把 URL 映射成目录名
  if (!name) { res.writeHead(404).end('not found'); return }                     // 没有对应页面就直接 404
  res.writeHead(200, { 'content-type': 'text/html; charset=utf-8' })             // 页面统一按 HTML 返回
  res.end(await renderPage(name))                                               // 渲染完直接吐给浏览器
})

await ensureDemo()                                                               // 先保证示例目录存在
server.listen(3000, () => console.log('http://localhost:3000'))                  // 打开浏览器可看到两个切片
```

跑起来之后，请留意三件事，它们就是这个结构的全部要点：

- `pages/home/` 里没有任何一行代码知道 `pages/orders/` 的存在，两个目录可以独立删除；
- 想改订单页的颜色，只改 `pages/orders/page.css`，首页不受影响，也不需要读 `shared/theme.css`；
- `renderPage()` 从头到尾只读三个文件，这就是第 5 节那个「3」在代码里的样子。

---

## 8. 症状 → 原因 → 解法对照表（Symptom Table）

| 症状 | 原因 | 解法 |
|---|---|---|
| 改一个按钮，AI 翻了 5 个目录还没定位 | 文件按类型横向散落，目录结构不表达归属 | 一个 URL 一个目录，页面结构 / CSS / JS 同置 |
| AI 改了 A 页，B 页样式跟着变了 | 共享 CSS 里混进了页面专属类名 | 页面样式就近放进 `page.css`，共享层只留变量与重置 |
| `shared/` 目录半年后变成第二个 `utils/` | 共享层没有准入规则，随手就放 | 白名单只留 API / theme / toast，其余按 rule of three 处理 |
| AI 一次任务读十几个文件，中途开始"忘记"前面的内容 | 修改半径跨了整个仓库，上下文被无关代码挤占 | 把修改半径压到一个目录 + 1 个共享文件 |
| 需求下线一个页面，删完还剩一堆死代码 | 页面代码散在多处，删除无法原子完成 | 删一个目录即完成下线，路由表同步删一行 |
| 每页都复制了一份格式化函数，看着很别扭 | 主动用重复换低耦合 | 接受重复：AI 侧成本取决于读取量，不取决于仓库行数 |
| 页面之间开始互相 import | 边界没守住，纵向切片退化回横向耦合 | 禁止跨页引用，共用需求一律走共享层白名单 |

---

## 9. 五个落地坑（Pitfalls）

**坑一：共享层只放 API，忘了主题和提示也是共享的。** 结果每个页面各写一份 toast，样式和位置都不一致。三类共享物是有内在理由的，不是随便挑的。

**坑二：把「公共组件」当成共享层。** `Button`、`Table`、`Modal` 看起来该共享，但它们一旦被二十个页面依赖，改一次就要回归二十页。正确做法是把它们**复制进各页**，让每页自己演化；等到真的三页以上需要完全一致的实现，再提取。

**坑三：页面目录里塞进不属于它的东西。** 比如把「订单页专用的日期格式化」放进 `pages/orders/utils/`，这没错；但如果这个 `utils/` 开始被别的页面 import，边界就破了。判断标准永远是：**这个文件是否只服务这一个页面**。

**坑四：路由表和目录不同步。** 加了目录忘了加路由，或者删了页面忘删路由，都会留下 404。把路由表当成唯一入口，加页面时先改路由表，再建目录。

**坑五：样式优先级打架。** 主题、页面样式、组件内联样式三层叠加，容易出现「改了没生效」。约定固定顺序：主题变量 → 页面样式 → 运行时覆盖，并且页面样式只写类选择器，不写标签选择器和 `!important`。

---

## 10. 判据：该切还是不该切（Verdict）

什么时候值得改成纵向切块：

- 页面数量超过 10 个，且页面之间业务差异明显；
- 主要修改者是 AI Agent，人只做评审和验收；
- 经常出现「改一页影响另一页」的回归问题；
- 团队已经能接受「同样的东西在不同目录出现两次」。

什么时候不必切，或者只能部分切：

- 页面很少（3 到 5 个），横向分层本身就没多少跳转成本；
- 核心是设计系统（design system，设计系统），组件一致性比修改半径更重要；
- 页面之间共享极重，几乎每个页面都是同一套表单的不同配置——这时该抽象的是**配置**，不是目录；
- 团队规模大、需要严格分层评审，人的维护习惯仍然优先。

如果决定要切，别一次性重构。挑一个正在改的页面，把它按新结构搬过去，跑通之后再搬第二个。三个页面搬完，你会对「哪些东西真的该进共享层」有完全不同的判断。

页面边界清晰、共享层只有三类、改一处只读一个目录时，这套结构值得用；页面极少、或核心诉求是组件一致性时，横向分层仍然更合适，别为结构而结构。

本专栏《全栈开发实战》从项目结构、样式体系一路讲到前后端联调与部署落地，每篇配一段可直接运行的代码和一张症状对照表，每周更新一篇。想按顺序读完，可在专栏页订阅。
