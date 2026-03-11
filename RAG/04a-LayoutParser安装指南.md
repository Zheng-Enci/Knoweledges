# 04a. LayoutParser 安装指南

## 1. 概述

本文档将指导我们完成 LayoutParser 的安装配置。LayoutParser 是一个功能强大的文档布局分析工具包，支持多种深度学习后端，但我们需要根据实际需求选择合适的安装方式，避免安装不必要的依赖。

## 2. Python 环境准备

LayoutParser 要求 **Python >= 3.6**（推荐 3.7+）。如果尚未安装 Python，请前往[官方网站](https://www.python.org/downloads/)下载安装合适版本。

**验证安装**：

```bash
python --version
```

## 3. LayoutParser 库安装

LayoutParser 采用**模块化设计**，我们可以根据需求选择不同的安装方式：

| 安装命令 | 说明 |
|----------|------|
| `pip install layoutparser` | **基础安装**：包含核心功能（布局数据结构、可视化、数据导入导出） |
| `pip install "layoutparser[effdet]"` | **带 EfficientDet 模型支持**：适合 Windows 用户，安装简单 |
| `pip install "layoutparser[paddledetection]"` | **带 PaddleDetection 模型支持**：百度飞桨后端，中文文档友好 |
| `pip install layoutparser torchvision && pip install "git+https://github.com/facebookresearch/detectron2.git@v0.5#egg=detectron2"` | **带 Detectron2 模型支持**：功能最全，但 Windows 安装复杂 |
| `pip install "layoutparser[ocr]"` | **带 OCR 支持**：添加文字识别功能 |

**推荐安装**（Windows 用户）：

```bash
pip install "layoutparser[effdet]" -i https://pypi.tuna.tsinghua.edu.cn/simple
```

## 4. 深度学习后端详细安装指南

### 4.1 EfficientDet 后端（推荐）

EfficientDet 是 Google 开发的轻量级目标检测模型，**安装最简单**，**Windows 兼容性好**。

**安装命令**：

```bash
pip install "layoutparser[effdet]"
```

**验证安装**：

```python
import layoutparser as lp

# 加载 EfficientDet 模型
model = lp.EfficientDetLayoutModel('lp://PubLayNet/efficientdet_d0')
print("模型加载成功！")
```

### 4.2 PaddleDetection 后端

PaddleDetection 是百度飞桨开发的检测框架，对中文文档支持良好。

**安装命令**：

```bash
pip install "layoutparser[paddledetection]"
```

### 4.3 Detectron2 后端

Detectron2 是 Meta（Facebook）开发的检测框架，**功能最全但安装复杂**。

#### Mac OS 和 Linux 用户

```bash
pip install layoutparser torchvision && pip install "detectron2@git+https://github.com/facebookresearch/detectron2.git@v0.5#egg=detectron2"
```

安装过程需要**编译**，耗时较长。如遇问题，请参考[Detectron2 官方安装文档](https://github.com/facebookresearch/detectron2/blob/master/INSTALL.md)。

#### Windows 用户

**⚠️ 重要提示**：Detectron2 **不提供 Windows 官方支持**，安装过程可能遇到以下问题：

| 问题 | 解决方案 |
|------|----------|
| `pycocotools` 安装失败 | 1. 参考[这篇教程](https://changhsinlee.com/pycocotools/)<br>2. 或尝试 `pip install pycocotools-windows` |
| Detectron2 编译错误 | 参考[Detectron2 Windows 安装指南](https://ivanpp.cc/detectron2-walkthrough-windows/) |

**建议**：Windows 用户优先使用 **EfficientDet** 或 **PaddleDetection** 后端。

## 5. OCR 功能安装

如果需要文字识别功能，需额外安装 OCR 模块：

```bash
pip install "layoutparser[ocr]"
```

**使用 Tesseract-OCR 引擎**：

LayoutParser 支持 Tesseract 作为 OCR 后端，需单独安装：

1. 下载安装 [Tesseract-OCR](https://tesseract-ocr.github.io/tessdoc/Installation.html)
2. 将安装路径添加到系统 PATH
3. 验证安装：`tesseract --version`

## 6. 常见问题

### 6.1 Google Cloud Vision API 版本错误

**错误信息**：`module 'google.cloud.vision' has no attribute 'types'`

**解决方案**：

```bash
pip install -U "layoutparser[ocr]"
```

### 6.2 模型下载缓慢或失败

**解决方案**：设置国内镜像源

```bash
pip install "layoutparser[effdet]" -i https://pypi.tuna.tsinghua.edu.cn/simple
```

### 6.3 显卡/GPU 支持

LayoutParser 默认使用 CPU 推理。如需 GPU 加速，请确保：

1. 安装 CUDA 和 cuDNN
2. 安装对应版本的 PyTorch/PaddlePaddle（带 GPU 支持）

## 7. 安装验证

完成安装后，运行以下代码验证：

```python
import layoutparser as lp

# 检查版本
print(f"LayoutParser 版本: {lp.__version__}")

# 测试模型加载（以 EfficientDet 为例）
model = lp.EfficientDetLayoutModel('lp://PubLayNet/efficientdet_d0')
print("模型加载成功！")
```

## 8. 总结

| 用户类型 | 推荐安装命令 | 说明 |
|----------|--------------|------|
| **Windows 用户** | `pip install "layoutparser[effdet]"` | 安装简单，功能完整 |
| **Linux/Mac 用户** | `pip install "layoutparser[effdet]"` 或 Detectron2 版本 | 根据需求选择 |
| **需要 OCR** | 额外安装 `pip install "layoutparser[ocr]"` | 添加文字识别功能 |

**下一步**：安装完成后，请参考《04. 智能文档解析技术》学习如何使用 LayoutParser 进行文档布局分析。
