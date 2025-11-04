import os
import uuid

from fastapi import FastAPI, BackgroundTasks
from fastapi.responses import FileResponse

from src.consumer.alpha_vantage_consumer import AlphaVantageConsumer
from src.consumer.consumer import Consumer
from src.consumer.yahoo_consumer import YahooConsumer
from src.domain.consumable import Consumable
from src.domain.wallet import Wallet

app = FastAPI()


def get_consumer(consumer: str, api_key: None) -> Consumer | None:
    if consumer == 'alpha':
        return AlphaVantageConsumer(api_key)
    elif consumer == 'yahoo':
        return YahooConsumer()


@app.get("/")
def index():
    path = os.path.join("src/resources/index.html")
    return FileResponse(path)


@app.post("/api/data")
async def consume(data: dict, background_tasks: BackgroundTasks):
    consumers = {}
    to_consume = {}
    consumables = []
    is_async = data['async']
    is_promiscuous = data['promiscuous']
    request_consumables = data["consumables"]
    for request_consumable in request_consumables:
        consumer_name = request_consumable['source']
        api_key = request_consumable['api_key'] if "api_key" in request_consumable else None
        if consumer_name not in consumers:
            to_consume[consumer_name] = []
            consumers[consumer_name] = get_consumer(consumer_name, api_key)
        data_type = Consumable.data_type(request_consumable['data_format'])
        interval = Consumable.interval(request_consumable["interval"])
        period = Consumable.period(request_consumable["period"])
        symbol = request_consumable["symbol"]

        consumable = Consumable(symbol, period, interval, data_type=data_type)
        to_consume[consumer_name].append(consumable)
        consumables.append(consumable)

    dataclasses = []

    if is_promiscuous:
        dataclasses = Consumer.promiscuous_consume(list(consumers.values()), consumables)
    else:
        for consumer_name in to_consume:
            consumer = consumers[consumer_name]
            dataclasses.extend(consumer.consume(to_consume[consumer_name], async_request=is_async))

    wallet = Wallet()
    wallet.add_data_classes(dataclasses)
    random_report_name = f'output/{str(uuid.uuid4())}.md'
    wallet.report(output_filename=random_report_name, steps=100, simulations=100)

    background_tasks.add_task(os.remove, random_report_name)

    return FileResponse(random_report_name, media_type="text/markdown")
