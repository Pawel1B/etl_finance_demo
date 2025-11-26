from enum import Enum
from datetime import datetime

class DataDownloadSource(Enum):
    STOOQ_PL = "stooq"
    ...

class DatabaseType(Enum):
    S3 = "s3"
    POSTGRESQL = "PostgreSQL"
    SQLITE = "SQLite"

OHLC_COLUMN_NAMES = ("date", "open", "high", "low", "close", "volume")
