import numpy as np
import pandas as pd
import sklearn
import xgboost
from sklearn.cross_decomposition import PLSRegression
from sklearn.ensemble import RandomForestRegressor
from sklearn.metrics import r2_score, mean_squared_error
from xgboost import XGBRegressor

from correlation import mapping_asv_select
from src.python.ml.regression import RegressionModel
from src.python.utils.importance import get_vips, get_shap

model = {
    "PLSR": PLSRegression(n_components=2),
    "XGBoost": XGBRegressor(n_estimators=100, random_state=42),
    "RF": RandomForestRegressor(n_estimators=100, random_state=42)
}


def AAs_select_feature():
    AAs = pd.read_csv("./data/result/AAs/AAs mean.csv", index_col=0)
    asv = pd.read_csv("./data/result/micro/mean/asv 30% mean.csv", index_col=0)
    asv = asv.loc[:, mapping_asv_select()]
    for m in model:
        print(m)
        model_score = pd.DataFrame()
        for AA in AAs.columns:
            reg = RegressionModel(asv, AAs[AA], model[m], test_size=0.3, seed=42)
            y = reg.model.predict(reg.X_test)
            r2 = r2_score(y, reg.y_test)
            mse = mean_squared_error(y, reg.y_test)
            print(AA, r2, mse)
            asv_sort, importance_sort = feature_select_top3(asv, reg)
            score = pd.DataFrame({"importance": importance_sort}, index=asv_sort)
            model_score = pd.concat([model_score, score], axis=1)
        model_score.columns = AAs.columns
        model_score.to_csv(f"./data/result/ml/{m} feature importance.csv")


def feature_select_top3(asv, reg):
    # 随机森林挑选特征重要性排名前3的微生物
    asv_sort = []
    importance_sort = []
    target_asv = []
    if isinstance(reg.model, sklearn.ensemble.RandomForestRegressor):
        importances = reg.model.feature_importances_
        indices = np.argsort(importances)[::-1]
        for i in range(asv.shape[1]):
            asv_sort.append(asv.columns[indices[i]])
            importance_sort.append(importances[indices[i]])

    # 偏最小二乘回归筛选vip排名前3的微生物
    if isinstance(reg.model, sklearn.cross_decomposition.PLSRegression):
        importances = get_vips(asv, reg.model)
        indices = np.argsort(importances)[::-1]
        for i in range(asv.shape[1]):
            asv_sort.append(asv.columns[indices[i]])
            importance_sort.append(importances[indices[i]])

    # xgboost筛选shap排名前3的微生物
    if isinstance(reg.model, xgboost.XGBRegressor):
        importance = get_shap(asv, reg.model)
        for idx in importance.index:
            asv_sort.append(idx)
            importance_sort.append(importance.loc[idx])

    return asv_sort, importance_sort


def predict_test():
    AAs = pd.read_csv("./data/result/AAs/AAs mean.csv", index_col=0)
    asv = pd.read_csv("./data/result/micro/mean/asv 30% mean.csv", index_col=0)
    fp = pd.read_csv("./data/result/fermentation parameters/fermentation parameters mean.csv", index_col=0)
    moisture = fp['Moisture (%)']
    for m in model:
        print(m)
        score1, score2, score3 = [], [], []
        score_mean1, score_mean2, score_mean3 = 0, 0, 0
        for AA in AAs.columns:
            asv_select = asv.loc[:,
                         ['B_ASV_15625', 'B_ASV_95119', 'B_ASV_125122', 'B_ASV_143173', 'B_ASV_131779']
                         ]
            X = asv_select
            reg = RegressionModel(X, AAs[AA], model[m], test_size=0.3, seed=42)
            y = reg.model.predict(reg.X_test)
            r2 = r2_score(reg.y_test, y)
            score_mean1 += r2
            score1.append(round(r2, 6))

            X = pd.concat([moisture], axis=1)
            if m == "PLSR":
                model[m] = PLSRegression(n_components=1)
            reg = RegressionModel(X, AAs[AA], model[m], test_size=0.3, seed=42)
            y = reg.model.predict(reg.X_test)
            r2 = r2_score(reg.y_test, y)
            score_mean2 += r2
            score2.append(round(r2, 6))
            model['PLSR'] = PLSRegression(n_components=2)

            X = pd.concat([asv_select, moisture], axis=1)
            reg = RegressionModel(X, AAs[AA], model[m], test_size=0.3, seed=42)
            y = reg.model.predict(reg.X_test)
            r2 = r2_score(reg.y_test, y)
            score_mean3 += r2
            score3.append(round(r2, 6))
        print(score_mean1 / 20, score_mean2 / 20, score_mean3 / 20)
        print((score_mean3 - score_mean1) / score_mean1 * 100)
        print((score_mean3 - score_mean2) / score_mean2 * 100)
        pd.DataFrame({"ASV": score1, "Moisture": score2, "ASV with Moisture": score3}, index=AAs.columns).to_csv(
            f"./data/result/ml/{m} predict score.csv")


