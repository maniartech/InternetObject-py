from internet_object.parsers.lexers import Lexer
import unittest

from internet_object.utils import helpers

from internet_object.schema.schema_compiler import compile
from internet_object.parsers.ast_parsers import AST


class SchemaCompilerTest(unittest.TestCase):

  def test(self):

    t1 = r"""
    name, age:number, address: {
      city:string,
      state: {string, len:2},
      test: {{}},
      test2: {},
      coordinates: {
        type: object,
        default: {}
      }
    }
    """

    # Test [], [{}], [string], {[]} *

    t2 = r"""
    name?:string, age*:number, tag:{string, minLen:1},
    test: {building, street, city, state},
    test2?: {schema:{a?:string, b*, c*?:}}
    """

    # b:{[string]}, c:{[{a, b, c}], d:{address:{}, min:0, type:array}, e:{schema:[]}}
    t3 = r"""
    a*:{[{string, maxLen:10}], default=[]}, b:{[{a, b, c:{x, y, z:[]}}]}
    """

    t4 = r"""
    a:{[]}
    """
    #  c:{[{[{{a, b, c}, default={}},], maxLen:10}]}}
    # lexer = Lexer(t2)
    # lexer.read_all()
    ast = AST(t3, True)
    ast.parse()
    # helpers.pretty_print(ast.tree)
    schema = compile(ast.header)

    helpers.pretty_print(schema)


# if __name__ == '__main__':
#   unittest.main()
