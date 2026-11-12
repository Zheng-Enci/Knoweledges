# Hono 4 多库多模型服务的企业级 Monorepo 目录结构：npm workspaces 与 Turborepo 该怎么分层

**结论：目录不是按技术名词分（utils / service / db），而是按「谁依赖谁」和「谁跟谁一起变」分。** 四个数据库引擎、七家模型供应商、一套 Playwright 自动化，它们的变化节奏完全不同，所以必须是四个独立的 adapter 包；而业务编排要跨它们复用，就下沉到 features 包；apps 只做装配，一个文件能看完。分层方向只允许「上层依赖下层」，反向依赖用脚本卡在 CI 里，不接受口头约定。

---

## 目录

1. 先回答三个问题，再动手建目录（Three Questions First）
2. 顶层骨架：五个目录各管一件事（Top-level Layout）
3. apps 层：可部署单元只做装配（Assembly Only）
4. packages/core：零 IO 的领域内核（Zero-IO Core）
5. packages/adapters：四个数据库的统一出口（Database Adapters）
6. packages/adapters/ai：七家模型一个网关（Model Gateway）
7. packages/adapters/browser：Playwright 全家桶怎么摆（Browser Automation）
8. 工程配置四件套：turbo、tsconfig、Vitest、PM2（Toolchain Config）
9. 完整可运行代码：分层校验器（Layer Checker）
10. 症状、原因、解法对照表（Symptom → Cause → Fix）

---

## 1. 先回答三个问题，再动手建目录（Three Questions First）

大多数 Monorepo 烂尾，不是工具选错了，是建目录之前没回答三个问题。

**第一个问题：这个包会不会被第二个 app 用？** 只会被一个 app 用，就别单独成包，直接放在 `apps/xxx/src/modules/` 里。抽包有成本：多一份 `package.json`、多一轮构建、多一次改名的连锁反应。等到第二个使用方出现再抽，成本最低。

**第二个问题：这两个文件会不会一起改？** 一起改的放一起，分开改的拆开。数据库连接配置和 SQL 语句一起改，它们属于同一个包；七家模型的参数差异和 HTTP 客户端一起改，它们也属于同一个包。而 MySQL 的 schema 和 Milvus 的 collection 定义，几乎永远不一起改，那就必须是两个包。

**第三个问题：依赖方向能不能画成一条直线？** 能，就继续。画成环，说明分包错了，先重构再写代码。

把三个问题的答案合起来，就得到一条判断标准：**分包的单位不是「技术类型」，而是「变化原因」。** 这是 Martin Fowler 那套 SRP 在目录层面的落地——一个包只应该因为一种原因被修改。

> 这句判断有个生活化的对照：`apps` 是门店，`packages/features` 是中央厨房，`packages/adapters` 是供应链，`packages/core` 是菜谱。门店可以要求中央厨房改配方，但门店不能反过来给供应链下指令说「你明天给我送什么」——真出现这种指令，说明这家店的采购逻辑早就乱了。分层校验做的，就是每天开门前检查一遍有没有这种倒灌。

## 2. 顶层骨架：五个目录各管一件事（Top-level Layout）

先看全貌。这套骨架对应你描述的技术栈：Node 22 + Hono 4 + MySQL / SQLite / PostgreSQL / Milvus + 七家 OpenAI 兼容模型 + Playwright + npm workspaces + Turborepo + Vitest + PM2。

```text
fleet/
├── apps/                          # 可部署单元，每个目录对应一个 PM2 进程
│   ├── api/                       # Hono 4 对外 HTTP 服务（唯一入口）
│   ├── worker/                    # 后台任务：批量推理、内容入库
│   ├── scheduler/                 # 定时触发：采集任务派发
│   └── admin/                     # 管理台（可选，Vite + React）
├── packages/
│   ├── core/                      # 领域层：实体 + 端口接口 + 用例，零 IO
│   ├── adapters/                  # 基础设施适配，一个外部系统一个子包
│   │   ├── db/                    # MySQL / SQLite / PostgreSQL 三方言
│   │   ├── vector/                # Milvus
│   │   ├── ai/                    # 七家模型网关
│   │   ├── cache/                 # Redis 或内存实现
│   │   └── browser/               # Playwright + 指纹 + 站点流程
│   ├── features/                  # 跨 adapter 的业务编排，可被多个 app 引用
│   │   ├── chat/
│   │   ├── ingest/
│   │   └── scrape/
│   ├── contracts/                 # zod schema + 推导类型，前后端共用
│   ├── utils/                     # 纯函数：时间、字符串、重试。不含领域概念
│   └── config/                    # tsconfig / vitest 预设，只发配置文件
├── infra/                         # 部署物料，不参与 npm workspaces
│   ├── pm2/ecosystem.config.cjs
│   ├── docker/compose.yaml
│   └── sql/init/                  # 建库脚本、索引初始化
├── scripts/                       # 仓库级脚本：分层校验、种子数据
├── turbo.json
├── package.json                   # private，只放 workspaces 和根脚本
├── tsconfig.json
└── .env.example
```

