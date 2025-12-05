from const import DatabaseType
from src.storage.Storage import Storage
from src.storage.StorageSQLite import StorageSQLite

def get_storage(db: DatabaseType) -> Storage:
    if db == DatabaseType.SQLITE:
        return StorageSQLite()
    else:
        raise ValueError(f"Unsupported database: {db}")