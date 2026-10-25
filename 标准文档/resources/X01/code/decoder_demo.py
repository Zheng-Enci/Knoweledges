"""
Transformer 解码器结构最小实现：掩码自注意力 + 交叉注意力 + 前馈网络

参数:
    d_model: 模型维度，默认 512
    n_heads: 注意力头数，默认 8
    d_ff: 前馈网络隐藏维度，默认 2048
    n_layers: 解码器堆叠层数，默认 6
返回:
    无返回值，脚本运行后打印张量形状、单层参数量与因果性校验结果
"""

import torch                                                        # 张量计算基础库 🔧
import torch.nn as nn                                               # 神经网络模块 🛠️

D_MODEL = 512                                                       # 模型维度 512，与原始论文 base 配置一致 📐
N_HEADS = 8                                                         # 注意力头数 8，每头维度 512 / 8 = 64 ⚡
D_FF = 2048                                                         # 前馈网络隐藏维度 4 × 512 = 2048 🧮
N_LAYERS = 6                                                        # 解码器堆叠 6 层，与原始论文 base 配置一致 🧱


class DecoderLayer(nn.Module):
    """
    解码器单层：掩码自注意力 → 交叉注意力 → 前馈网络，三个子层各自带残差

    参数:
        d_model: 模型维度，决定每个子层的输入输出宽度
        n_heads: 注意力头数，d_model 必须能被它整除
        d_ff: 前馈网络隐藏维度，一般为 4 × d_model
        dropout: 训练时随机丢弃比例，推理时不起作用
    返回:
        forward 输出 [batch, tgt_len, d_model] 的张量
    """

    def __init__(self, d_model: int, n_heads: int, d_ff: int, dropout: float = 0.1) -> None:
        super().__init__()                                                          # 初始化父类 nn.Module 🧩
        self.self_attn = nn.MultiheadAttention(                                     # 掩码自注意力：Q/K/V 全来自解码器自身 ✅
            d_model, n_heads, dropout=dropout, batch_first=True                     # batch_first=True 让输入形状为 [B, T, D] 📦
        )                                                                           # 构造完成，内部含 4 个 d×d 权重矩阵 🔢
        self.cross_attn = nn.MultiheadAttention(                                    # 交叉注意力：Q 来自解码器，K/V 来自编码器输出 🔀
            d_model, n_heads, dropout=dropout, batch_first=True                     # 超参与自注意力保持一致 ⚙️
        )                                                                           # 这层是解码器唯一的信息入口 🚪
        self.ffn = nn.Sequential(                                                   # 前馈网络：对每个位置独立做两层全连接 🏭
            nn.Linear(d_model, d_ff),                                               # 升维 512 → 2048 📈
            nn.ReLU(),                                                              # 非线性激活，SwiGLU 是它的现代替代 🔁
            nn.Dropout(dropout),                                                    # 训练时随机丢弃，抑制过拟合 🎲
            nn.Linear(d_ff, d_model),                                               # 降维 2048 → 512 📉
        )                                                                           # 参数量占本层的一半左右 💰
        self.norm1 = nn.LayerNorm(d_model)                                          # pre-norm：先归一化再进自注意力 🧼
        self.norm2 = nn.LayerNorm(d_model)                                          # pre-norm：先归一化再进交叉注意力 🧼
        self.norm3 = nn.LayerNorm(d_model)                                          # pre-norm：先归一化再进前馈网络 🧼

    def forward(self, x, memory, tgt_mask=None, memory_key_padding_mask=None):
        h = self.norm1(x)                                                           # [B, T, D] → 归一化后的输入 🧼
        x = x + self.self_attn(                                                     # 残差连接：新输出 = 输入 + 子层输出 ➕
            h, h, h, attn_mask=tgt_mask, need_weights=False                         # Q=K=V=h，tgt_mask 屏蔽未来位置 🚫
        )[0]                                                                        # 取第 0 个返回值，即注意力输出 🎯
        h = self.norm2(x)                                                           # 归一化后再做交叉注意力 🧼
        x = x + self.cross_attn(                                                    # 残差连接，把编码器信息缝进来 ➕
            h, memory, memory, key_padding_mask=memory_key_padding_mask,            # Q 来自解码器，K/V 来自 memory 🎯
            need_weights=False                                                      # 不返回注意力权重，省显存 💾
        )[0]                                                                        # 取出交叉注意力输出 🎯
        x = x + self.ffn(self.norm3(x))                                             # 残差连接包裹前馈网络 ➕
        return x                                                                    # 返回 [B, T, D] 🎁