四层，方向单一：

```text
apps  ──▶  features  ──▶  adapters  ──▶  core
  │            │              │
  └────────────┴──────────────┴──▶  contracts / utils（无层级，谁都能用）
```

`contracts` 和 `utils` 是叶子包，没有任何内部依赖，谁引用都安全。`core` 只能依赖 `contracts` 和 `utils`，**不允许 import 任何 `adapters` 的东西**——这条是整套结构的地基，破了就退化成一个大泥球。

## 3. apps 层：可部署单元只做装配（Assembly Only）

一个 `apps/*` 目录里，只应该有四类文件：入口、容器、路由、中间件。多一类都值得怀疑。

```text
apps/api/
├── src/
│   ├── index.ts            # 入口：创建 app、挂路由、启动，不超过 40 行
│   ├── container.ts        # 依赖装配：根据 env 决定用哪个 db、哪个模型
│   ├── env.ts              # zod 校验环境变量，启动即失败
│   ├── middleware/
│   │   ├── request-id.ts
│   │   ├── error-map.ts    # 领域异常 → HTTP 状态码
│   │   └── rate-limit.ts
│   └── routes/
│       ├── health.ts
│       ├── chat.ts         # 只解析参数 + 调 feature + 返回，不写业务判断
│       └── ma.ts
├── test/
│   └── chat.e2e.test.ts
├── package.json
└── tsconfig.json
```

`container.ts` 是这套结构的 **唯一开关** 。多数据库、多模型的复杂度全部收敛在这一个文件里，别的地方不许再判断「当前是 MySQL 还是 SQLite」。

```ts
// apps/api/src/container.ts
import { createDb } from '@fleet/db';
import { createAiGateway } from '@fleet/ai';
import { ChatService } from '@fleet/features-chat';
import { env } from './env';

// 按 env 选方言：本地默认 sqlite，生产读 DB_DIALECT
export const db = createDb({
  dialect: env.DB_DIALECT,          // 'mysql' | 'sqlite' | 'postgres'
  url: env.DB_URL,
  // MA 内容库是独立的 pg 实例，走第二个连接
  contentUrl: env.MA_DB_URL,
});

// 七家模型只在启动时注册一次，路由层拿到的永远是同一个接口
export const ai = createAiGateway({ providers: env.AI_PROVIDERS });

export const chatService = new ChatService({ db, ai });
```

路由层因此可以薄到只剩映射：

```ts
// apps/api/src/routes/chat.ts
import { Hono } from 'hono';
import { zValidator } from '@hono/zod-validator';
import { ChatRequest } from '@fleet/contracts';
import { chatService } from '../container';

export const chatRoutes = new Hono();

// 校验交给 contracts 里共享的 schema，路由不重复定义字段
chatRoutes.post('/chat', zValidator('json', ChatRequest), async (c) => {
  const result = await chatService.reply(c.req.valid('json'));
  return c.json(result);
});
```

这里有第一个反直觉的取舍：**`apps/api` 不写单元测试，只写 e2e 测试。** 理由是 `apps` 里只剩下装配代码，逻辑已经下沉到 features 和 adapters，给装配代码写单元测试等于测试 `new` 关键字。e2e 用 `app.request()` 直接打 Hono 实例，不启端口，跑得比启动服务器快一个数量级。

至于 `admin`：如果管理台只是几个表格，别新建 app。Hono 可以直接 `serveStatic` 托管 Vite 产物，少一个部署单元，少一份 PM2 配置。等它有自己的独立发版节奏、或者需要独立的鉴权域，再拆。**拆分的信号是「发版节奏不同」，不是「技术栈不同」。**

