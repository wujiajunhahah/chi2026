# -*- coding: utf-8 -*-
import os, glob, math, json
import numpy as np
import pandas as pd
from pathlib import Path
from scipy import stats
import matplotlib.pyplot as plt

plt.rcParams['font.size'] = 10

def windowed(arr, w, step):
    for i in range(0, max(0, len(arr)-w+1), step):
        yield i, arr[i:i+w]

def features(df, fs_emg=200, fs_gsr=10, win_s=2.0, step_s=0.5):
    import numpy as np, math, pandas as pd
    w_emg, s_emg = int(win_s*fs_emg), int(step_s*fs_emg)
    w_gsr, s_gsr = int(win_s*fs_gsr), int(step_s*fs_gsr)
    emg = df['emg'].to_numpy(dtype=float)
    gsr = df['gsr'].to_numpy(dtype=float)
    idx_list, rms_list, slope_list = [], [], []
    for i, seg in windowed(emg, w_emg, s_emg):
        rms = math.sqrt(np.mean(seg**2)) if len(seg)>0 else np.nan
        rms_list.append(rms); idx_list.append(i)
    for i, seg in windowed(gsr, w_gsr, s_gsr):
        if len(seg)>1:
            x = np.arange(len(seg)); k, _ = np.polyfit(x, seg, 1)
            slope_list.append(k)
        else:
            slope_list.append(np.nan)
    n = min(len(idx_list), len(slope_list))
    out = pd.DataFrame({'idx':idx_list[:n],'emg_rms':rms_list[:n],'gsr_slope':slope_list[:n]})
    out['emg_rms_z'] = (out['emg_rms']-np.nanmean(out['emg_rms']))/(np.nanstd(out['emg_rms'])+1e-8)
    out['gsr_slope_z'] = (out['gsr_slope']-np.nanmean(out['gsr_slope']))/(np.nanstd(out['gsr_slope'])+1e-8)
    out['CEI'] = 0.6*out['emg_rms_z'] + 0.4*out['gsr_slope_z']
    return out

def paired_test(a, b):
    import numpy as np, math
    from scipy import stats
    a, b = np.asarray(a), np.asarray(b)
    n = min(len(a), len(b))
    a, b = a[:n], b[:n]
    if n < 5: return {'test':'NA','p':None,'effect':'NA','effect_value':None}
    try:
        _, p_a = stats.shapiro(a); _, p_b = stats.shapiro(b)
    except Exception:
        p_a = p_b = 0.2
    if (p_a>0.1) and (p_b>0.1):
        t, p = stats.ttest_rel(a, b)
        d = (np.mean(a)-np.mean(b))/ (np.std(a, ddof=1)+1e-8)
        return {'test':'paired t','p':float(p),'effect':'Cohen d','effect_value':float(d)}
    else:
        w, p = stats.wilcoxon(a, b)
        z = stats.norm.ppf(min(p,1-p)) * (-1)
        r = z / math.sqrt(n)
        return {'test':'wilcoxon','p':float(p),'effect':'r','effect_value':float(r)}

def demo_pipeline(data_dir="data_demo", out_dir="analysis_out"):
    Path(out_dir).mkdir(parents=True, exist_ok=True)
    if not os.path.exists(data_dir) or len(glob.glob(f"{data_dir}/*.csv"))==0:
        import numpy as np, pandas as pd
        rng = np.random.default_rng(42)
        Path(data_dir).mkdir(parents=True, exist_ok=True)
        for sid in range(1,5):
            for cond in ['A','B']:
                n = 2000
                emg = rng.normal(0.2 if cond=='A' else 0.15, 0.05, size=n)
                gsr = rng.normal(0.1 if cond=='A' else 0.08, 0.02, size=n)
                ts = np.arange(n)
                df = pd.DataFrame({'timestamp':ts,'emg':emg,'gsr':gsr,'subject_id':f"S{sid:02d}",'condition':cond})
                df.to_csv(f"{data_dir}/S{sid:02d}_{cond}.csv", index=False)
        pd.DataFrame({
            'subject_id':[f"S{sid:02d}" for sid in range(1,5)],
            'focus_min_A':[46,41,44,40],
            'focus_min_B':[57,53,50,49]
        }).to_csv(f"{data_dir}/focus_minutes.csv", index=False)

    import pandas as pd, numpy as np, matplotlib.pyplot as plt, json
    fdf = pd.read_csv(f"{data_dir}/focus_minutes.csv")
    a, b = fdf['focus_min_A'].values, fdf['focus_min_B'].values
    test = paired_test(b, a)
    plt.figure()
    for ai,bi in zip(a,b):
        plt.plot([0,1],[ai,bi], marker='o')
    plt.xticks([0,1], ['A (no nudge)','B (gentle nudge)'])
    plt.ylabel('Focus minutes (block 1)')
    plt.title('Per-participant focus minutes')
    plt.tight_layout()
    plt.savefig(f"{out_dir}/focus_minutes_ab.pdf"); plt.close()
    with open(f"{out_dir}/focus_minutes_stats.json","w") as f:
        json.dump(test, f, indent=2)

    # CEI 前后
    import glob
    rows = []
    for pathA in glob.glob(f"{data_dir}/*_A*.csv"):
        sid = Path(pathA).stem.split('_')[0]
        a_df = pd.read_csv(pathA)
        b_df = pd.read_csv(pathA.replace('_A','_B'))
        feat_b = features(b_df)
        n5 = min(300, len(feat_b)//4)  # 简化：取固定窗口
        pre, post = feat_b['CEI'][:n5], feat_b['CEI'][-n5:]
        rows.append({'subject_id':sid,'B_pre':np.nanmean(pre),'B_post':np.nanmean(post)})
    ddf = pd.DataFrame(rows)
    test2 = paired_test(ddf['B_post'], ddf['B_pre'])
    plt.figure()
    for pre,post in zip(ddf['B_pre'], ddf['B_post']):
        plt.plot([0,1],[pre,post], marker='o')
    plt.xticks([0,1], ['Before (B)','After (B)'])
    plt.ylabel('Composite Embodied Index (CEI)')
    plt.title('CEI change within B (nudge) sessions')
    plt.tight_layout()
    plt.savefig(f"{out_dir}/cei_change_within_B.pdf"); plt.close()
    with open(f"{out_dir}/cei_change_within_B_stats.json","w") as f:
        json.dump(test2, f, indent=2)

if __name__ == "__main__":
    demo_pipeline()
