import unittest
from lexers import Lexer


class LexerTest(unittest.TestCase):

  def test(self):

    lexer = Lexer(r"""
    ~ "man\"iar
      ",
    ~ 10,  T, F, 20,  test: abc # This is a comment
    --- ab, b, N, testing,
    ~ { aamir: maniar  , -200.50  , 'adsfasdf'   }
    ~ "test  " "Wow"
    """)
    lexer.read_all()
    lexer.print_tokens()
    self.assertTrue(True)


if __name__ == '__main__':
  unittest.main()
