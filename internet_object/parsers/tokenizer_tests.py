import unittest
from tokenizer import Tokenizer


class TokenizerTest(unittest.TestCase):

  def test(self):

    tokenizer = Tokenizer(r""""man\"iar", 10, 20, "abc" """)
    tokenizer.read_all()
    tokenizer.print_tokens()
    self.assertTrue(True)


if __name__ == '__main__':
  unittest.main()



