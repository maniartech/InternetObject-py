

class Node:

  def __init__(self, value, node_type, start, end, row, col, pos=0, parent=None):

    self.start = start
    self.end = end
    self.row = row
    self.col = col

    self.pos = 0
    self.key = None
    self.value = value
    self.type = node_type

  @classmethod
  def from_token(cls, token, pos=0, parent=None):
    return Node(
        token.value,
        token.type,
        token.start,
        token.end,
        token.row,
        token.col
    )

  def __str__(self):
    return "%s (%s)" % (self.value,
                        self.type)

  def __repr__(self):
    return repr(self.to_dict())

  def to_dict(self):
    return {
        # "start": self.start,
        # "end": self.end,
        # "row": self.row,
        # "col": self.col,
        "pos": self.pos,
        "type": self.type,
        "key": self.key,
        "value": self.value
    }
