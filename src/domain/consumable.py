import datetime
from enum import Enum


class Consumable:
    class period(Enum):
        INTRADAY = 1
        DAILY = 2
        TWO_DAYS = 3
        ONE_WEEK = 4
        ONE_MONTH = 5
        THREE_MONTHS = 6
        SIX_MONTHS = 7
        ONE_YEAR = 8

    class interval(Enum):
        ONE_MIN = 1
        FIVE_MIN = 2
        FIFTEEN_MIN = 3
        THIRTY_MIN = 4
        SIXTY_MIN = 5
        NINETY_MIN = 6
        ONE_DAY = 7
        FIVE_DAYS = 8
        ONE_WEEK = 9
        ONE_MONTH = 10
        THREE_MONTHS = 11

        def resample_value(self) -> str:
            if self == Consumable.interval.ONE_MIN:
                return '1min'
            elif self == Consumable.interval.FIVE_MIN:
                return '5min'
            elif self == Consumable.interval.FIFTEEN_MIN:
                return '15min'
            elif self == Consumable.interval.THIRTY_MIN:
                return '30min'
            elif self == Consumable.interval.SIXTY_MIN:
                return '60min'
            elif self == Consumable.interval.NINETY_MIN:
                return '90min'
            elif self == Consumable.interval.ONE_DAY:
                return '1D'
            elif self == Consumable.interval.FIVE_DAYS:
                return '5D'
            elif self == Consumable.interval.ONE_WEEK:
                return '1W'
            elif self == Consumable.interval.ONE_MONTH:
                return '1M'
            elif self == Consumable.interval.THREE_MONTHS:
                return '3M'

            return self.value.__str__()

        def timedelta(self, n):
            if self.value < Consumable.interval.ONE_DAY.value:
                return datetime.timedelta(minutes=n)
            elif self.value < Consumable.interval.ONE_WEEK.value:
                return datetime.timedelta(days=n)
            elif self.value < Consumable.interval.ONE_MONTH.value:
                return datetime.timedelta(weeks=n)
            else:
                return datetime.timedelta(days=n*30)

    class data_type(Enum):
        CSV = "csv"
        JSON = "json"

    def __init__(self, symbol: str, period: period, interval: interval, data_type: data_type=data_type.JSON):
        self.symbol = symbol
        self.interval = interval
        self.data_type = data_type
        self.period = period
