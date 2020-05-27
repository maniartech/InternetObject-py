import re
import json

# from .token import Token

class Token:
    """
    Represents the Internet Object token
    """

    def __init__(self, token, token_type, start, end, row, col):

        self.start = start
        """int: The token start"""

        self.end = end
        self.row = row
        self.col = col
        self.type = token_type
        self.token = token # text[start:end+1]

    def __str__(self):
      return "%s (%s, %s, %s, %s, %s)" % (
        repr(self.token),
        self.type,
        self.start, self.end, self.row, self.col
      )


class Tokenizer():
  """
  Tokenizer helps parsing internet object text into tokens.
  """

  def __init__(self, text):
    self._index = 0
    self._tokens = []
    self._text = text

  def read_all(self):
    final, token = self.read()
    while(final is not True):
      if token:
        self._tokens.append(token)
      final, token = self.read()

    if final and token:
      self._tokens.append(token)

  @property
  def tokens(self):
    return self._tokens


  def print_tokens(self):
    for token in self._tokens:
      print('-', token)


  def read(self):
    text = self._text
    index = self._index

    ch, ch_code = self.get_char(self._index)
    next_ch, _ = self.get_char(self._index + 1)

    if ch is None:
      return True, None

    print("+++", repr(ch), index)

    is_last = next_ch is None

    # Scan white spaces
    if ch_code <= 32:
      return self.scan(index, r'[\s]', 'WS', need_token = False)

    # Scan regular string
    elif ch == '"':
      return self.scan_phrase(index, r"^\"(?:[^\"\\]|\\.)*\"$", "string")

    # Process separator
    elif re.search('[\{\}\[\]\:\,]', ch):
      self._index += 1
      return is_last, Token(ch, 'sep', index, index, -1, -1 )

    # Scan everything else
    return self.scan(index, r'[^\{\}\[\]\:\,]', 'string')

  def get_char(self, index):
    try:
      ch = self._text[index]
      ch_code = ord(ch)

      return ch, ch_code

    except IndexError as aer:
      return '', -1

  def get_phrase(self, start, end):
    try:
      phrase = self._text[start:end]
      return phrase

    except IndexError as aer:
      return None


  def get_token(self, text, value, start, end, row, col):
    pass


  def scan(self, index, exp, token_type, max=None, need_token=True):
    text = self._text
    start = index
    last = index
    count = 1

    ch, ch_code = self.get_char(self._index)
    is_ws = ch_code <= 32 and ch_code > -1

    while ch_code != -1 and  count <= max if max is not None else True:

      matched = re.search(exp, ch) is not None # experssion has matched

      # print(self._index, repr(ch), matched, ch_code, is_ws, last)

      if not matched:
        # token = text[start:last]
        return False, Token(text[start:last+1], token_type, start, last-1, -1, -1) if need_token else None

      self._index += 1
      ch, ch_code = self.get_char(self._index)

      # Reached the end of the text, break it
      if ch_code == -1:
        break

      count += 1
      is_ws = ch_code <= 32
      if not is_ws:
        last = self._index

    return True, Token(text[start:last+1], token_type, start, last, -1, -1) if need_token else None

  def scan_phrase(self, index, exp, token_type):
    text = self._text
    start = self._index
    last = start + 1
    count = 0

    # Loop until phrase is not matched
    while(True):
      phrase = self.get_phrase(start, last)
      matched = re.search(exp, phrase) is not None

      print(">>>", repr(phrase), start, last, self._index)

      count += 1
      last += 1
      self._index += 1

      if matched:
        break

      # if count == 10:
      #   break


    # print(phrase, matched, start, self._index)

    if not matched:
      raise SyntaxError()

    is_last = self._index == len(text) - 1
    return is_last, Token(phrase, token_type, start, last-2, -1, -1)











