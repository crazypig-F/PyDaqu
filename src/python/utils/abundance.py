import pandas as pd

import config
from src.python.utils.stack import StackData


def microbe_abundance():
    bacteria = pd.read_csv(config.basedir + '/data/result/micro/mean/bacteria genus top20.csv', index_col=0)
    fungi = pd.read_csv(config.basedir + '/data/result/micro/mean/fungi genus top20.csv', index_col=0)
    bacteria_stack = StackData(bacteria)
    fungi_stack = StackData(fungi)
    bacteria_abundance = bacteria_stack.abundance(rel=True)
    fungi_abundance = fungi_stack.abundance(rel=True)
    bacteria_abundance.to_csv(config.basedir + "/data/result/abundance/bacteria.csv")
    fungi_abundance.to_csv(config.basedir + "/data/result/abundance/fungi.csv")


def AAs_abundance():
    AAs = pd.read_csv(config.basedir + '/data/result/AAs/AAs stage mean.csv', index_col=0)
    stack = StackData(AAs.T)
    abundance = stack.abundance(rel=False)
    abundance.to_csv(config.basedir + "/data/result/abundance/AAs.csv")


if __name__ == '__main__':
    microbe_abundance()
    AAs_abundance()
