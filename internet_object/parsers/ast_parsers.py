from tokens import Token
from lexers import Lexer
from nodes import Node
from helpers import *


class AST:

  def __init__(self, text):
    self.text = text
    self.lexer = Lexer(text)
    self.last_token = None
    self.token = None
    self.index = 0

    self.stack = []
    self.val_pipe = []

    self.tree = {
        "data": None
    }

  def parse(self):
    lexer = self.lexer
    self.tree["data"] = self.get_or_create_last_container()

    while True:

      if lexer.done:
        break

      self.token = lexer.read()
      if self.token is None:
        continue

      self.process()

    if len(self.stack) == 2 and self.stack[-1].type == "collection":
      self.pop_container("collection")

    self.pop_container("object")

    # Stack must be empty
    self.check_complete()
    print(self.tree["data"])

  def get_object(self):
    pass

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
        self.push_container("collection", token)

      else:
        self.push_value(Node.from_token(token))

    elif token.type == "datasep":
      self.process_datasep()

    else:
      self.push_value(Node.from_token(token))

  def process_datasep(self):
    pass

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
              pipe[-1].type != "str"):
        print(pipe)
        raise SyntaxError("unexpected-colon")

      else:
        # Just add the colon
        pipe.append(":")

    else:
      # When the last char in pipe is : setup key-value
      if pipe_len > 0 and pipe[-1] == ":":
        last_value.key = last_value.val
        last_value.type = val.type
        last_value.val = val
        pipe.append(val)

      else:  # if pipe_len == 0 or pipe[-1] == ",":
        val.pos = values_len
        pipe.append(val)
        values.append(val)

  def check_complete(self):
    if len(self.stack) != 0:
      raise SyntaxError("incomplete-%s" % self.stack[0].type)

  def pop_container(self, container_type):
    container = self.stack[-1]
    if container.type != container_type:
      raise SyntaxError("incomplete-%s" % container.type)
    self.stack = self.stack[:-1]

  def push_container(self, object_type, token):
    parent = self.get_last_container()
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

    return node
