import pandas as pd
import sqlite3
from src.storage.Storage import Storage
import logging
logging.basicConfig(level=logging.INFO)


class StorageSQLite(Storage):

    def data_load(self, ticker_name: str) -> pd.DataFrame:
        try:
            db_file_name = self.config.path
            conn = sqlite3.connect(db_file_name)

            query = f"SELECT * FROM {ticker_name}"
            df = pd.read_sql(query, conn)
            df["date"] = pd.to_datetime(df["date"])
            df = df.set_index(df["date"])
            df = df.drop(columns="date")
            logging.info(f"Dataframe loaded from database")
        except Exception as e:
            raise RuntimeError(f"Cant read data from SQLite due to: {e}")
        finally:
            conn.close()
        return df

    def data_save(self, ticker_name: str, data: pd.DataFrame) -> None:
        try:
            db_file_name = self.config.path
            conn = sqlite3.connect(db_file_name)

            data.to_sql(ticker_name, conn, if_exists='replace', index=True)
            logging.info(f"Dataframe saved to database")
        except Exception as e:
            raise RuntimeError(f"Cant commit data to SQLite due to: {e}")
        finally:
            conn.close()
