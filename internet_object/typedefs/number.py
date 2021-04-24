import re

from internet_object.utils import is_scalar
from internet_object.core import parse, InternetObject, errors
from .common import clean
from .typedef import TypeDef

class NumberDef (TypeDef):

  definition = InternetObject.parse(r"""
                type        : { name:type, type:string, default:string, choices:[number, int, int32, int16, byte] },
                default     : { name:default, type:number, optional:T },
                # choices     : { name:choices, type:array, of:number, optional:T },
                min         : { name:min, type:int, min:0, optional:T },
                max         : { name:max, type:int, min:0, optional:T },
                optional    : { name:optional, type:bool, default:F},
                "null"      : { name:"null", type:bool, default:F}
                """)

  def __init__(self, typename='number'):
    self.typename = typename

  # def parse(self, node, memberDef):
  #   val, is_final = clean(node, memberDef)

  #   if is_final:
  #     return val

  #   is_valid, reason = self.validate(val, memberDef)
  #   if is_valid is False:
  #     raise errors.ValidationError(
  #       "validation-failed (string.%s) for %s at %s,%s" % (
  #         reason, node.path, node.row, node.col
  #       )
  #     )

  #   return val

  def validate(_, val, memberDef):
    if hasattr(memberDef, "min"):
      if val < memberDef.min:
        return False, "min"

    if hasattr(memberDef, "max"):
      if val > memberDef.max:
        return False, "max"

    return True, None

