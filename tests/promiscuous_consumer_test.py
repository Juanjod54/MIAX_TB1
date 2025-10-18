# Mini script to quickly test the promiscuous consume call
from src.consumer.alpha_vantage_consumer import AlphaVantageConsumer
from src.consumer.consumer import Consumer
from src.domain.consumable import Consumable

# It is not safe to publish personal API Keys.
# To make it as PnP as possible, this API key is not associated to a real email or organization -> Not personal
consumer_1 = AlphaVantageConsumer("TTFIK3GA2M9UCDXS")
consumer_2 = AlphaVantageConsumer("TTFIK3GA2M9UCDXS")
################################################################################################################
consumable_1 = Consumable("IBM", Consumable.time_delta.INTRADAY, Consumable.interval.five_min)
consumable_2 = Consumable("AAPL", Consumable.time_delta.INTRADAY, Consumable.interval.five_min)
results = Consumer.promiscuous_consume([consumer_1, consumer_2], [consumable_1, consumable_1])
print(results)