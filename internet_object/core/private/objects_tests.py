import unittest

from utils import helpers
from .objects import InternetObject


class ObjectTest(unittest.TestCase):

  def test(self):
    o = InternetObject.parse(r"""
    name: Spiderman,
    age: 25,
    address: {
      Bond Street, New York, NY
    }
    """)

    assert(o is not None)
