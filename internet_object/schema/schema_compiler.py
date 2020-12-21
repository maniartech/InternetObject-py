from .schema_utils                import find_name_val, find_key, join_path
from .schema_utils                import get_object, is_memberdef

from internet_object.core         import errors, InternetObject
from internet_object.utils        import helpers, is_datatype
from internet_object.typedefs     import registry
from internet_object.core.private import errors


def compile(tree, path='', defs=None):

  if tree is None:
    return None

  # Empty object
  if len(tree) == 0:
    return {}

  if tree.type != 'object':
    raise TypeError(errors.OBJECT_REQUIRED)

  schema = InternetObject()
  for item in tree.val:
    if item is None:
      assert('Check out why item is None')
      # raise ValueError(errors.VALUE_REQUIRED)

    # Find key, val
    name, val = find_name_val(item)

    if isinstance(name, str) is False:
      raise errors.INVALID_KEY # Key must be string!

    # TODO: Parse defs here!

    memberdef = None

    # Process string keys
    if is_datatype(val):
      # name
      # key: string
      # key: any
      memberdef = get_memberdef(name, val, path)

    elif item.type == 'object':
      # When item type is an object, it could be a schema
      # or a memberdef.
      # key: {string, default=test}
      # address: {city, state, zip}
      # color: {{r, g, b}, default={0, 0, 0}, null=True}
      # test: {}
      memberdef = get_object_memberdef(name, item, path, defs)

    elif item.type == 'array':
      # tags: []
      # tags: {[], min=1}
      # tags: [string]
      memberdef = get_array_memberdef(name, item, path, defs)

    else:
      raise errors.INVALID_DATATYPE

    if memberdef is not None:
      schema.append(memberdef, memberdef.name)

    else:
      raise TypeError(errors.INVALID_DATATYPE)

  return schema

def get_memberdef(name, type_, path, defs=None):
  memberdef = get_object(name, type_, path)

  if type_ == 'object':
    memberdef.schema = {}

  if type_ == 'array':
    memberdef.schema = []

  return memberdef

def get_object_memberdef(name, tree, path, defs=None):
  # typename = None
  o = get_object(name, 'object', path)

  # key: {}
  if len(tree.val) == 0:
    # Return any object memberdef
    o.schema = {}
    return o

  is_it_memberdef, datatype = is_memberdef(tree)
  # helpers.pretty_print (is_it_memberdef, tree, datatype)

  # key: {string, ...}
  # key: {{}, ...}
  if is_it_memberdef:
    try:
      if datatype == 'object':
        memberdef = parse_objectdef(o, tree)
      elif datatype == 'array':
        memberdef = parse_arraydef(name, tree, path, defs)
      else:
        memberdef = parse_memberdef(o, tree, datatype)
      return memberdef
    except errors.ValidationError as ex:
      # TODO: Improve error
      raise errors.ValidationError('Error while parsing %s (%s)' % (o.path, ex,))

  # address: { street, city, state }
  else:
    # TODO: Add default

    o.schema = compile(tree, o.path, defs)
    return o

def get_array_memberdef(name, tree, path, defs=None):
  """
  When o.type is an array!
  """

  o = get_object(name, 'array', path)

  array_len = len(tree.val)
  # tags: []
  if array_len == 0:
    o.schema = []
    return o

  if array_len == 1:
    first = tree.val[0]

    if first.type == 'string':
      if first.val == 'object':
        return {}
      elif first.type == 'array':
        return 'any'
      elif is_datatype(first.val):
        return first.val
      else:
        raise errors.INVALID_DATATYPE
        # return [get_object_memberdef(o.name, first.val, path, defs)]
    elif first.type == 'object':
      print(">>>", o.name)
      return get_object_memberdef(o.name, first, '' , defs)

  else:
    raise "multiple-schema"

def parse_memberdef(o, tree, datatype):
  # Scalar datatypes such as string, number etc...
  # key: { string, ... }
  typedef = registry.get_typedef(datatype)
  if typedef is None:
    raise errors.INVALID_DATATYPE

  memberdef = registry.get_typedef("object").parse(tree, typedef.definition)
  o.update(**memberdef)
  return o

def parse_arraydef(name, tree, path, defs=None):
  """
  Parses the tree def that looks like array!
  {[], ...},
  {[ string ], ...},
  {[ {a, b, c} ], ...}
  {[ [ { string } ] ], ...}

  Receives the objects in the following format!
  { type:object, val:[{ type:array, val:...}]}
  """

  o = get_object(name, 'array', path)

  if len(tree.val) == 0:
    o.schema = []
    o.type = "array"
    return o

  # {[string], ...} {[{a, b, c}], ....}
  elif tree.val[0].type == 'array':
    o.schema = get_array_memberdef('', tree.val[0], path + '[', defs)
    o.type = "array"

    return o

  elif tree.val[0].type == 'object':
    o.schema = get_object_memberdef('', tree.val[0], path + '[', defs)

    o.schema.type = 'array'
    return o

    # [ {} ]
    # if first

  # if schema is None:
  #   if (tree.val) > 0:
  #     raise exc
  #   if tree.val[0].type == 'array':
  #     val = tree.val[0].val

  #   else:
  #     # TODO: Check this!
  #     assert False, "invalid-block"

  # if schema is not None:

  #   return o

def parse_objectdef(o, tree, defs=None):
  schema = None
  # key: {'object', schema:{}, ...}
  if tree.type == 'object': # TODO: Fix this <- Find type key
    schema = find_key('schema', tree, None)

  # key: {{}, ...}
  if schema is None:
    if isinstance(tree.val[0], dict):
      schema = tree.val[0]
    else:
      # TODO: Check this!
      assert False, "invalid-block"

  o.schema = compile(schema, o.path)
  return o
