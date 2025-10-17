import requests
from enum import Enum
from requests import Response
from abc import ABC, abstractmethod
from src.domain.data_class import DataClass
from src.domain.consumable import Consumable
from concurrent.futures import ThreadPoolExecutor, as_completed


class Consumer(ABC):
    class methods(Enum):
        GET = 1
        POST = 2

    @abstractmethod
    def __process_raw_response__(self, consumable: Consumable, response: Response) -> DataClass:
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

    def __consume__(self, consumable: Consumable, params, method):
        url = self.__generate_api_url__(consumable)
        response = Consumer.__do_request__(url, params, method)
        return self.__process_raw_response__(consumable, response)

    def consume(self, consumables: list[Consumable], params=None, method: methods = methods.GET, async_request=False) -> \
            list[DataClass]:
        dataclasses = []

        if async_request:

            with ThreadPoolExecutor() as executor:
                futures = {executor.submit(self.__consume__,  ##
                                           consumable, params, method): consumable for consumable in consumables}
                for future in as_completed(futures):
                    consumable = futures[future]
                    try:
                        dataclasses.append(future.result())
                    except Exception as e:
                        print(f"There was an error while fetching consumable {consumable}: {e}")
        else:
            for consumable in consumables:
                dataclasses.append(self.__consume__(consumable, params, method))

        return dataclasses
