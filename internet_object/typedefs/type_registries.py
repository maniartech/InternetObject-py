from internet_object.utils.singletons import Singleton


class TypeRegistry(Singleton):

  def __init__(self):
    # The type registry
    self.__registry = {}
    self.__types = []

  def register(self, typename, typedef):
    if typename in self.__registry:
      return

    self.__registry[typename] = typedef
    self.__types.append(typename)

  def all_types(self):
    return self.__types[:]

  def all_typedefs(self):
    return [self.__registry[type_] for type_ in self.__types]

  def is_datatype(self, typename):
    return typename in self.__registry

  def get_typedef(self, typename):
    return self.__registry.get(typename, None)



registry = TypeRegistry()
schema_registry = TypeRegistry()
