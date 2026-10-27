---
platform: 腾讯云开发者社区
title: 三种代码组织方式的改动成本实测：AI 时代"改得动"为什么比"写得快"更重要
summary: 把"不可替代"拆成可测量的改动成本：同一段会员折扣业务、同一个需求变更，复制粘贴、一次抽象到底、表驱动三种写法实测改动行 18/8/4，必读行 27/20/9。抽象让改动点从 3 涨到 4，却把认知成本压了下来，文中代码可完整复算。
tags: [软件工程, 代码重构, 可维护性, Python, AI 编程]
limits: 标题 100 字 / 正文长度未实测
source: A04-AI时代什么样的程序员不会被淘汰：三种代码组织方式的改动成本实测.md
---

# 三种代码组织方式的改动成本实测：AI 时代"改得动"为什么比"写得快"更重要

> **全文摘要**：被淘汰的不是"不会写代码"的人，而是让改动成本失控的人。同一段会员折扣逻辑，我用三种组织方式各写一遍，再施加同一个需求变更，实测改动行分别为 18、8、4，必读行 27、20、9。三个数字都能用第 5 节代码复算。

## 目录

一、结论先行
二、为什么"会写代码"不再是护城河
三、我把"不被淘汰"变成了一个可复现的数字
四、三种写法，同一段业务
五、完整可运行代码
六、实测结果
七、反直觉：抽象让改动点变多了
八、症状 → 原因 → 解法
九、什么时候该复制、该抽象、该建表

## 1. 结论先行（Conclusion First）

先说结论：技术社区里关于"AI 是否替代程序员"的讨论，多数停在情绪层面。本文换一个可验证的角度——把"不可替代"拆成改动成本，用同一段业务、同一个需求变更，量化三种代码组织方式的代价。**AI 降低的是写出代码的边际成本，抬高的是改动代码的边际成本**，当生成变得廉价，稀缺性就从"能写"转移到"改得动"。

我把"不被淘汰"操作化（operationalize）成一个可测量的量：同一个需求变更，落到三种代码组织方式上，要改多少行、动手前要读懂多少行。实测结果是复制粘贴 18 行 / 27 行，一次抽象到底 8 行 / 20 行，表驱动 4 行 / 9 行，差距最大的一项接近 3 倍。

这不是"抽象优于复制"的老生常谈。下文会看到一个反直觉的结果：抽象之后，改动点反而从 3 个涨到 4 个。

## 2. 为什么"会写代码"不再是护城河（Why Writing Code Is No Longer a Moat）

2026 年 8 月，GitClear 发布了一份覆盖四年代码变更数据的报告《The Maintainability Gap》。几个关键数字：

- 被"移动"的代码（重构的主要动作）占变更行的比例，从 2022 年的 21% 掉到 2023 年的 13%，2026 年前八个月只剩 3.8%
- 块级重复（连续 5 行以上重复）从每百万变更行 40.3 涨到 73.0，涨幅 81%
- 重构型代码移动比 2022 年下降 70%，长期遗留维护下降 74%，跨文件函数调用下降 35%

同期，Google Cloud 的 DORA 2024 报告给出另一组数字：AI 采纳度每提高 25%，交付吞吐量估计下降 1.5%，交付稳定性下降 7.2%，花在有价值工作上的时间下降 2.6%。报告的解释是"AI 让单次生成量变大，批次变大，评审变慢，系统更容易不稳定"。

两组数据拼起来是一件事：**代码产出在涨，可维护性（maintainability）在跌**。在《AI真的会替代程序员吗》中我拆过 55.8% 提速与 19% 变慢的八组数据，那里讲的是"写"的效率；这篇讲的是"改"的代价。

> 打个比方 🎭：AI 把砖价打到了地板，谁都能一夜砌起一面墙。但房子能不能住，取决于你改一扇窗要不要拆承重墙——这件事 AI 帮不了你，因为图纸是你画的。

