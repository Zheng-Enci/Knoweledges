"""
07-位置编码 - 第5章代码
位置编码的可视化（热力图和波形图）
"""

import matplotlib.pyplot as plt
import torch
import math
import numpy as np

# 设置 Matplotlib 支持中文显示
plt.rcParams['font.sans-serif'] = ['SimHei', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False


def get_sinusoidal_pe(seq_len, d_model):
    """生成正弦位置编码矩阵 [seq_len, d_model]"""
    pe = torch.zeros(seq_len, d_model)
    position = torch.arange(0, seq_len, dtype=torch.float).unsqueeze(1)
    div_term = torch.exp(
        torch.arange(0, d_model, 2).float() * (-math.log(10000.0) / d_model)
    )
    pe[:, 0::2] = torch.sin(position * div_term)
    pe[:, 1::2] = torch.cos(position * div_term)
    return pe


def visualize_pe_heatmap(pe, save_path='07_chapter5_pe_heatmap.png'):
    """
    可视化位置编码热力图
    
    参数:
        pe: 位置编码矩阵 [seq_len, d_model]
        save_path: 图片保存路径
    """
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


def visualize_pe_waveforms(pe, dims_to_plot=[0, 1, 10, 11, 30, 31, 60, 61]):
    """
    可视化特定维度的位置编码波形
    
    参数:
        pe: 位置编码矩阵 [seq_len, d_model]
        dims_to_plot: 要绘制的维度索引列表
    """
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
    plt.savefig('07_chapter5_pe_waveforms.png', dpi=150, bbox_inches='tight')
    print("图片已保存为 07_chapter5_pe_waveforms.png")


# ========== 运行可视化 ==========
if __name__ == "__main__":
    seq_len, d_model = 100, 128
    pe = get_sinusoidal_pe(seq_len, d_model)
    
    print("生成热力图...")
    visualize_pe_heatmap(pe)
    
    print("\n生成波形图...")
    visualize_pe_waveforms(pe)
