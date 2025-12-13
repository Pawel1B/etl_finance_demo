from abc import ABC, abstractmethod
import pandas as pd
import numpy as np


class ForcastingModel(ABC):

    @abstractmethod
    def train_model(self, train_data: pd.DataFrame) -> None:
        ...

    @abstractmethod
    def test_model(self, test_data: pd.DataFrame) -> None:
        ...

    @abstractmethod
    def predict(self) -> np.array:
        ...

    @abstractmethod
    def save_model(self, path: str) ->None:
        ...

    @abstractmethod
    def load_model(self, path: str) -> None:
        ...
