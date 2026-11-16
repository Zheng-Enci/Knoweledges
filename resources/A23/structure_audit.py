"""目录体检脚本：量化项目结构的分散度，并自带两套对照布局用于复算。

使用示例:
    python structure_audit.py ../../AI开发范式        体检任意目录，输出结构指标
    python structure_audit.py --demo                  生成两套 16 文件布局并对比
    python structure_audit.py --demo --key order      指定按哪个功能名统计分散度

参数:
    命令行第 1 个参数为待体检目录；传 --demo 时改用内置样本
返回:
    无返回值，结果直接打印到标准输出
"""
import os
import re
import sys
import tempfile

IGNORE = {".git", "node_modules", "dist", "__pycache__", ".idea", ".venv"}   # 体检时跳过的目录
IMPORT_RE = re.compile(r"^\s*(?:from|import)\s+([\w\.]+)")                   # 抓取 import 的模块路径


def walk(root):
    """遍历目录，返回所有源码文件与其所在目录的相对路径。

    参数:
        root: str，待遍历的目录
    返回:
        list[tuple[str, str]]，元素为（文件相对路径，文件所在目录相对路径）
    """
    result = []                                                              # 收集（文件，目录）对
    for current, dirs, names in os.walk(root):                               # 逐层向下遍历
        dirs[:] = [d for d in dirs if d not in IGNORE]                       # 原地过滤忽略目录
        for name in sorted(names):                                           # 固定顺序，保证可复现
            if not name.endswith((".py", ".js", ".ts", ".jsx", ".tsx")):      # 只看源码文件
                continue                                                     # 非源码直接跳过
            full = os.path.join(current, name)                               # 文件绝对路径
            rel = os.path.relpath(full, root).replace("\\", "/")             # 转成统一的斜杠相对路径
            result.append((rel, os.path.dirname(rel)))                       # 记录文件与它所在目录
    return result


def cross_imports(root, files):
    """统计跨目录 import 条数：文件引用了自己目录之外的同项目模块即计一条。

    参数:
        root: str，体检根目录，用于拼出源文件绝对路径
        files: list[tuple[str, str]]，walk() 的返回值
    返回:
        int，跨目录 import 条数
    """
    dirs = {d for _, d in files}                                             # 全部目录集合
    count = 0                                                                # 跨目录引用计数
    for rel, folder in files:                                                # 逐个源码文件解析
        if not rel.endswith(".py"):                                          # 只解析 Python 便于复现
            continue                                                         # 其它语言跳过
        try:                                                                 # 文件可能非 UTF-8
            text = open(os.path.join(root, rel), encoding="utf-8").read()     # 按相对路径读源码
        except (OSError, UnicodeDecodeError):                                # 读不到就跳过
            continue                                                         # 不计入统计
        for module in IMPORT_RE.findall(text):                               # 每行 import 取模块路径
            candidate = module.replace(".", "/")                             # 模块路径转目录形态
            if any(d and (candidate + "/").startswith(d.split("/")[-1] + "/") for d in dirs):
                count += 1                                                   # 命中其它目录即计一条
    return count


def folder_spread(files, key):
    """统计含指定关键词的文件分布在几个不同目录，衡量一个功能被拆散的程度。

    参数:
        files: list[tuple[str, str]]，walk() 的返回值
        key: str，功能关键词，如 order
    返回:
        tuple[int, int]，元素为（相关文件数，涉及目录数）
    """
    hit = [(rel, d) for rel, d in files if key in rel.lower()]               # 文件名命中关键词
    return len(hit), len({d for _, d in hit})                                # 文件数、去重目录数


def max_depth(files):
    """计算源码文件的最大目录层级，深度为 0 表示文件全在根目录。

    参数:
        files: list[tuple[str, str]]，walk() 的返回值
    返回:
        int，最大目录深度
    """
    return max((d.count("/") + (1 if d else 0) for _, d in files), default=0)  # 目录段数即深度


