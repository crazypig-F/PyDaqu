import pandas as pd

from analyze.utils.significance import Significance


def significance_test(raw1, raw2):
    _, p = Significance.t_test(raw1, raw2)
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


if __name__ == '__main__':
    main()
