# Agent 查不出代码 Bug 怎么办：一份带时间戳的调试日志与读日志排查流程

> **核心结论**：AI 查不出 bug，多数时候不是模型不够聪明，而是它手里没有运行现场。读源码等于只看户型图，看不见漏水点。补上三样东西——带毫秒时间戳的 log（日志）、每个边界的数据 snapshot（快照）、一条贯穿全链路的 trace_id（链路标识）——再稳定复现一次，把日志交给 AI，定位效率会有量级变化。下文给一份可直接跑的埋点模板和一套读日志的顺序。

---

## 目录

- 1. AI 读的是代码，不是运行现场
- 2. 一条好日志的三个字段
- 3. 先复现，再读日志
- 4. 可直接运行的埋点模板
- 5. 让 AI 按时间线做因果排除
- 6. 症状 → 原因 → 解法对照表
- 7. 埋点位置清单：只在四个边界打
- 8. 四个把日志变废纸的坑
- 9. 什么时候日志救不了你

---

## 1. AI 读的是代码，不是运行现场（Code vs Runtime）

你让 AI 看一段代码，它能判断的是**写法层面**的问题：变量有没有定义、分支有没有漏、循环边界是否越界。它看不到的是**运行时（runtime）真正流过的值**——数据库里那条 `amount` 是字符串还是数字、接口返回的 `null` 会不会一路传到 `len()`、时区差 8 小时之后日期算到了哪一天。

举个最常见的现场：代码写着 `int(row["amount"])`，语法完全正确，静态读一百遍也读不出问题；但只要上游传进来的是 `"12.5"`，这一行必炸。问题不在逻辑，在**数据契约（data contract）**。而数据契约只存在于运行时，只存在于日志里。

打个比方 🔍：让 AI 只读代码去定位 bug，就像让侦探只看户型图去抓漏水——他知道哪面墙后面是水管，但不知道哪根管子正在滴水。

这里的收益可以用一个很小的算式说清。假设一条流水线有 6 个阶段，静态读代码时你有 6 个嫌疑段；如果每个阶段都打「进入 / 退出」两条日志，那么缺少一条 `exit` 就能把故障锁进 1 个阶段。定位范围从 6 段压到 1 段，收敛比例是 $(6-1)/6 \approx 83.3\%$。这个数字不依赖任何玄学，只取决于你打了多少个边界。

「日志能解决 99% 的问题」这类说法没有可复算的依据，不必当真。有意义的是**覆盖率**：你埋了点的分支，占所有可能出错分支的比例，就是这个方法能定位到的上限。埋得越密，区间收得越窄。

---

## 2. 一条好日志的三个字段（Log Fields）

日志不是写给人看的日记，而是写给机器读的事件流。Twelve-Factor 的说法很干脆：日志是**按时间排序的事件流（event stream）**，一个事件一行，直接写进 `stdout`，不自己做路由和存储。OpenTelemetry 的定义也一致：一条 log 就是**带时间戳的记录**，推荐用结构化格式。

一份能被 AI 直接读的日志，每行至少要带三个字段：

| 字段 | 作用 | 反例 | 正例 |
|---|---|---|---|
| 时间戳 | 把多行日志还原成时间线 | `2026-11-13 10:31:07`（无时区、无毫秒） | `2026-11-13T02:31:07.412+00:00` |
| trace_id | 把同一次运行的所有行串起来 | 每行独立，靠猜哪几行属于同一次 | `trace=9f3c1a7e`，全链路一致 |
| data 快照 | 记录当时真实流过的值 | `parse failed` | `{"row": {"id": 3, "amount": "12.5"}}` |

结构化日志（structured logging）的通用字段清单通常是：ISO 8601 的 UTC 时间戳、level、service、environment、trace_id，再按需补 `duration_ms`、`error.type`、`error.stack`。你不必一次全上，但**时间戳、trace、快照这三样缺一样，日志就退化成散文**。

再补一个容易被忽略的字段：`seq`。同一毫秒内可能打十几条日志，光靠时间戳排不出先后；一个进程内自增的序号，能让「谁在前谁在后」变成确定事实。

