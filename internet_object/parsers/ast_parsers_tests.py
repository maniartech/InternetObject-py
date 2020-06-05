import unittest
from ast_parsers import AST


class ASTTest(unittest.TestCase):

  def test(self):

    ast = AST(r"""
    a:1, b:T, c:[A:{B:C}]
    """)

    ast.parse()


if __name__ == '__main__':
  unittest.main()
