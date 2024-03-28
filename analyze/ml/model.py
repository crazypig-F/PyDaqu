import random

import pandas as pd
from sklearn.model_selection import train_test_split


class Model:
    def __init__(self, X, y, test_size=0.25, seed=42):
        self.test_size = test_size
        random.seed(seed)
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(X, y, test_size=test_size, random_state=seed)
        # print(self.y_test.value_counts())

        # self.X_train, self.X_test, self.y_train, self.y_test = self.dataset_split(X, y)

    def dataset_split(self, X, y):
        all_num = ["01", "02", "03", "04", "05", "06", "07", "08", "09", "10", "11", "12", "13", "14"]
        select_num = random.sample(all_num, 6)
        not_select_num = list(set(all_num) - set(select_num))
        return (
            X.loc[X.index.str.contains("|".join(not_select_num)), :],
            X.loc[X.index.str.contains("|".join(select_num)), :],
            y.loc[y.index.str.contains("|".join(not_select_num))],
            y.loc[y.index.str.contains("|".join(select_num))]
        )

    def split_my(self, X, y):
        n = X.shape[0] // 3
        tn = int(n * (1 - self.test_size))
        arr = list(range(n))
        random.shuffle(arr)
        train = []
        test = []
        for i in arr[:tn]:
            train.append(i * 3)
            train.append(i * 3 + 1)
            train.append(i * 3 + 2)
        for i in arr[tn:]:
            test.append(i * 3)
            test.append(i * 3 + 1)
            test.append(i * 3 + 2)
        random.shuffle(train)
        random.shuffle(test)
        return pd.DataFrame(X).iloc[train, :], pd.DataFrame(X).iloc[test, :], [y[i] for i in train], [y[i] for i in
                                                                                                      test]

    def cv_my(self, X, y, num=3):
        n = X.shape[0] // 3
        test_num = n // num
        arr = list(range(n))
        random.shuffle(arr)
        res = []
        for fold in range(num):
            train = []
            test = []
            for i in arr[(fold + 1) * test_num:] + arr[: fold * test_num]:
                train.append(i * 3)
                train.append(i * 3 + 1)
                train.append(i * 3 + 2)
            for i in arr[fold * test_num: (fold + 1) * test_num]:
                test.append(i * 3)
                test.append(i * 3 + 1)
                test.append(i * 3 + 2)
            random.shuffle(train)
            random.shuffle(test)
            res.append((pd.DataFrame(X).iloc[train, :], pd.DataFrame(X).iloc[test, :],
                        [y[i] for i in train], [y[i] for i in test]))
        return res
