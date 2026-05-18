"""
07-位置编码 - 第3章代码
正弦位置编码的完整实现
"""

import torch
import torch.nn as nn
import math


class SinusoidalPositionalEncoding(nn.Module):
    """
    正弦位置编码的 PyTorch 实现
    
    参数:
        d_model: 编码向量的维度（必须为偶数）
        max_len: 支持的最大序列长度
        dropout: Dropout 概率
    """
    def __init__(self, d_model, max_len=5000, dropout=0.1):
        super(SinusoidalPositionalEncoding, self).__init__()
        self.dropout = nn.Dropout(dropout)
        
        # 1. 创建位置编码矩阵 [max_len, d_model]
        pe = torch.zeros(max_len, d_model)
        
        # 2. 生成位置索引 [max_len, 1]
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        
        # 3. 计算频率除数项 [d_model/2]
        # 等价于 1 / (10000^(2i/d_model))
        div_term = torch.exp(
            torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model)
        )
        
        # 4. 偶数维度填 sin，奇数维度填 cos
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        
        # 5. 增加 batch 维度 [1, max_len, d_model]
        pe = pe.unsqueeze(0)
        
        # 6. 注册为 buffer（不参与梯度更新，但会随模型保存）
        self.register_buffer('pe', pe)
        
    def forward(self, x):
        """
        前向传播
        
        参数:
            x: 输入张量 [batch_size, seq_len, d_model]
            
        返回:
            加上位置编码后的张量 [batch_size, seq_len, d_model]
        """
        # 取出对应长度的位置编码并加到输入上
        x = x + self.pe[:, :x.size(1), :]
        return self.dropout(x)


if __name__ == "__main__":
    # 测试正弦位置编码
    torch.manual_seed(42)
    
    batch_size, seq_len, d_model = 2, 10, 512
    x = torch.randn(batch_size, seq_len, d_model)
    
    pe = SinusoidalPositionalEncoding(d_model=d_model, max_len=5000, dropout=0.0)
    output = pe(x)
    
    print("=" * 50)
    print("正弦位置编码测试")
    print("=" * 50)
    print(f"输入形状: {x.shape}")
    print(f"输出形状: {output.shape}")
    print(f"输入与输出形状一致: {x.shape == output.shape}")
    print(f"位置编码矩阵形状: {pe.pe.shape}")
    print(f"位置编码值范围: [{pe.pe.min():.4f}, {pe.pe.max():.4f}]")
    print("=" * 50)
