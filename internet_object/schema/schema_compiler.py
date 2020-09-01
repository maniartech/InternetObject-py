from utils import helpers
from utils import is_datatype, is_scalar, is_container
from .memberdef import MemberDef, SchemaDef
from processors import DataProcessor
from processors.objects import IOObject


# Return the python dictionary
def compile(tree, vars=None):

  if tree is None:
    return None

  if tree.type == "object":
    processor = DataProcessor(tree, True)
    obj = processor.parse()
    helpers.pretty_print(obj)
    return compile_schema(obj, "", vars)

  else:
    raise "Invalid object"


def compile_schema(obj, path="", vars=None):

  # print("+++", obj)

  # if is_memberdef(obj):
  #   return compile_memberdef(obj, vars)

  schema = IOObject()

  # helpers.pretty_print(tree)
  for item in obj.fields():

    if item.key == str(item.index):
      # if isinstance(item.val, IOObject)
      name = item.val
      val = "any"
    else:
      name = item.key
      val = item.val
      # print("***", name, val)

    # name = item.val if item.key == str(item.index) else item.key
    # val = "any" if item.key == str(item.index) else item.val

    if isinstance(val, str):
      if is_datatype(val):
        schema.append(get_memberdef(name, val, path), name)
      else:
        raise "invalid-datatype"

    if isinstance(val, IOObject):
      if is_memberdef(val):
        schema.append(get_object_memberdef(val), name)
      else:
        # print(">>>", name, compile_schema(val, name, vars))
        schema.append(
          get_memberdef(name, "object", path, schema=compile_schema(val, name, vars)),name)

  helpers.pretty_print(schema)

  return schema


def compile_memberdef(obj, var=None):
  if obj.type != "object":
    raise "invalid-operation"


def get_memberdef(name, type_, path, **kwargs):
  memberDef = IOObject({
      "name": name,
      "type": type_,
      "path": name if len(path) == 0 else "%s.%s" % (path, name)
  })
  memberDef.update(kwargs)
  return memberDef

def get_object_memberdef(o):
  return None


def is_memberdef(o):
  if len(o) == 0:
    return False

  if isinstance(o[0], IOObject):
    if is_memberdef(o[0]):
      raise "invalid-object"
    return True

  return is_datatype(o.get_key(0)) or (o.has_key("type") and is_datatype(o.type))

# def is_keyval()


def compile_array(tree, vars=None):
  pass


def compile_schema_bak(tree):
  header = tree.header

  if header is None:
    return None

  if header.type == "object":
    mdef = MemberDef("root", "object", "")
    mdef.schema = SchemaDef("object")
    __process_object(header, mdef)
    return mdef

  return None


def __process_object(o, odef):

  schema = odef.schema
  schema.members
  mdef = None

  for m in o.val:
    if __is_memberdef(m):
      mdef = __get_memberdef(m, odef.path)

    elif __is_object_schema(m):
      pass

    if mdef is not None:
      schema.members.append(mdef)


def __get_schema(o, schema_type, path):

  schema = SchemaDef(schema_type)

  for m in o.val:
    mdef = __get_memberdef(m, path)

    if mdef is not None:
      schema.members.append(mdef)

  return schema


def __get_memberdef(v, base_path):
  mtype = "any"
  optional = False
  null = False

  if v.key:
    name = v.key  # Key name

    if v.type == "string":
      if is_datatype(v.type):
        mtype = v.type
      else:
        raise ValueError('invalid-type')

    if v.type == 'object':
      if len(v.val) > 0 and is_datatype(v.val[0]):
        mtype = v.type
        index = 1
        props = __get_memberdef_props(v)

      else:  # Load object
        pass

  elif v.type == "string":
    name = v.val
  else:
    raise KeyError("invalid-key")

  mdef = MemberDef(
      name,
      mtype,
      name if base_path == '' else '.'.join([base_path, name]),
      optional=optional,
      null=null
  )
  return mdef


def __get_memberdef_props(o):
  pass


def __is_memberdef(o):
  if o.type == "string":
    return is_datatype(o.type)

  if o.type == "object":
    return (
        len(o.val) > 0 and
        is_datatype(o.val[0].val) and
        o.val[0].key is None
    )

  return False


def __is_object_schema(o):
  if (o.type == "object"):
    return len(o.val) == 0 or is_datatype(o.val[0]) is False
  return False


def __get_value(v, base_path):
  pass


# def __get
