import math

from sklearn.ensemble import RandomForestClassifier

from analyze.ml import plot
from analyze.ml.model import Model


class ProcessClassifyModel(Model):
    def __init__(self, X, y, test_size=0.3, seed=42):
        self.X = X
        self.y = y
        super().__init__(self.X, self.y, test_size=test_size, seed=seed)

    def train(self):
        model = RandomForestClassifier(n_estimators=50, random_state=self.seed)
        score_sum = 0
        kf_num = 4
        for idx, (X_train, X_test, y_train, y_test) in enumerate(self.cv_my(kf_num)):
            print("训练数据形状：", X_train.shape)
            print("测试数据形状：", X_test.shape)
            model.fit(X_train, y_train)
            y_p = model.predict(X_test)
            score = sum(y_p == y_test) / len(y_p)
            print(f"第{idx+1}次交叉验证准确率结果:", score)
            score_sum += score
            plot.plot_cm_process(idx, y_test, y_p)
            plot.plot_feature(idx, model, self.X.columns)
        return score_sum / kf_num
