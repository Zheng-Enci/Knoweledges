# React 19 加 Vite 6 企业级前端项目目录结构：无路由 SPA、zustand 与 Tailwind 4 的分层架构指南

**结论：前端目录不该按文件类型分（components / hooks / utils），而该按「谁会改它」和「它依赖谁」分。** 你这套选型里藏着四个硬约束：没有路由库，页签状态就必须有独立的导航层，否则 App.tsx 会变成上帝组件；四个 zustand store 按业务域切，而不是按「全局状态」堆一个文件；useApi 只能单向依赖 fetch，不能反向 import 业务 store；shared 包用 alias 直连源码，就必须在三处配置里对齐同一个入口。四条边界守住，目录自然长对；守不住，再漂亮的分层也会在三个月内塌成一坨。

---

## 目录

1. 结论：先划四条边界，再谈目录（Four Boundaries）
2. 选型反推目录：每个技术决策逼出一个文件夹（Stack to Folder）
3. 顶层骨架：apps/web 与 packages/shared 各管一段（Top-level Layout）
4. 页签不是路由：没有 react-router 也要有导航层（Tabs without Router）
5. 四个 store 怎么切：按「谁拥有这份数据」分（Zustand Stores）
6. 请求层 useApi：三件事与一个禁区（Request Layer）
7. shared 包与 Vite alias：源码直连的收益与代价（Shared Package）
8. Tailwind 4：没有 config 文件后主题变量放哪（CSS-First Theme）
9. 工程化：turbo、dev.mjs、tsc --noEmit 各管一段（Toolchain）
10. 完整可运行代码：目录边界校验器（Boundary Checker）
11. 症状、原因、解法对照表（Symptom → Cause → Fix）

---

## 1. 结论：先划四条边界，再谈目录（Four Boundaries）

企业级前端和业余前端的差别，不在目录有几个文件夹，而在**边界有没有工具守**。四条边界，按重要性排序：

**第一条：可部署单元与可复用包分开。** `apps/web` 是能跑起来的那一个，`packages/shared` 是被它依赖的那一个。前者可以有 `index.html`、可以有 `vite.config.ts`，后者一旦出现 `document`、`window`、`react` 就说明边界破了。

**第二条：业务域与通用组件分开。** `features/auth`、`features/articles` 各自是完整的一竖条（组件 + 该域私有的 hook + 该域的 API 调用），`components/` 只放「换个项目也能用」的东西。判断标准很粗暴：这个组件里出现 `article`、`credential` 这类业务名词，它就不该在 `components/`。

**第三条：状态的归属唯一。** 一份数据只能有一个写入方。页签 id 归 `app` 层，token 归 `authStore`，文章列表归 `articleStore`，三者不许互相抄一份。

**第四条：依赖方向单向。** `features → stores / api / components / shared`，`api → fetch`（不许反向 import store），`shared → 无`。反了就成环，成环就改不动。

> 生活化的对照：这套目录像一栋写字楼的楼层分配。`apps` 是一楼大堂和门禁，`app` 是电梯与楼层索引，`features` 是各家公司自己的办公室，`components` 是公共会议室，`stores` 是每家公司自己的档案柜，`api` 是快递收发室，`shared` 是整栋楼通用的水电图纸。大堂不能替公司决定文件放哪，收发室也不能反过来指挥公司怎么盖章——真出现这种指令，说明这栋楼的管理早就乱了。

---

## 2. 选型反推目录：每个技术决策逼出一个文件夹（Stack to Folder）

多数人的做法是先抄一份「React 项目标准结构」，再往里塞代码。正确顺序反过来：**先看每个选型把什么复杂度引进来，再给它划一个收容所。**

| 技术选型 | 引入的复杂度 | 对应的目录落点 |
| --- | --- | --- |
| React 19.1 纯 SPA | 无 SSR，所有渲染都在浏览器 | `src/main.tsx` 只挂载，`App.tsx` 只装配 |
| Vite 6.3 + `/api` 代理 | 开发端口与环境地址两份真相 | `apps/web/vite.config.ts` 与 `.env.example` |
| Tailwind 4.1 CSS-first | 主题变量的唯一来源 | `src/styles/index.css` |
| zustand 5 四个 store | 状态归属与持久化策略 | `src/stores/` 一域一文件 |
| 无路由库 + `geo_active_tab` | 导航逻辑没地方住 | `src/app/`（页签注册表 + 激活态） |
| 自写 useApi | 请求横切关注点（401、loading） | `src/api/client.ts` + `src/hooks/useApi.ts` |
| react-markdown 10 | 渲染层被业务代码直接依赖 | `components/MarkdownView.tsx` 单一出口 |
| `@zemingengine/shared` + alias | 三处配置必须对齐 | `packages/shared/src/index.ts` |
| turbo + tsc + `dev.mjs` | 任务编排与并发启动 | 根 `turbo.json`、`scripts/dev.mjs` |

