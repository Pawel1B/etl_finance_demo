from pydantic import BaseModel
from const import DATABASE_TYPE
import yaml
from dotenv import load_dotenv
import os

class DatabaseConfig(BaseModel):
    ...

class SQLiteConfig(DatabaseConfig):
    path: str

class PostgresConfig(DatabaseConfig):
    host: str
    dbname: str
    user: str
    password: str
    port: int

class RedisConfig(DatabaseConfig):
    ...

def get_config(databaseType: DATABASE_TYPE) -> DatabaseConfig:
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    match databaseType:
        case DATABASE_TYPE.SQLITE:
            return SQLiteConfig(**config["database"]["sqlite"])
        case DATABASE_TYPE.POSTGRESQL:
            load_dotenv()
            config = PostgresConfig(**config["database"]["postgres"])
            config.password = os.getenv(config.password)
            return config
        case DATABASE_TYPE.REDIS:
            ...
        case _:
            raise ValueError(f"Unsupported Database type: {databaseType}")
