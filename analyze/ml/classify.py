import math

import numpy as np
from matplotlib import pyplot as plt
from sklearn.ensemble import RandomForestClassifier
from sklearn.svm import SVC
from xgboost import XGBClassifier
from sklearn.tree import DecisionTreeClassifier
from sklearn.neighbors import KNeighborsClassifier

from analyze.ml import plot
from analyze.ml.model import Model
from sklearn.metrics import accuracy_score, precision_score, recall_score, f1_score, roc_curve, auc


class ProcessClassifyModel(Model):
    def __init__(self, X, y, test_size=0.3, seed=42):
        self.X = X
        self.y = y
        super().__init__(self.X, self.y, test_size=test_size, seed=seed)

    def train(self):
        model = RandomForestClassifier(n_estimators=100, random_state=self.seed)
        score_sum = 0
        kf_num = 4
        for idx, (X_train, X_test, y_train, y_test) in enumerate(self.cv_my(kf_num)):
            print("训练数据形状：", X_train.shape)
            print("测试数据形状：", X_test.shape)
            model.fit(X_train, y_train)
            y_p = model.predict(X_test)
            score = sum(y_p == y_test) / len(y_p)
            print(f"第{idx + 1}次交叉验证准确率结果:", score)
            score_sum += score
            # 创建画布
            # plot_roc_curve(estimator=model, X=X_test,
            #                y=y_test, linewidth=1)

            # 显示绘制的ROC曲线
            plt.show()
        return score_sum / kf_num


class PhaseClassifyModel(Model):
    def __init__(self, X, y, test_size=0.25, seed=42):
        super().__init__(X, y, test_size=test_size, seed=seed)
        # self.model = KNeighborsClassifier(n_neighbors=3)
        # self.model = SVC(kernel="rbf")
        # self.model = DecisionTreeClassifier(random_state=42)
        self.model = RandomForestClassifier(n_estimators=50, random_state=42)
        # self.model = XGBClassifier(n_estimators=50, random_state=42)

    def train(self):
        score_list = []
        for idx, (X_train, X_val, y_train, y_val) in enumerate(self.cv_my(self.X_train, self.y_train)):
            self.model.fit(X_train, y_train)
            y_p = self.model.predict(X_val)
            score = sum(y_p == y_val) / len(y_p)
            score_list.append(score)
            # plot.plot_cm(group + "_phase_" + str(idx), y_test, y_p)
            # plot.plot_feature(group + "_phase_" + str(idx), model, self.X.columns)
        score_sum = np.array(score_list)
        # print("验证集三折交叉验证平均准确率", score_sum.mean())
        return self.predict()

    def predict(self):
        y_p = self.model.predict(self.X_test)
        accuracy = accuracy_score(self.y_test, y_p)
        precision = precision_score(self.y_test, y_p, average='macro')
        recall = recall_score(self.y_test, y_p, average='macro')
        f1 = f1_score(self.y_test, y_p, average='macro')

        # print(f"准确率：{accuracy:.5}, 精确率：{precision:.5}，召回率：{recall:.5}，F1分数：{f1:.5}")
        return accuracy, precision, recall, f1
