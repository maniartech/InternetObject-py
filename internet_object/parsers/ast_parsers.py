from internet_object.utils import helpers

from .tokens import Token
from .lexers import Lexer
from .nodes import Node


class AST:

  def __init__(self, text, only_def=False):
    self.text = text
    self.lexer = Lexer(text)
    self.last_token = None
    self.token = None
    self.index = 0

    self.stack = []
    self.val_pipe = []
    self.only_def = only_def

    self.tree = {
        "header": None,
        "data": None
    }

  def parse(self):
    lexer = self.lexer

    while True:

      if lexer.done:
        break


      self.token = lexer.read()

      if self.token is None:
        continue

      if self.token.type == 'comment':
        continue

      self.process()

    self.finalize()

    if self.only_def:
      self.tree['header'] = self.tree['data']
      self.tree['data'] = None

    # helpers.pretty_print(self.tree)

  @property
  def header(self):
    return self.tree["header"]

  @property
  def data(self):
    return self.tree["data"]

  def process(self):
    token = self.token
    if token.type == "sep":
      if token.val == "{":
        self.push_container("object", token)

      elif token.val == "}":
        self.pop_container("object")

      elif token.val == "[":
        self.push_container("array", token)

      elif token.val == "]":
        # print_ast_stack(self.stack)
        self.pop_container("array")

      elif token.val == "~":
        self.process_collection()

      else:
        self.push_value(Node.from_token(token))

    elif token.type == "datasep":
      self.process_datasep()

    else:
      self.push_value(Node.from_token(token))

  def process_collection(self):
    data = self.tree['data']
    if data is None or isinstance(data, list):
      self.finalize()
      if data is None:
        self.tree["data"] = []
    else:
      raise SystemError("not-a-collection")

  def process_datasep(self):

    self.finalize()
    header = self.tree.get("header", None)

    if self.only_def:
      raise SyntaxError("invalid-datasep-found")

    if header is not None:
      raise SyntaxError("invalid-datasep-found")

    self.tree["header"] = self.tree["data"]
    self.tree["data"] = None

  def push_value(self, val):
    is_comma = val.type == "sep" and val.val == ","
    is_collon = val.type == "sep" and val.val == ":"
    pipe = self.val_pipe
    pipe_len = len(pipe)

    container = self.get_or_create_last_container()
    values = container.val
    values_len = len(values)

    try:
      last_value = values[-1]
    except IndexError:
      last_value = None

    if is_comma:
      # When comma is received while pipe is empty
      # push undefined token
      if pipe_len == 0 or pipe[-1] == ",":
        # undefined_node = self.get_undefined_node()
        values.append(None)
        pipe.append(",")

      else:
        pipe.append(",")

    elif is_collon:
      # Throw a syntax error
      # When colon is received while pipe is empty,
      if (pipe_len == 0 or
          # When last value in the pipe is colon
          pipe[-1] == ":" or
              # When last value in the pipe is not a string
              pipe[-1].type != "string"):
        print(pipe)
        raise SyntaxError("unexpected-colon")

      else:
        # Just add the colon
        pipe.append(":")

    else:
      # When the last char in pipe is : setup key-value
      if pipe_len > 0 and pipe[-1] == ":":
        # print(">>>", last_value)
        values[-1] = val
        values[-1].key = last_value.val

        # last_value.key = last_value.val
        # last_value.type = val.type
        # last_value.val = val
        pipe.append(val)

      else:  # if pipe_len == 0 or pipe[-1] == ",":
        val.pos = values_len
        pipe.append(val)
        values.append(val)

  def finalize(self):
    if len(self.stack) == 2 and self.stack[-1].type == "collection":
      self.pop_container("collection")

    # remove the root container object if found
    if len(self.stack) == 1:
      self.pop_container("object")

    if len(self.stack) != 0:
      raise SyntaxError("incomplete-%s" % self.stack[0].type)

  def pop_container(self, container_type):
    container = self.stack[-1]
    if container.type != container_type:
      raise SyntaxError("incomplete-%s" % container.type)
    self.stack = self.stack[:-1]

  def push_container(self, object_type, token):
    parent = self.get_last_container()

    if object_type == "collection":
      if parent is not None:
        raise SyntaxError("invalid-collection-postion")

      self.finalize()

    pos = parent.pos + 1 if parent is not None else 0
    node = Node([], object_type, token.start,
                token.end, token.row, token.col, pos, parent)

    self.push_value(node)
    self.stack.append(node)

  def get_undefined_node(self, parent=None):
    index = 0 if parent is None else len(parent.val)
    return Node(None, "undefined", 0, 0, 1, 1, 0, parent)

  def get_value_node(self, token, parent=None):
    index = 0 if parent is None else len(parent.val)
    return Node(token.val, token.type, token.start,
                token.end, token.raw, token.col, index, parent)

  def get_last_container(self):
    if len(self.stack) == 0:
      return None

    return self.stack[-1]

  def get_or_create_last_container(self):
    node = self.get_last_container()
    if node is None:
      node = Node([], "object", 0, 0, 1, 1, 0, None)
      self.stack.append(node)
      if isinstance(self.tree['data'], list):
        self.tree['data'].append(node)
      else:
        self.tree["data"] = node

    return node
