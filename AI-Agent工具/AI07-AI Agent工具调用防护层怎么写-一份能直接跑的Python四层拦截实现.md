# AI Agent 工具调用防护层怎么写：一份能直接跑的 Python 四层拦截实现

四层防护不用从零设计。下面这 150 行 Python 就是完整骨架，只依赖标准库，复制进 `guard.py` 直接运行，五个典型场景会依次打印出每一层在哪一步拦下调用——参数名幻觉、类型错误、越权、硬禁、重复调用，一条不漏。

## 目录

1. 这层代码管什么
2. 跑不通的症状对照表
3. 完整实现
4. 运行结果怎么读
5. 接进现有 Agent 的三个接入点
6. 边界：这层拦不住什么
7. 参考资料

## 1. 这层代码管什么（Scope）

设计原则在《AI Agent 工具误调用怎么解决》里已经讲完，本篇只做一件事：把它们收进一个文件。

这层代码像公司财务的报销审批：不管你是实习生还是总监，单据都得走同一套流程，唯一的区别是审批人不会疲劳、不会碍于情面放行。它就是 `ToolGuard`（工具防护执行器），三个约束贯穿全文：

1. **只依赖标准库**，无框架绑定，方便嵌进任何 runtime（运行时）；
2. **每次判定都返回结构化结果**，`status` + `layer` + `detail` 三个字段，直接可写审计 log（日志）；
3. **判定顺序固定**，白名单 → 硬禁 → 权限 → 确认 → 参数 → 熔断，顺序错了防线就会漏。

它管的是「不该发生的调用」，不管「调用合法但业务算错」。这条边界放在第 6 节细说。

## 2. 跑不通的症状对照表（Symptom, Cause, Fix）

自己写这层防护时，最常卡在下面五处。表里的现象都来自这段代码的真实行为，不是假设。

| 症状 | 原因 | 解法 |
|---|---|---|
| 高危工具加进候选集后，模型立刻开始乱选 | 只做了权限校验，没做暴露收敛，注册表全量下发给模型 | 用 `visible_tools()` 的输出生成候选集，别把 `REGISTRY` 整个塞给模型 |
| 加了确认逻辑，业务却一直卡在「待确认」 | 确认结果没有回传成 `confirmed=True` | `pending_confirm` 是正常状态不是异常，弹窗结果必须写回再调一次 |
| 幻觉出的参数名被静默忽略，查出来的结果不对 | 只校验了必填项，没有拒绝未定义字段 | 遍历参数做白名单校验，`key not in spec.schema` 直接拒绝 |
| 同参数重复调用十几次仍然放行 | 指纹直接序列化原始参数，两次 key 顺序不同就成了两个指纹 | 指纹用 `sort_keys=True`，保证 key 顺序无关 |
| 普通用户也能调到 L2 高危工具 | `max_level` 按角色写死成 2 | 普通用户 0、管理员 2，且硬禁名单判断优先于等级判断 |

## 3. 完整实现（Full Implementation）

整段代码没有省略，`if __name__ == "__main__"` 已经在文件末尾，复制保存后就能运行。

