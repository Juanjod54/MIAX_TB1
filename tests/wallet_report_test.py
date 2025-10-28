from src.consumer.alpha_vantage_consumer import AlphaVantageConsumer
from src.consumer.yahoo_consumer import YahooConsumer
from src.domain.wallet import Wallet
from src.domain.consumable import Consumable

wallet = Wallet()
#consumer = AlphaVantageConsumer('TTFIK3GA2M9UCDXS')
consumer = YahooConsumer()
consumable_1 = Consumable("IBM", Consumable.period.ONE_YEAR, Consumable.interval.ONE_WEEK)
consumable_2 = Consumable("IBEX", Consumable.period.ONE_YEAR, Consumable.interval.ONE_WEEK)
consumable_3 = Consumable("NVDA", Consumable.period.THREE_MONTHS, Consumable.interval.ONE_DAY)
data_classes = consumer.consume([consumable_1, consumable_2, consumable_3])
wallet.add_data_classes(data_classes)
wallet.report('wallet_report_test.md')