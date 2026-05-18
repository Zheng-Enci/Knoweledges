"""
07-位置编码 - 第7章代码
完整可运行示例（整合测试和可视化）
"""

import torch
import torch.nn as nn
import math
import matplotlib.pyplot as plt
import numpy as np

# 设置 Matplotlib 支持中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


class SinusoidalPositionalEncoding(nn.Module):
    """正弦位置编码"""
    
    def __init__(self, d_model, max_len=5000, dropout=0.1):
        super(SinusoidalPositionalEncoding, self).__init__()
        self.dropout = nn.Dropout(dropout)
        
        pe = torch.zeros(max_len, d_model)
        position = torch.arange(0, max_len, dtype=torch.float).unsqueeze(1)
        div_term = torch.exp(
            torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model)
        )
        pe[:, 0::2] = torch.sin(position * div_term)
        pe[:, 1::2] = torch.cos(position * div_term)
        pe = pe.unsqueeze(0)
        self.register_buffer('pe', pe)
        
    def forward(self, x):
        x = x + self.pe[:, :x.size(1), :]
        return self.dropout(x)


def test_positional_encoding():
    """测试位置编码模块"""
    torch.manual_seed(42)
    
    # 参数设置
    batch_size = 2
    seq_len = 10
    d_model = 512
    
    # 模拟词嵌入输入
    x = torch.randn(batch_size, seq_len, d_model)
    
    # 创建位置编码模块
    pe = SinusoidalPositionalEncoding(d_model=d_model, max_len=5000, dropout=0.0)
    
    # 前向传播
    output = pe(x)
    
    print("=" * 50)
    print("正弦位置编码测试")
    print("=" * 50)
    print(f"输入形状: {x.shape}")
    print(f"输出形状: {output.shape}")
    print(f"输入与输出形状一致: {x.shape == output.shape}")
    print(f"位置编码矩阵形状: {pe.pe.shape}")
    print(f"位置编码值范围: [{pe.pe.min():.4f}, {pe.pe.max():.4f}]")
    print("=" * 50)
    
    return pe.pe.squeeze(0)


def visualize_pe_heatmap(pe, save_path='07_chapter7_pe_heatmap.png'):
    """可视化位置编码热力图"""
    pe_np = pe.detach().cpu().numpy()
    
    plt.figure(figsize=(12, 6))
    plt.imshow(pe_np, aspect='auto', cmap='coolwarm')
    plt.colorbar(label='Encoding Value')
    plt.xlabel('Embedding Dimension')
    plt.ylabel('Token Position')
    plt.title('Sinusoidal Positional Encoding Heatmap')
    plt.tight_layout()
    plt.savefig(save_path, dpi=150, bbox_inches='tight')
    print(f"图片已保存为 {save_path}")


def visualize_pe_waveforms(pe, dims_to_plot=[0, 1, 30, 31, 100, 101, 300, 301]):
    """可视化特定维度的位置编码波形"""
    pe_np = pe.detach().cpu().numpy()
    seq_len = pe_np.shape[0]
    positions = np.arange(seq_len)
    
    fig, axes = plt.subplots(len(dims_to_plot), 1, figsize=(12, 2 * len(dims_to_plot)))
    
    for idx, dim in enumerate(dims_to_plot):
        axes[idx].plot(positions, pe_np[:, dim], linewidth=0.8)
        axes[idx].set_ylabel(f'Dim {dim}')
        axes[idx].set_xlim(0, seq_len)
        axes[idx].set_ylim(-1.1, 1.1)
        axes[idx].grid(True, alpha=0.3)
    
    axes[-1].set_xlabel('Token Position')
    fig.suptitle('Positional Encoding Waveforms (Selected Dimensions)', fontsize=14)
    plt.tight_layout()
    plt.savefig('07_chapter7_pe_waveforms.png', dpi=150, bbox_inches='tight')
    print("图片已保存为 07_chapter7_pe_waveforms.png")


if __name__ == "__main__":
    # 运行测试
    pe_matrix = test_positional_encoding()
    
    # 可视化热力图
    visualize_pe_heatmap(pe_matrix[:100, :128])
    
    # 可视化波形图
    visualize_pe_waveforms(pe_matrix[:200, :512])
