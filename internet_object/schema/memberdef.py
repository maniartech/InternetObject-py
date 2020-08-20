

class MemberDef(dict):

  def __init__(self, name, def_type, path,
               optional=False,
               null=False,
               default=False, choices=None):

    self.name = name
    self.type = def_type
    self.path = path
    self.optional = optional
    self.null = null
    self.default = default

  def __setattr__(self, name, value):
    dict.__setitem__(self, name, value)
    return super().__setattr__(name, value)


class SchemaDef(dict):

  def __init__(self, def_type, members=[]):
    self.type = def_type
    self.members = members

  def __setattr__(self, name, value):
    dict.__setitem__(self, name, value)
    return super().__setattr__(name, value)
