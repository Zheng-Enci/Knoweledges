"""
05-自注意力机制详解 - 第5章代码
手动代码实现：自注意力机制的完整实现与逐行讲解
"""

import torch
import torch.nn as nn
import math


class SelfAttention(nn.Module):
    """
    自注意力机制的手动实现

    结构：输入 → Q/K/V线性变换 → 缩放点积注意力 → 输出

    参数:
        d_model: 输入向量的维度
        d_k: Q、K的维度（默认与d_model相同）
        d_v: V的维度（默认与d_model相同）
        dropout: Dropout概率
    """

    def __init__(self, d_model, d_k=None, d_v=None, dropout=0.1):
        super(SelfAttention, self).__init__()
        d_k = d_k or d_model
        d_v = d_v or d_model

        self.W_Q = nn.Linear(d_model, d_k)
        self.W_K = nn.Linear(d_model, d_k)
        self.W_V = nn.Linear(d_model, d_v)

        self.dropout = nn.Dropout(dropout)
        self.d_k = d_k

    def forward(self, X, mask=None):
        """
        前向传播

        参数:
            X: 输入序列 [batch_size, seq_len, d_model]
            mask: 可选的掩码 [batch_size, seq_len] 或 [batch_size, seq_len, seq_len]

        返回:
            output: 自注意力输出 [batch_size, seq_len, d_v]
            attention_weights: 注意力权重 [batch_size, seq_len, seq_len]
        """
        Q = self.W_Q(X)
        K = self.W_K(X)
        V = self.W_V(X)

        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)

        if mask is not None:
            if mask.dim() == 2:
                mask = mask.unsqueeze(1).unsqueeze(2)
            scores = scores.masked_fill(mask == 0, float('-inf'))

        attention_weights = torch.softmax(scores, dim=-1)
        attention_weights = self.dropout(attention_weights)

        output = torch.matmul(attention_weights, V)

        return output, attention_weights


# ========== 测试代码 ==========
if __name__ == "__main__":
    torch.manual_seed(42)
    
    # 参数设置
    batch_size, seq_len, d_model = 2, 5, 16
    
    # 随机输入
    X = torch.randn(batch_size, seq_len, d_model)
    
    # 创建自注意力模块
    self_attn = SelfAttention(d_model=d_model, dropout=0.0)
    
    # 前向传播
    output, attention_weights = self_attn(X)
    
    print("=" * 50)
    print("自注意力机制测试")
    print("=" * 50)
    print(f"输入形状: {X.shape}")
    print(f"输出形状: {output.shape}")
    print(f"注意力权重形状: {attention_weights.shape}")
    print(f"\n注意力权重 (第一个batch):")
    print(attention_weights[0].detach().numpy())
    print(f"\n权重每行求和 (应接近1.0): {attention_weights[0].sum(dim=-1)}")
    print("=" * 50)
