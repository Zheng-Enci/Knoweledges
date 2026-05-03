# 03ab-PyTorch安装教程 📚

## 章节阅读路线图 🗺️

```mermaid
flowchart LR
    A["1. 概述"]:::concept --> B["2. 安装前准备"]:::setup
    B --> C["3. CPU版本安装"]:::cpu
    C --> D["4. GPU版本安装"]:::gpu
    D --> E["5. 验证安装"]:::verify

    classDef concept fill:#e3f2fd,stroke:#1565c0
    classDef setup fill:#f3e5f5,stroke:#6a1b9a
    classDef cpu fill:#e8f5e9,stroke:#2e7d32
    classDef gpu fill:#fff3e0,stroke:#ef6c00
    classDef verify fill:#fce4ec,stroke:#c62828
```

**阅读顺序说明**：

- **第1章 → 第2章**：先了解PyTorch是什么以及安装前需要准备什么
- **第2章 → 第3章**：准备好环境后，根据需求选择CPU或GPU版本
- **第3章 → 第4章**：CPU版本简单，GPU版本需要额外配置CUDA
- **第4章 → 第5章**：装完必须验证是否正常工作

## 1. 概述 📝

PyTorch是一个由Facebook开发的开源深度学习框架，从2016年发布至今已经成为学术界和工业界最受欢迎的深度学习工具之一。相比TensorFlow，PyTorch的最大特点是**动态计算图**，这意味着你可以在代码运行时随时改变网络结构，调试起来非常方便。

我们这个系列主要学习Transformer，而Transformer的代码实现离不开PyTorch。接下来的几节，我会手把手教你把PyTorch环境搭好。

## 2. 安装前准备 ⚙️

在安装PyTorch之前，我们需要先确认两件事：你有没有NVIDIA显卡、你用的是什么包管理工具。

### 2.1 检查NVIDIA显卡 🔍

打开命令提示符，输入以下命令：

```bash
nvidia-smi
```

如果你的电脑有NVIDIA显卡，会看到类似这样的输出：

```
+-----------------------------------------------------------------------------------------+
| NVIDIA-SMI 572.83                 Driver Version: 572.83         CUDA Version: 12.8     |
|-----------------------------------------+------------------------+----------------------+
| GPU  Name                  Driver-Model | Bus-Id          Disp.A | Volatile Uncorr. ECC |
|=========================================+========================+======================|
|   0  NVIDIA GeForce RTX 4060 ...  WDDM  |   00000000:01:00.0 Off |                  N/A |
+-----------------------------------------------------------------------------------------+
```

🔴 **注意**：如果你看到"CUDA Version: 12.8"，说明你的显卡驱动支持CUDA 12.8。安装PyTorch时，CUDA版本不能超过这个数字。

如果你没有看到任何NVIDIA相关输出，说明你的电脑没有NVIDIA显卡，只能安装CPU版本。

### 2.2 选择包管理工具 📦

Windows上常用的Python包管理工具主要有两种：

**pip**（推荐新手）：Python官方的包管理器，简单直接，安装命令一学就会。

**conda**：Anaconda自带的包管理器，功能强大，但需要额外学习环境管理命令，新手可以先跳过。

新手先用pip把PyTorch装上，跑通代码后再学conda也不迟。

## 3. CPU版本安装 💻

CPU版本安装最简单，适合没有NVIDIA显卡的同学，或者只是跑一些小模型练手。

### 3.1 检查Python版本 🐍

PyTorch要求Python版本在3.9以上。打开命令提示符检查：

```bash
python --version
```

如果版本低于3.9，需要先升级Python。建议安装Python 3.10或3.11。

### 3.2 安装PyTorch 🔧

**使用pip安装**（推荐）：

```bash
# CPU版本
pip install torch==2.10.0 torchvision==0.25.0 torchaudio==2.10.0 --index-url https://download.pytorch.org/whl/cpu
```

