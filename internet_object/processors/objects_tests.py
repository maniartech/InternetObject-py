

class IOObject(dict):

  def __init__(self, iterable):
    super().__init__(iterable)



  # Attribute
  def __setattr__(self, name, value):
    dict.__setitem__(self, name, value)
    return super().__setattr__(name, value)

  def __delattr__(self, name):
    dict.__delitem__(self, name)
    return super().__delattr__(name)

  # Items
  def __setitem__(self, name, value):
    dict.__setattr__(self, name, value)
    return super().__setitem__(name, value)

  def __delitem__(self, key):
    dict.__delattr__(self, key)
    return super().__delitem__(key)




