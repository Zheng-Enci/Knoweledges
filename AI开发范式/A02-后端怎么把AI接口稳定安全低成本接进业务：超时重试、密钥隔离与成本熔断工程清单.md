# 后端怎么把 AI 接口稳定、安全、低成本地接进业务：超时重试、密钥隔离与成本熔断工程清单

AI 接口接进业务，难点从来不是「调通」，而是「调崩之后谁来兜」。真正要解决的只有三件事：超时与限流不把业务拖死、密钥和用户数据不出自己的边界、token 花出去的每一分钱都能对上账。这三件事都不该散落在业务代码里，而应集中在一层薄薄的网关上——本篇给出可运行的那一层。

## 目录

1. 先划边界：这篇只管接口层
2. 上线后一定会遇到的现象对照表
3. 网关要收走的五件事
4. 完整实现：一个能直接跑的 AI 网关
5. 安全不是加个鉴权就完事
6. 成本不是一个单价，是四个维度
7. 看不见的故障最贵
8. 这层网关拦不住什么
9. 上线前自检清单

## 1. 先划边界：这篇只管接口层（Scope）

先把「接口层」这个词说死。它指业务代码和模型厂商之间的那一段：从一个 HTTP request（HTTP 请求）发出，到一段文本或一个 token 流回到业务手里。这一段里全是工程问题——超时、重试、限流、密钥、计费、日志。而模型选得对不对、prompt（提示词）写得好不好、RAG（Retrieval-Augmented Generation，检索增强生成）召回准不准，都不在这一段里。

打个比方：接口层就是公司的前台和总机。它负责把来访电话转对分机、占线时让你稍等、下班后告诉你明天再打；它不负责接线员聊得投不投机。前台可以换人、可以加人，业务部门不用知道今天是谁值班。

这层代码有三个贯穿全文的约束：

1. **业务代码不持有厂商密钥**，只拿内部签发的调用凭证，换 key（密钥）时不改业务代码；
2. **所有失败都有明确归类**，可重试的、不可重试的、该熔断的，分三条路走，绝不混成一个 `except Exception`；
3. **每次调用都留下可对账的账本**，租户、模型、输入输出 token 数、耗时、是否命中缓存，一个字段都不能少。

这三条对应三个老问题：安全、稳定、成本。它们不是三套系统，而是同一层网关的三个切面——这也是为什么分散在业务代码里做会越做越乱。

## 2. 上线后一定会遇到的现象对照表（Symptom, Cause, Fix）

下面六种现象，只要 AI 功能上过生产，至少会撞上三种。表里的原因不是推测，是这类系统的通病。

| 症状 | 原因 | 解法 |
|---|---|---|
| 换个模型供应商，八个服务一起改代码 | 每个服务各自读厂商 key、各自拼 request body（请求体） | 网关统一成 OpenAI 兼容协议，业务只认内部 endpoint |
| 高峰期 429 一片，重试之后更慢 | 无差别重试，且没有抖动，所有客户端同一时刻再打一次 | 只重试可恢复异常，指数退避叠加随机抖动，同时按 provider 分桶限流 |
| 长文档总结总是 15 秒准时失败 | read timeout 按短对话设的，没考虑推理耗时随输出长度线性增长 | 按场景分级超时：短对话 5 秒、长文 15–30 秒、embedding 3 秒，并改用流式 |
| 月底账单比预算高三倍，没人说得清花在哪 | 没有按租户、按功能的 token 计量，只有厂商总账单 | 每次调用写账本，按租户设预算闸门，超额直接拒绝而不是事后告警 |
| 出了故障只能看「接口 500」四个字 | 日志里没有 trace id，也没有记录模型名与 token 用量 | 按 OpenTelemetry GenAI 语义约定打点，一条 trace 串起重试全过程 |
| 用户手机号、身份证号原样进了厂商 | 只做了入口鉴权，没做出口脱敏 | 请求前做 PII（Personally Identifiable Information，个人可识别信息）替换，返回后按映射表还原 |

最后一行最容易被忽略：它不报错，只是悄悄把数据送了出去。安全章节会单独展开。

上述现象与治理手段的对应关系，在阿里云开发者社区那篇《大模型高可用适配架构》里有更完整的分层描述，SegmentFault 上那篇超时故障复盘则给出了根因分类决策树，两篇可以对照着看。

