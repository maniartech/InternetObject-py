import unittest
from .ast_parsers import AST
from internet_object.utils import helpers


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
    helpers.pretty_print(ast)


if __name__ == '__main__':
  unittest.main()
