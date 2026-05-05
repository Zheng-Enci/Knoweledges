"""
01d-前馈神经网络代码实现 - 第3章：感知机的局限（XOR问题）

本章代码验证感知机无法解决线性不可分的 XOR 问题

核心概念：
- XOR（异或）问题是线性不可分的经典示例
- 感知机只能解决线性可分问题，无法处理XOR
- 通过训练过程观察损失值不下降，证明感知机的局限性
- 为后续引入前馈神经网络（隐藏层+激活函数）做铺垫

文件结构：
- Perceptron类：单层感知机模型定义（与第2章相同）
- demonstrate_xor_problem()：演示感知机无法解决XOR问题
- visualize_xor_problem()：可视化XOR问题的线性不可分性
"""

import torch
import torch.nn as nn
import torch.optim as optim
from typing import Tuple, List

class Perceptron(nn.Module):
    """
    单层感知机实现
    
    与第2章相同的感知机实现，用于验证XOR问题的局限性
    
    参数:
        input_size: 输入特征的维度
    
    属性:
        linear: 线性层，执行Wx+b变换
        sigmoid: Sigmoid激活函数，将输出映射到(0,1)
    """
    def __init__(self, input_size: int) -> None:
        """初始化感知机"""
        super(Perceptron, self).__init__()
        # 线性层：input_size维输入 → 1维输出
        self.linear = nn.Linear(input_size, 1)
        # Sigmoid激活函数：将输出压缩到(0,1)区间
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        """
        前向传播
        
        参数:
            x: 输入张量，形状为[batch_size, input_size]
        
        返回:
            输出张量，形状为[batch_size, 1]，表示属于正类的概率
        """
        # 线性变换：Wx + b
        x = self.linear(x)
        # 非线性激活：将输出映射到(0,1)区间
        x = self.sigmoid(x)
        return x

def demonstrate_xor_problem() -> Tuple[Perceptron, List[float]]:
    """
    演示感知机无法解决 XOR 问题
    
    XOR逻辑门真值表:
        输入A | 输入B | 输出
        ------|------|-----
          0   |   0  |   0
          0   |   1  |   1
          1   |   0  |   1
          1   |   1  |   0
    
    XOR问题是线性不可分的，无法用单条直线完美分割
    通过训练过程观察损失值不下降，证明感知机的局限性
    
    返回:
        model_xor: 训练后的感知机模型
        losses: 训练过程中的损失值记录
    """
    print("=== 验证感知机无法解决 XOR 问题 ===")
    
    # XOR 数据集：4个样本，每个样本2个特征
    # 注意：XOR的输出模式是(0,1,1,0)，无法用单条直线分割
    X_xor: torch.Tensor = torch.tensor([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=torch.float32)
    y_xor: torch.Tensor = torch.tensor([[0], [1], [1], [0]], dtype=torch.float32)

    # 创建感知机模型
    model_xor: Perceptron = Perceptron(input_size=2)
    # 损失函数：二元交叉熵
    criterion: nn.BCELoss = nn.BCELoss()
    # 优化器：随机梯度下降
    optimizer: optim.SGD = optim.SGD(model_xor.parameters(), lr=0.1)

    # 记录训练过程中的损失值
    losses: List[float] = []
    
    # 训练循环：2000轮迭代（比AND/OR问题更多轮次）
    for epoch in range(2000):
        # 前向传播：计算模型预测
        outputs: torch.Tensor = model_xor(X_xor)
        # 计算损失：预测值与真实标签的差异
        loss: torch.Tensor = criterion(outputs, y_xor)
        # 记录损失值
        losses.append(loss.item())
        
        # 反向传播：计算梯度并更新参数
        optimizer.zero_grad()  # 清零梯度
        loss.backward()        # 反向传播
        optimizer.step()       # 更新参数
        
        # 每500轮打印一次损失值，观察训练进展
        if (epoch + 1) % 500 == 0:
            print(f'Epoch [{epoch+1}/2000], Loss: {loss.item():.4f}')

    # 测试阶段：关闭梯度计算
    with torch.no_grad():
        # 获取模型预测概率
        predicted: torch.Tensor = model_xor(X_xor)
        # 将概率转换为类别（>0.5为正类）
        predicted_class: torch.Tensor = (predicted > 0.5).float()
        
        print(f'XOR 预测结果: {predicted_class.flatten().tolist()}')
        print(f'XOR 真实标签: {y_xor.flatten().tolist()}')
        print(f'最终 Loss: {losses[-1]:.4f}')
        
        # 计算准确率：预测正确的样本比例
        correct: torch.Tensor = (predicted_class == y_xor).float().sum()
        accuracy: torch.Tensor = correct / len(y_xor)
        print(f'准确率: {accuracy.item():.1%}')
    
    return model_xor, losses

def visualize_xor_problem():
    """可视化 XOR 问题的线性不可分性"""
    import matplotlib.pyplot as plt
    import numpy as np
    
    # XOR 数据点
    points = np.array([[0, 0], [0, 1], [1, 0], [1, 1]])
    labels = np.array([0, 1, 1, 0])
    
    plt.figure(figsize=(8, 6))
    
    # 绘制数据点
    colors = ['red' if label == 0 else 'blue' for label in labels]
    for i, (point, color) in enumerate(zip(points, colors)):
        plt.scatter(point[0], point[1], c=color, s=100, alpha=0.7)
        plt.text(point[0] + 0.05, point[1] + 0.05, f'({point[0]},{point[1]})', fontsize=12)
    
    # 尝试画一条直线（任何直线都无法完美分开）
    x = np.linspace(-0.5, 1.5, 100)
    y1 = -x + 0.5  # 尝试的直线1
    y2 = -x + 1.5  # 尝试的直线2
    
    plt.plot(x, y1, 'g--', alpha=0.5, label='尝试的决策边界1')
    plt.plot(x, y2, 'g--', alpha=0.5, label='尝试的决策边界2')
    
    plt.xlim(-0.5, 1.5)
    plt.ylim(-0.5, 1.5)
    plt.xlabel('输入 A')
    plt.ylabel('输入 B')
    plt.title('XOR 问题：线性不可分性演示')
    plt.grid(True, alpha=0.3)
    plt.legend()
    
    # 添加说明文本
    plt.text(0.1, 1.3, '❌ 任何直线都无法完美分开红蓝点', fontsize=10, color='red')
    plt.text(0.1, 1.2, '红色: 输出=0, 蓝色: 输出=1', fontsize=10)
    
    plt.tight_layout()
    plt.savefig('xor_problem_visualization.png', dpi=150, bbox_inches='tight')
    print("\n✅ XOR 问题可视化图已保存为 xor_problem_visualization.png")
    plt.show()

if __name__ == "__main__":
    print("01d-前馈神经网络代码实现 - 第3章：感知机的局限")
    print("=" * 50)
    
    # 验证感知机无法解决 XOR
    model_xor, losses = demonstrate_xor_problem()
    
    # 可视化 XOR 问题
    visualize_xor_problem()
    
    print("\n❌ 感知机无法解决 XOR 问题，需要引入隐藏层和激活函数！")