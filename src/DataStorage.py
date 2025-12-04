from const import DatabaseType
import pandas as pd
import sqlite3
import logging
logging.basicConfig(level=logging.INFO)


class DataStorage:


    def __init__(self, storage_type: DatabaseType) -> None:
        self.database_type = storage_type

    def save_to_sql(self, df: pd.DataFrame, table_name: str) -> None:
        if self.database_type == DatabaseType.SQLITE:
            try:
                db_file_name = f"{DatabaseType.SQLITE.value}.db"
                conn = sqlite3.connect(db_file_name)
                df.to_sql(table_name, conn, if_exists='replace', index=True)
                logging.info(f"Dataframe saved to database")
            except Exception as e:
                raise RuntimeError(f"Cant commit data to SQLite due to: {e}")
            finally:
                conn.close()
