class MissingValueParserException(Exception):
    def __init__(self, missing_option):
        super().__init__(f'Missing value for option {missing_option}')