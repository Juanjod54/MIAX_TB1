from enum import Enum
from requests import Response
from src.domain.price import Price
from src.exceptions.option_not_available_exception import OptionNotAvailableException
from src.util.util import Util
from src.consumer.consumer import Consumer
from src.domain.data_class import DataClass
from src.domain.consumable import Consumable
from src.exceptions.incompatible_data_type_exception import IncompatibleDataTypeException


class AlphaVantageConsumer(Consumer):
    # Keys
    LOW_KEY = 'low'
    HIGH_KEY = 'high'
    OPEN_KEY = 'open'
    CLOSE_KEY = 'close'
    VOLUME_KEY = 'volume'
    TIMESTAMP_KEY = 'timestamp'
    META_DATA_KEY = 'Meta Data'
    TIME_ZONE_KEY = 'Time Zone'
    CLOSE_KEY_ADJUSTED = 'close'
    # Keys regex
    DEFAULT_KEY_REGEX = "\\d+\\.\\ (.+)"
    # Date patterns
    DEFAULT_DATE_PATTERN = '%Y-%m-%d %H:%M:%S'
    # API URL
    API_URL = "https://www.alphavantage.co/query?function={period}&symbol={symbol}&interval={interval}&datatype={data_type}&apikey={key}"

    class __period__(Enum):
        INTRADAY = "TIME_SERIES_INTRADAY"
        DAILY = "TIME_SERIES_DAILY_ADJUSTED"
        ONE_WEEK = "TIME_SERIES_WEEKLY_ADJUSTED"
        ONE_MONTH = "TIME_SERIES_MONTHLY_ADJUSTED"

    class __interval__(Enum):
        ONE_MIN = "1min"
        FIVE_MIN = "5min"
        FIFTEEN_MIN = "15min"
        THIRTY_MIN = "30min"
        SIXTY_MIN = "60min"

    def __init__(self, api_key, params=None, method: Consumer.methods = Consumer.methods.GET):
        super().__init__(params, method)
        self.api_key = api_key

    def __parse_json_response__(self, consumable: Consumable, response: Response) -> DataClass:
        # Create the return object
        dataclass = DataClass(consumable, self.__str__())
        json_response = Util.transform_keys(response.json(), AlphaVantageConsumer.DEFAULT_KEY_REGEX)
        if json_response:

            # Get the metadata to remove it from the dict and to get the date's timezone (UTC defaulted)
            md = json_response.pop(self.META_DATA_KEY)
            timezone = md[self.TIME_ZONE_KEY]

            # Get the prices information
            prices = []
            prices_info = next(iter(json_response.values()), {})
            for date_key in prices_info:
                tz_dt = Util.from_str(date_key, self.DEFAULT_DATE_PATTERN, timezone=timezone)
                utc_dt = Util.to_utc(tz_dt)
                price_info = prices_info[date_key]
                prices.append(
                    Price(utc_dt,
                          float(price_info[self.OPEN_KEY]),
                          float(price_info[self.CLOSE_KEY]),
                          float(price_info[self.CLOSE_KEY_ADJUSTED]),
                          float(price_info[self.HIGH_KEY]),
                          float(price_info[self.LOW_KEY]),
                          float(price_info[self.VOLUME_KEY]))
                )

            dataclass.add_prices(prices)

        return dataclass

    def __parse_csv_response__(self, consumable: Consumable, response: Response) -> DataClass:
        dataclass = DataClass(consumable, self.__str__())
        csv_response = response.content.decode("utf-8")

        # The CSV Output DOES NOT have the timezone metadata. We could get it by function = SYMBOL_SEARCH

        if csv_response:
            csv_rows = csv_response.split("\r\n")
            csv_headers = csv_rows.pop(0)
            headers_positions = {}

            # Dynamically get each header position
            for idx, header in enumerate(csv_headers.split(",")):
                headers_positions[header] = idx

            prices = []
            for i in range(1, len(csv_rows) - 1):
                price_info = csv_rows[i].split(",")
                dt = Util.from_str(price_info[headers_positions[self.TIMESTAMP_KEY]], self.DEFAULT_DATE_PATTERN)
                open_value = float(price_info[headers_positions[self.OPEN_KEY]])
                close_value = float(price_info[headers_positions[self.CLOSE_KEY]])
                close_value_adj = float(price_info[headers_positions[self.CLOSE_KEY_ADJUSTED]])
                high_value = float(price_info[headers_positions[self.HIGH_KEY]])
                low_value = float(price_info[headers_positions[self.LOW_KEY]])
                volume_value = float(price_info[headers_positions[self.VOLUME_KEY]])
                prices.append(Price(dt, open_value, close_value, close_value_adj, high_value, low_value, volume_value))

        return dataclass

    def __process_raw_response__(self, consumable: Consumable, response: Response) -> DataClass:
        if response.status_code != 200:
            raise Exception(response.text)

        data_type = consumable.data_type

        if data_type == Consumable.data_type.JSON:
            return self.__parse_json_response__(consumable, response)
        elif data_type == Consumable.data_type.CSV:
            return self.__parse_csv_response__(consumable, response)

        raise IncompatibleDataTypeException(data_type.value)

    def __generate_api_url__(self, consumable: Consumable) -> str:
        if consumable.interval.name not in AlphaVantageConsumer.__interval__.__members__:
            raise OptionNotAvailableException(consumable.interval.name)
        if consumable.period.name not in AlphaVantageConsumer.__period__.__members__:
            raise OptionNotAvailableException(consumable.interval.name)

        period = AlphaVantageConsumer.__period__[consumable.period.name]
        interval = AlphaVantageConsumer.__interval__[consumable.interval.name]
        data_type = consumable.data_type

        if not (data_type == Consumable.data_type.JSON or data_type == Consumable.data_type.CSV):
            raise IncompatibleDataTypeException(data_type.value)

        return self.API_URL.format(symbol=consumable.symbol,
                                   period=period.value,  ##
                                   interval=interval.value,  ##
                                   data_type=data_type.value,  ##
                                   key=self.api_key)
