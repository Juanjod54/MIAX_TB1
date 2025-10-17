from src.domain.consumable import Consumable


class IncompatibleDataTypeException(Exception):
    def __init__(self, data_type: Consumable.data_type ):
        super().__init__(f'Incompatible data type {data_type}')
