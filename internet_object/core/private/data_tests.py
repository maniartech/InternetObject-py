import unittest

from utils import helpers
from .data import DataProcessor


class DataParserTest(unittest.TestCase):

  def test(self):

    t1 = r"""
    name:string,
    age:{number},
    address: {
      schema:{
        city:string,
        state: {string, len:2},
        coordinates: {
          { lat, lng },
          type: object
        }
      }
    },
    *
    """

    t2 = "{building, street:string, city{string, maxLen:2}, state}"

    parser = DataProcessor(t1)
    data = parser.parse()
    # import pdb; pdb.set_trace()
    helpers.pretty_print(data)
