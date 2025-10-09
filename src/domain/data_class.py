from src.domain.price import Price


class DataClass:

    def __init__(self, name: str):
        self.name = name
        self.prices = []
        self.max = 0
        self.min = 0
        self.std = 0
        self.mean = 0
        self.variance = 0

    # Adding prices in batches reduces the number of times the statistics properties need to be measured
    def add_prices(self, prices: list[Price]):
        self.prices.extend(prices)
        # Todo calculate the values