参考资料：
- [大模型高可用适配架构：构建统一API网关，实现多模型兼容、重试、降级、限流机制 -- 阿里云开发者社区](https://developer.aliyun.com/article/1772129) ⭐值得阅读
- [从一次超时故障看大模型 API 的稳定性治理思路 -- SegmentFault 思否](https://segmentfault.com/a/1190000047981447) ⭐值得阅读
- [如何设计一个生产级 LLM Gateway -- CSDN](https://blog.csdn.net/u013970991/article/details/160795654)

## 3. 网关要收走的五件事（Responsibilities）

先说结论：网关只该做五件事，多一件都是在给自己挖坑。厂商能力在变、模型在换，唯独这五件事的逻辑十年不变。

**第一件，统一协议。** 业务侧只认一个 OpenAI 兼容的 `/v1/chat/completions`，请求头、参数结构、返回字段全部对齐。换供应商时改的是网关里的路由配置，不是八个服务的代码。腾讯云 AI 网关和 Azure API Management 的 genai gateway 能力都把这步叫「协议转换」，本质相同——真正的价值不是兼容，而是把「换厂商」从一次发版降级成一次配置变更。

**第二件，虚拟密钥。** 真实厂商 key 只存在网关进程或密钥管理服务里，业务拿到的是 `vk-` 开头的虚拟凭证。虚拟凭证能吊销、能限速、能挂预算，泄露了也不心疼。LiteLLM 的做法很典型：为每个团队发一把 virtual key 并绑定硬预算，key 触顶即拒绝，跑飞的批处理任务或泄露的 key 都不会悄悄把账单刷上去。

**第三件，超时、重试、熔断三件套。** 它们必须一起设计，缺一个都会出事。超时按场景分级（短对话 5 秒、长文 15–30 秒、embedding 3 秒）；重试只对可恢复异常（连接失败、5xx、429）开放，且必须带抖动；熔断则在连续失败后直接掐断上游，让请求快速失败而不是排队等死。阿里云那篇给出的分级降级（屏蔽单模型 → 关停非核心 → 返回兜底）也是同一套思路的延伸。

**第四件，限流分桶。** 至少三层：全局限并发、按模型限 QPS、按租户限配额。少一层就会出现「一个租户把整个模型的 TPM 吃干净」的事故。腾讯云把这块做得更细，QPM 之外还分 TPM / TPH / TPD（每分钟、每小时、每天 token 数）三档窗口。

**第五件，账本。** 每次调用写一行：租户、模型、输入 token、输出 token、耗时、是否命中缓存、是否重试。这行记录同时喂给三个下游——对账、告警、容量规划。没有它，成本控制就只能等月底看账单，那时候已经晚了。

五件事的边界也很清楚：网关不做 prompt 优化、不做模型效果评测、不做业务语义校验。它像小区门禁——刷卡、登记、限流、拦陌生人，至于你进楼找谁谈什么事，它不管。

参考资料：
- [LiteLLM — Open-Source AI Gateway & LLM Proxy -- LiteLLM](https://www.litellm.ai/) ⭐值得阅读
- [Budget Fallbacks -- LiteLLM Docs](https://docs.litellm.ai/docs/proxy/budget_fallbacks)
- [注册配置治理 AI 网关概述 -- 腾讯云](https://cloud.tencent.com/document/product/1364/127525)

## 4. 完整实现：一个能直接跑的 AI 网关（Full Implementation）

前面三章都在讲该做什么，这章直接给代码。下面这段只用 Python 标准库，自带一个假上游——它前两次请求返回 429，之后正常回话。整份文件保存为 `ai_gateway.py`，`python ai_gateway.py` 就能跑，不需要装任何依赖，也不需要真实 API key（密钥架在网关里，业务只拿 `vk-` 凭证，这一点在代码里是能看出来的）。

```python
"""能直接跑的 AI 网关：虚拟密钥 + 分级超时 + 分类重试 + 熔断 + 限流 + 预算闸门（仅标准库）。"""

import json                                                        # 组装请求体、解析响应体
import random                                                      # 生成抖动，避免重试风暴
import socket                                                      # 捕获连接级超时
import threading                                                   # 把假上游跑在后台线程
import time                                                        # 计时与指数退避
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer  # demo 用的假上游
from urllib import error, request                                   # 标准库 HTTP 客户端

UPSTREAM = "http://127.0.0.1:8801/v1/chat/completions"             # 上游地址，生产换成厂商 endpoint
UPSTREAM_KEY = "sk-real-7f3a"                                      # 真实密钥只活在网关进程里
VIRTUAL_KEYS = {"vk-web": "web", "vk-batch": "batch", "vk-agent": "agent"}  # 虚拟凭证 -> 租户
TIMEOUTS = {"short": 5.0, "long": 30.0}                            # 分级超时（秒）
MAX_RETRIES, FAIL_THRESHOLD, OPEN_SECONDS = 2, 3, 10.0             # 重试上限 / 熔断阈值 / 冷却秒数
QPS = {"web": 5, "batch": 1, "agent": 5}                           # 每租户每秒请求上限
BUDGETS = {"web": 0.01, "batch": 0.05, "agent": 0.05}              # 每租户预算（美元）
PRICE_IN, PRICE_OUT = 0.15 / 1000, 0.60 / 1000                     # 单价：美元 / token
RETRYABLE = {429, 500, 502, 503, 504}                              # 只有这些状态码值得重试


class GatewayError(Exception):
    """对外统一异常，code 直接映射成 HTTP 状态码。"""

    def __init__(self, code, detail=""):
        self.code, self.detail = code, detail                      # unauthorized / budget_exceeded ...
        super().__init__(f"{code}: {detail}")


class UpstreamError(Exception):
    """上游失败，retryable 决定是否进入下一轮重试。"""

    def __init__(self, kind, retryable):
        self.kind, self.retryable = kind, retryable                # timeout / http_429 / network
        super().__init__(kind)


class CircuitBreaker:
    """三态熔断：closed 正常 → open 拒绝 → half_open 放一次试探。"""

    def __init__(self):
        self.failures = 0                                          # 连续失败计数
        self.opened_at = 0.0                                       # 0 表示未打开

    def allow(self):
        if self.opened_at == 0.0:                                  # 正常期
            return True
        if time.monotonic() - self.opened_at < OPEN_SECONDS:        # 仍在冷却
            return False                                           # 快速失败，不打上游
        self.opened_at = 0.0                                       # 冷却结束，转 half_open
        return True                                                # 只放这一下试探

    def success(self):
        self.failures, self.opened_at = 0, 0.0                      # 成功回 closed

    def fail(self):
        self.failures += 1                                         # 失败 +1
        if self.failures >= FAIL_THRESHOLD:                         # 触达阈值
            self.opened_at = time.monotonic()                       # 记录打开时刻


class TokenBucket:
    """令牌桶限流：按租户匀速补令牌，容量取两倍速率以容忍短突发。"""

    def __init__(self, rate):
        self.rate = float(rate)                                    # 每秒补多少令牌
        self.capacity = rate * 2.0                                 # 桶容量
        self.tokens = self.capacity                                # 初始装满
        self.updated = time.monotonic()                            # 上次补充时刻

    def take(self):
        now = time.monotonic()                                     # 当前时刻
        self.tokens = min(self.capacity,                          # 不超过容量
                          self.tokens + (now - self.updated) * self.rate)  # 按流逝时间补水
        self.updated = now                                         # 刷新补充时刻
        if self.tokens < 1:                                        # 不足一个令牌
            return False                                           # 拒绝本次
        self.tokens -= 1                                           # 扣掉一个
        return True                                                # 放行


class Ledger:
    """按租户记账：每次调用一行，既能对账也能直接喂监控。"""

    def __init__(self):
        self.rows, self.spent = [], {}                             # 明细行 / 租户累计花费

    def charge(self, tenant, model, tokens_in, tokens_out, latency, retries):
        cost = tokens_in * PRICE_IN + tokens_out * PRICE_OUT       # 输入输出分开计价
        self.spent[tenant] = self.spent.get(tenant, 0.0) + cost    # 累加到租户总额
        self.rows.append({"tenant": tenant, "model": model,        # 谁、用了哪个模型
                          "in": tokens_in, "out": tokens_out,      # 输入输出 token 数
                          "cost": round(cost, 6),                  # 本次花费
                          "latency_ms": round(latency * 1000), "retries": retries})  # 耗时与重试
        return cost                                                # 返回本次花费


class Gateway:
    """业务唯一入口：鉴权 → 查预算 → 查熔断 → 限流 → 调上游 → 记账。"""

    def __init__(self):
        self.breaker = CircuitBreaker()                             # 每个上游一个
        self.buckets = {t: TokenBucket(r) for t, r in QPS.items()}   # 每租户一个令牌桶
        self.ledger = Ledger()                                      # 进程内账本
        self.budgets = dict(BUDGETS)                                # 可运行时调整

    def chat(self, virtual_key, messages, timeout_class="short"):
        tenant = VIRTUAL_KEYS.get(virtual_key)                      # 虚拟凭证换租户
        if tenant is None:                                          # 未知凭证
            raise GatewayError("unauthorized", "unknown virtual key")
        est_in = sum(len(m["content"]) for m in messages) // 4       # 粗估输入 token
        if self.ledger.spent.get(tenant, 0.0) + est_in * PRICE_IN > self.budgets[tenant]:
            raise GatewayError("budget_exceeded", tenant)           # 超额直接拒，不告警后放行
        if not self.breaker.allow():                                # 熔断期
            raise GatewayError("circuit_open", "upstream cooling down")
        if not self.buckets[tenant].take():                         # 令牌不足
            raise GatewayError("rate_limited", tenant)
        payload = {"model": "demo-model", "messages": messages}     # 上游协议固定
        for attempt in range(MAX_RETRIES + 1):                      # 首次 + 最多 2 次重试
            started = time.monotonic()                              # 本次尝试起点
            try:
                data = self._post(payload, TIMEOUTS[timeout_class])   # 带分级超时发起
                self.breaker.success()                              # 成功即恢复熔断器
                usage = data.get("usage", {})                        # 厂商返回的用量
                tokens_in = usage.get("prompt_tokens", est_in)      # 缺省用估算值兜底
                tokens_out = usage.get("completion_tokens", 0)      # 输出 token 数
                self.ledger.charge(tenant, payload["model"], tokens_in, tokens_out,
                                   time.monotonic() - started, attempt)  # 记账
                return data["choices"][0]["message"]["content"]      # 只把文本交回业务
            except UpstreamError as exc:
                self.breaker.fail()                                 # 每次失败都计入熔断
                if not exc.retryable or attempt == MAX_RETRIES:      # 不可重试或已用尽
                    raise GatewayError("upstream_failed",
                                       f"{exc.kind} after {attempt + 1} tries")
                time.sleep(min(2 ** attempt * 0.2, 2.0) * (0.5 + random.random()))  # 退避+抖动

    @staticmethod
    def _post(payload, timeout):
        """发一次上游请求，把各类底层异常翻译成 UpstreamError。"""
        req = request.Request(
            UPSTREAM,                                               # 上游 endpoint
            data=json.dumps(payload).encode("utf-8"),               # 序列化请求体
            headers={"Content-Type": "application/json",            # 固定 JSON
                     "Authorization": f"Bearer {UPSTREAM_KEY}"},     # 真 key 只在此出现
        )
        try:
            with request.urlopen(req, timeout=timeout) as resp:      # 超时由 urllib 兜底
                return json.loads(resp.read())                       # 解析并返回 JSON
        except error.HTTPError as exc:                               # 4xx / 5xx
            raise UpstreamError(f"http_{exc.code}", exc.code in RETRYABLE)  # 分类
        except (socket.timeout, TimeoutError):                       # 连接或读取超时
            raise UpstreamError("timeout", True)                     # 超时可重试
        except error.URLError:                                       # DNS、断网、拒连
            raise UpstreamError("network", True)                     # 网络问题可重试


class FakeUpstream(BaseHTTPRequestHandler):
    """本地假上游：前 fails_left 次返回 429，之后回显固定答案。"""

    fails_left = 2                                                 # 先制造两次限流

    def do_POST(self):
        size = int(self.headers.get("Content-Length", 0))           # 请求体长度
        payload = json.loads(self.rfile.read(size) or b"{}")        # 解析请求体
        if FakeUpstream.fails_left > 0:                             # 失败阶段
            FakeUpstream.fails_left -= 1                            # 消耗一次失败额度
            body, status = b'{"error": "rate_limited"}', 429         # 触发客户端重试
        else:                                                       # 成功阶段
            text = "收到：" + payload["messages"][-1]["content"][:8]   # 回显前 8 个字
            body = json.dumps({"choices": [{"message": {"content": text}}],
                               "usage": {"prompt_tokens": 32,
                                         "completion_tokens": 16}}).encode()  # 计费口径
            status = 200                                            # 正常返回
        self.send_response(status)                                  # 写状态行
        self.send_header("Content-Type", "application/json")        # 声明 JSON
        self.send_header("Content-Length", str(len(body)))          # 明确长度
        self.end_headers()                                          # 头结束
        self.wfile.write(body)                                      # 写响应体

    def log_message(self, *args):
        """关掉默认访问日志，让输出干净。"""
        return


if __name__ == "__main__":
    server = ThreadingHTTPServer(("127.0.0.1", 8801), FakeUpstream)  # 假上游
    threading.Thread(target=server.serve_forever, daemon=True).start()  # 后台跑
    time.sleep(0.2)                                                 # 等端口就绪
    gw = Gateway()                                                  # 起一个网关

    print("场景一：限流两次后成功")
    print("  输出:", gw.chat("vk-web", [{"role": "user", "content": "帮我写个摘要"}]))

    print("场景二：预算触顶")
    gw.budgets["web"] = gw.ledger.spent["web"]                       # 预算压到已花金额
    try:
        gw.chat("vk-web", [{"role": "user", "content": "再来一次"}])
    except GatewayError as exc:
        print("  拦下:", exc.code)                                   # budget_exceeded

    print("场景三：租户突发打满 QPS")
    for i in range(4):                                               # batch 桶容量只有 2
        try:
            print(f"  第 {i + 1} 次:", gw.chat("vk-batch", [{"role": "user", "content": "批处理"}]))
        except GatewayError as exc:
            print(f"  第 {i + 1} 次: 拦下", exc.code)                 # 后两次 rate_limited

    print("场景四：上游持续故障")
    FakeUpstream.fails_left = 99                                     # 让上游一直 429
    for i in range(2):
        try:
            gw.chat("vk-agent", [{"role": "user", "content": "问一句"}])
        except GatewayError as exc:
            print(f"  第 {i + 1} 次:", exc.code, "|", exc.detail)     # upstream_failed → circuit_open

    print("账本：")
    for row in gw.ledger.rows:                                       # 逐行打印明细
        print("  ", row)
    print("累计花费：", {k: round(v, 6) for k, v in gw.ledger.spent.items()})
```

### 4.1 运行结果怎么读（How to Read the Output）

输出大致如下（`latency_ms` 与等待时长随机器不同，不必与这里对得上）：

```text
场景一：限流两次后成功
  输出: 收到：帮我写个摘要
场景二：预算触顶
  拦下: budget_exceeded
场景三：租户突发打满 QPS
  第 1 次: 收到：批处理
  第 2 次: 收到：批处理
  第 3 次: 拦下 rate_limited
  第 4 次: 拦下 rate_limited
场景四：上游持续故障
  第 1 次: upstream_failed | http_429 after 3 tries
  第 2 次: circuit_open | upstream cooling down
累计花费： {'web': 0.0144, 'batch': 0.0288}
```

四个场景各自证明一件事，缺一件这段代码就不算完整：

| 场景 | 观察点 | 证明什么 |
|---|---|---|
| ① 两次 429 后成功 | `retries: 2`，输出正常 | 重试只对可恢复异常开放，且退避没有把请求打死 |
| ② 预算压到已花金额 | `budget_exceeded`，请求根本没打上游 | 预算是闸门不是报表，超额当场拒绝 |
| ③ batch 连打四次 | 前两次成功，后两次 `rate_limited` | 令牌桶按租户隔离，一个租户打不满整个模型 |
| ④ 上游持续 429 | 第一次耗尽重试，第二次直接 `circuit_open` | 熔断让第二次请求在毫秒级失败，而不是再等三轮 |

有两个细节值得单独说。第一，场景二里 `web` 的实际累计花费是 0.0144，比预算 0.01 高——因为闸门用的是请求前估算的输入 token，真正的账单以厂商返回的 `usage` 为准，估算只负责「别让明显超额的请求发出去」。第二，场景三的后两次是否被拦，取决于你的机器有多快：如果单次调用慢到超过 1 秒，令牌桶会补回一个令牌，第三次就会放行。这不是 bug，恰是令牌桶与「每分钟固定配额」的区别——它按时间匀速恢复，而不是整点重新发牌。

### 4.2 生产版必须补的三件事（Production Gaps）

这段代码故意留了三个缺口，因为补上它们会让文件长到不适合放在文章里，而它们又必须补。

**第一，超时不是一档，是三档。** 非流式请求一个 read timeout 够用；流式请求至少要三档：首字节 30 秒、token 间隔 15 秒、总时长 180 秒。三者谁先到谁终止上游调用，并向外返回结构化错误。厂商标称的 P99 再漂亮，也架不住某天机房抽风让首字节卡住 90 秒——那时你的 5 秒超时反而是优点。

**第二，取消必须传到上游。** 用户关掉页签后，服务端到厂商的 HTTP 连接如果不主动断，token 还会继续生成、继续计费。有团队实测过约 12% 的对话请求在完成前被取消，不做取消传播就等于给这 12% 全额买单。Python 里靠 `request.is_disconnected()` 或 task 取消，Node 里靠 `AbortController`，关键是这条信号要一路传到厂商 SDK。

**第三，流式要有有界队列。** 上游每秒吐几十个事件，下游是弱网手机，中间只要有一个无界缓冲，并发一上来内存就飙。做法是生产者队列满时等待、而不是丢弃或无限堆积，并且容量同时限制事件数与字节数——一百个短 token 和一百个工具调用结果完全不是一个量级。顺带一句：`nginx` 默认会缓冲响应，流式接上去发现「一次性刷出全文」，多半是漏了 `X-Accel-Buffering: no`。

参考资料：
- [LLM Streaming UX: Backpressure & Cancellation -- DevOpsNess](https://www.devopsness.com/blog/llm-streaming-ux-backpressure-cancellation) ⭐值得阅读
- [大模型流式输出上线后才遇到的问题：断连、取消、背压与重复计费排查 -- CSDN](https://blog.csdn.net/qq_50684356/article/details/166227212) ⭐值得阅读
- [接口一压就报 429：令牌桶限流、指数退避与抖动重试的落地实践 -- 腾讯云开发者社区](https://developer.cloud.tencent.com/article/2748371) ⭐值得阅读
- [Your retry logic is making your outage worse -- Digital Aultis](https://digitalaultis.com/journal/your-retry-logic-is-making-your-outage-worse/)

## 5. 安全不是加个鉴权就完事（Security）

很多团队的安全方案只有一句话：「接口加了鉴权，非登录用户进不来。」这句话等于给写字楼装了一扇门禁，然后放心地把整层楼的文件柜敞开。AI 接口的安全面比普通 CRUD（Create、Read、Update、Delete，增删改查）宽得多：你不只传参数，还把用户的原话、订单号、身份证、内部文档一起塞进了 prompt，而模型的返回又会被直接拼进 SQL、HTML 或者下一轮工具调用。

按数据流向拆三层，每层只回答一个问题：密钥会不会被业务带走、用户数据会不会被模型带走、模型的输出会不会把攻击带回来。

**第一层：密钥不出网关。** 业务侧拿到的必须是虚拟密钥（virtual key，前缀通常写作 `vk-`），真 key 只存在网关的环境变量里，最好再交给 KMS（Key Management Service，密钥管理服务）托管，由它负责加密存储与定期轮换。这样做的好处不在「更安全」这句空话，而在事故发生时的处置半径：虚拟密钥能按租户单独吊销、单独限额、单独记账，一个租户的 key 泄露不会波及全公司；真 key 一旦发给业务方，你就只剩下「全量轮换 + 挨个通知下游重启」这一条路。阿里云 AI 网关（AI Gateway）的产品设计把这件事拆成消费者鉴权与后端鉴权两道，前面认业务、后面认模型，中间那一段谁都不持有明文 key。

**第二层：数据不出边界。** 用户手机号、身份证、银行卡、病历这些个人信息（PII，Personally Identifiable Information）在进模型之前就该处理掉。这里最忌讳两种偷懒做法：一是不处理，二是简单打码成 `***`——打码后模型看不懂上下文，回答质量断崖式下跌，业务方第二天就会要求关掉这个开关。可行的做法是 **替换成合成 token**：把「张三的手机号是 138xxxx」换成「`USER_NAME_1` 的手机号是 `PHONE_1`」，语义完整保留，模型照样能推理；映射表存在服务端，模型返回后再还原。微软开源的 Presidio 就是为这件事准备的，Analyzer 负责识别、Anonymizer 负责替换、Image Redactor 处理截图里的文字。补两个容易漏的点：一是 **输出侧要再扫一遍**，模型可能自己编出一个手机号或者把映射表里的原文复述出来；二是 **审计日志只记 hash**，否则你为了合规建的日志，本身就是一份泄露清单。

**第三层：输出不回污染。** OWASP 的 LLM 应用风险榜单里，排第一的是提示词注入（prompt injection，LLM01），第十是无界消耗（unbounded consumption，LLM10）。前者说的是用户输入可以伪装成指令，让你精心写好的 system prompt 失效；后者说的是有人用超长输入、无限重试、批量刷接口把你账单打穿——这两条恰好一头一尾，一个偷你的权限，一个偷你的钱。工程上能落地的控制不多但很实在：把模型输出当成 **不可信输入** 处理，不要直接拼进 SQL、不要直接 `eval`、不要直接当 HTML 渲染；要求结构化输出时用 JSON Schema 校验，校验不过就重试或降级，而不是「大概是这个格式就往下走」；工具调用要有白名单，模型只能调用注册过的函数，参数还要按类型再校验一次。

一句总结这三层的关系：门禁管「谁能进」，保安管「带了什么进来」，X 光机管「出去的东西里有没有夹带」。三道都装，才叫安全；只装门禁，那叫心理安慰。

参考资料：
- [LLM01: Prompt Injection -- OWASP GenAI](https://genai.owasp.org/llmrisk/llm01-prompt-injection/) ⭐值得阅读
- [LLM10: Unbounded Consumption -- OWASP](https://owasp.org/www-project-top-10-for-large-language-model-applications/2_0_vulns/LLM10_UnboundedConsumption) ⭐值得阅读
- [How to Protect PII and Secrets in LLM Apps -- Khimananda](https://khimananda.com/blog/protect-pii-and-secrets-in-llm-apps) ⭐值得阅读
- [Presidio FAQ: PII Detection and De-identification -- Microsoft](https://omri374.github.io/presidio/faq/)
- [什么是 AI 网关：安全三层与数据脱敏插件 -- 阿里云](https://help.aliyun.com/zh/api-gateway/ai-gateway/product-overview/what-is-an-ai-gateway) ⭐值得阅读

## 6. 成本不是一个单价，是四个维度（Cost）

被问「这个功能一个月多少钱」时，答不上来通常不是数学问题，而是没搞清楚计费口径。AI 接口的账单由四个维度共同决定：调的哪个模型、输入多少 token、输出多少 token、有没有吃到缓存或走了错峰。缺少任何一个，报出来的数都是错的——同一次调用在不同维度组合下，成本能差十倍。

第一个容易被低估的机制是 **阶梯计费**。以阿里云百炼的 qwen3-max 为例，单次请求输入在 32K 以内时输入 2.5 元、输出 10 元（单位是元每百万 token）；32K 到 128K 档输入涨到 4 元；128K 到 256K 档涨到 7 元。关键在结算方式：**一旦请求跨过阶梯边界，这个请求里的所有 token 都按高档单价结算**，不是超出部分才涨价。所以长上下文场景的成本曲线是跳变的，不是线性的。把一份 40K 的合同全文塞进去，成本不是 32K 时的 1.25 倍，而是直接跳到 1.6 倍的输入单价。

拿客服场景算一笔可复算的账：月处理 100 万次对话，每次 2000 个输入 token、500 个输出 token，用 qwen3-max 的 32K 档。输入侧 `100 万 × 2000 ÷ 100 万 × 2.5 = 5000 元`，输出侧 `100 万 × 500 ÷ 100 万 × 10 = 5000 元`，合计约 1 万元每月。注意两侧刚好各占一半——很多人只盯着输入，结果优化了半天只动了半边账单。

第二个杠杆是 **提示词缓存（prompt caching，提示词缓存）**。原理是把请求前缀里稳定不变的部分（system prompt、few-shot 示例、知识库片段）缓存起来，命中的部分按极低价格计费。各家倍数不完全一样，但量级接近：写入缓存通常按 1.25 倍到 2 倍输入价收费，命中后按 0.1 倍左右计费。阿里云百炼对支持的模型默认开启隐式缓存，命中的输入前缀按输入单价的较低比例计费。

这里有个反直觉的坑，值得单独提醒：**先保证缓存能命中，再谈精简 prompt**。如果系统提示稳定命中缓存，精简它省下的钱只是「低价那部分」的零头；反过来，为了精简而频繁改动前缀，导致缓存全部失效，账单反而会涨。顺序颠倒的团队经常在周报里写「精简 prompt 节省 40%」，实际账单纹丝不动，因为节省是按全价算出来的纸面数字。

第三个杠杆是 **批处理（batch API，批量接口）**。不需要实时返回的任务——离线打标、历史数据清洗、日报摘要——扔进批处理能便宜一半：OpenAI、Anthropic、Google、Mistral、阿里都按对半计价，AWS Bedrock 的批量推理同样是按需价格的 50%。这是投入产出比最高的一档优化，因为它几乎不改业务代码，只改提交方式；代价是延迟从秒级变成小时级，所以只适合异步任务。

第四个杠杆是 **模型路由（model routing，模型路由）**。轻量与旗舰模型的单价差距常在数倍到十倍以上，而真实流量里大部分请求并不需要旗舰模型：闲聊、分类、抽取字段、改写标题，小模型完全够用。落地方式是给每个业务场景配「主模型 + 兜底模型」，命中简单意图走小模型，置信度低或校验失败再升级到旗舰；再往前一步是本地缓存完全相同的问答，FAQ 类流量命中率能到三成以上，这部分成本直接归零。

最后一句关于预算：第 4 章代码里的 `Ledger` 是进程内字典，单机演示够用，生产环境必须换成 Redis 或数据库，否则多副本部署时每个副本各记各的账，预算形同虚设。账本还要能按虚拟密钥、租户、功能三个维度拆开，否则月底你只知道「花了很多」，不知道「谁花的、花在哪」。

参考资料：
- [LLM Batch API pricing: what the 50% discount really buys -- AI//COST](https://aicost.tools/blog/llm-batch-api-discount/) ⭐值得阅读
- [成本支柱：Token 经济学与提示词预算工程化 -- 阿里云](https://help.aliyun.com/zh/document_detail/3063429.html) ⭐值得阅读

## 7. 看不见的故障最贵（Observability）

前面六章的东西，只有在你能看见现场时才有效。而 AI 接口的故障恰恰最擅长隐身：`200 OK` 返回了、日志没有 error、平均延迟还降了——与此同时用户在骂回答太慢，财务在问账单为什么翻倍。传统监控盯的是「服务活没活」，AI 接口要盯的是「这次调用值不值」。

标准答案是 OpenTelemetry 的生成式 AI 语义约定（GenAI semantic conventions，生成式 AI 语义约定）。它把一次模型调用该记什么定死了：`gen_ai.provider.name` 记厂商，`gen_ai.request.model` 记模型，`gen_ai.usage.input_tokens` 与 `gen_ai.usage.output_tokens` 记用量；操作类型覆盖 chat、embeddings、execute_tool、invoke_agent。好处不是「多了一套标准」，而是同一份 trace 能在网关、业务服务、Agent 编排三层之间串起来——用户在页面上点的那一下，和最后落在厂商账单上的那笔钱，是同一棵树上的节点。注意 prompt 与 completion 的原文属于 **可选采集项**，默认关掉，否则你的链路追踪会变成一个装满用户隐私的数据库。

指标体系建议按四组铺，每组只回答一个问题：

| 组别 | 关键指标 | 回答什么问题 |
|---|---|---|
| 性能 | TTFT（Time To First Token，首 token 时间）、TGS（Tokens per Second，生成速度）、P95/P99 端到端耗时 | 用户到底等了多久 |
| 可用性 | 成功率、429 率、5xx 率、熔断开启次数、重试成功率 | 上游抖没抖，兜住没有 |
| 成本 | 单请求 token 成本、缓存命中率、Batch 占比、异常重试成本 | 钱花在哪，有没有白花 |
| 安全 | 护栏命中率、注入拦截率、PII 识别率 | 防线有没有被绕过 |

有三个坑几乎每个团队都会踩。**第一，别用平均延迟做告警**。平均值会被大量命中的缓存请求拉平，真正出问题的是那 1% 卡了 90 秒的请求——用 P95/P99，并且按模型、按租户分开看，否则一个大客户的慢请求会把整体 P95 拉爆，而你分不清是他慢还是上游慢。**第二，把取消率单独记一笔**。第 4 章说过约 12% 的对话请求在完成前被取消，这个数字既是体验指标（用户等不及了），也是成本指标（token 已经烧了）——取消率高而账单不降，说明取消信号没传到上游。**第三，重试成本要单独归因**。熔断和重试救的是可用性，花的是钱；如果账本把重试消耗混进正常请求，你永远算不出「上游抖动这个月让我们多花了多少」。

再补一句 Agent 场景的差异。单次 API 调用失败有错误码，多轮 Agent 任务的失败常常是「静默失败」：工具调了一半、检索召回错了、阶段成果丢了，返回的却是一段看起来通顺的回答。中国信通院与阿里云联合编制的 AI 推理服务稳定性报告里，把这类问题的观测指标单列成任务完成率、平均执行步数、工具调用成功率与断点续跑成功率——它们的共同点是：**不报错，但不对**。所以网关层能给你的是延迟与成本，业务层必须自己补上质量与任务级指标，这两层缺一层，你的仪表盘就只是后视镜。

参考资料：
- [Inside the LLM Call: GenAI Observability with OpenTelemetry -- OpenTelemetry](https://opentelemetry.io/blog/2026/genai-observability/) ⭐值得阅读
- [Gen AI Semantic Conventions: Attribute Registry -- OpenTelemetry](https://opentelemetry.io/docs/specs/semconv/registry/attributes/gen-ai/) ⭐值得阅读
- [公共云 AI 推理服务稳定性建设研究报告 -- 中国信息通信研究院](http://www.caict.ac.cn/kxyj/qwfb/ztbg/202610/P020261012572436061557.pdf) ⭐值得阅读

## 8. 这层网关拦不住什么（Non-Goals）

写到这里必须把边界说清楚，否则你会误以为装上网关就万事大吉。网关是小区门口的保安：他能查证件、能拦外面的车、能登记访客，但他管不了住户在屋里做什么。

**第一，它拦不住语义错误。** 模型答非所问、编造引用、把两份合同的关键条款搞混，这些请求的 HTTP 状态码全是 200，token 用量也完全正常。网关最多做到「结构化输出校验失败就重试」，而「内容对不对」需要评测集、引用追溯和低置信度兜底，那是业务侧的事。信通院的报告把这类失败叫静默失败，说得很准：不报错，但不对。

**第二，它拦不住合规主体责任。** 备案登记、训练语料合规、生成合成内容标识、审核过滤能力——这些是运营主体的责任，网关只能承担其中「内容安全检测」这一小块技术措施。中央网信办的「清朗·整治 AI 应用乱象」专项行动里，第一阶段列的七类问题中，未按规定履行备案登记、安全审核能力不足、生成合成内容标识落实不到位都单列在案。换句话说，网关是必要项，不是免责项。

**第三，它拦不住「能跑但被重复执行」的请求。** 这里有个特别容易踩的坑：对上游厂商的 POST 请求做重试，语义上并不幂等。两次采样即使 prompt 完全一样，返回内容也不同，而且 **两份都计费**。所以第 4 章的重试只对「确定没成功」的失败开放，且上限两次；真正的业务级幂等要靠客户端带上 `Idempotency-Key` 请求头，服务端按 key 去重并返回第一次的结果，IETF 的 HTTP API 幂等键草案（draft-ietf-httpapi-idempotency-key-header）就是为这类场景写的，面向 AI Agent 的 HTTP API 设计文档也明确建议：有副作用的操作要支持客户端传入幂等键，让重试安全、可预览、可撤销。

**第四，多模态与出境这两个缺口常被漏掉。** 图片、音频、视频按不同规则计费，内容审核也走不同通道，网关如果只按文本 token 记账，账单会对不上；数据出境则取决于厂商的部署区域与你的调用链路，这不是加个开关能解决的，得在架构评审阶段就定下来。

知道拦不住什么，才知道该在哪里加第二道防线。下面这张清单，就是把这些「拦不住」逐条变成上线前的自查项。

参考资料：
- [The Idempotency-Key HTTP Request Header Field -- IETF Datatracker](https://datatracker.ietf.org/doc/html/draft-ietf-httpapi-idempotency-key-header-02) ⭐值得阅读
- [Design Considerations and Profile for HTTP APIs Consumed by AI Agents -- IETF](https://www.ietf.org/archive/id/draft-gaikwad-agent-friendly-http-api-profile-01.html) ⭐值得阅读
- [中央网信办部署开展「清朗·整治 AI 应用乱象」专项行动 -- 新华网](https://app.xinhuanet.com/news/article.html?articleId=20260430b1c17b7a72ad4d2ea8204fdf14fc95b9) ⭐值得阅读

## 9. 上线前自检清单（Pre-launch Checklist）

把前八章压缩成十二个可以逐条打勾的问题。每条都给合格线，不给「建议关注」这种废话——验收时说不清合格线的项，等于没做。

| # | 检查项 | 合格线 | 不通过的后果 |
|---|---|---|---|
| 1 | 业务代码是否持有厂商 key | 只有网关持有，业务拿 `vk-` 虚拟密钥 | 换供应商要改 N 个服务 |
| 2 | 超时是否分级 | 短对话 5s、长文 15–30s、embedding 3s，流式另设三档 | 长文档总结固定时刻失败 |
| 3 | 重试是否有选择 | 只重试 429/5xx/超时/连接失败，上限 2 次，带抖动 | 高峰期重试放大成雪崩 |
| 4 | 是否有熔断 | 连续失败 3 次开启，冷却 10s，半开探测 | 上游挂了，你的线程池先挂 |
| 5 | 限流是否分桶 | 至少按租户 + 模型两维，容量 = 速率 × 2 | 一个租户打满整个模型 |
| 6 | 预算是否前置 | 请求前校验，超额直接拒绝；账本落 Redis/DB | 事后告警，钱已经花完 |
| 7 | PII 是否出边界 | 请求前替换、返回后还原、输出侧二次扫描 | 一次泄露就是合规事故 |
| 8 | 审计日志是否留原文 | 只记 hash 与 token 数，不记明文 | 日志本身成为泄露源 |
| 9 | 输出是否当不可信数据 | Schema 校验 + 工具白名单，不直接进 SQL/HTML | 提示词注入变成 RCE 或 XSS |
| 10 | 是否按 OTel GenAI 打点 | `gen_ai.*` 属性齐全，trace 能串到业务请求 | 故障只能看「接口 500」 |
| 11 | 延迟告警是否用分位数 | P95/P99，按模型与租户拆分 | 均值掩盖长尾，用户先炸 |
| 12 | 是否支持幂等键 | 有副作用的写操作接受 `Idempotency-Key` | 用户重试两次，扣两份钱 |

十二条里最容易被跳过的是第 6 和第 8 条：它们不产生任何功能，只在事故发生时决定你是「损失可控」还是「损失不可控」。工程上真正值钱的往往是这类平时看不见的东西。

AI 功能已进生产、多个业务方共用模型账号时，这层网关必须做；还在内部试水、一天几百次调用，直接调 SDK 更快，等账单和故障真来了再抽这层也不迟。

本专栏《AI 开发范式》收录 AI 能力落到工程侧的具体做法：网关、评测、Agent 可靠性、成本治理，每篇都配一段能直接跑的代码，每周更新一篇。想按顺序读完，可在专栏页订阅。
