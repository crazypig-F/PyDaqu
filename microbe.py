import pandas as pd

from src.python.micro.amplicon import AmpliconStatistics


def asv2genus():
    amplicon_b = AmpliconStatistics('./data/raw/Daqu bacteria asv.csv', 'taxonomy')
    amplicon_f = AmpliconStatistics('./data/raw/Daqu fungi asv.csv', 'taxonomy')
    amplicon_b.get_top(20).to_csv('./data/result/Daqu bacteria genus top20.csv')
    amplicon_f.get_top(20).to_csv('./data/result/Daqu fungi genus top20.csv')


if __name__ == '__main__':
    asv2genus()
