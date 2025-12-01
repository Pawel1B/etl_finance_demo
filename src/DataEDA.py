import pandas as pd
from matplotlib import pyplot as plt
import sqlite3
import datetime



class DataEDA():
    def __init__(self, conn: sqlite3.Connection, ticker: str, ticker_timeline: list|None=None):
        self.df = self._load_ticker(conn, ticker, ticker_timeline)

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

    #NOTE features can be added via name of feature or feature expression, for that standardised format is required, swap dataframe to class may solve some design issues
    def add_features(self, feature_name: str, feature_expr: function = ...):
        ...
