from typing import Any
import pandas as pd
import numpy as np
import yaml


class FeatureEngineer:

    descriptions_file = None
    general_description = None

    def __init__(self, df: pd.DataFrame) -> None:
        self.df = df
        self._load_descriptions("src\eda\docs\metric_descriptions.yaml")
        self._instance_descriptions: dict[str, str] = {}

    @classmethod
    def _load_descriptions(cls, path: str) ->None:
        if cls.descriptions_file is None:
            with open(path, "r") as f:
                cls.descriptions_file = yaml.safe_load(f)
                cls.general_description = cls.descriptions_file["general_description"]["description"]

    def describe(func: Any) -> Any:
        def wrapper(self: Any, *args: Any, **kwargs: Any) -> Any:
            if len(args) > 0:
                feature_name: str = args[0]
            elif "feature_name" in kwargs:
                feature_name = kwargs["feature_name"]
            else:
                feature_name = func.__defaults__[0]
            self._instance_descriptions[feature_name] = f"{self.__class__.descriptions_file[func.__name__]}\n{self.__class__.general_description}"
            return func(self, *args, **kwargs)
        return wrapper

    # stationary
    @describe
    def add_spread(self, feature_name: str = "spread") -> None:
        """spread is difference between high and low value of daily trades"""
        self.df[feature_name] = self.df["high"] - self.df["low"]

    @describe
    def add_price_change(self, feature_name: str = "price_change") -> None:
        """price_change is difference between close and open value of daily trades"""
        self.df["price_change"] = self.df["close"] - self.df["open"]

    @describe
    def add_relative_spread(self, feature_name: str = "relative_spread") -> None:
        """relative_spread = (high - low)/close of daily trades"""
        self.df[feature_name] = (self.df["high"] - self.df["low"]) / self.df["close"]

    # period
    @describe
    def add_returns(self, feature_name: str = "returns", period: int = 1) -> None:
        """returns percentage change of close value over period"""
        self.df[feature_name] = self.df["close"].pct_change(periods=period)

    @describe
    def add_log_returns(self, feature_name: str = "log_returns", period: int = 1) -> None:
        """log_returns difference in log of close value and close value at period"""
        self.df[feature_name] = np.log(self.df["close"]) - np.log(self.df["close"].shift(period))
        self.df[feature_name] = self.df[feature_name]

    @describe
    def add_Simple_Moving_Average(self, feature_name: str = "SMA", period: int = 4) -> None:
        """SMA average of close value over period"""
        self.df[feature_name] = self.df["close"].rolling(period).mean()

    @describe
    def add_rolling_volume(self, feature_name: str = "rolling_volume", period: int = 4) -> None:
        """rolling_volume average of volume value over period"""
        self.df[feature_name] = self.df["volume"].rolling(period).mean()

    @describe
    def add_rolling_volume_zscore(self, feature_name: str = "rolling_volume_zscore", period: int = 21) -> None:
        """rolling_volume_zscore (volume - volume mean)/ volume standard deviation over period"""
        volume_mean = self.df["volume"].rolling(period).mean()
        volume_std = self.df["volume"].rolling(period).std()
        self.df[feature_name] = (self.df["volume"] - volume_mean) / volume_std

    @describe
    def add_momentum(self, feature_name: str = "momentum", period: int = 2) -> None:
        """momentum difference between close value and close value at period"""
        self.df[feature_name] = self.df["close"] - self.df["close"].shift(period)

    @describe
    def add_rate_of_change(self, feature_name: str = "ROC", period:int = 1) -> None:
        """ROC (close / close at period) -1"""
        self.df[feature_name] = (self.df["close"] / self.df["close"].shift(period)) - 1

    @describe
    def add_rolling_volatility(self, feature_name: str = "rolling_volatility", period:int = 21) -> None:
        """momentum difference between close value and close value at period"""
        self.df[feature_name] = self.df["close"].pct_change().rolling(window=period).std()

    @describe
    def add_rolling_Exponentional_Moving_Averages(self, feature_name: str = "EMA", period:int = 4) -> None:
        """momentum difference between close value and close value at period"""
        self.df[feature_name] = self.df["close"].ewm(span=period, adjust=False).mean()

    @describe
    def add_MACD(self, feature_name: str = "macd") -> None:
        """momentum difference between close value and close value at period"""
        ema_12 = self.df["close"].ewm(span=12, adjust=False).mean()
        ema_26 = self.df["close"].ewm(span=26, adjust=False).mean()

        self.df[feature_name] = ema_12 - ema_26
        self.df[f"{feature_name}_signal"] = self.df[feature_name].ewm(span=9, adjust=False).mean()
        self.df[f"{feature_name}_hist"] = self.df[feature_name] - self.df[f"{feature_name}_signal"]

    @describe
    def add_RSI(self, feature_name: str = "RSI", period:int = 14) -> None:
        """momentum difference between close value and close value at period"""
        delta = self.df["close"].diff()
        gain = delta.clip(lower=0)
        loss = -delta.clip(upper=0)
        avg_gain = gain.rolling(window=period).mean()
        avg_loss = loss.rolling(window=period).mean()

        rs = avg_gain / avg_loss
        self.df[feature_name] = 100 - (100 / (1 + rs))

    @describe
    def add_std(self, feature_name: str = "std", period:int = 14) -> None:
        """std standard deviation over period"""
        self.df[feature_name] = self.df["close"].rolling(period).std()

    # utility
    def handle_nan_values(self, method: str = "dropna") -> None:
        """Handle nan values in dataframe based on method"""
        if method == "dropna":
            self.df.dropna(inplace=True)
