import torch
import torch.nn as nn
import math
import matplotlib.pyplot as plt

# 设置 Matplotlib 支持中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


class ScaledDotProductAttention(nn.Module):
    """缩放点积注意力机制的手动实现"""
    
    def __init__(self, dropout=0.1):
        super(ScaledDotProductAttention, self).__init__()
        self.dropout = nn.Dropout(dropout)
        
    def forward(self, Q, K, V, mask=None):
        d_k = Q.size(-1)
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)
        
        if mask is not None:
            scores = scores.masked_fill(mask == 0, float('-inf'))
        
        attention_weights = torch.softmax(scores, dim=-1)
        attention_weights = self.dropout(attention_weights)
        output = torch.matmul(attention_weights, V)
        
        return output, attention_weights


def test_attention():
    """测试注意力模块"""
    # 设置随机种子，保证结果可复现
    torch.manual_seed(42)
    
    # 参数设置
    batch_size = 2
    n_heads = 4
    seq_len = 5
    d_k = 64
    d_v = 64
    
    # 随机生成 Q, K, V
    Q = torch.randn(batch_size, n_heads, seq_len, d_k)
    K = torch.randn(batch_size, n_heads, seq_len, d_k)
    V = torch.randn(batch_size, n_heads, seq_len, d_v)
    
    # 创建注意力模块
    attention = ScaledDotProductAttention(dropout=0.0)
    
    # 前向传播
    output, weights = attention(Q, K, V)
    
    print("=" * 50)
    print("缩放点积注意力测试")
    print("=" * 50)
    print(f"Q 形状: {Q.shape}")
    print(f"K 形状: {K.shape}")
    print(f"V 形状: {V.shape}")
    print(f"输出形状: {output.shape}")
    print(f"注意力权重形状: {weights.shape}")
    print(f"权重每行求和: {weights[0, 0].sum(dim=-1)}")  # 应该接近 1.0
    print("=" * 50)
    
    return output, weights


def visualize_attention(attention_weights, tokens=None):
    """可视化注意力权重"""
    import numpy as np
    
    if attention_weights.dim() == 4:
        attention_weights = attention_weights[0, 0]
    elif attention_weights.dim() == 3:
        attention_weights = attention_weights[0]
    
    weights = attention_weights.detach().cpu().numpy()
    
    plt.figure(figsize=(8, 6))
    plt.imshow(weights, cmap='gray', aspect='auto')
    plt.colorbar(label='Attention Weight')
    
    if tokens is not None:
        plt.xticks(range(len(tokens)), tokens, rotation=45)
        plt.yticks(range(len(tokens)), tokens)
    
    plt.xlabel('Key Positions')
    plt.ylabel('Query Positions')
    plt.title('Attention Weights Heatmap')
    plt.tight_layout()
    plt.savefig('attention_heatmap.png', dpi=150, bbox_inches='tight')
    print("图片已保存为 attention_heatmap.png")


if __name__ == "__main__":
    # 运行测试
    output, weights = test_attention()
    
    # 可视化
    words = ['我', '喜欢', '深度', '学习', '。']
    visualize_attention(weights, tokens=words)
