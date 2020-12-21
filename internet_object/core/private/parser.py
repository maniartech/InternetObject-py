# from objects import InternetObject
from collections.abc import MutableMapping

from parsers import AST
from utils import is_datatype, is_scalar, is_container
import core


# Return the python dictionary
def parse (data, is_header=False, defs=None):

  if isinstance(data, str):
    ast = AST(data)
    ast.parse()
    node = ast.data

  elif isinstance(data, AST):
    node = data.data if is_header is False else data.header

  elif isinstance(data, MutableMapping):
    node = data

  else:
    node = None

  if node is None:
    return None

  if is_scalar(node.type):
    return node.val

  is_array = node.type == "array"
  is_obj = node.type == "object"

  if is_container(node.type):
    # helpers.pretty_print(node)

    container = core.InternetObject() if is_obj else []

    # helpers.pretty_print(node)
    for index, member in enumerate(node.val):
      val = None

      if is_scalar(member.type):
        val = member.val

      if is_container(member.type):
        val = parse(member,
                    core.InternetObject() if member.type == "object" else [])

      if is_array:
        if member.key is not None:
          val = {member.key: val}

        container.append(val)

      elif is_obj:
        key = member.key if member.key is not None else str(index)
        # container[key] = val
        container.append(val, key)

    return container

  return None


def is_memberdef(o):
  if is_datatype(o["0"]):
    return True

  if is_datatype(o["type"]):
    return True

