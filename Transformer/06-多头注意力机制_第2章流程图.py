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
    
    fig, ax = plt.subplots(figsize=(14, 10))
    ax.set_xlim(0, 12)
    ax.set_ylim(0, 10)
    ax.set_aspect('equal')
    ax.axis('off')
    
    # 标题
    ax.text(6, 9.5, '多头注意力机制计算流程图', fontsize=18, fontweight='bold', 
            ha='center', va='center', color='#2c3e50')
    
    # ==================== 步骤1: 输入序列 ====================
    draw_step_box(ax, 6, 8.5, 3, 0.8, '#e8f5e8', '#1b5e20', 
                  '输入序列 X', '[batch, seq_len, 512]', 1)
    
    # ==================== 步骤2: 线性投影 ====================
    draw_step_box(ax, 6, 7.2, 3, 0.8, '#e1f5fe', '#01579b', 
                  '线性投影', 'Q = X × W^Q, K = X × W^K, V = X × W^V', 2)
    
    # 箭头
    ax.annotate('', xy=(6, 7.2), xytext=(6, 8.5), 
                arrowprops=dict(arrowstyle='->', color='#7f8c8d', lw=2))
    
    # ==================== 步骤3: 多头拆分 ====================
    draw_step_box(ax, 6, 5.9, 3, 0.8, '#e1f5fe', '#01579b', 
                  '多头拆分', '512 → 8×64 | [batch, 8, seq_len, 64]', 3)
    
    # 箭头
    ax.annotate('', xy=(6, 5.9), xytext=(6, 7.2), 
                arrowprops=dict(arrowstyle='->', color='#7f8c8d', lw=2))
    
    # ==================== 并行计算标题 ====================
    ax.text(6, 5.2, '↓ 并行注意力计算开始 ↓', fontsize=12, fontweight='bold', 
            ha='center', va='center', color='#7f8c8d')
    
    # ==================== 步骤4: 并行注意力计算 ====================
    # 8个注意力头
    head_positions = [
        (1.5, 4.0, '头1', 'Attention(Q₁,K₁,V₁)', '语法关系'),
        (3.5, 4.0, '头2', 'Attention(Q₂,K₂,V₂)', '语义关系'),
        (5.5, 4.0, '头3', 'Attention(Q₃,K₃,V₃)', '长距离依赖'),
        (7.5, 4.0, '头4', 'Attention(Q₄,K₄,V₄)', '局部模式'),
        (9.5, 4.0, '头5', 'Attention(Q₅,K₅,V₅)', '情感色彩'),
        (1.5, 2.5, '头6', 'Attention(Q₆,K₆,V₆)', '指代关系'),
        (3.5, 2.5, '头7', 'Attention(Q₇,K₇,V₇)', '位置信息'),
        (5.5, 2.5, '头8', 'Attention(Q₈,K₈,V₈)', '其他模式'),
    ]
    
    for i, (x, y, title, formula, desc) in enumerate(head_positions):
        draw_head_box(ax, x, y, title, formula, desc, i+1)
    
    # 并行计算区域框
    parallel_box = FancyBboxPatch((0.8, 1.8), 10.4, 2.8, 
                                 boxstyle="round,pad=0.1", 
                                 facecolor='#f3e5f5', edgecolor='#4a148c', 
                                 linewidth=2, alpha=0.3)
    ax.add_patch(parallel_box)
    ax.text(6, 1.5, '并行注意力计算 (8个头)', fontsize=12, fontweight='bold', 
            ha='center', va='center', color='#4a148c')
    
    # ==================== 并行计算结束 ====================
    ax.text(6, 1.0, '↓ 并行计算结束 ↓', fontsize=12, fontweight='bold', 
            ha='center', va='center', color='#7f8c8d')
    
    # ==================== 步骤5: 拼接输出 ====================
    draw_step_box(ax, 6, 0.2, 3, 0.8, '#e1f5fe', '#01579b', 
                  '拼接输出', 'Concat(head₁...head₈) | [batch, seq_len, 512]', 5)
    
    # 箭头
    ax.annotate('', xy=(6, 0.2), xytext=(6, 1.0), 
                arrowprops=dict(arrowstyle='->', color='#7f8c8d', lw=2))
    
    # ==================== 步骤6: 输出投影 ====================
    draw_step_box(ax, 6, -1.1, 3, 0.8, '#e1f5fe', '#01579b', 
                  '输出投影', 'Output = Concat × W^O', 6)
    
    # 箭头
    ax.annotate('', xy=(6, -1.1), xytext=(6, 0.2), 
                arrowprops=dict(arrowstyle='->', color='#7f8c8d', lw=2))
    
    # ==================== 步骤7: 最终输出 ====================
    draw_step_box(ax, 6, -2.4, 3, 0.8, '#fff3e0', '#e65100', 
                  '最终输出', '[batch, seq_len, 512]', 7)
    
    # 箭头
    ax.annotate('', xy=(6, -2.4), xytext=(6, -1.1), 
                arrowprops=dict(arrowstyle='->', color='#7f8c8d', lw=2))
    
    # ==================== 公式区域 ====================
    formula_box = FancyBboxPatch((0.5, -3.8), 11, 1.2, 
                                boxstyle="round,pad=0.1", 
                                facecolor='#fff3cd', edgecolor='#ffc107', 
                                linewidth=2)
    ax.add_patch(formula_box)
    
    formula_text = r'$\text{MultiHead}(Q,K,V) = \text{Concat}(\text{head}_1,...,\text{head}_8)W^O$'
    ax.text(6, -3.3, formula_text, fontsize=14, ha='center', va='center', 
            color='#2c3e50', fontweight='bold')
    
    formula_text2 = r'$\text{head}_i = \text{Attention}(QW_i^Q, KW_i^K, VW_i^V)$'
    ax.text(6, -4.0, formula_text2, fontsize=12, ha='center', va='center', 
            color='#2c3e50')
    
    # ==================== 技术要点说明 ====================
    tech_text = [
        "• 并行计算机制：8个注意力头同时独立计算，每个头有独立的投影矩阵",
        "• 维度拆分：512维输入拆分为8个64维子空间（512 = 8 × 64）", 
        "• 功能分化：不同头从随机初始化开始，自然学习关注不同的关系模式",
        "• 计算效率：总计算量与单头注意力相当，但表达能力显著增强",
        "• 维度保持：输入输出维度相同，便于Transformer层间堆叠"
    ]
    
    tech_box = FancyBboxPatch((0.5, -5.2), 11, 2.0, 
                             boxstyle="round,pad=0.1", 
                             facecolor='#e8f6f3', edgecolor='#1abc9c', 
                             linewidth=2)
    ax.add_patch(tech_box)
    
    ax.text(6, -4.8, '技术要点说明', fontsize=14, fontweight='bold', 
            ha='center', va='center', color='#16a085')
    
    for i, text in enumerate(tech_text):
        ax.text(1.0, -5.0 - i*0.3, text, fontsize=10, ha='left', va='center', 
                color='#2c3e50')
    
    plt.tight_layout()
    plt.savefig('06-多头注意力机制_第2章流程图.png', dpi=300, bbox_inches='tight', 
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
    box = FancyBboxPatch((x - 1.2, y - 0.6), 2.4, 1.2, 
                        boxstyle="round,pad=0.1", 
                        facecolor='#74b9ff', edgecolor='#0984e3', 
                        linewidth=1.5)
    ax.add_patch(box)
    
    # 头编号
    ax.text(x - 1.0, y + 0.4, title, fontsize=10, fontweight='bold', 
            ha='left', va='center', color='white')
    
    # 公式
    ax.text(x, y + 0.1, formula, fontsize=8, ha='center', va='center', 
            color='white', fontfamily='monospace')
    
    # 描述
    ax.text(x, y - 0.3, desc, fontsize=9, ha='center', va='center', 
            color='white')

if __name__ == "__main__":
    draw_multihead_attention_flowchart()
    print("多头注意力机制流程图已生成: 06-多头注意力机制_第2章流程图.png")