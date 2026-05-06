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


def visualize_self_attention(attention_weights, tokens=None):
    if attention_weights.dim() == 4:
        attention_weights = attention_weights[0, 0]
    elif attention_weights.dim() == 3:
        attention_weights = attention_weights[0]

    weights = attention_weights.detach().cpu().numpy()

    fig, axes = plt.subplots(1, 2, figsize=(14, 5))

    im = axes[0].imshow(weights, cmap='Blues', aspect='auto')
    plt.colorbar(im, ax=axes[0])
    if tokens:
        axes[0].set_xticks(range(len(tokens)))
        axes[0].set_yticks(range(len(tokens)))
        axes[0].set_xticklabels(tokens, rotation=45)
        axes[0].set_yticklabels(tokens)
    axes[0].set_xlabel('Key Positions')
    axes[0].set_ylabel('Query Positions')
    axes[0].set_title('Attention Heatmap')

    for i in range(weights.shape[0]):
        axes[1].bar(range(weights.shape[1]), weights[i], alpha=0.7, label=f'Q{i}' if tokens else f'Pos {i}')
    axes[1].set_xlabel('Key Positions')
    axes[1].set_ylabel('Attention Weight')
    axes[1].set_title('Attention Bar Chart')
    if tokens:
        axes[1].set_xticks(range(len(tokens)))
        axes[1].set_xticklabels(tokens, rotation=45)
    axes[1].legend()

    plt.tight_layout()
    plt.savefig('05_chapter6_visualization.png', dpi=150, bbox_inches='tight')
    print("Image saved as 05_chapter6_visualization.png")
    plt.show()


if __name__ == "__main__":
    torch.manual_seed(42)

    d_model, seq_len = 16, 6
    X = torch.randn(1, seq_len, d_model)

    self_attn = SelfAttention(d_model=d_model, dropout=0.0)
    output, weights = self_attn(X)

    words = ['我', '喜欢', '吃', '苹果', '因为', '甜']
    visualize_self_attention(weights, tokens=words)
