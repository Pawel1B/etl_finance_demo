import redis
import pandas as pd
from src.storage.Storage import Storage
from config import RedisConfig
import logging
logging.basicConfig(level=logging.INFO)


class StorageRedis(Storage[RedisConfig]):

    def data_load(self, ticker_name: str) -> pd.DataFrame:
        try:
            r = redis.Redis(host=self.config.host, port=self.config.port)
            df = pd.DataFrame(r.get(ticker_name))
            df["date"] = pd.to_datetime(df["date"])
            df = df.set_index(df["date"])
            df = df.drop(columns="date")

            logging.info(f"Dataframe loaded from memory")
        except Exception as e:
            raise RuntimeError(f"Cant read data from Redis due to: {e}")
        return df

    def data_save(self, ticker_name: str, data: pd.DataFrame) -> None:
        try:
            r = redis.Redis(host=self.config.host, port=self.config.port)
            r.set(ticker_name, data)

            logging.info(f"Dataframe saved to memory")
        except Exception as e:
            raise RuntimeError(f"Cant commit data to Redis due to: {e}")
