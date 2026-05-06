import matplotlib.pyplot as plt
import torch
import torch.nn.functional as F
import math

# 设置 Matplotlib 支持中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']  # 使用黑体或其他中文字体
plt.rcParams['axes.unicode_minus'] = False  # 解决负号显示问题




class ScaledDotProductAttention(torch.nn.Module):
    """
    手动实现的缩放点积注意力
    """
    def __init__(self, dropout=0.1):
        super(ScaledDotProductAttention, self).__init__()
        self.dropout = torch.nn.Dropout(dropout)
        
    def forward(self, Q, K, V, mask=None):
        # 获取维度 d_k
        d_k = Q.size(-1)
        
        # 计算注意力分数: Q @ K^T / sqrt(d_k)
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(d_k)
        
        # 应用掩码（如果有）
        if mask is not None:
            scores = scores.masked_fill(mask == 0, float('-inf'))
        
        # Softmax 归一化
        attention_weights = torch.softmax(scores, dim=-1)
        
        # Dropout
        attention_weights = self.dropout(attention_weights)
        
        # 加权求和
        output = torch.matmul(attention_weights, V)
        
        return output, attention_weights


def visualize_attention(attention_weights, tokens=None):
    """
    可视化注意力权重热力图
    
    参数:
        attention_weights: 注意力权重矩阵 [seq_len_q, seq_len_k]
        tokens: 可选的词列表，用于标注坐标轴
    """
    import numpy as np
    
    # 如果是多维张量，取第一个 batch 和第一个 head
    if attention_weights.dim() == 4:
        attention_weights = attention_weights[0, 0]
    elif attention_weights.dim() == 3:
        attention_weights = attention_weights[0]
    
    # 转换为 numpy 数组
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


# ========== 运行可视化示例 ==========

# 构造一个简单的输入
batch_size, n_heads, seq_len, d_k = 2, 4, 5, 64
Q = torch.randn(batch_size, n_heads, seq_len, d_k)
K = torch.randn(batch_size, n_heads, seq_len, d_k)
V = torch.randn(batch_size, n_heads, seq_len, d_k)

# 创建注意力模块并计算
attention = ScaledDotProductAttention(dropout=0.0)
output, weights = attention(Q, K, V)

# 可视化
words = ['我', '喜欢', '深度', '学习', '。']
visualize_attention(weights, tokens=words)
