import torch                                              # 导入 PyTorch 核心库
import torch.nn as nn                                     # 导入神经网络模块
import torch.optim as optim                               # 导入优化器模块

"""比较带偏置和无偏置线性层的训练效果

参数:
    num_epochs: 训练轮数（默认1000）
    
返回:
    无（打印最终损失对比）
    
示例:
    compare_training()
"""
def compare_training(num_epochs=1000):
    # 生成数据：真实规律 y = 2*x + 3（斜率2，截距3）
    # 数据流动：torch.linspace → x_train[100,1]
    x_train = torch.linspace(-1, 1, 100).reshape(-1, 1)   # 创建 100 个等间隔点，形状 [100,1]
    # 数据流动：2*x + 3 + 噪声 → y_train[100,1]
    y_train = 2 * x_train + 3 + 0.1 * torch.randn(100, 1) # 真实值加噪声，形状 [100,1]
    
    # 创建模型
    model_with_bias = nn.Linear(1, 1, bias=True)          # 带偏置模型：y = wx + b
    model_wo_bias = nn.Linear(1, 1, bias=False)           # 无偏置模型：y = wx
    
    # 分别训练
    results = []                                          # 存储训练结果
    for name, model in [("带偏置", model_with_bias), ("无偏置", model_wo_bias)]:
        optimizer = optim.SGD(model.parameters(), lr=0.1) # SGD 优化器，学习率 0.1
        loss_fn = nn.MSELoss()                            # 均方误差损失函数
        
        losses = []                                       # 记录每轮损失
        for epoch in range(num_epochs):                   # 训练循环
            optimizer.zero_grad()                         # 清零梯度
            y_pred = model(x_train)                       # 前向传播，数据流动：x[100,1] → y_pred[100,1]
            loss = loss_fn(y_pred, y_train)               # 计算损失
            loss.backward()                               # 反向传播
            optimizer.step()                              # 更新参数
            losses.append(loss.item())                    # 记录损失值
        
        # 获取训练后的参数
        w = model.weight.item()                           # 取权重数值
        b = model.bias.item() if model.bias is not None else 0.0  # 取偏置数值（如存在）
        
        results.append((name, w, b, losses[-1]))          # 存入结果
    
    print("=" * 60)                                       # 打印分隔线
    print("带偏置 vs 无偏置 训练效果对比")                 # 打印标题
    print("=" * 60)                                       # 打印分隔线
    print(f"真实规律: y = 2*x + 3")                       # 打印真实规律
    print(f"{'模型类型':<10} {'学习到的 w':<15} {'学习到的 b':<15} {'最终损失':<15}")
    print("-" * 60)                                       # 打印分隔线
    for name, w, b, loss in results:                      # 遍历结果
        print(f"{name:<10} {w:<15.4f} {b:<15.4f} {loss:<15.6f}")
    
    # 分析
    print("-" * 60)                                       # 打印分隔线
    w_bias_results = results[0]                           # 带偏置结果
    w_bias_results_wo = results[1]                        # 无偏置结果
    print(f"\n带偏置模型能否逼近真实规律? {'✅ 能 (w≈2.0, b≈3.0)' if abs(w_bias_results[1]-2)<0.1 and abs(w_bias_results[2]-3)<0.5 else '❌ 不能'}")
    print(f"无偏置模型能否逼近真实规律? {'✅ 能 (w≈2.0)' if abs(w_bias_results_wo[1]-2)<0.1 else '❌ 不能'}")
    print(f"\n结论：当数据存在 y 轴偏移（非零截距）时，")
    print(f"      带偏置的模型可以准确拟合，无偏置的模型永远无法逼近真实规律。")

# 运行训练对比
compare_training(num_epochs=1000)