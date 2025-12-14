from src.forcasting.preprocessing.Preprocessing import Preprocessing
from sklearn.preprocessing import StandardScaler
import pandas as pd
import numpy as np


class NumpyPreprocessor(Preprocessing):

    def fit(self, x_data: np.array) -> None:
        self.scaler = StandardScaler()
        self.scaler.fit(x_data)

    def transform(self, x_data: np.array) -> np.array:
        return self.scaler.transform(x_data)
