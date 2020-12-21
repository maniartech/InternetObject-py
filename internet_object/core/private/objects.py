from collections.abc import MutableMapping
from . import parser


class InternetObject (MutableMapping):
  """
  Represents the Internet Object.
  """

  def __init__(self, o=None):
    self.__dict__["_InternetObject__keys"] = []
    super().__init__()

    if o is not None:
      self.update(o)

  def __getitem__(self, key_index):
    key = self.get_key(key_index)
    return self.__dict__[key]

  def __setitem__(self, key_index, value):
    key = self.get_key(key_index)
    if key in self:
      self.__dict__[key] = value
    else:
      self.append(value, key)

  def __delitem__(self, key_index):
    key = self.get_key(key_index)
    index = self.index(key)

    del self.__keys[index]
    del self.__dict__[key]

  def __getattr__(self, key_index):
    key = self.get_key(key_index)
    if key in self.__dict__:
      return self.__dict__[key]

    raise AttributeError("%r object has no attribute %r" %
                             (self.__class__.__name__, key))

  def __setattr__(self, key_index, value):
    self.__setitem__(key_index, value)

  def __delattr__(self, key_index):
    self.__delitem__(key_index)

  def __iter__(self):
    for index, key in enumerate(self.__keys):
      yield index, key, self.__dict__[key]

  def __len__(self):
    return len(self.__keys)

  @staticmethod
  def from_list(l):
    o = InternetObject()
    for item in l:
      item_len = len(item)
      if item_len == 1:
        if isinstance(item, list) or isinstance(item, tuple):
          o.append(InternetObject.from_list(item))
        else:
          o.append(item)
      elif item_len == 2:
        val = item[0]
        key = item[1]
        if isinstance(key, str):
          if isinstance(val, list) or isinstance(val, tuple):
            o.append(InternetObject.from_list(val), key)
          else:
            o.append(val, key)
        else:
          raise ValueError("invalid-key")
      else:
        raise ValueError("invalid-item")
    return o

  @staticmethod
  def parse(ostr, defs=None):
    if isinstance(ostr, str) is False:
      raise TypeError('string-expted')

    return parser.parse(ostr, defs=defs)

  # Members
  def fields(self):
    for index in range(self.__len__()):
      key = self.__keys[index]
      yield InternetObject({
        "key": key,
        "index": index,
        "val": self.__dict__[key]
      })

  def get(self, key_index, default=None):
    key = self.get_key(key_index)
    # print("+++", key)
    if self.has_key(key):
      return self.__dict__[key]
    return default

  def has_key(self, key):
    return key in self.__dict__

  def get_key(self, key_index):
    return self.__keys[key_index] if isinstance(key_index, int) else key_index

  def index(self, key):
    return self.__keys.index(key)

  def append(self, value, key=None):
    index = len(self.__keys)
    key = key or str(index)

    self.__keys.append(key)
    self.__dict__[key] = value

  def values(self):
    return [self.__dict__[key] for key in self.__keys]

  def keys(self):
    return self.__keys[:]

  def __repr__(self):
    return repr(self.to_dict())

  def to_json(self):
    return self.to_dict()

  def to_dict(self):
    return { k:v for _, k, v in self }

