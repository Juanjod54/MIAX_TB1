from src.exceptions.missing_value_parser_exception import MissingValueParserException


class ParameterParser:

    def __init__(self, allowed_options=None):
        self.allowed_options = {}
        # Create a map with allowed options for faster parsing
        for option in ([] if allowed_options is None else allowed_options):
            self.allowed_options[option] = None

    def parse_user_input(self, user_inputs: list[str]):
        idx = 0
        length = len(user_inputs)
        while idx < length:
            user_input = user_inputs[idx]
            idx += 1  # Polyfill to user_inputs[idx++]
            if user_input in self.allowed_options:
                # As the index has increased, we're getting the next value
                # I.E.: "-o file.txt" -> ["-o", "file.txt"]
                ######################
                # # Check we are still in range and that we were given a value (not the next option)
                if idx >= length or user_inputs[idx] in self.allowed_options:
                    raise MissingValueParserException(user_input)
                ######################
                self.allowed_options[user_input] = user_inputs[idx]
                # Polyfill to user_inputs[idx++]. We want to skip the option's value
                idx = idx + 1

        return self.allowed_options
