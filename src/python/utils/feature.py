import numpy as np
import pandas as pd

import config


def normalization(data):
    _range = np.max(data) - np.min(data)
    return (data - np.min(data)) / _range


def feature_select():
    vip = pd.read_csv(config.basedir + '/data/result/ml/PLSR feature importance.csv', index_col=0)
    importance = pd.read_csv(config.basedir + '/data/result/ml/RF feature importance.csv', index_col=0)
    shap = pd.read_csv(config.basedir + '/data/result/ml/XGBoost feature importance.csv', index_col=0)
    feature1, feature2, feature3 = [], [], []
    for col in vip.columns:
        v = normalization(vip[col])
        i = normalization(importance[col])
        s = normalization(shap[col])
        r = (v + i + s).sort_values(ascending=False)
        feature1.append(r.index[0])
        feature2.append(r.index[1])
        feature3.append(r.index[2])
    feature = pd.DataFrame({"v1": feature1, "v2": feature2, "v3": feature3}, index=vip.columns)
    feature.to_csv(config.basedir + '/data/result/ml/AAs_feature.csv')
    print(pd.Series(feature1 + feature2 + feature3).value_counts())


if __name__ == '__main__':
    feature_select()
