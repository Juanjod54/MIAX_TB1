from datetime import datetime


class Price:

    def __init__(self, time: datetime, open_value: float, close_value: float, high: float, low: float, volume: float):
        self.low = low
        self.time = time
        self.high = high
        self.volume = volume
        self.open = open_value
        self.close = close_value