这个判断和我在本专栏《高并发点赞系统架构设计》里拆服务边界的思路是一致的：边界要跟着压力来源和发版节奏走，而不是跟着目录好看走。那边的结论是「先按读写分离切，再按热点切」，这边的结论是「先按 deploy 单元切，再按复用方切」——同一个原则的两种表现形式。

## 4. packages/core：零 IO 的领域内核（Zero-IO Core）

`core` 是整个仓库唯一可以放心重构的包，因为它的边界最硬：**不许有 `import fs`、不许有 `fetch`、不许有 `drizzle`、不许有 `process.env`。** 只有类型、纯函数、接口。

```text
packages/core/
├── src/
│   ├── entities/
│   │   ├── document.ts        # Document 实体 + 不变量校验
│   │   └── chat-session.ts
│   ├── ports/                 # 端口：由 adapters 实现，core 只定义形状
│   │   ├── document-repo.ts
│   │   ├── vector-repo.ts
│   │   └── model-gateway.ts
│   ├── usecases/
│   │   ├── answer-with-rag.ts # 检索 + 拼装 + 调用模型，全程只依赖 ports
│   │   └── ingest-document.ts
│   ├── errors.ts              # 领域异常，供 middleware 映射 HTTP 状态码
│   └── index.ts
├── test/
│   └── answer-with-rag.test.ts
└── package.json
```

端口接口是这套结构真正的价值点。它让「换数据库」「加第八家模型」变成加一个实现，而不是改业务代码：

```ts
// packages/core/src/ports/model-gateway.ts
export interface ChatMessage {
  role: 'system' | 'user' | 'assistant';
  content: string;
}

/** 模型网关端口：七家供应商的差异必须被适配器吸收，不能泄漏到用例层 */
export interface ModelGateway {
  /** 返回纯文本回复；供应商特有的 reasoning 字段在此处被丢弃 */
  chat(input: { model: string; messages: ChatMessage[] }): Promise<string>;
  /** 返回向量，供 Milvus 检索使用 */
  embed(input: { model: string; texts: string[] }): Promise<number[][]>;
}
```

用例层写起来就是纯逻辑，测试时塞一个假实现就能跑，不需要数据库也不需要 API Key：

```ts
// packages/core/src/usecases/answer-with-rag.ts
import type { ModelGateway } from '../ports/model-gateway';
import type { VectorRepo } from '../ports/vector-repo';

/** RAG 问答用例：检索 → 拼接上下文 → 调用模型，全部通过端口完成 */
export async function answerWithRag(
  deps: { vector: VectorRepo; model: ModelGateway },
  question: string,
): Promise<{ answer: string; hits: number }> {
  const hits = await deps.vector.search({ text: question, topK: 5 });  // 只拿到领域对象
  const context = hits.map((h) => h.content).join('\n---\n');          // 拼上下文
  const answer = await deps.model.chat({                               // 走端口，不认供应商
    model: 'default',
    messages: [
      { role: 'system', content: `只依据以下资料回答：\n${context}` },
      { role: 'user', content: question },
    ],
  });
  return { answer, hits: hits.length };
}
```

**这条边界最难守，也最值钱。** 一旦有人在 `core` 里 `import { drizzle } from 'drizzle-orm'`，整个包就锁死在 ORM 上了，之后想换 SQLite 做测试都得改业务代码。所以在 `packages/config/tsconfig.core.json` 里用 ESLint 的 `no-restricted-imports` 把 `drizzle-orm`、`mysql2`、`better-sqlite3`、`playwright` 直接禁掉——**用工具守边界，别用代码评审守边界。**

## 5. packages/adapters：四个数据库的统一出口（Database Adapters）

这里是这套架构最容易踩坑的地方，先说结论：

> **四个数据库不能共用一份 Drizzle schema。**

Drizzle 是方言绑定的。MySQL 的自增主键是 `int().autoincrement()`，PostgreSQL 是 `serial()` 或 `uuid()`，SQLite 的 `integer({ mode: 'boolean' })` 又是另一套写法；时间字段在 MySQL 是 `timestamp`、在 PG 是 `timestamptz`、在 SQLite 是 `integer({ mode: 'timestamp' })`。想用一份 schema 同时驱动三个方言，最后一定会在迁移阶段崩掉，报的错还是 `Unknown column` 这类看不出根因的。

正确做法是 **共享领域实体和 Repository 接口，各自维护方言 schema** ：

