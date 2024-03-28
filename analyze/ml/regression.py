import math

import numpy as np
from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.model_selection import GridSearchCV
from sklearn.svm import SVR
from xgboost import XGBRegressor

from analyze.ml.model import Model


def relative_root_mean_squared_error(true, pred):
    rmse = np.sqrt(np.mean((true - pred) ** 2))
    # 计算观测数据的均值
    mean_observed = np.mean(true)
    # 计算相对均方根误差 (RRMSE)
    rrmse = (rmse / mean_observed) * 100
    return rrmse


def calculate_r2(observed, predicted):
    # 计算总平方和
    total_sum_of_squares = np.sum((observed - np.mean(observed)) ** 2)
    # 计算残差平方和
    residual_sum_of_squares = np.sum((observed - predicted) ** 2)
    # 计算R²
    r2 = 1 - (residual_sum_of_squares / total_sum_of_squares)
    return r2


class RegressionModel(Model):
    def __init__(self, X, y, test_size=0.25, seed=42):
        super().__init__(X, y, test_size=test_size, seed=seed)
        # self.model = LinearRegression()
        # self.model = GradientBoostingRegressor(n_estimators=50, random_state=42)
        # self.model = XGBRegressor(n_estimators=50, random_state=42)
        self.model = RandomForestRegressor(n_estimators=100, random_state=42)

    def search(self):
        # param_test = {"n_estimators": range(1, 501, 10)}
        param_test = {"max_features": range(1, 6, 1)}
        gsearch1 = GridSearchCV(estimator=RandomForestRegressor(), param_grid=param_test,
                                scoring='r2', cv=4)
        gsearch1.fit(self.X_train, self.y_train)
        print(gsearch1.best_params_)
        print("best accuracy:%f" % gsearch1.best_score_)

    def train(self):
        # score_list = []
        # for idx, (X_train, X_val, y_train, y_val) in enumerate(self.cv_my(self.X_train, self.y_train)):
        #     self.model.fit(X_train, y_train)
        #     y_p = self.model.predict(X_val)
        #     score = r2_score(y_val, y_p)
        #     score_list.append(score)
        # score_list = np.array(score_list)
        # print(score_list.mean())
        self.model.fit(self.X_train, self.y_train)
        p, r2 = self.predict()
        return self.y_test, p, r2

    def predict(self):
        y_p = self.model.predict(self.X_test)
        r2 = r2_score(self.y_test, y_p)
        # print(f"r2：{r2:.5}")
        return y_p, r2
