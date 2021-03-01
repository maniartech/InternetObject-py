from internet_object.utils import helpers
import re
from typing import MutableMapping
from internet_object.core import InternetObject
from internet_object.utils import is_datatype

def get_object(name, type, path, **kwargs):
  regex = r'[\*\?]{1,2}$'
  matches = list(re.finditer(regex, name, re.MULTILINE))

  if len(matches) == 0:
    optional = False
    null = False
  else:
    match = matches[0].group()
    optional = '?' in match
    null = '*' in match
    name = name.replace('*', '').replace('?', '')

  path = join_path(path, name)

  o = InternetObject({
    'name': name,
    'type': type,
    'optional': optional,
    'null': null,
    'path': path
  })

  o.update(**kwargs)
  return o

def is_memberdef(tree):
  """
  Returns true in the following conditions!
  - The first value is a datatype name
    { string, ...}, {object, ...}, {number, ....}

  - The first value is an object or an array
    {{}, ...}, {[], ...}

  - Has a val with type key whose value is a datatype
    {..., type:string}, {..., type:object}

  - Type is missing but has a schema key, whose type is object or array
    {..., schema: {...}}, {..., schema:[] }
  """

  if len(tree.val) == 0:
    return False, None

  first = tree.val[0]

  # Checkout first non-key member!
  if first.key is None:

    # Value at zeroth position is datatype name
    # { string, ...}, {object, ...}, {number, ....}
    if first.type == 'string' and is_datatype(first.val):
      return True, first.val

    # The first value is an object or an array
    # {{}, ...} {[], ...}
    if first.type in ['array', 'object']:
      return True, first.type

  # Has a val with type key whose value is a datatype
  # {..., type:string}, {..., type:object}
  typename = find_key("type", tree)
  if typename is not None and is_datatype(typename):
    return True, typename

  # Type is missing but has a schema key, whose type is object or array
  # {..., schema: {...}}, {..., schema:[] }
  schema = find_key("schema", tree)
  if schema is not None and schema.type in ['object', 'array']:
    return True, schema.type

  return False, None

def find_name_val(tree):
  # Check if key exists or not!
  if tree.key is None:
    return tree.val, 'any'
  return tree.key, tree.val

def find_key(key, tree, default=None):
  try:
    for val in tree.val:
      if val.key == key:
        return val
  except:
    return default
  return default

def join_path(path, name):
  if len(path) == 0: return name

  if path[-1] == '[':
    return path
  return '%s.%s' % (path, name)
