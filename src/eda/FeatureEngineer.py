import pandas as pd
import numpy as np

class FeatureEngineer:

    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df

    # stationary
    def add_spread(self) -> None:
        self.df["spread"] = self.df["high"] - self.df["low"]

    def add_price_change(self) -> None:
        self.df["price_change"] = self.df["close"] - self.df["open"]

    def add_relative_spread(self) -> None:
        self.df["relative_spread"] = (self.df["high"] - self.df["low"]) / self.df["close"]

    # period
    def add_returns(self, feature_name: str = "returns", period: int = 1) -> None:
        self.df[feature_name] = self.df["close"].pct_change(periods=period)

    def add_log_returns(self, feature_name: str = "log_returns", period: int = 1) -> None:
        self.df[feature_name] = np.log(self.df["close"]) - np.log(self.df["close"].shift(period))
        self.df[feature_name] = self.df[feature_name]

    def add_Simple_Moving_Average(self, feature_name: str = "SMA", period: int = 4) -> None:
        self.df[feature_name] = self.df["close"].rolling(period).mean()

    def add_rolling_volume(self, feature_name: str = "rolling_volume", period: int = 4) -> None:
        self.df[feature_name] = self.df["volume"].rolling(period).mean()

    def add_rolling_volume_zscore(self, feature_name: str = "rolling_volume_zscore", period: int = 21) -> None:
        volume_mean = self.df["volume"].rolling(period).mean()
        volume_std = self.df["volume"].rolling(period).std()
        self.df[feature_name] = (self.df["volume"] - volume_mean) / volume_std

    def add_momentum(self, feature_name: str = "momentum", period: int = 2) -> None:
        self.df[feature_name] = self.df["close"] - self.df["close"].shift(period)

    def add_rate_of_change(self, feature_name: str = "ROC", period:int = 1) -> None:
        self.df[feature_name] = (self.df["close"] / self.df["close"].shift(period)) - 1

    def add_rolling_volatility(self, feature_name: str = "rolling_volatility", period:int = 21) -> None:
        self.df[feature_name] = self.df["close"].pct_change().rolling(window=period).std()

    def add_rolling_Exponentional_Moving_Averages(self, feature_name: str = "EMA", period:int = 4) -> None:
        self.df[feature_name] = self.df["close"].ewm(span=period, adjust=False).mean()

    def add_MACD(self) -> None:
        ema_12 = self.df["close"].ewm(span=12, adjust=False).mean()
        ema_26 = self.df["close"].ewm(span=26, adjust=False).mean()

        self.df["macd"] = ema_12 - ema_26
        self.df["macd_signal"] = self.df["macd"].ewm(span=9, adjust=False).mean()
        self.df["macd_hist"] = self.df["macd"] - self.df["macd_signal"]

    def add_RSI(self, feature_name: str = "RSI", period:int = 14) -> None:
        delta = self.df["close"].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()

        rs = avg_gain / avg_loss
        self.df[feature_name] = 100 - (100 / (1 + rs))

    def add_std(self, feature_name: str = "std", period:int = 14) -> None:
        self.df[feature_name] = self.df["close"].rolling(period).std()

    # utility
    def handle_nan_values(self, method: str = "dropna") -> None:
        if method == "dropna":
            self.df.dropna()
