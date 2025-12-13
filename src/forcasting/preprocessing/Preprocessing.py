from abc import ABC, abstractmethod
import pandas as pd
from typing import Any


class Preprocessing(ABC):

    @abstractmethod
    def fit(self, df: pd.DataFrame) -> None:
        ...

    @abstractmethod
    def transform(self, df: pd.DataFrame) -> Any:
        ...
