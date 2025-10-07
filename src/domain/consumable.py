from enum import Enum


class Consumable:
    class timedelta(Enum):
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

    def __init__(self, symbol: str, timedelta: timedelta, interval: interval):
        self.symbol = symbol
        self.timedelta = timedelta
        self.interval = interval
