from const import DATABASE_TYPE
from src.storage.Storage import Storage
from src.storage.StorageSQLite import StorageSQLite

def get_storage(db: DATABASE_TYPE) -> Storage:
    if db == DATABASE_TYPE.SQLITE:
        return StorageSQLite()
    else:
        raise ValueError(f"Unsupported database: {db}")