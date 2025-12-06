import pandas as pd
from matplotlib import pyplot as plt
from src.storage.Storage import Storage
from src.eda.FeatureEngineer import FeatureEngineer
from datetime import datetime



class DataEDA():
    def __init__(self, data_storage: Storage, ticker: str) -> None:
        self.df = self._load_ticker(data_storage, ticker)
        self._featureEngineer = FeatureEngineer(self.df)

    def _load_ticker(self, data_storage: Storage, ticker: str) -> pd.DataFrame:
        return data_storage.data_load(ticker)

    def _get_df_time_mask(self, time_start: datetime|None = None, time_stop: datetime|None = None) -> pd.Series:
        if time_start is None and time_stop is None:
            mask = pd.Series(True, index=self.df.index)
        elif time_stop is None:
            mask = self.df.index > time_start
        else:
            mask = (self.df.index > time_start) & (self.df.index < time_stop)
        return mask

    def set_ticker_timeline(self, time_start: datetime, time_stop: datetime|None = None):
        if time_stop is None:
            self.df = self.df[self.df.index > time_start]
        else:
            self.df = self.df[self.df.index > time_start and self.df.index < time_stop]

    def get_ticker_dataframe(self) -> pd.DataFrame:
        return self.df

    def plot_ticker(self) -> None:
        figs, ax = plt.subplots(len(self.df.columns), 1, figsize=[14,15])
        for idx, variable in enumerate(self.df.columns):
            ax[idx].plot(self.df[variable])
            figs.show()

    def plot_feature(self, feature_name: str, time_start: datetime|None = None, time_stop: datetime|None = None) -> None:
        mask = self._get_df_time_mask(time_start=time_start, time_stop=time_stop)
        plt.figure(figsize=(14,7))
        plt.plot(self.df.index[mask], self.df[feature_name].loc[mask])
        plt.show()

    def plot_feature_rsi(self, feature_name: str = "RSI", time_start: datetime|None = None, time_stop: datetime|None = None) -> None:
        mask = self._get_df_time_mask(time_start=time_start, time_stop=time_stop)
        if feature_name not in self.df.columns.values:
            self._featureEngineer.add_RSI()
        plt.figure(figsize=(14,7))
        plt.plot(self.df.index[mask], self.df[feature_name].loc[mask])
        plt.axhline(30, color="red", linestyle="--")
        plt.axhline(70, color="green", linestyle="--")
        plt.show()

    def plot_feature_bollinger(self, term: int = 20, time_start: datetime|None = None, time_stop: datetime|None = None) -> None:
        sma_term_feature_name = f"SMA_{term}"
        self._featureEngineer.add_Simple_Moving_Average(feature_name=sma_term_feature_name, period=term)
        std_feature_name = f"std_{term}"
        self._featureEngineer.add_std(feature_name=std_feature_name, period=term)
        if term >= 50:
            multiplier = 2.5
        elif term >= 20:
            multiplier = 2.0
        else:
            multiplier = 1.5
        self.df[f"Bollinger_Upper_{term}"] = self.df[sma_term_feature_name] + multiplier * self.df[std_feature_name]
        self.df[f"Bollinger_Lower_{term}"] = self.df[sma_term_feature_name] - multiplier * self.df[std_feature_name]

        mask = self._get_df_time_mask(time_start=time_start, time_stop=time_stop)
        plt.figure(figsize=(14,7))
        plt.plot(self.df.index[mask], self.df["close"].loc[mask])
        plt.plot(self.df.index[mask], self.df[f"Bollinger_Upper_{term}"][mask])
        plt.plot(self.df.index[mask], self.df[f"Bollinger_Lower_{term}"][mask])
        plt.fill_between(self.df.index[mask],
                         self.df[f"Bollinger_Lower_{term}"][mask],
                         self.df[f"Bollinger_Upper_{term}"][mask],
                         alpha=0.2)
        plt.show()


    def get_feature_names(self) -> None:
        print(self.df.columns.values)

    @property
    def featureEngineer(self) -> FeatureEngineer:
        return self._featureEngineer
