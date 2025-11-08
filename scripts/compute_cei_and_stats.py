#!/usr/bin/env python3
"""
GestureFlow CEI计算和统计分析脚本
严格限制：仅使用1路sEMG (200Hz) + 1路GSR (4-10Hz)
专注于CHI Poster所需的关键统计和可视化
"""

import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
from scipy import stats
from pathlib import Path

class GestureFlowAnalyzer:
    def __init__(self, sampling_rate_emg=200, sampling_rate_gsr=4):
        """
        初始化分析器
        Args:
            sampling_rate_emg: EMG采样率 (Hz)
            sampling_rate_gsr: GSR采样率 (Hz)
        """
        self.fs_emg = sampling_rate_emg
        self.fs_gsr = sampling_rate_gsr

    def load_calibration_data(self, emg_rest, emg_grip, gsr_rest, gsr_grip):
        """
        加载校准数据并计算阈值
        Args:
            emg_rest: 静息期EMG数据
            emg_grip: 握拳期EMG数据
            gsr_rest: 静息期GSR数据
            gsr_grip: 激活期GSR数据
        """
        # EMG特征提取
        emg_rest_rms = self.compute_rms(emg_rest)
        emg_grip_rms = self.compute_rms(emg_grip)

        # GSR特征提取
        gsr_rest_slope = self.compute_slope(gsr_rest)
        gsr_grip_slope = self.compute_slope(gsr_grip)

        # 计算个体化阈值 (p10-p90)
        self.emg_threshold = np.percentile([emg_rest_rms, emg_grip_rms], 90)
        self.gsr_threshold = np.percentile([gsr_rest_slope, gsr_grip_slope], 90)

        # 存储校准参数
        self.calibration = {
            'emg_rest_mean': np.mean(emg_rest_rms),
            'emg_grip_mean': np.mean(emg_grip_rms),
            'gsr_rest_mean': np.mean(gsr_rest_slope),
            'gsr_grip_mean': np.mean(gsr_grip_slope),
            'emg_threshold': self.emg_threshold,
            'gsr_threshold': self.gsr_threshold
        }

    def compute_rms(self, signal, window_size=1.0):
        """
        计算RMS (均方根)
        Args:
            signal: 输入信号
            window_size: 窗口大小 (秒)
        Returns:
            RMS值数组
        """
        samples_per_window = int(window_size * self.fs_emg)
        rms_values = []

        for i in range(0, len(signal) - samples_per_window, samples_per_window // 2):
            window = signal[i:i + samples_per_window]
            rms = np.sqrt(np.mean(window ** 2))
            rms_values.append(rms)

        return np.array(rms_values)

    def compute_slope(self, signal, window_size=5.0):
        """
        计算GSR斜率特征
        Args:
            signal: 输入GSR信号
            window_size: 窗口大小 (秒)
        Returns:
            斜率值数组
        """
        samples_per_window = int(window_size * self.fs_gsr)
        slopes = []

        for i in range(0, len(signal) - samples_per_window, samples_per_window // 2):
            window = signal[i:i + samples_per_window]
            time_axis = np.arange(len(window)) / self.fs_gsr
            if len(window) > 1:
                slope = np.polyfit(time_axis, window, 1)[0]
                slopes.append(slope)

        return np.array(slopes)

    def compute_cei(self, emg_data, gsr_data):
        """
        计算CEI (Combination Embodied Index)
        CEI = 0.6 * z(RMS_EMG) + 0.4 * z(slope_GSR)
        Args:
            emg_data: EMG数据
            gsr_data: GSR数据
        Returns:
            CEI时间序列
        """
        # 计算特征
        emg_rms = self.compute_rms(emg_data)
        gsr_slope = self.compute_slope(gsr_data)

        # 归一化处理
        emg_norm = (emg_rms - self.calibration['emg_rest_mean']) / (self.calibration['emg_grip_mean'] - self.calibration['emg_rest_mean'])
        gsr_norm = (gsr_slope - self.calibration['gsr_rest_mean']) / (self.calibration['gsr_grip_mean'] - self.calibration['gsr_rest_mean'])

        # 限制在[0,1]范围内
        emg_norm = np.clip(emg_norm, 0, 1)
        gsr_norm = np.clip(gsr_norm, 0, 1)

        # 计算CEI
        cei = 0.6 * emg_norm + 0.4 * gsr_norm

        return cei

    def analyze_focus_duration(self, window_events, session_data):
        """
        分析专注时长
        Args:
            window_events: 窗口切换事件
            session_data: 会话数据
        Returns:
            专注统计结果
        """
        focus_durations = []
        current_app = None
        focus_start = None

        for event in window_events:
            if event['type'] == 'focus':
                if current_app is None:
                    focus_start = event['timestamp']
                current_app = event['app']

            elif event['type'] == 'blur':
                if focus_start is not None:
                    duration = event['timestamp'] - focus_start
                    if duration > 60:  # 只计算>1分钟的专注时间
                        focus_durations.append({
                            'app': current_app,
                            'duration': duration,
                            'timestamp': focus_start
                        })
                    focus_start = None
                    current_app = None

        return focus_durations

    def statistical_analysis(self, condition_A_data, condition_B_data):
        """
        执行统计分析 (配对t检验/Wilcoxon)
        Args:
            condition_A_data: 对照组数据
            condition_B_data: 干预组数据
        Returns:
            统计结果字典
        """
        results = {}

        # 专注时长比较
        if len(condition_A_data['focus_durations']) > 0 and len(condition_B_data['focus_durations']) > 0:
            A_focus = [d['duration'] for d in condition_A_data['focus_durations']]
            B_focus = [d['duration'] for d in condition_B_data['focus_durations']]

            # 配对t检验
            t_stat, p_value = stats.ttest_rel(A_focus, B_focus)
            effect_size = (np.mean(B_focus) - np.mean(A_focus)) / np.std(np.array(A_focus) - np.array(B_focus), ddof=1)

            results['focus_duration'] = {
                'A_mean': np.mean(A_focus),
                'B_mean': np.mean(B_focus),
                'improvement_percent': ((np.mean(B_focus) - np.mean(A_focus)) / np.mean(A_focus)) * 100,
                't_statistic': t_stat,
                'p_value': p_value,
                'effect_size': effect_size,
                'significant': p_value < 0.05
            }

        # CEI变化分析
        if 'pre_intervention_cei' in condition_B_data and 'post_intervention_cei' in condition_B_data:
            pre_cei = condition_B_data['pre_intervention_cei']
            post_cei = condition_B_data['post_intervention_cei']

            t_stat, p_value = stats.ttest_rel(pre_cei, post_cei)

            results['cei_change'] = {
                'pre_mean': np.mean(pre_cei),
                'post_mean': np.mean(post_cei),
                'reduction_percent': ((np.mean(pre_cei) - np.mean(post_cei)) / np.mean(pre_cei)) * 100,
                't_statistic': t_stat,
                'p_value': p_value,
                'significant': p_value < 0.05
            }

        return results

    def generate_visualizations(self, results, output_dir='./figures'):
        """
        生成CHI论文所需的可视化图表
        Args:
            results: 分析结果
            output_dir: 输出目录
        """
        output_path = Path(output_dir)
        output_path.mkdir(exist_ok=True)

        # 图1: 专注时长对比 (A/B条件)
        if 'focus_duration' in results:
            fig, (ax1, ax2) = plt.subplots(1, 2, figsize=(12, 5))

            # 左侧：个人对比图
            participants = results['focus_duration']['participants_data']
            A_durations = [p['A_duration'] for p in participants]
            B_durations = [p['B_duration'] for p in participants]
            participant_ids = [p['id'] for p in participants]

            x = np.arange(len(participant_ids))
            width = 0.35

            ax1.bar(x - width/2, A_durations, width, label='Control (A)', alpha=0.7, color='lightcoral')
            ax1.bar(x + width/2, B_durations, width, label='Intervention (B)', alpha=0.7, color='lightblue')

            # 添加总体均值线
            ax1.axhline(y=results['focus_duration']['A_mean'], color='red', linestyle='--', alpha=0.5)
            ax1.axhline(y=results['focus_duration']['B_mean'], color='blue', linestyle='--', alpha=0.5)

            ax1.set_xlabel('Participants')
            ax1.set_ylabel('Focus Duration (seconds)')
            ax1.set_title('Individual Focus Duration: Control vs Intervention')
            ax1.set_xticks(x)
            ax1.set_xticklabels(participant_ids)
            ax1.legend()
            ax1.grid(True, alpha=0.3)

            # 右侧：汇总柱状图
            means = [results['focus_duration']['A_mean'], results['focus_duration']['B_mean']]
            labels = ['Control (A)', 'Intervention (B)']
            colors = ['lightcoral', 'lightblue']

            bars = ax2.bar(labels, means, color=colors, alpha=0.7)
            ax2.set_ylabel('Mean Focus Duration (seconds)')
            ax2.set_title(f'Focus Duration Improvement: +{results["focus_duration"]["improvement_percent"]:.1f}%')

            # 添加数值标签
            for bar, mean in zip(bars, means):
                height = bar.get_height()
                ax2.text(bar.get_x() + bar.get_width()/2., height,
                        f'{int(mean)}s', ha='center', va='bottom')

            # 添加显著性标记
            if results['focus_duration']['significant']:
                ax2.text(0.5, max(means)*1.05, f'p = {results["focus_duration"]["p_value"]:.3f}*',
                        ha='center', transform=ax2.transAxes)

            ax2.grid(True, alpha=0.3)

            plt.tight_layout()
            plt.savefig(output_path / 'figure_2_focus_duration.png', dpi=300, bbox_inches='tight')
            plt.close()

        # 图2: CEI时间序列变化
        if 'cei_time_series' in results:
            fig, ax = plt.subplots(figsize=(10, 6))

            time_series = results['cei_time_series']
            intervention_time = results['intervention_timestamp']

            ax.plot(time_series['time'], time_series['cei'], 'b-', linewidth=2, alpha=0.7, label='CEI')
            ax.axvline(x=intervention_time, color='red', linestyle='--', alpha=0.7, label='Intervention')

            # 添加5分钟窗口高亮
            intervention_end = intervention_time + 300  # 5分钟后
            ax.axvspan(intervention_time, intervention_end, alpha=0.2, color='green', label='5-min window')

            ax.set_xlabel('Time (seconds)')
            ax.set_ylabel('CEI (Combination Embodied Index)')
            ax.set_title('CEI Response to Intervention: 5-min Window Analysis')
            ax.legend()
            ax.grid(True, alpha=0.3)

            plt.tight_layout()
            plt.savefig(output_path / 'figure_3_cei_time_series.png', dpi=300, bbox_inches='tight')
            plt.close()

        print(f"可视化图表已保存到: {output_path}")

    def export_results_table(self, results, output_path='./results_table.csv'):
        """
        导出结果表格
        Args:
            results: 分析结果
            output_path: 输出文件路径
        """
        table_data = []

        # 添加基本信息
        table_data.append(['Metric', 'Control (A)', 'Intervention (B)', 'Improvement', 'p-value', 'Significant'])

        # 添加专注时长结果
        if 'focus_duration' in results:
            fd = results['focus_duration']
            table_data.append([
                'Focus Duration (s)',
                f"{fd['A_mean']:.1f}",
                f"{fd['B_mean']:.1f}",
                f"+{fd['improvement_percent']:.1f}%",
                f"{fd['p_value']:.3f}",
                "Yes" if fd['significant'] else "No"
            ])

        # 添加CEI结果
        if 'cei_change' in results:
            ce = results['cei_change']
            table_data.append([
                'CEI Change',
                f"{ce['pre_mean']:.3f}",
                f"{ce['post_mean']:.3f}",
                f"-{ce['reduction_percent']:.1f}%",
                f"{ce['p_value']:.3f}",
                "Yes" if ce['significant'] else "No"
            ])

        # 添加主观量表结果
        if 'subjective_scales' in results:
            for scale, data in results['subjective_scales'].items():
                table_data.append([
                    scale,
                    f"{data['A_mean']:.2f}±{data['A_std']:.2f}",
                    f"{data['B_mean']:.2f}±{data['B_std']:.2f}",
                    f"{data['improvement']:.2f}",
                    f"{data['p_value']:.3f}",
                    "Yes" if data['significant'] else "No"
                ])

        df = pd.DataFrame(table_data[1:], columns=table_data[0])
        df.to_csv(output_path, index=False)
        print(f"结果表格已保存到: {output_path}")


def main():
    """主函数示例用法"""
    print("🧠 GestureFlow CEI计算和统计分析脚本")
    print("📋 严格限制: 仅使用1路sEMG (200Hz) + 1路GSR (4-10Hz)")
    print("🎯 专注于CHI Poster论文所需的关键分析")

    # 创建分析器实例
    analyzer = GestureFlowAnalyzer()

    # 示例数据路径 (实际使用时替换为真实数据)
    emg_data_file = "data/emg_session.npy"
    gsr_data_file = "data/gsr_session.npy"

    if Path(emg_data_file).exists() and Path(gsr_data_file).exists():
        print(f"✅ 找到数据文件，开始分析...")

        # 加载数据
        emg_data = np.load(emg_data_file)
        gsr_data = np.load(gsr_data_file)

        # 加载校准数据
        # (实际使用时需要从校准文件加载)
        # analyzer.load_calibration_data(emg_rest, emg_grip, gsr_rest, gsr_grip)

        # 计算CEI
        print("📊 计算CEI指标...")
        cei = analyzer.compute_cei(emg_data, gsr_data)

        # 生成可视化
        print("📈 生成可视化图表...")
        results = {'cei_time_series': {'time': np.arange(len(cei))/200, 'cei': cei}}
        analyzer.generate_visualizations(results)

        print("✅ 分析完成！")
        print("📁 输出文件:")
        print("   - ./figures/figure_2_focus_duration.png")
        print("   - ./figures/figure_3_cei_time_series.png")
        print("   - ./results_table.csv")

    else:
        print("📁 数据文件不存在，请先运行实验采集数据")
        print("📂 预期数据文件:")
        print("   - data/emg_session.npy")
        print("   - data/gsr_session.npy")
        print("   - data/calibration_*.npy")


if __name__ == "__main__":
    main()