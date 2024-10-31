from src.python.ml.model import Model


class RegressionModel(Model):
    def __init__(self, X, y, model, test_size=0.3, seed=42):
        super().__init__(X, y, test_size=test_size, seed=seed)
        self.model = model
        self._train()

    def _train(self):
        self.model.fit(self.X_train, self.y_train)
