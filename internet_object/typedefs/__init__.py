from .typedef import *
from .type_registries import registry, schema_registry

from .any import AnyDef
from .object import ObjectDef
from .string import StringDef
from .number import NumberDef

registry.register("any", AnyDef())
registry.register("object", ObjectDef())
registry.register("string", StringDef("string"))
registry.register("number", NumberDef("number"))
registry.register("int", NumberDef("int"))
