# Mini script to quickly test the ParameterParser class
from src.parser.parameter_parser import ParameterParser
from src.exceptions.missing_value_parser_exception import MissingValueParserException

parser = ParameterParser(['-o', '-i', '-u'])
################################################################################################################
# Test output when all parameters are given
user_input_test_1 = 'test.py -o output_file.txt -i input_file.txt -u https://example.com'.split(' ')
output_test_1 = parser.parse_user_input(user_input_test_1)
assert output_test_1['-o'] == 'output_file.txt', f'-o should be output_file.txt, got {output_test_1["-o"]}'
assert output_test_1['-i'] == 'input_file.txt', f'-i should be input_file.txt, got {output_test_1["-i"]}'
assert output_test_1['-u'] == 'https://example.com', f'-u should be https://example.com, got {output_test_1["-u"]}'
################################################################################################################
# Test output when all parameters are given but not in order
exception_test_2 = None
user_input_test_2 = 'test.py -o output_file.txt input_file.txt -i -u https://example.com'.split(' ')
try:
    output_test_2 = parser.parse_user_input(user_input_test_2)
except Exception as e:
    exception_test_2 = e
assert exception_test_2 is not None and isinstance(exception_test_2, MissingValueParserException), \
    f'Parser was expected to throw MissingValueParserException, got {exception_test_2}'
################################################################################################################
# Test output when last parameter is not given
exception_test_3 = None
user_input_test_3 = 'test.py -o output_file.txt -i input_file.txt -u'.split(' ')
try:
    output_test_3 = parser.parse_user_input(user_input_test_3)
except Exception as e:
    exception_test_3 = e
assert exception_test_3 is not None and isinstance(exception_test_3, MissingValueParserException), \
    f'Parser was expected to throw MissingValueParserException, got {exception_test_3}'
