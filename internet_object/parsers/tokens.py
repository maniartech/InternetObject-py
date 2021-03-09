

class Token (dict):
  """
  Represents the Internet Object token
  """

  def __init__(self, token, token_type, val, start, end, row, col):
    self.start = start
    """int: The token start"""

    self.end = end
    self.row = row
    self.col = col
    self.type = token_type
    self.token = token  # text[start:end+1]
    self.val = val

  def __setattr__(self, name, value):
    dict.__setitem__(self, name, value)
    return super().__setattr__(name, value)

  def __str__(self):
    return "%s (%s, %s, %s, %s, %s, %s)" % (
        self.type,
        repr(self.val),
        repr(self.token),
        self.start, self.end, self.row, self.col
    )

  def __repr__(self):
    return repr(self.to_dict())

  def to_dict(self):
    return {
        # "start": self.start,
        # "end": self.end,
        # "row": self.row,
        # "col": self.col,
        "type": self.type,
        # "token": self.token,
        "val": self.val
    }
