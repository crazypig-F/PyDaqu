import math
import os.path
import pandas as pd

from src.python.utils.EC import get_module_ec, get_amino_acid_ec_map


def get_function():
    asv = ['ASV_15625', 'ASV_95119', 'ASV_125122', 'ASV_131779', 'ASV_143173']
    base_path = r"D:\write\MbPL2021091547_V3V4\function"
    ec_list = []
    for idx, file in enumerate(os.listdir(base_path)):
        df = pd.read_table(os.path.join(base_path, file), sep="\t")
        ec = df["function"]
        sequence = df["sequence"]
        df = df.loc[:, df.columns.str.contains("AZ|BZ|CZ|DZ")]
        df["ec"] = ec
        df["sequence"] = sequence
        df = df.loc[df["sequence"].isin(asv), :]
        ec_list.append(df)
        print(idx, df)
    function_df = pd.concat(ec_list, axis=0, ignore_index=True)
    function_df.to_csv("./data/result/function/amino_function.csv")


def filter_function():
    df = pd.read_csv("./data/result/function/amino_function.csv", index_col=0)
    df_amino_function = df.loc[df["ec"].isin(get_module_ec()), :]
    df_left_AZ = df_amino_function.loc[:, df.columns.str.contains("AZ")].mean(axis=1)
    df_left_BZ = df_amino_function.loc[:, df.columns.str.contains("BZ")].mean(axis=1)
    df_left_CZ = df_amino_function.loc[:, df.columns.str.contains("CZ")].mean(axis=1)
    df_left_DZ = df_amino_function.loc[:, df.columns.str.contains("DZ")].mean(axis=1)
    df_right = df_amino_function.iloc[:, -2:]
    df_right["AZ"] = df_left_AZ
    df_right["BZ"] = df_left_BZ
    df_right["CZ"] = df_left_CZ
    df_right["DZ"] = df_left_DZ

    ec_list = []
    value_list = []
    map_list = []
    sequence_list = []
    map_ec_list = []
    for idx in df_right.index:
        ec = df_right["ec"][idx]
        for key in get_amino_acid_ec_map():
            if ec[3:] in get_amino_acid_ec_map()[key]:
                for phase in ["AZ", "BZ", "CZ", "DZ"]:
                    ec_list.append(ec)
                    value_list.append(df_right[phase][idx])
                    sequence_list.append(phase + df_right["sequence"][idx])
                    map_list.append(key)
                    map_ec_list.append(key + " " + ec)
    pd.DataFrame(
        {
            "ec": ec_list,
            "value": value_list,
            "sequence": sequence_list,
            "map_ko": map_list,
            "map_ec": map_ec_list,
        }
    ).sort_values(by="map_ko").to_csv("./data/result/function/amino_ec_value.csv", index=False)


if __name__ == '__main__':
    # get_function()
    filter_function()
