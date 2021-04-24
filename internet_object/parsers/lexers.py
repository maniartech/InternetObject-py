import re

from .regexes import *
from .tokens import Token

escapables = ['"', 'b', 'f', 'r', 'n', 't']

escape_map = {
  '"': '"',
  'b': '\b',
  'f': '\f',
  'r': '\r',
  'n': '\n',
  't': '\t',
}


class Lexer():
  """
  Lexer helps parsing internet object text into tokens.
  """

  def __init__(self, text):
    self._index = -1
    self._text = text
    self._done = False
    self._col = 0
    self._row = 0
    self._tokens = []
    self._len = len(text)
    self.val = None
    self.advance()

  @property
  def done(self):
    return self._done

  def read_all(self):
    token = self.read()

    while(self._done is not True):
      if token:
        self._tokens.append(token)
      token = self.read()

    if self._done and token:
      self._tokens.append(token)

  @property
  def tokens(self):
    return self._tokens

  def print_tokens(self):
    for token in self._tokens:
      print('-', token)

  def read(self):

    if self._done is True:
      return

    self.val = None

    ch = self._ch
    ch_code = self._ch_code

    # print("+++", repr(ch), self._index)
    should_advance = False
    token = None

    # Validators

    is_datasep = False
    if ch == '-':
      is_datasep = self.is_datasep

    # Scanner and Processor
    if ch_code <= 32:
      self.scan('ws',
                lambda a, b: self._ch_code <= 32,
                True)

    # Scan regular string
    elif ch == '"':
      self.val = ""
      token = self.scan("string", self.regular_string_scanner, confined=True)
      self.advance()

    # Scan raw string
    elif ch == "'":
      self.val = ""
      token = self.scan("string", self.raw_string_scanner, confined=True)
      self.advance()

    elif ch == '#':
      token = self.scan('comment', self.comment_scanner)

    elif is_datasep:
      token = Token("---", "datasep", "---", self._index,
                    self._index + 3, self._row, self._col)
      self.advance(3)

    # Process separator
    elif re_separator.match(ch):
      # self._index += 1
      token = Token(ch, 'sep', ch, self._index,
                    self._index, self._row, self._col)
      self.advance()

    else:
      # Scan everything else
      token = self.scan("string", self.sep_scanner)
      value, token_type = self.process_open_values(token.token)
      token.val = value
      token.type = token_type

    return token

  def ws_scanner(self, start, end):
    return self._ch_code <= 32

  def advance(self, times=1):
    advanced = 1
    try:
      self._ch = self._text[self._index+1]
      self._ch_code = ord(self._ch)

      self._index += 1
      self._col += 1

      if self._ch == '\n':
        self._col = 1
        self._row += 1

      result = True
      while advanced < times:
        result = self.advance()
        advanced += 1

      return result

    except IndexError:  # End of the text
      self._ch = None
      self._ch_code = -1
      self._done = True
      self._index = len(self._text) - 1
      return False

  def scan(self, token_type, scanner, confined=False, skip=False):

    start = self._index

    while self.advance():

      # Reached the end of the text, break it
      if self._done is True:
        break

      if scanner(start, self._index) is False:
        break

    token = self._text[start:self._index +
                       (1 if confined or self._done else 0)].strip()
    val = token
    if self.val is not None:
      val = self.val

    return None if skip else (Token(token, token_type, val,
                                    start, start + len(token)-1, self._row, self._col))

  # Validators, Scanners and Processors
  @property
  def is_datasep(self):
    start = self._index
    end = self._index + 3
    try:
      token = self._text[start:end]
      next_ch = self._text[start+3]
      return token == "---" and next_ch != "-"

    except IndexError:
      return False

  def regular_string_scanner(self, start, end):
    ch = self._ch

    # Handle escapes
    if ch == "\\":
      try:
        next = self._text[self._index+1]
        # check if
        if next in escapables:
          self.val += escape_map[next]
          self.advance(1)

        elif next in ('x', 'X'):
          pass

        elif next in ('U', 'u'):
          pass

      except (IndexError):
        return True

    elif ch != '"':
      # Last char reached without closing the regular string!
      if self._index == self._len - 1:
        raise SyntaxError("incomplete-string (%s, %s)" %
                          (self._row, self._col,))
      self.val += ch
      return True

    if ch == '"':
      return False

    return True

  def raw_string_scanner(self, start, end):
    if self._ch != "'":
      if self._index == self._len - 1:
        raise SyntaxError("incomplete-string (%s, %s)" %
                          (self._row, self._col,))
      self.val += self._ch
      return True


    # If next ch is ' too, ignore it
    try:
      next_ch = self._text[self._index+1]
      if next_ch == "'":
        self.val += "'"
        self.advance()
        return True
      return False
    except IndexError:
      return False

    if self._ch == '"':
      return False

    return True

    token = self._text[start:self._index+1]
    return re_raw_string.match(token) is None

  def sep_scanner(self, start, end):
    if re_separator.match(self._ch) is not None:
      return False

    elif self._ch == '#':
      return False

    if self._ch == "-":
      return not self.is_datasep

    return True

  def comment_scanner(self, start, end):
    return self._ch != '\n'

  def process_open_values(self, token):

    if token == 'T' or token == 'true':
      return True, 'bool'

    elif token == 'F' or token == 'false':
      return False, 'bool'

    elif token == 'N' or token == 'null':
      return None, 'null'

    elif re_number.match(token) is not None:
      try:
        return (
            int(token) if re.search(r"[\.eE]", token) is None else float(token)
        ), 'number'
      except ValueError:
        pass

    # Binary number
    elif re_binary.match(token) is not None:
      return int(re_binary.findall(token)[0], 2), 'number'

    # Octal number
    elif re_octal.match(token) is not None:
      return int(re_octal.findall(token)[0], 8), 'number'

    # Hex number
    elif re_hexa.match(token) is not None:
      return int(re_hexa.findall(token)[0], 16), 'number'

    return token, "string"
