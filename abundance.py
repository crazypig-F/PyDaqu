import pandas as pd

from analyze.plot.stack import StackData
from utils import save_csv


def save_microbe(df, n1, n2):
    stack = StackData(df)
    abundance_r = stack.abundance()
    save_csv(abundance_r, f"./data/temp/abundance/{n1}/{n2}.csv")


def save_amino(df, n1, n2):
    stack = StackData(df)
    abundance_r = stack.abundance(rel=False)
    save_csv(abundance_r, f"./data/temp/abundance/{n1}/{n2}.csv")


def microbe_abundance():
    bacteria_complete = pd.read_csv("./data/temp/microbe/parallel/bacteria/top/complete.csv", index_col=0)
    bacteria_t = pd.read_csv("./data/temp/microbe/parallel/bacteria/top/traditional.csv", index_col=0)
    bacteria_m = pd.read_csv("./data/temp/microbe/parallel/bacteria/top/mechanical.csv", index_col=0)

    fungi_complete = pd.read_csv("./data/temp/microbe/parallel/fungi/top/complete.csv", index_col=0)
    fungi_t = pd.read_csv("./data/temp/microbe/parallel/fungi/top/traditional.csv", index_col=0)
    fungi_m = pd.read_csv("./data/temp/microbe/parallel/fungi/top/mechanical.csv", index_col=0)
    save_microbe(bacteria_complete, "bacteria", "complete")
    save_microbe(bacteria_t, "bacteria", "traditional")
    save_microbe(bacteria_m, "bacteria", "mechanical")
    save_microbe(fungi_complete, "fungi", "complete")
    save_microbe(fungi_t, "fungi", "traditional")
    save_microbe(fungi_m, "fungi", "mechanical")

    bacteria_env_complete = pd.read_csv("./data/temp/microbe/parallel_env/bacteria/top/complete.csv", index_col=0)
    bacteria_env_t = pd.read_csv("./data/temp/microbe/parallel_env/bacteria/top/traditional.csv", index_col=0)
    bacteria_env_m = pd.read_csv("./data/temp/microbe/parallel_env/bacteria/top/mechanical.csv", index_col=0)

    fungi_env_complete = pd.read_csv("./data/temp/microbe/parallel_env/fungi/top/complete.csv", index_col=0)
    fungi_env_t = pd.read_csv("./data/temp/microbe/parallel_env/fungi/top/traditional.csv", index_col=0)
    fungi_env_m = pd.read_csv("./data/temp/microbe/parallel_env/fungi/top/mechanical.csv", index_col=0)
    save_microbe(bacteria_env_complete, "bacteria_env", "complete")
    save_microbe(bacteria_env_t, "bacteria_env", "traditional")
    save_microbe(bacteria_env_m, "bacteria_env", "mechanical")
    save_microbe(fungi_env_complete, "fungi_env", "complete")
    save_microbe(fungi_env_t, "fungi_env", "traditional")
    save_microbe(fungi_env_m, "fungi_env", "mechanical")


def amino_abundance():
    amino_t = pd.read_csv("./data/temp/amino/stage/mean/traditional.csv", index_col=0)
    amino_m = pd.read_csv("./data/temp/amino/stage/mean/mechanical.csv", index_col=0)
    save_amino(amino_t.T, "stack", "traditional")
    save_amino(amino_m.T, "stack", "mechanical")


def main():
    microbe_abundance()
    amino_abundance()


if __name__ == '__main__':
    main()