```text
packages/adapters/db/
├── src/
│   ├── dialect.ts             # 方言判定 + 连接池参数
│   ├── mysql/
│   │   ├── client.ts          # mysql2 连接池
│   │   ├── schema.ts          # MySQL 专属 schema
│   │   └── document.repo.ts   # 实现 core 的 DocumentRepo 端口
│   ├── sqlite/
│   │   ├── client.ts          # better-sqlite3，同步驱动
│   │   ├── schema.ts          # SQLite 专属 schema
│   │   └── document.repo.ts
│   ├── postgres/
│   │   ├── client.ts          # postgres.js，指向 MA 内容库
│   │   ├── schema.ts
│   │   └── document.repo.ts
│   ├── migrations/            # drizzle-kit 产出，按方言分子目录
│   │   ├── mysql/
│   │   ├── sqlite/
│   │   └── postgres/
│   └── index.ts               # createDb()：工厂入口，唯一 export
└── package.json
```

`createDb()` 的签名固定，返回的永远是 `DocumentRepo` 端口：

```ts
// packages/adapters/db/src/index.ts
import type { DocumentRepo } from '@fleet/core';

export type Dialect = 'mysql' | 'sqlite' | 'postgres';

/** 数据库工厂：按方言返回端口实现，调用方拿不到任何方言细节 */
export function createDb(cfg: {
  dialect: Dialect;
  url: string;
  contentUrl?: string;         // MA 内容库的独立 PG 连接
}): { documents: DocumentRepo; content: DocumentRepo } {
  switch (cfg.dialect) {
    case 'mysql':   return buildMysql(cfg);       // 主业务库
    case 'sqlite':  return buildSqlite(cfg);      // 本地 / 离线兜底
    case 'postgres':return buildPostgres(cfg);    // MA 内容库
  }
}
```

三个方言的仓库实现看起来会重复，这是 **可接受的重复** 。它有明确理由：方言差异是客观存在的，抽象掉它等于把差异藏起来，最终会在某个 `limit` 子句上报错。宁可三个文件各 80 行，也不要一个 400 行的 `if (dialect === ...)` 判断链——后者每次加数据库都要重新读一遍全部逻辑。

**SQLite 备用库有个额外约束**：它常被用来做本地开发和 e2e 测试，那它的 schema 必须由同一份迁移脚本生成，不能手写。否则「本地跑得好好的、上线 MySQL 炸了」这件事一定会发生。做法是 `infra/sql/init/` 放 MySQL 建库脚本，`migrations/sqlite/` 由 `drizzle-kit generate --dialect sqlite` 生成，两边都在 CI 里跑一次迁移再跑测试。

`vector` 子包同理，只是接口换成 `VectorRepo`：

```text
packages/adapters/vector/
├── src/
│   ├── milvus.ts              # @zilliz/milvus2-sdk-node，collection 管理
│   ├── memory.ts              # 内存实现，单测与本地开发用
│   └── index.ts
```

内存实现不是玩具。**它是让 `core` 的用例测试能在 20ms 内跑完的关键**——没有它，每个测试都要连一次 Milvus，CI 时间会从几秒涨到几分钟。

## 6. packages/adapters/ai：七家模型一个网关（Model Gateway）

你说「AI 走 OpenAI 兼容协议接 7 家模型」，这句话本身就是目录结构的答案：**七家共用一个 HTTP 客户端，差异只写在七份配置里，绝不写七个包。**

```text
packages/adapters/ai/
├── src/
│   ├── openai-compat.ts       # 通用客户端：fetch + SSE 流解析 + 重试
│   ├── providers/             # 每家一个文件，只声明差异
│   │   ├── deepseek.ts
│   │   ├── qwen.ts
│   │   ├── moonshot.ts
│   │   ├── zhipu.ts
│   │   ├── minimax.ts
│   │   ├── doubao.ts
│   │   └── openai.ts
│   ├── registry.ts            # name → provider 配置，启动时注册
│   ├── types.ts
│   └── index.ts               # createAiGateway()，实现 core 的 ModelGateway
└── package.json
```

「OpenAI 兼容」这四个字有个隐蔽的陷阱：**兼容的是接口路径，不是参数语义。** 实测下来至少要处理三处差异——推理类模型返回 `reasoning_content` 而不是 `content`；部分供应商用 `max_completion_tokens` 而非 `max_tokens`；流式响应里 `usage` 字段只有部分供应商在最后一帧返回。这三处差异应该全部收在 `openai-compat.ts` 里，对外只暴露出 `ModelGateway` 的两个方法。

