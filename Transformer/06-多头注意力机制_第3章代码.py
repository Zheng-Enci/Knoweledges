import torch
import torch.nn as nn
import math


class MultiHeadAttention(nn.Module):
    def __init__(self, d_model=512, n_heads=8, dropout=0.1):
        super(MultiHeadAttention, self).__init__()
        assert d_model % n_heads == 0, "d_model must be divisible by n_heads"

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
    torch.manual_seed(42)

    d_model, n_heads, seq_len = 32, 4, 5
    X = torch.randn(2, seq_len, d_model)

    mha = MultiHeadAttention(d_model=d_model, n_heads=n_heads, dropout=0.0)
    output, weights = mha(X, X, X)

    print("=" * 50)
    print("Multi-Head Self-Attention Test")
    print("=" * 50)
    print(f"d_model: {d_model}, n_heads: {n_heads}, d_k: {d_model // n_heads}")
    print(f"Input shape: {X.shape}")
    print(f"Output shape: {output.shape}")
    print(f"Attention weights shape: {weights.shape}")
    print(f"\nHead 1 attention weights (batch 0):")
    print(weights[0, 0].detach().numpy())
    print(f"\nRow sums (should be ~1.0): {weights[0, 0].sum(dim=-1)}")
    print("=" * 50)
