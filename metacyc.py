import numpy as np
import pandas as pd
import statsmodels.stats.multitest as smt

from analyze.utils.significance import Significance

df = pd.read_csv("./data/raw/path_fungi.csv", index_col=0)
description = df["description"]
df = df.drop(columns='description')
AY = df.loc[:, df.columns.str.startswith("AY")]
AZ = df.loc[:, df.columns.str.startswith("AZ")]
BY = df.loc[:, df.columns.str.startswith("BY")]
BZ = df.loc[:, df.columns.str.startswith("BZ")]
CY = df.loc[:, df.columns.str.startswith("CY")]
CZ = df.loc[:, df.columns.str.startswith("CZ")]
DY = df.loc[:, df.columns.str.startswith("DY")]
DZ = df.loc[:, df.columns.str.startswith("DZ")]
p_values = []
log_fcs = []
for idx in df.index:
    row1 = AY.loc[idx, :]
    row2 = AZ.loc[idx, :]
    t, p = Significance.t_test(row1, row2)
    if row1.mean() == 0 and row2.mean() == 0:
        p_values.append(1)
        log_fcs.append(0)
        continue
    elif row1.mean() == 0:
        row1 += row2.mean() / 10
    elif row2.mean() == 0:
        row2 += row1.mean() / 10
    p_values.append(p)
    log_fc = np.log2(row2.mean() / row1.mean())
    log_fcs.append(log_fc)
# 设置阈值为0.05
threshold = 0.05
# 进行FDR控制
rejected, p_values_corrected, _, _ = smt.multipletests(p_values, method="fdr_bh")
pd.DataFrame({"log2FC": log_fcs, "FDR": p_values_corrected, "label": description}).to_csv(
    "./data/temp/pathway/MetaCyc_fungi_RC.csv")