def best_model():
    score_PLSR = pd.read_csv("./data/result/ml/PLSR predict score.csv", index_col=0)
    score_XGBoost = pd.read_csv("./data/result/ml/XGBoost predict score.csv", index_col=0)
    score_RF = pd.read_csv("./data/result/ml/RF predict score.csv", index_col=0)
    model_dict = {}
    score_dict = {}
    for idx in score_PLSR.index:
        s1, s2 = score_PLSR.loc[idx, 'ASV'], score_PLSR.loc[idx, 'ASV with Moisture']
        s3, s4 = score_XGBoost.loc[idx, 'ASV'], score_XGBoost.loc[idx, 'ASV with Moisture']
        s5, s6 = score_RF.loc[idx, 'ASV'], score_RF.loc[idx, 'ASV with Moisture']
        score_list = [s1, s2, s3, s4, s5, s6]
        max_score = max(score_list)
        max_index = score_list.index(max_score)
        if max_index == 0:
            model_dict[idx] = "PLSR ASV"
        elif max_index == 1:
            model_dict[idx] = "PLSR ASV + M"
        elif max_index == 2:
            model_dict[idx] = "XGBoost ASV"
        elif max_index == 3:
            model_dict[idx] = "XGBoost ASV + M"
        elif max_index == 4:
            model_dict[idx] = "RF ASV"
        else:
            model_dict[idx] = "RF ASV + M"
        score_dict[idx] = max_score

    return model_dict, score_dict


def best_model_prediction_value():
    model_dict, score_dict = best_model()
    print(model_dict)
    print(score_dict)
    AAs = pd.read_csv("./data/result/AAs/AAs mean.csv", index_col=0)
    asv = pd.read_csv("./data/result/micro/mean/asv 30% mean.csv", index_col=0)
    fp = pd.read_csv("./data/result/fermentation parameters/fermentation parameters mean.csv", index_col=0)
    moisture = fp['Moisture (%)']
    predict = {}
    measure = {}
    for key, val in model_dict.items():
        asv_select = asv.loc[:,
                     ['B_ASV_15625', 'B_ASV_95119', 'B_ASV_125122', 'B_ASV_143173', 'B_ASV_131779']
                     ]
        X = asv_select
        if "+ M" in val:
            X = pd.concat([asv_select, moisture], axis=1)
        if "RF" in val:
            reg = RegressionModel(X, AAs[key], model["RF"], test_size=0.3, seed=42)
        elif "PLSR" in val:
            reg = RegressionModel(X, AAs[key], model["PLSR"], test_size=0.3, seed=42)
        else:
            reg = RegressionModel(X, AAs[key], model["XGBoost"], test_size=0.3, seed=42)
        y = reg.model.predict(reg.X_test)
        r2 = r2_score(reg.y_test, y)
        predict[key] = y
        measure[key] = reg.y_test
        print(key, r2, score_dict[key])
    pd.DataFrame(predict).to_csv("./data/result/ml/predict value.csv")
    pd.DataFrame(measure).to_csv("./data/result/ml/measure value.csv")
    pd.DataFrame({"score": score_dict.values(), "model": model_dict.values()}, index=list(score_dict.keys())).to_csv(
        "./data/result/ml/score model.csv")


if __name__ == '__main__':
    # AAs_select_feature()
    # predict_test()
    best_model_prediction_value()
