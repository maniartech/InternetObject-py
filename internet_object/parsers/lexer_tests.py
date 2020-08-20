import unittest
from lexers import Lexer


class LexerTest(unittest.TestCase):

  def test(self):

    t1 = r"""
    ~ "man\"iar
      ",, 'tasdfasdf'' asdfasdf',
    ~ 10,  T, F, 20,  test: abc # This is a comment
    --- ab, b, N, testing,
    ~ { aamir: maniar  , -200.50  , 'adsfasdf'   }
    ~ "test  " 'wow'
    """

    t2 = "testing"
    lexer = Lexer(t1)
    lexer.read_all()
    lexer.print_tokens()
    self.assertTrue(True)


if __name__ == '__main__':
  unittest.main()
