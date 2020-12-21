import re
from collections.abc import MutableMapping
from utils import helpers
from utils import is_datatype, is_scalar, is_container
from .memberdef import MemberDef, SchemaDef
from core import parse, errors, InternetObject
from typedefs import registry


# Return the python dictionary
def compile(tree, vars=None):
  if tree is None:
    return None

  if tree.type == "object":
    helpers.pretty_print(tree)
    schema = compile_object(tree, "", vars)

  else:
    raise "Invalid object"


def compile_object(tree, path="", vars=None):

  schema = InternetObject()
  for item in tree.val:

    if item is None:
      assert("Check out why item is None")
      # raise ValueError(errors.VALUE_REQUIRED)

    # Find key, val
    name, val = find_name_val(item)

    if isinstance(val, str):
      if is_datatype(val):
        schema.append(InternetObject({
          "name": name,
          "type": val,
          "path": join_path(name, path)
        }), name)
      else:
        raise errors.INVALID_DATATYPE

    if item.type == 'object':
      memberdef = get_object_memberdef(item)

      if memberdef is not None:
        schema.append(memberdef, name)
      else:
        obj = parse(item)
        schema.append(get_memberdef_from_object(name, item), name)

  helpers.pretty_print(schema)
  return schema

def compile_array(tree, path="", vars=None):
  pass

def find_name_val(item):
  # Check if key exists or not!
  if item.key is None:
    return item.val, "any"

  return item.key, item.val

def join_path(name, path):
  return name if len(path) == 0 else "%s.%s" % (path, name)


def get_memberdef_from_object(name, item):
  obj = parse(item)

  # Datatype is found at 0th position
  typename = obj.get("0")
  if is_datatype(typename):
    obj.type = typename
    del obj["0"]

  if typename is None:
    typename = obj.get("type")
    if is_datatype(typename):
      obj.type = typename
      del obj["type"]

  if typename is None:
    raise TypeError(errors.INVALID_DATATYPE)

  objectdef = registry.get_typedef("object")
  typedef = registry.get_typedef(typename)
  definition = typedef.definition

  o = objectdef.parse(item, definition)
  # print (o)

  return obj


def get_object_memberdef(tree):
  typename = None

  if tree.type == 'object':
    # name: {}
    # Return any object memberdef
    if len(tree.val) == 0:
      typename = 'object'

    for index, item in enumerate(tree.val):
      if index == 0:
        # name: {string, ...}
        # Return string memberdef
        if item.key is None and is_datatype(item.val):
          typename = item.val

      # name: {..., type:string}
      # Return memberfed
      elif item.key == 'type' and is_datatype(item.val):
        typename = item.val

    if typename is not None:
      return parse_memberdef(typename, tree)

  # Array
  elif tree.type == 'array':
    array_len = len(tree.val)
    # name: []
    if array_len == 0:
      return 'array'

    if array_len == 1:
      val = tree.val[0]

      # name: [string]
      if is_datatype(val):
        return 'array'

    else:
      raise ValueError(errors.INVALID_OPERATION)
  else:
    return None

  if typename is not None:
    typedef = registry.get_typedef(typename)

    if typedef is None:
      raise ValueError(errors.INVALID_DATATYPE)

    typedef.parse(tree, typedef.definition)

  return None



def parse_memberdef(typename, data):
  typedef = registry.get_typedef(typename)
  objectdef = registry.get_typedef('object')
  memberdef = objectdef.parse(data, typedef.definition)
  return memberdef

def is_memberdef(o):
  if len(o) == 0:
    return False

  return (
    (
      # is_datatype(o.keys()[0]) or # { string, ... }
      is_datatype(o.get("0")) or # { "0": string }
      (o.has_key("type") and is_datatype(o.type))
    ) and (
      o.has_key("schema") is False
    )
  )


