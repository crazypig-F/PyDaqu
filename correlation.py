import pandas as pd

from analyze.plot.corr import CorrNetworkGraph
from analyze.utils.sheet import SheetOperator
from utils import save_csv


def get_corr_network_graph(df1, df2):
    cng = CorrNetworkGraph(df1, df2, method="spearman")
    # cng = CorrNetworkGraph(df1, df2)
    return cng


def core_species(mat_r):
    core = (~mat_r.isna()).sum(axis=0).sort_values(ascending=False)
    print(core)
    return core


def bacteria_fungi():
    merge_t = pd.read_csv("./data/temp/microbe/chamber/merge/top/traditional.csv", index_col=0)
    merge_t = SheetOperator.clean_zero(merge_t)
    d1_t = pd.read_csv("./data/temp/microbe/chamber/bacteria/top/traditional.csv", index_col=0)
    d2_t = pd.read_csv("./data/temp/microbe/chamber/fungi/top/traditional.csv", index_col=0)
    save_bacteria_fungi(merge_t, d1_t, d2_t, "traditional")

    merge_m = pd.read_csv("./data/temp/microbe/chamber/merge/top/mechanical.csv", index_col=0)
    merge_m = SheetOperator.clean_zero(merge_m)
    d1_m = pd.read_csv("./data/temp/microbe/chamber/bacteria/top/mechanical.csv", index_col=0)
    d2_m = pd.read_csv("./data/temp/microbe/chamber/fungi/top/mechanical.csv", index_col=0)
    save_bacteria_fungi(merge_m, d1_m, d2_m, "mechanical")


def save_bacteria_fungi(df, d1, d2, n1):
    cng = get_corr_network_graph(df, df)
    save_csv(cng.r, f"./data/temp/corr/bac_fun/{n1}_r.csv")
    save_csv(cng.p, f"./data/temp/corr/bac_fun/{n1}_p.csv")
    core_species(cng.r)
    save_csv(cng.edge(), f"./data/temp/corr/bac_fun/{n1}_edge.csv", index=False)
    save_csv(cng.self_node(d1, d2), f"./data/temp/corr/bac_fun/{n1}_node.csv", index=False)


def main():
    bacteria_fungi()


if __name__ == '__main__':
    main()
