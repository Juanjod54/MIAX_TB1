# Mini script to quickly test the AlphaVantageConsumer class
from src.consumer.alpha_vantage_consumer import AlphaVantageConsumer
from src.domain.consumable import Consumable

consumer = AlphaVantageConsumer("demo")
################################################################################################################
# Test API consumer with demo API URL:
# https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo
consumable_1 = Consumable("IBM", Consumable.timedelta.INTRADAY, Consumable.interval.five_min)
result_1 = consumer.consume([consumable_1])
################################################################################################################
# Test API consumer with demo API URL:
# https://www.alphavantage.co/query?function=TIME_SERIES_INTRADAY&symbol=IBM&interval=5min&apikey=demo
consumable_2 = Consumable("IBM", Consumable.timedelta.INTRADAY, Consumable.interval.five_min)
consumable_3 = Consumable("IBM", Consumable.timedelta.INTRADAY, Consumable.interval.five_min)
result_2 = consumer.consume([consumable_1, consumable_2, consumable_3], async_request=True)