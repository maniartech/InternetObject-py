from utils import helpers
from utils import is_datatype, is_scalar, is_container
from .memberdef import MemberDef, SchemaDef



# Return the python dictionary
def compile_schema (tree, vars=None):

  if tree is None:
    return None

  if is_scalar(tree.type):
    return tree.val

  is_array = tree.type == "array"
  is_obj = tree.type == "object"

  if is_container(tree.type):
    # helpers.pretty_print(tree)

    container = {} if is_obj else []

    members = []

    # helpers.pretty_print(tree)
    for index, member in enumerate(tree.val):
      val = None

      if is_scalar(member.type):
        val = member.val

      if is_container(member.type):
        val = compile_schema(member,
                    {} if member.type == "object" else [])

      if is_array:
        if member.key is not None:
          val = {member.key: val}

        container.append(val)

      elif is_obj:
        key = member.key if member.key is not None else str(index)
        container[key] = val

      members.append({
          "key": key if member.key else index,
          "val": val
        })


    helpers.pretty_print(members)
    helpers.pretty_print(container)

    return container

  return None


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
