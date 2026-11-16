"""规则体检脚本：统计规则目录的体积、重复条目与否定式条目占比。

使用示例:
    python rule_audit.py .trae/rules

参数:
    命令行第 1 个参数为待体检目录，缺省为 .trae/rules
返回:
    无返回值，结果直接打印到标准输出
"""
import os
import re
import sys
from collections import Counter

# 判定「否定式规则」的关键词：这类句子只在违规时生效，却全程占用常驻 token
NEGATIVE_WORDS = ("禁止", "不要", "不许", "不得", "不准", "不能", "勿", "严禁")


def normalize(line):
    """归一化一行规则用于查重：去掉列表符号、序号、标点与强调符。

    参数:
        line: str，原始规则行文本
    返回:
        str，归一化后的文本，可直接用于相等比较查重
    """
    text = re.sub(r"^[\s\-\*\d\.\)、]+", "", line)                 # 去掉列表符号与序号
    text = re.sub(r"[，。；：、（）()\[\]【】\"'`*#]", "", text)     # 去掉标点与强调符
    return text.strip()                                            # 两端空白一并去掉


def main():
    """遍历目录下所有 .md 规则，输出体积、重复条目与否定式占比。

    参数:
        无（目录从 sys.argv[1] 取，缺省为 .trae/rules）
    返回:
        None，统计结果直接打印到标准输出
    """
    root = sys.argv[1] if len(sys.argv) > 1 else ".trae/rules"      # 默认体检 .trae/rules
    files, items, total = [], [], 0                                 # 汇总容器
    for name in sorted(os.listdir(root)):                           # 固定顺序，保证结果可复现
        if not name.endswith(".md"):                                # 只统计 markdown 规则
            continue
        text = open(os.path.join(root, name), encoding="utf-8").read()
        lines = [l.strip() for l in text.splitlines() if l.strip()]  # 丢弃空行
        total += len(text)                                          # 累计字符数
        files.append((name, len(text), len(lines)))                 # 逐文件体积
        items += [(name, l) for l in lines]                         # 逐条规则入池

    normed = Counter(normalize(l) for _, l in items if len(normalize(l)) > 8)
    dups = {k: v for k, v in normed.items() if v > 1}               # 归一化后完全一致才计重复
    dup_chars = sum(len(k) * v for k, v in dups.items())            # 重复占用字符（近似）
    neg = [l for _, l in items if any(w in l for w in NEGATIVE_WORDS)]
    neg_chars = sum(len(l) for l in neg)                            # 否定式占用字符

    print(f"目录: {root}")
    for name, chars, n in files:
        print(f"{name:34s}{chars:8d}{n:6d}")                        # 逐文件明细
    print(f"{'合计':34s}{total:8d}{len(items):6d}")
    print(f"\n重复组数 {len(dups)} / 占用 {dup_chars} 字符 ({dup_chars/total:.1%})")
    print(f"否定式 {len(neg)} 条 / 占用 {neg_chars} 字符 ({neg_chars/total:.1%})")
    print(f"常驻 token 粗估: 约 {round(total/1.6)}（1.6 字符 ≈ 1 token）")


if __name__ == "__main__":
    main()
