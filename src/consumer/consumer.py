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
        """
        Abstract method to process the raw response from an API call
        :param consumable: The consumable to process
        :param response: The raw response from the API call
        :return: An object containing the result data in a normalized DataClass object
        """
        pass

    @abstractmethod
    def __generate_api_url__(self, consumable: Consumable) -> str:
        """
        Abstract method to generate the 'to-call' API url from a consumable
        :param consumable: The consumable to process
        :return: The API url
        """
        pass

    @staticmethod
    def __do_request__(url: str, params: dict, method: methods) -> Response | None:
        """
        Abstract method to do the actual request
        :param url: The API url
        :param params: The parameters to pass to the API call
        :param method: The method to use (POST or GET)
        :return: The response from the API call. None if method is neither POST nor GET
        """
        if method == Consumer.methods.GET:
            return requests.get(url, params=params)
        elif method == Consumer.methods.POST:
            return requests.post(url, params=params)
        return None

    def __init__(self, params=None, method: methods = methods.GET):
        self.params = params
        self.method = method

    def __str__(self):
        return self.__class__.__name__

    def __consume__(self, consumable: Consumable, params, method) -> DataClass:
        """
        Method to consume the consumable. This method calls abstract methods implemented in the end consumer so it
        can be generic
        :param consumable: The consumable to process
        :param params: The parameters to pass to the API call
        :param method: The method to use (POST or GET)
        :return: The processed response from the API call, as a DataClass object
        """
        url = self.__generate_api_url__(consumable)
        response = Consumer.__do_request__(url, params, method)
        return self.__process_raw_response__(consumable, response)

    @staticmethod
    def promiscuous_consume(consumers: list["Consumer"], consumables: list[Consumable]) -> list[DataClass]:
        """
        Static and asynchronous method to consume all the consumables in a list with each given consumer
        :param consumers: The consumers to consume with
        :param consumables: The consumables to consume
        :return: A list of DataClass objects, merge of each consumer's consume result
        """
        dataclasses = []

        with ThreadPoolExecutor() as executor:
            futures = {executor.submit(consumer.consume, consumables, True): consumer for consumer in consumers}
            for future in as_completed(futures):
                consumer_future = futures[future]
                try:
                    dataclasses.extend(future.result())
                except Exception as e:
                    print(f"There was an error while consuming with {consumer_future}: {e}")

        return dataclasses

    def consume(self, consumables: list[Consumable], async_request=False) -> \
            list[DataClass]:
        """
        Method to consume the consumables. If async_request is True, the method is executed asynchronously
        in different threads.
        :param consumables: A list of consumables to process
        :param params: The parameters to pass to the API call
        :param method: The method to use (POST or GET)
        :param async_request: Whether to execute the method asynchronously
        :return: A list of DataClass objects
        """
        dataclasses = []

        if async_request:

            with ThreadPoolExecutor() as executor:
                futures = {executor.submit(self.__consume__,  ##
                                           consumable, self.params, self.method): consumable for consumable in
                           consumables}
                for future in as_completed(futures):
                    consumable = futures[future]
                    try:
                        dataclasses.append(future.result())
                    except Exception as e:
                        print(f"There was an error while fetching consumable {consumable}: {e}")
        else:
            for consumable in consumables:
                dataclasses.append(self.__consume__(consumable, self.params, self.method))

        return dataclasses