💡 **提示**：具体的pip安装命令，请前往[PyTorch官方历史版本页面](https://pytorch.org/get-started/previous-versions/)查找，页面上会根据你的需求提供对应的命令。

如果网络比较慢，可以使用国内镜像加速：

```bash
pip install torch==2.10.0 torchvision==0.25.0 torchaudio==2.10.0 -i https://pypi.tuna.tsinghua.edu.cn/simple
```

如果镜像速度也不行，可以参考[03aa-PyTorch迅雷加速下载小妙招](https://juejin.cn/post/7559781687904747556)（[CSDN版](https://blog.csdn.net/2301_79239314/article/details/160743376)），用迅雷下载.whl文件本地安装。

## 4. GPU版本安装 🔧

GPU版本可以加速深度学习训练，比CPU快几十倍不止。**只有NVIDIA显卡才能使用GPU版本**，如果你没有NVIDIA显卡，请跳过这节，直接看第五章验证安装。

### 4.1 安装CUDA Toolkit 🔧

首先用nvidia-smi查看你的显卡驱动支持什么版本的CUDA。

**下载地址**：https://developer.nvidia.com/cuda-downloads

下载对应版本后，打开下载页面，按以下选择（以**Windows 11 x86_64**为例）：

- **Operating System**：Windows
- **Architecture**：x86_64（64位系统）
- **Version**：Windows 11（根据你的系统选择）
- **Installer Type**：推荐选**exe (local)**（本地安装包，包含所有组件）

然后点击Download下载。下载完后双击安装包，按照提示一路下一步即可。安装完成后，打开命令提示符验证：

```bash
nvcc -V
```

看到类似输出就说明安装成功：

```
nvcc: NVIDIA (R) Cuda compiler driver
Copyright (c) 2005-2026 NVIDIA Corporation
Built on Thu_Mar_19_22:28:55_Pacific_Daylight_Time_2026
Cuda compilation tools, release 13.2, V13.2.78
Build cuda_13.2.r13.2/compiler.37668154_0
```

### 4.2 安装PyTorch GPU版本 🚀

根据你的CUDA版本选择安装命令：

```bash
# CUDA 12.6
pip install torch==2.10.0 torchvision==0.25.0 torchaudio==2.10.0 --index-url https://download.pytorch.org/whl/cu126
```

💡 **提示**：具体的pip安装命令，请前往[PyTorch官方历史版本页面](https://pytorch.org/get-started/previous-versions/)查找，页面上会根据你的CUDA版本提供对应的命令。

### 4.3 安装cuDNN（可选）📚

cuDNN是NVIDIA提供的深度学习加速库，安装它可以让PyTorch运行得更快。

**下载地址**：https://developer.nvidia.com/cudnn

点击Download，选择对应CUDA版本的cuDNN，下载后双击安装即可。这步不是必须的，但有的话会更好。

## 5. 验证安装 ✅

不管你安装的是CPU还是GPU版本，都需要验证一下是否正常工作。

### 5.1 基础验证 🧪

进入Python环境，输入以下代码：

```python
import torch

# 打印PyTorch版本
print(f"PyTorch版本: {torch.__version__}")

# 检查CUDA是否可用
print(f"CUDA是否可用: {torch.cuda.is_available()}")

# 创建一个随机张量测试
x = torch.rand(5, 3)
print("随机张量测试:")
print(x)
```

如果输出正常，说明PyTorch已经安装成功。

### 5.2 GPU验证 🔍

如果你安装的是GPU版本，还需要额外验证：

```python
import torch

print(f"CUDA是否可用: {torch.cuda.is_available()}")
print(f"当前设备: {torch.cuda.current_device()}")
print(f"设备名称: {torch.cuda.get_device_name(0)}")
print(f"CUDA版本: {torch.version.cuda}")
```

如果`torch.cuda.is_available()`返回True，说明GPU已经可以用了。

### 5.3 简单加速测试 ⚡

最后跑个小测试，感受一下GPU的速度：

```python
import torch
import time

# 创建两个大矩阵
size = 10000
a = torch.rand(size, size)
b = torch.rand(size, size)

# CPU计算
start = time.time()
c_cpu = torch.matmul(a, b)
print(f"CPU耗时: {time.time() - start:.4f}秒")

# GPU计算（如果有）
if torch.cuda.is_available():
    a = a.cuda()
    b = b.cuda()
    start = time.time()
    c_gpu = torch.matmul(a, b)
    print(f"GPU耗时: {time.time() - start:.4f}秒")
```

GPU矩阵乘法通常比CPU快几十倍，这就是深度学习离不开GPU的原因。

---

**最后更新时间：2026-05-03**

**参考资料**：
- [PyTorch官方历史版本安装页面 -- PyTorch](https://pytorch.org/get-started/previous-versions/)
- [PyTorch官方Windows安装指南 -- GitHub](https://github.com/pytorch/pytorch.github.io/blob/master/get_started/installation/windows.md)
- [PyTorch 2025保姆级安装教程 -- CSDN](https://blog.csdn.net/2401_82355416/article/details/148203144)
- [2025年Windows最新Pytorch安装教程 -- CSDN](https://blog.csdn.net/2302_80370282/article/details/148084414)
