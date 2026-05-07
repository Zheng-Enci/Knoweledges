"""
多头注意力机制计算流程图可视化
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
from matplotlib.patches import FancyBboxPatch
import numpy as np
import platform

# 设置中文字体和数学符号
system = platform.system()
if system == 'Windows':
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
elif system == 'Darwin':
    plt.rcParams['font.sans-serif'] = ['PingFang SC', 'Arial Unicode MS', 'DejaVu Sans']
else:
    plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'Noto Sans CJK SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False
plt.rcParams['mathtext.fontset'] = 'cm'

def draw_multihead_attention_flowchart():
    """绘制多头注意力机制计算流程图"""
    
    fig, ax = plt.subplots(figsize=(16, 14))
    ax.set_xlim(0, 14)
    ax.set_ylim(0, 13)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # 标题
    ax.text(7, 12.5, 'Multi-Head Attention Flowchart', fontsize=20, fontweight='bold', 
            ha='center', va='center', color='#2c3e50')
    
    # ==================== 步骤1: 输入序列 ====================
    draw_step_box(ax, 7, 11.0, 4, 0.9, '#e8f5e8', '#1b5e20', 
                  'Input Sequence X', '[batch, seq_len, 512]', 1)
    
    # ==================== 步骤2: 线性投影 ====================
    draw_step_box(ax, 7, 9.2, 4, 0.9, '#e1f5fe', '#01579b', 
                  'Linear Projection', 'Q = X × W^Q, K = X × W^K, V = X × W^V', 2)
    
    # 箭头
    ax.annotate('', xy=(7, 9.2), xytext=(7, 11.0), 
                arrowprops=dict(arrowstyle='->', color='#7f8c8d', lw=2))
    
    # ==================== 步骤3: 多头拆分 ====================
    draw_step_box(ax, 7, 7.4, 4, 0.9, '#e1f5fe', '#01579b', 
                  'Multi-Head Split', '512 → 8×64 | [batch, 8, seq_len, 64]', 3)
    
    # 箭头
    ax.annotate('', xy=(7, 7.4), xytext=(7, 9.2), 
                arrowprops=dict(arrowstyle='->', color='#7f8c8d', lw=2))
    
    # ==================== 并行计算标题 ====================
    ax.text(7, 6.6, '↓ Parallel Attention Computation Starts ↓', fontsize=14, fontweight='bold', 
            ha='center', va='center', color='#7f8c8d')
    
    # ==================== 步骤4: 并行注意力计算 ====================
    # 8个注意力头
    head_positions = [
        (2.5, 5.0, 'Head 1', 'Attention(Q₁,K₁,V₁)', 'Syntax'),
        (5.0, 5.0, 'Head 2', 'Attention(Q₂,K₂,V₂)', 'Semantics'),
        (7.5, 5.0, 'Head 3', 'Attention(Q₃,K₃,V₃)', 'Long-range'),
        (10.0, 5.0, 'Head 4', 'Attention(Q₄,K₄,V₄)', 'Local'),
        (2.5, 3.0, 'Head 5', 'Attention(Q₅,K₅,V₅)', 'Emotion'),
        (5.0, 3.0, 'Head 6', 'Attention(Q₆,K₆,V₆)', 'Reference'),
        (7.5, 3.0, 'Head 7', 'Attention(Q₇,K₇,V₇)', 'Position'),
        (10.0, 3.0, 'Head 8', 'Attention(Q₈,K₈,V₈)', 'Other'),
    ]
    
    for i, (x, y, title, formula, desc) in enumerate(head_positions):
        draw_head_box(ax, x, y, title, formula, desc, i+1)
    
    # 并行计算区域框
    parallel_box = FancyBboxPatch((1.5, 2.2), 11.0, 3.6, 
                                 boxstyle="round,pad=0.1", 
                                 facecolor='#f3e5f5', edgecolor='#4a148c', 
                                 linewidth=2, alpha=0.3)
    ax.add_patch(parallel_box)
    ax.text(7, 1.8, 'Parallel Attention Computation (8 Heads)', fontsize=14, fontweight='bold', 
            ha='center', va='center', color='#4a148c')
    
    # ==================== 并行计算结束 ====================
    ax.text(7, 1.2, '↓ Parallel Computation Ends ↓', fontsize=14, fontweight='bold', 
            ha='center', va='center', color='#7f8c8d')
    
    # ==================== 步骤5: 拼接输出 ====================
    draw_step_box(ax, 7, -0.2, 4, 0.9, '#e1f5fe', '#01579b', 
                  'Concatenation', 'Concat(head₁...head₈) | [batch, seq_len, 512]', 5)
    
    # 箭头
    ax.annotate('', xy=(7, -0.2), xytext=(7, 1.2), 
                arrowprops=dict(arrowstyle='->', color='#7f8c8d', lw=2))
    
    # ==================== 步骤6: 输出投影 ====================
    draw_step_box(ax, 7, -1.8, 4, 0.9, '#e1f5fe', '#01579b', 
                  'Output Projection', 'Output = Concat × W^O', 6)
    
    # 箭头
    ax.annotate('', xy=(7, -1.8), xytext=(7, -0.2), 
                arrowprops=dict(arrowstyle='->', color='#7f8c8d', lw=2))
    
    # ==================== 步骤7: 最终输出 ====================
    draw_step_box(ax, 7, -3.4, 4, 0.9, '#fff3e0', '#e65100', 
                  'Final Output', '[batch, seq_len, 512]', 7)
    
    # 箭头
    ax.annotate('', xy=(7, -3.4), xytext=(7, -1.8), 
                arrowprops=dict(arrowstyle='->', color='#7f8c8d', lw=2))
    
    # ==================== 公式区域 ====================
    formula_box = FancyBboxPatch((7 - 2, -5.0), 4, 1.5, 
                                boxstyle="round,pad=0.1", 
                                facecolor='#fff3cd', edgecolor='#ffc107', 
                                linewidth=2)
    ax.add_patch(formula_box)
    
    formula_text = r'$\text{MultiHead}(Q,K,V) = \text{Concat}(\text{head}_1,...,\text{head}_8)W^O$'
    ax.text(7, -4.6, formula_text, fontsize=16, ha='center', va='center', 
            color='#2c3e50', fontweight='bold')
    
    formula_text2 = r'$\text{head}_i = \text{Attention}(QW_i^Q, KW_i^K, VW_i^V)$'
    ax.text(7, -5.4, formula_text2, fontsize=14, ha='center', va='center', 
            color='#2c3e50')
    
    plt.tight_layout()
    plt.savefig('06-multihead_attention_flowchart.png', dpi=300, bbox_inches='tight', 
                facecolor='white', edgecolor='none')
    plt.show()

def draw_step_box(ax, x, y, width, height, facecolor, edgecolor, title, desc, step_num):
    """绘制步骤框"""
    # 步骤框
    box = FancyBboxPatch((x - width/2, y - height/2), width, height, 
                        boxstyle="round,pad=0.1", 
                        facecolor=facecolor, edgecolor=edgecolor, 
                        linewidth=2)
    ax.add_patch(box)
    
    # 步骤编号
    ax.text(x - width/2 + 0.2, y + height/2 - 0.15, f'{step_num}', 
            fontsize=10, fontweight='bold', ha='left', va='top', 
            color='white', 
            bbox=dict(boxstyle="circle,pad=0.3", facecolor='#3498db', 
                     edgecolor='none'))
    
    # 标题
    ax.text(x, y + 0.15, title, fontsize=12, fontweight='bold', 
            ha='center', va='center', color=edgecolor)
    
    # 描述
    ax.text(x, y - 0.15, desc, fontsize=10, ha='center', va='center', 
            color='#2c3e50')

def draw_head_box(ax, x, y, title, formula, desc, head_num):
    """绘制注意力头框"""
    # 头框
    box = FancyBboxPatch((x - 1.5, y - 0.8), 3.0, 1.6, 
                        boxstyle="round,pad=0.1", 
                        facecolor='#74b9ff', edgecolor='#0984e3', 
                        linewidth=1.5)
    ax.add_patch(box)
    
    # 头编号
    ax.text(x - 1.3, y + 0.5, title, fontsize=12, fontweight='bold', 
            ha='left', va='center', color='white')
    
    # 公式
    ax.text(x, y + 0.1, formula, fontsize=10, ha='center', va='center', 
            color='white', fontfamily='monospace')
    
    # 描述
    ax.text(x, y - 0.4, desc, fontsize=11, ha='center', va='center', 
            color='white')

if __name__ == "__main__":
    draw_multihead_attention_flowchart()
    print("多头注意力机制流程图已生成: 06-多头注意力机制_第2章流程图.png")