from internet_object.typedefs import TypeDef
from internet_object.core import undefined
import re

from utils import is_scalar, is_datatype
from core import parse, InternetObject, errors
from .type_registries import type_registry as registry


class SchemaObjectDef(TypeDef):

  definition = InternetObject.parse(r"""
                schema: object,
                default?: object,
                "null"?: {bool, default:F},
                optional?: {bool, default:F},
                type?: {
                  string,
                  default:"object",
                  choices:["object"] },
                """)

  def __init__(self):
    self.typename = 'object'

  def parse(self, node, memberDef):
    val, is_final = self.clean(None if node is None else node.val, node, memberDef)

    if is_final:
      return val

    o = InternetObject()
    keyedMembers = False

    for index, item in enumerate(val):
      if item.key is None:
        # positional members must not appear after the keyed members
        if keyedMembers is True:
          raise ValueError(errors.INVALID_POSITIONAL_VALUE)

        schema = memberDef.get(index)
      else:
        keyedMembers = True
        schema = memberDef.get(item.key)

      typedef = registry.get_typedef(schema.type)
      val = typedef.parse(item, schema)
      o[schema.name] = val

    # keyedMembers = False
    for index, key in enumerate(memberDef.keys()):
      if key in o:
        continue

      schema = memberDef.get(index)
      typedef = registry.get_typedef(schema.type)
      if typedef is None:
        continue

      val = typedef.parse(None, schema)
      if val is not undefined:
        o[schema.name] = val

    return o

  def find_key_val(self, member):
    # Check if key exists or not!
    if member["key"] is None:
      return member["val"], "any"

    return member["key"], member["val"]
