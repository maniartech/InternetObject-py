import unittest

from utils import helpers

from schema.schema_compiler import compile_schema
from parsers.ast_parsers import AST


class SchemaCompilerTest(unittest.TestCase):

  def test(self):

    t1 = r"""
    name, age:number, address:{string, maxLength: 40}
    """

    ast = AST(t1, True)
    ast.parse()
    schema = compile_schema(ast.header)
    # helpers.pretty_print(schema)


# if __name__ == '__main__':
#   unittest.main()
