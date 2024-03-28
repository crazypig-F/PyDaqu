import pandas as pd

from analyze.amplicon import AmpliconStatistics
from analyze.characteristics import NumCharacteristics
from utils import save_csv


def split_qu_env():
    df1 = pd.read_csv("./data/raw/bacteria_filtered.csv", index_col=0)
    df2 = pd.read_csv("./data/raw/fungi_filtered.csv", index_col=0)

    Q1 = df1.loc[:, df1.columns.str.contains("AZ|BZ|CZ|DZ|AY|BY|CY|DY")].copy()
    Q2 = df2.loc[:, df2.columns.str.contains("AZ|BZ|CZ|DZ|AY|BY|CY|DY")].copy()
    Q1_ASV = Q1.apply(lambda x: x != 0).sum(axis=1).apply(lambda x: x > len(Q1.columns) // 12)
    Q2_ASV = Q2.apply(lambda x: x != 0).sum(axis=1).apply(lambda x: x > len(Q2.columns) // 12)
    Q1 = Q1.loc[Q1_ASV, :]
    Q2 = Q2.loc[Q2_ASV, :]
    E1 = df1.loc[:, df1.columns.str.contains("MZ|WZ|RZ|EZ|MY|WY|RY|EY")].copy()
    E2 = df2.loc[:, df2.columns.str.contains("MZ|WZ|RZ|EZ|MY|WY|RY|EY")].copy()
    E1_ASV = E1.apply(lambda x: x != 0).sum(axis=1).apply(lambda x: x > len(E1.columns) // 12)
    E2_ASV = E2.apply(lambda x: x != 0).sum(axis=1).apply(lambda x: x > len(E2.columns) // 12)
    E1 = E1.loc[E1_ASV, :]
    E2 = E2.loc[E2_ASV, :]

    Q1["taxonomy"] = df1["taxonomy"]
    Q2["taxonomy"] = df2["taxonomy"]
    E1["taxonomy"] = df1["taxonomy"]
    E2["taxonomy"] = df2["taxonomy"]
    save_csv(Q1, "./data/raw/qu_b.csv")
    save_csv(Q2, "./data/raw/qu_f.csv")
    save_csv(E1, "./data/raw/env_b.csv")
    save_csv(E2, "./data/raw/env_f.csv")


def amplicon_operate():
    bac = AmpliconStatistics("./data/raw/qu_b.csv", "taxonomy")
    bac_all = bac.get_top(top_k=-1)
    tm(bac_all, "parallel", "bacteria", "all")
    bac_top = bac.get_top(top_k=20)
    tm(bac_top, "parallel", "bacteria", "top")

    fun = AmpliconStatistics("./data/raw/qu_f.csv", "taxonomy")
    fun_all = fun.get_top(top_k=-1)
    tm(fun_all, "parallel", "fungi", "all")
    fun_top = fun.get_top(top_k=20)
    tm(fun_top, "parallel", "fungi", "top")

    merge_all = pd.concat([bac_all, fun_all], axis=1)
    tm(merge_all, "parallel", "merge", "all")
    merge_top = pd.concat([bac_top.iloc[:, :-1], fun_top.iloc[:, :-1]], axis=1)
    tm(merge_top, "parallel", "merge", "top")

    character(bac_all, "bacteria", "all")
    character(bac_top, "bacteria", "top")

    character(fun_all, "fungi", "all")
    character(fun_top, "fungi", "top")

    character(merge_all, "merge", "all")
    character(merge_top, "merge", "top")

    bac_env = AmpliconStatistics("./data/raw/env_b.csv", "taxonomy")
    bac_env_all = bac_env.get_top(top_k=-1)
    tm_env(bac_env_all, "parallel_env", "bacteria", "all")
    bac_env_top = bac_env.get_top(top_k=20)
    tm_env(bac_env_top, "parallel_env", "bacteria", "top")

    fun_env = AmpliconStatistics("./data/raw/env_f.csv", "taxonomy")
    fun_env_all = fun_env.get_top(top_k=-1)
    tm_env(fun_env_all, "parallel_env", "fungi", "all")
    fun_env_top = fun_env.get_top(top_k=20)
    tm_env(fun_env_top, "parallel_env", "fungi", "top")

    merge_env_all = pd.concat([bac_env_all, fun_env_all], axis=1)
    tm_env(merge_env_all, "parallel_env", "merge", "all")
    merge_env_top = pd.concat([bac_env_top.iloc[:, :-1], fun_env_top.iloc[:, :-1]], axis=1)
    tm_env(merge_env_top, "parallel_env", "merge", "top")

    character_env(bac_env_all, "bacteria", "all")
    character_env(bac_env_top, "bacteria", "top")

    character_env(fun_env_all, "fungi", "all")
    character_env(fun_env_top, "fungi", "top")

    character_env(merge_env_all, "merge", "all")
    character_env(merge_env_top, "merge", "top")


def character(df, n1, n2):
    nct_df = NumCharacteristics(df)
    df_chamber = nct_df.get_mean(prefix=-1, save_type="int")
    df_stage = nct_df.get_mean(prefix=2, save_type="int")
    tm(df_chamber, "chamber", n1, n2)
    tm(df_stage, "stage", n1, n2)


def character_env(df, n1, n2):
    nct_df = NumCharacteristics(df)
    df_chamber = nct_df.get_mean(prefix=-1, save_type="int")
    df_stage = nct_df.get_mean(prefix=2, save_type="int")
    tm_env(df_chamber, "chamber_env", n1, n2)
    tm_env(df_stage, "stage_env", n1, n2)


def tm(df, n1, n2, n3):
    df_t = df.loc[df.index.str.contains("AY|BY|CY|DY"), :]
    df_m = df.loc[df.index.str.contains("AZ|BZ|CZ|DZ"), :]
    save_csv(df, f"./data/temp/microbe/{n1}/{n2}/{n3}/complete.csv")
    save_csv(df_t, f"./data/temp/microbe/{n1}/{n2}/{n3}/traditional.csv")
    save_csv(df_m, f"./data/temp/microbe//{n1}/{n2}/{n3}/mechanical.csv")


def tm_env(df, n1, n2, n3):
    df_t = df.loc[df.index.str.contains("MY|WY|RY|EY"), :]
    df_m = df.loc[df.index.str.contains("MZ|WZ|RZ|EZ"), :]
    save_csv(df, f"./data/temp/microbe/{n1}/{n2}/{n3}/complete.csv")
    save_csv(df_t, f"./data/temp/microbe/{n1}/{n2}/{n3}/traditional.csv")
    save_csv(df_m, f"./data/temp/microbe//{n1}/{n2}/{n3}/mechanical.csv")


def main():
    split_qu_env()
    amplicon_operate()


if __name__ == '__main__':
    main()
