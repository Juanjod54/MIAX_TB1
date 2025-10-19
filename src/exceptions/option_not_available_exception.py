class OptionNotAvailableException(Exception):
    def __init__(self, option):
        super().__init__(f'Option {option} not available')