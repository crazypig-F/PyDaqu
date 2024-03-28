import pandas as pd
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


def dominant_microbe(group, top):
    bac = pd.read_csv(f"./data/temp/microbe/stage/bacteria/top/{group}.csv", index_col=0).iloc[:, :-1]
    fun = pd.read_csv(f"./data/temp/microbe/stage/fungi/top/{group}.csv", index_col=0).iloc[:, :-1]
    dominant = []
    if group == "traditional":
        for i in ["AY", "BY", "CY", "DY"]:
            dominant += bac.loc[i, :].sort_values(ascending=False)[:top].index.to_list()
        for i in ["AY", "BY", "CY", "DY"]:
            dominant += fun.loc[i, :].sort_values(ascending=False)[:top].index.to_list()
    else:
        for i in ["AZ", "BZ", "CZ", "DZ"]:
            dominant += bac.loc[i, :].sort_values(ascending=False)[:top].index.to_list()
        for i in ["AZ", "BZ", "CZ", "DZ"]:
            dominant += fun.loc[i, :].sort_values(ascending=False)[:top].index.to_list()
    return dominant


def amino_core(group):
    df = pd.read_csv(f"./data/temp/corr/micro_amino/{group}_edge.csv", index_col=0)
    target = df['Target']
    data = pd.DataFrame(target.value_counts())
    data.columns = ["degree"]
    save_csv(data, f"./data/temp/core/micro_amino/amino_micro_{group}.csv")

    source = df['Source']
    data = pd.DataFrame(source.value_counts())
    data.columns = ["degree"]
    save_csv(data, f"./data/temp/core/micro_amino/amino_{group}.csv")


def main():
    # microbe_degree()
    amino_core("traditional")
    amino_core("mechanical")


if __name__ == '__main__':
    main()
