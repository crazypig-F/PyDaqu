import pandas as pd

from analyze.utils.significance import Significance
from scipy.stats import normaltest


def significance_test(raw1, raw2):
    # _, p = Significance.t_test(raw1, raw2)
    _, p = Significance.wilcoxon_test(raw1, raw2)
    if 0.01 <= p < 0.05: print("*")
    if 0.001 <= p < 0.01: print("**")
    if p < 0.001: print("***")
    if p >= 0.05: print("NS")


def main():
    df = pd.read_csv("./data/temp/phy/parallel/complete.csv", index_col=0)
    for col in df.columns:
        for i in ["A", "B", "C", "D"]:
            print(col, i, end=" ")
            raw1 = df.loc[df.index.str.startswith(f"{i}Y"), col]
            raw2 = df.loc[df.index.str.startswith(f"{i}Z"), col]
            significance_test(raw1, raw2)
            print(raw1.mean(), raw2.mean())

            if i == "B":
                print("BY_AY", end=" ")
                raw1 = df.loc[df.index.str.startswith(f"BY"), col]
                raw2 = df.loc[df.index.str.startswith(f"AY"), col]
                significance_test(raw1, raw2)
                print("BZ_AZ", end=" ")
                raw1 = df.loc[df.index.str.startswith(f"BZ"), col]
                raw2 = df.loc[df.index.str.startswith(f"AZ"), col]
                significance_test(raw1, raw2)

            if i == "C":
                print("CY_BY", end=" ")
                raw1 = df.loc[df.index.str.startswith(f"CY"), col]
                raw2 = df.loc[df.index.str.startswith(f"BY"), col]
                significance_test(raw1, raw2)
                print("CZ_BZ", end=" ")
                raw1 = df.loc[df.index.str.startswith(f"CZ"), col]
                raw2 = df.loc[df.index.str.startswith(f"BZ"), col]
                significance_test(raw1, raw2)

            if i == "D":
                print("DY_CY", end=" ")
                raw1 = df.loc[df.index.str.startswith(f"DY"), col]
                raw2 = df.loc[df.index.str.startswith(f"CY"), col]
                significance_test(raw1, raw2)
                print("DZ_CZ", end=" ")
                raw1 = df.loc[df.index.str.startswith(f"DZ"), col]
                raw2 = df.loc[df.index.str.startswith(f"CZ"), col]
                significance_test(raw1, raw2)


if __name__ == '__main__':
    main()
