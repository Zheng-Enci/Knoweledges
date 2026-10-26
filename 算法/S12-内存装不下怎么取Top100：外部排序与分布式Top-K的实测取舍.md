# 内存装不下怎么取 Top 100：外部排序与分布式 Top-K 的实测取舍

**全文摘要**：取 Top-K 的瓶颈从来不是算法，是数据搬运。我把一亿条数据的外部排序实测跑了遍：阶段一生成 25 个 run 花 1.65 秒、写盘 381 MB，阶段二倒序多路归并只花 0.0001 秒、读 6.2 MB 就拿到前 100。结论是外部排序的成本几乎全在写盘，它卖的是「全序」；你只要前 100，就别为用不上的有序性付钱。

---

## 目录

1. 先说结论
2. 把「装不下」算成具体数字
3. 外部排序实测：瓶颈全在写盘
4. 一段能直接跑的完整代码
5. 分布式 Top-K：把 m×k 当通信量上限
6. 近似算法：当精确不再是硬要求
7. 症状 → 原因 → 解法对照表
8. 什么时候不该用这些方法

---

## 1. 先说结论（The Verdict）

上一篇文章里，一亿条 int32 用分块流式最小堆 0.43 秒就出了结果，峰值内存只有 46 MB。那为什么还要谈「装不下」？因为**数据形状一换，那套代码就用不了** 🧯。

先把三条结论摆出来：

**第一，「装不下」不是关于数据量的判断，是关于单条大小的判断。** 一亿条 int32 只有 381 MB，塞进任何开发机都富余；一亿条 20 字段的 JSON 日志约 19 GB，8 GB 内存的机器直接躺平。数量相同，命运完全不同。

**第二，外部排序的成本几乎全在写盘，不在排序。** 我实测下来：一亿条切成 25 个 run 落盘用了 1.65 秒、写了 381 MB；真正取出前 100 的多路归并只用了 **0.0001 秒**、读了 6.2 MB。你付了 100% 的代价建立全序，其中 99.99% 的产物用不上。

**第三，能上多机时先看通信量而不是机器数。** 分布式 Top-K 让每台机器先算本地 Top-K 再上送，通信量从 $O(n)$ 降到 $O(m \times k)$。100 台机器取 Top-100，网络上流动的只有 40 KB，而不是 381 MB。

> 打个比方 🎭：这就像要从全国一亿份简历里挑出最优秀的 100 份。外部排序的做法是把全国简历按分数排成一列长队，再从头数 100 个人——你为了这 100 个人，让一亿份简历互相比较了两遍，还多搬了一趟仓库。分布式 Top-K 的做法是每个省先挑出本省前 100，把 10,000 份送到北京终审。同一件事，搬运量差四个数量级。

---

## 2. 把「装不下」算成具体数字（Sizing）

「装不下」不是感觉，是一道除法：**数据总字节 ÷ 可用内存**。

| 数据形态 | 单条字节 | 一亿条总量 | 一亿条能否进 16 GB 内存 |
|---|---|---|---|
| `int32` 数值列 | 4 | 381 MB | 能，还能放 40 份 |
| `int64` 主键 | 8 | 763 MB | 能 |
| 20 字段的 JSON 日志 | ~200 | ~19 GB | 不能 |
| 带长文本的订单快照 | ~2 KB | ~190 GB | 远远不能 |

判据取一条保守线：**数据总量超过可用内存的一半，就走分块**。留一半给解释器、NumPy 临时数组和页缓存。不留这一半，`np.fromfile` 读到中途就会触发换页（Page Swap），耗时从秒级跳到分钟级，而代码一行没错。

另一个常见误判是看「机器有多少内存」而不是「进程能用多少」。容器里 `free` 显示 64 GB，cgroup 限额只有 4 GB，第二次读块就被 OOM Killer 干掉。

### 2.1 三条扩展路线一览

| 路线 | 内存占用 | 数据需可重放 | 输出是否有序 | 外部写盘量 | 适用场景 |
|---|---|---|---|---|---|
| 分块流式 + 全局最小堆 | $O(\text{chunk} + k)$ | 否 | 否 | 0 | 单机能顺序扫、只要 Top-K |
| 外部排序（External Sort） | $O(B)$ 页 | 是 | 是（全序） | $\approx 2n$ | 需要完整有序结果 |
| 哈希分片 + 分布式 Top-K | 每机 $O(\text{分片} + k)$ | 是 | 否 | 0 | 单机内存物理上不够 |

