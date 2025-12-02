import pandas as pd
from matplotlib import pyplot as plt
import sqlite3
from src.FeatureEngineer import FeatureEngineer



class DataEDA():
    def __init__(self, conn: sqlite3.Connection, ticker: str, ticker_timeline: list|None=None):
        self.df = self._load_ticker(conn, ticker, ticker_timeline)
        self._featureEngineer = FeatureEngineer(self.df)

    def _load_ticker(self, conn: sqlite3.Connection, ticker: str, ticker_timeline:list|None) -> pd.DataFrame:
        if ticker_timeline is None:
            query = f"SELECT * FROM {ticker}"
        else:
            query = f"SELECT * FROM {ticker} WHERE date BETWEEN {ticker_timeline[0]} AND {ticker_timeline[1]}"
        df = pd.read_sql(query, conn)
        df["date"] = pd.to_datetime(df["date"])
        df = df.set_index(df["date"])
        df = df.drop(columns="date")
        return df

    def get_ticker_dataframe(self) -> pd.DataFrame:
        return self.df

    def plot_ticker(self) -> None:
        figs, ax = plt.subplots(len(self.df.columns), 1, figsize=[14,15])
        for idx, variable in enumerate(self.df.columns):
            ax[idx].plot(self.df[variable])
            figs.show()

    def plot_feature(self, feature: str, ticker_timeline: list|None=None):
        if ticker_timeline is None:
            plt.figure(figsize=(14,7))
            plt.plot(self.df.index, self.df[feature])
            plt.show()

    @property
    def featureEngineer(self) -> FeatureEngineer:
        return self._featureEngineer
