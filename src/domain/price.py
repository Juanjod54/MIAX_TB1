from datetime import datetime


class Price:

    def __init__(self, dt: datetime, open_value: float, close_value: float, close_value_adjusted: float, high: float,
                 low: float, volume: float):
        self.low = low
        self.high = high
        self.datetime = dt
        self.volume = volume
        self.open = open_value
        self.close = close_value
        self.close_adj = close_value_adjusted
        self.performance = ((close_value - open_value) / open_value) * 100
