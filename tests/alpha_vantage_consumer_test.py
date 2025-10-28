# Mini script to quickly test the AlphaVantageConsumer class
from src.consumer.alpha_vantage_consumer import AlphaVantageConsumer
from src.domain.consumable import Consumable

# It is not safe to publish personal API Keys.
# To make it as PnP as possible, this API key is not associated to a real email or organization -> Not personal
consumer = AlphaVantageConsumer("TTFIK3GA2M9UCDXS")
################################################################################################################
# Test API consumer with demo API URL
consumable_1 = Consumable("IBM", Consumable.period.INTRADAY, Consumable.interval.FIVE_MIN)
result_1 = consumer.consume([consumable_1])
################################################################################################################
# Test API consumer with demo API URL in parallel
consumable_2 = Consumable("IBM", Consumable.period.INTRADAY, Consumable.interval.FIVE_MIN)
consumable_3 = Consumable("IBM", Consumable.period.INTRADAY, Consumable.interval.FIVE_MIN)
result_2 = consumer.consume([consumable_1, consumable_2, consumable_3], async_request=True)
# Test API consumer with demo API URL in CSV
consumable_4 = Consumable("IBM", Consumable.period.INTRADAY, Consumable.interval.FIVE_MIN,
                          data_type=Consumable.data_type.CSV)
result_3 = consumer.consume([consumable_4])
