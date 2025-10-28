from enum import Enum
import yfinance as yf
from requests import Response
from src.domain.price import Price
from src.consumer.consumer import Consumer
from src.domain.data_class import DataClass
from src.domain.consumable import Consumable
from src.exceptions.option_not_available_exception import OptionNotAvailableException
from src.util.util import Util


class YahooConsumer(Consumer):
    class __period__(Enum):
        INTRADAY = "1d"
        DAILY_ADJUSTED = "1d"
        TWO_DAYS = "2d"
        ONE_WEEK = "1wk"
        ONE_MONTH = "1mo"
        THREE_MONTHS = "3mo"
        SIX_MONTHS = "6mo"
        ONE_YEAR = "1y"

    class __interval__(Enum):
        ONE_MIN = "1m"
        TWO_MIN = "2m"
        FIVE_MIN = "5m"
        FIFTEEN_MIN = "15m"
        THIRTY_MIN = "30m"
        SIXTY_MIN = "60m"
        NINETY_MIN = "90m"
        ONE_DAY = "1d"
        FIVE_DAYS = "5d"
        ONE_WEEK = "1wk"
        ONE_MONTH = "1mo"
        THREE_MONTHS = "3mo"

    def __init__(self):
        super().__init__()

    def __process_raw_response__(self, consumable: Consumable, response: Response) -> DataClass:
        """
        Abstract method to process the raw response from an API call
        :param consumable: The consumable to process
        :param response: The raw response from the API call
        :return: An object containing the result data in a normalized DataClass object
        """
        pass

    def __generate_api_url__(self, consumable: Consumable) -> str:
        """
        Abstract method to generate the 'to-call' API url from a consumable
        :param consumable: The consumable to process
        :return: The API url
        """
        pass

    # @OVERRIDE
    def __consume__(self, consumable: Consumable, params, method) -> DataClass:
        """
        METHOD OVERRIDES PARENT CLASS __consume__
        Method to consume the consumable. This method calls abstract methods implemented in the end consumer so it
        can be generic
        :param consumable: The consumable to process
        :param params: The parameters to pass to the API call
        :param method: The method to use (POST or GET)
        :return: The processed response from the API call, as a DataClass object
        """

        data_class = DataClass(consumable, self.__str__())

        if consumable.interval.name not in YahooConsumer.__interval__.__members__:
            raise OptionNotAvailableException(consumable.interval.name)
        if consumable.period.name not in YahooConsumer.__period__.__members__:
            raise OptionNotAvailableException(consumable.interval.name)

        ticker = consumable.symbol
        period = YahooConsumer.__period__[consumable.period.name]
        interval = YahooConsumer.__interval__[consumable.interval.name]

        prices = []
        data = yf.download(ticker, period=period.value, interval=interval.value, progress=False, auto_adjust=False)
        # Normalize column names
        data.columns = [col[0].lower().replace(' ', '_') for col in data.columns.to_flat_index()]
        # May seem redundant, but standardizes data:
        for row in data.itertuples(name='Price'):
            close_adj = row.adj_close if 'adj_close' in data.columns else row.close
            utc_dt = Util.to_utc(row.Index.to_pydatetime())
            prices.append(Price(utc_dt, row.open, row.close, close_adj, row.high, row.low, row.volume))

        data_class.add_prices(prices)
        return data_class