```python
"""AI Agent 工具调用四层防护：最小可运行实现（仅依赖标准库）。"""

import hashlib  # 生成调用指纹，用于重复调用熔断
import json  # 稳定序列化参数，保证指纹可复算
from dataclasses import dataclass  # 定义规格与结果结构
from typing import Any, Callable  # 类型注解


@dataclass(frozen=True)
class ToolSpec:
    """工具规格：风险等级 + 参数类型 + 必填项 + 执行函数。"""

    name: str  # 工具名，必须与模型输出的函数名一致
    level: int  # 风险等级：0 只读 / 1 写入 / 2 高危
    schema: dict[str, type]  # 参数名到期望类型的映射
    required: tuple[str, ...]  # 必填参数集合，缺失即拒绝
    handler: Callable[..., Any]  # 真正执行业务逻辑的函数


REGISTRY: dict[str, ToolSpec] = {  # 工具注册表，未登记的工具一律不可调用
    "query_report": ToolSpec(  # L0 只读工具
        "query_report", 0,  # 名称与风险等级
        {"report_id": str, "max_rows": int},  # 参数类型约束
        ("report_id",),  # 只有 report_id 必填
        lambda report_id, max_rows=100: f"报表 {report_id} 返回 {max_rows} 行",  # 模拟执行
    ),
    "purge_cache": ToolSpec(  # L2 高危工具，结果不可逆
        "purge_cache", 2,  # 名称与风险等级
        {"scope": str},  # 参数类型约束
        ("scope",),  # scope 必填
        lambda scope: f"已清理缓存 scope={scope}",  # 模拟执行
    ),
    "delete_all_logs": ToolSpec(  # L2 高危工具，生产环境硬禁
        "delete_all_logs", 2,  # 名称与风险等级
        {"directory": str},  # 参数类型约束
        ("directory",),  # directory 必填
        lambda directory: f"已删除 {directory}",  # 模拟执行
    ),
}

DENIED_TOOLS: set[str] = {"delete_all_logs"}  # 生产硬禁名单，优先级最高
PARAM_ALIASES: dict[str, str] = {  # 仅收录语义等价的同义参数名
    "reportId": "report_id",  # 驼峰写法归一
    "reportID": "report_id",  # 全大写缩写归一
    "rows": "max_rows",  # 简写归一
}
MAX_SAME_CALLS = 2  # 同一调用指纹允许的最大次数


@dataclass
class GuardResult:
    """一次工具调用的判定结果。"""

    status: str  # executed / rejected / pending_confirm / circuit_broken
    layer: str  # 命中的防线层，便于审计定位
    detail: str  # 人类可读的说明或拒绝原因
    output: Any = None  # 执行成功时的返回值


class ToolGuard:
    """四层防护执行器：Schema 校验、暴露收敛、权限白名单、运行时熔断。"""

    def __init__(self, role: str = "normal") -> None:
        """初始化执行器，按角色确定可触达的最高风险等级。"""

        self.role = role  # 主体角色，决定可见工具范围
        self.max_level = 2 if role == "admin" else 0  # 普通用户只见 L0，管理员可触达 L2
        self.call_counts: dict[str, int] = {}  # 调用指纹计数器

    def visible_tools(self) -> list[str]:
        """返回当前主体可见的工具列表，实现第二层暴露收敛。"""

        return [name for name, spec in REGISTRY.items()  # 遍历注册表
                if spec.level <= self.max_level and name not in DENIED_TOOLS]  # 等级达标且不在硬禁名单

    def call(self, name: str, raw_args: dict[str, Any], confirmed: bool = False) -> GuardResult:
        """执行一次工具调用，按四层顺序逐级拦截。"""

        spec = REGISTRY.get(name)  # 第三层：查白名单注册表
        if spec is None:  # 未登记的工具名
            return GuardResult("rejected", "L3-allowlist", f"工具未在白名单中: {name}")  # 拒绝幻觉工具名
        if name in DENIED_TOOLS:  # 命中硬禁名单
            return GuardResult("rejected", "L3-denylist", f"工具被生产环境硬禁: {name}")  # 优先于一切规则
        if spec.level > self.max_level:  # 超出主体权限等级
            return GuardResult("rejected", "L3-permission", f"角色 {self.role} 无权调用 L{spec.level} 工具")  # 拒绝越权
        if spec.level == 2 and not confirmed:  # 高危工具且尚未确认
            preview = f"即将执行 {name}({json.dumps(raw_args, ensure_ascii=False)})，不可逆"  # 生成操作预览
            return GuardResult("pending_confirm", "L4-confirm", preview)  # 挂起等待人工确认
        args = {PARAM_ALIASES.get(key, key): value for key, value in raw_args.items()}  # 第一层：别名归一化
        missing = [key for key in spec.required if key not in args]  # 第一层：检查必填项
        if missing:  # 缺必填参数即拒绝
            return GuardResult("rejected", "L1-schema", f"缺少必填参数: {missing}")  # 返回可修复信息
        for key, value in args.items():  # 第一层：逐个参数做白名单与类型校验
            if key not in spec.schema:  # 出现未定义字段
                return GuardResult("rejected", "L1-schema", f"未定义的参数名: {key}")  # 拒绝而非静默忽略
            if not isinstance(value, spec.schema[key]):  # 类型不匹配
                expected = spec.schema[key].__name__  # 期望类型名
                return GuardResult("rejected", "L1-schema", f"参数 {key} 期望 {expected}，实际 {type(value).__name__}")  # 报错要具体
        fingerprint = hashlib.sha256(  # 第四层：生成调用指纹
            f"{name}:{json.dumps(args, sort_keys=True, ensure_ascii=False)}".encode()  # 工具名 + 稳定序列化参数
        ).hexdigest()  # 转成定长摘要
        self.call_counts[fingerprint] = self.call_counts.get(fingerprint, 0) + 1  # 累加同指纹次数
        if self.call_counts[fingerprint] > MAX_SAME_CALLS:  # 超过阈值即熔断
            return GuardResult("circuit_broken", "L4-breaker", f"检测到重复调用 {name}，已熔断")  # 阻止原地重试
        return GuardResult("executed", "pass", "通过四层校验", spec.handler(**args))  # 全部通过后执行


def demo() -> None:
    """跑通五个典型场景，输出每一层的拦截效果。"""

    guard = ToolGuard(role="normal")  # 普通用户会话
    print("普通用户可见工具:", guard.visible_tools())  # 高危工具不在可见列表
    scenarios = [  # 每个元组为 说明 + 工具名 + 参数
        ("正常查询", "query_report", {"report_id": "RPT-000123", "max_rows": 20}),  # 应放行
        ("参数名幻觉", "query_report", {"reportId": "RPT-000123"}),  # 归一化后放行
        ("参数类型错误", "query_report", {"report_id": "RPT-000123", "max_rows": "十"}),  # 第一层拦截
        ("高危删除", "delete_all_logs", {"directory": "/var/log"}),  # 硬禁名单拦截
        ("普通用户调高危", "purge_cache", {"scope": "all"}),  # 权限等级拦截
    ]
    for title, name, args in scenarios:  # 依次执行场景
        result = guard.call(name, args)  # 走完整四层
        print(f"[{title}] {result.status} | {result.layer} | {result.detail}")  # 输出判定
    admin = ToolGuard(role="admin")  # 管理员会话，可触发高危确认
    print("管理员可见工具:", admin.visible_tools())  # 硬禁工具仍不可见
    pending = admin.call("purge_cache", {"scope": "all"})  # 未确认时应挂起
    print(f"[管理员高危] {pending.status} | {pending.detail}")  # 输出 pending_confirm
    done = admin.call("purge_cache", {"scope": "all"}, confirmed=True)  # 确认后执行
    print(f"[确认后执行] {done.status} | {done.output}")  # 输出执行结果
    for index in range(1, 4):  # 同一参数连续调用三次
        repeated = admin.call("query_report", {"report_id": "RPT-000123"})  # 同指纹调用
        print(f"[重复调用第 {index} 次] {repeated.status} | {repeated.detail}")  # 第三次应熔断


if __name__ == "__main__":  # 作为脚本直接运行时
    demo()  # 执行演示
```