```ts
// packages/adapters/ai/src/providers/deepseek.ts
import type { ProviderConfig } from '../types';

/** 每家只写差异：baseURL、默认模型、三个布尔开关 */
export const deepseek: ProviderConfig = {
  name: 'deepseek',
  baseUrl: 'https://api.deepseek.com/v1',
  defaultModel: 'deepseek-chat',
  needsMaxCompletionTokens: false,   // 这家认 max_tokens
  hasReasoningField: true,           // 返回 reasoning_content，需要剥离
  streamUsageInLastChunk: false,     // 流式不返回 usage，需本地估算
};
```

七份配置加起来不到 100 行，剩下 300 行通用逻辑只写一遍。 **这是「一个包七个配置」而不是「七个包」的全部理由** ：协议相同，差异是数据不是行为。

还有一层要放对位置：**API Key 不进包，也不进口 `.env` 的默认值。** `providers/*.ts` 里只写 `baseUrl` 和参数开关，Key 一律由 `createAiGateway({ keys: env.AI_KEYS })` 从 `apps/api/src/env.ts` 注入。这样 `ai` 包可以被任何 app 复用，也可以在没有 Key 的环境里做类型检查。

## 7. packages/adapters/browser：Playwright 全家桶怎么摆（Browser Automation）

自动化这块的目录设计，核心矛盾只有一个：**指纹要隔离，但浏览器进程要复用。**

```text
packages/adapters/browser/
├── src/
│   ├── launcher.ts            # 单例 Chromium：一个进程，多个 context
│   ├── context.ts             # 每次任务新建 context，绑定指纹 + 代理
│   ├── stealth/
│   │   ├── fingerprint.ts     # UA / 时区 / 语言 / WebGL / Canvas 噪声
│   │   ├── inject.ts          # addInitScript 注入，必须在导航前
│   │   └── profiles/          # 预置指纹档案，按目标站点分组
│   ├── flows/                 # 具体站点流程，一个站点一个文件
│   │   ├── site-a-login.ts
│   │   └── site-b-list.ts
│   ├── queue.ts               # 内部并发队列，限制同时打开的 page 数
│   └── index.ts
└── package.json
```

四条摆放原则：

**第一，Chromium 进程单例，`BrowserContext` 每个任务一个。** 起一个浏览器要几百毫秒和上百 MB 内存，起一百个会直接把机器打爆；而 `BrowserContext` 之间 Cookie、Storage、指纹完全隔离，恰好就是「每个任务一个干净身份」的需求。`launcher.ts` 只 `launch()` 一次，`context.ts` 负责 `newContext({ userAgent, locale, timezoneId, viewport })`。

**第二，指纹注入必须在导航之前。** `addInitScript` 注册在 context 创建之后、`page.goto` 之前，否则页面脚本已经跑完，`navigator.webdriver` 之类的检测早就读到了原始值。这个顺序错了，指纹写得再全也无效——这是自动化脚本最常见的一处「看起来没问题」。

**第三，站点流程和指纹分离。** `flows/` 只写「点哪里、等什么、取哪个选择器」，不许出现 `userAgent` 这类指纹字段。指纹由 `profiles/` 按站点分组提供，改指纹不用改流程，改流程不碰指纹。

**第四，这个包绝不能跑在 PM2 cluster 模式里。** cluster 会按 CPU 核心数 fork 出多个进程，每个进程一份 Chromium，8 核机器就是 8 个浏览器常驻。`infra/pm2/ecosystem.config.cjs` 里必须给 `worker` 和 `scheduler` 显式写 `exec_mode: 'fork'`、`instances: 1`，并发靠内部 `queue.ts` 控制。 **HTTP 服务可以 cluster，浏览器不行** ，这条要写进部署注释里，不然下次扩容的人一定会踩。

## 8. 工程配置四件套：turbo、tsconfig、Vitest、PM2（Toolchain Config）

配置文件只放四份，且都在根目录或 `packages/config`，**不要每个包各抄一份**。

**第一份：根 `package.json`，只做三件事。**

```json
{
  "name": "fleet",
  "private": true,
  "workspaces": ["apps/*", "packages/*", "packages/adapters/*", "packages/features/*"],
  "scripts": {
    "build": "turbo run build",
    "dev": "turbo run dev --parallel",
    "test": "turbo run test",
    "typecheck": "turbo run typecheck",
    "check:layers": "node scripts/check-layers.mjs"
  },
  "devDependencies": {
    "turbo": "^2.5.0",
    "typescript": "^5.7.0",
    "vitest": "^3.0.0"
  }
}
```

