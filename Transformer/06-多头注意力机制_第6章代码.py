import torch
import torch.nn as nn
import math
import matplotlib.pyplot as plt
import numpy as np
from matplotlib.colors import ListedColormap

def get_color(value):
    color1 = np.array([255, 255, 255])
    color2 = np.array([0, 0, 0])
    return tuple((color1 + (color2 - color1) * value) / 255)

cmap_colors = [get_color(i/20) for i in range(21)]
cmap = ListedColormap(cmap_colors)

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


if __name__ == "__main__":
    print("=" * 60)
    print("Example 1: Multi-Head Self-Attention")
    print("=" * 60)

    torch.manual_seed(42)
    d_model, n_heads, seq_len = 32, 4, 5
    X = torch.randn(2, seq_len, d_model)

    mha = MultiHeadAttention(d_model=d_model, n_heads=n_heads, dropout=0.0)
    output, weights = mha(X, X, X)

    print(f"Input shape: {X.shape}")
    print(f"Output shape: {output.shape}")
    print(f"Attention weights shape: {weights.shape}")
    print(f"d_k (per head): {d_model // n_heads}")
    print(f"\nHead 1 attention weights (batch 0):")
    print(weights[0, 0].detach().numpy())
    print(f"Row sums (should be ~1.0): {weights[0, 0].sum(dim=-1)}")
    print()

    print("=" * 60)
    print("Example 2: Multi-Head Cross-Attention")
    print("=" * 60)

    seq_len_enc, seq_len_dec = 6, 4
    encoder_output = torch.randn(2, seq_len_enc, d_model)
    decoder_input = torch.randn(2, seq_len_dec, d_model)

    output_cross, weights_cross = mha(decoder_input, encoder_output, encoder_output)

    print(f"Encoder output shape: {encoder_output.shape}")
    print(f"Decoder input shape: {decoder_input.shape}")
    print(f"Cross-attention output shape: {output_cross.shape}")
    print(f"Cross-attention weights shape: {weights_cross.shape}")
    print(f"\nCross-attention weights (batch 0, head 0):")
    print(weights_cross[0, 0].detach().numpy())
    print(f"Row sums (should be ~1.0): {weights_cross[0, 0].sum(dim=-1)}")
    print()

    print("=" * 60)
    print("Example 3: Multi-Head Self-Attention with Causal Mask")
    print("=" * 60)

    causal_mask = torch.tril(torch.ones(seq_len, seq_len)).unsqueeze(0).unsqueeze(0)
    output_causal, weights_causal = mha(X, X, X, mask=causal_mask)

    print(f"Causal mask:\n{causal_mask[0, 0]}")
    print(f"\nCausal attention weights (batch 0, head 0):")
    print(weights_causal[0, 0].detach().numpy())
    print(f"Upper triangle should be all zeros: {(weights_causal[0, 0].detach().numpy() == 0).all()}")
    print()

    fig, axes = plt.subplots(2, 2, figsize=(14, 10))

    w0 = weights[0, 0].detach().numpy()
    w0 = w0 / w0.max() if w0.max() > 0 else w0
    im0 = axes[0, 0].imshow(w0, cmap=cmap, aspect='auto', vmin=0, vmax=1)
    axes[0, 0].set_title('Self-Attention (Head 1)')
    axes[0, 0].set_xlabel('Key')
    axes[0, 0].set_ylabel('Query')
    plt.colorbar(im0, ax=axes[0, 0])

    w1 = weights[0, 1].detach().numpy()
    w1 = w1 / w1.max() if w1.max() > 0 else w1
    im1 = axes[0, 1].imshow(w1, cmap=cmap, aspect='auto', vmin=0, vmax=1)
    axes[0, 1].set_title('Self-Attention (Head 2)')
    axes[0, 1].set_xlabel('Key')
    axes[0, 1].set_ylabel('Query')
    plt.colorbar(im1, ax=axes[0, 1])

    w2 = weights_cross[0, 0].detach().numpy()
    w2 = w2 / w2.max() if w2.max() > 0 else w2
    im2 = axes[1, 0].imshow(w2, cmap=cmap, aspect='auto', vmin=0, vmax=1)
    axes[1, 0].set_title('Cross-Attention (Head 1)')
    axes[1, 0].set_xlabel('Encoder Positions')
    axes[1, 0].set_ylabel('Decoder Positions')
    plt.colorbar(im2, ax=axes[1, 0])

    w3 = weights_causal[0, 0].detach().numpy()
    w3 = w3 / w3.max() if w3.max() > 0 else w3
    im3 = axes[1, 1].imshow(w3, cmap=cmap, aspect='auto', vmin=0, vmax=1)
    axes[1, 1].set_title('Causal Self-Attention (Head 1)')
    axes[1, 1].set_xlabel('Key')
    axes[1, 1].set_ylabel('Query')
    plt.colorbar(im3, ax=axes[1, 1])

    plt.suptitle('Multi-Head Attention: Three Usage Scenarios', fontsize=14, fontweight='bold')
    plt.tight_layout()
    plt.savefig('06_chapter6_visualization.png', dpi=150, bbox_inches='tight')
    print("Image saved as 06_chapter6_visualization.png")
    plt.show()
