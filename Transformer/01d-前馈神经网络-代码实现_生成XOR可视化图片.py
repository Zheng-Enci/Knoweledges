"""
生成XOR问题相关可视化图片
"""

import matplotlib.pyplot as plt
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

# ==================== 图1：XOR数据点分布 ====================
fig1, ax1 = plt.subplots(figsize=(5, 5))

# 设置坐标轴范围：-1 到 2
ax1.set_xlim(-1.2, 2.2)
ax1.set_ylim(-1.2, 2.2)
ax1.set_aspect('equal')

# 绘制坐标轴（在-1处交叉，作为新的原点）
ax1.axhline(y=-1, color='black', linewidth=1.5)
ax1.axvline(x=-1, color='black', linewidth=1.5)

# 添加箭头
ax1.annotate('', xy=(2.2, -1), xytext=(2.1, -1),
             arrowprops=dict(arrowstyle='->', color='black', lw=1.5))
ax1.annotate('', xy=(-1, 2.2), xytext=(-1, 2.1),
             arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

# 坐标轴标签
ax1.text(2.2, -1.35, 'A (输入A)', fontsize=11, ha='center')
ax1.text(-1.35, 2.2, 'B (输入B)', fontsize=11, va='center')

# 刻度
ax1.set_xticks([-1, 0, 1, 2])
ax1.set_yticks([-1, 0, 1, 2])

# 数据点
# (0,1) - 绿色，输出1
ax1.plot(0, 1, 'o', color='#4CAF50', markersize=15, markeredgewidth=2, markeredgecolor='white')
ax1.text(0, 1.15, '(0,1)', fontsize=10, ha='center', fontweight='bold')
ax1.text(0, 0.85, '绿色', fontsize=9, ha='center', color='#666')

# (1,1) - 红色，输出0
ax1.plot(1, 1, 'o', color='#F44336', markersize=15, markeredgewidth=2, markeredgecolor='white')
ax1.text(1, 1.15, '(1,1)', fontsize=10, ha='center', fontweight='bold')
ax1.text(1, 0.85, '红色', fontsize=9, ha='center', color='#666')

# (0,0) - 红色，输出0
ax1.plot(0, 0, 'o', color='#F44336', markersize=15, markeredgewidth=2, markeredgecolor='white')
ax1.text(0, -0.2, '(0,0)', fontsize=10, ha='center', fontweight='bold')
ax1.text(0, -0.4, '红色', fontsize=9, ha='center', color='#666')

# (1,0) - 绿色，输出1
ax1.plot(1, 0, 'o', color='#4CAF50', markersize=15, markeredgewidth=2, markeredgecolor='white')
ax1.text(1, -0.2, '(1,0)', fontsize=10, ha='center', fontweight='bold')
ax1.text(1, -0.4, '绿色', fontsize=9, ha='center', color='#666')

# 网格
ax1.grid(True, alpha=0.3, linestyle='--')

# 图例说明
ax1.text(0.5, -1.35, '绿色 = 输出1，红色 = 输出0', fontsize=9, ha='center', color='#666')

ax1.set_title('XOR数据点分布', fontsize=12, fontweight='bold')

# 隐藏边框但保留刻度
for spine in ax1.spines.values():
    spine.set_visible(False)

# 调整布局，右下角留出额外空间用于水印
plt.subplots_adjust(right=0.85, bottom=0.15)
plt.savefig('01d-前馈神经网络-代码实现_XOR数据点分布.png', dpi=150)
print("✅ 图1已保存：01d-前馈神经网络-代码实现_XOR数据点分布.png")
plt.close()

# ==================== 图2：XOR数据点简化版 ====================
fig2, ax2 = plt.subplots(figsize=(4, 4))

# 设置坐标轴范围：-1 到 2
ax2.set_xlim(-1.2, 2.2)
ax2.set_ylim(-1.2, 2.2)
ax2.set_aspect('equal')

# 绘制坐标轴（在-1处交叉，作为新的原点）
ax2.axhline(y=-1, color='black', linewidth=1.5)
ax2.axvline(x=-1, color='black', linewidth=1.5)

# 添加箭头
ax2.annotate('', xy=(2.2, -1), xytext=(2.1, -1),
             arrowprops=dict(arrowstyle='->', color='black', lw=1.5))
ax2.annotate('', xy=(-1, 2.2), xytext=(-1, 2.1),
             arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

# 坐标轴标签（使用LaTeX格式渲染下标）
ax2.text(2.2, -1.35, r'$x_1$ (输入A)', fontsize=10, ha='center')
ax2.text(-1.35, 2.2, r'$x_2$ (输入B)', fontsize=10, va='center')

# 刻度
ax2.set_xticks([-1, 0, 1, 2])
ax2.set_yticks([-1, 0, 1, 2])

# 数据点
# A(0,1) - 绿色
ax2.plot(0, 1, 'o', color='#4CAF50', markersize=12, markeredgewidth=2, markeredgecolor='white')
ax2.text(0.15, 1.05, '(A)', fontsize=10, fontweight='bold', color='#4CAF50')

# B(1,1) - 红色
ax2.plot(1, 1, 'o', color='#F44336', markersize=12, markeredgewidth=2, markeredgecolor='white')
ax2.text(1.15, 1.05, '(B)', fontsize=10, fontweight='bold', color='#F44336')

# C(0,0) - 红色
ax2.plot(0, 0, 'o', color='#F44336', markersize=12, markeredgewidth=2, markeredgecolor='white')
ax2.text(0.15, -0.15, '(C)', fontsize=10, fontweight='bold', color='#F44336')

# D(1,0) - 绿色
ax2.plot(1, 0, 'o', color='#4CAF50', markersize=12, markeredgewidth=2, markeredgecolor='white')
ax2.text(1.15, -0.15, '(D)', fontsize=10, fontweight='bold', color='#4CAF50')

# 网格
ax2.grid(True, alpha=0.3, linestyle='--')

ax2.set_title('XOR数据点', fontsize=12, fontweight='bold')

# 隐藏边框但保留刻度
for spine in ax2.spines.values():
    spine.set_visible(False)

# 调整布局，右下角留出额外空间用于水印
plt.subplots_adjust(right=0.85, bottom=0.15)
plt.savefig('01d-前馈神经网络-代码实现_XOR数据点简化.png', dpi=150)
print("✅ 图2已保存：01d-前馈神经网络-代码实现_XOR数据点简化.png")
plt.close()

# ==================== 图3：XOR解决方案 - 两条直线分离 ====================
fig3, ax3 = plt.subplots(figsize=(5, 5))

# 设置坐标轴范围：-1 到 2
ax3.set_xlim(-1.2, 2.2)
ax3.set_ylim(-1.2, 2.2)
ax3.set_aspect('equal')

# 绘制坐标轴（在-1处交叉，作为新的原点）
ax3.axhline(y=-1, color='black', linewidth=1.5)
ax3.axvline(x=-1, color='black', linewidth=1.5)

# 添加箭头
ax3.annotate('', xy=(2.2, -1), xytext=(2.1, -1),
             arrowprops=dict(arrowstyle='->', color='black', lw=1.5))
ax3.annotate('', xy=(-1, 2.2), xytext=(-1, 2.1),
             arrowprops=dict(arrowstyle='->', color='black', lw=1.5))

# 坐标轴标签（使用LaTeX格式渲染下标）
ax3.text(2.2, -1.35, r'$x_1$', fontsize=11, ha='center')
ax3.text(-1.35, 2.2, r'$x_2$', fontsize=11, va='center')

# 刻度
ax3.set_xticks([-1, 0, 1, 2])
ax3.set_yticks([-1, 0, 1, 2])

# 数据点
# A(0,1) - 绿色
ax3.plot(0, 1, 'o', color='#4CAF50', markersize=15, markeredgewidth=2, markeredgecolor='white')
ax3.text(0.15, 1.05, 'A(0,1)', fontsize=10, fontweight='bold')

# B(1,1) - 红色
ax3.plot(1, 1, 'o', color='#F44336', markersize=15, markeredgewidth=2, markeredgecolor='white')
ax3.text(1.15, 1.05, 'B(1,1)', fontsize=10, fontweight='bold')

# C(0,0) - 红色
ax3.plot(0, 0, 'o', color='#F44336', markersize=15, markeredgewidth=2, markeredgecolor='white')
ax3.text(0.15, -0.15, 'C(0,0)', fontsize=10, fontweight='bold')

# D(1,0) - 绿色
ax3.plot(1, 0, 'o', color='#4CAF50', markersize=15, markeredgewidth=2, markeredgecolor='white')
ax3.text(1.15, -0.15, 'D(1,0)', fontsize=10, fontweight='bold')

# 第一条线：x₁+x₂=0.5，从(-1, 1.5)到(2, -1)
x1_line1 = np.array([-1, 2])
y1_line1 = 0.5 - x1_line1
ax3.plot(x1_line1, y1_line1, color='#2196F3', linewidth=2, linestyle='-')
ax3.text(-0.8, 1.6, r'$x_1+x_2=0.5$', fontsize=9, color='#2196F3', fontweight='bold')

# 第二条线：x₁+x₂=1.5，从(-0.5, 2)到(2, -0.5)
x1_line2 = np.array([-0.5, 2])
y1_line2 = 1.5 - x1_line2
ax3.plot(x1_line2, y1_line2, color='#2196F3', linewidth=2, linestyle='-')
ax3.text(1.2, 0.4, r'$x_1+x_2=1.5$', fontsize=9, color='#2196F3', fontweight='bold')

# 网格
ax3.grid(True, alpha=0.3, linestyle='--')

ax3.set_title('XOR解决方案：两条直线分离', fontsize=12, fontweight='bold')

# 隐藏边框但保留刻度
for spine in ax3.spines.values():
    spine.set_visible(False)

# 调整布局，右下角留出额外空间用于水印
plt.subplots_adjust(right=0.85, bottom=0.15)
plt.savefig('01d-前馈神经网络-代码实现_XOR解决方案.png', dpi=150)
print("✅ 图3已保存：01d-前馈神经网络-代码实现_XOR解决方案.png")
plt.close()

print("\n🎉 所有图片生成完成！")
