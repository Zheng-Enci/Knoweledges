import torch
import torch.nn as nn
import math


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


if __name__ == "__main__":
    torch.manual_seed(42)
    
    batch_size, seq_len, d_model = 2, 5, 16
    X = torch.randn(batch_size, seq_len, d_model)
    
    self_attn = SelfAttention(d_model=d_model, dropout=0.0)
    output, attention_weights = self_attn(X)
    
    print("=" * 50)
    print("Self-Attention Test")
    print("=" * 50)
    print(f"Input shape: {X.shape}")
    print(f"Output shape: {output.shape}")
    print(f"Attention weights shape: {attention_weights.shape}")
    print(f"\nAttention weights (batch 0):")
    print(attention_weights[0].detach().numpy())
    print(f"\nRow sums (should be ~1.0): {attention_weights[0].sum(dim=-1)}")
    print("=" * 50)
