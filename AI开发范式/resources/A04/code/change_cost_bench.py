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
