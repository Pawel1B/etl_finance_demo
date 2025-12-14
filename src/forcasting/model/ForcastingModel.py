from abc import ABC, abstractmethod
from typing import Any
import numpy as np


class ForcastingModel(ABC):

    @abstractmethod
    def train_model(self, train_data: list) -> None:
        ...

    @abstractmethod
    def test_model(self, test_data: list) -> None:
        ...

    @abstractmethod
    def predict(self, data: Any) -> np.array:
        ...

    @abstractmethod
    def save_model(self, path: str) ->None:
        ...

    @abstractmethod
    def load_model(self, path: str) -> None:
        ...
