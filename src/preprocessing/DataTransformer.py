from const import OHLC_COLUMN_NAMES
from io import StringIO
import pandas as pd
import logging
logger = logging.getLogger(__name__)


class DataTransformer:


    def get_dataframe(self, response: str) -> pd.DataFrame:
        return pd.read_csv(StringIO(response))

    def clean_dataframe(self, df: pd.DataFrame) -> pd.DataFrame:
        self._transform_column_names(df)
        self._transform_data_types(df)
        self._validate_data_values(df)
        logger.info(f"Dataframe cleaned")
        return df.set_index("date")

    def _transform_column_names(self, df: pd.DataFrame) -> None:
        try:
            df.columns = OHLC_COLUMN_NAMES
        except Exception as e:
            msg = f"Error with assigment of new column names: {e}"
            logger.error(msg)
            raise RuntimeError(msg)

    def _transform_data_types(self, df: pd.DataFrame) -> None:
        try:
            df["date"] = pd.to_datetime(df["date"])
            ohlc_cols = ['open', 'high', 'low', 'close']
            df[ohlc_cols] = df[ohlc_cols].astype('float64')
            df["volume"] = df["volume"].astype("int64")
        except Exception as e:
            msg = f"Error with data type transformation: {e}"
            logger.error(msg)
            raise RuntimeError(msg)

    def _validate_data_values(self, df: pd.DataFrame) -> None:
        if (df["volume"] < 0).any():
            logging.error("volume is negative")
            raise ValueError("volume is negative")
        if (df["low"] > df["high"]).any():
            logging.error("low is bigger than high")
            raise ValueError("low is bigger than high")
        # df = df.dropna()#TODO handle nan values
        if df.isna().sum().sum() > 0:
            logging.error("There are nan values")
            raise ValueError("There are nan values")
        if df["date"].nunique() != len(df):
            logging.error("Dates are not unique")
            raise ValueError("Dates are not unique")
