import pandas as pd

from src.python.corr.graph import CorrNetworkGraph
from src.python.utils.sheet import SheetOperator


# 4DBBD5 node1
# 3C5488 node2
# F4A8AC 红色边的颜色
# 00A087 蓝色边的颜色

def get_corr_network_graph(df1, df2):
    cng = CorrNetworkGraph(df1, df2, method="spearman")
    return cng


def microbe_amino():
    asv = pd.read_csv("./data/result/micro/mean/asv 30% mean.csv", index_col=0)
    AAs = pd.read_csv("./data/result/AAs/AAs mean.csv", index_col=0)

    asv = SheetOperator.clean_zero(asv)
    AAs = SheetOperator.clean_zero(AAs)
    cng = get_corr_network_graph(asv, AAs)
    cng.r.to_csv("./data/result/corr/micro_amino_r.csv")
    cng.p.to_csv("./data/result/corr/micro_amino_p.csv")
    cng.edge().to_csv("./data/result/corr/micro_amino_edge.csv", index=False)
    cng.node().to_csv("./data/result/corr/micro_amino_node.csv", index=False)


def asv_mapping():
    asv_b = pd.read_csv("./data/raw/Daqu bacteria asv.csv", index_col=0)
    asv_f = pd.read_csv("./data/raw/Daqu fungi asv.csv", index_col=0)
    tax_b = asv_b.loc[:, ['taxonomy']]
    tax_f = asv_f.loc[:, ['taxonomy']]
    tax_b['taxonomy'] = [i.split(";")[-2][4:] for i in tax_b['taxonomy']]
    tax_f['taxonomy'] = [i.split(";")[-2][4:] for i in tax_f['taxonomy']]
    tax = pd.concat([tax_b, tax_f], axis=0)

    edge = pd.read_csv("./data/result/corr/micro_amino_edge.csv", index_col=0)
    mapping_taxonomy = [tax.loc[i[2:], 'taxonomy'] for i in edge['Source']]
    edge['taxonomy'] = mapping_taxonomy
    mapping = edge.loc[:, ['Source', 'Target', 'Relevance', 'taxonomy']]
    mapping.to_csv("./data/result/corr/asv_mapping.csv", index=False)


def mapping_tax_count():
    mapping = pd.read_csv("./data/result/corr/asv_mapping.csv")
    tax_count = {}
    for idx in mapping.index:
        tax = mapping.loc[idx, 'taxonomy']
        relevance = mapping.loc[idx, 'Relevance']
        if tax not in tax_count.keys():
            tax_count[tax] = [0, 0]
        if relevance >= 0:
            tax_count[tax][0] += 1
        else:
            tax_count[tax][1] += 1
    p, n = [], []
    for key, value in tax_count.items():
        p.append(value[0])
        n.append(value[1])
    tax_count_df = pd.DataFrame({'taxonomy': tax_count.keys(), 'p': p, 'n': n})
    tax_count_df.to_csv("./data/result/corr/tax_count.csv")


def mapping_asv_select():
    mapping = pd.read_csv("./data/result/corr/asv_mapping.csv")
    target_genus = ['Bacillus', 'Saccharopolyspora', 'Virgibacillus', 'Lactobacillus']
    target_asv = mapping.loc[mapping['taxonomy'].isin(target_genus), 'Source']
    return list(set(target_asv))


def set_node_color():
    node = pd.read_csv("./data/result/corr/micro_amino_node.csv", index_col=0)
    mapping = pd.read_csv(f"./data/result/corr/asv_mapping.csv")
    taxonomy = mapping.loc[:, ['Source', 'taxonomy']].drop_duplicates()
    taxonomy.index = taxonomy['Source']
    taxonomy = taxonomy['taxonomy']
    print(taxonomy)

    def set_color(row):
        if row["Color"] == "node1":
            if row['Label'] in taxonomy.index.tolist():
                return taxonomy[row["Label"]]
            else:
                return "others"
        else:
            return "node2"

    node["taxonomy"] = node.apply(lambda row: set_color(row), axis=1)
    node["Label"] = node.apply(lambda x: x["Label"] if x["Color"] == "node2" else "", axis=1)
    node.to_csv("./data/result/corr/micro_amino_node.csv")


if __name__ == '__main__':
    microbe_amino()
    asv_mapping()
    mapping_tax_count()
    set_node_color()
