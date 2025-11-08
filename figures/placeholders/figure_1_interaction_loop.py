#!/usr/bin/env python3
"""
Figure 1: GestureFlow Interaction Loop (CHI Poster版)
环形箭头设计，体现Perception → Interpretation → Gentle Support → Reflection
"""

import matplotlib.pyplot as plt
import matplotlib.patches as patches
import numpy as np
from pathlib import Path

def create_interaction_loop_figure():
    """创建交互循环图表"""
    fig, ax = plt.subplots(figsize=(10, 10), facecolor='white')
    ax.set_xlim(0, 10)
    ax.set_ylim(0, 10)
    ax.axis('off')

    # 环形布局参数
    center = (5, 5)
    radius = 3.5

    # 四个阶段位置
    positions = {
        'Perception': (8.5, 5),      # 右
        'Interpretation': (5, 1.5),  # 下
        'Gentle Support': (1.5, 5),  # 左
        'Reflection': (5, 8.5)       # 上
    }

    # 定义颜色
    colors = {
        'Perception': '#4A90E2',       # 蓝色
        'Interpretation': '#7B68EE',   # 紫色
        'Gentle Support': '#50C878',  # 绿色
        'Reflection': '#F39C12'       # 橙色
    }

    # 绘制环形箭头
    theta_start = 0
    theta_step = 2 * np.pi / 4

    for i, (phase, pos) in enumerate(positions.items()):
        # 计算箭头位置
        theta_mid = theta_start + i * theta_step + theta_step/2
        theta_start_arrow = theta_start + i * theta_step + theta_step/3
        theta_end_arrow = theta_start + (i+1) * theta_step - theta_step/3

        # 绘制圆弧箭头
        arrow = patches.FancyArrowPatch(
            (center[0] + radius * np.cos(theta_start_arrow),
             center[1] + radius * np.sin(theta_start_arrow)),
            (center[0] + radius * np.cos(theta_end_arrow),
             center[1] + radius * np.sin(theta_end_arrow)),
            arrowstyle='->', mutation_scale=25,
            linewidth=3, color=colors[phase],
            alpha=0.8
        )
        ax.add_patch(arrow)

    # 绘制四个阶段节点
    for phase, pos in positions.items():
        # 外圈
        circle = plt.Circle(pos, 0.8, color=colors[phase], alpha=0.2)
        ax.add_patch(circle)

        # 内圈
        circle_inner = plt.Circle(pos, 0.6, color=colors[phase], alpha=0.6)
        ax.add_patch(circle_inner)

        # 标题
        ax.text(pos[0], pos[1], phase,
                fontsize=14, fontweight='bold',
                ha='center', va='center', color='white')

    # 中心标题
    ax.text(center[0], center[1], 'GestureFlow\nInteraction Loop',
            fontsize=18, fontweight='bold',
            ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgray', alpha=0.5))

    # 添加详细说明
    descriptions = {
        'Perception': 'EMG+GSR\nSensing\nNatural Hand\nMovements',
        'Interpretation': 'CEI Algorithm\nState Classification\nWork/Rest/Leisure',
        'Gentle Support': 'Ambient\nInterventions\nWind/Water/Light\nMicro-tasks',
        'Reflection': 'User Awareness\nSelf-regulation\nCo-regulated\nCalmness'
    }

    for phase, pos in positions.items():
        # 调整文本位置
        if phase == 'Perception':
            text_pos = (pos[0] + 1.2, pos[1])
        elif phase == 'Interpretation':
            text_pos = (pos[0], pos[1] - 1.2)
        elif phase == 'Gentle Support':
            text_pos = (pos[0] - 1.2, pos[1])
        else:  # Reflection
            text_pos = (pos[0], pos[1] + 1.2)

        ax.text(text_pos[0], text_pos[1], descriptions[phase],
                fontsize=10, ha='center', va='center',
                bbox=dict(boxstyle="round,pad=0.3", facecolor=colors[phase], alpha=0.2))

    # 添加技术参数说明
    tech_text = """Technical Specifications:
• EMG: 8 channels @ 1kHz → Hand movement patterns
• GSR: 1 channel @ 100Hz → Arousal levels
• CEI: 0.6*z(EMG_RMS) + 0.4*z(GSR_slope)
• Latency: <100ms real-time processing"""

    ax.text(5, 0.2, tech_text,
            fontsize=9, ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.5", facecolor='lightblue', alpha=0.3))

    # 添加设计理念
    design_text = """Design Philosophy:
Sensing-rather-than-controlling
Embodied awareness through natural movements
Ambient support preserving user agency
Co-regulated calmness through gentle mirroring"""

    ax.text(5, 9.8, design_text,
            fontsize=9, ha='center', va='center',
            bbox=dict(boxstyle="round,pad=0.5", facecolor='lightgreen', alpha=0.3))

    plt.title('GestureFlow Interaction Loop: Embodied Sensing to Ambient Support',
             fontsize=16, fontweight='bold', pad=20)

    return fig

def main():
    """生成并保存图表"""
    print("🎨 生成Figure 1: GestureFlow Interaction Loop")

    # 创建图表
    fig = create_interaction_loop_figure()

    # 保存
    output_dir = Path('./figures')
    output_dir.mkdir(exist_ok=True)

    output_file = output_dir / 'figure_1_interaction_loop.png'
    fig.savefig(output_file, dpi=300, bbox_inches='tight', facecolor='white')

    print(f"✅ 图表已保存: {output_file}")
    print("📊 特点:")
    print("   - 环形箭头设计体现循环特性")
    print("   - 四阶段颜色编码清晰")
    print("   - 包含技术参数和设计理念")
    print("   - 符合CHI Poster可视化标准")

if __name__ == "__main__":
    main()