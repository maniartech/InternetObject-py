from tokens import Token
from lexers import Lexer
from nodes import Node


class AST:

  def __init__(self, text):
    self.text = text
    self.lexer = Lexer(text)
    self.last_token = None
    self.token = None
    self.index = 0

    self.stack = []
    self.value_pipe = []

    self.tree = {
        "data": None
    }

  def parse(self):
    lexer = self.lexer
    self.tree["data"] = self.get_or_create_last_container()

    while True:

      if lexer.done:
        break

      token = lexer.read()
      if token is None:
        continue

      self.process(token)

    print("+++", self.tree["data"])

  def get_object(self):
    pass

  def process(self, token):
    if token.type == "sep":
      if token.value == "{":
        self.push_container("object", token)

      elif token.value == "}":
        self.pop_container("object")

      elif token.value == "[":
        self.push_container("array", token)

      elif token.value == "]":
        self.pop_container("array")

      elif token.value == "~":
        self.push_container("collection", token)

      else:
        self.push_value(Node.from_token(token))

    elif token.type == "datasep":
      raise NotImplementedError("not-ready")

    else:
      self.push_value(Node.from_token(token))

  def push_value(self, value):
    is_comma = value.type == "sep" and value.value == ","
    is_collon = value.type == "sep" and value.value == ":"
    pipe = self.value_pipe
    pipe_len = len(pipe)

    container = self.get_or_create_last_container()
    values = container.value
    values_len = len(values)

    try:
      last_value = values[-1]
    except IndexError:
      last_value = None

    if is_comma:
      # When comma is received while pipe is empty
      # push undefined token
      if pipe_len == 0:
        undefined_node = self.get_undefined_node()
        values.append(undefined_node)

      # When value exists in the pipe clear it
      elif pipe_len == 1 or pipe_len == 3:
        pipe.clear()

    elif is_collon:
      # Throw a syntax error
      # When colon is received while pipe is empty,
      if (pipe_len == 0 or
          # When last value in the pipe is colon
          pipe[-1] == ":" or
              # When last value in the pipe is not a string
              pipe[-1].type != "str"):
        # print(pipe)
        raise SyntaxError("unexpected-colon")

      elif pipe_len == 1:
        # Just add the colon
        pipe.append(":")

    else:
      if pipe_len == 0:
        pipe.append(value)
        values.append(value)

      # When the last char in pipe is : setup key-value
      if pipe_len == 2 and pipe[-1] == ":":
        # print("----")
        # print(values)
        # print(last_value)
        last_value.key = last_value.value
        last_value.value = value
        pipe.append(value)

  def pop_container(self, container_type):
    container = self.stack[0]
    self.stack = self.stack[1:]

  def push_container(self, object_type, token):
    parent = self.get_last_container()
    pos = parent.pos + 1 if parent is not None else 0
    node = Node([], object_type, token.start,
                token.end, token.row, token.col, pos, parent)

    self.push_value(node)
    self.stack.append(node)

  def get_undefined_node(self, parent=None):
    index = 0 if parent is None else len(parent.value)
    return Node(None, "undefined", 0, 0, 1, 1, 0, parent)

  def get_value_node(self, token, parent=None):
    index = 0 if parent is None else len(parent.value)
    return Node(token.value, token.type, token.start,
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
