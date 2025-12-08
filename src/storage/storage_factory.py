from const import DATABASE_TYPE
from src.storage.StorageSQLite import StorageSQLite
from src.storage.StoragePostgreSQL import StoragePostgreSQL
from src.storage.StorageRedis import StorageRedis
from config import get_config, SQLiteConfig, PostgresConfig, RedisConfig
from typing import Union


def get_storage(db: DATABASE_TYPE) -> Union[StorageSQLite, StoragePostgreSQL, StorageRedis]:
    config = get_config(db)
    if isinstance(config, SQLiteConfig):
        return StorageSQLite(config)
    elif isinstance(config, PostgresConfig):
        return StoragePostgreSQL(config)
    elif isinstance(config, RedisConfig):
        return StorageRedis(config)
    else:
        raise ValueError(f"Unsupported config for: {db}")