import pandas as pd

import utils
from analyze.utils.significance import Significance


def pathway_total(stage, name):
    pathway = pd.read_csv("./data/raw/pathway.csv", index_col=0)
    classification = pd.read_csv("./data/raw/KEGG-pathway-classification.csv", index_col=0)
    idx_list = classification.loc[classification['Pathway Class 1'] == "Metabolism", "Pathway ID"]
    pathway = pathway.loc[pathway.index.isin(idx_list), pathway.columns.str.contains(stage)]
    m = dict(zip(classification['Pathway ID'], classification['Pathway Class2']))
    # m = dict(zip(classification['Pathway ID'], classification['Pathway ID']))
    pathway['class'] = [m[i] for i in pathway.index]
    pathway = pathway.groupby(by='class').sum()
    pathway = pathway.mean(axis=1)
    pathway = pd.DataFrame(pathway, columns=["value"])
    utils.save_csv(pathway, f"./data/temp/pathway/{name}.csv")


def pathway_amino_acid(g1, g2, stage):
    pathway = pd.read_csv("./data/raw/pathway.csv", index_col=0)
    classification = pd.read_csv("./data/raw/KEGG-pathway-classification.csv", index_col=0)
    idx_list = classification.loc[classification['Pathway Class2'] == "Amino acid metabolism", "Pathway ID"]
    pathway = pathway.loc[pathway.index.isin(idx_list), pathway.columns.str.contains(f"{g1}|{g2}")]
    m = dict(zip(classification['Pathway ID'], classification['Pathway ID']))
    pathway['class'] = [m[i] for i in pathway.index]
    pathway = pathway.groupby(by='class').sum()
    for idx in pathway.index:
        raw1 = pathway.loc[idx, pathway.columns.str.startswith(g1)]
        raw2 = pathway.loc[idx, pathway.columns.str.startswith(g2)]
        _, p = Significance.t_test(raw1, raw2)
        print(idx, end=" ")
        if 0.01 <= p < 0.05: print("*")
        if 0.001 <= p < 0.01: print("**")
        if p < 0.001: print("***")
        if p >= 0.05: print("NS")
    pathway1_m = pathway.loc[:, pathway.columns.str.startswith(g1)].mean(axis=1)
    pathway2_m = pathway.loc[:, pathway.columns.str.startswith(g2)].mean(axis=1)
    pathway1_s = pathway.loc[:, pathway.columns.str.startswith(g1)].std(axis=1)
    pathway2_s = pathway.loc[:, pathway.columns.str.startswith(g2)].std(axis=1)
    pd.DataFrame(
        {"mean": pathway1_m.to_list() + pathway2_m.to_list(), "std": pathway1_s.to_list() + pathway2_s.to_list(),
         "name": pathway.index.to_list() + pathway.index.to_list(),
         "group": ["Y"] * len(pathway.index) + ["Z"] * len(pathway.index)}).to_csv(
        f"./data/temp/pathway/pathway_amino_acid_{stage}.csv")


if __name__ == '__main__':
    # pathway_total("AY|BY|CY|DY", "traditional")
    # pathway_total("AZ|BZ|CZ|DZ", "mechanical")
    print("-"*20, "RC")
    pathway_amino_acid("AY", "AZ", "RC")
    print("-" * 20, "YF")
    pathway_amino_acid("BY", "BZ", "YF")
    print("-" * 20, "EF")
    pathway_amino_acid("CY", "CZ", "EF")
    print("-" * 20, "CC")
    pathway_amino_acid("DY", "DZ", "CC")
