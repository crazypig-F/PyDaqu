from sklearn.model_selection import train_test_split
from sklearn.preprocessing import scale


class Model:
    def __init__(self, X, y, test_size=0.3, seed=42):
        self.X_train, self.X_test, self.y_train, self.y_test = train_test_split(scale(X), y, test_size=test_size,
                                                                                random_state=seed)
        # self.X_valid, self.X_test, self.y_valid, self.y_test = train_test_split(self.X_test, self.y_test, test_size=0.5,
        #                                                                         random_state=seed)
