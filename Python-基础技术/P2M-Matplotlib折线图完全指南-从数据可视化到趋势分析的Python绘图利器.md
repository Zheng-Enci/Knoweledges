# P2M-Matplotlib折线图完全指南-从数据可视化到趋势分析的Python绘图利器

本文档基于 Matplotlib 从零实现折线图的绘制，涵盖环境准备、`plot()` 函数核心参数详解（线型、颜色、标记、线宽）、完整代码实现及逐行解析、运行结果展示等内容。通过一个2026年两款产品月度销售额对比的实际案例，帮助读者深入理解折线图的绘制方法和参数配置技巧 📈

This document implements line chart drawing from scratch using Matplotlib, covering environment setup, detailed parameter explanation of the `plot()` function (linestyle, color, marker, linewidth), complete code implementation with line-by-line analysis, and result visualization. Through a real-world 2026 monthly sales comparison case study of two products, it helps readers deeply understand line chart drawing techniques and parameter configuration 📈

---

## 术语表 / Terminology

| 术语 / Term | 说明 / Description |
|-------------|-------------------|
| **Line Chart（折线图）** | 用于展示数据随时间或顺序变化的趋势图，通过连接数据点形成折线 |
| **plot()** | Matplotlib 中绘制折线图的核心函数，支持线型、颜色、标记等参数 |
| **linestyle（线型）** | 线条的样式，如实线 `-`、虚线 `--`、点线 `:`、点划线 `-.` |
| **marker（标记）** | 数据点的形状标识，如菱形 `D`、方形 `s`、圆形 `o`、三角形 `^` |
| **linewidth（线宽）** | 线条的粗细，以浮点数表示，默认值为 1 |
| **legend（图例）** | 图表中用于区分不同数据系列的标识说明 |
| **grid（网格线）** | 图表中的辅助网格线，提升数据的可读性 |
| **alpha（透明度）** | 图形元素的透明度，取值范围 [0, 1]，0 为完全透明 |

---

## 章节阅读路线图 🗺️ / Chapter Reading Roadmap

1. **环境准备** 🧰 / Environment Setup → 确认 Matplotlib 安装并导入必要库
2. **折线图基础概念** 📈 / Basic Concepts of Line Chart → 了解折线图的定义、适用场景和核心要素
3. **核心参数详解** 🔧 / Core Parameters Explained → 深入理解 `plot()` 函数的关键参数及其作用
4. **完整代码实现** 💻 / Complete Code Implementation → 产品月销售额对比案例的完整代码
5. **代码逐行解析** 🔍 / Line-by-Line Code Analysis → 详细拆解每一步的数据处理和图元配置
6. **运行结果展示** 📊 / Result Visualization → 展示生成的折线图效果
7. **总结** 📝 / Summary → 回顾核心要点和参数配置技巧

---

## 1. 环境准备 🧰 / Environment Setup

> 📦 **Note:** 本章确认 Matplotlib 安装并导入必要库 / This chapter confirms Matplotlib installation and imports required libraries.

🔧 在开始绘图之前，请确保你的环境中已经安装了 Matplotlib。如果还没有安装，可以通过以下命令快速安装：

```bash
pip install matplotlib
```

📚 绘制折线图通常只需要导入 Matplotlib 的 pyplot 模块，同时为了处理中文显示问题，还需要进行字体配置：

```python
import matplotlib.pyplot as plt              # 导入 pyplot 模块，提供类似 MATLAB 的绘图接口 📈
import numpy as np                           # 导入 NumPy 库，用于数值计算和数组操作 🔢

# 设置 Matplotlib 支持中文显示 🇨🇳
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']  # 设置中文字体为黑体，英文字体为 DejaVu Sans
plt.rcParams['axes.unicode_minus'] = False   # 解决坐标轴负号显示为方块的问题 ✅
```

- **matplotlib.pyplot** 📈：Matplotlib 的核心模块，提供类似 MATLAB 的绘图接口
- **numpy** 🔢：数值计算库，用于处理数据数组
- **rcParams** ⚙️：Matplotlib 的运行时配置参数字典，用于全局设置字体、样式等

