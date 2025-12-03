import pandas as pd
import numpy as np

class FeatureEngineer:

    def __init__(self, df: pd.DataFrame):
        self.df = df

    # stationary
    def add_spread(self):
        self.df["spread"] = self.df["high"] - self.df["low"]

    def add_price_change(self):
        self.df["price_change"] = self.df["close"] - self.df["open"]

    def add_relative_spread(self):
        self.df["relative_spread"] = (self.df["high"] - self.df["low"]) / self.df["close"]

    # period
    def add_returns(self, feature_name: str = "returns", period: int = 1):
        self.df[feature_name] = self.df["close"].pct_change(periods=period)

    def add_log_returns(self, feature_name: str = "log_returns", period: int = 1):
        self.df[feature_name] = np.log(self.df["close"]) - np.log(self.df["close"].shift(period))
        self.df[feature_name] = self.df[feature_name]

    def add_rolling_mean(self, feature_name: str = "rolling_mean", period: int = 4):
        self.df[feature_name] = self.df["close"].rolling(period).mean()

    def add_rolling_volume(self, feature_name: str = "rolling_volume", period: int = 4):
        self.df[feature_name] = self.df["volume"].rolling(period).mean()

    def add_rolling_volume_zscore(self, feature_name: str = "rolling_volume_zscore", period: int = 21):
        volume_mean = self.df["volume"].rolling(period).mean()
        volume_std = self.df["volume"].rolling(period).std()
        self.df[feature_name] = (self.df["volume"] - volume_mean) / volume_std

    def add_momentum(self, feature_name: str = "momentum", period: int = 2):
        self.df[feature_name] = self.df["close"] - self.df["close"].shift(period)

    def add_rate_of_change(self, feature_name: str = "ROC", period:int = 1):
        self.df[feature_name] = (self.df["close"] / self.df["close"].shift(period)) - 1

    # utility
    def handle_nan_values(self, method: str = "dropna"):
        if method == "dropna":
            self.df.dropna()
