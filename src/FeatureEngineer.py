import pandas as pd


class FeatureEngineer:

    def __init__(self, df: pd.DataFrame):
        self.df = df

    def add_returns(self, feature_name: str = "returns", period: int = 1):
        self.df[feature_name] = self.df["close"].pct_change(periods=period).dropna()

    def add_spread(self):
        self.df["spread"] = self.df["high"] - self.df["low"]

    def add_price_change(self):
        self.df["price_change"] = self.df["close"] - self.df["open"]