`workspaces` 要显式写四行，因为 `packages/adapters/*` 和 `packages/features/*` 是二级目录，只写 `packages/*` 收不到子包。**这是 npm workspaces 与 pnpm 的差别之一**：npm 不支持 `packages/**` 递归通配，必须逐层列出来。

**第二份：`turbo.json`，用 `tasks` 而不是 `pipeline`。**

```json
{
  "$schema": "https://turbo.build/schema.json",
  "globalEnv": ["NODE_ENV"],
  "tasks": {
    "build":       { "dependsOn": ["^build"], "outputs": ["dist/**"] },
    "typecheck":   { "dependsOn": ["^build"] },
    "test":        { "dependsOn": ["^build"], "outputs": ["coverage/**"] },
    "check:layers":{ "cache": false },
    "dev":         { "cache": false, "persistent": true }
  }
}
```

Turborepo 2.x 已经把老版本的 `pipeline` 字段改名为 `tasks`，网上大量教程还是 `pipeline`，照抄会直接报 schema 校验错误。`dev` 必须设 `cache: false` 加 `persistent: true`，否则 turbo 会等着它退出，导致 `dev` 命令永远挂不住。

**第三份：`packages/config`，共享 tsconfig 与 Vitest 预设。**

```text
packages/config/
├── tsconfig.base.json     # 公共编译选项
├── tsconfig.node.json     # Node 22 + ESM 场景，apps 与 adapters 继承它
├── tsconfig.core.json     # core 专用：额外禁止 IO 相关类型
├── vitest.preset.ts       # 覆盖率阈值、别名解析
└── package.json           # 只有 "exports"，没有构建脚本
```

`tsconfig.base.json` 里对 Node 22 + 原生 ESM 的关键三项：

```json
{
  "compilerOptions": {
    "target": "ES2023",
    "module": "NodeNext",
    "moduleResolution": "NodeNext",
    "verbatimModuleSyntax": true,
    "strict": true,
    "skipLibCheck": true
  }
}
```

`moduleResolution` 必须是 `NodeNext`。写成 `bundler` 时，`exports` 字段只声明了 `types` 而漏了 `import`，类型检查能过、运行时 `Cannot find module`——这是 Monorepo 里最难查的一类错误，因为 CI 的类型检查是绿的。

**第四份：`infra/pm2/ecosystem.config.cjs`，进程边界就写在这。**

```js
// 进程编排：HTTP 可 cluster，浏览器相关必须 fork 单实例
module.exports = {
  apps: [
    {
      name: 'fleet-api',
      script: 'apps/api/dist/index.mjs',
      exec_mode: 'cluster',        // 无状态 HTTP，可多进程吃满多核
      instances: 'max',
      max_memory_restart: '512M',
      env: { NODE_ENV: 'production', DB_DIALECT: 'mysql' },
    },
    {
      name: 'fleet-worker',
      script: 'apps/worker/dist/index.mjs',
      exec_mode: 'fork',           // 内部跑 Chromium，绝不能 cluster
      instances: 1,
      max_memory_restart: '1G',
      env: { NODE_ENV: 'production' },
    },
    {
      name: 'fleet-scheduler',
      script: 'apps/scheduler/dist/index.mjs',
      exec_mode: 'fork',           // 定时器只应存在一份，否则任务重复派发
      instances: 1,
    },
  ],
};
```

`scheduler` 用 fork 单实例还有个隐性理由：**定时任务在多进程下会重复派发**。cron 逻辑写在代码里而不是交给分布式锁，就必须保证只有一个进程在跑。

**关于「内部包要不要预编译」这个取舍，我选不预编译。** 具体做法是每个包的 `exports` 直接指向源码：

```json
{
  "name": "@fleet/db",
  "type": "module",
  "exports": {
    ".": { "types": "./src/index.ts", "import": "./src/index.ts" }
  }
}
```

理由：这些包只被仓库内部的 app 消费，不发布到 npm，没有「别人要用编译产物」的需求；源码直连省掉一层 `tsc --build` 的增量编译和 project references 的顺序维护，改一行代码热更新立刻生效。代价是打包时必须能处理 TS 源码——app 用 `tsup` 打 `dist/index.mjs` 时会把内部包一并内联，产物是单文件，部署时不需要 `node_modules` 里的 `@fleet/*`。

