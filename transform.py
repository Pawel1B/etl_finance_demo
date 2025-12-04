from const import DataDownloadSource, DatabaseType
from src.DataDownloader import DataDownloader
from src.DataTransformer import DataTransformer
from src.DataStorage import DataStorage

def download_transform_load(ticker: str, source: DataDownloadSource) -> None:
    download = DataDownloader(source)
    data = download.get_single_stock(ticker)
    transform = DataTransformer()
    df = transform.get_dataframe(data)
    df = transform.clean_dataframe(df)
    storage = DataStorage(DatabaseType.SQLITE)
    storage.save_to_sql(df, ticker)

if __name__ == "__main__":
    download_transform_load(ticker="cla", source=DataDownloadSource.STOOQ_PL)