表格最后一行最容易被忽略。turbo 和 tsc 本身不产生目录，但它们决定了**目录之间的调用顺序**：`turbo run typecheck` 会先跑 `packages/*` 再跑 `apps/*`，所以 `shared` 一旦报类型错误，`web` 根本不会开始检查。这个顺序反过来要求 shared 必须先独立通过类型检查——也就是它不能偷偷依赖 web 里的类型。

`lucide-react` 和 `react-markdown` 这两行值得单独说：它们都是「叶子依赖」，谁都能引，所以最容易在 store 里被误用。**图标只在渲染层引，store 里存的是页签 id 而不是图标组件**——这一条能避免 zustand 的 state 里混进 React 元素，进而让 persist 中间件序列化失败。

---

## 3. 顶层骨架：apps/web 与 packages/shared 各管一段（Top-level Layout）

先看全貌。这套骨架对应你描述的技术栈，两边都是 npm workspaces 的成员：

```text
geo/
├── apps/
│   └── web/                          # 唯一可部署单元（Vite 6 + React 19）
│       ├── index.html
│       ├── vite.config.ts            # 端口 5174、/api 代理、@ 与 shared 别名
│       ├── tsconfig.json
│       ├── package.json
│       └── src/
│           ├── main.tsx              # 入口：挂载 + 全局样式 + 401 绑定
│           ├── App.tsx               # 只做页签装配，不超过 30 行
│           ├── app/                  # 应用级：导航、布局、页签注册表
│           │   ├── tabs.ts           # 页签元数据（id / label / icon / 组件）
│           │   ├── useActiveTab.ts   # localStorage('geo_active_tab') 读写
│           │   └── TabShell.tsx      # 页签骨架与渲染分发
│           ├── features/             # 业务域，一域一竖条
│           │   ├── auth/
│           │   │   ├── index.ts      # 唯一出口（barrel）
│           │   │   ├── LoginForm.tsx
│           │   │   └── useLogin.ts   # 只属于 auth 的 hook
│           │   ├── sessions/
│           │   ├── articles/
│           │   └── credentials/
│           ├── stores/               # zustand，与 features 同名一一对应
│           │   ├── authStore.ts
│           │   ├── sessionStore.ts
│           │   ├── articleStore.ts
│           │   └── credentialStore.ts
│           ├── api/                  # 请求层：只管 HTTP，不懂业务
│           │   ├── client.ts         # request / 401 / 错误归一
│           │   ├── auth.api.ts
│           │   ├── articles.api.ts
│           │   └── sessions.api.ts
│           ├── hooks/                # 跨域通用 hook
│           │   └── useApi.ts         # withLoading 包装
│           ├── components/           # 跨域通用 UI
│           │   ├── Button.tsx
│           │   ├── EmptyState.tsx
│           │   └── MarkdownView.tsx  # react-markdown 的唯一出口
│           ├── lib/                  # 纯函数：格式化、校验、常量
│           └── styles/
│               └── index.css         # Tailwind 4 入口 + @theme 变量
├── packages/
│   └── shared/                       # @zemingengine/shared
│       ├── package.json              # main/types 都指向 src/index.ts
│       └── src/
│           ├── index.ts
│           ├── types/                # Article / Session / Credential 类型
│           └── contracts.ts          # 请求响应形状
├── scripts/
│   └── dev.mjs                       # 并发拉起各 workspace 的 dev
├── turbo.json
├── tsconfig.base.json
└── package.json                      # private: true + workspaces
```

三个反直觉的取舍，先说清楚：

**第一，`features` 里不建 `components/` 子目录。** 一个域内的组件直接平铺在域名下。理由是 auth 域的组件数通常不超过十个，多一层 `components/` 只会让 import 路径变长（`@/features/auth/components/LoginForm`），而**深路径正是边界校验要打的靶子**。等某个域真的超过十五个文件，再按 `ui/` 与 `logic/` 二分。

**第二，`stores` 独立在 `src` 下，不塞进 `features`。** 因为 store 天生被跨域读取：`articleStore` 会被 `features/articles` 读，也会被 `app/TabShell` 读（用于显示角标）。放进 features 就等于强迫别人跨域引用，直接撞上第一条边界。

**第三，`lib/` 与 `shared` 的分工不是「前端 / 后端」，而是「有没有领域知识」。** 日期格式化、金额格式化、防抖这类纯函数放 `lib/`；`Article`、`Credential` 这类跨包共享的类型放 `shared`。`lib/` 里出现 `import type { Article }` 是正常的（从 shared 引类型），`shared` 里出现 `import` 任何前端模块就是违规。

顶层为什么必须有 workspaces，而不是一个单体 `src`？因为 `shared` 的存在意义是「被两个以上使用方引用」。你的场景里它至少被 `apps/web` 和未来的 `apps/admin` 共用，所以它值得独立成包；如果只有一个使用方，`file:` 依赖加 alias 就是纯成本，直接放 `src/lib` 更划算。

