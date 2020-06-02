import re
import regexes

from tokens import Token


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
    self.advance()
    self._len = len(text)

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

    ch = self._ch
    ch_code = self._ch_code

    print("+++", repr(ch), self._index)
    should_advance = False
    token = None

    # Validators

    is_datasep = False
    if ch == '-':
      is_datasep = self.is_datasep

    # Scanner and Processor
    if ch_code <= 32:
      self.scan('ws',
                lambda a, b: self._ch_code > 32,
                True)

    # Scan regular string
    elif ch == '"':
      token = self.scan("str", self.string_stopper, confined=True)
      self.advance()

    # Scan raw string
    # elif ch == "'":
    #   token = self.scan("str", self.string_stopper, confined=True)
    #   self.advance()

    elif is_datasep:
      token = Token("---", "datasep", self._index,
                    self._index + 3, self._row, self._col)
      self.advance()
      self.advance()
      self.advance()

    # Process separator
    elif re.match(regexes.separator, ch):
      # self._index += 1
      token = Token(ch, 'sep', self._index,
                    self._index, self._row, self._col)
      self.advance()

    else:
      # Scan everything else
      token = self.scan("str", self.sep_stopper)

    return token

  def ws_scanner(self, start, end):
    return self._ch_code <= 32

  def advance(self):
    try:
      self._index += 1
      self._ch = self._text[self._index]
      self._ch_code = ord(self._ch)

      self._col += 1

      if self._ch == '\n':
        self._col = 1
        self._row += 1

      return True

    except IndexError:  # End of the text
      self._ch = None
      self._ch_code = -1
      self._done = True
      self._index = len(self._text) - 1
      return False

  def get_char(self, index):
    try:
      ch = self._text[index]
      ch_code = ord(ch)

      return ch, ch_code

    except IndexError as aer:
      return None, -1

  def get_phrase(self, start, end):
    try:
      phrase = self._text[start:end]
      return phrase

    except IndexError as aer:
      return None

  def scan(self, token_type, stopper, confined=False, skip=False):

    start = self._index
    end = start

    stopped = False

    while self.advance():

      # Reached the end of the text, break it
      if self._done is True:
        break
      if stopper(start, self._index) is True:
        stopped = True
        break

      if self._ch_code > 32:
        end = self._index+1

    end = end + (1 if confined else 0)
    token = self._text[start] if start == end else self._text[start:end]

    return None if skip else (Token(token, token_type,
                                    start, self._index, self._row, self._col))

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

  def string_stopper(self, start, end, scan_finished=False):
    if self._ch != '"':
      if self._index == self._len - 1:
        raise SyntaxError("incomplete-string (%s, %s)" %
                          (self._row, self._col,))

      return False
    token = self._text[start:end+1]
    # print(repr(self._ch), repr(token), regexes.regular_string.match(token) is not None)
    return regexes.regular_string.match(token) is not None

  def sep_stopper(self, start, end):
    if regexes.separator.match(self._ch) is not None:
      return True

    if self._ch == "-":
      return self.is_datasep

    return False
