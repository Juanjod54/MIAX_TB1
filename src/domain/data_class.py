import pandas as pd
from enum import Enum
import matplotlib.pyplot as plt
from src.domain.price import Price


class DataClass:

    class Field(Enum):
        OPEN = 1
        CLOSE = 2
        HIGH = 3
        LOW = 4
        VOLUME = 5,
        DATE = 6

    def __init__(self, source: str, name: str):
        self.name = name
        self.source = source
        self.prices = pd.DataFrame()

    def __get_data__(self, field: Field):
        if field == DataClass.Field.OPEN:
            return self.prices['open']
        elif field == DataClass.Field.CLOSE:
            return self.prices['close']
        elif field == DataClass.Field.HIGH:
            return self.prices['high']
        elif field == DataClass.Field.LOW:
            return self.prices['low']
        elif field == DataClass.Field.VOLUME:
            return self.prices['volume']
        elif field == DataClass.Field.DATE:
            return self.prices['date']

        raise NotImplementedError(f"Field {field} not implemented")

    def min(self, field: Field):
        data = self.__get_data__(field)
        return data.min()

    def max(self, field: Field):
        data = self.__get_data__(field)
        return data.max()

    def mean(self, field: Field):
        data = self.__get_data__(field)
        return data.mean()

    def std(self, field: Field):
        data = self.__get_data__(field)
        return data.std()

    def monte_carlo(self, field: Field):
        np_array = self.__get_data__(field)


    # Adding prices in batches reduces the number of times the statistics properties need to be measured
    def add_prices(self, prices: list[Price]):
        prices_columns = { 'open': [], 'close': [], 'high': [], 'low': [], 'volume': [], 'date': [] }
        for price in prices:
            prices_columns['open'].append(price.open)
            prices_columns['close'].append(price.close)
            prices_columns['high'].append(price.high)
            prices_columns['low'].append(price.low)
            prices_columns['volume'].append(price.volume)
            prices_columns['date'].append(price.datetime)

        self.prices = pd.concat([self.prices, pd.DataFrame(prices_columns, index=prices_columns['date'])])

    def plot(self, field: Field):
        plt.figure(figsize=(10, 5))
        if field == DataClass.Field.CLOSE:
            plt.plot(self.__get_data__(DataClass.Field.DATE), self.__get_data__(DataClass.Field.CLOSE), label="Close",
                     linestyle="--", marker="o")
            # plt.plot(df["date"], df["close"], label="Close", linestyle="-", marker="x")
            plt.title("Close Price Evolution")
            plt.ylabel("Price")
            plt.xlabel("Date")

        plt.legend()
        plt.show()

    def plots_report(self):
        plots = []
        for field in DataClass.Field:
            plots.append(self.plot(field))
        return plots
