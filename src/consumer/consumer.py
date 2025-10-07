import requests
from enum import Enum
from requests import Response
from abc import ABC, abstractmethod
from src.domain.data_class import DataClass
from src.domain.consumable import Consumable


class Consumer(ABC):
    class methods(Enum):
        GET = 1
        POST = 2

    @abstractmethod
    def __process_raw_response__(self, name: str, response: Response) -> DataClass:
        pass

    @abstractmethod
    def __generate_api_url__(self, consumable: Consumable) -> str:
        pass

    @staticmethod
    def __do_request__(url: str, params: dict, method: methods) -> Response:
        if method == Consumer.methods.GET:
            return requests.get(url, params=params)
        elif method == Consumer.methods.POST:
            return requests.post(url, params=params)
        return None

    def consume(self, consumables: list[Consumable], params=None, method: methods = methods.GET, async_request=False) -> \
            list[DataClass]:
        dataclasses = []

        if async_request:
            raise Exception("Not implemented")
        else:
            for consumable in consumables:
                url = self.__generate_api_url__(consumable)
                response = Consumer.__do_request__(url, params, method)
                dataclasses.append(self.__process_raw_response__(consumable.symbol, response))

        return dataclasses
