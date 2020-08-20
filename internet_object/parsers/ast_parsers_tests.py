import unittest
from parsers.ast_parsers import AST


class ASTTest(unittest.TestCase):

  def test(self):

    t1 = r"""
    ~ a:1,N,, b:{T}, c:[A:{B:C}]
    ~ 1, 2, 3
    ---
    """

    t2 = r"""
    a:1,N,, b:{T}, c:[A:{B:C}]
    """

    t3 = r"""
    a
    """

    ast = AST(t1, False)
    ast.parse()


if __name__ == '__main__':
  unittest.main()
