import matplotlib.pyplot as plt
import torch
import math
import torch.nn as nn

plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


class MultiHeadAttention(nn.Module):
    def __init__(self, d_model=512, n_heads=8, dropout=0.1):
        super(MultiHeadAttention, self).__init__()
        assert d_model % n_heads == 0
        self.d_model = d_model
        self.n_heads = n_heads
        self.d_k = d_model // n_heads
        self.W_Q = nn.Linear(d_model, d_model)
        self.W_K = nn.Linear(d_model, d_model)
        self.W_V = nn.Linear(d_model, d_model)
        self.W_O = nn.Linear(d_model, d_model)
        self.dropout = nn.Dropout(dropout)

    def split_heads(self, x):
        batch_size, seq_len, _ = x.size()
        x = x.view(batch_size, seq_len, self.n_heads, self.d_k)
        return x.transpose(1, 2)

    def combine_heads(self, x):
        batch_size, _, seq_len, _ = x.size()
        x = x.transpose(1, 2).contiguous()
        return x.view(batch_size, seq_len, self.d_model)

    def forward(self, Q, K, V, mask=None):
        Q = self.W_Q(Q)
        K = self.W_K(K)
        V = self.W_V(V)
        Q = self.split_heads(Q)
        K = self.split_heads(K)
        V = self.split_heads(V)
        scores = torch.matmul(Q, K.transpose(-2, -1)) / math.sqrt(self.d_k)
        if mask is not None:
            scores = scores.masked_fill(mask == 0, float('-inf'))
        attention_weights = torch.softmax(scores, dim=-1)
        attention_weights = self.dropout(attention_weights)
        context = torch.matmul(attention_weights, V)
        context = self.combine_heads(context)
        output = self.W_O(context)
        return output, attention_weights


def visualize_multi_head_attention(attention_weights, tokens=None, n_heads=8):
    weights = attention_weights[0].detach().cpu().numpy()

    cols = 4
    rows = (n_heads + cols - 1) // cols
    fig, axes = plt.subplots(rows, cols, figsize=(16, 4 * rows))
    axes = axes.flatten()

    for i in range(n_heads):
        im = axes[i].imshow(weights[i], cmap='RdYlBu_r', aspect='auto', vmin=0, vmax=1)
        if tokens:
            axes[i].set_xticks(range(len(tokens)))
            axes[i].set_yticks(range(len(tokens)))
            axes[i].set_xticklabels(tokens, rotation=45)
            axes[i].set_yticklabels(tokens)
        axes[i].set_xlabel('Key Positions')
        axes[i].set_ylabel('Query Positions')
        axes[i].set_title(f'Head {i + 1}')

    for i in range(n_heads, len(axes)):
        axes[i].axis('off')

    plt.suptitle('Multi-Head Attention Weights — Each Head Learns Different Patterns',
                 fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('06_chapter5_visualization.png', dpi=150, bbox_inches='tight')
    print("Image saved as 06_chapter5_visualization.png")
    plt.show()


if __name__ == "__main__":
    torch.manual_seed(42)

    d_model, n_heads, seq_len = 64, 8, 6
    X = torch.randn(1, seq_len, d_model)

    mha = MultiHeadAttention(d_model=d_model, n_heads=n_heads, dropout=0.0)
    output, weights = mha(X, X, X)

    print("=" * 60)
    print("各注意力头的权重矩阵：")
    print("=" * 60)
    
    words = ['我', '喜欢', '吃', '苹果', '因为', '甜']
    weights_np = weights[0].detach().cpu().numpy()
    
    for head_idx in range(n_heads):
        print(f"\n【Head {head_idx + 1}】")
        print(f"  词: {words}")
        for i, word_i in enumerate(words):
            row_weights = weights_np[head_idx, i, :]
            top_k = 3
            top_indices = row_weights.argsort()[-top_k:][::-1]
            top_pairs = [(words[j], row_weights[j]) for j in top_indices]
            print(f"  {word_i}({i}) 关注: {top_pairs}")
    
    print("\n" + "=" * 60)
    print("（完整权重矩阵见下方热力图）")
    print("=" * 60)
    
    visualize_multi_head_attention(weights, tokens=words, n_heads=n_heads)
