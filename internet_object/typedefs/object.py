from internet_object.typedefs import TypeDef, registry
from internet_object.core import undefined


from internet_object.utils import helpers, is_scalar, is_datatype
from internet_object.core import parse, InternetObject, errors

class ObjectDef(TypeDef):

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

         # When memberdef is not available
        if schema is None:
          # TODO: Validate dynamic members
          # Also try to get path from memberdef!
          if node.key:
            raise KeyError("%s.%s" % (node.key, item.key))
          else:
            raise KeyError("%s" % item.key)

      typedef = registry.get_typedef(schema.type)
      o[schema.name] = typedef.parse(item, schema)

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
