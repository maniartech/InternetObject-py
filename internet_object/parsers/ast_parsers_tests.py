import unittest
from ast_parsers import AST


class ASTTest(unittest.TestCase):

  def test(self):

    ast = AST(r"""
    a, b, c
    """)

    ast.parse()


if __name__ == '__main__':
  unittest.main()