> 💡 如果你的系统没有 SimHei 字体，也可以使用其他中文字体如 `'Microsoft YaHei'`（微软雅黑）或 `'KaiTi'`（楷体），具体取决于你的操作系统。

---

**参考资料：**

- [matplotlib.pyplot.plot 官方文档 -- Matplotlib](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html) ⭐值得阅读
- [Matplotlib 绘图线 -- 菜鸟教程](https://www.runoob.com/matplotlib/matplotlib-line.html)
- [Matplotlib 中文乱码解决方案教程 -- 知乎](https://zhuanlan.zhihu.com/p/30790786209)
- [Matplotlib 中设置自定义中文字体的正确姿势 -- 阿里云](https://developer.aliyun.com/article/1640810)

---

## 2. 折线图基础概念 📈 / Basic Concepts of Line Chart

> 📈 **Note:** 本章介绍折线图的定义、适用场景和核心要素 / This chapter introduces the definition, use cases, and core elements of line charts.

### 2.1 什么是折线图？🤔 / What is a Line Chart?

**折线图（Line Chart）** 是一种将数据点按顺序用直线段连接起来的统计图表。它将数据点绘制在二维坐标系中，横轴通常表示时间或顺序（如月份、年份），纵轴表示数值（如销售额、温度）。折线图的**核心价值在于展示趋势** —— 通过折线的上升、下降或平坦来直观反映数据随时间或顺序的变化规律。

**直观类比** 🏔️：想象你记录了一座山峰在攀登过程中每个时间点的海拔高度

- 将每个时间点的海拔位置标记出来（数据点）
- 用线把这些点连接起来（折线）
- 如果线路一路上升 → 表示在持续爬升
- 如果线路先升后降 → 表示翻过了山顶开始下山

### 2.2 适用场景 🎯 / When to Use Line Charts

折线图最适合展示 **"数据随时间或顺序的变化趋势"**，特别是在以下场景：

| 场景 | 示例 | 说明 |
|------|------|------|
| **时间序列分析** 📅 | 月度销售额变化趋势 | 展示数据随时间的变化方向 |
| **对比趋势** ⚔️ | 多款产品同期销售对比 | 比较不同系列的趋势差异 |
| **增长分析** 📊 | 用户数量增长曲线 | 展示增长速度变化 |
| **波动分析** 🌊 | 股价每日收盘价变化 | 展示数据波动规律 |

### 2.3 使用注意事项 ⚠️ / Usage Considerations

折线图虽然直观，但有以下注意事项：

1. **横轴建议有序** 🔢：折线图假设横轴的数据是有序的（如时间序列），如果横轴是无序类别，建议使用条形图
2. **线条不宜过多** 📏：同一图表中线条建议不超过 5 条，过多会导致图表混乱难以辨认
3. **数据点密度适中** 🎯：数据点太少可能隐藏趋势细节，太多则可能使图表显得拥挤
4. **纵轴从零开始** ⚖️：除非有特殊原因，纵轴应从零开始以避免夸大趋势变化

---

**参考资料：**

- [Line Plots in Matplotlib -- DataCamp](https://www.datacamp.com/tutorial/line-plots-in-matplotlib-with-python) ⭐值得阅读
- [Matplotlib 绘图线类型样式 -- 菜鸟教程](https://www.runoob.com/matplotlib/matplotlib-line.html)
- [Matplotlib 折线图教程 -- CSDN](https://blog.csdn.net/bbaaa123/article/details/142074009)

---

## 3. 核心参数详解 🔧 / Core Parameters Explained

> 🔧 **Note:** 本章深入讲解 `plot()` 函数的关键参数及其作用 / This chapter explains the key parameters of the `plot()` function in detail.

`plt.plot()` 是 Matplotlib 中用于绘制折线图的核心函数，其基本语法如下：

```python
plt.plot(x, y, fmt, linestyle='-', linewidth=1, marker=None,
         color=None, label=None, markersize=6, markeredgecolor=None)
```

### 3.1 核心参数速查表 📋 / Core Parameters Quick Reference

| 参数 | 类型 | 默认值 | 说明 |
|------|------|--------|------|
| `x` | array-like | 必填 | 数据点的横坐标，通常为时间或有序序列 |
| `y` | array-like | 必填 | 数据点的纵坐标，即要展示的数值 |
| `color` / `c` | str | 自动循环 | 线条颜色，支持颜色名称、十六进制、RGB 等 |
| `linestyle` / `ls` | str | `'-'` | 线型：`'-'` 实线、`'--'` 虚线、`':'` 点线、`'-.'` 点划线 |
| `linewidth` / `lw` | float | 1 | 线条宽度，值越大线条越粗 |
| `marker` | str | None | 数据点标记样式：`'D'` 菱形、`'s'` 方形、`'o'` 圆形、`'^'` 上三角 |
| `markersize` / `ms` | float | 6 | 标记点的大小 |
| `markeredgecolor` / `mec` | str | 自动 | 标记点边缘颜色 |
| `markerfacecolor` / `mfc` | str | 自动 | 标记点填充颜色 |
| `label` | str | None | 图例标签文字，用于 `plt.legend()` 显示 |

### 3.2 格式化字符串 fmt 🏷️ / Format String

`plot()` 支持使用**格式化字符串（fmt）** 快速设置颜色、标记和线型。格式为：

```python
plt.plot(x, y, '[color][marker][linestyle]')
```

**示例**：`'bo-'` 表示蓝色（b）圆形标记（o）实线（-）

| 颜色码 | 含义 | 标记码 | 含义 | 线型码 | 含义 |
|--------|------|--------|------|--------|------|
| `'b'` | 蓝色 | `'D'` | 菱形 | `'-'` | 实线 |
| `'r'` | 红色 | `'s'` | 方形 | `'--'` | 虚线 |
| `'g'` | 绿色 | `'o'` | 圆形 | `':'` | 点线 |
| `'k'` | 黑色 | `'^'` | 上三角 | `'-.'` | 点划线 |
| `'m'` | 品红 | `'*'` | 星形 | `''` | 无线条 |

> ⚠️ **注意**：fmt 字符串中颜色的字母代码、标记符号和线型符号**顺序不可颠倒**，且三者之间不需要空格。如果不指定某一部分，该部分使用默认值。

### 3.3 关键参数详解 🔍 / Key Parameters Deep Dive

#### 3.3.1 `color` 参数 —— 线条颜色 🎨

`color` 参数控制线条和标记的颜色，支持多种颜色指定方式：

```python
plt.plot(x, y, color='blue')        # 颜色名称 🎨
plt.plot(x, y, color='#1f77b4')     # 十六进制颜色码 🎯
plt.plot(x, y, color=(0.1, 0.5, 0.8))  # RGB 元组（值范围 0-1）🌈
```

#### 3.3.2 `linestyle` 参数 —— 线条样式 📏

`linestyle` 控制线条的绘制样式：

```python
plt.plot(x, y, linestyle='-')        # 实线（默认），简写 '-' ➖
plt.plot(x, y, linestyle='--')       # 虚线，简写 '--' ➖➖
plt.plot(x, y, linestyle=':')        # 点线，简写 ':' ➖➖➖
plt.plot(x, y, linestyle='-.')       # 点划线，简写 '-.' ➖➖🔵
```

![linestyle 参数效果对比：左图使用实线+虚线搭配，两条折线清晰可辨；右图两条线均为实线，重叠部分难以区分](https://raw.gitcode.com/ZhengEnCi/knoweledges/raw/master/Python-%E5%9F%BA%E7%A1%80%E6%8A%80%E6%9C%AF/resources/P2M/photo/p2m_linestyle_comparison.png)

**图解读** 🔍：左图产品A 使用实线、产品B 使用虚线，两条线的趋势一目了然；右图两条线均为实线，在 2-4 月区域重叠纠缠，读者很难区分哪条线对应哪个产品。linestyle 的差异化搭配是折线图多系列展示的关键技巧。

*图片来源：本文档配套生成 -- Python-基础技术*

#### 3.3.3 `marker` 参数 —— 数据点标记 🔵

`marker` 控制每个数据点的显示形状：

```python
plt.plot(x, y, marker='D')           # 大菱形标记 💎
plt.plot(x, y, marker='s')           # 方形标记 ■
plt.plot(x, y, marker='o')           # 圆形标记 ●
plt.plot(x, y, marker='^')           # 上三角标记 ▲
plt.plot(x, y, marker='*')           # 星形标记 ✦
```

**常用标记样式速查表**：

| 标记码 | 样式 | 填充类型 | 适用场景 |
|--------|------|---------|---------|
| `'D'` | 大菱形 💎 | 填充型 | 数据点较少，需醒目显示 |
| `'d'` | 小菱形 🔹 | 填充型 | 普通数据点标注 |
| `'s'` | 方形 ■ | 填充型 | 商业图表常用 |
| `'o'` | 圆形 ● | 填充型 | 最通用的标记 |
| `'^'` | 上三角 ▲ | 填充型 | 特殊区分场景 |
| `'*'` | 星形 ✦ | 填充型 | 强调特定数据点 |
| `'.'` | 点 · | 非填充型 | 数据点密集时 |

![marker 参数效果对比：左图使用菱形标记(D)，数据点呈菱形醒目突出；右图使用方形标记(s)，数据点呈方块状清晰可见](https://raw.gitcode.com/ZhengEnCi/knoweledges/raw/master/Python-%E5%9F%BA%E7%A1%80%E6%8A%80%E6%9C%AF/resources/P2M/photo/p2m_marker_comparison.png)

**图解读** 🔍：左图展示了菱形标记（`marker='D'`），每个数据点以醒目的菱形图标标注，同时显示具体数值便于精确读取；右图展示了方形标记（`marker='s'`），数据点以方块图标标注。两种标记都能有效增强数据点的辨识度，选择哪种取决于视觉风格偏好。

*图片来源：本文档配套生成 -- Python-基础技术*

#### 3.3.4 `linewidth` 参数 —— 线条粗细 📏

```python
plt.plot(x, y, linewidth=2)          # 设置线宽为 2（默认值为 1）
```

`linewidth` 可以简写为 `lw`。较大的值使线条更粗，增强可视性。

![linewidth 参数效果对比：左图 linewidth=1 线条较细，视觉上不够突出；右图 linewidth=3 线条明显加粗，趋势更加醒目](https://raw.gitcode.com/ZhengEnCi/knoweledges/raw/master/Python-%E5%9F%BA%E7%A1%80%E6%8A%80%E6%9C%AF/resources/P2M/photo/p2m_linewidth_comparison.png)

**图解读** 🔍：左图为默认线宽（linewidth=1），线条偏细，在展示屏或打印时可能不够醒目；右图将线宽增加到 3，线条明显加粗，数据和趋势的可视性大幅提升。linewidth=2 是商业报告常用的折衷值，既醒目又不显得粗犷。

*图片来源：本文档配套生成 -- Python-基础技术*

#### 3.3.5 完整参数组合示例 💡

```python
# 产品A：蓝色实线，菱形标记，线宽 2
plt.plot(months, product_a, color='blue', linestyle='-', marker='D', linewidth=2, label='产品A')

# 产品B：红色虚线，方形标记，线宽 2
plt.plot(months, product_b, color='red', linestyle='--', marker='s', linewidth=2, label='产品B')
```

---

**参考资料：**

- [matplotlib.pyplot.plot 官方参数文档 -- Matplotlib](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html) ⭐值得阅读
- [Line plot styles in Matplotlib -- GeeksforGeeks](https://www.geeksforgeeks.org/python/line-plot-styles-in-matplotlib/)
- [Matplotlib Marker Reference -- Matplotlib](https://matplotlib.org/stable/gallery/lines_bars_and_markers/marker_reference.html) ⭐值得阅读
- [Matplotlib plot 参数配置 -- CSDN](https://blog.csdn.net/bbaaa123/article/details/142074009)
- [matplotlib 线型样式 -- 博客园](https://www.cnblogs.com/ShineLeBlog/p/16283685.html)

---

## 4. 完整代码实现 💻 / Complete Code Implementation

> 💻 **Note:** 本章展示两款产品月度销售额对比折线图的完整代码 / This chapter presents the complete code for the monthly sales comparison line chart of two products.

### 4.1 案例数据 📊 / Case Data

某公司 **2026 年第一季度（1-3月）和第二季度（4-6月）** 两款产品的月度销售额数据如下：

| 月份 | 产品A销售额（万元） | 产品B销售额（万元） |
|------|-------------------|-------------------|
| 1月 | 12.5 | 18.0 |
| 2月 | 15.0 | 14.5 |
| 3月 | 18.5 | 16.0 |
| 4月 | 22.0 | 13.5 |
| 5月 | 25.5 | 20.0 |
| 6月 | 30.0 | 24.5 |

### 4.2 完整代码 🎬 / Complete Code

```python
import matplotlib.pyplot as plt              # 导入 pyplot 模块，提供绘图接口 📈
import numpy as np                           # 导入 NumPy，用于数组运算 🔢

# ========== 1. 设置中文字体 ========== 🇨🇳
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']  # 设置黑体为默认字体，确保中文正常显示
plt.rcParams['axes.unicode_minus'] = False   # 解决负号显示为方块的问题 ✅

# ========== 2. 准备数据 ========== 📊
# 月份列表，数据流动：字符串列表 → x 轴坐标
months = ['1月', '2月', '3月', '4月', '5月', '6月']

# 产品A各月销售额（万元），数据流动：[12.5, 15, 18.5, 22, 25.5, 30] → 第一条折线
product_a = [12.5, 15.0, 18.5, 22.0, 25.5, 30.0]

# 产品B各月销售额（万元），数据流动：[18, 14.5, 16, 13.5, 20, 24.5] → 第二条折线
product_b = [18.0, 14.5, 16.0, 13.5, 20.0, 24.5]

# ========== 3. 绘制折线图 ========== 📈
# 绘制产品A：蓝色实线 + 菱形标记，线宽 2 🔵
plt.plot(months, product_a,                    # x=月份, y=产品A销售额
         color='blue', linestyle='-',           # 蓝色实线
         marker='D', linewidth=2,               # 菱形标记(D), 线宽 2
         label='产品A')                         # 图例标签

# 绘制产品B：红色虚线 + 方形标记，线宽 2 🔴
plt.plot(months, product_b,                    # x=月份, y=产品B销售额
         color='red', linestyle='--',           # 红色虚线
         marker='s', linewidth=2,               # 方形标记(s), 线宽 2
         label='产品B')                         # 图例标签

# ========== 4. 添加图表装饰 ========== 🏷️
plt.title('2026年产品月度销售对比')              # 设置图表标题，说明图表内容
plt.xlabel('月份')                              # 设置 x 轴标签，表示时间维度
plt.ylabel('销售额（万元）')                      # 设置 y 轴标签，表示销售额数值

plt.legend()                                    # 显示图例，区分产品A和产品B

plt.grid(True, alpha=0.3)                       # 添加网格线，透明度 0.3，提升可读性

# ========== 5. 显示图表 ========== 👁️
plt.show()                                      # 渲染并显示折线图（Jupyter 中可省略）
```

> 💡 **提示**：如果需要在非交互式环境中保存图片，可以使用 `plt.savefig('line_chart.png', dpi=150, bbox_inches='tight')` 替代 `plt.show()`。

---

**参考资料：**

- [matplotlib.pyplot.plot 官方文档 -- Matplotlib](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html) ⭐值得阅读
- [matplotlib.pyplot.grid 官方文档 -- Matplotlib](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.grid.html)
- [matplotlib.pyplot.legend 官方文档 -- Matplotlib](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html)
- [Line Plots in Matplotlib with Python -- DataCamp](https://www.datacamp.com/tutorial/line-plots-in-matplotlib-with-python) ⭐值得阅读
- [数据可视化| 一文带你搞定Matplotlib 绘图 -- 知乎](https://zhuanlan.zhihu.com/p/360591534)

---

## 5. 代码逐行解析 🔍 / Line-by-Line Code Analysis

> 🔍 **Note:** 本节详细拆解每一步的操作和数据流向 / This section breaks down each step's operation and data flow.

### 第1步：设置中文字体 🇨🇳

```python
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']  # 设置中文字体为黑体 SimHei
plt.rcParams['axes.unicode_minus'] = False   # 修复负号显示为方块的问题 ✅
```

Matplotlib 默认字体不支持中文，直接使用中文标签会出现乱码（显示为小方块）。通过修改 `rcParams` 配置：

- `font.sans-serif`：设置无衬线字体列表，SimHei（黑体）排在第一优先级
- `axes.unicode_minus`：设置为 `False` 解决负号显示异常

> 💡 **为什么需要设置中文字体？** Matplotlib 的默认字体是 DejaVu Sans，它不包含中文字符集。SimHei（黑体）是 Windows 系统自带的中文字体，也可以使用 `'Microsoft YaHei'`（微软雅黑）。

### 第2步：准备数据 📊

```python
months = ['1月', '2月', '3月', '4月', '5月', '6月']
product_a = [12.5, 15.0, 18.5, 22.0, 25.5, 30.0]
product_b = [18.0, 14.5, 16.0, 13.5, 20.0, 24.5]
```

**数据准备要点** 💡：

1. **months（横轴数据）**：是月份标签列表，用作 x 轴刻度标签
2. **product_a（纵轴数据）**：产品A在 1-6 月的销售额，呈现**持续上升**趋势（12.5 → 30.0）
3. **product_b（纵轴数据）**：产品B在 1-6 月的销售额，呈现**先降后升**的波动趋势（18.0 → 14.5 → 24.5）
4. **数据对齐**：两个产品的数据与 months 列表一一对应，月份索引相同的数据点在同一个 x 轴位置

### 第3步：绘制折线图 📈

这是最核心的一步，`plt.plot()` 的每个参数都有明确的作用：

```python
# 绘制产品A：蓝色实线 + 菱形标记，线宽 2 🔵
plt.plot(months, product_a,
         color='blue', linestyle='-',
         marker='D', linewidth=2,
         label='产品A')

# 绘制产品B：红色虚线 + 方形标记，线宽 2 🔴
plt.plot(months, product_b,
         color='red', linestyle='--',
         marker='s', linewidth=2,
         label='产品B')
```

**参数详解** 🔍：

**`color='blue'` 和 `color='red'`** 🎨：

定义两条折线的颜色，帮助读者快速区分两个产品系列。产品A使用蓝色，传递专业、稳定的视觉感知；产品B使用红色，传递活力、波动的视觉感知。

**`linestyle='-'` 和 `linestyle='--'`** 📏：

- 产品A使用实线 `'-'`，表示其销售额持续稳定增长的趋势
- 产品B使用虚线 `'--'`，表示其销售额有波动的特点
- 线型和颜色的双重区分，确保即使黑白打印也能识别

**`marker='D'` 和 `marker='s'`** 🔵：

- 产品A使用菱形标记 `'D'`（Diamond），每个数据点用菱形标识
- 产品B使用方形标记 `'s'`（Square），每个数据点用方形标识
- 标记显著增强了每个数据点的可视性，读者可以精确定位到各个月的销售数据

**`linewidth=2`** 📏：

`linewidth=2` 将线条宽度设为默认值的 2 倍，使折线更醒目。在实际的商业报告中，适当的线宽（1.5-2.5）通常比默认的 1.0 更具可读性。

**`label='产品A'` 和 `label='产品B'`** 🏷️：

`label` 参数为每条折线赋予一个名称，用于图例显示。该名称会出现在 `plt.legend()` 生成的图例框中，帮助读者理解每条折线对应哪个产品。

### 第4步：添加图表装饰 🏷️

```python
plt.title('2026年产品月度销售对比')              # 设置标题，说明图表主题
plt.xlabel('月份')                              # 设置 x 轴标签
plt.ylabel('销售额（万元）')                      # 设置 y 轴标签
plt.legend()                                    # 显示图例
plt.grid(True, alpha=0.3)                       # 添加网格线，透明度 0.3
```

**`plt.title()`** 🏷️：

设置图表的标题，置于图表顶部，说明图表展示的内容。标题应简洁明了，让读者一眼看出图表主题。

**`plt.xlabel()` 和 `plt.ylabel()`** 📍：

分别设置 x 轴和 y 轴的标签：
- x 轴标签 `'月份'`：说明横轴表示时间维度（1 月到 6 月）
- y 轴标签 `'销售额（万元）'`：说明纵轴表示销售额数值，单位为万元

**`plt.legend()`** 🏷️：

`legend()` 会自动读取每条折线的 `label` 参数值，生成一个图例框。图例通常放置在图表空白区域（默认 `loc='best'` 自动选择最佳位置），帮助读者对照颜色和线型识别数据系列。

**`plt.grid(True, alpha=0.3)`** 📐：

`grid(True)` 开启网格线，`alpha=0.3` 设置网格线透明度为 30%：
- 网格线帮助读者更精确地读取数据点的数值
- 透明度 0.3 使网格线不会喧宾夺主，保持图表干净
- 读者可以在网格线的辅助下，快速估算每个数据点的大致数值

![grid 参数效果对比：左图无网格线，数据点估值困难；右图添加半透明网格线（alpha=0.3），数据定位更精准](https://raw.gitcode.com/ZhengEnCi/knoweledges/raw/master/Python-%E5%9F%BA%E7%A1%80%E6%8A%80%E6%9C%AF/resources/P2M/photo/p2m_grid_comparison.png)

**图解读** 🔍：左图没有开启网格线，读者虽然能看到两条折线的相对走势，但无法准确判断某个数据点的具体数值（如产品A 5月的销售额是接近 25 还是 26 万元？）。右图添加了 alpha=0.3 的半透明网格线，每个数据点都有横纵网格参考，可以快速估算出产品A 5月销售额约 25.5 万元。网格线的 alpha=0.3 保证了可读性的同时不会喧宾夺主。

*图片来源：本文档配套生成 -- Python-基础技术*

### 数据趋势解读 📊

从生成的折线图中可以观察到两个产品的不同销售趋势：

| 产品 | 趋势 | 解读 |
|------|------|------|
| **产品A** 📈 | **持续上升**（12.5 → 30.0） | 销售额逐月稳步增长，6 月比 1 月增长 140%，表现强劲 |
| **产品B** 📉📈 | **先降后升**（18.0 → 14.5 → 24.5） | 1-2 月下滑，3-4 月筑底，5-6 月反弹回升 |

---

**参考资料：**

- [Matplotlib 核心类与常用函数 -- 博客园](https://www.cnblogs.com/wangya216/p/19268153) ⭐值得阅读
- [Matplotlib 设置图表标签 -- STEAM 教育学习网](https://steam.oxxostudio.tw/category/python/example/matplotlib-label.html)
- [Customizing Line Properties in Matplotlib -- Medium](https://medium.com/@budisumandra/customizing-line-properties-in-matplotlib-mastering-the-basics-be67f457ae65)

---

## 6. 运行结果展示 📊 / Result Visualization

> 📊 **Note:** 本章展示生成的折线图效果 / This chapter shows the resulting line chart.

运行上述代码后，将生成一张包含两条折线的对比图表：

- 🔵 **产品A（蓝色实线 + 菱形标记）**：1-6 月销售额持续上升，从 12.5 万元增长到 30.0 万元
- 🔴 **产品B（红色虚线 + 方形标记）**：1-4 月先降后稳（18.0 → 13.5），5-6 月快速反弹增长到 24.5 万元

**折线图解读要点** 🔍：

1. **趋势线方向** 📈：折线的倾斜方向反映变化趋势（上升/下降/平稳）
   - 产品A 的线整体向上倾斜 → 持续增长
   - 产品B 的线先向下然后向上 → V 型反弹
2. **线条陡峭程度** 📏：线条越陡表示变化越快
   - 产品A 的 4-6 月段明显比 1-3 月更陡 → 增长速度加快
3. **数据点位置** 🎯：标记点的纵坐标位置对应具体的销售额
   - 使用网格线辅助，可以快速读出每条线各月的大致销售额
4. **两条线的交叉** ⚡：折线的交叉点表示两个产品在该月的销售额相等或接近
   - 产品A 和产品B 在 3 月左右销售额最为接近

> 💡 **Key Takeaways / 核心要点**
>
> - **Line chart visualizes trends** — reveal patterns of increase, decrease, or fluctuation over time / 折线图展示趋势变化，揭示增长、下降或波动规律
> - **Color + linestyle + marker triple encoding** — use multiple visual cues to distinguish data series / 颜色+线型+标记三重编码，多维度区分数据系列
> - **Grid improves readability** — semi-transparent grid helps estimate values accurately / 网格线提升可读性，半透明网格辅助精确估值
> - **Linewidth enhances visibility** — thicker lines (lw=2) make trends more prominent / 增加线宽（lw=2）让趋势更加醒目

---

**参考资料：**

- [Line plot styles in Matplotlib -- GeeksforGeeks](https://www.geeksforgeeks.org/python/line-plot-styles-in-matplotlib/)
- [Matplotlib 绘图线 -- 菜鸟教程](https://www.runoob.com/matplotlib/matplotlib-line.html)
- [Customizing Line Properties in Matplotlib -- Medium](https://medium.com/@budisumandra/customizing-line-properties-in-matplotlib-mastering-the-basics-be67f457ae65)

---

## 7. 总结 📝 / Summary

本节我们完成了 Matplotlib 折线图的绘制，从案例数据到完整代码实现，核心要点回顾：🎯

| 步骤 | 操作 | 代码对应 |
|------|------|---------|
| 1️⃣ | 设置中文字体 | `plt.rcParams['font.sans-serif'] = ['SimHei', ...]` |
| 2️⃣ | 准备数据 | `months = [...]`, `product_a = [...]`, `product_b = [...]` |
| 3️⃣ | 绘制产品A折线 | `plt.plot(months, product_a, color='blue', linestyle='-', marker='D', linewidth=2)` 🔵 |
| 4️⃣ | 绘制产品B折线 | `plt.plot(months, product_b, color='red', linestyle='--', marker='s', linewidth=2)` 🔴 |
| 5️⃣ | 添加标题和标签 | `plt.title()`, `plt.xlabel()`, `plt.ylabel()` 🏷️ |
| 6️⃣ | 显示图例 | `plt.legend()` 🏷️ |
| 7️⃣ | 添加网格线 | `plt.grid(True, alpha=0.3)` 📐 |
| 8️⃣ | 显示图表 | `plt.show()` 👁️ |

🔴 **关键理解**：

- 📈 折线图的核心是展示**数据随时间的变化趋势**，使用 `plot()` 函数绘制
- 🎨 `color` 参数通过颜色区分不同数据系列，让图表一目了然
- 📏 `linestyle` 和 `linewidth` 控制线条样式和粗细，增强视觉层次
- 🔵 `marker` 参数为数据点添加标记（菱形 `'D'`、方形 `'s'`），精确标示每个数据值
- 🏷️ `legend()` 自动根据 `label` 生成图例，帮助读者识别数据系列
- 📐 `grid(True, alpha=0.3)` 添加半透明网格线，大幅提升数据可读性

---

**参考资料：**

- [matplotlib.pyplot.plot 官方文档 -- Matplotlib](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.plot.html) ⭐值得阅读
- [matplotlib.pyplot.grid 官方文档 -- Matplotlib](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.grid.html)
- [matplotlib.pyplot.legend 官方文档 -- Matplotlib](https://matplotlib.org/stable/api/_as_gen/matplotlib.pyplot.legend.html)
- [Line plot styles in Matplotlib -- GeeksforGeeks](https://www.geeksforgeeks.org/python/line-plot-styles-in-matplotlib/)
- [Matplotlib Marker Reference -- Matplotlib](https://matplotlib.org/stable/gallery/lines_bars_and_markers/marker_reference.html) ⭐值得阅读
- [Matplotlib Linestyles -- Matplotlib](https://matplotlib.org/stable/gallery/lines_bars_and_markers/linestyles.html) ⭐值得阅读
- [Line Plots in Matplotlib with Python -- DataCamp](https://www.datacamp.com/tutorial/line-plots-in-matplotlib-with-python)
- [Matplotlib 绘图线 -- 菜鸟教程](https://www.runoob.com/matplotlib/matplotlib-line.html)
- [数据可视化| 一文带你搞定Matplotlib 绘图 -- 知乎](https://zhuanlan.zhihu.com/p/360591534)
- [Matplotlib 核心类与常用函数 -- 博客园](https://www.cnblogs.com/wangya216/p/19268153)

---

**最后更新时间**：2026-06-29
