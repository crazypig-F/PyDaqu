import pandas as pd
from analyze.characteristics import NumCharacteristics
from utils import save_csv


def generate(df, n1):
    df_t = df.loc[df.index.str.contains("AY|BY|CY|DY"), :]
    df_m = df.loc[df.index.str.contains("AZ|BZ|CZ|DZ"), :]
    save_csv(df, f"./data/temp/{n1}/parallel/complete.csv")
    save_csv(df_t, f"./data/temp/{n1}/parallel/traditional.csv")
    save_csv(df_m, f"./data/temp/{n1}/parallel/mechanical.csv")
    character(df, n1)


def character(df, n1):
    nct_df = NumCharacteristics(df)
    df_chamber_mean = nct_df.get_mean(prefix=-1)
    df_stage_mean = nct_df.get_mean(prefix=2)
    df_chamber_std = nct_df.get_std(prefix=-1)
    df_stage_std = nct_df.get_std(prefix=2)
    tm(df_chamber_mean, n1, "chamber", "mean")
    tm(df_stage_mean, n1, "stage", "mean")
    tm(df_chamber_std, n1, "chamber", "std")
    tm(df_stage_std, n1, "stage", "std")


def tm(df, n1, n2, n3):
    df_t = df.loc[df.index.str.contains("AY|BY|CY|DY"), :]
    df_m = df.loc[df.index.str.contains("AZ|BZ|CZ|DZ"), :]
    save_csv(df, f"./data/temp/{n1}/{n2}/{n3}/complete.csv")
    save_csv(df_t, f"./data/temp/{n1}/{n2}/{n3}/traditional.csv")
    save_csv(df_m, f"./data/temp/{n1}/{n2}/{n3}/mechanical.csv")


def main():
    physic = pd.read_csv("./data/raw/physicochemical.csv", index_col=0)
    amino = pd.read_csv("./data/raw/amino_acid.csv", index_col=0)
    alpha = pd.read_csv("./data/raw/alpha.csv", index_col=0)
    generate(physic, "phy")
    generate(amino, "amino")
    generate(alpha, "alpha")


if __name__ == '__main__':
    main()
