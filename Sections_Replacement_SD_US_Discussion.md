## System Design（最小生理输入 → 共调节）
…（此处粘贴到论文相应章节，保持单栏样式）…
GestureFlow 以最小生理输入为前提：单路 sEMG（≈200 Hz）与单路 GSR（4–10 Hz）。我们关注趋势级特征（EMG RMS、过零率；GSR 均值与斜率）来刻画紧张/放松的节律变化。在线管线含 1 分钟个体化自校准（30s 静息 + 30s 轻握，得 p10/p90），将特征映射到 [0,1]；复合指标 CEI=0.6·z(RMS_EMG)+0.4·z(slope_GSR)。当 CEI 持续高于个体阈值，系统通过 iOS 徽章 App 触发“风/光/水”微任务，形成 gentle nudge；信号弱时切换情境代理（久坐/噪声/亮度）维持闭环。

## User Study（情境化 ABAB + 微随机）
…（粘贴到 User Study）…
采用情境化 ABAB 设计并嵌入微随机试验（MRT）：A=仅记录；B=轻提示与共调节。N=12–15 远程工作者在两天内完成 ABAB；B 日以 p=0.5 概率推送提示。每日流程：佩戴→1min 自校准→40min 工作→10min 压力→（B）3–5min 恢复→20min 工作→简表+访谈。体验指标：专注时长、窗口切换、中断恢复时间、不打断感/恰当性；生理指标：CEI 在干预前后 5 分钟的变化。统计使用配对检验（正态→t；非正态→Wilcoxon）与效应量。

## Discussion / Design Implications（三条洞见）
(1) **Trust‑in‑Embodiment**：用户接受“被理解”的轻提示多于“被命令”的强干预。→ implication: 以同频共调为叙事。  
(2) **Embodied Awareness**：最小感知足以触发自我觉察的微时刻，关键在节律变化。→ implication: 用 CEI 等趋势指标驱动 1–3 分钟微任务。  
(3) **Co‑regulated Calmness**：当系统与用户形成“你进我退”的节律关系时，干预更易被认为恰当。→ implication: 设计“何时不提醒”的策略。
