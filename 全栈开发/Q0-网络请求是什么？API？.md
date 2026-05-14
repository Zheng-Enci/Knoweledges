# Q0-网络请求是什么？API？🌐

本文档从零讲解网络请求和 API 的核心概念，涵盖什么是 API、HTTP 协议基础、RESTful 设计风格、常见的 HTTP 请求方法、现代网络请求 API（Fetch、XMLHttpRequest、Axios）的对比，以及完整的代码示例。通过通俗易懂的方式，帮助读者建立对网络通信的系统性认知 🧠

## 章节阅读路线图 🗺️

```mermaid
flowchart LR
    A["1. 什么是 API"]:::api --> B["2. HTTP 协议基础"]:::http
    B --> C["3. RESTful API 设计"]:::rest
    C --> D["4. HTTP 请求方法详解"]:::method
    D --> E["5. 网络请求 API 技术对比"]:::tech
    E --> F["6. 完整代码示例"]:::example
    F --> G["7. 大模型 API 接口"]:::llm
    G --> H["8. 总结"]:::summary

    classDef api fill:#e3f2fd,stroke:#1565c0
    classDef http fill:#fff3e0,stroke:#ef6c00
    classDef rest fill:#e8f5e9,stroke:#2e7d32
    classDef method fill:#f3e5f5,stroke:#6a1b9a
    classDef tech fill:#fce4ec,stroke:#c62828
    classDef example fill:#fff8e1,stroke:#f9a825
    classDef llm fill:#e0f7fa,stroke:#006064
    classDef summary fill:#eceff1,stroke:#546e7a
```

**阅读顺序说明**：

- **第1章 → 第2章**：先理解 API 是什么，再学习底层通信协议 HTTP
- **第2章 → 第3章**：掌握 HTTP 后，了解如何设计优雅的 API 接口
- **第3章 → 第4章**：学习 RESTful 设计后，深入理解各种请求方法的区别
- **第4章 → 第5章**：理解理论后，对比前端常用的网络请求技术
- **第5章 → 第6章**：把所有内容整合成可运行的代码示例
- **第6章 → 第7章**：学习当前最火爆的大模型 API，发现它本质上也是 RESTful API

---

## 1. 什么是 API 🤔

> 本章解释 API 的核心概念和作用

### 1.1 API 的本质 💡

**API（Application Programming Interface，应用程序编程接口）** 是两个系统之间进行通信的"契约"或"桥梁"。

**通俗理解**：想象你去餐厅吃饭——

- **你（客户端）**：想吃一道菜，但不会自己做
- **服务员（API）**：接收你的点单，告诉厨房，再把菜端给你
- **厨房（服务器）**：真正做菜的地方，但你不需要知道它怎么做

你不需要知道厨房的运作细节，只需要通过服务员（API）告诉厨房你想要什么，就能得到结果。这就是 API 的核心思想：**封装复杂性，提供简单接口**。

**参考资料：**

