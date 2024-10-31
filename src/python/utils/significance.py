import pandas as pd
from scipy.stats import stats, wilcoxon
from scipy.stats import normaltest

import config


class Significance:
    def __init__(self):
        pass

    @classmethod
    def normal_test(cls, data):
        """
        数据正态性检验
        """
        res = stats.normaltest(data)
        print(res)

    @classmethod
    def t_test(cls, data1, data2):
        """
        成对样本t检验
        """
        t, p = stats.ttest_rel(data1, data2)
        return t, p

    @classmethod
    def wilcoxon_test(cls, data1, data2):
        """
        非参数检验
        """
        res = wilcoxon(data1, data2)
        return res.statistic, res.pvalue


def significance_test(raw1, raw2):
    _, p = Significance.wilcoxon_test(raw1, raw2)
    if 0.01 <= p < 0.05: print("*")
    if 0.001 <= p < 0.01: print("**")
    if p < 0.001: print("***")
    if p >= 0.05: print("NS")


def test(df):
    for col in df.columns:
        print(col, "RC_YF")
        raw1 = df.loc[df.index.str.startswith(f"RC"), col]
        raw2 = df.loc[df.index.str.startswith(f"YF"), col]
        print(raw1.mean(), raw2.mean())
        significance_test(raw1, raw2)

        print(col, "YF_EF")
        raw1 = df.loc[df.index.str.startswith(f"YF"), col]
        raw2 = df.loc[df.index.str.startswith(f"EF"), col]
        print(raw1.mean(), raw2.mean())
        significance_test(raw1, raw2)

        print(col, "EF_CC")
        raw1 = df.loc[df.index.str.startswith(f"EF"), col]
        raw2 = df.loc[df.index.str.startswith(f"CC"), col]
        print(raw1.mean(), raw2.mean())
        significance_test(raw1, raw2)


def main():
    # phy = pd.read_csv(config.basedir + "/data/result/fermentation parameters/fermentation parameters mean.csv",
    #                   index_col=0)
    alpha = pd.read_csv(config.basedir + "/data/result/diversity/alpha.csv", index_col=0)
    # test(phy)
    test(alpha)


if __name__ == '__main__':
    main()