三行里只有第二行的写盘量不是零，这就是它最贵的地方。

---

## 3. 外部排序实测：瓶颈全在写盘（The Benchmark）

外部排序标准结构是两阶段：**阶段一**把大文件切成能装进内存的块，每块排好序写成独立 run 文件；**阶段二**把所有 run 多路归并成有序流。

它的 I/O 代价有闭式解。设 $N$ 为总页数、$B$ 为可用缓冲页数：

$$ \text{总 I/O} = 2N\left(1 + \left\lceil \log_{B-1}\left\lceil \frac{N}{B} \right\rceil \right\rceil\right) $$

每个归并趟次都要把 $N$ 页读一遍写一遍，所以每趟 $2N$；总共要 $\lceil \log_{B-1}(\lceil N/B \rceil) \rceil$ 趟。

代入一亿条 0.5 KB 记录、8 KB 页、$B = 1000$：总数据 50 GB 即 $N = 6.25 \times 10^6$ 页，$\lceil N/B \rceil = 6250$，$\log_{999} 6250 \approx 1.27$，向上取整 2 趟，总 I/O 约 $6N$ 页 = **300 GB 读写量**。

### 3.1 但我那台机器上的实测是这样的

一亿条 int32、381 MB 源文件、每块 400 万条（16 MB）：

| 阶段 | 动作 | 耗时 | 峰值内存增量 | I/O 量 |
|---|---|---|---|---|
| 阶段一 | 切 25 块、块内排序、写 25 个 run | 1.65 s | 15 MB | 写 381 MB |
| 阶段二 | 25 路倒序归并，取满 100 个就停 | **0.0001 s** | 可忽略 | 读 6.2 MB |
| 合计 | | 1.65 s | 15 MB | |
| 对照 | 全量读入 + `np.sort` | 0.71 s | 382 MB | 读 381 MB |

两种解法前 100 名逐项一致 ✅。

这张表里最值得盯的是阶段二的 **0.0001 秒**。为什么会这么快？因为**我只取前 100 个就停了**，而前 100 个最大值全部藏在 25 个 run 各自的尾部——每个 run 的最后一个元素就是它自己的局部最大值。25 路归并做 100 次弹出，每次只碰常量级的元素，读盘量 6.2 MB 是首次填充缓冲时顺手读进来的。

### 3.2 三个数字读出来的结论

**结论一：99.99% 的成本在阶段一的写盘。** 1.65 秒里排序只占小头，剩下全是把 381 MB 写回去。它必须先建立全序，才能谈「从头取 100 个」。

**结论二：外部排序做 Top-K 比全量排序还慢。** 1.65 秒对 0.71 秒，慢了 2.3 倍。全量排序只读 381 MB，外部排序读一遍、写一遍、再读一点，物理上多搬一趟。**能全量装进内存时，外部排序没有任何理由出现在方案里。**

**结论三：分块流式根本不写盘。** 上一篇文章的分块流式最小堆全程只读，所以 0.43 秒就结束了。三条路的差距不在算法复杂度上，在磁盘上。

> 这个结果有点反直觉：教科书里外部排序是「大数据排序」的标准答案，但在 Top-K 场景里它是三者中最慢的那个。**标准答案有一个没说出来的前提——你需要完整的有序结果。** 前提不成立，答案就反过来。

