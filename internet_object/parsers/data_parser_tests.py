import unittest

from utils import helpers
from parsers import DataParser


class DataParserTest(unittest.TestCase):

  def test(self):

    t1 = r"""
    {string, maxLength: 10, choices:[test, best]}
    """

    t2 = "{building, street:string, city{string, maxLen:2}, state}"

    parser = DataParser(t2)
    data = parser.parse()
    helpers.pretty_print(data)
