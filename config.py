from pydantic import BaseModel
from const import DATABASE_TYPE
import yaml
from dotenv import load_dotenv
import os
import logging.config


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
    host: str
    port: int

def get_config(databaseType: DATABASE_TYPE) -> DatabaseConfig:
    with open("config.yaml", "r") as f:
        config = yaml.safe_load(f)

    logging.config.dictConfig(config["logging_config"])

    match databaseType:
        case DATABASE_TYPE.SQLITE:
            return SQLiteConfig(**config["database"]["sqlite"])
        case DATABASE_TYPE.POSTGRESQL:
            load_dotenv()
            config = PostgresConfig(**config["database"]["postgres"])
            password = os.getenv(config.password)
            if password is None:
                raise ValueError("Password variable not added")
            config.password = password
            return config
        case DATABASE_TYPE.REDIS:
            return RedisConfig(**config["database"]["redis"])
        case _:
            raise ValueError(f"Unsupported Database type: {databaseType}")
