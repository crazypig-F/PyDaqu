import math

import numpy as np
import pandas as pd
import scipy
from scipy.stats import linregress
from sklearn.metrics import r2_score

from analyze.ml.classify import ProcessClassifyModel, PhaseClassifyModel
from analyze.ml.regression import RegressionModel
from core import dominant_microbe


def process_predict():
    process_map = {"Y": 0, "Z": 1}
    microbe = pd.read_csv("./data/temp/microbe/parallel/merge/top/complete.csv", index_col=0)
    data = microbe.loc[microbe.index.str.startswith("D"), :]
    y = np.array([process_map[i[1]] for i in data.index])
    clf = ProcessClassifyModel(data, y, seed=42)
    s = clf.train()
    print(f"交叉验证平均结果", s)


def phase_predict(group):
    if group == "traditional":
        phase_map = {"AY": 0, "BY": 1, "CY": 2, "DY": 3}
    else:
        phase_map = {"AZ": 0, "BZ": 1, "CZ": 2, "DZ": 3}
    microbe = pd.read_csv(f"./data/temp/microbe/chamber/merge/top/{group}.csv", index_col=0)
    # core = pd.read_csv(f"./data/temp/core/{group}.csv", index_col=0)
    # dominant = dominant_microbe(group, top)
    # print(set(dominant))
    # core = core.loc[core['degree'] >= degree, :].index.to_list()
    # print(set(core))
    # key = sorted(list(set(dominant) & set(core)))
    # print(key)
    top = ["Pantoea", "Bacillus", "Virgibacillus", "Weissella", "Saccharopolyspora", "Enterobacter", "Thermomyces",
           "Thermoascus", "Pichia"]
    microbe = microbe.loc[:, top]
    physic = pd.read_csv(f"./data/temp/phy/chamber/mean/{group}.csv", index_col=0)
    physic.columns = ["starch", "moisture", "SP", "RS", "TA", "TE"]
    physic = physic.loc[:, ["moisture"]]
    data = pd.concat([microbe, physic], axis=1)
    y = pd.Series(np.array([phase_map[i[:2]] for i in data.index]), index=data.index)
    accuracy, precision, recall, f1 = 0, 0, 0, 0
    exp_num = 50
    print(data.columns)
    for i in range(exp_num):
        clf = PhaseClassifyModel(data, y, test_size=0.3, seed=i)
        res = clf.train()
        accuracy += res[0]
        precision += res[1]
        recall += res[2]
        f1 += res[3]
    print(accuracy / exp_num, precision / exp_num, recall / exp_num, f1 / exp_num)


def microbe_amino(group, degree_micro, degree_amino):
    microbe = pd.read_csv(f"./data/temp/microbe/chamber/merge/top/{group}.csv", index_col=0)
    # core_microbe = pd.read_csv(f"./data/temp/core/micro_amino/amino_micro_{group}.csv", index_col=0)
    # microbe = microbe.loc[:, core_microbe.loc[core_microbe['degree'] >= degree_micro, :].index]
    # print(core_microbe.loc[core_microbe['degree'] >= degree_micro, :].index)

    amino = pd.read_csv(f"./data/temp/amino/chamber/mean/{group}.csv", index_col=0)
    # core_amino = pd.read_csv(f"./data/temp/core/micro_amino/amino_{group}.csv", index_col=0)
    # amino = amino.loc[:, core_amino.loc[core_amino['degree'] > degree_amino, :].index]
    # print(core_amino.loc[core_amino['degree'] >= degree_amino, :].index)
    # corr_microbe = pd.read_csv(f"./data/temp/corr/micro_amino/{group}_edge.csv", index_col=0)

    physic = pd.read_csv(f"./data/temp/phy/chamber/mean/{group}.csv", index_col=0)
    physic.columns = ["starch", "moisture", "SP", "RS", "TA", "TE"]

    # [["Bacillus"], ["Halomonas"], ["Lactobacillus"], ["Pantoea"], ["Pseudonocardiaceae"],
    #  ["Saccharopolyspora"], ["Virgibacillus"], ["Weissella"], ["Bacillus", "Halomonas"],
    #  ["Bacillus", "Lactobacillus"], ["Bacillus", "Pantoea"], ["Bacillus", "Pseudonocardiaceae"],
    #  ["Bacillus", "Saccharopolyspora"], ["Bacillus", "Virgibacillus"], ["Bacillus", "Weissella"]]        real = {}

    microbe_select = microbe.loc[:, ["Bacillus"]]
    physic_select = physic.loc[:, ["moisture"]]
    data = pd.concat([microbe_select, physic_select], axis=1)
    amino_select = amino.loc[:,
                   ["Gln", "Lys", "His", "Pro", "Phe", "Val", "Glu", "Gly", "Ile", "Leu", "Thr", "Ser", "Tyr", "Ala"]
                   ]

    real = {}
    predict = {}
    score = []
    for col in amino_select.columns:
        print(col, data.columns.to_list())
        exp_num = 50
        r2 = 0
        for i in range(exp_num):
            reg = RegressionModel(data, amino_select[col], test_size=0.3, seed=i)
            res = reg.train()
            r2 += res[2]
            r = scipy.stats.pearsonr(res[0].to_list(), res[1])[0]
            p = scipy.stats.pearsonr(res[0].to_list(), res[1])[1]
            print(r, p)
        mean_score = r2 / exp_num
        print(mean_score)
        score.append(mean_score)
        min_sub_score = 10000
        for i in range(exp_num):
            reg = RegressionModel(data, amino_select[col], test_size=0.3, seed=i)
            res = reg.train()
            if abs(res[2] - mean_score) < min_sub_score:
                real[col] = res[0].to_list()
                predict[col] = res[1]
                min_sub_score = abs(res[2] - mean_score)
    pd.DataFrame(real).to_csv(f"./data/temp/ml/real_amino_{group}.csv")
    pd.DataFrame(predict).to_csv(f"./data/temp/ml/predict_amino_{group}.csv")
    pd.DataFrame({"score": score}, index=amino_select.columns).to_csv(f"./data/temp/ml/predict_amino_score_{group}.csv")


# Bacillus_Virgibacillus
# 0.281332095
# 0.481495885
# 0.553991389

# Bacillus
# 0.394566925
# 0.627769925
# 0.70571265


# Bacillus_Saccharopolyspora
# 0.533103469
# 0.474726715
# 0.315911683
# 0.557064062
# 0.6350019
# 0.531931199

# Bacillus
# 0.601081629
# 0.68555016
# 0.650241265
# 0.745319985
# 0.829849802
# 0.758358006


def main():
    # process_predict()
    # print("traditional")
    # phase_predict("traditional")
    # print("mechanical")
    # phase_predict("mechanical")
    print("traditional")
    microbe_amino("traditional", 1, 1)
    print("mechanical")
    microbe_amino("mechanical", 5, 3)


if __name__ == '__main__':
    main()