## 4. 运行结果怎么读（Real Output）

Python 3.12 实测输出，与上面代码逐字对应：

```text
普通用户可见工具: ['query_report']
[正常查询] executed | pass | 通过四层校验
[参数名幻觉] executed | pass | 通过四层校验
[参数类型错误] rejected | L1-schema | 参数 max_rows 期望 int，实际 str
[高危删除] rejected | L3-denylist | 工具被生产环境硬禁: delete_all_logs
[普通用户调高危] rejected | L3-permission | 角色 normal 无权调用 L2 工具
管理员可见工具: ['query_report', 'purge_cache']
[管理员高危] pending_confirm | 即将执行 purge_cache({"scope": "all"})，不可逆
[确认后执行] executed | 已清理缓存 scope=all
[重复调用第 1 次] executed | 通过四层校验
[重复调用第 2 次] executed | 通过四层校验
[重复调用第 3 次] circuit_broken | 检测到重复调用 query_report，已熔断
```

三条信息值得单独拎出来：

**第一，`visible_tools()` 的返回值就是候选集的上限。** 普通用户拿到的是 `['query_report']`，管理员才是 `['query_report', 'purge_cache']`，而 `delete_all_logs` 对谁都不出现。这就是「高危工具从来没进过候选集」的代码形态——不是靠模型自觉不选，是它压根没得选。

**第二，`pending_confirm` 是状态，不是 exception（异常）。** 输出里 `[管理员高危] pending_confirm` 那一行之后必须有回执：把用户点「确认」的结果写回 `confirmed=True` 再调一次。漏了这一步，高危操作会永远停在挂起态，「加了二次确认但业务跑不通」十有八九是这个原因。

