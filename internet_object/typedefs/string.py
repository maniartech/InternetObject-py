import re

from internet_object.utils import helpers
from core import parse, InternetObject, errors
from .typedef import TypeDef

class StringDef (TypeDef):

  definition = InternetObject.parse(r"""
                type        : { name:type, type:string, default:string, choices:{ type:array, of:string } },
                default     : { name:default, type:string, optional:T },
                choices     : { name:choices, type:array, of:string, optional:T },
                minLen      : { name:minLen, type:int, min:0, optional:T },
                maxLen      : { name:maxLen, type:int, min:0, optional:T },
                len         : { name:len, type:int, min:0, optional:T },
                pattern     : { name:pattern, type:string, min:T, optional:T },
                optional    : { name:optional, type:bool, default:F },
                "null"      : { name:"null", type:bool, default:F }
              """)

  def __init__(self, typename='string'):
    self.typename = typename

  def validate(self, val, memberDef):
    if hasattr(memberDef, "minLen"):
      if len(val) < memberDef.minLen:
        return False, "minLen"

    if hasattr(memberDef, "maxLen"):
      if len(val) > memberDef.maxLen:
        return False, "maxLen"

    if hasattr(memberDef, "len"):
      if len(val) == memberDef.len:
        return False, "len"

    if hasattr(memberDef, "pattern"):
      return True, None

    return True, None
