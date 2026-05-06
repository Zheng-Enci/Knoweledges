"""
01d-前馈神经网络代码实现 - 第4章：前馈神经网络解决 XOR

本章代码演示如何用前馈神经网络（隐藏层+激活函数）解决 XOR 问题
"""

import torch
import torch.nn as nn
import torch.optim as optim
from typing import Tuple, List

class FeedforwardNN(nn.Module):
    """
    前馈神经网络实现
    
    结构：输入层(2) → 隐藏层(4, ReLU) → 输出层(1, Sigmoid)
    
    参数:
        input_size: 输入维度
        hidden_size: 隐藏层神经元数量
        output_size: 输出维度
    """
    def __init__(self, input_size: int = 2, hidden_size: int = 4, output_size: int = 1) -> None:
        super(FeedforwardNN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)   # 输入 → 隐藏
        self.relu = nn.ReLU()                            # 非线性激活
        self.fc2 = nn.Linear(hidden_size, output_size)   # 隐藏 → 输出
        self.sigmoid = nn.Sigmoid()                      # 输出概率
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.fc1(x)       # 线性变换：2 → 4
        x = self.relu(x)      # 非线性激活
        x = self.fc2(x)       # 线性变换：4 → 1
        x = self.sigmoid(x)   # 输出 0~1 概率
        return x

def train_feedforward_nn() -> Tuple[FeedforwardNN, List[float]]:
    """训练前馈神经网络解决 XOR 问题"""
    print("=== 训练前馈神经网络解决 XOR 问题 ===")
    
    # XOR 数据集
    X: torch.Tensor = torch.tensor([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=torch.float32)
    y: torch.Tensor = torch.tensor([[0], [1], [1], [0]], dtype=torch.float32)

    # 创建模型
    model: FeedforwardNN = FeedforwardNN(input_size=2, hidden_size=4, output_size=1)
    
    # 打印模型结构
    print("模型结构:")
    print(f"  输入层: {2} 个神经元")
    print(f"  隐藏层: {4} 个神经元 (ReLU激活)")
    print(f"  输出层: {1} 个神经元 (Sigmoid激活)")
    print(f"  总参数: {sum(p.numel() for p in model.parameters())} 个")

    # 损失函数：二元交叉熵
    criterion: nn.BCELoss = nn.BCELoss()
    # 优化器：Adam（自适应学习率，收敛更快）
    optimizer: optim.Adam = optim.Adam(model.parameters(), lr=0.1)

    # 记录训练过程
    loss_history: List[float] = []

    # 训练
    num_epochs: int = 2000
    for epoch in range(num_epochs):
        # 1. 前向传播：计算预测值
        outputs: torch.Tensor = model(X)
        loss: torch.Tensor = criterion(outputs, y)
        loss_history.append(loss.item())
        
        # 2. 反向传播：计算梯度
        optimizer.zero_grad()   # 清零上一步的梯度
        loss.backward()         # 自动计算所有参数的梯度
        
        # 3. 更新参数
        optimizer.step()        # 根据梯度更新权重
        
        if (epoch + 1) % 400 == 0:
            print(f'Epoch [{epoch+1}/{num_epochs}], Loss: {loss.item():.4f}')

    # 测试
    with torch.no_grad():
        predicted: torch.Tensor = model(X)
        predicted_class: torch.Tensor = (predicted > 0.5).float()
        print(f'\nXOR 预测结果: {predicted_class.flatten().tolist()}')
        print(f'XOR 真实标签: {y.flatten().tolist()}')
        print(f'预测概率:    {[f"{p:.4f}" for p in predicted.flatten().tolist()]}')
        
        # 计算准确率
        correct: torch.Tensor = (predicted_class == y).float().sum()
        accuracy: torch.Tensor = correct / len(y)
        print(f'准确率: {accuracy.item():.1%}')
    
    return model, loss_history

def analyze_network_behavior(model):
    """分析网络内部行为"""
    print("\n=== 网络内部行为分析 ===")
    
    X = torch.tensor([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=torch.float32)
    
    with torch.no_grad():
        # 获取隐藏层输出
        hidden_output = model.relu(model.fc1(X))
        final_output = model(X)
        
        print("隐藏层输出 (ReLU激活后):")
        for i, (input_point, hidden_vec) in enumerate(zip(X, hidden_output)):
            print(f"  输入 {input_point.tolist()} → 隐藏层 {[f'{h:.3f}' for h in hidden_vec.tolist()]}")
        
        print("\n最终输出 (Sigmoid激活后):")
        for i, (input_point, output_prob) in enumerate(zip(X, final_output)):
            print(f"  输入 {input_point.tolist()} → 输出概率: {output_prob.item():.4f}")

if __name__ == "__main__":
    print("01d-前馈神经网络代码实现 - 第4章：前馈神经网络解决 XOR")
    print("=" * 60)
    
    # 训练前馈神经网络
    model, loss_history = train_feedforward_nn()
    
    # 分析网络内部行为
    analyze_network_behavior(model)
    
    print("\n✅ 前馈神经网络成功解决了 XOR 问题！")
    print("💡 关键改进：隐藏层 + 非线性激活函数 = 突破线性不可分性")