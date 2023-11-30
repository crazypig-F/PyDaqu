import math

from sklearn.ensemble import RandomForestRegressor, GradientBoostingRegressor
from sklearn.linear_model import LinearRegression
from sklearn.metrics import r2_score
from sklearn.svm import SVR
from xgboost import XGBRegressor
from analyze.ml.model import Model


class RegressionModel(Model):
    def __init__(self, X, y, test_size=0.3, seed=42):
        super().__init__(X, y, test_size=test_size, seed=seed)

    def train(self):
        model = RandomForestRegressor(n_estimators=50, random_state=42)
        # model = GradientBoostingRegressor(n_estimators=50, random_state=42)
        # model = XGBRegressor(n_estimators=50, random_state=42)
        # X_train, X_test, y_train, y_test = self.split()
        best_r = None
        best_p = None
        best_s = -math.inf
        score_sum = 0
        kf_num = 4
        for X_train, X_test, y_train, y_test in self.cv(kf_num):
            model.fit(X_train, y_train)
            y_p = model.predict(X_test)
            score = r2_score(y_test, y_p)
            if score > best_s:
                best_r = y_test
                best_p = y_p
                best_s = score
            score_sum += score
        return best_r.to_list(), best_p, score_sum / kf_num, best_s
