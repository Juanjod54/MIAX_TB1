from src.consumer.yahoo_consumer import YahooConsumer
from src.domain.consumable import Consumable
from src.domain.wallet import Wallet

consumer = YahooConsumer()
consumable_1 = Consumable("IBM", Consumable.period.ONE_YEAR, Consumable.interval.ONE_WEEK)
consumable_2 = Consumable("AAPL", Consumable.period.ONE_YEAR, Consumable.interval.ONE_WEEK)
consumable_3 = Consumable("IBEX", Consumable.period.ONE_YEAR, Consumable.interval.ONE_WEEK)
data_classes = consumer.consume([consumable_1, consumable_2, consumable_3])
data_classes[0].monte_carlo(80, 100, show=True)
wallet = Wallet()
wallet.add_data_classes(data_classes)
wallet.monte_carlo(100, 500, show=True)
wallet.monte_carlo(200, 1000, show=True, consumable=consumable_2)
