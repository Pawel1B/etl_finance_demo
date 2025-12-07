from const import OHLC_COLUMN_NAMES
from io import StringIO
import logging
logging.basicConfig(level=logging.INFO)
import pandas as pd

class DataTransformer:


    def get_dataframe(self, response: str) -> pd.DataFrame:
        return pd.read_csv(StringIO(response))

    def clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        self._transform_column_names(df)
        self._transform_data_types(df)
        self._validate_data_values(df)
        logging.info(f"Dataframe cleaned")
        return df.set_index("date")

    def _transform_column_names(self, df: pd.DataFrame) -> None:
        try:
            df.columns = OHLC_COLUMN_NAMES
        except Exception as e:
            raise RuntimeError(f"Error with assigment of new column names: {e}")

    def _transform_data_types(self, df: pd.DataFrame) -> None:
        try:
            df["date"] = pd.to_datetime(df["date"])
            ohlc_cols = ['open', 'high', 'low', 'close']
            df[ohlc_cols] = df[ohlc_cols].astype('float64')
            df["volume"] = df["volume"].astype("int64")
        except Exception as e:
            raise RuntimeError(f"Error with data type transformation: {e}")

    def _validate_data_values(self, df: pd.DataFrame) -> None:
        if (df["volume"] < 0).any():
            raise ValueError("volume is negative")
        if (df["low"] > df["high"]).any():
            raise ValueError("low is bigger than high")
        # df = df.dropna()#TODO handle nan values
        if df.isna().sum().sum() > 0:
            raise ValueError("There are nan values")
        if df["date"].nunique() != len(df):
            raise ValueError("Dates are not unique")
