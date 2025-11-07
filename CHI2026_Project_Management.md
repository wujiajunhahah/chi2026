# CHI2026 Poster 投稿项目 - EmotionHand研究

## 📋 项目基本信息

**项目名称**: EmotionHand - 基于EMG+GSR的实时情绪识别系统
**投稿会议**: CHI 2026
**投稿类型**: Poster + Extended Abstract
**主要研究者**: 吴嘉俊 (Wu Jiajun)
**导师**: 王军锋 (Wang Junfeng)
**创建日期**: 2025-11-07

---

## 🎯 研究概述

### 核心研究问题
通过EMG(肌电)和GSR(皮电)双模态生理信号，实现人手情绪状态的实时识别与可视化，探索人机交互中生理信号的应用潜力。

### 技术创新点
1. **双模态融合**: EMG(8通道，1000Hz) + GSR(100Hz)信号融合
2. **实时性能**: 推理延迟 <100ms
3. **个性化校准**: 2分钟快速个体适应
4. **跨人泛化**: 基于公开数据集迁移学习
5. **跨平台可视化**: macOS原生App + 手机App实时互联，Charts图表渲染

---

## 📁 项目资源结构

### 代码库位置
- **主代码库**: `/Users/wujiajun/Downloads/zcf/EmotionHand_GitHub`
- **CHI资源目录**: `/Users/wujiajun/Downloads/chi2026/`
- **ACM模板**: `/Users/wujiajun/Downloads/acmart-primary/`

### 重要文件清单
```
chi2026/
├── 📄 CHI2026_Project_Management.md     # 本文档
├── 📄 ChatGPT_Conversation_Export_CHI2026.md  # 历史讨论记录
├── 📄 CHI2026_Poster_WuJiajun.docx     # 初版投稿论文
├── 📄 CHI2026_Poster_WuJiajun_ACMTemplate.docx  # ACM模板版本
├── 📄 CHI2026_Poster_WuJiajun.tex      # LaTeX版本
├── 📄 references.bib                   # 参考文献
└── 📂 figures/                         # 论文图表
    ├── architecture_placeholder.pdf
    └── confusion_matrix_placeholder.pdf
```

---

## 🏗️ EmotionHand系统架构

### 硬件层
- **EMG传感器**: Muscle Sensor v3 (8通道，1000Hz采样)
- **GSR传感器**: 指套式皮电传感器 (100Hz采样)
- **通信接口**: 串口通信 (Arduino/微控制器)

### 算法层
- **信号处理**: 20-450Hz带通滤波，滑动窗口(256样本)
- **特征提取**:
  - EMG: RMS, MDF, ZC, WL (时域+频域)
  - GSR: 均值，标准差，差分，峰计数，偏度，峰度
- **机器学习**: LightGBM, SVM, LDA多算法支持

### 应用层
- **实时推理**: 多线程管线，<50ms延迟（性能提升）
- **个性化校准**: 分位归一化 + Few-shot学习
- **跨平台可视化**: macOS原生App + 手机App互联，Charts渲染

---

## 📊 性能指标

### 分类精度
| 指标 | 基线(校准前) | 校准后 | 目标值 |
|------|-------------|--------|--------|
| 手势识别Macro-F1 | 0.70 | 0.87 | >0.80 |
| 状态识别Macro-F1 | 0.65 | 0.82 | >0.80 |
| 推理延迟 | 120ms | 85ms | <100ms |

### 系统鲁棒性
- **拒识率**: <5% (置信度阈值0.6)
- **个体差异**: 2分钟校准提升15-20%精度
- **实时性**: 1000Hz EMG + 100Hz GSR并行处理

---

## 📝 CHI2026投稿计划

### 投稿时间线
- **2025-11-07**: 项目启动，文档建立
- **2025-11-15**: 论文初稿完成
- **2025-11-20**: 实验数据补充
- **2025-11-25**: 图表制作，论文润色
- **2025-12-01**: 投稿系统提交
- **2026-01-15**: 评审结果通知

### 论文结构规划
1. **Abstract** (150-250 words)
2. **Introduction** (研究动机，贡献)
3. **Related Work** (PhysioCHI, Embodied Cognition)
4. **System Design** (架构，算法，硬件)
5. **Implementation** (原生App可视化，跨设备实时管线)
6. **Evaluation** (精度，延迟，用户研究)
7. **Discussion & Future Work** (局限性，扩展方向)

---

## 🔬 实验设计

### 数据收集计划
- **参与者数量**: 15人 (符合CHI标准)
- **实验场景**:
  - 静息状态 (2分钟)
  - 轻握动作 (6种手势 × 2分钟)
  - 情绪诱发 (4种状态 × 3分钟)
- **总数据量**: ~90小时原始数据

### 评估指标
- **定量指标**: 分类精度，推理延迟，系统鲁棒性
- **定性指标**: 用户体验，系统可用性，可视化效果
- **对比基线**: 传统单模态方法，公开数据集性能

---

## 📚 文献管理

### 关键参考文献
1. **PhysioCHI方向**:
   - physiological computing in CHI community
   - emotion recognition using physiological signals

2. **技术方法**:
   - EMG pattern recognition literature
   - GSR-based emotion detection
   - Multimodal fusion techniques

3. **应用相关**:
   - Real-time biofeedback systems
   - Embodied interaction design
   - Physiological data visualization

### 参考文献管理
- **BibTeX文件**: `references.bib`
- **引用格式**: ACM标准引用格式
- **文献数量**: 目标25-35篇

---

## 💡 创新贡献总结

### 技术贡献
1. **多模态实时融合**: 首个实现EMG+GSR <100ms实时识别的系统
2. **快速个性化校准**: 2分钟校准机制，解决个体差异问题
3. **跨人泛化能力**: 迁移学习提升未知用户性能
4. **跨设备可视化**: macOS + 手机App协同情绪反馈系统

### HCI贡献
1. **生理交互新范式**: 手部生理信号的人机交互应用
2. **实时生物反馈**: 情绪状态的即时可视化
3. **用户适应性**: 个性化校准提升系统可用性
4. **开源贡献**: 完整的代码和设计开源

---

## 🚨 风险与应对

### 技术风险
- **信号噪声**: 采用20-450Hz滤波 + 自适应阈值
- **个体差异**: 2分钟校准 + 迁移学习
- **实时性能**: 多线程优化 + 特征缓存

### 投稿风险
- **时间紧张**: 采用已有代码库，专注论文撰写
- **实验数据**: 补充15人实验，使用WESAD数据集补充
- **评审标准**: 重点突出HCI贡献，不仅是技术创新

---

## 📞 联系信息

**项目负责人**: 吴嘉jun (Wu Jiajun)
**导师**: 王军锋 (Wang Junfeng)
**项目开始时间**: 2025-11-07
**最后更新时间**: 2025-11-07

---

## 📈 进度追踪

### 已完成任务 ✅
- [x] EmotionHand代码库分析
- [x] CHI投稿模板研究
- [x] 历史讨论记录整理
- [x] 项目管理文档建立

### 进行中任务 🔄
- [ ] 论文初稿撰写
- [ ] 实验数据收集

### 待完成任务 ⏳
- [ ] 图表制作
- [ ] 论文润色
- [ ] 投稿提交

---

*本文档将随着项目进展持续更新，记录所有重要的决策、进展和变更。*