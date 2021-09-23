import math
from re import split
import unittest
from lexers import Lexer


class LexerTest(unittest.TestCase):
    print("")

    def test_number(self):
        tests = {"213": 213, "37.697": 37.697, "-68": -68, "-348.978": -348.978,  "1.10e+20": 1.10e+20, "0xff":
                 hex(255), "0o77": oct(63), str(math.pi): math.pi, f"{str(oct(34))}": oct(34), f"{str(bin(52346))}": bin(52346),
                 "Inf": "Inf", "NaN": "NaN"}
        for i in tests:
            lex = Lexer(i+" ")
            lex.read_all()
            token = lex.return_tokens()
            tokenVal = token.__dict__["val"]
            self.assertTrue(
                tokenVal == tests[i], f"Expected : {tests[i]}, Got : {tokenVal}")

    def test_strings(self):
        tests = {'"hello"': '"hello"', 'World': "World", "'Hello \n'": "'Hello \n'", '"Test \n Test2"': '"Test \n Test2"', "'Tab\ttest'": """'Tab\ttest'""",
                 "'World'": "'World'", "'as\"df'": "'as\"df'", "''": "''", '""': '""', "test": "test"}
        for i in tests:
            lex = Lexer(i+" ")
            lex.read_all()
            token = lex.return_tokens()
            tokenVal = token.__dict__["val"]
            self.assertTrue(
                tokenVal == tests[i], f"Expected : {tests[i]}, Got : {tokenVal}")

    def test_boolean(self):
        tests = {"T": True, "F": False, "false": False, "true": True}
        for i in tests:
            lex = Lexer(i+" ")
            lex.read_all()
            token = lex.return_tokens()
            tokenVal = token.__dict__["val"]
            self.assertTrue(
                tokenVal == tests[i], f"Expected : {tests[i]}, Got : {tokenVal}")
if __name__ == '__main__':
    unittest.main()
