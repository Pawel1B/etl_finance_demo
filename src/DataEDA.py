import pandas as pd
from matplotlib import pyplot as plt
import sqlite3
from src.FeatureEngineer import FeatureEngineer
from datetime import datetime



class DataEDA():
    def __init__(self, conn: sqlite3.Connection, ticker: str, ticker_timeline: list|None=None) -> None:
        self.df = self._load_ticker(conn, ticker, ticker_timeline)
        self._featureEngineer = FeatureEngineer(self.df)

    def _load_ticker(self, conn: sqlite3.Connection, ticker: str, time_start: datetime|None = None, time_stop: datetime|None = None) -> pd.DataFrame:
        if time_start is None and time_stop is None:
            query = f"SELECT * FROM {ticker}"
        else:
            query = f"SELECT * FROM {ticker} WHERE date BETWEEN {time_start} AND {time_stop}"
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

    def plot_feature(self, feature: str, time_start: datetime|None = None, time_stop: datetime|None = None) -> None:
        if time_start is None and time_stop is None:
            plt.figure(figsize=(14,7))
            plt.plot(self.df.index, self.df[feature])
            plt.show()
        elif time_stop is None:
            plt.figure(figsize=(14,7))
            plt.plot(self.df.index[self.df.index > time_start],
                     self.df[feature].loc[self.df.index > time_start])
            plt.show()
        else:
            plt.figure(figsize=(14,7))
            plt.plot(self.df.index[self.df.index > time_start and self.df.index < time_stop],
                     self.df[feature].loc[self.df.index > time_start and self.df.index < time_stop])
            plt.show()

    def get_feature_names(self) -> None:
        print(self.df.columns.values)

    @property
    def featureEngineer(self) -> FeatureEngineer:
        return self._featureEngineer
