from config import DatabaseConfig
import pandas as pd
from abc import ABC, abstractmethod

class Storage(ABC):
    """Basic representation of data Storage"""
    def __init__(self, config: DatabaseConfig) -> None:
        self.config = config

    @abstractmethod
    def data_load(self, ticker_name: str) -> pd.DataFrame:
        """Load data from data storage"""

    @abstractmethod
    def data_save(self, ticker_name: str, data: pd.DataFrame) -> None:
        """Save data to storage"""
