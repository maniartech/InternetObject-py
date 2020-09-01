import unittest

from utils import helpers

from schema.schema_compiler import compile
from parsers.ast_parsers import AST


class SchemaCompilerTest(unittest.TestCase):

  def test(self):

    t1 = r"""
    name, age:number, address: {
      city:string,
      state: {string, len:2},
      coordinates: {
        { type:string, maxLen:{int} },
        type: object,
        default: {}
      }
    },
    *
    """

    ast = AST(t1, True)
    ast.parse()
    schema = compile(ast.header)
    # helpers.pretty_print(ast.tree)


# if __name__ == '__main__':
#   unittest.main()
