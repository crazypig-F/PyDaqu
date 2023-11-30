import pandas as pd
import path

from analyze.plot.stack import StackData
from utils import save_csv


def save(df, n1, n2):
    stack = StackData(df)
    abundance_r = stack.abundance()
    save_csv(abundance_r, f"./data/temp/abundance/{n1}/{n2}.csv")


def save_abundance():
    bacteria_complete = pd.read_csv("./data/temp/microbe/parallel/bacteria/top/complete.csv", index_col=0)
    bacteria_t = pd.read_csv("./data/temp/microbe/parallel/bacteria/top/traditional.csv", index_col=0)
    bacteria_m = pd.read_csv("./data/temp/microbe/parallel/bacteria/top/mechanical.csv", index_col=0)

    fungi_complete = pd.read_csv("./data/temp/microbe/parallel/fungi/top/complete.csv", index_col=0)
    fungi_t = pd.read_csv("./data/temp/microbe/parallel/fungi/top/traditional.csv", index_col=0)
    fungi_m = pd.read_csv("./data/temp/microbe/parallel/fungi/top/mechanical.csv", index_col=0)
    save(bacteria_complete, "bacteria", "complete")
    save(bacteria_t, "bacteria", "traditional")
    save(bacteria_m, "bacteria", "mechanical")
    save(fungi_complete, "fungi", "complete")
    save(fungi_t, "fungi", "traditional")
    save(fungi_m, "fungi", "mechanical")


def main():
    save_abundance()


if __name__ == '__main__':
    main()
