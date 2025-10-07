from enum import Enum
from requests import Response
from src.consumer.consumer import Consumer
from src.domain.data_class import DataClass
from src.domain.consumable import Consumable


class AlphaVantageConsumer(Consumer):
    API_URL = "https://www.alphavantage.co/query?function={timedelta}&symbol={symbol}&interval={interval}&apikey={key}"

    class __timedelta__(Enum):
        INTRADAY = "TIME_SERIES_INTRADAY"
        DAILY = "TIME_SERIES_DAILY"
        WEEKLY = "TIME_SERIES_WEEKLY"
        MONTHLY = "TIME_SERIES_MONTHLY"

    class __interval__(Enum):
        one_min = "1min"
        five_min = "5min"
        fifteen_min = "15min"
        thirty_min = "30min"
        sixty_min = "60min"

    def __init__(self, api_key):
        self.api_key = api_key

    def __process_raw_response__(self, name: str, response: Response) -> DataClass:
        if response is None:
            pass

        response_obj = response.json()
        return DataClass(name)

    def __generate_api_url__(self, consumable: Consumable) -> str:
        timedelta = AlphaVantageConsumer.__timedelta__[consumable.timedelta.name].value
        interval = AlphaVantageConsumer.__interval__[consumable.interval.name].value
        return self.API_URL.format(symbol=consumable.symbol, timedelta=timedelta, interval=interval, key=self.api_key)
