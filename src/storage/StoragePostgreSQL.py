import pandas as pd
from urllib.parse import quote_plus
from sqlalchemy import create_engine
from src.storage.Storage import Storage
from config import PostgresConfig
import logging
logging.basicConfig(level=logging.INFO)


class StoragePostgreSQL(Storage[PostgresConfig]):

    def data_load(self, ticker_name: str) -> pd.DataFrame:
        try:
            conn_string = self._get_sqlalchemy_engine_url()
            engine = create_engine(conn_string)

            query = f"SELECT * FROM {ticker_name}"
            df = pd.read_sql(query, engine)
            df["date"] = pd.to_datetime(df["date"])
            df = df.set_index(df["date"])
            df = df.drop(columns="date")
            logging.info(f"Dataframe loaded from database")
        except Exception as e:
            raise RuntimeError(f"Cant read data from PostgreSQL due to: {e}")
        return df

    def data_save(self, ticker_name: str, data: pd.DataFrame) -> None:
        try:
            conn_string = self._get_sqlalchemy_engine_url()
            engine = create_engine(conn_string)

            data.to_sql(ticker_name, engine, if_exists='replace', index=True)
            logging.info(f"Dataframe saved to database")
        except Exception as e:
            raise RuntimeError(f"Cant commit data to PostgreSQL due to: {e}")

    def _get_sqlalchemy_engine_url(self) -> str:
        return "postgresql+psycopg2://{user}:{password}@{host}:{port}/{dbname}".format(
            user = quote_plus(self.config.user),
            password = quote_plus(self.config.password),
            host = self.config.host,
            port = self.config.port,
            dbname = self.config.dbname,
        )
