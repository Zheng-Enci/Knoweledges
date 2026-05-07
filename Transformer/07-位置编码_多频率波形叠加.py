"""
位置编码多频率波形叠加可视化
"""

import matplotlib.pyplot as plt
import numpy as np
import platform

system = platform.system()
if system == 'Windows':
    plt.rcParams['font.sans-serif'] = ['Microsoft YaHei', 'SimHei', 'DejaVu Sans']
elif system == 'Darwin':
    plt.rcParams['font.sans-serif'] = ['PingFang SC', 'Arial Unicode MS', 'DejaVu Sans']
else:
    plt.rcParams['font.sans-serif'] = ['WenQuanYi Micro Hei', 'Noto Sans CJK SC', 'DejaVu Sans']
plt.rcParams['axes.unicode_minus'] = False

seq_len = 20
positions = np.arange(seq_len)

freq_high = 1.0
freq_mid = 0.3
freq_low = 0.1

wave_high = np.sin(positions * freq_high)
wave_mid = np.sin(positions * freq_mid)
wave_low = np.sin(positions * freq_low)

wave_combined = wave_high * 0.5 + wave_mid * 0.3 + wave_low * 0.2

fig, axes = plt.subplots(4, 1, figsize=(14, 10), sharex=True)

axes[0].plot(positions, wave_high, 'o-', color='#FF6B6B', linewidth=2, markersize=6, label='High Freq (i=0)')
axes[0].set_ylabel('High Freq\n(i=0)', fontsize=11)
axes[0].set_title('High Frequency Wave (i=0): Fast changes, distinguishes nearby positions', fontsize=12, color='#FF6B6B')
axes[0].axhline(y=0, color='gray', linestyle='--', alpha=0.5)
axes[0].grid(True, alpha=0.3)
axes[0].set_ylim(-1.3, 1.3)

axes[1].plot(positions, wave_mid, 's-', color='#4ECDC4', linewidth=2, markersize=6, label='Mid Freq (i=1)')
axes[1].set_ylabel('Mid Freq\n(i=1)', fontsize=11)
axes[1].set_title('Medium Frequency Wave (i=1): Medium changes', fontsize=12, color='#4ECDC4')
axes[1].axhline(y=0, color='gray', linestyle='--', alpha=0.5)
axes[1].grid(True, alpha=0.3)
axes[1].set_ylim(-1.3, 1.3)

axes[2].plot(positions, wave_low, '^-', color='#45B7D1', linewidth=2, markersize=6, label='Low Freq (i=2)')
axes[2].set_ylabel('Low Freq\n(i=2)', fontsize=11)
axes[2].set_title('Low Frequency Wave (i=2): Slow changes, distinguishes distant positions', fontsize=12, color='#45B7D1')
axes[2].axhline(y=0, color='gray', linestyle='--', alpha=0.5)
axes[2].grid(True, alpha=0.3)
axes[2].set_ylim(-1.3, 1.3)

axes[3].plot(positions, wave_combined, 'D-', color='#9B59B6', linewidth=2.5, markersize=8)
axes[3].set_ylabel('Combined', fontsize=11)
axes[3].set_title('Combined Wave: Each position has a unique "fingerprint"', fontsize=12, color='#9B59B6')
axes[3].set_xlabel('Token Position', fontsize=12)
axes[3].axhline(y=0, color='gray', linestyle='--', alpha=0.5)
axes[3].grid(True, alpha=0.3)
axes[3].set_ylim(-1.3, 1.3)

for i, (h, m, l, c) in enumerate(zip(wave_high, wave_mid, wave_low, wave_combined)):
    axes[3].annotate(f'{c:.2f}', (i, c), textcoords="offset points", xytext=(0,10), ha='center', fontsize=8)

plt.suptitle('Positional Encoding: Multi-Frequency Wave Superposition', fontsize=14, fontweight='bold', y=1.02)
plt.tight_layout()
plt.savefig('07_positional_encoding_wave_superposition.png', dpi=150, bbox_inches='tight')
print("图片已保存为 07_positional_encoding_wave_superposition.png")
plt.close()

fig2, ax2 = plt.subplots(figsize=(14, 6))
ax2.plot(positions, wave_high, 'o-', color='#FF6B6B', linewidth=2, markersize=6, label='High Freq (i=0)', alpha=0.8)
ax2.plot(positions, wave_mid, 's-', color='#4ECDC4', linewidth=2, markersize=6, label='Mid Freq (i=1)', alpha=0.8)
ax2.plot(positions, wave_low, '^-', color='#45B7D1', linewidth=2, markersize=6, label='Low Freq (i=2)', alpha=0.8)
ax2.plot(positions, wave_combined, 'D-', color='#9B59B6', linewidth=3, markersize=8, label='Combined')
ax2.set_xlabel('Token Position', fontsize=12)
ax2.set_ylabel('Wave Value', fontsize=12)
ax2.set_title('Wave Superposition: All Frequencies Overlaid', fontsize=14, fontweight='bold')
ax2.axhline(y=0, color='gray', linestyle='--', alpha=0.5)
ax2.grid(True, alpha=0.3)
ax2.legend(loc='upper right', fontsize=10)
ax2.set_xlim(-0.5, seq_len-0.5)
ax2.set_ylim(-1.5, 1.5)

plt.tight_layout()
fig2.savefig('07_positional_encoding_wave_overlay.png', dpi=150, bbox_inches='tight')
print("图片已保存为 07_positional_encoding_wave_overlay.png")
plt.close()
