from .typedef import *
from .type_registries import registry, schema_registry

from .any import AnyDef
from .object import ObjectDef
from .string import StringDef
from .number import NumberDef

# registry.register("any", AnyDef())
registry.register("object", ObjectDef())
registry.register("string", StringDef("string"))
registry.register("number", NumberDef("number"))
registry.register("int", NumberDef("int"))


schema_registry.register("object", ObjectDef())
schema_registry.register("string", StringDef("string"))
schema_registry.register("number", NumberDef("number"))
schema_registry.register("int", NumberDef("int"))
