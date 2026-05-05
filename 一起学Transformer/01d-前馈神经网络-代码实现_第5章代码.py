"""
01d-前馈神经网络代码实现 - 第5章：激活函数可视化

本章代码可视化对比三种常用激活函数：Sigmoid、Tanh、ReLU
"""

import torch
import matplotlib.pyplot as plt
import numpy as np
from typing import Tuple

def visualize_activation_functions() -> None:
    """可视化三种常用激活函数"""
    print("=== 激活函数可视化对比 ===")
    
    # 设置 Matplotlib 支持中文显示
    plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False

    # 生成 x 轴数据：-5 到 5，200个点
    x: torch.Tensor = torch.linspace(-5, 5, 200)

    # 计算三种激活函数的输出
    y_sigmoid: torch.Tensor = torch.sigmoid(x)
    y_tanh: torch.Tensor = torch.tanh(x)
    y_relu: torch.Tensor = torch.relu(x)

    # 绘图
    fig, axes = plt.subplots(1, 3, figsize=(15, 4))

    # Sigmoid
    axes[0].plot(x.numpy(), y_sigmoid.numpy(), color='#2196F3', linewidth=2)
    axes[0].axhline(y=0, color='gray', linestyle='--', linewidth=0.5)
    axes[0].axhline(y=1, color='gray', linestyle='--', linewidth=0.5)
    axes[0].set_title('Sigmoid\nσ(x) = 1/(1+e⁻ˣ)', fontsize=12)
    axes[0].set_xlabel('x')
    axes[0].set_ylabel('σ(x)')
    axes[0].set_ylim(-0.1, 1.1)
    axes[0].grid(True, alpha=0.3)
    axes[0].text(2, 0.15, '输出范围: (0, 1)', fontsize=9, color='#666')

    # Tanh
    axes[1].plot(x.numpy(), y_tanh.numpy(), color='#4CAF50', linewidth=2)
    axes[1].axhline(y=0, color='gray', linestyle='--', linewidth=0.5)
    axes[1].axhline(y=1, color='gray', linestyle='--', linewidth=0.5)
    axes[1].axhline(y=-1, color='gray', linestyle='--', linewidth=0.5)
    axes[1].set_title('Tanh\ntanh(x) = (eˣ-e⁻ˣ)/(eˣ+e⁻ˣ)', fontsize=12)
    axes[1].set_xlabel('x')
    axes[1].set_ylabel('tanh(x)')
    axes[1].set_ylim(-1.1, 1.1)
    axes[1].grid(True, alpha=0.3)
    axes[1].text(2, -0.7, '输出范围: (-1, 1)', fontsize=9, color='#666')

    # ReLU
    axes[2].plot(x.numpy(), y_relu.numpy(), color='#FF5722', linewidth=2)
    axes[2].axhline(y=0, color='gray', linestyle='--', linewidth=0.5)
    axes[2].set_title('ReLU\nReLU(x) = max(0, x)', fontsize=12)
    axes[2].set_xlabel('x')
    axes[2].set_ylabel('ReLU(x)')
    axes[2].set_ylim(-0.5, 5.5)
    axes[2].grid(True, alpha=0.3)
    axes[2].text(2, 0.5, '输出范围: [0, +∞)', fontsize=9, color='#666')

    plt.suptitle('三种常用激活函数对比', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('activation_functions.png', dpi=150, bbox_inches='tight')
    print("✅ 激活函数对比图已保存为 activation_functions.png")
    plt.show()

def compare_activation_characteristics():
    """对比激活函数特性"""
    print("\n=== 激活函数特性对比 ===")
    
    # 测试数据
    test_inputs = torch.tensor([-2.0, -1.0, 0.0, 1.0, 2.0])
    
    print("输入值: ", test_inputs.tolist())
    print("\n各激活函数输出:")
    
    # Sigmoid
    sigmoid_outputs = torch.sigmoid(test_inputs)
    print(f"Sigmoid: {[f'{v:.4f}' for v in sigmoid_outputs.tolist()]}")
    
    # Tanh
    tanh_outputs = torch.tanh(test_inputs)
    print(f"Tanh:    {[f'{v:.4f}' for v in tanh_outputs.tolist()]}")
    
    # ReLU
    relu_outputs = torch.relu(test_inputs)
    print(f"ReLU:    {[f'{v:.4f}' for v in relu_outputs.tolist()]}")
    
    print("\n💡 特性总结:")
    print("  • Sigmoid: 输出范围(0,1)，适合二分类输出层")
    print("  • Tanh:    输出范围(-1,1)，零中心化，适合RNN/LSTM")
    print("  • ReLU:    计算快，缓解梯度消失，隐藏层首选")

def demonstrate_gradient_behavior():
    """演示激活函数的梯度行为"""
    print("\n=== 激活函数梯度行为演示 ===")
    
    # 创建需要梯度的张量
    x = torch.tensor([-2.0, -1.0, 0.0, 1.0, 2.0], requires_grad=True)
    
    # 测试 Sigmoid 梯度
    y_sigmoid = torch.sigmoid(x)
    y_sigmoid.sum().backward()
    print(f"Sigmoid 在 {x.detach().tolist()} 的梯度: {[f'{g:.4f}' for g in x.grad.tolist()]}")
    
    # 重置梯度
    x.grad = None
    
    # 测试 ReLU 梯度
    y_relu = torch.relu(x)
    y_relu.sum().backward()
    print(f"ReLU    在 {x.detach().tolist()} 的梯度: {[f'{g:.4f}' for g in x.grad.tolist()]}")
    
    print("\n💡 梯度观察:")
    print("  • Sigmoid: 梯度在两端接近0，可能导致梯度消失")
    print("  • ReLU:    负值梯度为0，正值梯度为1，缓解梯度消失")

if __name__ == "__main__":
    print("01d-前馈神经网络代码实现 - 第5章：激活函数可视化")
    print("=" * 60)
    
    # 可视化激活函数
    visualize_activation_functions()
    
    # 对比特性
    compare_activation_characteristics()
    
    # 演示梯度行为
    demonstrate_gradient_behavior()
    
    print("\n✅ 激活函数可视化完成！")