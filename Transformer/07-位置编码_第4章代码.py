"""
07-位置编码 - 第4章代码
可学习位置编码的实现
"""

import torch
import torch.nn as nn


class LearnedPositionalEncoding(nn.Module):
    """
    可学习位置编码
    
    参数:
        d_model: 编码向量维度
        max_len: 支持的最大序列长度
    """
    def __init__(self, d_model, max_len=5000):
        super(LearnedPositionalEncoding, self).__init__()
        # 创建一个可学习的 Embedding 层
        self.pe = nn.Embedding(max_len, d_model)
        
    def forward(self, x):
        """
        参数:
            x: 输入张量 [batch_size, seq_len, d_model]
        """
        seq_len = x.size(1)
        # 生成位置索引 [0, 1, ..., seq_len-1]
        positions = torch.arange(seq_len, device=x.device).unsqueeze(0)
        # 查表获取位置编码并加到输入上
        x = x + self.pe(positions)
        return x


if __name__ == "__main__":
    # 测试可学习位置编码
    torch.manual_seed(42)
    
    batch_size, seq_len, d_model = 2, 10, 512
    x = torch.randn(batch_size, seq_len, d_model)
    
    pe = LearnedPositionalEncoding(d_model=d_model, max_len=5000)
    output = pe(x)
    
    print("=" * 50)
    print("可学习位置编码测试")
    print("=" * 50)
    print(f"输入形状: {x.shape}")
    print(f"输出形状: {output.shape}")
    print(f"可学习参数量: {sum(p.numel() for p in pe.parameters())}")
    print(f"位置编码矩阵形状: {pe.pe.weight.shape}")
    print("=" * 50)