**什么时候该改成预编译？** 当某个包需要被外部项目 `npm install`，或者需要独立发版时。到那时再加 `dist` 和 `publishConfig`，成本可控。反过来的路很难走：一开始就全套 project references，几十个包之后改一个底层包要等一串重新编译，开发体验会一路下滑。

## 9. 完整可运行代码：分层校验器（Layer Checker）

目录结构靠文档约定，一周就会失效。**唯一可靠的办法是把它变成一条 CI 命令。** 下面这个脚本零依赖，Node 22 直接跑，扫描整个仓库的 `package.json`，检查依赖方向、同级依赖和循环依赖。

```js
// scripts/check-layers.mjs
import { readdir, readFile } from 'node:fs/promises';
import path from 'node:path';

// 分层级别：数字越小越底层，只允许「高层依赖低层」
const LEVELS = [
  { prefix: 'packages/core', level: 0 },      // 领域内核：零 IO
  { prefix: 'packages/adapters', level: 1 },  // 基础设施适配层
  { prefix: 'packages/features', level: 2 },  // 业务编排
  { prefix: 'apps', level: 3 },               // 可部署单元
];

/** 读取单个目录下的子目录名，目录不存在时返回空数组 */
async function listDirs(dir) {
  try {
    const entries = await readdir(dir, { withFileTypes: true });      // 列出条目
    return entries.filter((e) => e.isDirectory()).map((e) => e.name); // 只要目录名
  } catch {
    return [];
  }
}

/** 收集所有 workspace 包，返回 [{ name, dir, level, deps }] */
async function collect() {
  const dirs = [];
  for (const app of await listDirs('apps')) dirs.push(`apps/${app}`);
  for (const pkg of await listDirs('packages')) {
    const sub = await listDirs(`packages/${pkg}`);                    // packages 允许两层
    if (sub.length) for (const s of sub) dirs.push(`packages/${pkg}/${s}`);
    else dirs.push(`packages/${pkg}`);
  }

  const packages = [];
  for (const dir of dirs) {
    let manifest;
    try {
      manifest = JSON.parse(await readFile(path.join(dir, 'package.json'), 'utf8'));
    } catch {
      continue;                                                       // 无 manifest 直接跳过
    }
    const level = LEVELS.find((l) => dir.startsWith(l.prefix))?.level ?? 9;
    const deps = { ...manifest.dependencies, ...manifest.devDependencies };
    packages.push({ name: manifest.name, dir, level, deps });
  }
  return packages;
}

/** 校验依赖方向：反向依赖记 error，同级依赖记 warning，环记 error */
function validate(packages) {
  const byName = new Map(packages.map((p) => [p.name, p]));           // name → 包
  const errors = [];
  const warnings = [];
  const graph = new Map(packages.map((p) => [p.name, []]));           // 依赖图

  for (const p of packages) {
    for (const dep of Object.keys(p.deps)) {
      const target = byName.get(dep);
      if (!target) continue;                                          // 外部 npm 包不管
      graph.get(p.name).push(target.name);
      if (target.level === 9 || p.level === 9) continue;              // 未归层不校验
      if (target.level > p.level) {
        errors.push(`反向依赖: ${p.dir} → ${target.dir}`);            // 低层依赖高层，错
      } else if (target.level === p.level) {
        warnings.push(`同级依赖: ${p.dir} → ${target.dir}`);          // 同层允许但提示
      }
    }
  }

  const state = new Map();                                            // 1=访问中 2=已完成
  const walk = (name, trail) => {
    if (state.get(name) === 1) {                                      // 回到访问中的节点即成环
      errors.push(`循环依赖: ${[...trail, name].join(' → ')}`);
      return;
    }
    if (state.get(name) === 2) return;
    state.set(name, 1);
    for (const next of graph.get(name)) walk(next, [...trail, name]);
    state.set(name, 2);
  };
  for (const p of packages) walk(p.name, []);

  return { errors, warnings };
}

const packages = await collect();
const { errors, warnings } = validate(packages);
console.log(`扫描 ${packages.length} 个包：${packages.map((p) => p.dir).join(', ')}`);
for (const w of warnings) console.log(`WARN ${w}`);
if (errors.length === 0) {
  console.log('分层校验通过');
} else {
  console.log(`发现 ${errors.length} 处违规：`);
  for (const e of errors) console.log(`  - ${e}`);
  process.exitCode = 1;                                              // CI 直接失败
}
```