**第三，指纹用的不是原始参数。** `json.dumps(..., sort_keys=True)` 保证 `{"a":1,"b":2}` 和 `{"b":2,"a":1}` 命中同一个指纹；少这一个参数，RAC（Repeated API Calls，重复调用）就检测不出来，熔断阈值形同虚设。

## 5. 接进现有 Agent 的三个接入点（Integration）

这段代码本身不调用任何模型，接进现有 runtime 只需要守住三个点：

1. **候选集来源**：把 `guard.visible_tools()` 的结果转成模型侧的 `tools` 数组，而不是把 `REGISTRY` 全量下发。这一行决定了第二层防线是否生效。
2. **调用入口唯一**：所有 `tool_call` 必须经过 `guard.call()`，业务代码禁止直接调 `handler`。只要留了一条后门，前面四层都白做。
3. **确认走状态机**：`pending_confirm` 落进会话状态，回执里带上本次调用的指纹，确认时比对指纹一致才执行——否则用户确认的是 A 操作，实际执行的是被篡改过的 B 操作。

第三点常被忽略。确认框和真正执行之间如果隔了一次模型调用，参数就有被重写的窗口。

## 6. 边界：这层拦不住什么（Boundaries）

必须说清三件事，否则这段代码会被当成万灵药：

- **拦不住业务逻辑错。** 参数合法、权限合规、用户也确认了，结果仍然是错误的决策——那是业务校验和可观测性的活。防护层只保证「调用是按规则发生的」。
- **拦不住用户本人要求的危险操作。** 用户明确说「清空所有日志」，硬禁名单会拦下，但这是策略选择而非安全结论；真正需要的是把不可逆操作改成可恢复操作（软删除 + 保留期）。
- **拦不住提示注入。** 攻击者把恶意指令藏在合法任务背后时，参数看起来完全正常。这类要靠在执行期逐步收窄权限来防，AgenTRIM 走的就是这条路：离线重建工具接口，运行时按步动态过滤（[arXiv:2601.12449](https://doi.org/10.48550/arXiv.2601.12449)）。

另一个工程细节：`call_counts` 是进程内字典，多实例部署时会各算各的。生产环境要换成 Redis 计数器，并且带 TTL（Time To Live，过期时间），否则重启即清零、水平扩容即失效。

底层判据没有变：模型侧的错误率是统计性的，ToolScan 在 10 类环境、30 多个任务上证实这些错误会稳定复现（[arXiv:2411.13547](https://doi.org/10.48550/arXiv.2411.13547)）；暴露面收窄带来的收益也是可复算的，100 个工具全暴露时成功率 0.83、平均 1.25 次错误调用，只暴露因果必需工具时是 0.99 与 0.01（[arXiv:2606.06284](https://doi.org/10.48550/arXiv.2606.06284)）。

## 7. 参考资料（References）

- Kokane 等. *ToolScan: A Benchmark for Characterizing LLM Tool Calling Errors*. ICLR 2025 Workshop. DOI: [10.48550/arXiv.2411.13547](https://doi.org/10.48550/arXiv.2411.13547)
- *ToolChoiceConfusion: Causal Minimal Tool Filtering for Agent Tool Selection*（CMTF）. arXiv, 2026. DOI: [10.48550/arXiv.2606.06284](https://doi.org/10.48550/arXiv.2606.06284)
- *AgenTRIM: Runtime Least-Privilege Enforcement for LLM Agents*. arXiv, 2026. DOI: [10.48550/arXiv.2601.12449](https://doi.org/10.48550/arXiv.2601.12449)
- 全国网络安全标准化技术委员会. 《网络安全标准实践指南——智能体交互安全要求（征求意见稿 v0.23）》, 8.2 c / 8.2 d / 8.2 g 条. [原文下载](https://www.tc260.org.cn/sysFile/downloadFile/fac60a9027c041aba5b6f18930cde11b)
- OWASP. *LLM06:2025 Excessive Agency*. [条目原文](https://genai.owasp.org/llmrisk/llm062025-excessive-agency/)

工具数超过 5 个、且存在至少一个不可逆操作时，这段代码值得直接抄走；只接两三个只读工具的轻量 Agent 用不上第四层，把参数校验那 30 行留下就够了。

本专栏《AI Agent 工具》已发 7 篇，从工具选型、Skill 路由一路讲到误调用治理与权限收敛，每篇都配可直接运行的代码，每周更新一篇。
