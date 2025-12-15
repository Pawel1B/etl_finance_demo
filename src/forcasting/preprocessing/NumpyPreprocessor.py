from src.forcasting.preprocessing.Preprocessing import Preprocessing
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np


class NumpyPreprocessor(Preprocessing):

    def fit(self, x_data: np.array) -> None:
        if len(np.shape(x_data)) > 2:
            self.scaler = StandardScaler()
            X_train_2d = x_data.reshape(-1, x_data.shape[-1])
            self.scaler.fit(X_train_2d)
        else:
            self.scaler = StandardScaler()
            self.scaler.fit(x_data)

    def transform(self, x_data: np.array) -> np.array:
        if len(np.shape(x_data)) > 2:
            X_train_2d = x_data.reshape(-1, x_data.shape[-1])
            return self.scaler.transform(X_train_2d).reshape(x_data.shape)
        else:
            return self.scaler.transform(x_data)
