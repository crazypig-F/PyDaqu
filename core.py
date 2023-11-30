import pandas as pd

import path
from utils import save_csv


def microbe_degree():
    df_t = pd.read_csv("./data/temp/corr/bac_fun/traditional_edge.csv", index_col=0)
    df_m = pd.read_csv("./data/temp/corr/bac_fun/mechanical_edge.csv", index_col=0)
    save_degree(df_t, "traditional")
    save_degree(df_m, "mechanical")


def save_degree(df, n1):
    source = df['Source']
    target = df['Target']
    data = pd.concat([source, target])
    data = pd.DataFrame(data.value_counts())
    data.columns = ["degree"]
    save_csv(data, f"./data/temp/core/{n1}.csv")


def dominant_microbe():
    bac = pd.read_csv("./data/temp/microbe/stage/bacteria/top/traditional.csv", index_col=0)
    fun = pd.read_csv("./data/temp/microbe/stage/fungi/top/traditional.csv", index_col=0)
    dominant = []
    for i in ["AY", "BY", "CY", "DY"]:
        dominant += bac.loc[i, :].sort_values(ascending=False)[:2].index.to_list()
    for i in ["AY", "BY", "CY", "DY"]:
        dominant += fun.loc[i, :].sort_values(ascending=False)[:2].index.to_list()
    return dominant


def main():
    microbe_degree()


if __name__ == '__main__':
    main()