class Decoder(nn.Module):
    """
    解码器整体：词嵌入 + 位置嵌入 + N 层 DecoderLayer + 输出投影

    参数:
        vocab_size: 词表大小，决定词嵌入与输出层的宽度
        d_model: 模型维度
        n_heads: 注意力头数
        d_ff: 前馈网络隐藏维度
        n_layers: 堆叠层数
        max_len: 支持的最大目标序列长度
        dropout: 训练时随机丢弃比例
    返回:
        forward 输出 [batch, tgt_len, vocab_size] 的词表打分
    """

    def __init__(self, vocab_size: int, d_model: int = D_MODEL, n_heads: int = N_HEADS,
                 d_ff: int = D_FF, n_layers: int = N_LAYERS, max_len: int = 1024,
                 dropout: float = 0.1) -> None:
        super().__init__()                                                          # 初始化父类 nn.Module 🧩
        self.tok_emb = nn.Embedding(vocab_size, d_model)                            # 词嵌入：token id → 512 维向量 🔤
        self.pos_emb = nn.Embedding(max_len, d_model)                               # 位置嵌入：位置 id → 512 维向量 📍
        self.layers = nn.ModuleList([                                               # 逐层堆叠，方便按索引取单层核对参数 🧱
            DecoderLayer(d_model, n_heads, d_ff, dropout)                           # 每一层结构完全相同 ⚙️
            for _ in range(n_layers)                                                # 循环 n_layers 次，默认 6 层 🔁
        ])                                                                          # ModuleList 会正确注册全部子模块 ✅
        self.norm = nn.LayerNorm(d_model)                                           # 最后一层归一化，接输出投影 🧼
        self.lm_head = nn.Linear(d_model, vocab_size, bias=False)                   # 输出投影：512 维 → 词表打分 📊

    def forward(self, tgt_ids, memory, memory_key_padding_mask=None):
        batch, tgt_len = tgt_ids.shape                                             # 读出批大小与目标长度，[2, 6] → 2 和 6 📦
        pos = torch.arange(tgt_len, device=tgt_ids.device).unsqueeze(0)             # 位置 id 序列 [0..5] → 形状 [1, 6] 📍
        x = self.tok_emb(tgt_ids) + self.pos_emb(pos)                               # 词向量与位置向量逐元素相加 🎯
        causal = torch.triu(                                                        # 上三角布尔矩阵，True 表示该位置被屏蔽 🚫
            torch.ones(tgt_len, tgt_len, dtype=torch.bool), diagonal=1               # diagonal=1 表示不屏蔽主对角线 📐
        )                                                                           # 形状 [T, T]，可广播到所有批次与头 🌐
        for layer in self.layers:                                                    # 逐层前向，共 6 次 🔁
            x = layer(x, memory, tgt_mask=causal,                                   # 每层都吃同一份因果掩码 🚫
                      memory_key_padding_mask=memory_key_padding_mask)              # 源侧 padding 屏蔽，可传 None ⚙️
        return self.lm_head(self.norm(x))                                           # 归一化后投影到词表，输出 [B, T, V] 📊


if __name__ == "__main__":                                                          # 脚本入口，直接运行即可 🚪
    torch.manual_seed(0)                                                           # 固定随机种子，保证每次输出一致 🎲
    BATCH, TGT_LEN, SRC_LEN, VOCAB = 2, 6, 9, 1000                                 # 批 2、目标 6、源 9、词表 1000 📦
    model = Decoder(vocab_size=VOCAB, n_layers=1, max_len=64, dropout=0.0)          # 只建 1 层，便于核对单层参数量 🔍
    model.eval()                                                                   # 切到推理模式，让因果性校验结果精确为 0 🧊
    memory = torch.randn(BATCH, SRC_LEN, D_MODEL)                                  # 模拟编码器输出，形状 [2, 9, 512] 🧠
    tgt = torch.randint(0, VOCAB, (BATCH, TGT_LEN))                                # 模拟已生成的目标 token，[2, 6] 🔤
    logits = model(tgt, memory)                                                    # 前向一次，得到 [2, 6, 1000] 📊
    print("logits.shape =", tuple(logits.shape))                                    # 期待 (2, 6, 1000) ✅
    layer_params = sum(p.numel() for p in model.layers[0].parameters())             # 单层参数量，含 bias 应为 4204032 🔢
    print("decoder layer params =", layer_params)                                   # 打印出来与正文公式对账 🧮
    tgt2 = tgt.clone()                                                              # 复制输入，只改最后一个 token 🔁
    tgt2[:, -1] = (tgt2[:, -1] + 1) % VOCAB                                         # 把末位 token 换成词表里的另一个词 🎯
    logits2 = model(tgt2, memory)                                                   # 再前向一次 📊
    prefix_diff = (logits2[:, :-1] - logits[:, :-1]).abs().max().item()             # 前 5 个位置的最大差值，应为 0.0 ✅
    last_diff = (logits2[:, -1] - logits[:, -1]).abs().max().item()                 # 最后 1 个位置的最大差值，应大于 0 🔍
    print("prefix max diff =", prefix_diff)                                         # 掩码生效的直接证据 🚫
    print("last token max diff =", last_diff)                                       # 末位确实被改动影响 🎯
