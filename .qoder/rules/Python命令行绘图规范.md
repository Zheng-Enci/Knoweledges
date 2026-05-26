---
trigger: manual
alwaysApply: false
---
# Python 命令行绘图规范

## 1. 执行方式

**只能通过命令行执行 Python 代码绘图，禁止修改任何项目文件。**

使用 `python -c` 内联方式执行：

```powershell
python -c @"
import matplotlib.pyplot as plt
import numpy as np
# ... 绘图代码 ...
plt.savefig('目标路径/图片名.png', dpi=150, bbox_inches='tight')
"@
```

**禁止**：
- 创建或修改 `.py` 脚本文件保存到项目目录
- 修改任何已存在的项目文档
- 在文档内嵌入 Python 绘图代码块

> 💡 如果遇到 `ModuleNotFoundError: No module named 'matplotlib'`，先用 `pip install matplotlib` 安装依赖。

## 2. 图片保存位置

图片必须保存到对应的知识文件夹中，不能留在项目根目录：

| 文档所属专题 | 图片保存路径 |
|-------------|-------------|
| Transformer | `Knowledges/Transformer/` |
| Java 系列 | `Knowledges/Java-基础技术/` 等对应文件夹 |
| Python 系列 | `Knowledges/Python-基础技术/` 等对应文件夹 |

## 3. 图片命名规范

### 3.1 命名规则

图片名使用全英文、snake_case（蛇形命名），**禁止使用中文**。

格式：`{文档编号}_{描述性英文名称}.png`

### 3.2 命名模式

**模式一：章节专属图片**（文中某章节的可视化）

```
{文档编号}_chapter{章节号}_{描述}.png
```

示例：
- `01d_chapter5_activation_functions.png` — 01d 文档第5章的激活函数图
- `01d_chapter6_training_process.png` — 01d 文档第6章的训练过程图
- `05_chapter6_visualization.png` — 05 文档第6章的可视化
- `07_chapter5_pe_heatmap.png` — 07 文档第5章的位置编码热力图
- `07_chapter5_pe_waveforms.png` — 07 文档第5章的位置编码波形图

**模式二：专题概念图片**（独立的概念说明图）

```
{文档编号}_{核心概念英文描述}.png
```

示例：
- `01d_xor_data_points.png` — 01d 文档的 XOR 数据点图
- `01d_xor_solution.png` — 01d 文档的 XOR 解空间图
- `09aa_bias_vertical_shift.png` — 09aa 文档的偏置平移效果图
- `07_positional_encoding_wave_overlay.png` — 07 文档的位置编码波形叠加图

### 3.3 规则总结

| 规则项 | 要求 | 示例 |
|-------|------|------|
| **语言** | 全英文 | `bias_vertical_shift` ✅，`偏置效果` ❌ |
| **分隔符** | 下划线 `_` | `activation_functions` ✅，`activation-functions` ❌ |
| **文档编号前缀** | 必须有（数字+可选字母） | `09aa_`、`01d_`、`05_` ✅ |
| **章节号** | 章节专属图加 `chapter{数字}_` | `chapter5_` ✅ |
| **描述** | 统一用名词短语，勿用动词句式 | `pe_heatmap` ✅，`showing_pe` ❌ |
| **后缀** | `.png`，分辨率 ≥ 150 DPI | `.png` ✅ |

## 4. DPI 和质量

- 图片分辨率至少 150 DPI
- 使用 `plt.savefig(路径, dpi=150, bbox_inches='tight')`
- 若需中文显示，必须设置中文字体：

```python
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
```

## 5. 图片创建后

1. 图片创建后自动提交 git（add + commit）
2. 文档中引用该图片时，必须使用 GitCode Raw URL 格式（参见 `GitCode图片URL转换规范.md`）
