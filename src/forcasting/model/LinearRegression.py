from src.forcasting.model.ForcastingModel import ForcastingModel
from sklearn.linear_model import Lasso
import numpy as np
import pickle


class LinearRegression(ForcastingModel):

    def __init__(self, alpha:float = 2) -> None:
        self.model: Lasso = Lasso(alpha = alpha)

    def train_model(self, train_data: list) -> None:
        x_train, y_train = train_data
        self.model.fit(x_train, y_train)

    def test_model(self, test_data: list) -> None:
        x_test, y_test = test_data
        print(self.model.score(x_test, y_test))

    def predict(self, data: np.array) -> np.array:
        return self.model.predict(data)

    def save_model(self, path: str) ->None:
        with open(path,'wb') as f:
            pickle.dump(self.model, f)

    def load_model(self, path: str) -> None:
        with open(path, 'rb') as f:
            self.model = pickle.load(f)
