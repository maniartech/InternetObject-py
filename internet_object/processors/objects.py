from collections.abc import MutableMapping




class IOObject (MutableMapping):
  """
  Represents the Internet Object.
  """

  def __init__(self, o=None):
    self.__dict__["_IOObject__keys"] = []
    super().__init__()

    if o is not None:
      for key in o.keys():
        self[key] = o[key]

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
    return self.__dict__[key]

  def __setattr__(self, key_index, value):
    self.__setitem__(key_index, value)

  def __delattr__(self, key_index):
    self.__delitem__(key_index)

  def __iter__(self):
    for key in self.__keys:
      yield key, self.__dict__[key]

  def fields(self):
    for index in range(self.__len__()):
      key = self.__keys[index]
      yield IOObject({
        "key": key,
        "index": index,
        "val": self.__dict__[key]
      })

  def __len__(self):
    return len(self.__keys)

  # Members

  def has_key(self, key):
    return hasattr(self.__dict__, key)

  def get_key(self, key_index):
    return self.__keys[key_index] if isinstance(key_index, int) else key_index

  def index(self, key):
    return self.__keys.index(key)

  def append(self, value, key=None):
    index = len(self.__keys)
    key = key or str(index)

    self.__keys.append(key)
    print(">>>", key, value)
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
    return { k:v for k, v in self }