- [什么是 API？ -- AWS](https://aws.amazon.com/cn/what-is/api/) ⭐值得阅读
- [什么是应用程序编程接口 (API)？ -- IBM](https://www.ibm.com/cn-zh/topics/api) ⭐值得阅读

### 1.2 Web API 的工作原理 🌍

在互联网世界中，Web API 通常指 **通过网络（HTTP/HTTPS）调用的接口**。当你打开浏览器访问网页时，背后发生了以下过程：

```
浏览器（客户端） → 发送 HTTP 请求 → 服务器
浏览器（客户端） ← 接收 HTTP 响应 ← 服务器
```

**一个真实的例子**：

当你在淘宝搜索"手机"时：
1. 浏览器向淘宝服务器发送请求：`GET https://search.taobao.com?q=手机`
2. 服务器查询数据库，找到相关商品
3. 服务器返回 JSON 格式的数据：`{"products": [{"name": "iPhone 15", "price": 5999}, ...]}`
4. 浏览器解析数据，渲染成网页展示给你

这个过程就是 **网络请求**，而淘宝提供的搜索接口就是一个 **Web API**。

**参考资料：**

- [Web API 是什么？ -- MDN](https://developer.mozilla.org/zh-CN/docs/Web/API)
- [什么是 Web API？ -- 菜鸟教程](https://www.runoob.com/w3cnote/what-is-web-api.html)

### 1.3 为什么需要 API？🎯

**1. 前后端分离**

现代 Web 开发中，前端（浏览器/手机 App）和后端（服务器）完全独立：
- 前端负责界面展示和用户交互
- 后端负责数据处理和业务逻辑
- API 是它们之间的唯一沟通渠道

**2. 数据复用**

同一个 API 可以被多个客户端调用：
- 网站 Web 端
- 手机 App（iOS/Android）
- 第三方开发者（开放 API）

**3. 服务集成**

不同系统通过 API 协同工作：
- 微信支付 API → 在电商网站接入支付功能
- 高德地图 API → 在 App 中显示地图
- OpenAI API → 在应用中集成 AI 能力

---

## 2. HTTP 协议基础 📡

> 本章讲解网络请求的底层通信协议

### 2.1 什么是 HTTP 📝

**HTTP（HyperText Transfer Protocol，超文本传输协议）** 是互联网上应用最广泛的一种网络协议。所有的 Web API 都建立在 HTTP 协议之上。

**HTTP 的核心特点**：

1. **请求-响应模型**：客户端发请求，服务器给响应
2. **无状态**：每次请求都是独立的，服务器不记住你（除非用 Cookie/Session）
3. **基于 TCP/IP**：底层使用 TCP 协议保证数据传输的可靠性

**参考资料：**

- [HTTP 协议入门 -- 阮一峰](http://www.ruanyifeng.com/blog/2016/08/http.html) ⭐值得阅读
- [HTTP 是什么？ -- MDN](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Overview)

### 2.2 HTTP 请求的组成部分 🔧

一个完整的 HTTP 请求包含以下部分：

```
GET /api/users/123 HTTP/1.1
Host: example.com
Authorization: Bearer token123
Content-Type: application/json
```

**拆解说明**：

| 部分 | 示例 | 说明 |
|------|------|------|
| **请求方法** | `GET` | 告诉服务器要做什么（获取/创建/更新/删除） |
| **请求路径** | `/api/users/123` | 资源的地址（URL 路径） |
| **HTTP 版本** | `HTTP/1.1` | 协议版本 |
| **请求头** | `Host: example.com` | 附加信息（认证、内容类型等） |
| **请求体** | （GET 请求没有） | POST/PUT 请求携带的数据 |

### 2.3 HTTP 响应的组成部分 📦

服务器返回的响应也类似：

```
HTTP/1.1 200 OK
Content-Type: application/json
Content-Length: 123

{
  "id": 123,
  "name": "张三",
  "email": "zhangsan@example.com"
}
```

**关键要素**：

| 部分 | 示例 | 说明 |
|------|------|------|
| **状态码** | `200 OK` | 请求结果（成功/失败/重定向等） |
| **响应头** | `Content-Type: application/json` | 响应元信息 |
| **响应体** | `{...}` | 实际返回的数据 |

**常见状态码**：

| 状态码 | 含义 | 使用场景 |
|--------|------|---------|
| 200 | 成功 | 请求成功 |
| 201 | 已创建 | POST 创建资源成功 |
| 400 | 请求错误 | 参数不正确 |
| 401 | 未授权 | 需要登录 |
| 403 | 禁止访问 | 没有权限 |
| 404 | 未找到 | 资源不存在 |
| 500 | 服务器错误 | 后端出 bug 了 |

**参考资料：**

- [HTTP 状态码 -- MDN](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Status)
- [HTTP 响应 -- MDN](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Messages)

---

## 3. RESTful API 设计 🎨

> 本章介绍现代 Web API 的主流设计风格

### 3.1 什么是 RESTful 🌟

**REST（Representational State Transfer，表现层状态转移）** 是一种设计 Web API 的架构风格，由 Roy Fielding 在 2000 年提出。遵循 REST 原则的 API 被称为 **RESTful API**。

**RESTful 的核心思想**：

1. **资源导向**：用 URL 表示资源（名词，不用动词）
2. **统一接口**：用 HTTP 方法表示操作（GET/POST/PUT/DELETE）
3. **无状态**：每次请求包含所有必要信息
4. **数据格式灵活**：支持 JSON、XML 等格式

### 3.2 RESTful 设计示例 📋

**❌ 不好的设计（非 RESTful）**：

```
GET /getUser?id=123
POST /createUser
POST /updateUser?id=123
POST /deleteUser?id=123
```

问题：
- URL 中包含动词（`get`、`create`）
- 所有操作都用 POST，语义不清晰
- 不符合资源导向原则

**✅ 好的设计（RESTful）**：

```
GET    /api/users/123      # 获取用户
POST   /api/users          # 创建用户
PUT    /api/users/123      # 更新用户
DELETE /api/users/123      # 删除用户
```

优势：
- URL 只包含资源名词（`users`）
- HTTP 方法清晰表达操作意图
- 符合 CRUD（增删改查）映射

**RESTful 与 CRUD 的对应关系**：

| CRUD 操作 | HTTP 方法 | URL 示例 | 说明 |
|-----------|-----------|---------|------|
| Create（创建） | POST | `POST /api/users` | 创建新用户 |
| Read（读取） | GET | `GET /api/users/123` | 获取指定用户 |
| Update（更新） | PUT | `PUT /api/users/123` | 更新用户信息 |
| Delete（删除） | DELETE | `DELETE /api/users/123` | 删除用户 |

**参考资料：**

- [什么是 RESTful API？ -- AWS](https://aws.amazon.com/cn/what-is/restful-api/) ⭐值得阅读
- [RESTful API 设计最佳实践 -- 阮一峰](http://www.ruanyifeng.com/blog/2014/05/restful_api.html) ⭐值得阅读
- [REST API 教程 -- 菜鸟教程](https://www.runoob.com/w3cnote/restful-architecture.html)

### 3.3 RESTful 设计规范 📏

**1. 使用名词复数**

```
✅ /api/users        # 好
❌ /api/user         # 不好
❌ /api/getUsers     # 不好（包含动词）
```

**2. 嵌套资源表示关系**

```
GET /api/users/123/orders        # 获取用户 123 的所有订单
GET /api/users/123/orders/456    # 获取用户 123 的订单 456
```

**3. 使用查询参数过滤**

```
GET /api/users?role=admin          # 获取所有管理员
GET /api/users?age_gt=18           # 获取年龄大于 18 的用户
GET /api/users?sort=-created_at    # 按创建时间倒序
```

**4. 版本控制**

```
/api/v1/users    # 第 1 版 API
/api/v2/users    # 第 2 版 API（兼容旧版）
```

---

## 4. HTTP 请求方法详解 🔧

> 本章深入讲解常用的 HTTP 方法及其区别

### 4.1 五大核心方法 📝

| 方法 | 用途 | 幂等性 | 安全性 | 示例 |
|------|------|--------|--------|------|
| **GET** | 获取资源 | ✅ 是 | ✅ 是 | `GET /api/users/123` |
| **POST** | 创建资源 | ❌ 否 | ❌ 否 | `POST /api/users` |
| **PUT** | 完整更新资源 | ✅ 是 | ❌ 否 | `PUT /api/users/123` |
| **PATCH** | 部分更新资源 | ❌ 否 | ❌ 否 | `PATCH /api/users/123` |
| **DELETE** | 删除资源 | ✅ 是 | ❌ 否 | `DELETE /api/users/123` |

**什么是幂等性？**

幂等性指**多次执行相同操作，结果与执行一次相同**。

举个例子：
- **GET 是幂等的**：请求 10 次 `/api/users/123`，返回的数据不变
- **POST 不是幂等的**：提交 10 次创建订单请求，会创建 10 个订单
- **PUT 是幂等的**：更新 10 次用户信息，最终结果和更新 1 次一样
- **DELETE 是幂等的**：删除 10 次同一个资源，结果还是删除了

**什么是安全性？**

安全性指**该操作不会修改服务器资源**。

- **GET 是安全的**：只读取数据，不修改
- **POST/PUT/DELETE 都不安全**：都会修改服务器数据

**参考资料：**

- [HTTP 请求方法 -- MDN](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Methods) ⭐值得阅读
- [HTTP 方法的幂等性 -- 知乎](https://zhuanlan.zhihu.com/p/431284613)

### 4.2 GET vs POST 的经典对比 🆚

这是面试和实战中最常被问到的问题：

| 特性 | GET | POST |
|------|-----|------|
| **用途** | 获取数据 | 提交数据/创建资源 |
| **参数位置** | URL 查询参数 | 请求体（Body） |
| **数据长度限制** | 有（URL 长度限制） | 无 |
| **缓存** | 可被缓存 | 不缓存 |
| **书签** | 可收藏为书签 | 不可 |
| **安全性** | 参数暴露在 URL 中 | 参数在 Body 中（相对安全） |
| **幂等性** | ✅ 幂等 | ❌ 不幂等 |

**示例对比**：

```
# GET 请求 - 参数在 URL 中
GET /api/users?name=张三&age=25

# POST 请求 - 参数在 Body 中
POST /api/users
Content-Type: application/json

{
  "name": "张三",
  "age": 25,
  "email": "zhangsan@example.com"
}
```

> 💡 **注意**：POST 比 GET"安全"只是相对的——HTTP 本身是明文传输，真正安全需要 HTTPS！

### 4.3 PUT vs PATCH 的区别 🔄

两者都用于更新，但有微妙差异：

**PUT - 完整替换**

```
PUT /api/users/123
{
  "name": "李四",
  "age": 28,
  "email": "lisi@example.com"
}
```

PUT 要求提供**完整的资源表示**，相当于"替换"整个资源。如果只传 `{"name": "李四"}`，其他字段可能会被清空。

**PATCH - 部分更新**

```
PATCH /api/users/123
{
  "name": "李四"
}
```

PATCH 只更新**提供的字段**，其他字段保持不变。更符合日常使用习惯。

**类比理解**：
- **PUT**：给你一张全新的表，替换旧的
- **PATCH**：在旧表上修改几处内容

**参考资料：**

- [PUT 和 PATCH 的区别 -- Apifox](https://apifox.com/apiskills/difference-between-put-and-patch/)
- [POST、GET、PUT、DELETE 的含义与区别 -- 知乎](https://zhuanlan.zhihu.com/p/431284613)

---

## 5. 网络请求 API 技术对比 🛠️

> 本章对比前端常用的网络请求技术

### 5.1 技术演进历史 📈

```
1999  XMLHttpRequest（XHR）
   ↓
2005  AJAX（基于 XHR）
   ↓
2015  Fetch API（原生 Promise）
   ↓
2016  Axios（第三方库）
```

### 5.2 XMLHttpRequest（XHR）📜

**最传统的网络请求方式**，诞生于 1999 年，是 AJAX 技术的基石。

```javascript
// 创建 XHR 对象
const xhr = new XMLHttpRequest();

// 配置请求
xhr.open('GET', '/api/users/123', true);
xhr.setRequestHeader('Content-Type', 'application/json');

// 监听响应
xhr.onload = function() {
  if (xhr.status === 200) {
    const data = JSON.parse(xhr.responseText);
    console.log('成功:', data);
  } else {
    console.error('错误:', xhr.status);
  }
};

// 发送请求
xhr.send();
```

**特点**：
- ✅ 兼容性好（支持 IE6+）
- ❌ API 设计复杂，回调地狱
- ❌ 不支持 Promise
- ❌ 不符合关注点分离原则

**参考资料：**

- [XMLHttpRequest -- MDN](https://developer.mozilla.org/zh-CN/docs/Web/API/XMLHttpRequest)

### 5.3 Fetch API 🚀

**现代浏览器原生 API**，2015 年随 ES6 推出，基于 Promise 设计。

```javascript
fetch('/api/users/123', {
  method: 'GET',
  headers: {
    'Content-Type': 'application/json',
    'Authorization': 'Bearer token123'
  }
})
  .then(response => {
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    return response.json();
  })
  .then(data => console.log('成功:', data))
  .catch(error => console.error('错误:', error));
```

**Async/Await 写法（推荐）**：

```javascript
async function getUser() {
  try {
    const response = await fetch('/api/users/123');
    
    if (!response.ok) {
      throw new Error(`HTTP error! status: ${response.status}`);
    }
    
    const data = await response.json();
    console.log('成功:', data);
  } catch (error) {
    console.error('错误:', error);
  }
}

getUser();
```

**特点**：
- ✅ 原生支持 Promise，链式调用优雅
- ✅ API 设计简洁，符合现代 JavaScript 风格
- ✅ 支持 Stream API，可处理大文件
- ❌ 不自动转换 JSON（需要手动 `.json()`）
- ❌ 默认不携带 Cookie（需要 `credentials: 'include'`）
- ❌ 只有网络错误才 reject，HTTP 错误（404/500）不 reject

**参考资料：**

- [Fetch API -- MDN](https://developer.mozilla.org/zh-CN/docs/Web/API/Fetch_API) ⭐值得阅读
- [使用 Fetch -- MDN](https://developer.mozilla.org/zh-CN/docs/Web/API/Fetch_API/Using_Fetch)

### 5.4 Axios 📦

**最流行的第三方 HTTP 客户端库**，基于 XHR 实现，但 API 更友好。

```javascript
import axios from 'axios';

// GET 请求
axios.get('/api/users/123')
  .then(response => console.log('成功:', response.data))
  .catch(error => console.error('错误:', error));

// POST 请求
axios.post('/api/users', {
  name: '张三',
  age: 25
})
  .then(response => console.log('创建成功:', response.data));

// Async/Await 写法
async function createUser() {
  try {
    const response = await axios.post('/api/users', {
      name: '张三',
      age: 25
    });
    console.log('创建成功:', response.data);
  } catch (error) {
    console.error('错误:', error);
  }
}
```

**特点**：
- ✅ 自动转换 JSON（无需手动 `.json()`）
- ✅ 自动拦截 HTTP 错误（4xx/5xx 进入 catch）
- ✅ 支持请求/响应拦截器
- ✅ 支持请求取消、超时设置
- ✅ 浏览器和 Node.js 通用
- ❌ 需要额外安装依赖（`npm install axios`）
- ❌ 体积较大（~13KB gzipped）

### 5.5 三种技术对比总览 📊

| 特性 | XMLHttpRequest | Fetch API | Axios |
|------|----------------|-----------|-------|
| **推出时间** | 1999 | 2015 | 2016 |
| **API 设计** | 回调函数 | Promise | Promise |
| **JSON 处理** | 手动 `JSON.parse()` | 手动 `.json()` | 自动转换 |
| **错误处理** | 检查 `status` | 检查 `response.ok` | 自动 reject |
| **拦截器** | ❌ 不支持 | ❌ 不支持 | ✅ 支持 |
| **进度监控** | ✅ 支持 | ✅ 支持（Stream） | ✅ 支持 |
| **浏览器兼容** | IE6+ | 现代浏览器 | 现代浏览器 + IE |
| **依赖** | 原生 | 原生 | 需安装 |
| **体积** | 0 | 0 | ~13KB |

> 💡 **建议**：
> - 学习阶段：先学 **Fetch**（原生、现代标准）
> - 企业项目：用 **Axios**（功能强大、生态成熟）
> - 老旧项目维护：可能会遇到 **XHR**

**参考资料：**

- [Ajax、Fetch、Axios、XMLHttpRequest 的关系与区别 -- CSDN](https://blog.csdn.net/weixin_45274678/article/details/144079224)
- [一文分清 axios、XHR、XML、AJAX 和 Fetch -- 知乎](https://zhuanlan.zhihu.com/p/601204002) ⭐值得阅读
- [深入理解 XHR 和 Fetch 在 Web 开发中 -- 稀土掘金](https://juejin.cn/post/7342400998856228879)

---

## 6. 完整可运行示例 🎯

> 本章提供前端调用 RESTful API 的完整代码

### 6.1 使用 Fetch 调用 API

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>Fetch API 示例</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
    .result { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
    .error { background: #ffebee; color: #c62828; }
    button { padding: 10px 20px; margin: 5px; cursor: pointer; }
  </style>
</head>
<body>
  <h1>🌐 Fetch API 完整示例</h1>
  
  <button onclick="getUsers()">获取用户列表</button>
  <button onclick="getUser(1)">获取单个用户</button>
  <button onclick="createUser()">创建用户</button>
  <button onclick="updateUser(1)">更新用户</button>
  <button onclick="deleteUser(1)">删除用户</button>
  
  <div id="result" class="result">点击按钮查看结果...</div>

  <script>
    // 使用 JSONPlaceholder 免费测试 API
    const BASE_URL = 'https://jsonplaceholder.typicode.com';

    // GET - 获取用户列表
    async function getUsers() {
      try {
        const response = await fetch(`${BASE_URL}/users`);
        
        if (!response.ok) {
          throw new Error(`HTTP 错误: ${response.status}`);
        }
        
        const users = await response.json();
        displayResult(`✅ 获取成功！共 ${users.length} 个用户`, users.slice(0, 3));
      } catch (error) {
        displayError(error.message);
      }
    }

    // GET - 获取单个用户
    async function getUser(id) {
      try {
        const response = await fetch(`${BASE_URL}/users/${id}`);
        const user = await response.json();
        displayResult(`✅ 获取用户 ${id} 成功`, user);
      } catch (error) {
        displayError(error.message);
      }
    }

    // POST - 创建用户
    async function createUser() {
      try {
        const response = await fetch(`${BASE_URL}/users`, {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            name: '张三',
            username: 'zhangsan',
            email: 'zhangsan@example.com'
          })
        });
        
        const newUser = await response.json();
        displayResult('✅ 创建用户成功', newUser);
      } catch (error) {
        displayError(error.message);
      }
    }

    // PUT - 更新用户
    async function updateUser(id) {
      try {
        const response = await fetch(`${BASE_URL}/users/${id}`, {
          method: 'PUT',
          headers: {
            'Content-Type': 'application/json',
          },
          body: JSON.stringify({
            id: id,
            name: '李四',
            username: 'lisi',
            email: 'lisi@example.com'
          })
        });
        
        const updatedUser = await response.json();
        displayResult(`✅ 更新用户 ${id} 成功`, updatedUser);
      } catch (error) {
        displayError(error.message);
      }
    }

    // DELETE - 删除用户
    async function deleteUser(id) {
      try {
        const response = await fetch(`${BASE_URL}/users/${id}`, {
          method: 'DELETE'
        });
        
        displayResult(`✅ 删除用户 ${id} 成功`, { id: id, deleted: true });
      } catch (error) {
        displayError(error.message);
      }
    }

    // 显示结果
    function displayResult(message, data) {
      const resultDiv = document.getElementById('result');
      resultDiv.className = 'result';
      resultDiv.innerHTML = `
        <h3>${message}</h3>
        <pre>${JSON.stringify(data, null, 2)}</pre>
      `;
    }

    // 显示错误
    function displayError(message) {
      const resultDiv = document.getElementById('result');
      resultDiv.className = 'result error';
      resultDiv.innerHTML = `<h3>❌ 错误</h3><p>${message}</p>`;
    }
  </script>
</body>
</html>
```

### 6.2 使用 Axios 调用 API

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>Axios API 示例</title>
  <script src="https://cdn.jsdelivr.net/npm/axios/dist/axios.min.js"></script>
  <style>
    body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
    .result { background: #f5f5f5; padding: 15px; margin: 10px 0; border-radius: 5px; }
    .error { background: #ffebee; color: #c62828; }
    button { padding: 10px 20px; margin: 5px; cursor: pointer; }
  </style>
</head>
<body>
  <h1>📦 Axios 完整示例</h1>
  
  <button onclick="getUsers()">获取用户列表</button>
  <button onclick="createUser()">创建用户</button>
  
  <div id="result" class="result">点击按钮查看结果...</div>

  <script>
    const BASE_URL = 'https://jsonplaceholder.typicode.com';

    // 创建 axios 实例（配置通用设置）
    const api = axios.create({
      baseURL: BASE_URL,
      timeout: 5000,
      headers: {
        'Content-Type': 'application/json'
      }
    });

    // 请求拦截器
    api.interceptors.request.use(
      config => {
        console.log('🚀 发起请求:', config.method.toUpperCase(), config.url);
        return config;
      },
      error => Promise.reject(error)
    );

    // 响应拦截器
    api.interceptors.response.use(
      response => {
        console.log('✅ 请求成功:', response.status);
        return response;
      },
      error => {
        console.error('❌ 请求失败:', error.response?.status || error.message);
        return Promise.reject(error);
      }
    );

    // GET 请求
    async function getUsers() {
      try {
        const response = await api.get('/users');
        displayResult(`✅ 获取成功！共 ${response.data.length} 个用户`, response.data.slice(0, 3));
      } catch (error) {
        displayError(error.message);
      }
    }

    // POST 请求
    async function createUser() {
      try {
        const response = await api.post('/users', {
          name: '张三',
          username: 'zhangsan',
          email: 'zhangsan@example.com'
        });
        displayResult('✅ 创建用户成功', response.data);
      } catch (error) {
        displayError(error.message);
      }
    }

    function displayResult(message, data) {
      const resultDiv = document.getElementById('result');
      resultDiv.className = 'result';
      resultDiv.innerHTML = `
        <h3>${message}</h3>
        <pre>${JSON.stringify(data, null, 2)}</pre>
      `;
    }

    function displayError(message) {
      const resultDiv = document.getElementById('result');
      resultDiv.className = 'result error';
      resultDiv.innerHTML = `<h3>❌ 错误</h3><p>${message}</p>`;
    }
  </script>
</body>
</html>
```

### 6.3 运行结果示例

将上述 HTML 文件保存后在浏览器中打开，点击按钮会看到类似输出：

```
✅ 获取成功！共 10 个用户
[
  {
    "id": 1,
    "name": "Leanne Graham",
    "username": "Bret",
    "email": "Sincere@april.biz"
  },
  ...
]

✅ 创建用户成功
{
  "name": "张三",
  "username": "zhangsan",
  "email": "zhangsan@example.com",
  "id": 11
}
```

---

## 7. 大模型 API 接口 🤖

> 本章介绍当前最火爆的大语言模型 API 接口

### 7.1 什么是大模型 API 🌟

**大模型 API（Large Language Model API）** 是当前人工智能领域最热门的技术之一。它允许开发者通过网络请求调用云端部署的超大规模 AI 模型，而无需自己训练模型或购买昂贵的 GPU 硬件。

**通俗理解**：就像你不需要自己发电就能使用电器一样，你不需要自己训练 AI 模型，只需通过 API 发送请求，就能获得强大的 AI 能力——对话、写作、编程、翻译等。

### 7.2 主流大模型 API 一览 📊

**国外主流大模型**：

| 模型 | 公司 | API 接口 | 特点 |
|------|------|---------|------|
| **GPT-4/GPT-4o** | OpenAI | `api.openai.com` | 最强通用能力，生态最完善 |
| **Claude 3.5/4** | Anthropic | `api.anthropic.com` | 长上下文、安全性强 |
| **Gemini 2.0** | Google | `generativelanguage.googleapis.com` | 多模态能力强 |
| **Llama 3** | Meta | 开源可自部署 | 开源免费 |

**国内主流大模型**：

| 模型 | 公司 | API 接口 | 特点 |
|------|------|---------|------|
| **通义千问 (Qwen)** | 阿里巴巴 | `dashscope.aliyuncs.com` | 中文能力强，性价比高 |
| **文心一言 (ERNIE)** | 百度 | `aip.baidubce.com` | 国内最早开放 API |
| **DeepSeek** | 深度求索 | `api.deepseek.com` | 编程能力强，价格低 |
| **Kimi** | 月之暗面 | `api.moonshot.cn` | 超长上下文（200K） |
| **豆包** | 字节跳动 | `api.deepseek.com` | 多模态支持 |

**参考资料：**

- [2025版国内外主流大模型API接口调用完整指南 -- 知乎](https://zhuanlan.zhihu.com/p/1983367855245375096) ⭐值得阅读
- [三大同步大模型厂商API深度对比 -- 腾讯云](https://cloud.tencent.com/developer/article/2560292)

### 7.3 大模型 API 也是 RESTful 接口 🎯

**关键认知**：现在所有主流大模型的 API 接口，本质上都是 **基于 HTTP 协议的 RESTful API**！

这意味着：
- ✅ 你前面学的 HTTP 请求方法（POST）、请求头、请求体等知识，完全可以用于调用大模型 API
- ✅ 大模型 API 遵循 RESTful 设计规范：资源导向、统一接口、无状态
- ✅ 使用前面学到的 Fetch、Axios 等技术，同样可以调用大模型 API

**OpenAI API 调用示例（标准 RESTful 格式）**：

```javascript
// 使用 Fetch 调用 OpenAI GPT-4 API
async function chatWithGPT4(prompt) {
  const response = await fetch('https://api.openai.com/v1/chat/completions', {
    method: 'POST',  // ← 使用 POST 方法创建对话
    headers: {
      'Content-Type': 'application/json',
      'Authorization': 'Bearer sk-your-api-key-here'
    },
    body: JSON.stringify({
      model: 'gpt-4',
      messages: [
        { role: 'system', content: '你是一个有用的助手' },
        { role: 'user', content: prompt }
      ],
      temperature: 0.7
    })
  });
  
  const data = await response.json();
  return data.choices[0].message.content;
}

// 使用示例
chatWithGPT4('请解释什么是 API')
  .then(response => console.log(response));
```

**通义千问 API 调用示例**：

```javascript
// 使用 Axios 调用阿里通义千问 API
async function chatWithQwen(prompt) {
  const response = await axios.post(
    'https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions',
    {
      model: 'qwen-plus',
      messages: [
        { role: 'user', content: prompt }
      ]
    },
    {
      headers: {
        'Authorization': 'Bearer your-dashscope-api-key',
        'Content-Type': 'application/json'
      }
    }
  );
  
  return response.data.choices[0].message.content;
}
```

**看到了吗？** 大模型 API 的调用方式和你前面学的普通 Web API **完全一样**——
- 都是 `POST` 请求
- 都需要设置请求头（认证、内容类型）
- 都在请求体中传递 JSON 数据
- 都返回 JSON 格式的响应

### 7.4 OpenAI 兼容格式：事实上的行业标准 🏆

**重要趋势**：现在几乎所有大模型都提供 **OpenAI 兼容格式**的 API 接口！

这意味着什么？
- OpenAI 定义了大模型 API 的标准格式（RESTful + JSON）
- 其他厂商（阿里、百度、DeepSeek 等）都模仿这个格式
- 开发者只需学习一次，就能调用所有大模型

**OpenAI 兼容格式的核心结构**：

```json
// 请求格式（所有大模型都类似）
{
  "model": "模型名称",
  "messages": [
    { "role": "system", "content": "系统提示词" },
    { "role": "user", "content": "用户问题" }
  ],
  "temperature": 0.7,
  "max_tokens": 1000
}

// 响应格式
{
  "choices": [
    {
      "message": {
        "role": "assistant",
        "content": "AI 的回答内容"
      },
      "finish_reason": "stop"
    }
  ],
  "usage": {
    "prompt_tokens": 10,
    "completion_tokens": 50,
    "total_tokens": 60
  }
}
```

**支持 OpenAI 兼容格式的主流大模型**：

| 大模型 | 兼容接口地址 | 说明 |
|--------|-------------|------|
| OpenAI GPT-4 | `api.openai.com` | 原始标准 |
| 通义千问 | `dashscope.aliyuncs.com/compatible-mode/v1` | 阿里提供兼容接口 |
| DeepSeek | `api.deepseek.com` | 完全兼容 |
| Claude | 通过第三方代理 | Anthropic 官方 API 不同 |
| 文心一言 | 通过第三方代理 | 百度官方 API 不同 |
| Kimi | `api.moonshot.cn/v1` | 兼容 OpenAI 格式 |

**参考资料：**

- [OpenAI API 协议完全指南 -- 墨滴](https://mdnice.com/writing/7f7dbe9fc98a4fca8f9a34f81b9e1789) ⭐值得阅读
- [通过标准的OpenAI API 格式访问所有的大模型 -- CSDN](https://deepseek.csdn.net/67bda6df3b685529b70019e4.html)
- [大模型（LLM）的若干科普之问：OpenAI 的API 接口规范 -- CSDN](https://blog.csdn.net/qiy_icbc/article/details/145208903)

### 7.5 大模型 API 与普通 Web API 的对比 🔄

| 特性 | 普通 Web API | 大模型 API |
|------|-------------|-----------|
| **协议** | HTTP/HTTPS | HTTP/HTTPS（相同） |
| **设计风格** | RESTful | RESTful（相同） |
| **请求方法** | GET/POST/PUT/DELETE | 几乎全是 POST |
| **数据格式** | JSON | JSON（相同） |
| **认证方式** | Token/API Key | API Key（Bearer Token） |
| **响应时间** | 毫秒级 | 秒级（需要推理计算） |
| **返回内容** | 结构化数据 | 自然语言文本 |
| **计费方式** | 通常免费 | 按 Token 数量收费 |

**核心差异**：
- 普通 API：返回确定的数据（如用户信息、商品列表）
- 大模型 API：返回**生成的文本**（具有创造性、不确定性）

### 7.6 实战：用前端代码调用大模型 💻

```html
<!DOCTYPE html>
<html lang="zh-CN">
<head>
  <meta charset="UTF-8">
  <title>大模型 API 调用示例</title>
  <style>
    body { font-family: Arial, sans-serif; max-width: 800px; margin: 50px auto; padding: 20px; }
    .chat-box { border: 1px solid #ddd; padding: 20px; border-radius: 10px; margin: 20px 0; }
    .input-area { display: flex; gap: 10px; margin: 20px 0; }
    input { flex: 1; padding: 10px; border: 1px solid #ddd; border-radius: 5px; }
    button { padding: 10px 20px; background: #4CAF50; color: white; border: none; border-radius: 5px; cursor: pointer; }
    button:hover { background: #45a049; }
    .response { background: #f5f5f5; padding: 15px; border-radius: 5px; margin-top: 10px; white-space: pre-wrap; }
  </style>
</head>
<body>
  <h1>🤖 大模型 API 调用示例</h1>
  
  <div class="chat-box">
    <div class="input-area">
      <input type="text" id="prompt" placeholder="输入你的问题..." value="请解释什么是 API">
      <button onclick="callAI()">发送</button>
    </div>
    <div id="response" class="response">AI 的回答将显示在这里...</div>
  </div>

  <script>
    async function callAI() {
      const prompt = document.getElementById('prompt').value;
      const responseDiv = document.getElementById('response');
      
      responseDiv.textContent = '正在思考中...';
      
      try {
        // 这里以通义千问为例（你有哪个 API Key 就替换成对应的）
        const response = await fetch('https://dashscope.aliyuncs.com/compatible-mode/v1/chat/completions', {
          method: 'POST',
          headers: {
            'Content-Type': 'application/json',
            'Authorization': 'Bearer your-api-key-here'  // ← 替换为你的 API Key
          },
          body: JSON.stringify({
            model: 'qwen-plus',
            messages: [
              { role: 'user', content: prompt }
            ],
            temperature: 0.7
          })
        });
        
        const data = await response.json();
        const aiResponse = data.choices[0].message.content;
        
        responseDiv.textContent = aiResponse;
      } catch (error) {
        responseDiv.textContent = '错误：' + error.message;
      }
    }
  </script>
</body>
</html>
```

> 💡 **提示**：要运行此示例，你需要先申请一个大模型的 API Key（大多数都提供免费额度）。推荐使用通义千问或 DeepSeek，国内访问速度快，免费额度充足。

**参考资料：**

- [2025最新免费的大模型和免费的大模型API -- 火山引擎](https://developer.volcengine.com/articles/7537037650508087305)
- [【玩转大模型的API】2025年最全大模型API申请与调用实战指南 -- CSDN](https://deepseek.csdn.net/681ca35fe9858151797f8d5b.html)

---

## 8. 总结 📝

本节我们完成了网络请求和 API 的系统学习，核心要点回顾：

| 要点 | 说明 |
|------|------|
| **API 本质** | 系统间通信的接口，封装复杂性 |
| **HTTP 协议** | Web API 的底层协议，请求-响应模型 |
| **RESTful 设计** | 资源导向、统一接口、无状态 |
| **HTTP 方法** | GET（获取）、POST（创建）、PUT（更新）、DELETE（删除） |
| **Fetch API** | 现代浏览器原生 API，基于 Promise |
| **Axios** | 第三方库，功能强大，企业项目首选 |
| **大模型 API** | 本质上也是 RESTful API，遵循 OpenAI 兼容格式 |

🔴 **关键理解**：

- API 是前后端分离架构的核心桥梁，理解 API 才能理解现代 Web 开发
- RESTful 不是技术，而是一种**设计风格**，遵循 HTTP 协议的语义
- HTTP 方法的幂等性和安全性是面试高频考点
- Fetch 是现代标准，但 Axios 在实际项目中更受欢迎（功能更全、API 更友好）
- 学习网络请求的最佳方式是**动手调用真实的 API**（如 JSONPlaceholder）
- 🤖 **大模型 API 本质上也是 RESTful API**，使用 POST 方法 + JSON 格式，与普通 Web API 调用方式完全相同
- 现在几乎所有大模型都提供 **OpenAI 兼容格式**，学习一次即可调用所有大模型
- 掌握网络请求基础后，你就可以轻松接入 ChatGPT、Claude、通义千问等所有大模型

---

**参考资料：**

- [什么是 REST API？ -- IBM](https://www.ibm.com/cn-zh/think/topics/rest-apis) ⭐值得阅读
- [RESTful API 教程 -- 菜鸟教程](https://www.runoob.com/restfulapi/restful-api-intro.html)
- [HTTP 请求方法 -- MDN](https://developer.mozilla.org/zh-CN/docs/Web/HTTP/Methods) ⭐值得阅读
- [Fetch API -- MDN](https://developer.mozilla.org/zh-CN/docs/Web/API/Fetch_API) ⭐值得阅读
- [Axios 官方文档](https://axios-http.com/zh/)
- [RESTful API 系列之 HTTP 基础 -- 知乎](https://zhuanlan.zhihu.com/p/187541438)
