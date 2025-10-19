from enum import Enum


class Consumable:
    class period(Enum):
        INTRADAY = 1
        TWO_DAYS = 2
        ONE_WEEK = 3
        ONE_MONTH = 4
        THREE_MONTHS = 5
        SIX_MONTHS = 6
        ONE_YEAR = 7

    class interval(Enum):
        one_min = 1
        five_min = 2
        fifteen_min = 3
        thirty_min = 4
        sixty_min = 5
        ninety_min = 6
        one_day = 7
        five_days = 8
        one_week = 9
        one_month = 10
        three_months = 11

    class data_type(Enum):
        CSV = "csv"
        JSON = "json"

    def __init__(self, symbol: str, period: period, interval: interval, data_type: data_type=data_type.JSON):
        self.symbol = symbol
        self.interval = interval
        self.data_type = data_type
        self.period = period
