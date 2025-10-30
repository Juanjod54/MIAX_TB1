from src.domain.consumable import Consumable
from src.consumer.yahoo_consumer import YahooConsumer

consumer = YahooConsumer()
consumable_1 = Consumable("IBM", Consumable.period.ONE_YEAR, Consumable.interval.ONE_WEEK)
data_classes = consumer.consume([consumable_1])
for data_class in data_classes:
    data_class.monte_carlo(80, 100, show=True)