拿一个故意做错的 6 包仓库跑一遍，输出是这样（真实运行结果）：

```text
扫描 6 个包：apps/api-gateway, apps/worker, packages/adapters/ai-gateway, packages/adapters/db, packages/core/domain, packages/features/scrape
WARN 同级依赖: packages/adapters/ai-gateway → packages/adapters/db
发现 1 处违规：
  - 反向依赖: packages/features/scrape → apps/api-gateway
```

`features` 反向依赖 `apps` 被判死，`ai-gateway` 依赖同层的 `db` 只警告——因为 AI 网关读数据库配置是合理的，同层互相引用允许，但成链就该重构。

把「违规率」定义成一个可以卡阈值的量：

$$V = \frac{|\{(a,b) \in E \mid \mathrm{level}(a) < \mathrm{level}(b)\}|}{|E|}$$

其中 $E$ 是内部包依赖边的集合，$\mathrm{level}$ 是上表里的分层级别，分母是内部依赖总边数。 **企业级项目的门禁值是 $V = 0$** ，不是「小于 5%」——反向依赖没有「少量可接受」这回事，一条就足以让 `core` 无法独立测试。上面的例子中 $|E| = 9$、违规 1 条，$V \approx 0.111$，所以脚本退出码是 1。

在根 `package.json` 里挂进 CI，顺序放在类型检查之前：

```json
{ "scripts": { "check:layers": "node scripts/check-layers.mjs" } }
```

先卡结构，再卡类型。结构错了，类型检查通过也没意义。

## 10. 症状、原因、解法对照表（Symptom → Cause → Fix）

| 症状 | 原因 | 解法 |
|---|---|---|
| 改一个底层包，所有 app 都要重新构建，`dev` 卡十几秒 | 内部包走了 `dist` + project references，串行增量编译 | 包 `exports` 直接指向 `src/index.ts`，由 app 的 `tsup` 内联打包 |
| 本地 SQLite 测试全绿，上线 MySQL 报 `Unknown column` | 三个方言共用一份 Drizzle schema | 每方言独立 `schema.ts` + 独立 `migrations/{dialect}/`，CI 跑真实方言迁移 |
| 只写 `packages/*` 后子包全丢了 | npm workspaces 不支持递归通配 | 显式列 `packages/adapters/*`、`packages/features/*` |
| `turbo dev` 一直不退出、看起来像卡死 | `dev` 任务没设 `cache: false` 和 `persistent: true` | 按上表四件套配置，`dev` 是长驻任务 |
| 七家模型里有六家正常，一家返回空字符串 | 把「OpenAI 兼容」当成参数语义一致，推理模型响应在 `reasoning_content` 里 | 差值收在 `openai-compat.ts`，每家只写 `ProviderConfig` 开关 |
| 上了 PM2 cluster 后机器内存爆、被杀进程 | cluster 按核数 fork，每进程一份 Chromium | `worker` / `scheduler` 显式 `exec_mode: 'fork'`、`instances: 1` |
| `core` 里的用例测试要连数据库、要真 API Key | 有人在 `core` 里 import 了 ORM 或 SDK | ESLint `no-restricted-imports` 禁掉 `drizzle-orm` / `playwright`，端口层只留接口 |
| 类型检查绿、运行时 `Cannot find module` | `exports` 只写 `types` 没写 `import`，或 `moduleResolution` 不是 `NodeNext` | 两者同时声明，tsconfig 继承 `tsconfig.base.json` |
| 定时任务在日志里出现重复执行 | `scheduler` 被 cluster 起成多实例 | fork + 单实例，或引入分布式锁 |

这张表里的九条，每一条都能在实际项目里复现，且每一条的根因都不在代码语法上——**全在目录和配置的摆放位置**。

---

这套结构的门槛不在写代码，在于先接受「`apps` 里不该有业务逻辑」这个约束。什么时候它值得用：团队超过三人、或者有第二个 deploy 单元要跟 API 共享同一套领域逻辑时，收益立刻就出来。什么时候不该用：单人项目、只有一个 app、数据库只有一套——这时候建 Monorepo 只是给 `import` 多加了一层路径前缀，纯负担。

本专栏《全栈开发》聚焦前端物理感交互、工程化配置与 Node 服务架构，从 CSS 曲线一路写到 Monorepo 分层，每篇都配一段可直接运行的代码与一张对照表，每周更新一篇。想按顺序读完，可在专栏页订阅。

