from .typedef import *

from .anydefs import AnyDef
from .objectdefs import ObjectDef
from .stringdefs import StringDef
from .numberdefs import NumberDef



from .type_registries import type_registry as registry

# registry.register("any", AnyDef())
registry.register("object", ObjectDef())
registry.register("string", StringDef("string"))
registry.register("number", NumberDef("number"))
registry.register("int", NumberDef("int"))