维护成本的分量，Glass 在《Facts and Fallacies of Software Engineering》第 41 条给过一个被反复引用的口径：维护通常吃掉软件总成本的 40%–80%，均值 60%。代码交付那天，账单才刚开始。

参考资料：
- [The Maintainability Gap: 2026 AI Code Quality Research -- GitClear](https://www.gitclear.com/the_ai_code_quality_maintainability_gap)
- [2024 DORA Accelerate State of DevOps Report -- DORA](https://dora.dev/research/2024/dora-report/)
- [Facts and Fallacies of Software Engineering 讲义（第 41 条） -- bfwa.com](http://bfwa.com/cs428/2021f/cs428-211108-factsfallacies03.pdf)

## 3. 我把"不被淘汰"变成了一个可复现的数字（Operationalizing the Question）

"不会被淘汰"无法直接测量。要让它可验证，只能找代理指标（proxy metric）。我选的代理是**改动成本**，依据是 ISO/IEC 25010 对可维护性子特性"模块化（modularity）"的定义：系统由离散组件构成，使得**改动其中一个组件对其余组件的影响最小**。这句话把"好架构"翻译成了一个可计数的东西——影响范围。

三个指标，全部按非空行计：

| 指标 | 定义 | 回答的问题 |
| --- | --- | --- |
| 改动点 | 发生变化的顶层定义个数（函数 / 类 / 模块级常量） | 这次变更碰了几处？ |
| 改动行 | 每个变更定义内部，新增 + 删除的行数 | 真正敲了多少行？ |
| 必读行 | 变更定义 + 其基类 + 读取变更名字的其他函数 | 动手前必须读懂多少行？ |

"必读行"是关键。改动成本的大头不是敲键盘，是**理解上下文**——你得先知道这个函数被谁依赖、它的基类承诺了什么。一个 3 行的改动，如果需要读懂 40 行才能下手，真实成本是 43 行。

为保证可复算，口径写死在这里：只数非空行；"改动行"用 difflib 对每个定义单独做行级差异（diff），避免整模块对齐漂移；"读取"指抽象语法树（AST）中出现该名字且上下文为 Load，含调用但不限于调用。

局限也说清楚：这是代理指标，不是"会不会失业"的直接测量。它衡量"面对变更时的局部性"，不衡量需求判断、沟通、系统设计这些同样重要的能力。但局部性能被任何人用同一份代码复算——这一点比任何形容词都有说服力。

参考资料：
- [ISO/IEC 25010:2011 产品质模型（modularity 定义见 4.2.7.1.1） -- ISO](https://www.iso.org/obp/ui/en/#!iso:std:35733:en)

## 4. 三种写法，同一段业务（Three Implementations）

业务足够小，差异才只来自组织方式，而不是业务复杂度：

- 会员折扣：SILVER 95 折、GOLD 9 折，其他不打折
- 满减：订单满 500 减 40
- 折后金额四舍五入到分

需求变更（工单里最常见的那种）：

1. 新增 PLATINUM 等级，85 折
2. 新增满 1000 减 120

三种组织方式：

| 代号 | 写法 | 一次变更要动哪里 |
| --- | --- | --- |
| A | 复制粘贴：购物车 / 订单 / 退款各写一份同样的规则 | 三份都要改 |
| B | 一次抽象到底：抽象基类 + 策略类 + 工厂 + 策略组合 | 新增类、改注册表、改入口函数 |
| C | 表驱动：规则写成字典和列表，入口函数只有一份 | 改两个常量 |

注意 A 不是稻草人。它就是多数项目里真实存在的形态：同一个规则因为三个入口被复制了三遍，每份都"能跑、能过评审"。

## 5. 完整可运行代码（Runnable Code）

下面这段代码复制粘贴即可运行，无第三方依赖，Python 3.8 以上均可。它把 A / B / C 三种实现的前后版本都写成字符串，用抽象语法树拆成顶层定义、逐定义做差异、统计三个指标，最后用 4 个样本交叉验证三种实现行为一致。

```python
"""改动成本基准：同一个需求变更，在三种代码组织方式下的代价对比。

指标（按非空行计）：
    改动点  发生变化的顶层定义个数（函数 / 类 / 模块级常量）
    改动行  每个变更定义内部，新增 + 删除的行数
    必读行  变更定义 + 其基类 + 读取变更名字的其他函数的行数
"""

import ast
import difflib
import textwrap

# ---------------- 组织方式 A：复制粘贴，同一套规则写三遍 ----------------
A_BEFORE = textwrap.dedent('''
    def payable_cart(total, member):
        rate = 1.0
        if member == "SILVER": rate = 0.95
        elif member == "GOLD": rate = 0.90
        amount = total * rate
        if total >= 500: amount -= 40
        return round(amount, 2)

    def payable_order(total, member):
        rate = 1.0
        if member == "SILVER": rate = 0.95
        elif member == "GOLD": rate = 0.90
        amount = total * rate
        if total >= 500: amount -= 40
        return round(amount, 2)

    def payable_refund(total, member):
        rate = 1.0
        if member == "SILVER": rate = 0.95
        elif member == "GOLD": rate = 0.90
        amount = total * rate
        if total >= 500: amount -= 40
        return round(amount, 2)
''')

A_AFTER = textwrap.dedent('''
    def payable_cart(total, member):
        rate = 1.0
        if member == "PLATINUM": rate = 0.85
        elif member == "SILVER": rate = 0.95
        elif member == "GOLD": rate = 0.90
        amount = total * rate
        if total >= 1000: amount -= 120
        elif total >= 500: amount -= 40
        return round(amount, 2)

    def payable_order(total, member):
        rate = 1.0
        if member == "PLATINUM": rate = 0.85
        elif member == "SILVER": rate = 0.95
        elif member == "GOLD": rate = 0.90
        amount = total * rate
        if total >= 1000: amount -= 120
        elif total >= 500: amount -= 40
        return round(amount, 2)

    def payable_refund(total, member):
        rate = 1.0
        if member == "PLATINUM": rate = 0.85
        elif member == "SILVER": rate = 0.95
        elif member == "GOLD": rate = 0.90
        amount = total * rate
        if total >= 1000: amount -= 120
        elif total >= 500: amount -= 40
        return round(amount, 2)
''')

# ---------------- 组织方式 B：一次抽象到底，策略类 + 工厂 ----------------
B_BEFORE = textwrap.dedent('''
    from abc import ABC, abstractmethod

    class MemberRule(ABC):
        @abstractmethod
        def apply(self, amount):
            ...

    class NoRule(MemberRule):
        def apply(self, amount): return amount

    class SilverRule(MemberRule):
        def apply(self, amount): return amount * 0.95

    class GoldRule(MemberRule):
        def apply(self, amount): return amount * 0.90

    class MemberRuleFactory:
        registry = {"SILVER": SilverRule, "GOLD": GoldRule}

        @classmethod
        def get(cls, name): return cls.registry.get(name, NoRule)()

    class RebatePolicy(ABC):
        @abstractmethod
        def cut(self, total):
            ...

    class HighRebate(RebatePolicy):
        def cut(self, total): return 40 if total >= 500 else 0

    def payable(total, member):
        amount = MemberRuleFactory.get(member).apply(total)
        amount -= HighRebate().cut(total)
        return round(amount, 2)
''')

B_AFTER = textwrap.dedent('''
    from abc import ABC, abstractmethod

    class MemberRule(ABC):
        @abstractmethod
        def apply(self, amount):
            ...

    class NoRule(MemberRule):
        def apply(self, amount): return amount

    class SilverRule(MemberRule):
        def apply(self, amount): return amount * 0.95

    class GoldRule(MemberRule):
        def apply(self, amount): return amount * 0.90

    class PlatinumRule(MemberRule):
        def apply(self, amount): return amount * 0.85

    class MemberRuleFactory:
        registry = {"SILVER": SilverRule, "GOLD": GoldRule, "PLATINUM": PlatinumRule}

        @classmethod
        def get(cls, name): return cls.registry.get(name, NoRule)()

    class RebatePolicy(ABC):
        @abstractmethod
        def cut(self, total):
            ...

    class HighRebate(RebatePolicy):
        def cut(self, total): return 40 if total >= 500 else 0

    class TopRebate(RebatePolicy):
        def cut(self, total): return 120 if total >= 1000 else 0

    def payable(total, member):
        amount = MemberRuleFactory.get(member).apply(total)
        amount -= max(HighRebate().cut(total), TopRebate().cut(total))
        return round(amount, 2)
''')

# ---------------- 组织方式 C：表驱动，规则写成数据 ----------------
C_BEFORE = textwrap.dedent('''
    MEMBER_RATE = {"SILVER": 0.95, "GOLD": 0.90}
    REBATE = [(500, 40)]

    def payable(total, member):
        amount = total * MEMBER_RATE.get(member, 1.0)
        for threshold, cut in REBATE:
            if total >= threshold:
                amount -= cut
                break
        return round(amount, 2)
''')

C_AFTER = textwrap.dedent('''
    MEMBER_RATE = {"PLATINUM": 0.85, "SILVER": 0.95, "GOLD": 0.90}
    REBATE = [(1000, 120), (500, 40)]

    def payable(total, member):
        amount = total * MEMBER_RATE.get(member, 1.0)
        for threshold, cut in REBATE:
            if total >= threshold:
                amount -= cut
                break
        return round(amount, 2)
''')


def defs(source):
    """把模块拆成顶层定义：名字 -> 源码。"""
    result = {}
    for node in ast.parse(source).body:
        if isinstance(node, (ast.FunctionDef, ast.ClassDef)):
            result[node.name] = ast.get_source_segment(source, node) or ""
        elif isinstance(node, ast.Assign):
            for target in node.targets:
                if isinstance(target, ast.Name):
                    result[target.id] = ast.get_source_segment(source, node) or ""
    return result


def bases(source):
    """类名 -> 直接基类名集合。"""
    return {node.name: {b.id for b in node.bases if isinstance(b, ast.Name)}
            for node in ast.parse(source).body if isinstance(node, ast.ClassDef)}


def readers(source, names):
    """函数体内读取（含调用）names 的顶层函数名。"""
    found = set()
    for node in ast.parse(source).body:
        if isinstance(node, ast.FunctionDef):
            used = {x.id for x in ast.walk(node)
                    if isinstance(x, ast.Name) and isinstance(x.ctx, ast.Load)}
            if used & names:
                found.add(node.name)
    return found


def diff_lines(old_text, new_text):
    """单个定义内部的新增 + 删除行数。"""
    diff = difflib.unified_diff(old_text.splitlines(), new_text.splitlines(),
                                lineterm="", n=0)
    return sum(1 for line in diff
               if line[:1] in "+-"
               and not line.startswith(("+++", "---"))
               and line[1:].strip())


def non_blank(text):
    """非空行数。"""
    return sum(1 for line in text.splitlines() if line.strip())


def measure(name, before, after):
    """计算改动点、改动行、必读行。"""
    old, new = defs(before), defs(after)
    touched = {k for k in old if new.get(k) != old[k]} | (set(new) - set(old))
    lines = sum(diff_lines(old.get(k, ""), new.get(k, "")) for k in touched)
    parents = bases(before)
    parents.update(bases(after))
    extra = {p for k in touched for p in parents.get(k, set())}
    extra |= readers(before, touched) | readers(after, touched)
    extra -= touched
    read = sum(non_blank(new.get(k, old.get(k, ""))) for k in touched | extra)
    return name, len(touched), lines, read


def outputs(source, entry):
    """执行源码，取入口函数在四个样本上的结果。"""
    namespace = {}
    exec(source, namespace)
    samples = [(120, "NONE"), (260, "SILVER"), (560, "GOLD"), (1200, "PLATINUM")]
    return [namespace[entry](total, member) for total, member in samples]


CASES = [("A 复制粘贴", A_BEFORE, A_AFTER, "payable_cart"),
         ("B 一次抽象到底", B_BEFORE, B_AFTER, "payable"),
         ("C 表驱动", C_BEFORE, C_AFTER, "payable")]

print(f"{'组织方式':<14}{'改动点':>6}{'改动行':>7}{'必读行':>7}")
for case in CASES:                                     # 逐个组织方式输出三项指标
    _, points, lines, read = measure(*case[:3])        # 一次性拿到三项指标
    print(f"{case[0]:<14}{points:>8}{lines:>8}{read:>8}")

baseline = outputs(A_BEFORE, "payable_cart")
upgraded = outputs(C_AFTER, "payable")
for label, source, entry in [("A after", A_AFTER, "payable_cart"),
                             ("B before", B_BEFORE, "payable"),
                             ("B after", B_AFTER, "payable"),
                             ("C before", C_BEFORE, "payable")]:
    got = outputs(source, entry)
    assert got in (baseline, upgraded), f"{label} 行为不一致: {got}"

copies = [outputs(A_BEFORE, f) for f in ("payable_cart", "payable_order", "payable_refund")]
assert copies[0] == copies[1] == copies[2], "A 的三份实现本身就不一致"
print("六份样本行为一致，A 的三份副本逐项相等")
```

输出：

```text
组织方式             改动点    改动行    必读行
A 复制粘贴               3      18      27
B 一次抽象到底             4       8      20
C 表驱动                2       4       9
六份样本行为一致，A 的三份副本逐项相等
```

最后一行断言不能省。如果三份实现的输出不一致，"改动成本"的对比就失去意义——那只是在比三个不同需求的实现难度。这也是所有基准测试（benchmark）里最容易被跳过的一步。

## 6. 实测结果（Measured Results）

| 组织方式 | 改动点 | 改动行 | 必读行 |
| --- | --- | --- | --- |
| A 复制粘贴 | 3 | 18 | 27 |
| B 一次抽象到底 | 4 | 8 | 20 |
| C 表驱动 | 2 | 4 | 9 |

每个数字都能手算复核：

- **A 的 18 行**：三个函数各改一次，单函数内是 2 删 + 4 增（新增 PLATINUM 分支、新增满 1000 档），3 × 6 = 18；必读行是三个函数变更后的非空行数 3 × 9 = 27。
- **B 的 8 行**：新增 `PlatinumRule` 2 行、新增 `TopRebate` 2 行、工厂 `registry` 一行替换 2 行、`payable` 的满减一行替换 2 行，合计 8；必读行由四个变更定义（2 + 4 + 2 + 4）加两个基类（`MemberRule` 4 行、`RebatePolicy` 4 行）构成，等于 20。
- **C 的 4 行**：`MEMBER_RATE` 与 `REBATE` 各一行替换（1 删 1 增），合计 4；必读行是两个常量各 1 行加上 `payable` 的 7 行，等于 9。

三份实现的最终行为完全相同：`(120, "NONE")` 得 120.0，`(260, "SILVER")` 得 247.0，`(560, "GOLD")` 得 464.0，`(1200, "PLATINUM")` 得 900.0。

差距最大的是必读行：27 对 9，正好 3 倍。改动行是 18 对 4，4.5 倍。改动点则是 3 / 4 / 2，没有单调关系——这正是下一节要解释的地方。

## 7. 反直觉：抽象让改动点变多了（The Counterintuitive Part）

B 的改动点是 4，比 A 的 3 还多。如果只看这一列，结论会变成"抽象有害"。

这是必须解释的取舍：**抽象不减少改动点，它把改动收敛到局部**。A 的每一处改动都包含完整业务规则，你必须把规则读三遍、改三遍、验三遍；B 的四处里，两处是纯新增的空实现（各 2 行），两处是一行替换。同样是"碰 4 处"，认知负担完全不同。

理由在这里：改动点带来的是**切换成本**（在文件之间跳几次），改动行和必读行带来的是**认知成本**（大脑里要同时装下多少上下文）。切换成本可以并行、可以被打断，认知成本不行。所以本文的判断是局部性优先于改动点数量，而不是相反。

但这个判断有边界。如果规则条数很少、一年改一次，B 的四层结构（基类、策略、工厂、组合）本身就是需要读懂的成本——你为了省 10 行改动，先付出了 60 行理解。这时 A 反而是对的。

C 在三个维度上都赢了，原因是它把"规则是什么"和"规则怎么用"拆开了：规则退化成数据，入口函数负责遍历数据。新增一档折扣，等于往字典里加一个键值对。

## 8. 症状 → 原因 → 解法（Symptom-Cause-Fix）

| 症状 | 原因 | 解法 |
| --- | --- | --- |
| 改一个折扣，三个地方要同步改 | 规则被复制进多个入口函数 | 先把规则收进一个函数或一张常量表 |
| 新增一个等级，要建类、还要登记注册表 | 抽象粒度比规则粒度细 | 规则种类少于 10 条时用表驱动，不用类 |
| 新人不敢动这段代码 | 入口函数太长，或依赖关系不显式 | 缩短入口函数，把规则外置为数据 |
| 评审只看懂改动，看不出影响范围 | 缺少"谁依赖我"的显式结构 | 用注册表或常量表让依赖变成可见数据 |
| 每次变更都在猜有没有漏改 | 重复代码没有统一收敛点 | 先收敛，再决定形态，不要反过来 |

这张表的用法是反查：先描述症状，再找原因，最后看解法。对症下药比背设计模式（design pattern）有效。

## 9. 什么时候该复制、该抽象、该建表（Which One to Choose）

先泼一盆冷水：重复不总是坏的。2026 年 ICSE 的 TechDebt 会议收录了一篇民族志研究（ethnographic study），作者向 Linux 内核的 AMDGPU 和 IIO 子系统真实提交去重补丁，观察维护者如何决策。结论是维护者会拒绝一部分"技术上正确但没必要"的去重——跨模块合并会引入集成耦合，可读性与评审成本可能高于重复本身的代价。

所以选择形态时看这四个条件：

| 条件 | 建议 |
| --- | --- |
| 规则条数 ≤ 5、一年改一次 | 复制粘贴不是罪，A 的可读性最高 |
| 规则条数 6–20、每季度都有新增 | 表驱动，C |
| 不同等级走的是不同算法，不只是系数不同 | 策略类，B |
| 同一份逻辑出现在 3 个及以上入口 | 先收敛到一处，再决定形态 |

三条可迁移的判据：

1. **先数入口，再选形态**。规则只出现在一个入口，怎么写都行；出现在三个入口，形态已经被约束了，先收敛是唯一解。
2. **用必读行做提交前的自查**。按下提交前问一句：别人要读懂多少行，才能确认我这个改动是对的？
3. **让规则变成数据，而不是让数据变成类**。系数、阈值、档位天然是表；只有算法本身不同，才值得动用类。

回到标题。AI 时代不会淘汰"暂时写得少"的人，会淘汰"每加一档折扣都要动三处、且自己说不清动了哪三处"的人。这个能力不依赖你熟悉哪种语言，也不依赖模型有多强——它依赖你把变化关在一个可以被数清楚的格子里。

如果一段逻辑只在一年改一次的地方、且只有 3 条规则，复制粘贴反而更划算，没必要为了"架构感"提前抽象；如果它每周都在加档位，表驱动几乎总是最优解。

建议收藏这篇：第 8 节那张"症状 → 原因 → 解法"表，下次评审卡住时可以直接拿去对；第 5 节代码可以原样跑一遍，验证你手上的项目落在哪个量级。想继续看同类文章，可以关注我，专栏《AI开发范式》收录 AI 参与研发之后的工程实践与可复现的数据实验，每月更新两到三篇。
