"""
01d-前馈神经网络代码实现 - 第6章：完整可运行示例

本章代码整合所有内容，提供一个可直接运行的完整示例
包含：感知机、前馈神经网络、激活函数可视化、训练过程可视化
"""

import torch
import torch.nn as nn
import torch.optim as optim
import matplotlib.pyplot as plt

class Perceptron(nn.Module):
    """单层感知机：输入 → 输出（无隐藏层）"""
    def __init__(self, input_size: int) -> None:
        super(Perceptron, self).__init__()
        self.linear = nn.Linear(input_size, 1)
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.linear(x)
        x = self.sigmoid(x)
        return x

class FeedforwardNN(nn.Module):
    """前馈神经网络：输入 → 隐藏 → 输出"""
    def __init__(self, input_size: int = 2, hidden_size: int = 4, output_size: int = 1) -> None:
        super(FeedforwardNN, self).__init__()
        self.fc1 = nn.Linear(input_size, hidden_size)
        self.relu = nn.ReLU()
        self.fc2 = nn.Linear(hidden_size, output_size)
        self.sigmoid = nn.Sigmoid()
    
    def forward(self, x: torch.Tensor) -> torch.Tensor:
        x = self.fc1(x)
        x = self.relu(x)
        x = self.fc2(x)
        x = self.sigmoid(x)
        return x

def train_perceptron_logic_gates():
    """训练感知机解决 AND/OR 逻辑门"""
    print("=== 感知机解决线性可分问题 ===")
    
    # 数据集
    X_logic = torch.tensor([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=torch.float32)
    y_and = torch.tensor([[0], [0], [0], [1]], dtype=torch.float32)
    y_or = torch.tensor([[0], [1], [1], [1]], dtype=torch.float32)
    y_xor = torch.tensor([[0], [1], [1], [0]], dtype=torch.float32)

    # 训练 AND
    model_and = Perceptron(input_size=2)
    criterion = nn.BCELoss()
    optimizer = optim.SGD(model_and.parameters(), lr=0.1)
    
    for epoch in range(1000):
        outputs = model_and(X_logic)
        loss = criterion(outputs, y_and)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    
    # 训练 OR
    model_or = Perceptron(input_size=2)
    optimizer = optim.SGD(model_or.parameters(), lr=0.1)
    
    for epoch in range(1000):
        outputs = model_or(X_logic)
        loss = criterion(outputs, y_or)
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
    
    # 测试
    with torch.no_grad():
        # AND
        pred_and = (model_and(X_logic) > 0.5).float()
        acc_and = (pred_and == y_and).float().mean()
        
        # OR
        pred_or = (model_or(X_logic) > 0.5).float()
        acc_or = (pred_or == y_or).float().mean()
        
        # XOR（尝试）
        model_xor = Perceptron(input_size=2)
        pred_xor = (model_xor(X_logic) > 0.5).float()
        acc_xor = (pred_xor == y_xor).float().mean()
        
        print(f"AND 准确率: {acc_and.item():.1%}")
        print(f"OR  准确率: {acc_or.item():.1%}")
        print(f"XOR 准确率: {acc_xor.item():.1%} (随机猜测)")
    
    return model_and, model_or

def train_feedforward_xor():
    """训练前馈神经网络解决 XOR 问题"""
    print("\n=== 前馈神经网络解决 XOR 问题 ===")
    
    # XOR 数据集
    X = torch.tensor([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=torch.float32)
    y = torch.tensor([[0], [1], [1], [0]], dtype=torch.float32)

    # 创建模型
    model = FeedforwardNN(input_size=2, hidden_size=4, output_size=1)
    criterion = nn.BCELoss()
    optimizer = optim.Adam(model.parameters(), lr=0.1)

    # 训练
    loss_history = []
    for epoch in range(2000):
        outputs = model(X)
        loss = criterion(outputs, y)
        loss_history.append(loss.item())
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()
        
        if (epoch + 1) % 500 == 0:
            print(f'Epoch [{epoch+1}/2000], Loss: {loss.item():.4f}')

    # 测试
    with torch.no_grad():
        predicted = (model(X) > 0.5).float()
        accuracy = (predicted == y).float().mean()
        print(f'XOR 准确率: {accuracy.item():.1%}')
    
    return model, loss_history

def visualize_training_process(loss_history):
    """可视化训练过程"""
    plt.figure(figsize=(10, 4))
    
    plt.subplot(1, 2, 1)
    plt.plot(loss_history, color='#FF5722', linewidth=2)
    plt.xlabel('训练轮次')
    plt.ylabel('损失值')
    plt.title('训练损失曲线')
    plt.grid(True, alpha=0.3)
    
    plt.subplot(1, 2, 2)
    plt.semilogy(loss_history, color='#2196F3', linewidth=2)
    plt.xlabel('训练轮次')
    plt.ylabel('损失值 (对数尺度)')
    plt.title('对数尺度损失曲线')
    plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('01d_chapter6_training_process.png', dpi=150, bbox_inches='tight')
    print("Image saved as 01d_chapter6_training_process.png")
    plt.show()

def visualize_activation_functions():
    """快速可视化激活函数"""
    x = torch.linspace(-3, 3, 100)
    
    plt.figure(figsize=(12, 3))
    
    functions = [
        ('Sigmoid', torch.sigmoid, '#2196F3'),
        ('Tanh', torch.tanh, '#4CAF50'),
        ('ReLU', torch.relu, '#FF5722')
    ]
    
    for i, (name, func, color) in enumerate(functions):
        plt.subplot(1, 3, i+1)
        plt.plot(x.numpy(), func(x).numpy(), color=color, linewidth=2)
        plt.title(name)
        plt.xlabel('x')
        plt.ylabel('f(x)')
        plt.grid(True, alpha=0.3)
    
    plt.tight_layout()
    plt.savefig('01d_chapter6_activation_functions.png', dpi=150, bbox_inches='tight')
    print("Image saved as 01d_chapter6_activation_functions.png")

if __name__ == "__main__":
    print("01d-前馈神经网络代码实现 - 第6章：完整可运行示例")
    print("=" * 70)
    
    # 设置中文显示
    plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
    plt.rcParams['axes.unicode_minus'] = False
    
    torch.manual_seed(42)  # 固定随机种子
    
    # 1. 感知机演示
    model_and, model_or = train_perceptron_logic_gates()
    
    # 2. 前馈神经网络演示
    model_fnn, loss_history = train_feedforward_xor()
    
    # 3. 可视化
    visualize_training_process(loss_history)
    visualize_activation_functions()
    
    print("\n" + "=" * 70)
    print("🎉 完整示例运行完成！")
    print("💡 关键结论:")
    print("  • 感知机能解决 AND/OR（线性可分）")
    print("  • 感知机无法解决 XOR（线性不可分）")
    print("  • 前馈神经网络（隐藏层+激活函数）能解决 XOR")
    print("  • 激活函数提供非线性，让网络真正\"深\"起来")
    print("=" * 70)