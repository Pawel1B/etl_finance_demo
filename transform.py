from const import DATA_DOWNLOAD_SOURCE, DATABASE_TYPE
from src.DataDownloader import DataDownloader
from src.DataTransformer import DataTransformer
from src.storage.storage_factory import get_storage

def download_transform_load(ticker: str, source: DATA_DOWNLOAD_SOURCE, databaseType: DATABASE_TYPE) -> None:
    download = DataDownloader(source)
    data = download.get_single_stock(ticker)
    transform = DataTransformer()
    df = transform.get_dataframe(data)
    df = transform.clean_dataframe(df)
    storage_inst = get_storage(databaseType)
    storage_inst.data_save(ticker, df)

if __name__ == "__main__":
    download_transform_load(ticker="cla", source=DATA_DOWNLOAD_SOURCE.STOOQ_PL, databaseType = DATABASE_TYPE.SQLITE)
