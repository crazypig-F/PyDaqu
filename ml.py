import numpy as np
import pandas as pd

from analyze.ml.classify import ProcessClassifyModel


def process_predict():
    process_map = {"Y": 0, "Z": 1}
    microbe = pd.read_csv("./data/temp/microbe/parallel/merge/top/complete.csv", index_col=0)
    data = microbe.loc[microbe.index.str.startswith("D"), :]
    y = np.array([process_map[i[1]] for i in data.index])
    clf = ProcessClassifyModel(data, y, seed=42)
    s = clf.train()
    print(f"交叉验证平均结果", s)


def main():
    process_predict()


if __name__ == '__main__':
    main()
