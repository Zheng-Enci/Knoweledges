import torch.nn as nn

# 定义编码器
class Encoder(nn.Module):
    def __init__(self, vocab_size, embed_dim, hidden_dim):
        super().__init__()
        self.embedding = nn.Embedding(vocab_size, embed_dim)
        self.lstm = nn.LSTM(embed_dim, hidden_dim, batch_first=True)
    
    def forward(self, x):
        # x: [batch_size, seq_len]
        embedded = self.embedding(x)  # [batch_size, seq_len, embed_dim]
        
        # outputs: [batch_size, seq_len, hidden_dim]
        # hidden: [1, batch_size, hidden_dim]
        # cell: [1, batch_size, hidden_dim]
        outputs, (hidden, cell) = self.lstm(embedded)
        
        # 上下文向量 = 最后的隐藏状态
        context_vector = hidden.squeeze(0)  # [batch_size, hidden_dim]
        return context_vector, hidden, cell