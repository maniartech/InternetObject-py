

class DictList():

  def __init__(self):
    self.__dict = {}
    self.__list = []


  def append(self, value, key=None):
    self.__list.append(value)
    if key is not None:
      self.__dict[key] = value


  def __getattribute__(self, name):
    return self.__dict.get(name)


  def __repr__(self):
    return self._list




  # # Attribute
  # def __setattr__(self, name, value):
  #   dict.__setitem__(self, name, value)
  #   return super().__setattr__(name, value)

  # def __delattr__(self, name):
  #   dict.__delitem__(self, name)
  #   return super().__delattr__(name)

  # # Items
  # def __setitem__(self, name, value):
  #   dict.__setattr__(self, name, value)
  #   return super().__setitem__(name, value)

  # def __delitem__(self, key):
  #   dict.__delattr__(self, key)
  #   return super().__delitem__(key)