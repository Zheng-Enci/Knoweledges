"""
05-自注意力机制详解 - 第7章代码
完整可运行示例：整合所有内容，包含 Padding Mask 和 Causal Mask 的完整示例
"""

import torch
import torch.nn as nn
import math
import matplotlib.pyplot as plt

plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


class SelfAttention(nn.Module):
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


def create_padding_mask(seq_lengths, max_len):
    """创建 Padding Mask：True 表示有效位置"""
    batch_size = len(seq_lengths)
    mask = torch.zeros(batch_size, max_len)
    for i, length in enumerate(seq_lengths):
        mask[i, :length] = 1
    return mask


def create_causal_mask(seq_len):
    """创建 Causal Mask：下三角矩阵"""
    return torch.tril(torch.ones(seq_len, seq_len))


# ========== 示例1：无掩码自注意力 ==========
print("=" * 50)
print("示例1：无掩码自注意力")
print("=" * 50)

torch.manual_seed(42)
d_model, seq_len = 8, 4
X = torch.randn(1, seq_len, d_model)

self_attn = SelfAttention(d_model=d_model, dropout=0.0)
output, weights = self_attn(X)

print(f"输入形状: {X.shape}")
print(f"输出形状: {output.shape}")
print(f"注意力权重形状: {weights.shape}")
print(f"注意力权重:\n{weights[0].detach().numpy()}")
print()

# ========== 示例2：带 Padding Mask 的自注意力 ==========
print("=" * 50)
print("示例2：带 Padding Mask 的自注意力")
print("=" * 50)

seq_lengths = [3, 4]
max_len = 4
X_batch = torch.randn(2, max_len, d_model)
padding_mask = create_padding_mask(seq_lengths, max_len)

output_masked, weights_masked = self_attn(X_batch, mask=padding_mask)

print(f"Padding Mask:\n{padding_mask}")
print(f"\n第一个样本（长度3）的注意力权重:\n{weights_masked[0].detach().numpy()}")
print(f"注意：第4列（PAD位置）的权重全为0")
print()

# ========== 示例3：带 Causal Mask 的自注意力 ==========
print("=" * 50)
print("示例3：带 Causal Mask 的自注意力")
print("=" * 50)

causal_mask = create_causal_mask(seq_len)
output_causal, weights_causal = self_attn(X, mask=causal_mask)

print(f"Causal Mask:\n{causal_mask}")
print(f"\n因果注意力权重:\n{weights_causal[0].detach().numpy()}")
print(f"注意：每行只看得到自己和前面的位置（上三角全为0）")
print()

# ========== 可视化对比 ==========
fig, axes = plt.subplots(1, 3, figsize=(18, 5))

titles = ['无掩码', 'Padding Mask (长度=3)', 'Causal Mask']
weights_list = [weights[0], weights_masked[0], weights_causal[0]]

for ax, w, title in zip(axes, weights_list, titles):
    im = ax.imshow(w.detach().numpy(), cmap='Blues', aspect='auto', vmin=0, vmax=1)
    plt.colorbar(im, ax=ax)
    ax.set_title(title)
    ax.set_xlabel('Key')
    ax.set_ylabel('Query')

plt.tight_layout()
plt.savefig('self_attention_masks_comparison.png', dpi=150, bbox_inches='tight')
print("对比图已保存为 self_attention_masks_comparison.png")
plt.show()
