from utils import helpers
from utils import is_datatype, is_scalar, is_container
from .memberdef import MemberDef, SchemaDef
from core import parse, errors, InternetObject


# Return the python dictionary
def compile(tree, vars=None):
  if tree is None:
    return None

  if tree.type == "object":
    obj = parse(tree, True)
    helpers.pretty_print(tree)
    helpers.pretty_print(obj)
    schema = compile_schema(obj, "", vars)
    helpers.pretty_print(schema)

  else:
    raise "Invalid object"


def compile_schema(obj, path="", vars=None):

  schema = InternetObject()

  # helpers.pretty_print(tree)
  for item in obj.fields():

    # Find key, val
    name, val = find_key_val(item)

    if val.type == 'object':
      print(">>>", val)
      print("---", is_memberdef(val))
      if is_memberdef(val):
        schema.append(get_memberdef(name, "object", path, **val), name)
      else:
        schema.append(
          get_memberdef(name, "object", path, schema=compile_schema(val, name, vars)),name)

    if isinstance(val, str):
      if is_datatype(val):
        schema.append(get_memberdef(name, val, path), name)
      else:
        raise errors.INVALID_DATATYPE

  return schema

def find_key_val(item):
  if item.key is not None:
    return item.key, item.val

  if item.type == 'string':
    return item.val, 'any'

  if item.type in ['number', 'int', 'int32', 'int16', 'byte']:
    return str(item.val), 'any'

  raise ValueError(errors.INVALID_KEY)

def compile_memberdef(obj, var=None):
  if obj.type != "object":
    raise errors.INVALID_OPERATION

def normalize_memberdef(name, memberdef):

  if is_datatype(memberdef):
    type_ = memberdef

  type_ = memberdef.type or memberdef.get("0")

  return InternetObject()


def get_memberdef(name, type_, path, **kwargs):
  memberDef = InternetObject({
      "name": name,
      "type": type_,
      "path": name if len(path) == 0 else "%s.%s" % (path, name)
  })
  memberDef.update(kwargs)
  return memberDef


def get_object_memberdef(name, o):
  return None


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


def compile_array(tree, vars=None):
  pass

