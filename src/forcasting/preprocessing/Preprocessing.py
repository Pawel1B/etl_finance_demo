from abc import ABC, abstractmethod
import numpy as np
from typing import Any


class Preprocessing(ABC):

    @abstractmethod
    def fit(self, x_data: np.array) -> None:
        ...

    @abstractmethod
    def transform(self, x_data: np.array) -> Any:
        ...
