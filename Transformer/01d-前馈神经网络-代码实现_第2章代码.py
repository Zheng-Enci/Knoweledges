"""
01d-前馈神经网络代码实现 - 第2章：感知机实现

本章代码演示感知机如何解决线性可分问题（AND、OR逻辑门）

核心概念：
- 感知机是神经网络的最简形式，只有输入层和输出层
- 使用Sigmoid激活函数将输出映射到(0,1)区间，适合二分类
- 能够解决线性可分问题（如AND、OR逻辑门）
- 无法解决线性不可分问题（如XOR逻辑门）

文件结构：
- Perceptron类：单层感知机模型定义
- train_perceptron_and()：训练感知机解决AND问题
- train_perceptron_or()：训练感知机解决OR问题
"""

import torch
import torch.nn as nn
import torch.optim as optim


class Perceptron(nn.Module):
    """
    单层感知机实现
    
    结构：输入层 → 输出层（无隐藏层）
    激活函数：Sigmoid（输出0~1之间的概率）
    
    参数:
        input_size: 输入特征的维度
    
    属性:
        linear: 线性层，执行Wx+b变换
        sigmoid: Sigmoid激活函数，将输出映射到(0,1)
    
    前向传播流程:
        输入x → 线性变换 → Sigmoid激活 → 输出概率
    """
    def __init__(self, input_size: int) -> None:
        """
        初始化感知机
        
        参数:
            input_size: 输入特征的维度
        """
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

def train_perceptron_and() -> Perceptron:
    """
    训练感知机解决 AND 逻辑门问题
    
    AND逻辑门真值表:
        输入A | 输入B | 输出
        ------|------|-----
          0   |   0  |   0
          0   |   1  |   0
          1   |   0  |   0
          1   |   1  |   1
    
    AND问题是线性可分的，可以用一条直线完美分割
    
    返回:
        训练好的感知机模型
    """
    print("=== 训练感知机解决 AND 问题 ===")
    
    # AND 数据集：4个样本，每个样本2个特征
    X_and: torch.Tensor = torch.tensor([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=torch.float32)
    y_and: torch.Tensor = torch.tensor([[0], [0], [0], [1]], dtype=torch.float32)

    # 创建感知机：输入维度为2（两个输入特征A和B）
    model_and: Perceptron = Perceptron(input_size=2)

    # 损失函数：二元交叉熵，适合二分类问题
    criterion: nn.BCELoss = nn.BCELoss()
    # 优化器：随机梯度下降，学习率0.1
    optimizer: optim.SGD = optim.SGD(model_and.parameters(), lr=0.1)

    # 训练循环：1000轮迭代
    for epoch in range(1000):
        # 前向传播：计算模型预测值
        outputs: torch.Tensor = model_and(X_and)
        # 计算损失：预测值与真实标签的差异
        loss: torch.Tensor = criterion(outputs, y_and)
        
        # 反向传播：计算梯度
        optimizer.zero_grad()  # 清零梯度，避免累积
        loss.backward()        # 反向传播计算梯度
        optimizer.step()       # 根据梯度更新参数
        
        # 每200轮打印一次损失值
        if (epoch + 1) % 200 == 0:
            print(f'Epoch [{epoch+1}/1000], Loss: {loss.item():.4f}')

    # 测试阶段：关闭梯度计算以提高效率
    with torch.no_grad():
        # 获取模型预测概率
        predicted: torch.Tensor = model_and(X_and)
        # 将概率转换为类别（>0.5为正类）
        predicted_class: torch.Tensor = (predicted > 0.5).float()
        print(f'AND 预测结果: {predicted_class.flatten().tolist()}')
        print(f'AND 真实标签: {y_and.flatten().tolist()}')
    
    return model_and

def train_perceptron_or() -> Perceptron:
    """训练感知机解决 OR 问题"""
    print("\n=== 训练感知机解决 OR 问题 ===")
    
    # OR 数据集
    X_or: torch.Tensor = torch.tensor([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=torch.float32)
    y_or: torch.Tensor = torch.tensor([[0], [1], [1], [1]], dtype=torch.float32)

    model_or: Perceptron = Perceptron(input_size=2)
    criterion: nn.BCELoss = nn.BCELoss()
    optimizer: optim.SGD = optim.SGD(model_or.parameters(), lr=0.1)

    for epoch in range(1000):
        outputs: torch.Tensor = model_or(X_or)
        loss: torch.Tensor = criterion(outputs, y_or)
        
        optimizer.zero_grad()
        loss.backward()
        optimizer.step()

    with torch.no_grad():
        predicted: torch.Tensor = model_or(X_or)
        predicted_class: torch.Tensor = (predicted > 0.5).float()
        print(f'OR 预测结果: {predicted_class.flatten().tolist()}')
        print(f'OR 真实标签: {y_or.flatten().tolist()}')
    
    return model_or

if __name__ == "__main__":
    print("01d-前馈神经网络代码实现 - 第2章：感知机实现")
    print("=" * 50)
    
    # 训练 AND 感知机
    model_and = train_perceptron_and()
    
    # 训练 OR 感知机
    model_or = train_perceptron_or()
    
    print("\n✅ 感知机成功解决了 AND 和 OR 线性可分问题！")