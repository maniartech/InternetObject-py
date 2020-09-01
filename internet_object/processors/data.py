# from objects import InternetObject
from collections.abc import MutableMapping
from parsers import AST
from utils import is_datatype, is_scalar, is_container
from .objects import IOObject

class DataProcessor:

  def __init__(self, data, is_header=False):
    super().__init__()

    if isinstance(data, str):
      ast = AST(data)
      ast.parse()
      self.data_tree = ast.data

    elif isinstance(data, AST):
      self.data_tree = data.data if is_header is False else data.header

    elif isinstance(data, MutableMapping):
      self.data_tree = data

    else:
      self.data_tree = None

  def parse(self):
    return parse(self.data_tree)


# Return the python dictionary
def parse (tree, vars=None):


  if tree is None:
    return None

  if is_scalar(tree.type):
    return tree.val

  is_array = tree.type == "array"
  is_obj = tree.type == "object"

  if is_container(tree.type):
    # helpers.pretty_print(tree)

    container = IOObject() if is_obj else []

    # helpers.pretty_print(tree)
    for index, member in enumerate(tree.val):
      val = None

      if is_scalar(member.type):
        val = member.val

      if is_container(member.type):
        val = parse(member,
                    IOObject() if member.type == "object" else [])

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

