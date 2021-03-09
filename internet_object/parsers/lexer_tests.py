import unittest
from internet_object.parsers.lexers import Lexer


class LexerTest(unittest.TestCase):

  def test(self):

    t1 = r"""
    ~ "man\"iar       ",, 'tasdfasdf'' asdfasdf',
    ~ 10,  T, F, 20,  test: abc # This is a comment
    --- ab, b, N, testing,
    ~ { aamir: maniar  , -200.50  , 'adsfasdf'   }
    ~ "test  " 'wow'
    """

    t2 = r"""
    "Hello\"World   ", wopw, 'Peter D''silva ', 0b100, 0xFF, 0c10
    """
    lexer = Lexer(t2)
    lexer.read_all()
    lexer.print_tokens()
    self.assertTrue(True)

if __name__ == '__main__':
  unittest.main()
