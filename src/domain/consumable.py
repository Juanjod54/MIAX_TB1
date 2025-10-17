from enum import Enum


class Consumable:
    class time_delta(Enum):
        INTRADAY = 1
        DAILY = 2
        WEEKLY = 3
        MONTHLY = 4

    class interval(Enum):
        one_min = 1
        five_min = 2
        fifteen_min = 3
        thirty_min = 4
        sixty_min = 5

    class data_type(Enum):
        CSV = "csv"
        JSON = "json"

    def __init__(self, symbol: str, time_delta: time_delta, interval: interval, data_type: data_type=data_type.JSON):
        self.symbol = symbol
        self.interval = interval
        self.data_type = data_type
        self.time_delta = time_delta
