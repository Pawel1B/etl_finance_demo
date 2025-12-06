import requests
from const import DATA_DOWNLOAD_SOURCE
from http import HTTPStatus
import logging
logging.basicConfig(level=logging.INFO)


class DataDownloader:


    def __init__(self, source: DATA_DOWNLOAD_SOURCE) -> None:
        self.dataDownloadSource = source

    def get_single_stock(self, stock_name: str) -> str:
        if self.dataDownloadSource == DATA_DOWNLOAD_SOURCE.STOOQ_PL:
            url = f"https://stooq.pl/q/d/l/?s={stock_name}&i=d"
            response = requests.get(url)
            if response.status_code == HTTPStatus.OK:
                logging.info(f"Stock returned {stock_name}")

                return response.text
            else:
                raise RuntimeError(
                    f"There is an issue with request, check status of service or ticker: {stock_name}")
        else:
            raise ValueError(f"Mentioned data download resource not supported: {self.dataDownloadSource}")
