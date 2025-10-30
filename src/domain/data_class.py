import io
import copy
import math
import base64
import random
import datetime

import numpy as np
import pandas as pd
from enum import Enum
from pandas import DataFrame
import matplotlib.pyplot as plt
from src.domain.plot import Plot
from src.domain.price import Price
from src.domain.consumable import Consumable


class DataClass:
    class Field(Enum):
        OPEN = 1
        CLOSE = 2
        HIGH = 3
        LOW = 4
        VOLUME = 5,
        DATE = 6
        PERFORMANCE = 7
        RETURNS = 8

        def unit(self):
            if self == DataClass.Field.PERFORMANCE or self == DataClass.Field.RETURNS:
                return "%"
            elif self == DataClass.Field.VOLUME:
                return ""
            return "$"

    def __init__(self, consumable: Consumable, source: str):
        self.source = source
        self.prices = pd.DataFrame()
        self.name = consumable.symbol
        self.period = consumable.period
        self.interval = consumable.interval

    def __get_data__(self, field: Field):
        if field == DataClass.Field.OPEN:
            return self.prices['open']
        elif field == DataClass.Field.CLOSE:
            return self.prices['close_adj']
        elif field == DataClass.Field.HIGH:
            return self.prices['high']
        elif field == DataClass.Field.LOW:
            return self.prices['low']
        elif field == DataClass.Field.VOLUME:
            return self.prices['volume']
        elif field == DataClass.Field.DATE:
            return self.prices.index
        elif field == DataClass.Field.PERFORMANCE:
            return self.prices['performance']
        elif field == DataClass.Field.RETURNS:
            return self.prices['returns']

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

    def volatility(self):
        data = self.__get_data__(DataClass.Field.RETURNS)
        return data.std()

    def monte_carlo(self, steps: int, n_simulations: int, show: bool = False) -> DataFrame:
        returns = self.__get_data__(DataClass.Field.RETURNS)
        mu = returns.mean()/100
        sigma = returns.std()/100
        s0 = self.__get_data__(DataClass.Field.CLOSE).iloc[-1]
        last_date = self.__get_data__(DataClass.Field.DATE).max().to_pydatetime()

        dt = 1  # Dt is always one since we are gonna use the data class interval to simulate "steps" steps
        df = pd.DataFrame(0,  #
                          columns=[f"Sim_{i + 1}" for i in range(n_simulations)],  #
                          index=[(last_date + self.interval.timedelta(s)) for s in range(steps)])

        for i in range(n_simulations):
            _s0 = s0
            prices = []
            randoms = np.random.uniform(-1, 1, size=steps)
            for s in range(steps):
                z = randoms[s]
                _s0 = _s0 * math.e ** ((mu - 0.5 * sigma ** 2) * dt + sigma * math.sqrt(dt) * z)
                prices.append(_s0)
            df[f"Sim_{i + 1}"] = prices

        if show:
            series = []
            for i in range(n_simulations):
                simulation_label = f"Sim_{i + 1}"
                series.append({  #
                    'x': df.index,  #
                    'y': df[simulation_label],  #
                    'linestyle': '--'  #
                })
            DataClass.__plot_field__('Monte Carlo Simulation', series, ylabel='Price', show=True)

        return df

    # Adding prices in batches reduces the number of times the statistics properties need to be measured
    def add_prices(self, prices: list[Price]):
        dates = []
        prices_columns = {'open': [], 'close': [], 'close_adj': [], 'high': [], 'low': [], 'volume': [],
                          'performance': []}
        for price in prices:
            dates.append(price.datetime)
            prices_columns['low'].append(price.low)
            prices_columns['open'].append(price.open)
            prices_columns['high'].append(price.high)
            prices_columns['close'].append(price.close)
            prices_columns['volume'].append(price.volume)
            prices_columns['close_adj'].append(price.close_adj)
            prices_columns['performance'].append(price.performance)

        prices_df = pd.DataFrame(prices_columns, index=dates)
        self.prices = pd.concat([self.prices, prices_df])
        # Get the returns
        self.prices['returns'] = self.prices['close_adj'].pct_change().apply(lambda r: r * 100)
        self.__clean_prices__()

    def __clean_prices__(self):
        self.prices.dropna(inplace=True)

    def create_plot(self, field: Field | None, show: bool = False) -> Plot:
        if field is None:
            title = f"{self.name} Prices Evolution"
            fields = [DataClass.Field.OPEN, DataClass.Field.CLOSE, DataClass.Field.HIGH, DataClass.Field.LOW]
        else:
            fields = [field]
            title = f"{field.name.title()} Evolution"

        return DataClass.plot_field(title, [self], fields, "Prices", linestyle='--', show=show)

    def plots_report(self, show: bool = False) -> dict:
        plots = {}
        for field in DataClass.Field:
            if field != DataClass.Field.DATE:
                plots[field] = self.create_plot(field, show)

        # Create a plot with all prices in one place for quick comparison
        plots[None] = self.create_plot(None, show)
        return plots

    def resample(self, to_interval: Consumable.interval) -> 'DataClass':
        new_data_class = copy.copy(self)
        if to_interval <= self.interval:
            new_data_class.prices = new_data_class.prices.resample(to_interval.resample_value()).ffill()
        else:
            new_data_class.prices = new_data_class.prices.resample(to_interval.resample_value()).agg({
                'open': 'first',
                'high': 'max',
                'low': 'min',
                'close': 'last',
                'volume': 'sum'
            })
        new_data_class.__clean_prices__()
        return new_data_class

    @staticmethod
    def plot_field(title: str, data_classes: list['DataClass'], fields: list[Field], ylabel: str, linestyle: str = None,
                   show: bool = False):
        series = []
        for data_class in data_classes:
            for field in fields:
                label = f"{data_class.name}: {field.name} ({field.unit()})"
                series.append({  #
                    'x': data_class.__get_data__(DataClass.Field.DATE),  #
                    'y': data_class.__get_data__(field),  #
                    'linestyle': linestyle,  #
                    'label': label  #
                })

        return DataClass.__plot_field__(title, series, ylabel, show=show)

    @staticmethod
    def __plot_field__(title: str, series: list[any], ylabel: str, show: bool = False) -> Plot:

        for serie in series:
            x = serie['x']
            y = serie['y']
            linestyle = serie['linestyle']
            label = serie['label'] if 'label' in serie else None
            marker = serie['marker'] if 'marker' in serie else None
            plt.plot(x, y, linestyle=linestyle, marker=marker, label=label)

        plt.xticks(rotation=45)
        plt.xlabel("Date")
        plt.ylabel(ylabel)
        plt.title(title)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()

        if show:
            plt.show()

        buffer = io.BytesIO()
        plt.savefig(buffer, format='png')
        buffer.seek(0)

        img_bytes = base64.b64encode(buffer.read()).decode('utf-8')
        buffer.close()
        plt.close()

        return Plot(img_bytes)