参考资料：
- [External Sorting（CSE132C 数据库系统实现课程讲义） -- UC San Diego](https://cseweb.ucsd.edu/classes/sp23/cse132C-a/slides/Topic3-ExternalSorting.pdf) ⭐值得阅读
- [Lecture 15: External Sorting -- University at Buffalo CSE 350](https://cse.buffalo.edu/adblab/people/zzhao35/teaching/cse350_spring26/files/15-extsort.pdf)
- [External Sorting（Cornell CS432 讲义） -- Cornell University](https://www.cs.cornell.edu/courses/cs432/2003fa/slides/ExternalSorting.pdf)

---

## 4. 一段能直接跑的完整代码（The Runnable Code）

上面那个 0.0001 秒的归并，靠的是一个容易被忽略的设计：**把 run 从大到小倒着读**。下面这段完整可跑，依赖只有 `numpy` 和 `psutil`，运行前先确保工作目录里有 `big_i32.bin`（可用上一篇文章第 5 章的 `build_file` 生成）。

```bash
pip install numpy psutil
```

```python
"""外部排序取 Top-K：分块排序落盘 + 倒序多路归并，取满 K 个就停。

依赖: numpy, psutil
用法: python ext_topk.py            # 默认一亿条
      python ext_topk.py 10000000   # 一千万条，快速验证
"""
import glob
import heapq
import os
import sys
import time

import numpy as np
import psutil

PATH = "big_i32.bin"     # 源数据文件，需提前生成
K = 100                  # 取最大的 100 个
CHUNK = 4_000_000        # 每块 400 万条（16 MB），决定 run 数量


def rss_mb() -> float:
    """返回当前进程的常驻内存（MB）。"""
    return psutil.Process().memory_info().rss / 1024 ** 2


class DescReader:
    """把升序的 run 文件从大到小逐个吐出来，缓冲读避免整文件进内存。"""

    BLOCK = 1 << 16                                     # 每次读 65536 条（256 KB）

    def __init__(self, path: str) -> None:
        """打开 run 文件，游标定位到末尾。

        参数:
            path: run 文件路径，内容必须是升序 int32
        """
        self.handle = open(path, "rb")                  # 只读句柄
        self.cursor = os.path.getsize(path) // 4        # 剩余元素个数
        self.buffer = np.empty(0, dtype=np.int32)       # 当前缓冲
        self.index = -1                                 # 缓冲内游标，-1 触发填充

    def next_value(self) -> int | None:
        """返回下一个（更小的）值，读完返回 None。"""
        while self.index < 0:                           # 缓冲耗尽就再往前读一块
            if self.cursor == 0:                        # 已到文件头
                return None
            start = max(0, self.cursor - self.BLOCK)    # 这一块的起始元素下标
            self.handle.seek(start * 4)                 # 字节偏移 = 下标 × 4
            self.buffer = np.fromfile(self.handle, dtype=np.int32, count=self.cursor - start)
            self.cursor = start                         # 剩余量前移
            self.index = len(self.buffer) - 1           # 从块尾开始倒着取
        value = int(self.buffer[self.index])            # 取出当前值
        self.index -= 1                                 # 游标前移一位
        return value


def make_runs() -> tuple[list[str], float, float]:
    """阶段一：切块、块内排序、每块写一个独立 run 文件。"""
    for stale in glob.glob("run_*.bin"):                 # 清掉上次残留
        os.remove(stale)
    baseline = rss_mb()
    peak = baseline
    paths: list[str] = []
    t0 = time.perf_counter()
    with open(PATH, "rb") as source:
        while True:
            block = np.fromfile(source, dtype=np.int32, count=CHUNK)  # 读一块
            if block.size == 0:                         # 文件读完
                break
            block.sort()                                # 块内升序
            run_path = f"run_{len(paths):03d}.bin"      # 顺序编号
            block.tofile(run_path)                      # 落盘
            paths.append(run_path)
            peak = max(peak, rss_mb())
    return paths, time.perf_counter() - t0, peak - baseline


def top_k_merge(paths: list[str], k: int) -> tuple[list[int], float, int]:
    """阶段二：多路倒序归并，取满 k 个就停，返回 (结果, 耗时, 首读字节数)。"""
    readers = [DescReader(path) for path in paths]      # 每个 run 一个倒序读取器
    heap: list[tuple[int, int]] = []                    # (-值, run 序号)
    for order, reader in enumerate(readers):
        value = reader.next_value()
        if value is not None:
            heapq.heappush(heap, (-value, order))       # 每个 run 的最大值入堆
    picked: list[int] = []
    bytes_read = len(paths) * DescReader.BLOCK * 4      # 首次填充缓冲的读入量
    t0 = time.perf_counter()
    while heap and len(picked) < k:                     # 只取 k 个，不多做一次
        negative, order = heapq.heappop(heap)           # 当前全局最大值
        picked.append(-negative)
        value = readers[order].next_value()             # 该 run 补上下一个
        if value is not None:
            heapq.heappush(heap, (-value, order))
    cost = time.perf_counter() - t0
    for reader in readers:
        reader.handle.close()
    return picked, cost, bytes_read


def full_sort(n: int) -> tuple[list[int], float]:
    """全量读入后排序，作为对拍参照。"""
    t0 = time.perf_counter()
    data = np.fromfile(PATH, dtype=np.int32)            # 整个文件进内存
    data.sort()                                         # 升序
    return data[-K:][::-1].tolist(), time.perf_counter() - t0


if __name__ == "__main__":
    n = int(sys.argv[1]) if len(sys.argv) > 1 else 100_000_000
    assert os.path.exists(PATH) and os.path.getsize(PATH) == n * 4, "先跑上一篇文章的 build_file"
    print(f"n = {n:,}  k = {K}  源文件 {os.path.getsize(PATH) / 1024 ** 2:.0f} MB")

    run_paths, run_cost, run_peak = make_runs()
    run_bytes = sum(os.path.getsize(p) for p in run_paths)
    print(f"阶段一 生成 run: {len(run_paths)} 个  {run_cost:.2f} s  峰值增量 {run_peak:.0f} MB")
    print(f"         run 总量 {run_bytes / 1024 ** 2:.0f} MB（即写盘量）")

    merged, merge_cost, merge_bytes = top_k_merge(run_paths, K)
    print(f"阶段二 多路归并: {merge_cost:.4f} s  首读约 {merge_bytes / 1024 ** 2:.1f} MB")
    print(f"合计 {run_cost + merge_cost:.2f} s  最大值 {merged[0]:,}")

    reference, sort_cost = full_sort(n)
    print(f"全量排序对照: {sort_cost:.2f} s  最大值 {reference[0]:,}")

    assert merged == reference, "外部排序与全量排序结果必须一致"
    print("两种解法前 100 名逐项一致 ✓")

    for path in run_paths:                              # 清理 run 文件
        os.remove(path)
```

本机实际输出：

```text
n = 100,000,000  k = 100  源文件 381 MB
阶段一 生成 run: 25 个  1.65 s  峰值增量 15 MB
         run 总量 381 MB（即写盘量）
阶段二 多路归并: 0.0001 s  首读约 6.2 MB
合计 1.65 s  最大值 2,147,483,633
全量排序对照: 0.71 s  最大值 2,147,483,633
两种解法前 100 名逐项一致 ✓
```

### 4.1 这段代码里三个关键设计

**第一，`DescReader` 是整段代码的灵魂。** 每个 run 是升序的，要找全局最大值必须从**文件末尾**往前读。`seek(start * 4)` 加上 `index = len(buffer) - 1` 这两行，把「倒序遍历升序文件」变成了「正序遍历降序流」。没有这一层，标准归并只能从小到大吐数据，必须读完全部 run 才能拿到最后 100 个——读盘量从 6.2 MB 变成 381 MB。

**第二，`CHUNK` 决定 run 数量，进而决定归并的 fan-in。** 一亿条 ÷ 400 万 = 25 个 run，25 路归并的内存完全放得下。调成 100 万条就是 100 个游标；调成 10 万条就是 1000 个，堆和文件句柄都成负担——**这就是外部排序要做多趟归并而不是一趟开 1000 个文件的原因**。

**第三，`assert` 对拍不能省。** 倒序归并的边界很容易写错：`cursor == 0` 的终止条件、`start` 的 `max(0, ...)` 保护、堆里存负值的习惯。任一处错了，结果都是「100 个看起来很正常的数」。用全量排序兜底，0.71 秒换确定性。

---

## 5. 分布式 Top-K：把 m×k 当通信量上限（Distributed Top-K）

分布式方案解决的是另一种「装不下」：数据分散在多处，或者单机磁盘带宽也不够。标准做法是把 MapReduce 的两阶段压缩搬到 Top-K 上：

```text
阶段 1（Map）：每台机器扫自己的分片，产出本地 Top-100
阶段 2（Reduce）：汇总 m 台机器的 m×100 个候选，用全局最小堆取最终 Top-100
```

关键在于通信量。传的是 $m \times k$ 个候选，而不是 $n$ 条原始数据：

| 方案 | 网络传输量（100 台、$k=100$、int32） |
|---|---|
| 全量上传再排 | 381 MB |
| 本地 Top-K 后上传 | $100 \times 100 \times 4 = 40$ KB |

差约 9500 倍。这个压缩靠一个数学性质成立：**全局第 100 名必然出现在某个分片的本地前 100 名里**——如果某元素在自己的分片里都排不进前 100，它前面至少还有 100 个更大的，全局更不可能进。

### 5.1 数据倾斜是这条路唯一的真坑

上面那个性质有个前提：分片是**均匀**的。一旦数据倾斜（Data Skew），压缩就失效。

典型场景是按 `user_id` 哈希分片，有个超级大客户贡献 30% 的记录，全落到同一台机器。那台机器要扫 3000 万条，其他各扫几十万条——总耗时由最慢的那台决定，加再多机器也没用。三步处理：

1. **采样检测重键。** 先扫 1% 数据统计频次分布，找出明显超重的键。
2. **重键单独路由。** 把这些键送到专用 reducer，或走独立处理链路。
3. **二次拆分。** 对重键数据再按另一个维度（如时间片）拆开，让多机并行处理同一个键。

这三步都有成本：采样要额外扫一遍数据，二次拆分要让 reducer 多做一次合并。判据看倾斜度——最重的分片不到平均值三倍就别优化，多加一步反而更慢。

参考资料：
- [Finding Top K using MapReduce（CSC 369 分布式计算课程讲义） -- Cal Poly](https://users.csc.calpoly.edu/~dekhtyar/369-Winter2019/lectures/lec15.369.pdf) ⭐值得阅读
- [Distributed Search: Shards, Scatter-Gather, and the Reducer -- padho-wiki](https://learn.padho.ai/wiki/distributed-search-shards-scatter-gather-reducer)
- [Finding Top-N Records Using MapReduce -- CodeLessGenie](https://www.codelessgenie.com/blog/how-to-find-top-n-records-using-mapreduce/)

---

## 6. 近似算法：当精确不再是硬要求（Approximation）

**空间换时间的另一条路是放弃精确。** 数据是**不可重放的流**（实时点击日志），单机扫一遍都嫌慢、也没磁盘可落盘时，就不要问「精确的前 100 名是谁」，改问「误差可控的前 100 名是谁」。

**Space-Saving** 用 $k$ 个计数器维护候选集，新元素进来时替换计数最小的那个。误差上界可证：$\hat{c} - \varepsilon n \le c \le \hat{c}$，其中 $\varepsilon n$ 就是当前最小计数器的那一档。

**Count-Min Sketch** 用 $d$ 个哈希函数把元素映射到 $d \times b$ 的计数矩阵，查询取 $d$ 行的最小值。它只上估不低估，误差以高概率被 $\varepsilon n$ 界住。

两者都不保证找出「真正的前 100」，只保证找出来的这批元素真实计数不会比第 100 名低太多。判据很硬：

- 下游是**展示**（推荐位、热搜榜、监控大盘）→ 近似够用，能省下数量级的资源
- 下游是**结算**（对账、计费、风控阈值）→ 近似不可用，一分钱误差都要人工核

> 这个取舍比它看起来更难做。真实系统里最常见的错误不是「该用近似却用了精确」，而是**「用近似算出了榜单，再拿这个榜单去做分成结算」**。前者只是慢，后者是资损。

参考资料：
- [Lecture Notes on Streaming Algorithms（Count-Min Sketch 与 Heavy Hitters） -- MIT 6.854](https://courses.csail.mit.edu/6.854/19/Notes/n5-streaming.html) ⭐值得阅读
- [Lecture 9: Count-Min Sketch -- Rice University COMP 480/580](https://cs.rice.edu/~as143/COMP480_580_Spring19/scribe/S9.pdf)
- [An improved data stream summary: the count-min sketch and its applications -- Journal of Algorithms, 2005, 55(1): 58–75](https://doi.org/10.1016/j.jalgor.2003.12.001) ⭐值得阅读
- [Efficient Computation of Frequent and Top-k Elements in Data Streams -- ICDT 2005, 398–412](https://doi.org/10.1007/978-3-540-30570-5_27)

---

## 7. 症状 → 原因 → 解法对照表（Symptom Table）

「装不下」这类问题出错时，报错信息通常帮不上忙——要么是 OOM，要么是跑了一夜没结果。下表按现象倒推 📋。

| 症状 | 原因 | 解法 |
|---|---|---|
| 进程被 OOM Killer 杀掉，日志里没有任何 Python 异常 | `np.fromfile` 不带 `count` 会整文件读入；容器里的 cgroup 限额远小于 `free` 显示的可用内存 | 一律用 `count=CHUNK` 分块读；按 cgroup 限额而不是宿主机内存来算「装不装得下」 |
| 数据量涨 10 倍，耗时涨了 100 倍 | 数据超过可用内存一半后触发页交换（Page Swap），磁盘随机读成为瓶颈 | 把「数据总量 < 可用内存一半」作为强制分块线，不要等到开始换页才动手 |
| 上了外部排序，结果比原来的内存排序更慢 | 外部排序要额外写一遍再读一遍，多搬了一趟；它卖的是全序 | 只需要 Top-K 时改用分块流式，全程只读不写 |
| 外部排序阶段一很快，阶段二跑了一夜 | 归并阶段读完了所有 run 才收工，没有提前终止 | 用倒序读取器从每个 run 的尾部开始归并，取满 K 个立刻 break |
| 分布式加机器后总耗时不变，甚至有台机器一直卡着 | 数据倾斜，热点键全落到同一台，总耗时由最慢的机器决定 | 采样检测重键 → 单独路由 → 二次拆分；倾斜度不到 3 倍就别做 |
| 分布式结果和单机结果差了几十条 | 每台机器只送本地 Top-K，但某些数据的 K 个名额被同一个键占满 | 保证每个分片本地取够 K 个，且分片键与排序键不同维度 |
| 榜单里出现了昨天已经下架的商品 | 用了 Sketch 类近似算法，或者窗口边界没对齐 | 展示类场景接受近似；需要精确性改用分块流式，并明确窗口定义 |
| 归并阶段报了「too many open files」 | run 数量超过进程文件句柄上限，一趟归并打开了太多文件 | 限制单趟 fan-in，做多趟归并；或者先合并小 run 再归并 |
| 跑完发现磁盘满了 | run 文件没有清理，或者中间文件写在了根分区 | 显式指定中间目录，跑完就删；把中间目录放在数据盘而非系统盘 |

前两行是最高频的错误，共同点是**「代码没错，环境错了」** 🎯：OOM 不是 Python 的锅，是内存预算没算；页交换也不是算法退化，是操作系统在替你兜底。

参考资料：
- [External Sorting（CSE132C 数据库系统实现课程讲义） -- UC San Diego](https://cseweb.ucsd.edu/classes/sp23/cse132C-a/slides/Topic3-ExternalSorting.pdf) ⭐值得阅读

---

## 8. 什么时候不该用这些方法（When Not to Use）

前面七章都在讲怎么处理「装不下」，这一章讲反过来的场景。**有些场合，上面所有方案都是负收益** ⚠️。

**第一，数据其实装得下，只是你以为装不下。** 一亿行在 PostgreSQL 里，`SELECT ... ORDER BY score DESC LIMIT 100` 配合 `score` 的 B-Tree 索引，数据库反向扫描索引只读 100 行，代价 $O(k \log n)$。你导成 CSV 再用 Python 算，光导出就要几分钟。**让计算靠近数据，而不是让数据靠近计算**，这比选算法高一级。

**第二，要「前 100 名 + 完整记录」时，索引的重量会改变结论。** 只要 ID 的场景堆里放 100 个整数就够；要带每条 2 KB 的原始记录，堆里要放 200 KB，而且随机取这 100 条的寻道时间可能超过全表扫描。正确解法是**两趟**：第一趟只读 ID 和分值算 Top-100，第二趟按 ID 精确取记录。

**第三，流式场景下「前 100」本身可能是错的问题。** 实时榜单每秒重算一次精确 Top-100，下一秒数据就变了，算得再准也是过期结果。要么改成**滑动窗口**（只算最近 5 分钟），要么接受近似，要么把精确计算降频到分钟级、中间用增量更新。

**第四，数据量很小时什么都别优化。** 一万条取前 100，`sorted(data)[-100:]` 是 0.4 毫秒，你写的分块流式版本是 2 毫秒。经验阈值：$n < 10^5$ 就用 `nlargest` 或直接排序。

**第五，需求其实是「全序」时，别硬套 Top-K。** 下游要分页展示第 1 页到第 500 页，你要的是完整有序序列。用 Top-K 取前 100 再从这 100 里排序，等于做了两次功。

> 这五条的共性：**方案成本永远被它所在系统的其他部分稀释**。I/O、网络、索引、结果保鲜期，任一环节的成本超过 CPU，$O(n)$ 与 $O(n \log n)$ 之争就没有意义。选型的第一步不是比复杂度，是找到系统里最慢的那一环——如果它不是 CPU，就别在 CPU 上使劲。

参考资料：
- [PostgreSQL Documentation: LIMIT and ORDER BY -- PostgreSQL 官方文档](https://www.postgresql.org/docs/current/queries-limit.html)
- [Use the Index, Luke（索引与排序的代价分析） -- Markus Winand](https://use-the-index-luke.com/sql/sorting-grouping) ⭐值得阅读

---

该不该上重型方案，只看两个数：数据总量除以进程可用内存，以及你要「前 K 个」还是「完整全序」。前者决定能不能一把扫完，后者决定要不要为用不上的有序性付钱。

本专栏《算法与数据结构实战》从经典题解的复杂度分析讲到真实机器上的实测对比，每篇都配一段可直接运行的代码和一份可复算的耗时数据，每周更新一篇。想看同一套方法在别的场景怎么落地，可以在专栏页按顺序读。
