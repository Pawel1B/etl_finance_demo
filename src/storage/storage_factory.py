from const import DATABASE_TYPE
from src.storage.Storage import Storage
from src.storage.StorageSQLite import StorageSQLite
from src.storage.StoragePostgreSQL import StoragePostgreSQL
from src.storage.StorageRedis import StorageRedis
from config import get_config

def get_storage(db: DATABASE_TYPE) -> Storage:
    if db == DATABASE_TYPE.SQLITE:
        return StorageSQLite(get_config(db))
    elif db == DATABASE_TYPE.POSTGRESQL:
        return StoragePostgreSQL(get_config(db))
    elif db == DATABASE_TYPE.REDIS:
        return StorageRedis(get_config(db))
    else:
        raise ValueError(f"Unsupported database: {db}")