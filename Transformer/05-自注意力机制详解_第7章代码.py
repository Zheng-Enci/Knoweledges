"""
05-自注意力机制详解 - 第7章代码
Complete runnable example with Padding Mask and Causal Mask
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
    batch_size = len(seq_lengths)
    mask = torch.zeros(batch_size, max_len)
    for i, length in enumerate(seq_lengths):
        mask[i, :length] = 1
    return mask


def create_causal_mask(seq_len):
    return torch.tril(torch.ones(seq_len, seq_len))


print("=" * 50)
print("Example 1: Self-Attention without Mask")
print("=" * 50)

torch.manual_seed(42)
d_model, seq_len = 8, 4
X = torch.randn(1, seq_len, d_model)

self_attn = SelfAttention(d_model=d_model, dropout=0.0)
output, weights = self_attn(X)

print(f"Input shape: {X.shape}")
print(f"Output shape: {output.shape}")
print(f"Attention weights shape: {weights.shape}")
print(f"Attention weights:\n{weights[0].detach().numpy()}")
print()

print("=" * 50)
print("Example 2: Self-Attention with Padding Mask")
print("=" * 50)

seq_lengths = [3, 4]
max_len = 4
X_batch = torch.randn(2, max_len, d_model)
padding_mask = create_padding_mask(seq_lengths, max_len)

output_masked, weights_masked = self_attn(X_batch, mask=padding_mask)

print(f"Padding Mask:\n{padding_mask}")
print(f"\nAttention weights (sample 0, length=3):\n{weights_masked[0].detach().numpy()}")
print(f"Note: Column 4 (PAD position) has all weights = 0")
print()

print("=" * 50)
print("Example 3: Self-Attention with Causal Mask")
print("=" * 50)

causal_mask = create_causal_mask(seq_len)
output_causal, weights_causal = self_attn(X, mask=causal_mask)

print(f"Causal Mask:\n{causal_mask}")
print(f"\nCausal attention weights:\n{weights_causal[0].detach().numpy()}")
print(f"Note: Each row can only see itself and previous positions (upper triangle = 0)")
print()

fig, axes = plt.subplots(3, 2, figsize=(14, 12))

weights_list = [weights[0], weights_masked[0], weights_causal[0]]
titles = ['No Mask', 'Padding Mask (len=3)', 'Causal Mask']

for i, (w, title) in enumerate(zip(weights_list, titles)):
    w_np = w.detach().cpu().numpy()
    im = axes[i, 0].imshow(w_np, cmap='Blues', aspect='auto', vmin=0, vmax=1)
    plt.colorbar(im, ax=axes[i, 0])
    axes[i, 0].set_title(f'{title} - Heatmap')
    axes[i, 0].set_xlabel('Key')
    axes[i, 0].set_ylabel('Query')

    for j in range(w_np.shape[0]):
        y_data = [float(x) for x in w_np[j]]
        axes[i, 1].bar(list(range(w_np.shape[1])), y_data, alpha=0.7, label=f'Q{j}')
    axes[i, 1].set_xlabel('Key')
    axes[i, 1].set_ylabel('Attention Weight')
    axes[i, 1].set_title(f'{title} - Bar Chart')
    axes[i, 1].legend()

plt.tight_layout()
plt.savefig('05_chapter7_visualization.png', dpi=150, bbox_inches='tight')
print("Image saved as 05_chapter7_visualization.png")
plt.show()
