from src.consumer.alpha_vantage_consumer import AlphaVantageConsumer
from src.consumer.yahoo_consumer import YahooConsumer
from src.domain.wallet import Wallet
from src.domain.consumable import Consumable

wallet = Wallet()
#consumer = AlphaVantageConsumer('TTFIK3GA2M9UCDXS')
consumer = YahooConsumer()
consumable_1 = Consumable("IBM", Consumable.period.INTRADAY, Consumable.interval.five_min)
#consumable_2 = Consumable("AAPL", Consumable.time_delta.INTRADAY, Consumable.interval.five_min)
data_classes = consumer.consume([consumable_1], async_request=True)
wallet.add_data_classes(data_classes)
wallet.report('wallet_report_test.md')