日志字段与变量的参考资料：
- [Logs -- The Twelve-Factor App](https://www.12factor.net/logs) ⭐值得阅读
- [Logs -- OpenTelemetry](https://opentelemetry.io/docs/concepts/signals/logs/) ⭐值得阅读
- [Structured logging best practices -- Middleware](https://middleware.io/blog/structured-logging-best-practices/)

---

## 3. 先复现，再读日志（Reproduction）

日志的价值建立在「同一次运行」上。如果每次跑输入都不一样，你拿到的是一堆无法对齐的碎片，AI 读得再细也只能编故事。

复现要做的事只有四件：

1. **把触发 bug 的入参存成 fixture（固定输入）**，落到 `fixtures/bug_input.json`，以后每次都用这一份。
2. **固定不确定源**：随机种子、当前时间、时区、并发度。排查期间把并发降到 1，让顺序可预测。
3. **把输出落盘**：`python demo.py > bug.log 2>&1`，注意 `2>&1` 要写在重定向后面，否则报错信息还在终端里，日志文件只有一半。
4. **确认「同一份输入必然复现」**，再开始加日志。加一条、跑一次、看一行，比一次性埋二十条再猜快得多。

一次成功复现，等于拿到了三样东西：可以反复加日志的现场、可以验证修复的回归用例、可以交给 AI 的原始证据。缺了这一步，后面全是猜。

---

## 4. 可直接运行的埋点模板（Runnable Template）

下面这段直接存成 `demo_bug.py` 就能跑。它是一条 6 段流水线的缩小版：加载数据、逐条解析、累加。第 3 条数据是脏的（`"12.5"`），`int()` 会抛异常——这正是我们要让 AI 通过日志看见的东西。

```python
# demo_bug.py：一条故意写坏的流水线，配一套能被 AI 直接读的 JSON 日志
import json
import logging
import sys
import uuid
from datetime import datetime, timezone


class JsonFormatter(logging.Formatter):
    """把每条日志压成一行 JSON，方便 grep、排序，也方便模型逐行读"""

    def format(self, record):
        payload = {
            # 统一用 UTC + 毫秒，跨机器排序不会错位
            "ts": datetime.fromtimestamp(record.created, timezone.utc).isoformat(timespec="milliseconds"),
            "level": record.levelname,
            "trace": getattr(record, "trace", "-"),      # 同一次运行共用一个 trace
            "seq": getattr(record, "seq", 0),            # 进程内自增，用来定先后
            "stage": getattr(record, "stage", "-"),      # 哪个阶段
            "event": getattr(record, "event", "-"),      # enter / exit / exception
            "data": getattr(record, "data", None),       # 当时真实流过的值
        }
        if record.exc_info:
            payload["err"] = self.formatException(record.exc_info)   # 堆栈别丢
        return json.dumps(payload, ensure_ascii=False)


logger = logging.getLogger("demo")
logger.setLevel(logging.DEBUG)
handler = logging.StreamHandler(sys.stdout)          # 日志写 stdout，交给外部收集
handler.setFormatter(JsonFormatter())
logger.addHandler(handler)
logger.propagate = False

_seq = 0                                             # 全局序号，每打一条加一


def log(trace, stage, event, data=None, level=logging.INFO):
    """在边界上打一个点：谁、哪一步、进还是出、当时的数据长什么样"""
    global _seq
    _seq += 1
    logger.log(
        level,
        f"{stage}.{event}",
        extra={"trace": trace, "seq": _seq, "stage": stage, "event": event, "data": data},
    )


def load_rows(trace):
    """加载待处理数据；真实项目里换成数据库或接口查询"""
    log(trace, "load_rows", "enter", {"source": "fixture"})
    rows = [
        {"id": 1, "amount": "10"},
        {"id": 2, "amount": "20"},
        {"id": 3, "amount": "12.5"},                 # 复现用的那条脏数据
    ]
    log(trace, "load_rows", "exit", {"count": len(rows)})
    return rows


def parse_amount(row, trace):
    """把金额解析成整数；字符串带小数点时，int() 必然抛 ValueError"""
    log(trace, "parse_amount", "enter", {"row": row})
    amount = int(row["amount"])                      # 故障点：int("12.5")
    log(trace, "parse_amount", "exit", {"amount": amount})
    return amount


def compute(rows, trace):
    """逐条累加；每条都打进入 / 退出，缺一条就能看出断在哪"""
    total = 0
    for row in rows:
        log(trace, "compute", "enter_item", {"id": row["id"]})
        total += parse_amount(row, trace)
        log(trace, "compute", "exit_item", {"id": row["id"], "total": total})
    return total


def main():
    """入口：分配 trace，捕获异常时连同堆栈一起落盘"""
    trace = uuid.uuid4().hex[:8]
    log(trace, "main", "enter", {"trace": trace})
    try:
        total = compute(load_rows(trace), trace)
        log(trace, "main", "exit", {"total": total})
    except Exception:
        log(trace, "main", "exception", {"action": "abort"}, level=logging.ERROR)
        logger.exception("pipeline failed", extra={"trace": trace, "seq": _seq, "stage": "main", "event": "traceback", "data": None})
        raise


if __name__ == "__main__":
    main()
```

跑一次，日志长这样（截取关键几行）：

```json
{"ts": "2026-11-13T02:31:07.415+00:00", "level": "INFO", "trace": "9f3c1a7e", "seq": 12, "stage": "compute", "event": "enter_item", "data": {"id": 3}}
{"ts": "2026-11-13T02:31:07.415+00:00", "level": "INFO", "trace": "9f3c1a7e", "seq": 13, "stage": "parse_amount", "event": "enter", "data": {"row": {"id": 3, "amount": "12.5"}}}
{"ts": "2026-11-13T02:31:07.416+00:00", "level": "ERROR", "trace": "9f3c1a7e", "seq": 14, "stage": "main", "event": "exception", "data": {"action": "abort"}}
{"ts": "2026-11-13T02:31:07.416+00:00", "level": "ERROR", "trace": "9f3c1a7e", "seq": 15, "stage": "main", "event": "traceback", "data": null, "err": "ValueError: invalid literal for int() with base 10: '12.5'"}
```

读法只有一句：`seq=13` 的 `parse_amount.enter` 之后，下一条直接是 `seq=14` 的 `main.exception`，中间**没有对应的 `exit`**——故障就锁死在 `parse_amount` 里。再看 `enter` 的 `data`，`"amount": "12.5"` 是字符串，而代码是 `int()`，异常是必然而不是偶然。

Python 的 logging 模块本身提供了足够的能力：`logging.exception()` 只在异常处理块里调用，会自动把 traceback 追加到消息里；日志级别从 `DEBUG` 到 `CRITICAL`，按「谁会消费这条信息」来选，而不是随手写 `print`。

日志模块与异常堆栈的参考资料：
- [Logging HOWTO -- Python 官方文档](https://docs.python.org/3/howto/logging.html) ⭐值得阅读

---

## 5. 让 AI 按时间线做因果排除（Log-Driven Triage）

拿到日志后，别整份贴给 AI。几千行原始文本只会让模型摘抄，不会让它推理。正确顺序是：**先过滤，再排序，最后只让它做三件事**。

第一步，按 trace 过滤，只留这一次运行：

```bash
grep '"trace": "9f3c1a7e"' bug.log > one_run.log
```

第二步，检查 `seq` 是否连续。序号跳号通常意味着有日志没落盘（异步写入丢缓冲），这本身就是一条线索。

第三步，给 AI 一段固定格式的指令，把「改代码」这个冲动先按下去：

```markdown
下面是一次运行的 JSON 日志，已按 seq 排好序。只做三件事，不要改代码：
1. 画出时间线：每一步的 stage、event、关键 data；
2. 指出断点：最后一个成功事件，和第一个异常事件之间，缺了哪条日志；
3. 给出两个可验证假设，每个假设配一条验证命令，或一行需要补打的日志。
```

为什么一定要限制输出形态？因为「帮我看看哪里错了」这种开放提问，模型最容易给出「可能是空值、也可能是类型问题、建议加日志」这类正确但无用的回答。而「缺哪条日志」是一个有唯一答案的问题，答错了一眼就能看出来。

验证顺序也要固定：先补日志验证假设，再改代码。跳过验证直接改，往往会顺手改坏三处，最后连原来的症状都复现不了。在[Agent 如何动态存储运行时经验](https://juejin.cn/post/7706762779600830490)中我们讲过，一次排查的价值不止修好这一次，更在于把结论沉淀成下次能直接调用的经验——日志就是这份经验的原始素材。

---

## 6. 症状 → 原因 → 解法对照表（Symptom Table）

| 症状 | 原因 | 解法 |
|---|---|---|
| AI 说「代码看起来没问题」 | 它只读到源码，没读到运行时的值 | 补边界日志，复现一次，把日志交给它 |
| 改了三处还是没修好 | 没有断点，一直在按猜测改 | 先定位到具体 stage，再动代码 |
| 偶发 bug 抓不到 | 每次输入都不同，无法对齐 | 把触发出参存成 fixture，固定种子、时钟与并发 |
| 日志几千行，AI 读完还是懵 | 没有 trace 和 seq，顺序靠猜 | 按 trace 过滤，按 seq 排序，只给它一次运行 |
| 异常只有一句 `error` | 没打数据快照和堆栈 | `logging.exception()` 带 traceback，日志里加 data |
| 修好了，下周又犯 | 没有沉淀成判据 | 把这次的日志特征写进排查 checklist |

---

## 7. 埋点位置清单：只在四个边界打（Instrumentation Points）

埋点不是越多越好。全函数覆盖会把日志变成噪音，真正有效的是**边界**——数据进入、离开、变化、失败的那四个瞬间。

| 位置 | 打什么 | 解决什么问题 |
|---|---|---|
| 阶段进出 | stage、event、关键入参 | 缺一条 `exit` 就是断点 |
| 外部调用 | 方法、URL、耗时、状态码、响应前 200 字 | 区分「本地逻辑错」和「下游返回错」 |
| 状态变更 | 变更前后的值、主键 | 定位数据被写坏的那一刻 |
| 异常与重试 | 堆栈、重试次数、退避时长 | 区分偶发失败与必现失败 |

一条实用约束：**循环体内部不要逐条打 INFO**。一万条数据就是一万行日志，AI 读不完。循环里只打首条、末条和异常条，或者按 1% 采样，其余靠聚合数字（总数、成功数、失败数）表达。

---

## 8. 四个把日志变废纸的坑（Pitfalls）

**坑一：时间戳用本地时间，还不带时区。** 本地时间在跨机器、跨容器时无法排序，夏令时还会出现重复的一小时。统一用 UTC + ISO 8601 + 毫秒，展示层再转本地时区。

**坑二：只写「失败了」，不写当时的值。** `parse failed` 和 `parse failed, row={"amount": "12.5"}` 的信息量差一个数量级。前者只能让你猜，后者能让你直接判断。

**坑三：把 token、密码、手机号写进 data。** 日志会被收集、转发、长期留存，一旦进日志就等于进了公共仓库。打点前先脱敏，手机号只留后四位，token 只留前六位。

**坑四：并发场景靠打印顺序理解因果。** 多线程或多进程下，写入顺序和实际执行顺序无关。用 `trace + seq` 建立因果关系，不要靠「它出现在后面所以它后发生」。

---

## 9. 什么时候日志救不了你（Verdict）

日志解决的是「**值不对**」这一类问题：空值、类型错、顺序错、分支走错。它解决不了另外几类：

- **性能问题** —— 日志只能告诉你哪一步慢，不能告诉你为什么慢。这时候要上 profiler（性能剖析器），看 CPU 火焰图和内存分配。
- **样式与渲染问题** —— 页面错位、颜色不对，日志里什么都没有。截图加元素审查比日志快十倍。
- **无法复现的线上偶发** —— 没有稳定输入，日志只能提供旁证。这时需要分布式 trace（分布式链路追踪）和采样，而不是继续加打印。
- **崩溃与内存泄漏** —— 进程直接挂掉时日志可能没落盘。要 core dump（核心转储）或 heap snapshot（堆快照）。

判断标准很朴素：**这个问题能不能用「某个值在某一步不对」描述**。能，就上日志；不能，就换工具。日志不是万能钥匙，它只是把「看不见的运行时」变成「可读的一行行事实」。

---

能稳定复现、关键边界都有快照时，这套流程值得用；问题无法复现、或根因落在性能与资源上时，先换 profiler，别指望多打几行日志。

本专栏《AI Agent 工具专栏》从工具调用、记忆管理、上下文压缩一路讲到调试排查与运行时观测，每篇配一段可直接运行的代码和一张症状对照表，每周更新一篇。想系统看完 Agent 工程这条线，可在专栏页订阅。
