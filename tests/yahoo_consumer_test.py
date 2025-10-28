# Mini script to quickly test the AlphaVantageConsumer class
from src.consumer.yahoo_consumer import YahooConsumer
from src.domain.consumable import Consumable

# It is not safe to publish personal API Keys.
# To make it as PnP as possible, this API key is not associated to a real email or organization -> Not personal
consumer = YahooConsumer()
################################################################################################################
# Test API consumer with demo API URL
consumable_1 = Consumable("IBM", Consumable.period.INTRADAY, Consumable.interval.FIVE_MIN)
result_1 = consumer.consume([consumable_1])
