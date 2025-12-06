from enum import Enum

class DATA_DOWNLOAD_SOURCE(Enum):
    STOOQ_PL = "stooq"
    ...

class DATABASE_TYPE(Enum):
    S3 = "s3"
    POSTGRESQL = "PostgreSQL"
    SQLITE = "SQLite"

OHLC_COLUMN_NAMES = ("date", "open", "high", "low", "close", "volume")