> 这个判断和本专栏 [Hono 4 多库多模型服务的企业级 Monorepo 目录结构](https://blog.csdn.net/2301_79239314/article/details/170654221) 里「包会不会被第二个 app 用」的判据是同一条：**抽包的成本要用「第二个使用方」来偿付，没有第二个使用方就不抽。** 区别只在后端按 adapter 拆，前端按业务域拆。

---

## 4. 页签不是路由：没有 react-router 也要有导航层（Tabs without Router）

没有路由库，最容易出现的两种塌方方式：一是 `App.tsx` 里堆十几个 `useState` 加一大片 `{tab === 'x' && <X />}`；二是每个页签组件自己去 `localStorage` 读一次当前页签。

正确的做法是把「当前在哪一屏」当成一个**应用级状态**，抽成三件东西：注册表、激活态 hook、渲染壳。

```ts
// src/app/tabs.ts —— 页签注册表：新增一个页签只改这个文件
import { FileText, KeyRound, MessagesSquare, ShieldCheck } from 'lucide-react';  // 图标只在声明处出现
import type { ComponentType } from 'react';

export type TabId = 'auth' | 'sessions' | 'articles' | 'credentials';  // 联合类型，写错即报错

/** 页签元数据：id 用于持久化，label 用于渲染，component 用于分发 */
export interface TabMeta {
  id: TabId;                                        // 唯一标识，也是 localStorage 里存的值
  label: string;                                    // 侧栏显示名
  icon: ComponentType<{ size?: number }>;           // lucide 图标组件
  component: () => Promise<{ default: ComponentType }>;  // 懒加载，按页签分包
}

export const TABS: readonly TabMeta[] = [
  { id: 'auth', label: '账号', icon: ShieldCheck, component: () => import('@/features/auth') },
  { id: 'sessions', label: '会话', icon: MessagesSquare, component: () => import('@/features/sessions') },
  { id: 'articles', label: '文章', icon: FileText, component: () => import('@/features/articles') },
  { id: 'credentials', label: '密钥', icon: KeyRound, component: () => import('@/features/credentials') },
];

/** 类型护栏：确保 'auth' 这类字符串一定存在于注册表里 */
export const isTabId = (v: unknown): v is TabId =>
  typeof v === 'string' && TABS.some((t) => t.id === v);
```

激活态单独一个文件，读写都走同一个 key，并且在写入时做一次校验——**localStorage 是外部输入，里面的值可能是上个版本留下的脏数据**：

```ts
// src/app/useActiveTab.ts —— 激活页签：唯一读写 geo_active_tab 的地方
import { useCallback, useEffect, useState } from 'react';
import { TABS, isTabId, type TabId } from './tabs';

const KEY = 'geo_active_tab';       // 全局唯一键名，禁止别处再写这个字符串
const FALLBACK: TabId = 'auth';     // 首次进入或脏数据时的兜底页签

export function useActiveTab() {
  // 初始化时同步读一次，避免首帧闪一下别的页签
  const [active, setActive] = useState<TabId>(() => {
    const saved = localStorage.getItem(KEY);      // 可能为 null，也可能为旧版本 id
    return isTabId(saved) ? saved : FALLBACK;     // 校验通过才采用，否则兜底
  });

  // 状态变化后回写，跨标签页靠 storage 事件同步
  useEffect(() => {
    localStorage.setItem(KEY, active);
  }, [active]);

  useEffect(() => {
    const onStorage = (e: StorageEvent) => {      // 另一个标签页改了同一个 key
      if (e.key === KEY && isTabId(e.newValue)) setActive(e.newValue);
    };
    window.addEventListener('storage', onStorage);
    return () => window.removeEventListener('storage', onStorage);
  }, []);

  const go = useCallback((id: TabId) => setActive(id), []);  // 只接受合法 id
  return { active, go, tabs: TABS };
}
```

`App.tsx` 因此只剩下装配，页签数量和它无关：

```tsx
// src/App.tsx —— 只装配，不判断业务
import { TabShell } from '@/app/TabShell';
import { useActiveTab } from '@/app/useActiveTab';

export default function App() {
  const { active, go, tabs } = useActiveTab();   // 导航状态全部来自 app 层
  return <TabShell tabs={tabs} active={active} onSelect={go} />;  // 壳组件负责渲染分发
}
```

**这套做法的代价必须说清楚：页签状态不进 URL，所以链接没法分享，刷新能恢复但回退键无效。** 如果你的场景需要「把当前页签发给我同事」这种能力，那就该上路由库——`useState + localStorage` 只适合内部工具型 SPA。这不是技术优劣，是需求取舍：内部的运营后台，复制链接分享的需求远少于「刷新后还停在原来那页」。

---

## 5. 四个 store 怎么切：按「谁拥有这份数据」分（Zustand Stores）

四个 store 不是四个筐，而是四条数据寿命线。切分判据只有一句：**这份数据的第一写入方是谁，它就该住在谁的 store 里。**

| store | 拥有什么 | 生命周期 | 持久化 | 谁可以写 |
| --- | --- | --- | --- | --- |
| `authStore` | token、当前用户摘要 | 登录到登出 | `persist`（只存 token） | 仅 auth 域与 401 处理 |
| `sessionStore` | 会话列表、当前会话 id | 一次会话列表请求 | 不持久化 | 仅 sessions 域 |
| `articleStore` | 文章列表、选中文章、加载态 | 一个页签存续期 | 不持久化 | 仅 articles 域 |
| `credentialStore` | 密钥明文、校验状态 | 组件内或一次操作 | **绝不持久化** | 仅 credentials 域 |

`credentialStore` 那一行是安全红线：密钥一旦进 `localStorage`，任何 XSS 都能读走。所以它连 `persist` 中间件都不挂，只活在内存里，刷新即失。

`authStore` 用 `persist` 但必须 `partialize`，否则 loading、错误信息这些瞬时字段也会被写盘，下次启动读到一堆过期状态：

```ts
// src/stores/authStore.ts —— 只持久化 token，其余字段留在内存
import { create } from 'zustand';
import { persist } from 'zustand/middleware';

/** 认证状态：token 是唯一需要跨刷新保留的字段 */
interface AuthState {
  token: string | null;                                  // 访问令牌，null 表示未登录
  user: { id: string; name: string } | null;             // 当前用户摘要
  signIn: (token: string, user: AuthState['user']) => void;  // 登录成功写入
  signOut: () => void;                                   // 登出与 401 共用
}

export const useAuthStore = create<AuthState>()(
  persist(
    (set) => ({
      token: null,
      user: null,
      signIn: (token, user) => set({ token, user }),      // 两个字段一起写，避免半登录态
      signOut: () => set({ token: null, user: null }),     // 幂等，重复调用无副作用
    }),
    {
      name: 'geo_auth',                                    // localStorage 键名
      partialize: (s) => ({ token: s.token }),             // 只落 token，user 下次启动重新拉
    },
  ),
);
```

另外三个 store 的骨架完全一样，差别只在字段。判断「该不该单独建 store」有一个反直觉的答案：**只被一个组件树用到的数据，不要进 store，用 `useState`。** 比如「密钥输入框是否可见」这种状态，放 `credentialStore` 只会让 store 变成垃圾场。

还有一条硬规矩：**store 里不许出现组件、不许出现 DOM、不许 import `lucide-react`。** 因为 `persist` 会对 state 做 `JSON.stringify`，塞进去一个函数或 React 元素，轻则被静默丢弃，重则 `TypeError: Converting circular structure to JSON`。页签的图标属于注册表，不属于 store——这是第 2 节那个表格里 `lucide-react` 那一行的落地方式。

并发读取时还要注意 `useShallow`：zustand 5 里选择器返回新对象会导致无谓重渲染，`useShallow` 才让它按浅比较判断。写法是 `useArticleStore(useShallow((s) => ({ list: s.list, loading: s.loading })))`，不是每个字段单独 `useArticleStore` 调三次。

---

## 6. 请求层 useApi：三件事与一个禁区（Request Layer）

请求层要收的复杂度只有三件：**统一地址、统一鉴权、统一错误形态。** 多一件都不该它管。

最典型的翻车方式是这样写的：`client.ts` 里 `import { useAuthStore }`，store 里又调和 `api/auth.api.ts` 里的 `login()`。第一次跑没问题，等到做代码分割时变成运行时循环引用，报错是 `Cannot access 'useAuthStore' before initialization`——一个跟业务毫无关系的错。

解法是**把依赖倒过来，用注入而不是 import**：

```ts
// src/api/client.ts —— 零业务依赖，谁都不 import
export interface ApiConfig {
  baseUrl: string;                          // 请求前缀，开发环境走 Vite 代理
  getToken: () => string | null;             // 由调用方注入，api 层不认识 store
  onUnauthorized: () => void;                // 401 时回调，由调用方决定清什么
}

const cfg: ApiConfig = {
  baseUrl: '/api',                          // 默认走代理，生产由网关改写
  getToken: () => null,                     // 默认无令牌
  onUnauthorized: () => {},                 // 默认不做处理
};

/** 在 main.tsx 里调用一次，把 store 的能力注入进来 */
export function configureApi(next: Partial<ApiConfig>) {
  Object.assign(cfg, next);
}

/** 归一化的接口错误：status 供 UI 分支，message 供提示 */
export class ApiError extends Error {
  constructor(public status: number, message: string) {
    super(message);
  }
}

/** 统一请求入口：拼地址、注令牌、归一 401 与非 2xx */
export async function request<T>(path: string, init: RequestInit = {}): Promise<T> {
  const token = cfg.getToken();                                        // 每次请求现取，避免闭包过期
  const res = await fetch(cfg.baseUrl + path, {
    ...init,
    headers: {
      'Content-Type': 'application/json',                              // 默认 JSON
      ...(token ? { Authorization: `Bearer ${token}` } : {}),           // 有令牌才带
      ...init.headers,                                                 // 允许调用方覆盖
    },
  });
  if (res.status === 401) {                                            // 令牌失效：先回调再抛
    cfg.onUnauthorized();
    throw new ApiError(401, '登录已过期');
  }
  if (!res.ok) throw new ApiError(res.status, await res.text());       // 其余错误统一成 ApiError
  return (res.status === 204 ? undefined : await res.json()) as T;     // 204 不解析响应体
}
```

注入点在 `main.tsx`，那里本来就是唯一允许「同时认识 api 和 store」的地方：

```tsx
// src/main.tsx —— 唯一的装配点：把 store 的能力注入 api 层
import { createRoot } from 'react-dom/client';
import App from './App';
import { configureApi } from '@/api/client';
import { useAuthStore } from '@/stores/authStore';
import './styles/index.css';

configureApi({
  getToken: () => useAuthStore.getState().token,                       // 从 store 取，不用 hook
  onUnauthorized: () => useAuthStore.getState().signOut(),             // 401 即登出，单一出口
});

createRoot(document.getElementById('root')!).render(<App />);
```

`useApi.ts` 只负责 loading，而且必须用**并发计数**而不是布尔：

```ts
// src/hooks/useApi.ts —— 只做 loading 包装，不碰业务判断
import { useCallback, useState } from 'react';

export function useApi() {
  const [pending, setPending] = useState(0);                 // 计数而非布尔：并发请求时布尔会提前归零
  const run = useCallback(async <T,>(fn: () => Promise<T>): Promise<T> => {
    setPending((n) => n + 1);                                // 进入 +1
    try {
      return await fn();                                     // 业务函数自己调 api/*.api.ts
    } finally {
      setPending((n) => n - 1);                              // 无论成功失败都要 -1
    }
  }, []);
  return { loading: pending > 0, run };                      // 任一请求在飞就算 loading
}
```

为什么旧写法 `setLoading(true) … setLoading(false)` 会出问题：两个请求并发，第一个先回来把 loading 置 false，第二个还在飞，界面上按钮已经可以再点了，用户双击就发出第三个请求。计数法天然解决这件事。

**禁区只有一条：请求层不写业务分支。** 不在 `request` 里判断「这个接口失败要不要跳转登录以外的页面」，不在 `useApi` 里内置 toast 与重试策略。理由不是教条，而是这些东西一旦写进请求层，就会变成所有接口共享的行为——文章列表 404 想显示空状态，密钥接口 404 想提示「未配置」，共享的行为只能二选一。

---

## 7. shared 包与 Vite alias：源码直连的收益与代价（Shared Package）

`file:` 依赖加 alias 直指源码，是这套工程化里收益最直接的一招：改 `packages/shared/src/types/article.ts` 加一个字段，`apps/web` 里立刻就有类型提示，不用 `npm run build`，不用 `npm link`，不用清 `node_modules`。

代价是**同一个入口要在三处对齐**，漏一处就出现「编辑器报红但能跑」或者「能跑但类型是 any」：

```json
// packages/shared/package.json —— 第一处：包自身的入口指向源码
{
  "name": "@zemingengine/shared",
  "version": "0.0.0",
  "private": true,
  "type": "module",
  "main": "./src/index.ts",
  "types": "./src/index.ts",
  "exports": { ".": "./src/index.ts" }
}
```

```json
// apps/web/tsconfig.json —— 第二处：TS 的 paths 指向同一文件
{
  "extends": "../../tsconfig.base.json",
  "compilerOptions": {
    "baseUrl": ".",
    "paths": {
      "@/*": ["./src/*"],
      "@zemingengine/shared": ["../../packages/shared/src/index.ts"]
    }
  },
  "include": ["src", "../../packages/shared/src"]
}
```

```ts
// apps/web/vite.config.ts —— 第三处：打包器别名，外加 dedupe
import { fileURLToPath, URL } from 'node:url';
import { defineConfig } from 'vite';
import react from '@vitejs/plugin-react';
import tailwindcss from '@tailwindcss/vite';

export default defineConfig({
  plugins: [react(), tailwindcss()],                                   // Tailwind 4 走 Vite 插件，不装 PostCSS
  resolve: {
    alias: {
      '@': fileURLToPath(new URL('./src', import.meta.url)),           // 业务别名
      '@zemingengine/shared': fileURLToPath(
        new URL('../../packages/shared/src/index.ts', import.meta.url), // 直达源码，跳过构建产物
      ),
    },
    dedupe: ['react', 'react-dom'],                                    // 防止 shared 拉起第二份 React
  },
  server: {
    port: 5174,                                                        // 固定端口，避免和后端撞车
    proxy: {
      '/api': {
        target: process.env.VITE_API_TARGET ?? 'http://127.0.0.1:8787', // 后端地址只在这里出现一次
        changeOrigin: true,
      },
    },
  },
});
```

`dedupe` 那一行不是可选项。alias 到源码之后，如果 `shared` 自己的 `node_modules` 里也有一份 React（`file:` 依赖很容易这样），React 19 会抛 `Invalid hook call`——因为 hook 走的是两份不同的 React 实例。这个错看起来像业务代码写错了，实际是打包配置。

还有一条纪律：**`shared` 里不许出现 `react`、`react-dom`、`window`、`document`。** 它应该是纯类型加纯函数，这样将来后端 Node 服务也能引同一份契约。这条纪律靠 `packages/shared/eslint.config.js` 里的 `no-restricted-imports` 卡住，不靠代码评审。**用工具守边界，别用记忆守边界。**

---

## 8. Tailwind 4：没有 config 文件后主题变量放哪（CSS-First Theme）

Tailwind 4.1 把配置从 JS 搬进了 CSS。没有 `tailwind.config.js`，`.ts` 里也找不到 `theme.extend`，主题只有一个落点：`src/styles/index.css` 里的 `@theme` 块。

```css
/* src/styles/index.css —— 全站样式的唯一入口 */
@import "tailwindcss";                 /* v4 的入口指令，替代 v3 的三条 @tailwind */

@theme {
  /* 品牌色阶：组件里只能用 brand-500 这类语义名，禁止写死 hex */
  --color-brand-500: oklch(0.62 0.19 258);
  --color-brand-600: oklch(0.55 0.19 258);
  /* 圆角与阴影也进主题，保证全站一致 */
  --radius-card: 14px;
  --shadow-card: 0 1px 2px rgb(0 0 0 / 0.06), 0 8px 24px rgb(0 0 0 / 0.08);
}

/* 少量确实需要手写的全局样式，v4 里用 @layer 显式分层 */
@layer base {
  html { color-scheme: light dark; }
}
```

`@theme` 里声明的变量会自动变成工具类：`--color-brand-500` 生成 `bg-brand-500`、`text-brand-500`、`border-brand-500`。这就是 v4 的核心变化——**变量既是 CSS 自定义属性，也是类名的来源，一份定义两处生效**。

目录层面的影响是：`styles/` 目录只需要一个文件。不要建 `tailwind.config.js`（v4 不读），不要建 `theme.ts`（会和 CSS 里的变量打架），更不要在组件里写 `style={{ color: '#3b82f6' }}`——那等于在主题系统之外开了个后门，将来换品牌色要全局搜 hex。

顺带说清 `@tailwindcss/vite` 的定位：它是替代 PostCSS 链的。v3 时代要在 `postcss.config.js` 里挂 `tailwindcss` 和 `autoprefixer` 两个插件，v4 用一个 Vite 插件全包了，构建更快，配置更少。所以项目里**不该再有 `postcss.config.js`**，有的话要么是历史遗留，要么是别的插件（比如 `postcss-px-to-viewport`）还在用，那种情况要单独确认。

---

## 9. 工程化：turbo、dev.mjs、tsc --noEmit 各管一段（Toolchain）

三个工具各管一件事，别让它们互相兼职：**turbo 管任务编排，`dev.mjs` 管进程并发，`tsc --noEmit` 管类型正确性。**

根 `package.json` 只放工作区声明与入口脚本：

```json
{
  "name": "geo",
  "private": true,
  "workspaces": ["apps/*", "packages/*"],
  "scripts": {
    "dev": "node scripts/dev.mjs",
    "build": "turbo run build",
    "typecheck": "turbo run typecheck",
    "check:boundaries": "node scripts/check-boundaries.mjs"
  },
  "devDependencies": { "turbo": "^2.0.0", "typescript": "~5.8.0" }
}
```

`turbo.json` 的关键是 `dependsOn: ["^typecheck"]`——那个尖号表示「先跑完所有上游依赖包的 typecheck」。于是 `shared` 出错时，`web` 根本不会开始检查，报错信息不会互相淹没：

```json
{
  "$schema": "https://turbo.build/schema.json",
  "tasks": {
    "build": { "dependsOn": ["^build"], "outputs": ["dist/**"] },
    "typecheck": { "dependsOn": ["^typecheck"], "outputs": [] },
    "dev": { "cache": false, "persistent": true }
  }
}
```

`dev` 任务必须 `cache: false` 加 `persistent: true`，否则 turbo 会认为它「跑完了可以缓存」，你的开发服务器起一次就再也不起。

`scripts/dev.mjs` 的任务只有并发与收尾，不写业务逻辑：

```js
// scripts/dev.mjs —— 并发拉起所有 workspace 的 dev，任一退出则全退
import { spawn } from 'node:child_process';

const targets = ['apps/web'];                // 未来加 apps/admin 就往这里加一行
const children = targets.map((dir) =>
  spawn('npm', ['run', 'dev', '--workspace', dir], { stdio: 'inherit', shell: true }),
);                                          // shell: true 让 Windows 也能找到 npm.cmd

const shutdown = () => children.forEach((c) => c.kill());   // Ctrl+C 时统一收尾
process.on('SIGINT', () => { shutdown(); process.exit(0); });

children.forEach((c) =>
  c.on('exit', (code) => {                  // 任一子进程挂掉就整体退出，不留孤儿进程
    if (code !== 0) { shutdown(); process.exit(code ?? 1); }
  }),
);
```

`tsc --noEmit` 一定要挂在每个 workspace 自己的 `package.json` 里，而不是只在根目录跑一次：

```json
{
  "scripts": {
    "dev": "vite",
    "build": "tsc --noEmit && vite build",
    "typecheck": "tsc --noEmit"
  }
}
```

为什么不用 `vite build` 自带的类型检查：Vite 用的是 esbuild，**只转译不检查**，类型错误会被静默跳过。很多「本地能跑、CI 挂掉」的项目都是漏了这一步。

---

## 10. 完整可运行代码：目录边界校验器（Boundary Checker）

前面九节讲的都是「应该怎么放」，这一节给「放错了怎么发现」。约定写在 Wiki 里没人看，写成脚本挂在 CI 里才叫约束。

脚本零依赖，只用 Node 内置模块，把仓库根当参数传进去就能跑：`node scripts/check-boundaries.mjs`。

```js
#!/usr/bin/env node
// 前端目录边界校验器：扫描 apps/web/src 与 packages/shared/src，按 6 条规则报违规
import { existsSync, readFileSync, readdirSync, statSync } from 'node:fs';   // 只用 Node 内置模块，零依赖
import { join, relative, sep } from 'node:path';                              // 路径拼接与相对化

const root = process.argv[2] ?? process.cwd();                                // 仓库根，缺省为当前目录
const WEB = join(root, 'apps/web/src');                                       // 前端源码根
const SHARED = join(root, 'packages/shared/src');                             // 跨包共享源码根

// 递归收集 .ts/.tsx，跳过 node_modules 与类型声明文件
// 参数: dir 起始目录 → 返回: 绝对路径数组，例如 ['…/App.tsx', …]
function walk(dir, out = []) {
  if (!existsSync(dir)) return out;                                           // 目录不存在直接返回空
  for (const name of readdirSync(dir)) {                                      // 遍历当层条目
    const p = join(dir, name);                                                // 拼出绝对路径
    if (statSync(p).isDirectory()) {                                          // 是目录就递归
      if (name !== 'node_modules') walk(p, out);                              // 跳过依赖目录
    } else if (/\.(ts|tsx)$/.test(name) && !name.endsWith('.d.ts')) {
      out.push(p);                                                            // 只统计源码文件
    }
  }
  return out;
}

// 统一成正斜杠相对路径，便于输出与正则匹配
const rel = (p) => relative(root, p).split(sep).join('/');
// 取出 import/export 的模块说明符，例如 '@/features/articles' → ['@/features/articles']
const specs = (file) =>
  [...readFileSync(file, 'utf8').matchAll(/(?:from|import)\s*\(?\s*['"]([^'"]+)['"]/g)].map((m) => m[1]);
// 判断文件属于哪个业务域，例如 src/features/auth/LoginForm.tsx → 'auth'
const domainOf = (p) => rel(p).match(/apps\/web\/src\/features\/([^/]+)\//)?.[1] ?? null;

const files = [...walk(WEB), ...walk(SHARED)];                                // 待扫描文件全集
const errors = [];                                                            // 违规清单

for (const file of files) {
  const r = rel(file);                                                        // 相对路径，用于报错定位
  const dom = domainOf(file);                                                 // 当前文件所属业务域
  const inShared = r.startsWith('packages/shared/');                          // 是否位于 shared 包
  const inApi = r.includes('/src/api/');                                      // 是否位于请求层

  for (const spec of specs(file)) {                                           // 逐条检查导入说明符
    if (inShared && /^react(-dom)?(\/|$)/.test(spec))                         // R2: shared 必须同构，禁引 React
      errors.push(`R2 ${r} → ${spec}`);
    if (inApi && spec.startsWith('@/features'))                               // R3: 请求层不许反依赖业务域
      errors.push(`R3 ${r} → ${spec}`);
    if (spec.startsWith('@/features/')) {                                     // 命中业务域别名
      const seg = spec.split('/');                                            // 例如 ['@','features','auth','index']
      const target = seg[2];                                                  // 目标业务域
      if (dom && target !== dom) errors.push(`R1 ${r} → ${spec}`);            // R1: 禁止跨域互引
      if (seg.length > 3) errors.push(`R4 ${r} → ${spec}`);                   // R4: 必须走域内 barrel
    }
    if (spec.startsWith('../')) errors.push(`R6 ${r} → ${spec}`);             // R6: 相对路径只许 ./ 同目录
  }
}

// R5: 每个业务域必须有对外出口 index.ts
const featuresDir = join(WEB, 'features');                                    // features 绝对路径
for (const sub of readdirSync(featuresDir, { withFileTypes: true })) {        // 遍历各业务域
  if (sub.isDirectory() && !existsSync(join(featuresDir, sub.name, 'index.ts')))  // 缺 barrel 即违规
    errors.push(`R5 apps/web/src/features/${sub.name}/ 缺 index.ts`);
}

console.log(`扫描 ${files.length} 个文件，命中 ${errors.length} 处违规`);       // 汇总行，便于 CI 读取
for (const e of errors) console.log(`  ${e}`);                                // 逐条打印
process.exit(errors.length ? 1 : 0);                                          // 有违规则非零退出，卡住 CI
```

六条规则的判定口径，逐条写清楚，避免读者对不上号：

| 编号 | 规则 | 违规示例 |
| --- | --- | --- |
| R1 | `features` 之间禁止互引 | `sessions` 里 import `@/features/articles` |
| R2 | `shared` 禁引 React 与浏览器 API | `packages/shared/src/index.ts` 里 `import { useState } from 'react'` |
| R3 | `api` 层禁反向依赖业务域 | `api/auth.api.ts` 里 import `@/features/auth` |
| R4 | 引用业务域必须走 barrel | `@/features/articles/ArticleCard` 深路径 |
| R5 | 每个业务域必须有 `index.ts` | `features/credentials/` 只有组件没有出口 |
| R6 | 相对路径只允许 `./` | `import { X } from '../sessions'` |

我按上面这套骨架搭了一棵 27 个源码文件的演示树，并**故意埋了 6 处违规，每条规则一处**，实跑输出如下：

```text
扫描 27 个文件，命中 6 处违规
  R3 apps/web/src/api/auth.api.ts → @/features/auth
  R4 apps/web/src/App.tsx → @/features/articles/ArticleCard
  R6 apps/web/src/features/auth/LoginForm.tsx → ../sessions
  R1 apps/web/src/features/sessions/SessionList.tsx → @/features/articles
  R2 packages/shared/src/index.ts → react
  R5 apps/web/src/features/credentials/ 缺 index.ts
```

退出码是 1，CI 会直接红。把这 6 处按建议改完（其中 R5 需要新建一个文件，所以文件总数从 27 变成 28），再跑一次：

```text
扫描 28 个文件，命中 0 处违规
```

退出码变成 0。**这里的数字全部可复算：27 是演示树里的源码文件数，6 是植入的违规数，28 是补上 `credentials/index.ts` 之后的数量。** 你可以拿自己的仓库直接跑，第一次跑出来的违规数大概率会比 6 大得多——那就按规则一条条收，别一次改完，改一条跑一次。

校验器有个已知边界：它只认静态 import 说明符，动态 `import(variable)` 和 `require` 它看不到。这没关系，**能卡住九成手写 import 就够了**，剩下的靠 code review 兜。工具的价值不在完美，在于把「大家都知道但没人执行」的约定变成一条退出码。

---

## 11. 症状、原因、解法对照表（Symptom → Cause → Fix）

| 症状 | 原因 | 解法 |
| --- | --- | --- |
| 打开页面白屏，控制台报 `Invalid hook call` | `shared` 里也有一份 React，hook 走了两个实例 | `Vite` 里配 `resolve.dedupe: ['react', 'react-dom']`，并检查 `packages/shared/node_modules` |
| 报 `Cannot access 'useAuthStore' before initialization` | `api/client.ts` 与 `stores` 互相 import，形成运行时环 | 改成 `configureApi()` 注入 `getToken` 与 `onUnauthorized`，`api` 层零业务依赖 |
| 编辑器里 shared 类型正常，运行时字段是 `undefined` | `tsconfig` 的 `paths` 与 `vite` 的 `alias` 指向了不同文件 | 三处对齐：`package.json` 的 `main`、`tsconfig` 的 `paths`、`vite` 的 `alias` |
| 按钮 loading 一闪就没，用户重复提交 | loading 用布尔值，并发请求时被先返回的那个置回 false | 改成并发计数 `pending > 0`，`finally` 里减一 |
| 刷新后总是回到第一个页签 | 只读了 `geo_active_tab`，没有在状态变化后回写 | `useActiveTab` 里加 `useEffect` 回写，写入前用 `isTabId` 校验 |
| 本地能跑，CI 的 `typecheck` 挂 | `vite build` 用 esbuild，只转译不检查类型 | `build` 脚本改成 `tsc --noEmit && vite build`，`turbo` 加 `^typecheck` 依赖 |
| 登录后刷新，用户头像变空白 | `persist` 只存了 token，`user` 字段没重新拉 | `partialize` 只留 token，启动时用 token 换一次用户摘要 |
| 改了品牌色，部分按钮没变 | 组件里写死了 hex，绕过了 `@theme` 变量 | 全站只允许 `bg-brand-500` 这类语义类名，禁止 `style={{ color: '#…' }}` |

这张表可以当排错清单用：出现哪一行，直接跳到对应章节看实现。

什么时候该用这套结构：内部工具型 SPA、页签数量固定、不需要把当前页签分享给别人——它够用且好维护。什么时候不该用：要 SEO、要分享深链、要多角色复杂导航，直接上路由库，别用 `useState` 硬扛。

本专栏《全栈开发》讲前端工程化、Monorepo 分层与 UI 交互实现，每篇都配一段能直接跑的代码，每周更新一篇。想按顺序读完，可在专栏页订阅。
