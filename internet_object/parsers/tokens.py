

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
    self.token = token  # text[start:end+1]

  def __str__(self):
    return "%s (%s, %s, %s, %s, %s)" % (
        repr(self.token),
        self.type,
        self.start, self.end, self.row, self.col
    )
