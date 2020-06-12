

class Node(dict):

  def __init__(self, val, node_type, start, end, row, col, pos=0, parent=None):
    self.type = node_type
    self.pos = 0
    self.start = start
    self.end = end
    self.row = row
    self.col = col

    self.key = None
    self.val = val

  def __setattr__(self, name, value):
    dict.__setitem__(self, name, value)
    return super().__setattr__(name, value)

  @classmethod
  def from_token(cls, token, pos=0, parent=None):
    return Node(
        token.val,
        token.type,
        token.start,
        token.end,
        token.row,
        token.col
    )

  def __str__(self):
    return "%s (%s)" % (self.val,
                        self.type)

  def __repr__(self):
    return repr(self.to_dict())

  def to_dict(self):
    d = {
        "pos": self.pos,
        "type": self.type,
    }

    if self.key is not None:
      d["key"] = self.key

    d["val"] = self.val
    return d