def report(root, key):
    """打印一份目录体检报告：体积、分散度、跨目录引用与最大深度。

    参数:
        root: str，待体检目录
        key: str，用于统计分散度的功能关键词
    返回:
        dict，各项指标，便于外部复用
    """
    files = walk(root)                                                       # 收集源码文件
    size, spread = folder_spread(files, key)                                 # 功能文件数与目录分布
    stat = {
        "文件数": len(files),                                                 # 源码文件总数
        "目录数": len({d for _, d in files if d}),                            # 非根目录数量
        "功能文件数": size,                                                   # 命中关键词的文件数
        "功能分布目录数": spread,                                             # 这些文件散落在几个目录
        "跨目录import": cross_imports(root, files),                           # 跨目录引用条数
        "最大深度": max_depth(files),                                         # 最深层级
    }
    print(f"目录: {root}")                                                   # 报告抬头
    for name, value in stat.items():                                         # 逐项输出指标
        print(f"  {name:12s}{value}")
    return stat


def make_demo(base):
    """生成两套对照布局：layer 按类型分层，feature 按功能切块，各 16 个文件。

    参数:
        base: str，样本生成目录
    返回:
        tuple[str, str]，元素为（分层布局目录，切块布局目录）
    """
    feats = ("order", "user", "pay", "report")                               # 四个功能名，作为对照单元
    layer = os.path.join(base, "demo_layer")                                 # 按类型分层的样本根目录
    feature = os.path.join(base, "demo_feature")                             # 按功能切块的样本根目录

    for f in feats:                                                          # 逐个功能写分层版文件
        for sub in ("controllers", "services", "models"):                    # 三个层目录
            os.makedirs(os.path.join(layer, sub), exist_ok=True)             # 缺目录就补建
        open(os.path.join(layer, "controllers", f + "_controller.py"), "w",
             encoding="utf-8").write(f"from services.{f}_service import run_{f}\n")   # 控制器引服务
        open(os.path.join(layer, "services", f + "_service.py"), "w",
             encoding="utf-8").write(f"from models.{f}_model import {f}_model\n"
                                     f"from utils.money import to_cents\n")   # 服务引模型与工具
        open(os.path.join(layer, "models", f + "_model.py"), "w",
             encoding="utf-8").write("from utils.base import Base\n")        # 模型引工具基类
        os.makedirs(os.path.join(feature, "features", f), exist_ok=True)     # 切块版按功能建目录
        open(os.path.join(feature, "features", f, "controller.py"), "w",
             encoding="utf-8").write(f"from features.{f}.service import run_{f}\n")  # 功能内引用
        open(os.path.join(feature, "features", f, "service.py"), "w",
             encoding="utf-8").write(f"from features.{f}.model import {f}_model\n"
                                     "from shared.money import to_cents\n")  # 仅共享工具跨出功能
        open(os.path.join(feature, "features", f, "model.py"), "w",
             encoding="utf-8").write("from shared.base import Base\n")       # 共享基类跨出功能

    for name in ("base", "money", "dates", "strings"):                       # 两侧都需要工具文件
        os.makedirs(os.path.join(layer, "utils"), exist_ok=True)             # 分层版工具目录
        os.makedirs(os.path.join(feature, "shared"), exist_ok=True)          # 切块版共享目录
        open(os.path.join(layer, "utils", name + ".py"), "w", encoding="utf-8").write("")  # 空工具文件
        open(os.path.join(feature, "shared", name + ".py"), "w", encoding="utf-8").write("")  # 空共享文件
    return layer, feature                                                    # 返回两套样本路径


if __name__ == "__main__":
    args = [a for a in sys.argv[1:]]                                         # 复制命令行参数
    key = "order"                                                            # 默认统计 order 功能
    if "--key" in args:                                                      # 支持自定义功能关键词
        key = args[args.index("--key") + 1]                                  # 取关键词后的那个值
    if "--demo" in args:                                                     # 对照模式：现场生成样本
        tmp = tempfile.mkdtemp(prefix="structure_audit_")                    # 临时目录，用完不落盘
        layer, feature = make_demo(tmp)                                      # 生成两套 16 文件布局
        print("== 按类型分层 ==")                                            # 第一组：分层
        a = report(layer, key)                                               # 体检分层样本
        print("\n== 按功能切块 ==")                                          # 第二组：切块
        b = report(feature, key)                                             # 体检切块样本
        print("\n== 差值（切块 - 分层）==")                                  # 对比输出
        for name in a:                                                       # 同名指标逐项相减
            print(f"  {name:12s}{b[name] - a[name]:+d}")
    else:
        root = args[0] if args else "."                                      # 体检目标目录
        report(root, key)                                                    # 输出单目录报告
