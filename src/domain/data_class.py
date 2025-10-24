import base64
import io

import pandas as pd
from enum import Enum
from datetime import date
import matplotlib.pyplot as plt
from src.domain.plot import Plot
from src.domain.price import Price
from src.exceptions.option_not_available_exception import OptionNotAvailableException


class DataClass:
    class Field(Enum):
        OPEN = 1
        CLOSE = 2
        HIGH = 3
        LOW = 4
        VOLUME = 5,
        DATE = 6

    def __init__(self, name: str, source: str):
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
        prices_columns = {'open': [], 'close': [], 'high': [], 'low': [], 'volume': [], 'date': []}
        for price in prices:
            prices_columns['open'].append(price.open)
            prices_columns['close'].append(price.close)
            prices_columns['high'].append(price.high)
            prices_columns['low'].append(price.low)
            prices_columns['volume'].append(price.volume)
            prices_columns['date'].append(price.datetime)

        self.prices = pd.concat([self.prices, pd.DataFrame(prices_columns, index=prices_columns['date'])])

    def create_plot(self, field: Field | None, show: bool = False) -> Plot:
        plt.figure(figsize=(10, 5))
        if field is None:
            plt.plot(self.__get_data__(DataClass.Field.DATE), self.__get_data__(DataClass.Field.OPEN), label="Open",
                     color="red")
            plt.plot(self.__get_data__(DataClass.Field.DATE), self.__get_data__(DataClass.Field.CLOSE), label="Close",
                     color="green")
            plt.plot(self.__get_data__(DataClass.Field.DATE), self.__get_data__(DataClass.Field.HIGH), label="High",
                     color="orange")
            plt.plot(self.__get_data__(DataClass.Field.DATE), self.__get_data__(DataClass.Field.CLOSE), label="Low",
                     color="blue")
            plt.title(f"{self.name} Prices Evolution")
            plt.ylabel("Price")
        else:
            field_name = field.name.title()
            plt.plot(self.__get_data__(DataClass.Field.DATE), self.__get_data__(field), label=field_name, linestyle="--", marker="o")
            if field == DataClass.Field.VOLUME:
                plt.ylabel("Volume")
                plt.title(f"{field_name} Evolution")
            else:
                plt.ylabel("Price")
                plt.title(f"{field_name} Price Evolution")

        plt.xlabel("Date")
        plt.grid(True)
        plt.legend()

        if show:
            plt.show()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        img_bytes = base64.b64encode(buffer.read()).decode('utf-8')
        buffer.close()
        plt.close()

        return Plot(img_bytes)

    def plots_report(self, show: bool = False) -> dict:
        plots = {}
        for field in DataClass.Field:
            if field != DataClass.Field.DATE:
                plots[field] = self.create_plot(field, show)

        # Create a plot with all prices in one place for quick comparison
        plots[None] = self.create_plot(None, show)
        return plots
